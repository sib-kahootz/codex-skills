---
name: cfdocs
description: Look up CFML tags and functions on CFDocs and summarize the reference information. Use when the user provides a ColdFusion/CFML tag such as cfquery or cfsavecontent, a function such as arrayMap or queryExecute, asks "what does this CFML tag/function do?", asks for syntax, parameters, examples, return values, compatibility notes, or wants a concise CFDocs-based reference summary.
---

# CFDocs

## Overview

Use CFDocs as the source of truth for quick CFML tag and function reference lookups. Always fetch the relevant CFDocs page before answering unless the user explicitly asks not to browse.

## Workflow

1. Normalize the requested name:
   - Strip leading `<`, `</`, trailing `>`, parentheses, attributes, and whitespace.
   - Preserve the canonical CFML identifier in the answer, e.g. `cfquery`, `arrayMap`, `queryExecute`.
   - For tags, try `https://cfdocs.org/<tag-name-without-angle-brackets>`.
   - For functions, try `https://cfdocs.org/<function-name>`.

2. Open CFDocs:
   - Browse directly to `https://cfdocs.org/<normalized-name>`.
   - If the page is missing or ambiguous, search CFDocs for the exact identifier.
   - If multiple matches exist, prefer exact case-insensitive match; otherwise state ambiguity and summarize only after choosing the closest page.

3. Summarize the reference:
   - Purpose: what it does in one or two sentences.
   - Syntax: include concise syntax or common call form.
   - Arguments/attributes: list required and important optional items.
   - Returns/body behavior: explain return value for functions, body/output behavior for tags.
   - Examples: include or paraphrase a small representative example when it removes ambiguity.
   - Compatibility: mention engine/version differences, deprecations, aliases, member function forms, or security warnings when CFDocs provides them.

4. Cite source:
   - Link the CFDocs page used.
   - If any detail comes from inference rather than CFDocs, label it as inference.

## Response Shape

Prefer compact, practical output:

- Start with `CFDocs: <name>`.
- Use short sections only when helpful: `Purpose`, `Syntax`, `Key Params`, `Returns`, `Example`, `Notes`.
- Avoid dumping the full CFDocs page.
- For code, keep examples minimal and valid CFML.

## Failure Handling

If CFDocs is unavailable, say so and stop unless the user asks for best-effort memory. Do not silently answer from model memory for this skill, because the core value is current CFDocs reference lookup.
