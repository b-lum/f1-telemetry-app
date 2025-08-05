from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telemetry import get_latest_telemetry
import random

app = FastAPI()

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
    return {"speed": random.randint(0, 400), "throttle": round(random.uniform(0, 1), 2), "brake": round(random.uniform(0, 1), 2)}
