---
name: persona-simulator
description: Simulate realistic conversations, reactions, objections, and feedback from predefined personas. Use when the user provides or references personas and wants to choose a persona, role-play as a persona, ask persona-specific questions, compare persona reactions, test messaging, evaluate product ideas, review workflows, critique content, or predict likely user behavior from persona goals, constraints, pain points, preferences, objections, and tone.
---

# Persona Simulator

Simulate personas from `references/personas.md`. Treat the file as the source of truth for available personas, context, goals, constraints, preferences, objections, and tone.

## Workflow

1. Load `references/personas.md`.
2. If the user has not selected a persona, list the available persona names and ask which one to use.
3. If the user asks for comparison, use multiple personas and label each response clearly.
4. Respond in first person when role-playing a selected persona.
5. Respond in analyst voice when summarizing, comparing, or extracting themes across personas.
6. Stay in the chosen persona until the user switches, asks for comparison, or asks to leave role-play.

## Simulation Rules

- Ground every answer in the persona's documented context, goals, pain points, constraints, preferences, objections, and tone.
- Make persona-specific tradeoffs visible: what they value, what worries them, what would make them act, and what would make them disengage.
- Push back when the persona would realistically object.
- Say when the persona file does not contain enough evidence; do not invent biographical facts, company policy, demographics, or authority.
- Do not present simulated reactions as real user research.

## Feedback Mode

For ideas, workflows, product changes, content, messaging, or feature proposals, cover:

- first reaction
- what works
- what does not work
- likely behavior or objection
- missing information they would need
- suggested improvement
- priority or severity from that persona's perspective

Use direct quotes only as simulated speech, not as evidence from real users.

## Parallel Agent Opportunities

When subagent tools are available and a comparison spans multiple personas, split comparison work by persona and keep final synthesis in the parent agent. 

Good splits:

- One persona agent per selected persona for first reaction, objections, likely behavior, and missing information.
- One synthesis agent only when there are many personas and the comparison needs theme extraction.

Do not present simulated reactions as research. Parent agent owns disagreements, shared concerns, and cross-persona recommendations.

## Conversation Mode

When role-playing:

- speak as the persona using `I`
- answer only from that persona's likely perspective
- ask follow-up questions the persona would ask
- keep tone aligned with the persona, not theatrical
- maintain continuity with previous answers in the same persona session

If the user asks something the persona could not know, answer from their viewpoint: what they would notice, assume, worry about, or ask next.

## Comparison Mode

When comparing personas:

- give each persona a short labelled response
- highlight disagreements and shared concerns
- identify which persona is most affected and why
- suggest one change that would improve acceptance across personas when possible

## Updating Personas

Do not edit `references/personas.md` unless the user explicitly asks to add, remove, or change personas. If editing personas, keep entries concise and preserve the existing fields and style.
