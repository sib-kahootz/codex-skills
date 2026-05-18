# Review Checklist

Use this checklist to find material PR review issues. Prioritize real defects and risks over style preferences, speculative rewrites, or generic advice.

| Area | Check for |
| --- | --- |
| Correctness | Regressions, edge cases, nullability, ordering, async behavior, stale state, cleanup, error handling, and conflicts with Jira acceptance criteria or PR intent. |
| Security | Authentication, authorization, validation, injection, XSS, SSRF, redirects, path traversal, sensitive logging, and trust in client-provided data. |
| API/data | Contract drift, error shape changes, partial failures, idempotency, transaction boundaries, migrations, backwards compatibility, unbounded queries, and N+1 query patterns. |
| Accessibility | Labels, semantic HTML, keyboard flow, focus management, ARIA usage, screen-reader behavior, color-only indicators, dialogs, and dynamic updates. |
| Performance | Meaningful bottlenecks: query shape, repeated work, payload size, cache invalidation, synchronous blocking, hot paths, and avoidable work in loops. Avoid micro-optimization unless the PR touches a hot path. |
| Maintainability | Coupling, mixed responsibilities, brittle interfaces, duplication, confusing flow, weak UI/API boundaries, hidden side effects, and code paths future changes are likely to break. |
| Tests | Risky behavior coverage: async paths, failure paths, edge cases, security checks, permissions, accessibility-relevant UI behavior, migrations, and API contracts. |

Do not require tests for every small change. Require them when changed behavior is risky, user-facing, security-sensitive, data-sensitive, or likely to regress.
