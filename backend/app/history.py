import time
from datetime import datetime, timezone

from app.storage import CSVTelemetryStore


def collect_history(collector, output_path, samples=10, interval=2):
    if samples < 1:
        raise ValueError("samples must be at least 1")

    if interval < 0:
        raise ValueError("interval cannot be negative")

    store = CSVTelemetryStore(output_path)

    for index in range(samples):
        telemetry = collector.collect()

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **telemetry,
        }

        store.append(record)

        print(
            f"[{index + 1}/{samples}] "
            f"Uptime: {telemetry['uptime_seconds']}s | "
            f"RAM: {telemetry['free_memory_bytes']} bytes | "
            f"RSSI: {telemetry['wifi_rssi']} dBm"
        )

        if index < samples - 1:
            time.sleep(interval)

    return store
