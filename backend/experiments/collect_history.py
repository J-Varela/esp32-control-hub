
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from app.collector import TelemetryCollector
from app.history import collect_history


collector = TelemetryCollector(
    "http://192.168.1.238"
)

collect_history(
    collector=collector,
    output_path="data/telemetry/esp32_history.csv",
    samples=10,
    interval=2,
)
