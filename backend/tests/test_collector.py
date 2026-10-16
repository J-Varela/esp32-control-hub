
import json
import sys
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from app.collector import TelemetryCollector


class FakeResponse:
    def __init__(self, data):
        self.data = BytesIO(json.dumps(data).encode())

    def read(self, size=-1):
        return self.data.read(size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.data.close()


def test_collect_telemetry():
    sample = {
        "uptime_seconds": 120,
        "free_memory_bytes": 124704,
        "wifi_connected": True,
        "wifi_rssi": -51
    }

    with patch(
        "app.collector.urlopen",
        return_value=FakeResponse(sample)
    ) as mock_urlopen:
        collector = TelemetryCollector(
            "http://192.168.1.238/"
        )

        result = collector.collect()

    assert result == sample

    mock_urlopen.assert_called_once_with(
        "http://192.168.1.238/api/system",
        timeout=3
    )


def test_custom_timeout():
    sample = {
        "uptime_seconds": 10,
        "free_memory_bytes": 100000,
        "wifi_connected": True,
        "wifi_rssi": -60
    }

    with patch(
        "app.collector.urlopen",
        return_value=FakeResponse(sample)
    ) as mock_urlopen:
        collector = TelemetryCollector(
            "http://192.168.1.238",
            timeout=5
        )

        collector.collect()

    assert mock_urlopen.call_args.kwargs["timeout"] == 5
