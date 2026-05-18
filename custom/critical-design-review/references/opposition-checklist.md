# Opposition Checklist

Use this checklist to find the strongest case against a proposal. Do not report every category; report only objections with real evidence or material risk.

## Problem And Scope

- The proposal solves a symptom rather than the underlying problem.
- The success criteria are missing, unverifiable, or disconnected from user/business value.
- Important non-goals are unstated, making scope creep likely.
- The design assumes a single happy path and ignores lifecycle states, cancellation, retries, partial completion, or reversals.

## Domain Model

- Terms conflict with repository docs, product language, database names, or existing APIs.
- A new abstraction duplicates or weakens an existing concept.
- Ownership boundaries are unclear: no one obviously owns data, permissions, cleanup, support, or failure recovery.
- The design creates state that can become contradictory across systems.

## Compatibility And Data

- Existing consumers, integrations, exports, imports, reports, or background jobs may break.
- Backfill, migration, rollback, re-run, and idempotency behavior is unspecified.
- The design assumes data quality that the system does not enforce.
- Deletion, retention, audit, timezone, locale, or historical reporting behavior is vague.

## Security And Permissions

- Trust boundaries are crossed without explicit validation.
- Permission checks are too late, too broad, cached unsafely, or inconsistent with adjacent flows.
- Sensitive data could appear in logs, analytics, client payloads, exports, or error messages.
- The design lacks an audit trail where users or operators will need one.

## Operations And Delivery

- The rollout has no kill switch, feature flag, staged migration, or monitoring plan despite meaningful blast radius.
- Failures would be hard to detect, diagnose, or recover from.
- The change couples deploy order across services, jobs, schemas, clients, or third parties.
- Support, documentation, training, or customer communication burden is underestimated.

## UX And Accessibility

- The design creates ambiguous user choices or irreversible actions without enough context.
- Error states, empty states, loading states, and permission-denied states are not designed.
- Keyboard, screen-reader, color contrast, focus order, motion, or mobile constraints are ignored.
- The proposal optimizes first use while making repeated work slower or riskier.

## Testing And Evidence

- Tests cover implementation mechanics but not the risky behavior.
- No fixture, migration rehearsal, contract test, accessibility test, load test, or rollback test exists where one is warranted.
- The proposal relies on assumptions that could be cheaply validated before implementation.
- The test plan cannot catch the failure mode the design is most likely to produce.

## Complexity And Alternatives

- A simpler local change, configuration, process change, or documentation fix may solve the problem.
- The design introduces long-lived concepts for a short-lived need.
- The approach creates lock-in to a vendor, protocol, schema, workflow, or ownership model without acknowledging the cost.
- The proposal chooses flexibility before there is evidence that flexibility is needed.
