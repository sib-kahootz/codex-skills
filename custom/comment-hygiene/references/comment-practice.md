# Comment Practice

## Principles And Actions

- **Create** comments at abstraction boundaries: public modules, classes, functions, APIs, data formats, and cross-boundary helpers. Explain caller-visible behavior, assumptions, errors, side effects, ownership/lifetime, ordering, idempotency, retries, and failure modes.
- **Create** local comments for non-obvious algorithms, invariants, concurrency rules, performance constraints, security-sensitive choices, correctness arguments, and workaround rationale.
- **Update** comments that are stale, vague, misleading, too low-level, or missing caller-visible constraints.
- **Delete** comments that restate names, types, syntax, simple control flow, or obvious statements.
- **Keep** comments that raise the abstraction level by explaining purpose, contract, invariant, limitation, side effect, assumption, tradeoff, or design intent.

## Warning Signs

- Repeated code: `// increment i`, `// get user by id`, `// loop through items`.
- Header comments that list methods but do not explain the abstraction.
- Comments that explain syntax instead of design intent.
- Comments with uncertain terms: should, probably, generally, normally, magic, stuff, thing, helper, simple.
- TODO comments without owner, condition, or reason.
- Workaround comments without the external bug, constraint, or removal condition.
- Interface comments that expose implementation details instead of a caller-facing contract.
- Comments that appear stale after behavior changes.

## Replacement Patterns

### Interface comment

```text
<What abstraction this provides and when to use it.>

<Caller-visible contract: inputs, outputs, errors, side effects, ordering, ownership, or concurrency notes.>
```

### Rationale comment

```text
// <Why this approach is necessary, including the constraint or tradeoff that is not visible in the code.>
```

### Invariant comment

```text
// Invariant: <condition that must remain true and why later code relies on it>.
```

### Workaround comment

```text
// Workaround for <external constraint/bug/reference>: <why the normal approach fails>. Remove when <specific condition>.
```

### TODO comment

```text
// TODO(<owner or tracker>): <specific change>. Needed because <current limitation>; safe to remove when <condition>.
```
