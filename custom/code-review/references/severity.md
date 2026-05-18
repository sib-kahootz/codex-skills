# Severity Rubric

Use the lowest severity that accurately captures the likely user, operational, security, data, accessibility, or maintenance impact. Do not inflate severity for style preferences, weak suspicions, or hypothetical failures without a plausible path.

| Severity | Use when |
| --- | --- |
| Critical | Likely data loss, production outage, privilege escalation, serious security exposure, privacy breach, or broad release-blocking regression. |
| High | Likely breakage of an important workflow, sensitive data exposure, weakened authorization, corrupted important state, inaccessible core flow, or serious deployment risk. |
| Medium | Real bug or bounded regression, meaningful edge-case failure, contract drift, missing risky-path tests, or maintainability issue likely to cause near-term defects. |
| Low | Minor localized defect, robustness gap, unclear code path, small accessibility issue, or maintainability improvement with low user or operational impact. |
| Nitpick | Optional polish, wording, naming, formatting, or consistency cleanup. Use sparingly and only when it helps the author. |

Guidance:
- Prefer fewer, sharper findings over exhaustive commentary.
- Do not file nitpicks as findings if they distract from material review concerns.
- If a concern is plausible but uncertain, state the assumption and evidence; omit it if the assumption is too speculative.
- Severity describes the issue. Use `references/verdict.md` separately to decide merge posture.
