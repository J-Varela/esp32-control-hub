import csv

from app.main import DATA_PATH
from app.storage import CSVTelemetryStore

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "esp32-control-hub"
    }

def test_latest_telemetry(tmp_path, monkeypatch):
    path = tmp_path / "telemetry.csv"

    store = CSVTelemetryStore(path)
    store.append({
        "timestamp": "2026-10-16T04:00:00+00:00",
        "uptime_seconds": 120,
        "free_memory_bytes": 124496,
        "wifi_connected": True,
        "wifi_rssi": -51
    })

    monkeypatch.setattr("app.main.DATA_PATH", path)

    response = client.get("/api/telemetry/latest")

    assert response.status_code == 200

    data = response.json()

    assert data["uptime_seconds"] == 120
    assert data["free_memory_bytes"] == 124496
    assert data["wifi_connected"] is True
    assert data["wifi_rssi"] == -51


def test_latest_telemetry_missing(tmp_path, monkeypatch):
    path = tmp_path / "missing.csv"

    monkeypatch.setattr("app.main.DATA_PATH", path)

    response = client.get("/api/telemetry/latest")

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "No telemetry data available"
    )


def test_telemetry_history(tmp_path, monkeypatch):
    path = tmp_path / "history.csv"
    store = CSVTelemetryStore(path)

    for index in range(5):
        store.append({
            "timestamp": f"2026-10-16T00:00:{index:02d}+00:00",
            "uptime_seconds": index,
            "free_memory_bytes": 124000,
            "wifi_connected": True,
            "wifi_rssi": -50 - index
        })

    monkeypatch.setattr("app.main.DATA_PATH", path)

    response = client.get(
        "/api/telemetry/history?limit=3"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert len(data["samples"]) == 3
    assert data["samples"][0]["uptime_seconds"] == 2
    assert data["samples"][-1]["uptime_seconds"] == 4


def test_telemetry_history_invalid_limit():
    response = client.get(
        "/api/telemetry/history?limit=0"
    )

    assert response.status_code == 400



def test_telemetry_history_chronological(tmp_path, monkeypatch):
    path = tmp_path / "history.csv"
    store = CSVTelemetryStore(path)

    timestamps = [
        "2026-10-16T05:46:36+00:00",
        "2026-10-16T05:46:30+00:00",
        "2026-10-16T05:46:34+00:00",
    ]

    for index, timestamp in enumerate(timestamps):
        store.append({
            "timestamp": timestamp,
            "uptime_seconds": index,
            "free_memory_bytes": 124496,
            "wifi_connected": True,
            "wifi_rssi": -52,
        })

    monkeypatch.setattr("app.main.DATA_PATH", path)

    response = client.get("/api/telemetry/history")

    assert response.status_code == 200

    samples = response.json()["samples"]

    returned_timestamps = [
        sample["timestamp"] for sample in samples
    ]

    assert returned_timestamps == sorted(timestamps)



def test_latest_telemetry_uses_newest_timestamp(
    tmp_path, monkeypatch
):
    path = tmp_path / "telemetry.csv"
    store = CSVTelemetryStore(path)

    for timestamp, uptime in [
        ("2026-10-16T05:46:36+00:00", 300),
        ("2026-10-16T05:46:30+00:00", 294),
    ]:
        store.append({
            "timestamp": timestamp,
            "uptime_seconds": uptime,
            "free_memory_bytes": 124496,
            "wifi_connected": True,
            "wifi_rssi": -52,
        })

    monkeypatch.setattr("app.main.DATA_PATH", path)

    response = client.get("/api/telemetry/latest")

    assert response.status_code == 200
    assert response.json()["uptime_seconds"] == 300

