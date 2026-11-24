# Plan

Tracewell is built in sessions, each with a clear success test. Later sessions build on
earlier ones. The first two sessions build the bitemporal fact store and the recompute engine,
because everything else depends on them and their guarantees must hold before any screen
exists.

## The four bars

Each is enforced by an automated test.

1. **Incremental equals replay.** For random corrections applied in random orders, the
   incrementally maintained state is identical to a full replay of all facts.
2. **The past stays fixed.** A replay of any past moment never changes after a later
   correction.
3. **Clusters are right.** Clusters match an independent implementation on seeded outbreaks
   where the true chains are known.
4. **Corrections are fast enough.** One correction on a 100,000-case outbreak stays within a
   stated time budget on the desktop.

## Sessions

| # | Session | Success |
|---|---|---|
| 1 | Bitemporal fact store: facts (onset, test date, meeting, person details, rules version) with valid time and recorded time, append-only corrections and retractions, and "as known at" queries | No fact is ever overwritten; an as-of query returns exactly the facts recorded by then; property tests cover out-of-order and back-dated corrections |
| 2 | Recompute engine: pure functions derive infectious windows, contacts and quarantine dates from facts as known at a moment (building on `exposure.py`), with incremental updates when a fact changes | Bars 1 and 2, checked with randomised correction sequences against full replay |
| 3 | Evidence-weighted links and clusters: links carry their evidence and strength; clusters grow and split; only the affected group is recomputed | Bar 3 on seeded outbreaks; splitting after a withdrawn link matches a full recompute |
| 4 | Persistence, API, roles and audit: the fact store in Postgres, row-level security so tracers see only their own cases, an audit entry for every read | Tests as each role prove what they can and cannot see; the app's database role cannot bypass row-level security; bars 1 and 2 still hold against Postgres |
| 5 | Tracing workflow: interviews that record meetings, daily follow-up queues, contacts becoming cases, duplicate people suggested for a person to merge, with undo as a correction | Nobody is missed or called twice in a day; a merge and its undo both replay correctly |
| 6 | Web app: case and contact views, the correction cascade shown as a diff, the "as known on" view, and the cluster view, with details masked until a record is opened | Playwright covers an interview, a correction that adds contacts and splits a cluster, and a tracer being refused another tracer's case |
| 7 | Retention and scale: deletion at the end of retention removes facts and their history everywhere, an anonymised export, and a 100,000-case outbreak | Bar 4; deleted people are gone from every table; exports contain no direct identifiers; benchmarks fail the build on regression |

## Rules

- Facts are never updated in place. A correction or retraction is a new fact.
- Derived results (windows, contact status, quarantine dates, clusters) are never stored as
  truth. They are recomputed from facts and may be cached, but a cache must always equal a
  replay.
- Only made-up people. No real patient data in the repo, fixtures, logs or screenshots.
- No personal details in logs, errors, URLs or the command line.
- Every read of a person's record is audited.
- Deletion at the end of retention removes history as well. Privacy law wins over
  replayability.
- Tracing rules belong to an outbreak and come from the health authority; defaults are
  examples, not medical advice.
- Tests that need Postgres use a separate test database and never touch a developer's data.
