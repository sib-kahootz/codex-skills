# Verdict Guidance

Choose exactly one final verdict. For pre-PR review, interpret the verdict as readiness to open the PR and eventual merge risk. Base it on unresolved risk, not the number of comments. Severity informs the verdict, but does not mechanically determine it.

| Verdict | Use when | Do not use when |
| --- | --- | --- |
| Approve | No required pre-merge action remains; comments are optional; tests and labels fit the risk. | Any finding requires a code or test change before merge. |
| Approve with minor changes | Only small, local, low-risk edits remain and another full review cycle is not needed. | The fix needs design judgment, broader regression checking, or changes across multiple areas. |
| Request changes | A material bug, regression, contract drift, accessibility failure, missing risky-path test, or incomplete requirement should be fixed and re-reviewed before merge. | The risk is critical enough that normal author edits are not enough to make merge safe. |
| Block merge | Merging would be unsafe because of a high-confidence security, data loss, permission, privacy, production workflow, deployment, release, or hard Jira/GitHub blocker. | The issue is serious but fixable through ordinary PR revision. Use `Request changes` instead. |

For `Approve`, say the branch appears ready to open as a PR.

For `Request changes`, say the branch should be revised before opening or merging the PR.

For `Block merge`, clearly state the blocker and the minimum condition required before reconsidering the branch.
