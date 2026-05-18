# Report Template

Use this structure for the final adversarial review.

```md
## Verdict

{One decisive sentence: do not proceed as proposed / proceed only if objections are resolved / acceptable risk with named weak points.}

## Strongest Objections

- {Severity} `{file:line or artifact}` {Finding title}
  {Why this undermines the proposal. Explain impact and what would have to change for the objection to fall away.}

## Fragile Assumptions

- {Assumption}: {why it may be false, how the design fails if false, what evidence would reduce the concern}

## Questions That Must Be Answered

- {Question}

## Evidence Reviewed

- {Diffs, docs, tickets, branches, files, commands, or user-provided material reviewed}

## Not Verified

- {Relevant checks or sources that were unavailable, skipped, or blocked}
```

Keep the report concise. If there are no material objections, say so, but still identify the weakest assumptions and what evidence would change the assessment.
