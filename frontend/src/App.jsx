import { useEffect, useState } from "react";

const API = "http://localhost:8000/employees";

export default function App() {
  const [emps, setEmps] = useState([]);
  const [first, setFirst] = useState("");
  const [last, setLast] = useState("");

  // Initial-Load
  useEffect(() => {
    fetch(API)
      .then(r => r.json())
      .then(setEmps)
      .catch(console.error);
  }, []);

  // Neuer Mitarbeiter
  const add = () => {
    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ first_name: first, last_name: last, weekly_hours: 40 })
    })
      .then(r => r.json())
      .then(emp => setEmps(prev => [...prev, emp]));
  };

  return (
    <main style={{ fontFamily: "sans-serif", padding: 20 }}>
      <h1>Pluspunkt – Mitarbeiterliste</h1>

      <input placeholder="Vorname" value={first} onChange={e => setFirst(e.target.value)} />
      <input placeholder="Nachname" value={last} onChange={e => setLast(e.target.value)} />
      <button onClick={add}>Hinzufügen</button>

      <ul>
        {emps.map(e => (
          <li key={e.id}>
            {e.first_name} {e.last_name} – {e.weekly_hours} h/W
          </li>
        ))}
      </ul>
    </main>
  );
}
