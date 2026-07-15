# AI Skills

A collection of reusable, runtime-neutral instruction packages for AI assistants and agents. Skills provide focused workflows, domain knowledge, and optional supporting resources so that common tasks can be performed consistently.

## Getting started

1. Install or copy this repository into the skills directory configured by your AI assistant or agent runtime.
2. Refresh the runtime's skill catalogue or start a new session if required.
3. Ask for a task covered by a skill. The runtime selects a matching skill from its name and description.

The discovery location and refresh process are runtime-specific; consult your runtime's documentation for those details.

To update an existing installation, run `git pull` from this directory, then refresh the skill catalogue if necessary.

## Repository layout

```text
skills/
+-- .system/        # Runtime or tooling support skills
+-- custom/         # Maintained skills built for this collection
+-- experimental/   # Work-in-progress skills and workflow prototypes
+-- third-party/    # Imported community or external skills
+-- README.md
```

Keep third-party skills attributable to their source and preserve any applicable licence or notice files.

## Using a skill

Each skill has a `SKILL.md` file. Its frontmatter identifies the skill and describes when it applies; its body contains the workflow. A skill may also include scripts, references, and assets.

```text
skill-name/
+-- SKILL.md                 # Required: metadata and instructions
+-- agents/                  # Optional: runtime-specific interface metadata
+-- scripts/                 # Optional: deterministic helper tools
+-- references/              # Optional: supporting material loaded when needed
+-- assets/                  # Optional: templates or other output resources
```

Use a skill's bundled scripts and resources when they are relevant to the task. Treat scripts as code: review them before changing them and run an appropriate check after editing.

## Creating or improving skills

- Keep instructions concise, specific, and action-oriented.
- Put reliable trigger conditions in the `description` frontmatter so the right tasks select the skill.
- Store reusable, detailed material in `references/` rather than duplicating it in `SKILL.md`.
- Add scripts only where repeatability or deterministic behaviour is valuable.
- Keep examples realistic and remove placeholders or obsolete paths before publishing.
- Validate changed metadata, run relevant scripts or tests, and check that links and referenced files exist.

## Local agent guidance

Projects using this collection can add a root `AGENTS.md` with local rules for selecting and applying skills. For example:

```markdown
## Skills

- For non-trivial coding or refactoring, use the `karpathy-guidelines` and `ousterhout-comment-guidelines` skills when they are available.
- Before choosing between materially different approaches, scopes, trade-offs, or outcomes, use the `grilling` skill when it is available.
- Skip `grilling` when the choice is routine, low-risk and easily reversible, or already made explicitly by the user.
- After using a skill from `skills/custom` or `skills/experimental`, suggest at most one concrete improvement to that skill, and only when the suggestion is genuinely worthwhile.
```

Keep project-specific instructions outside individual skills unless they are genuinely reusable across projects.
