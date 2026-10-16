
import csv
from pathlib import Path
from statistics import mean, stdev

path = Path("data/telemetry/esp32_history.csv")

with path.open(newline="") as file:
    records = list(csv.DictReader(file))

rssi = [
    int(row["wifi_rssi"])
    for row in records
    if row["wifi_rssi"]
]

memory = [
    int(row["free_memory_bytes"])
    for row in records
]

print("ESP32 TELEMETRY ANALYSIS")
print("------------------------")
print("Samples:", len(records))

print("\nWi-Fi Signal")
print("Mean RSSI:", round(mean(rssi), 2), "dBm")
print("Minimum RSSI:", min(rssi), "dBm")
print("Maximum RSSI:", max(rssi), "dBm")
print("Standard deviation:", round(stdev(rssi), 2), "dB")

print("\nMemory")
print("Initial free memory:", memory[0], "bytes")
print("Final free memory:", memory[-1], "bytes")
print("Net change:", memory[-1] - memory[0], "bytes")
