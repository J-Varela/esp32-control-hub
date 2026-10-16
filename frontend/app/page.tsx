
import LiveDashboard from "@/components/LiveDashboard";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 p-8 text-white">
      <div className="mx-auto max-w-5xl">
        <header className="mb-10">
          <p className="text-sm text-cyan-400">
            EMBEDDED SYSTEMS / TELEMETRY
          </p>

          <h1 className="mt-2 text-4xl font-bold">
            ESP32 Control Hub
          </h1>

          <p className="mt-3 text-slate-400">
            Live hardware monitoring and device telemetry
          </p>
        </header>

        <LiveDashboard />
      </div>
    </main>
  );
}
