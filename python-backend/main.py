from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telemetry import get_latest_telemetry, get_session_id
from telemetry_objects import Session, Lap, Telemetry_data
import random

app = FastAPI()


sessions = {}

#Session(get_session_id)
#print(session.session_id)

# Let frontend (localhost:5173) access backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:5173"] later for React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/telemetry")
def telemetry():
    data = get_latest_telemetry()
    if data:
        return data
    return {"speed": 0.0, "throttle": 0.0, "brake": 0.0}
    # return {"speed": random.randint(0, 400), "throttle": round(random.uniform(0, 1), 2), "brake": round(random.uniform(0, 1), 2)}
