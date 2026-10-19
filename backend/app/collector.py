
import json
from urllib.request import urlopen


class TelemetryCollector:
    def __init__(self, device_url, timeout=3):
        self.device_url = device_url.rstrip("/")
        self.timeout = timeout

    def collect(self):
        url = self.device_url + "/api/system"

        with urlopen(url, timeout=self.timeout) as response:
            data = json.load(response)

        return validate_telemetry(data)


def validate_telemetry(data):
    if not isinstance(data, dict):
        raise ValueError("Telemetry must be a JSON object")

    fields = (
        "uptime_seconds",
        "free_memory_bytes",
        "wifi_connected",
        "wifi_rssi",
    )

    for field in fields:
        if field not in data:
            raise ValueError(f"Missing telemetry field: {field}")

    for field in ("uptime_seconds", "free_memory_bytes"):
        value = data[field]

        if type(value) is not int or value < 0:
            raise ValueError(f"Invalid {field}: {value!r}")

    connected = data["wifi_connected"]

    if type(connected) is not bool:
        raise ValueError("wifi_connected must be boolean")

    rssi = data["wifi_rssi"]

    if connected:
        if type(rssi) is not int or not -127 <= rssi <= 0:
            raise ValueError("Invalid Wi-Fi RSSI")
    elif rssi is not None:
        raise ValueError(
            "wifi_rssi must be None when disconnected"
        )

    return {field: data[field] for field in fields}
