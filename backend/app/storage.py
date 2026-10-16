
import csv
from pathlib import Path


FIELDS = [
    "timestamp",
    "uptime_seconds",
    "free_memory_bytes",
    "wifi_connected",
    "wifi_rssi",
]


class CSVTelemetryStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record):
        write_header = (
            not self.path.exists()
            or self.path.stat().st_size == 0
        )

        with self.path.open("a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=FIELDS
            )

            if write_header:
                writer.writeheader()

            writer.writerow(record)

    def read_all(self):
        if not self.path.exists():
            return []

        with self.path.open(newline="") as file:
            return list(csv.DictReader(file))
