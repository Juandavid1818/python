import { useEffect, useState } from "react";

export default function App() {
  const base = import.meta.env.VITE_API_URL ?? "/api";
  const [hello, setHello] = useState<string>("");
  const [status, setStatus] = useState<string>("");

  useEffect(() => {
    fetch(`${base}/hello`).then(r => r.json()).then(d => setHello(d.message));
    fetch(`${base}/status`).then(r => r.json()).then(d => setStatus(d.status));
  }, []);

  return (
    <div className="p-6 space-y-2">
      <h1 className="text-2xl font-bold">Frontend + Backend</h1>
      <div>👋 Backend dice: <b>{hello || "..."}</b></div>
      <div>🩺 Estado: <b>{status || "..."}</b></div>
    </div>
  );
}
