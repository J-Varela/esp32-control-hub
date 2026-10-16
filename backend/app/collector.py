
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

        return {
            "uptime_seconds": data["uptime_seconds"],
            "free_memory_bytes": data["free_memory_bytes"],
            "wifi_connected": data["wifi_connected"],
            "wifi_rssi": data["wifi_rssi"],
        }
