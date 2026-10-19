from app.poller import poll_once, run_polling


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


class FlakyCollector:
    """Simulate an ESP32 that fails once, then recovers."""

    def __init__(self):
        self.attempts = 0

    def collect(self):
        self.attempts += 1

        if self.attempts == 1:
            raise TimeoutError("ESP32 not responding")

        return {
            "uptime_seconds": 105,
            "free_memory_bytes": 124000,
            "wifi_connected": True,
            "wifi_rssi": -57,
        }


class StopAfterTwoPolls:
    """Avoid real delays during testing."""

    def __init__(self):
        self.cycles = 0

    def is_set(self):
        return self.cycles >= 2

    def wait(self, interval):
        self.cycles += 1
        return self.is_set()


def test_polling_recovers_after_device_failure():
    collector = FlakyCollector()
    store = FakeStore()
    stop_event = StopAfterTwoPolls()

    run_polling(
        collector,
        store,
        interval=0.01,
        stop_event=stop_event,
    )

    assert collector.attempts == 2
    assert len(store.records) == 1
    assert store.records[0]["uptime_seconds"] == 105
    assert store.records[0]["wifi_rssi"] == -57
