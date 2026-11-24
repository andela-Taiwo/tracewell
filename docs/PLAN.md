# Plan

Tracewell is built in sessions, each with a clear success test. Later sessions build on
earlier ones.

| # | Session | Success |
|---|---|---|
| 1 | Data model and Postgres schema: outbreaks with their tracing rules, people, cases, contacts, meetings, places and follow-ups; migrations; a seed of made-up people | Database rules refuse impossible states (a contact quarantined before their exposure, a case with no outbreak); the seed creates a realistic week; the test database is separate from the dev one |
| 2 | API, sign-in and roles (tracer, supervisor, administrator), with row-level security so a tracer sees only their own cases, and an audit log of every read and change | Tests as each role prove what they can and cannot see; reading a case writes an audit entry; the API's database role cannot bypass row-level security |
| 3 | Interviews and contacts: record meetings, turn those inside the infectious window into contacts, set quarantine dates, recompute everything when onset or test dates are corrected | Every date rule has a test at its edges; correcting a case's onset updates every contact and is audited; no personal detail appears in any log line |
| 4 | Follow-up work: daily call queues per tracer, outcomes, contacts who become cases linked to their source, supervisor reassignment | Nobody is missed or called twice in a day in tests; reassignment keeps the audit trail |
| 5 | Duplicates and clusters: likely-duplicate people suggested and merged only by a person, with undo; clusters from shared places and contact chains | Merges never lose a meeting or audit entry; clustering matches an independent implementation on generated data |
| 6 | Web app: case list, interview flow, contact follow-up, cluster view, with masked details until a record is opened | Playwright covers an interview creating contacts, a follow-up call, and a tracer being refused another tracer's case |
| 7 | Retention, export and scale: deletion after the retention period with a report, an anonymised export for analysts, and an outbreak of 100,000 cases | Deleted people are gone from every table and the search index; exports contain no direct identifiers; benchmarks fail the build on regression |

## Rules

- Only made-up people. No real patient data in the repo, fixtures, logs or screenshots.
- No personal details in logs, errors, URLs or the command line.
- Every read of a person's record is audited.
- Tracing rules belong to an outbreak and come from the health authority; defaults are
  examples, not medical advice.
- Tests that need Postgres use a separate test database and never touch a developer's data.
