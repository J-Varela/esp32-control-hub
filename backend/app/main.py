import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from threading import Event, Thread

from app.collector import TelemetryCollector
from app.poller import run_polling
from app.storage import CSVTelemetryStore



@asynccontextmanager
async def lifespan(app):
    device_url = os.environ.get(
        "ESP32_DEVICE_URL",
        "http://192.168.1.238"
    )

    interval = 5
    stop_event = Event()

    collector = TelemetryCollector(device_url)
    store = CSVTelemetryStore(DATA_PATH)

    worker = Thread(
        target=run_polling,
        args=(collector, store),
        kwargs={
            "interval": interval,
            "stop_event": stop_event,
        },
        daemon=True,
    )

    worker.start()
    print("Telemetry polling started")

    try:
        yield
    finally:
        stop_event.set()
        worker.join(timeout=interval + 5)
        print("Telemetry polling stopped")


app = FastAPI(
    title="ESP32 Control Hub API",
    version="0.1.0",
    lifespan=lifespan,
)

DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "telemetry"
    / "esp32_history.csv"
)

DATA_PATH = Path(
    os.environ.get("ESP32_TELEMETRY_PATH", str(DEFAULT_DATA_PATH))
)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "esp32-control-hub"
    }


@app.get("/api/telemetry/latest")
def latest_telemetry():
    store = CSVTelemetryStore(DATA_PATH)
    records = store.read_all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No telemetry data available"
        )

    latest = max(
        records,
        key=lambda row: row["timestamp"]
    )

    return {
        "timestamp": latest["timestamp"],
        "uptime_seconds": int(latest["uptime_seconds"]),
        "free_memory_bytes": int(latest["free_memory_bytes"]),
        "wifi_connected": latest["wifi_connected"] == "True",
        "wifi_rssi": (
            int(latest["wifi_rssi"])
            if latest["wifi_rssi"] else None
        )
    }



@app.get("/api/telemetry/history")
def telemetry_history(limit: int = 100):
    if not 1 <= limit <= 1000:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 1000"
        )

    store = CSVTelemetryStore(DATA_PATH)
    records = store.read_all()

    records.sort(key=lambda row: row["timestamp"])
    recent = records[-limit:]

    return {
        "count": len(recent),
        "samples": [
            {
                "timestamp": row["timestamp"],
                "uptime_seconds": int(row["uptime_seconds"]),
                "free_memory_bytes": int(row["free_memory_bytes"]),
                "wifi_connected": row["wifi_connected"] == "True",
                "wifi_rssi": (
                    int(row["wifi_rssi"])
                    if row["wifi_rssi"] else None
                )
            }
            for row in recent
        ]
    }
