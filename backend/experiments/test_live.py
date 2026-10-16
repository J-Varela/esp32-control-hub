from pathlib import Path
import sys
from pprint import pprint

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from app.collector import TelemetryCollector


collector = TelemetryCollector(
    "http://192.168.1.238"
)

telemetry = collector.collect()

print("ESP32 LIVE TELEMETRY")
print("--------------------")
pprint(telemetry)