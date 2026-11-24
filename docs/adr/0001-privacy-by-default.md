# 0001: Privacy by default

## Status

Accepted

## Context

Contact tracing records who was ill, when, and whom they met. That is health data about the
cases and sensitive data about their contacts, many of whom never agreed to be in the system.
A leak or a misuse would harm people and end public trust in tracing. Rules added at the end
of a project are usually incomplete, so they are set here, before any feature exists.

## Decision

- **Least access.** A tracer sees only cases and contacts assigned to them. Supervisors see
  their team's. Access is enforced by Postgres row-level security, not only in the API.
- **Audit everything.** Every read and change of a person's record is logged with who, when
  and why, in a table the application role can append to but not edit or delete.
- **Minimise.** Only fields needed for tracing are stored. Lists show masked details until a
  record is opened.
- **Nothing personal in logs or URLs.** Identifiers in URLs are random IDs; a logging filter
  redacts phone numbers, emails and health service numbers anywhere they slip through.
- **Delete on time.** Records are deleted when the outbreak's retention period ends, and the
  deletion is reported.
- **Made-up data only** in the repository, tests and demos.

## Consequences

- Every feature needs a test for who must not see it, not only for who can.
- Debugging production issues relies on IDs and the audit log rather than names.
- Row-level security adds query complexity and must be covered by tests run as the
  application's own database role.
