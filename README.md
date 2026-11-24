# Tracewell

Case management for contact tracers during an epidemic, built on a bitemporal fact store.
Tracers record cases, interviews and meetings; Tracewell works out who counts as a contact
and until when, and keeps every answer explainable after the facts are corrected: what did we
believe on day 7, and why?

> **Status: foundation only.** The project layout, tooling, exposure and quarantine date
> rules, redaction of personal details (backend) and a placeholder web app exist and are
> tested. The fact store, recompute engine, clusters, API, roles, audit, interview flow and
> retention are not built yet. See [the plan](docs/PLAN.md).

## What it will do

- **Facts, never overwritten**: onset and test dates, meetings, people and places, each with
  the time it was true and the time it was recorded. A correction is a new fact.
- **The correction cascade**: correct one onset date and every result that depends on it is
  recomputed: the infectious window, new contacts, quarantine dates, links and clusters.
- **Replay**: open any case as it was known on any past day and see exactly what was believed
  then, unchanged by later corrections.
- **Evidence-weighted links and clusters**: every link carries its evidence and strength;
  clusters grow and split as links are added and withdrawn; duplicate people are merged only
  by a person, with undo.
- **Tracing work**: interviews, daily follow-up calls, and contacts who become cases linked to
  their source.
- **Privacy**: tracers see only their own cases; every read is audited; personal details never
  reach logs or URLs; records and their history are deleted when the retention period ends.

All sample people and places are made up. Tracewell never ships real patient data.

## What exists today

| Part | What it does |
|---|---|
| `backend/src/tracewell/exposure.py` | Infectious windows from onset or test date, contact assessment and quarantine end dates, with configurable rules |
| `backend/src/tracewell/redaction.py` | Removes phone numbers, emails and health service numbers from text and logs, and masks details for partial display |
| `web/` | React and Vite app with a placeholder contact list and calendar-date helpers that never shift a day |

## Quickstart

Requires [uv](https://docs.astral.sh/uv/), Python 3.12, and Node 22 or newer.

```bash
make setup     # install locked backend and web dependencies
make check     # lint, type checks and tests for backend and web
make dev-web   # run the web app on http://localhost:5173
make help      # list every target
```

## Licence

MIT. See [LICENSE](LICENSE).
