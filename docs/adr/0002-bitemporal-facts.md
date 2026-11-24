# 0002: Bitemporal facts, derived results

## Status

Accepted

## Context

Contact tracing runs on interviews, and interviews are corrected constantly. A case remembers
that their symptoms started two days earlier than they said. That one correction moves their
infectious window, turns earlier meetings into exposures, adds contacts, moves quarantine
dates, and can join or split clusters.

If the app overwrites the old value, two things are lost. Nobody can explain a decision made
before the correction ("why was this contact released on day 7?"). And the derived state can
quietly drift from what the facts now say.

## Decision

- **Facts are bitemporal.** Every fact that drives a decision has a valid time (when it was
  true in the world) and a recorded time (when Tracewell learned it). Those facts are onset,
  test date, meeting, person details, place details, merge and the tracing rules version.
- **Facts are append-only.** A correction or retraction is a new fact with a later recorded
  time.
- **Results are derived.** Infectious windows, contact status, quarantine dates and clusters
  are pure functions of the facts as known at a recorded time. They can be cached and updated
  incrementally, but the cache must always equal a full replay. Randomised tests enforce this.
- **Replays are fixed.** Asking what was believed at recorded time T gives the same answer
  forever, whatever is recorded later.
- **Deletion wins.** When a person's retention period ends, their facts and all their history
  are deleted, and the replays that included them change. The deletion is itself recorded,
  without personal details.

## Consequences

- Every feature is built as facts plus a derivation, which is more work up front than
  updating rows.
- Bars 1 and 2 in the plan (incremental equals replay; the past stays fixed) become the main
  correctness tests for the whole app.
- Clusters must be able to split, so they are recomputed per affected group rather than kept
  in a union-find structure.
- Storage grows with corrections. That's acceptable at outbreak scale and is measured in
  session 7.
