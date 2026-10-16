
from app.history import collect_history


class FakeCollector:
    def collect(self):
        return {
            "uptime_seconds": 100,
            "free_memory_bytes": 124496,
            "wifi_connected": True,
            "wifi_rssi": -55,
        }


def test_history_appends_across_runs(tmp_path):
    path = tmp_path / "history.csv"
    collector = FakeCollector()

    collect_history(
        collector, path, samples=2, interval=0
    )

    collect_history(
        collector, path, samples=2, interval=0
    )

    lines = path.read_text().splitlines()

    assert len(lines) == 5
    assert lines[0].startswith("timestamp,")
    assert sum(
        line.startswith("timestamp,") for line in lines
    ) == 1


def test_history_rejects_invalid_samples(tmp_path):
    path = tmp_path / "history.csv"

    try:
        collect_history(
            FakeCollector(), path, samples=0
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

    assert not path.exists()
