import { useEffect, useState } from "react";

export default function App() {
  const base = import.meta.env.VITE_API_URL ?? "/api";

  const [hello, setHello] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [dbStatus, setDbStatus] = useState<string>("");

  useEffect(() => {
    // ✅ Mensaje de prueba backend
    fetch(`${base}/hello`)
      .then(r => r.json())
      .then(d => setHello(d.message))
      .catch(() => setHello("Error al conectar con backend ❌"));

    // ✅ Estado general backend
    fetch(`${base}/status`)
      .then(r => r.json())
      .then(d => setStatus(d.status))
      .catch(() => setStatus("error"));

    // ✅ Estado de la base de datos
    fetch(`${base}/db-check`)
      .then(r => r.json())
      .then(d => setDbStatus(d.db_status === "ok" ? "Conectada ✅" : "Error ❌"))
      .catch(() => setDbStatus("Error al conectar ❌"));
  }, []);

  return (
    <div className="p-6 space-y-4 text-gray-800">
      <h1 className="text-3xl font-bold">Frontend + Backend + Base de Datos</h1>

      <div>👋 <b>Backend dice:</b> {hello || "Cargando..."}</div>

      <div>🩺 <b>Estado del Backend:</b>{" "}
        {status === "ok" ? "En línea ✅" : status || "Cargando..."}
      </div>

      <div>💾 <b>Base de datos:</b>{" "}
        {dbStatus || "Verificando..."}
      </div>

      <hr className="my-4 border-gray-300" />

      <p className="text-sm text-gray-500">
        Proyecto local con FastAPI, MySQL y Nginx — versión demo 🚀
      </p>
    </div>
  );
}
