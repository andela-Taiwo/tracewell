# Tracewell

Case management for contact tracers during an epidemic: record a case, interview them, list
the people they met, work out who counts as a contact and until when, and follow every
contact up, while treating every patient's data as the sensitive health record it is.

> **Status: foundation only.** The project layout, tooling, exposure and quarantine date
> rules, redaction of personal details (backend) and a placeholder web app exist and are
> tested. The data model, API, sign-in and roles, audit log, interview flow, follow-up queues,
> clusters and retention are not built yet. See [the plan](docs/PLAN.md).

## What it will do

- **Cases**: intake from a positive test, symptom onset, and the infectious window worked out
  from the outbreak's rules.
- **Interviews**: a guided flow for listing places and people, with meetings inside the
  infectious window turned into contacts automatically.
- **Contacts**: quarantine end dates from the last exposure, daily follow-up calls assigned to
  tracers, and contacts who become cases linked back to their source.
- **People, once**: likely duplicates found and merged by a person, never automatically.
- **Clusters**: cases linked through shared places or chains of contacts, shown as groups.
- **Privacy**: tracers see only their own cases; every view of a record is audited; personal
  details never reach logs or URLs; records are deleted after the retention period.

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
