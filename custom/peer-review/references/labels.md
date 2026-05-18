# PR Label Guidance

Review labels against the PR diff, Jira context, changed files, and release impact. Report labels as `correct`, `missing`, or `questionable`; do not change labels.

Call out missing labels when they affect review expectations, release handling, deployment steps, support/docs follow-up, or test scope. Ignore harmless extra labels unless they could mislead reviewers or release managers.

## Required Code-Change Label

Any PR with code changes must have the `for patch` label. Treat source, test, configuration, build, schema, migration, dependency, script, and application asset changes as code changes. Report `for patch` as `missing` when any code change is present and the label is absent. Documentation-only changes do not require `for patch` unless the diff also changes code.

## Merge State

| Label | Meaning |
| --- | --- |
| `DO NOT MERGE YET`, `On hold` | Not ready to merge. Treat as release-blocking until removed or explained. |
| `Deleted PR`, `Duplicate`, `Reverted`, `Wrong fix` | Non-standard lifecycle state. Confirm intent before treating the PR as normally mergeable. |

## Change Type

| Label | Meaning |
| --- | --- |
| `bug` | Fixes a defect. |
| `Regression` | Fixes a defect introduced by a previous PR. |
| `enhancement`, `New Feature`, `UI Improvement` | Adds or improves user-facing behaviour. |
| `Remove Functionality` | Removes behaviour or access users may rely on. |
| `Refactor Code`, `Tidy` | Internal cleanup or restructuring with no intended behaviour change. |
| `Sorry` | Unusually large, risky, or difficult review; expect extra scrutiny. |

## Areas And Risk

| Label | Meaning |
| --- | --- |
| `Accessibility` | Accessibility-impacting UI change; expect semantic, keyboard, focus, and screen-reader checks. |
| `Security`, `ITHC` | Security or compliance-sensitive change; check auth, data exposure, validation, logging, and audit implications. |
| `Performance` | Performance-sensitive change; check query shape, caching, loops, payload size, and realistic bottlenecks. |
| `AWS` | AWS-specific behaviour, infrastructure, or deployment concern. |
| `Marketing` | Marketing-owned content, tracking, or public-facing campaign change. |
| `Client Plugin` | Client plugin added or changed; check compatibility and rollout impact. |
| `Ops`, `Tool`, `Dev` | Ops/tooling/dev-only change; verify whether production behaviour is truly unaffected. |

## Language And Dependency

| Label | Meaning |
| --- | --- |
| `Golang`, `Java` | Language-specific backend change. |
| `Java lib update`, `JS library update` | Dependency update; check compatibility, security, lockfiles, and affected runtime. |

## Tests And Documentation

| Label | Meaning |
| --- | --- |
| `Testing` | MXUnit/JUnit or test-support change. |
| `Documentation` | User, developer, or product documentation changed. |
| `NEED Knowledgebase change`, `NEED Support ticket update` | Follow-up required outside code before or after release. |
| `API Doc Change` | API doc header changed; API docs need rebuilding. |

## Deployment And Release Actions

| Label | Meaning |
| --- | --- |
| `for patch`, `Hotfix`, `Patched`, `Urgent`, `Quickie` | Patch/release urgency or live-patch state; check narrowness, rollback, and verification. |
| `NEED Config Change`, `NEED migrate step`, `Need Post-Release Action`, `NEED Schema change`, `NEED Live Brand Rebuild` | Release action needed; verify it is documented, ordered, and safe to repeat where relevant. |
| `NEED Apache restart`, `NEED Tomcat restart`, `NEED Java restart` | Service restart needed; check operational impact and timing. |
| `NEED Cache clear`, `NEED cfcrefresh`, `NEED Java prefs reload`, `NEED Site refresh`, `NEED softfullrestart`, `NEED static refresh` | Runtime, cache, static asset, or config reload needed after deployment. |
