
from app.storage import CSVTelemetryStore


def test_append_and_read(tmp_path):
    path = tmp_path / "telemetry.csv"
    store = CSVTelemetryStore(path)

    record = {
        "timestamp": "2026-10-15T12:00:00+00:00",
        "uptime_seconds": 100,
        "free_memory_bytes": 124496,
        "wifi_connected": True,
        "wifi_rssi": -57,
    }

    store.append(record)
    store.append(record)

    rows = store.read_all()

    assert len(rows) == 2
    assert rows[0]["uptime_seconds"] == "100"
    assert rows[0]["wifi_rssi"] == "-57"


def test_missing_file(tmp_path):
    store = CSVTelemetryStore(
        tmp_path / "missing.csv"
    )

    assert store.read_all() == []
