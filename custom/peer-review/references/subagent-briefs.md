# Subagent Briefs

Use these briefs as lane prompts. Fill placeholders with PR-specific context. Keep prompts short and read-only.

## Common Instructions

You are one reviewer lane in a peer review. Work read-only. Do not edit files, fetch, checkout, post comments, change labels, change branches, update Jira, mutate GitHub state, or mutate local repo state.

When the parent supplies PR metadata, Jira context, changed files, and diff excerpts, treat that as the lane evidence source. Do not report `did not fetch` or `did not checkout` as a limitation unless the lane needed additional repository context to support or reject a specific finding.

Review PR `<pr>` in repo `<repo>`.

Mode:

`<reviewModeInstructions>`

Context:

- Base ref: `<baseRef>`
- Review ref: `<reviewRef>`
- Jira summary and acceptance criteria: `<jiraContext>`
- Changed files: `<changedFiles>`
- Parent risk summary: `<riskSummary>`

Return:

- `Lane summary`: one paragraph.
- `Findings`: concrete issues only, with file/line evidence, impact, suggested fix, and lowest accurate severity.
- `Verification`: what you checked and what you could not check.
- `Residual risk`: lane-specific risks not proven enough to report as findings.

Say `No lane findings` if no material issue exists.

## Context Lane

Focus on PR/Jira alignment:

- GitHub title/body/labels/comments/reviews/checks.
- Jira requirements, acceptance criteria, linked blockers, status, components, fix versions.
- Conflicts between PR text, Jira requirements, reviewer comments, and code intent.
- Missing or questionable labels.

Do not deep-review code except to confirm label or requirement alignment.

## Correctness Lane

Focus on behavior:

- Changed control flow, edge cases, regressions, API/data contracts.
- Persistence behavior, migrations, idempotency, backward compatibility.
- Error handling, null/empty states, transaction boundaries.
- File/line-level failure paths.

Do not spend time on styling, label review, or test command execution unless directly tied to a finding.

## Security And Accessibility Lane

Focus on risk surfaces:

- Authn/authz, permission checks, validation, output encoding, XSS/CSRF, sensitive data.
- Input trust boundaries, external service calls, secrets, audit/log exposure.
- UI keyboard access, names/labels, focus behavior, contrast risk, screen reader semantics.
- User-facing failures that create inaccessible or unsafe behavior.

Report only plausible failure paths grounded in diff evidence.

## Verification Lane

Focus on proof:

- Test files changed or missing for risky behavior.
- Check status from GitHub when available.
- Repo-documented commands that should be run locally.
- Build/lint/typecheck/migration/seed/deployment checks.
- Rollback and release risk.

In connector-first read-only mode, do not run local commands; use connector-provided check results and code inspection only. Otherwise, run focused commands only when safe, read-only, and reasonable. If a command may write source files, update snapshots, alter DB state, call production services, or require broad sandbox/network approval, do not run it; state exact blockers.

## Data Or Migration Lane

Use when schema, persistence, indexing, deletion, irreversible writes, or data migration changed.

Focus on:

- Schema compatibility and rollout order.
- Backfill/idempotency/retry behavior.
- Locking, long-running queries, indexes, FK/null/default behavior.
- Rollback path and partial-failure behavior.

## Frontend Lane

Use when UI, forms, routing, layout, or client state changed.

Focus on:

- User workflow regressions.
- Form validation and state consistency.
- Responsive behavior and accessible controls.
- Client/server contract mismatch.
- Browser/runtime errors from changed code.

## Performance Lane

Use when hot paths, batch jobs, queues, search, reports, or large data operations changed.

Focus on:

- Query count, indexing, N+1 behavior, caching correctness.
- Memory growth, batch size, retry storms, queue throughput.
- Expensive work moved into request paths.
- Metrics, alerting, and rollback implications.
