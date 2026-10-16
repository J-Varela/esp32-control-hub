from app.poller import poll_once


class FakeCollector:
    def collect(self):
        return {
            "uptime_seconds": 100,
            "free_memory_bytes": 124496,
            "wifi_connected": True,
            "wifi_rssi": -55,
        }


class FakeStore:
    def __init__(self):
        self.records = []

    def append(self, record):
        self.records.append(record)


def test_poll_once_saves_telemetry():
    collector = FakeCollector()
    store = FakeStore()

    result = poll_once(collector, store)

    assert len(store.records) == 1
    assert store.records[0] == result
    assert result["uptime_seconds"] == 100
    assert result["wifi_rssi"] == -55
    assert "timestamp" in result
