
import gc
import time


class DeviceTelemetry:
    def __init__(self, wifi):
        self.wifi = wifi
        self.start_ms = time.ticks_ms()

    def get_status(self):
        gc.collect()

        connected = self.wifi.isconnected()

        return {
            "uptime_seconds": time.ticks_diff(
                time.ticks_ms(),
                self.start_ms
            ) // 1000,
            "free_memory_bytes": gc.mem_free(),
            "wifi_connected": connected,
            "wifi_rssi": (
                self.wifi.status("rssi")
                if connected else None
            )
        }
