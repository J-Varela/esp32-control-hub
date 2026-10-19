
import json
import sys
import pytest
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


@pytest.mark.parametrize(
    "field,value",
    [
        ("uptime_seconds", -1),
        ("free_memory_bytes", "unknown"),
        ("wifi_connected", 1),
        ("wifi_rssi", None),
        ("wifi_rssi", 100),
    ],
)
def test_rejects_invalid_telemetry(field, value):
    sample = {
        "uptime_seconds": 120,
        "free_memory_bytes": 124704,
        "wifi_connected": True,
        "wifi_rssi": -55,
    }

    sample[field] = value

    with patch(
        "app.collector.urlopen",
        return_value=FakeResponse(sample),
    ):
        collector = TelemetryCollector(
            "http://192.168.1.238"
        )

        with pytest.raises(ValueError):
            collector.collect()


def test_accepts_disconnected_wifi():
    sample = {
        "uptime_seconds": 120,
        "free_memory_bytes": 124704,
        "wifi_connected": False,
        "wifi_rssi": None,
    }

    with patch(
        "app.collector.urlopen",
        return_value=FakeResponse(sample),
    ):
        collector = TelemetryCollector(
            "http://192.168.1.238"
        )

        result = collector.collect()

    assert result == sample
