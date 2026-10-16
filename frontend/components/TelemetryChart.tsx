
"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export type TelemetrySample = {
  timestamp: string;
  uptime_seconds: number;
  free_memory_bytes: number;
  wifi_connected: boolean;
  wifi_rssi: number | null;
};

export default function TelemetryChart({
  samples,
}: {
  samples: TelemetrySample[];
}) {
  const data = samples.map((sample) => ({
    time: new Date(sample.timestamp).toLocaleTimeString(),
    rssi: sample.wifi_rssi,
  }));

  return (
    <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold">
        Wi-Fi Signal History
      </h2>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />

            <XAxis
            dataKey="time"
            stroke="#94a3b8"
            tick={{ fontSize: 11 }}
            minTickGap={35}
            tickMargin={12}
            />

            <YAxis
            stroke="#94a3b8"
            domain={[-70, -40]}
            ticks={[-70, -60, -50, -40]}
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `${value}`}
            width={45}
            />

            <Tooltip />
            <Line
              type="monotone"
              dataKey="rssi"
              stroke="#22d3ee"
              strokeWidth={2}
              dot={false}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
