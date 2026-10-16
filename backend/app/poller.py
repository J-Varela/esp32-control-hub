import time
from datetime import datetime, timezone


def poll_once(collector, store):
    telemetry = collector.collect()

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **telemetry,
    }

    store.append(record)
    return record


def run_polling(collector, store, interval=5, stop_event=None):
    if interval <= 0:
        raise ValueError("Interval must be positive")

    while stop_event is None or not stop_event.is_set():
        try:
            record = poll_once(collector, store)
            print(
                "Collected telemetry:",
                record["timestamp"]
            )
        except Exception as error:
            print("Telemetry collection failed:", error)

        if stop_event is not None:
            if stop_event.wait(interval):
                break
        else:
            time.sleep(interval)
