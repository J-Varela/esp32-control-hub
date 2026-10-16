
"use client";

import { useEffect, useState } from "react";
import TelemetryChart, {
  type TelemetrySample,
} from "./TelemetryChart";

type HistoryResponse = {
  count: number;
  samples: TelemetrySample[];
};

export default function LiveDashboard() {
  const [latest, setLatest] = useState<TelemetrySample | null>(null);
  const [history, setHistory] = useState<TelemetrySample[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [now, setNow] = useState<number | null>(null);

  useEffect(() => {
    let active = true;

    async function refresh() {
      try {
        const [latestResponse, historyResponse] = await Promise.all([
          fetch("/api/telemetry/latest", { cache: "no-store" }),
          fetch("/api/telemetry/history?limit=50", {
            cache: "no-store",
          }),
        ]);

        if (!latestResponse.ok || !historyResponse.ok) {
          throw new Error("Telemetry API unavailable");
        }

        const latestData: TelemetrySample =
          await latestResponse.json();

        const historyData: HistoryResponse =
          await historyResponse.json();

        if (active) {
          setLatest(latestData);
          setHistory(historyData.samples);
          setError(null);
        }
      } catch {
        if (active) {
          setError("Unable to refresh telemetry");
        }
      }
    }

    void refresh();

    const timer = setInterval(() => {
      void refresh();
    }, 5000);

    const clockTimer = setInterval(() => {
        setNow(Date.now());
    }, 1000);

    return () => {
      active = false;
      clearInterval(timer);
      clearInterval(clockTimer);
    };
  }, []);

  const ageSeconds =
    latest && now !== null
        ? Math.max(
            0,
            Math.floor(
            (now - new Date(latest.timestamp).getTime()) / 1000
            )
        )
        : null;

  const isFresh =
    ageSeconds !== null && ageSeconds <= 15;

  return (
    <section>
      {error && (
        <p className="mb-4 text-amber-400">{error}</p>
      )}



    <div className="mb-6 flex items-center gap-3">
    <span
        className={`h-3 w-3 rounded-full ${
        isFresh ? "bg-emerald-400" : "bg-amber-400"
        }`}
    />

    <span className="text-sm text-slate-300">
        {ageSeconds === null
        ? "Waiting for device telemetry"
        : isFresh
            ? `Recent telemetry (${ageSeconds}s ago)`
            : `Stale telemetry (${ageSeconds}s ago)`}
    </span>
    </div>


      {!latest ? (
        <p className="text-slate-400">
          Waiting for telemetry...
        </p>
      ) : (

        <>
          <div className="grid gap-6 md:grid-cols-3">
            <MetricCard
              label="Wi-Fi Signal"
              value={
                latest.wifi_rssi === null
                  ? "Unavailable"
                  : `${latest.wifi_rssi} dBm`
              }
            />

            <MetricCard
              label="Free Memory"
              value={`${(
                latest.free_memory_bytes / 1024
              ).toFixed(1)} KiB`}
            />

            <MetricCard
              label="Device Uptime"
              value={`${latest.uptime_seconds}s`}
            />
          </div>

          <p className="mt-6 text-sm text-slate-400">
            Last sample:{" "}
            {new Date(latest.timestamp).toLocaleString()}
          </p>
        </>
      )}

      {history.length > 0 && (
        <TelemetryChart samples={history} />
      )}
    </section>
  );
}

function MetricCard({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-4 text-3xl font-semibold">{value}</p>
    </div>
  );
}
