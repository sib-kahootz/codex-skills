---
name: repo-onboarding
description: Build a practical onboarding brief for an unfamiliar code repository, using optional parallel subagent evidence-gathering lanes only when repository size, scope, or risk justifies the token cost. Use when Codex should explore a repo, explain architecture, map directories and workflows, identify install/dev/build/test/lint/typecheck commands, summarize conventions, locate key files, explain data flow and integrations, identify risks and unknowns, or help a new contributor make a first safe change.
---

# Repo Onboarding

Create an evidence-backed guide that helps a new contributor understand the repository and make a first safe change. Prefer local docs, manifests, source files, CI config, and runnable commands over guesses.

Do not edit files unless the user explicitly asks for an onboarding document to be written.

Default to single-agent onboarding. Use read-only subagent evidence lanes only when the repository is large, unfamiliar, crosses several subsystems, or the user explicitly asks for parallel onboarding. Parent always scopes, samples, verifies, resolves conflicts, and synthesizes one brief.

## Workflow

### 1. Scope

Identify:

- repo root
- requested area, if any
- current branch and dirty state
- whether the user wants a chat brief or a file
- whether subagent tools are available and permitted by current runtime/tool policy, if the scope appears broad enough to justify them

Start with:

```bash
git status --short
git branch --show-current
rg --files
```

Use directory listings when `rg --files` is unavailable or when high-level structure is hard to see.

Default to single-agent assessment for small and medium repositories. Use parallel subagents only when the extra coverage is likely to justify the token cost. If subagents would help but are unavailable or not permitted, continue single-agent and state that limitation in `## How This Was Assessed`.

Before spawning optional subagents, define:

- shared constraints: repo root, dirty state, requested area, output type, safe command limits
- non-overlapping lanes and which files/directories each lane should prioritize or avoid
- parent task: keep working locally on scoping, quick inventory, verification, conflict resolution, and final synthesis

### 2. Read Evidence

Read or assign docs and manifests before source deep-dives:

- `README*`, `CONTRIBUTING*`, `AGENTS.md`
- `docs/`, ADRs, architecture notes, runbooks
- package/build manifests and lockfiles
- CI/workflow config
- Docker/container/dev environment files
- env examples and config templates
- test config and fixtures

Then inspect or assign source entry points, routing, services, packages, shared libraries, database/migration files, API contracts, and tests around important flows.

Avoid duplicating lane work. Parent should directly inspect only enough evidence to verify key claims, resolve conflicts, and fill gaps.

### 3. Identify Commands

Find install, dev, build, test, lint, typecheck, format, database, migration, seed, and service commands from docs, manifests, scripts, CI, and Makefiles.

Mark command confidence:

- `verified`: actually run successfully in this session
- `doc-sourced`: found in repo docs
- `manifest-sourced`: found in package/build scripts
- `inferred`: likely from stack conventions but not documented
- `blocked`: could not run because dependencies, network, credentials, services, sandbox, time, or secrets are missing

Do not run slow, destructive, network-heavy, secret-dependent, or environment-mutating commands unless the user asks or the repo clearly documents them as safe.

### 4. Map Architecture

Explain:

- runtime shape: app, service, library, monorepo, CLI, worker, frontend, backend
- entry points and request/job/event flow
- main directories and ownership boundaries
- data stores, migrations, models, schemas, and contracts
- APIs, integrations, auth, permissions, validation, logging, and error handling
- generated files and files that should not be edited by hand
- where tests live and how test data is organized

Keep the map tied to exact files and directories.

### 5. Extract Conventions

Summarize repo-specific patterns:

- naming and module layout
- dependency injection or service boundaries
- state/data access patterns
- API shape and error conventions
- auth, tenancy, permissions, and security checks
- testing style and fixture strategy
- formatting/linting/type conventions
- migration, config, release, and deployment expectations
- frontend styling/accessibility conventions when relevant

Avoid generic advice that could apply to any repo.

### 6. First-Change Guide

Give a practical path for a new contributor:

- where to start reading
- where common changes usually go
- how to add or update tests
- what commands to run before a PR
- what files are risky
- what questions to ask maintainers before changing unclear areas

If the user requested a specific area, tailor the first-change guide to that area.

## Subagent Lanes

Split repository exploration into independent map-building tasks only when optional subagents are justified. Keep final synthesis in the parent agent. Use two lanes for broad repos, three for large repos, and four only for monorepos or explicit deep parallel review. For tiny repos, single-file questions, or narrow subsystem requests, stay single-agent.

Lane selection:

- Docs and commands lane: use for unfamiliar repos; inspect README, docs, manifests, CI, scripts, env examples, and setup/test/build commands.
- Architecture lane: use when runtime or data flow is unclear; inspect entry points, routing, services, packages, data stores, integrations, and request/job/event flow.
- Conventions and risks lane: use when the user wants first-change guidance or PR readiness; inspect tests, fixtures, auth/permissions patterns, generated files, and risky areas.
- Area-specific lane: use when the user names a subsystem, feature, or changed files; inspect that slice deeply.

Use prompts like:

```text
You are one read-only repo-onboarding lane. Inspect <repo> for <lane focus>.
Do not edit files, install dependencies, fetch network resources, start services, run migrations, or mutate repo state.
Return:
- Lane summary
- Evidence: exact files/dirs inspected and intentionally skipped
- Commands: commands found with confidence labels
- Architecture/conventions
- Risks/unknowns
- Suggested brief snippets
```

Avoid broad duplicate scans. Subagents should cite exact files and commands and should not write the final onboarding brief. Parent agent owns confidence labels, unknowns, conflict resolution, and the final onboarding brief.

## Parent Synthesis

After lane results return:

- Merge lane outputs by report topic, not by agent.
- De-duplicate repeated evidence and preserve the strongest citations.
- Resolve conflicts by checking source files directly; mark unresolved conflicts as unknowns.
- Treat subagent claims as unverified unless backed by cited files, exact command evidence, or parent-run commands.
- Convert lane snippets into one coherent onboarding narrative; do not expose raw lane dumps unless the user asks.
- Own final command confidence labels.

## Report

Use this structure unless asked otherwise:

```markdown
# Repository Onboarding

## How This Was Assessed

## What This Repo Is

## How It Is Organized

## How It Runs

## Architecture Map

## Development Conventions

## First-Change Guide

## Risks And Unknowns
```

Keep it skimmable. Cite exact files, directories, and commands. Distinguish verified facts from inference. In `## How This Was Assessed`, list areas covered, coverage gaps, whether subagents were used, and whether helpful subagents were unavailable or not permitted.

## Safety Rules

- Do not modify repo files unless asked.
- Do not install dependencies, fetch network resources, start long-running services, run migrations, or mutate databases without user approval.
- Do not hide dirty worktree state.
- Do not claim commands work unless run in this session or backed by explicit user-provided evidence.
- If the repo is huge, sample intelligently: docs, manifests, entry points, changed/requested areas, and representative tests first.
- If using subagents, keep them read-only and do not let them create generated artifacts, run formatters, or mutate local, remote, service, or database state.
