import { useEffect, useState } from "react";

type User = { id: number; email: string; name: string };

export default function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const base = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api";
    fetch(`${base}/users`)
      .then(async (res) => {
        if (!res.ok) {
          const txt = await res.text().catch(() => "");
          throw new Error(`HTTP ${res.status}: ${txt}`);
        }
        return res.json() as Promise<User[]>;
      })
      .then(setUsers)
      .catch((e) => setError(String(e)))
      .finally(() => setTimeout(() => setLoading(false), 100)); // evita parpadeo
  }, []);

  if (loading) return <div className="p-6 text-lg">Cargando usuarios…</div>;
  if (error) return <div className="p-6 text-red-600">Error: {error}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">🚀 Usuarios del Backend</h1>
      {users.length === 0 ? (
        <div className="text-gray-600">No hay usuarios</div>
      ) : (
        <ul className="list-disc pl-6 space-y-1">
          {users.map((u) => (
            <li key={u.id}>
              <span className="font-medium">{u.name}</span>{" "}
              <span className="text-gray-600">({u.email})</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
