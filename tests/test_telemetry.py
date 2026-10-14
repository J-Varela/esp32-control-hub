
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from telemetry import DeviceTelemetry


class FakeWiFi:
    def __init__(self, connected=True, rssi=-55):
        self.connected = connected
        self.rssi = rssi

    def isconnected(self):
        return self.connected

    def status(self, key):
        if key == "rssi":
            return self.rssi
        raise ValueError("Unknown status key")


def test_telemetry_connected():
    wifi = FakeWiFi()

    with patch("telemetry.time.ticks_ms",
               side_effect=[1000, 6000], create=True), \
         patch("telemetry.time.ticks_diff",
               return_value=5000, create=True), \
         patch("telemetry.gc.mem_free",
               return_value=80000, create=True):

        telemetry = DeviceTelemetry(wifi)
        result = telemetry.get_status()

    assert result["uptime_seconds"] == 5
    assert result["free_memory_bytes"] == 80000
    assert result["wifi_connected"] is True
    assert result["wifi_rssi"] == -55


def test_telemetry_disconnected():
    wifi = FakeWiFi(connected=False)

    with patch("telemetry.time.ticks_ms",
               side_effect=[1000, 3000], create=True), \
         patch("telemetry.time.ticks_diff",
               return_value=2000, create=True), \
         patch("telemetry.gc.mem_free",
               return_value=75000, create=True):

        telemetry = DeviceTelemetry(wifi)
        result = telemetry.get_status()

    assert result["uptime_seconds"] == 2
    assert result["wifi_connected"] is False
    assert result["wifi_rssi"] is None
