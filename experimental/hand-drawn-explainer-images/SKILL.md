---
name: hand-drawn-explainer-images
description: >-
  Create raster explainer images with a polished hand-drawn infographic style similar to a personalized "many hats" poster: warm paper background, large hand-lettered title, central portrait or subject, labeled role cards, arrows, icons, checklists, small doodles, and limited accent colors. Use when the user asks Codex to generate, edit, or prompt for illustrated explainer images, visual summaries, personal/team role maps, product explainers, concept posters, capability maps, or infographic-style images inspired by a provided reference image.
---

# Hand-Drawn Explainer Images

## Workflow

1. Identify the core subject, audience, and message from the user request.
2. Ask only for missing factual content that cannot be reasonably inferred, such as a person's exact roles, product facts, or required wording.
3. Read `references/style-guide.md` before writing an image prompt.
4. Produce an image-generation prompt that specifies composition, text hierarchy, illustration style, palette, subject treatment, panels, icons, and negative constraints.
5. If generating directly, use the image tool with the finished prompt. If not generating directly, give the user the prompt and a short note about any assumptions.

## Prompt Structure

Use this order when writing prompts:

1. Format and purpose: "wide illustrated explainer poster" or the requested aspect ratio.
2. Main subject: person, product, process, concept, or organization.
3. Title and subtitle text.
4. Layout: central subject plus surrounding cards, arrows, bottom ribbon, footer badges, notes, or scene panel.
5. Card content: short headings, concise bullets, icons, and color accents.
6. Visual treatment: hand-drawn ink lines, soft watercolor shading, warm off-white paper, playful but legible lettering.
7. Quality controls: accurate spelling, no cramped text, no extra unreadable words, no photorealistic corporate template look.

## Text Rules

- Keep generated image text short enough to fit: headings under 5 words, bullets under 6 words where possible.
- Prefer 4-6 surrounding cards for a wide poster, or 2-3 cards for a square/portrait image.
- Use sentence case for subtitles and compact title case for card headings.
- Tell the image model to preserve exact supplied names, titles, and labels.
- When the user provides lots of prose, summarize into image-safe labels instead of trying to place paragraphs.

## Output Expectations

- For direct generation, call the image generation tool with one complete prompt.
- For prompt-only requests, return one final prompt, not a long explanation.
- For iterations, preserve the established layout unless the user asks for a structural change.
