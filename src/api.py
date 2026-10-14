
import json


def handle_request(method, path, body, led, telemetry=None):
    if method == "GET" and path == "/api/status":
        return 200, {
            "device": "ESP32 Control Hub",
            "led": led.get_status()
        }

    if method == "POST" and path == "/api/led":
        try:
            data = json.loads(body)
        except (ValueError, TypeError):
            return 400, {"error": "Invalid JSON"}

        if not isinstance(data, dict):
            return 400, {"error": "Expected JSON object"}

        brightness = data.get("brightness")

        if type(brightness) is not int or not 0 <= brightness <= 100:
            return 400, {
                "error": "Brightness must be an integer from 0 to 100"
            }

        led.set_brightness(brightness)

        return 200, {
            "led": led.get_status()
        }

    if method == "GET" and path == "/api/system":
        if telemetry is None:
            return 503, {"error": "Telemetry unavailable"}

        return 200, telemetry.get_status()

    return 404, {"error": "Not found"}
