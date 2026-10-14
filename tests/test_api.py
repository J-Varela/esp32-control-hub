
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from api import handle_request


class FakeLED:
    def __init__(self):
        self.brightness = 0

    def set_brightness(self, value):
        self.brightness = value

    def get_status(self):
        return {
            "brightness": self.brightness,
            "enabled": self.brightness > 0
        }


def test_get_status():
    led = FakeLED()

    status, response = handle_request(
        "GET", "/api/status", "", led
    )

    assert status == 200
    assert response["led"]["brightness"] == 0


def test_set_brightness():
    led = FakeLED()

    status, response = handle_request(
        "POST", "/api/led", '{"brightness": 50}', led
    )

    assert status == 200
    assert led.brightness == 50
    assert response["led"]["enabled"] is True


def test_invalid_brightness():
    led = FakeLED()

    status, response = handle_request(
        "POST", "/api/led", '{"brightness": 150}', led
    )

    assert status == 400
    assert led.brightness == 0



class FakeTelemetry:
    def get_status(self):
        return {
            "uptime_seconds": 120,
            "free_memory_bytes": 80000,
            "wifi_connected": True,
            "wifi_rssi": -55
        }


def test_get_system_telemetry():
    led = FakeLED()
    telemetry = FakeTelemetry()

    status, response = handle_request(
        "GET",
        "/api/system",
        "",
        led,
        telemetry
    )

    assert status == 200
    assert response["uptime_seconds"] == 120
    assert response["free_memory_bytes"] == 80000
    assert response["wifi_connected"] is True
    assert response["wifi_rssi"] == -55


def test_system_telemetry_unavailable():
    led = FakeLED()

    status, response = handle_request(
        "GET",
        "/api/system",
        "",
        led
    )

    assert status == 503
    assert response == {
        "error": "Telemetry unavailable"
    }
