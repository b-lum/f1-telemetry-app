import os
import asyncio
import asyncpg
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from telemetry import get_next_packet
from telemetry_objects import Session, Lap, Telemetry_data

# Load environment variables
load_dotenv()

app = FastAPI()

#DATABASE_URL = os.getenv("DATABASE_URL")

# State
sessions = {}
latest_session_time = None
#db_pool = None

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup
@app.on_event("startup")
async def startup():
    #global db_pool
    #db_pool = await asyncpg.create_pool(DATABASE_URL)
    print("Database pool created")

# Shutdown
@app.on_event("shutdown")
async def shutdown():
    #await db_pool.close()
    print("Database pool closed")

# DB save helper
async def save_telemetry_to_db(telemetry: Telemetry_data):
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO telemetry (speed, throttle, brake, telemetry_time)
            VALUES ($1, $2, $3, $4)
            """,
            telemetry.speed, telemetry.throttle, telemetry.brake, str(telemetry.time),
        )

# Telemetry generator
async def telemetry_generator(websocket: WebSocket):
    global latest_session_time
    await websocket.accept()

    try:
        while True:
            packet = get_next_packet()
            if not packet:
                await asyncio.sleep(0.01)
                continue

            session_id = packet.header.sessionUID
            if session_id not in sessions:
                sessions[session_id] = Session(session_id)

            # ---- Motion packet (wheel slip) ----
            if packet.header.packetId == 0:
                # Packet gives wheelSlip in F1 UDP order: [RL, RR, FL, FR]
                await websocket.send_json({
                    "packetType": "motion",
                    "wheelSlip": list(packet.wheelSlip)
                })

            # ---- Lap data ----
            elif packet.header.packetId == 2:
                player_idx = packet.header.playerCarIndex
                lap_data = packet.lapData[player_idx]
                latest_session_time = lap_data.currentLapTime

                # Send to frontend
                await websocket.send_json({
                    "packetType": "lapData",
                    "currentLapTime": lap_data.currentLapTime,
                    "currentLapNum": lap_data.currentLapNum,
                    "lastLapTime": lap_data.lastLapTime
                })

                # Update session/lap objects
                if lap_data.currentLapNum not in sessions[session_id].laps:
                    sessions[session_id].add_lap(Lap(lap_data.currentLapNum))
                    if lap_data.currentLapNum - 1 in sessions[session_id].laps:
                        sessions[session_id].laps[lap_data.currentLapNum - 1].set_lap_time(
                            lap_data.lastLapTime
                        )
                sessions[session_id].laps[lap_data.currentLapNum].set_lap_time(
                    lap_data.currentLapTime
                )

            # ---- Car telemetry ----
            elif packet.header.packetId == 6:
                telemetry_time = latest_session_time or 0
                car = packet.carTelemetryData[packet.header.playerCarIndex]
                telemetry_obj = Telemetry_data(
                    telemetry_time,
                    car.throttle,
                    car.brake,
                    car.speed
                )

                recent_lap = sessions[session_id].most_recent_lap
                if recent_lap:
                    recent_lap.add_data(telemetry_obj)

                # Send telemetry to frontend
                await websocket.send_json({
                    "packetType": "carTelemetry",
                    "speed": telemetry_obj.speed,
                    "throttle": telemetry_obj.throttle,
                    "brake": telemetry_obj.brake,
                    "time": telemetry_obj.time
                })

            await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        print("WebSocket client disconnected")


@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await telemetry_generator(websocket)
