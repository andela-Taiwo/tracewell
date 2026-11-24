import { daysRemaining, formatDay } from "./lib/dates";

const TODAY = "2026-03-12";
const SAMPLE = [
  { id: "C-0001", contact: "A. L.", quarantineUntil: "2026-03-19" },
  { id: "C-0002", contact: "G. H.", quarantineUntil: "2026-03-11" },
];

export function App() {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: 16 }}>
      <h1>Tracewell</h1>
      <p>Foundation only: made-up contacts shown until the API exists.</p>
      <table>
        <thead>
          <tr>
            <th>Case</th>
            <th>Contact</th>
            <th>Quarantine until</th>
            <th>Days left</th>
          </tr>
        </thead>
        <tbody>
          {SAMPLE.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.contact}</td>
              <td>{formatDay(row.quarantineUntil)}</td>
              <td>{daysRemaining(TODAY, row.quarantineUntil)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
