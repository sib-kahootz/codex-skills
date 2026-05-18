# PR Description Guide

Use this structure unless the repository has a stricter template.

```markdown
## Jira
- [ABC-123](https://your-jira.example/browse/ABC-123)

## Summary
Briefly explain what changed and why.

## Changes
- Concrete implementation change.
- Concrete implementation change.
- Concrete implementation change.

## Testing
- Automated check or test command.
- Manual verification performed.
- Note any relevant screenshots, API examples, or environment details.

## Reviewer Testing Focus
- High-level area, workflow, or risk reviewers should prioritize.
- Important scenario, role, environment, or regression surface to inspect.
- Call out any unverified behavior that deserves reviewer attention.

## TODO Items
- [ ] `path/to/file.ext:123` - TODO text added by this PR.

## Deployment Steps
- Ordered deployment, migration, config, cache, restart, rebuild, rollout, or rollback action.
- Use `Standard deploy only. No special deployment steps.` only when that is true.
- For migrations, state where the migration lives, when to run it, whether it is safe to re-run, how to verify completion, the rollback plan, and whether it can run before the new code is deployed.

## Risks / Impacts
- Performance, security, accessibility, compatibility, user, operational, docs, or support impact.
- Use `Low risk. No schema changes.` only when that is true.
```

## Writing Rules

- Make the title concise and action-oriented.
- Prefix the title with the Jira ticket id in square brackets when one clear ticket is available, for example `[ABC-123] Fix null reference in invoice export`.
- Render every Jira ticket id in the PR description body as a Markdown link when a ticket URL can be determined, for example `[ABC-123](https://your-jira.example/browse/ABC-123)`.
- Keep Jira ticket ids in the PR title as plain text because GitHub titles do not render Markdown links.
- If multiple Jira ticket ids are found and no primary ticket is clear, ask which one to use or omit the prefix and disclose the ambiguity before publishing.
- Use the body to explain both what changed and why reviewers should care.
- Include a high-level reviewer testing focus section even when automated tests exist.
- Include a TODO Items section only when the branch adds new code TODOs. Use one unchecked checkbox per TODO, with file and line context when available. Omit the section when no new TODOs are introduced.
- Include deployment steps even when no special deployment action is required.
- Mention unverified areas directly instead of implying broader coverage.
- Keep risk language specific; avoid vague reassurance.
