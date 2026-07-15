---
name: build-math1554-lesson
description: Create, review, preview, and optionally publish unified MATH 1554 Canvas lecture-note lessons from the course's Kaltura captions. Use when a user supplies a topic number such as 4.3, a media prefix such as M4W11T1, or a topic title and asks to download transcripts, build or revise lecture notes, produce Canvas-ready HTML, or update the matching Canvas lecture-notes page.
---

# Build a MATH 1554 Canvas Lesson

Create one transcript-grounded lesson through the deterministic helper and an agent writing/review loop. Keep Canvas writes separate from preparation and require explicit confirmation.

## Set up

1. Read [references/lesson-rules.md](references/lesson-rules.md) completely before drafting or reviewing a lesson.
2. Run commands from the repository root.
3. Use the project environment:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py COMMAND
```

Use `CANVAS_ACCESS_TOKEN` from the repository `.env`. Never print or copy that token, a Kaltura session, a signed caption URL, or Canvas verifier values.

## Prepare the source bundle

Run:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py prepare "TOPIC"
```

Accept topic forms such as `4.3`, `M4W11T1`, or `Orthogonal Projections`. If resolution is ambiguous, show the candidates and ask the user to choose; do not guess. Use `--target-page-slug SLUG` only when the user identifies an existing lecture-notes page.

Read the returned `manifest.json`, `source-bundle.md`, and raw caption files. Treat the raw captions as the mathematical source of truth and use the normalized bundle for convenient reading. Do not add facts merely because they are commonly associated with the topic.

## Draft the lesson

Write the complete Canvas fragment to `RUN_DIR/lesson.html` using the rules reference. Synthesize every source into one lesson rather than producing one section per video.

Preserve useful examples and definitions while removing timestamps, caption artifacts, repetition, instructor false starts, and references to the source medium. Resolve an obvious caption error only when the surrounding mathematics makes the intended statement clear. Avoid unnecessary specificity when the source remains ambiguous.

Default to four to six assessment-style comprehension checks. Use a seventh only when it tests a distinct, useful idea. Prefer turning a meaningful simplification or inference into a check instead of stating it immediately beforehand. Remove process boxes that merely repeat an adjacent formula or worked example.

## Review independently

Ask one independent reviewer agent, when reviewer agents are available, to compare these raw inputs without editing the file:

- `references/lesson-rules.md`
- `RUN_DIR/manifest.json`
- every raw caption file listed by the manifest
- `RUN_DIR/lesson.html`

Request only a structured list of unsupported claims, missing source concepts, mathematical errors, formatting violations, redundant material, and comprehension-check problems. Do not give the reviewer an expected answer or prior diagnosis. When reviewer agents are unavailable, perform the same rubric as a distinct fresh review pass.

Revise the lesson for every confirmed issue. Stop after three write/review cycles and report unresolved issues instead of weakening the rubric.

## Validate and preview

Run deterministic validation:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py validate RUN_DIR
```

Fix every error and rerun it. Warnings require judgment but do not block local output. A successful validation copies the final fragment to the stable `output/lessons/` path recorded in the manifest.

Render and inspect the complete screenshot:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py render RUN_DIR
```

Inspect `preview.png` for clipped content, unreadable math, broken tables, weak spacing, or malformed disclosure blocks. Revise and repeat validation after any change.

## Publish only after confirmation

Local generation does not authorize a Canvas update. Show the user the final output path, validation status, target page title, exact slug, and publication state. Ask whether to publish that exact page.

After affirmative confirmation, pass the exact slug:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py publish RUN_DIR --confirm-slug EXACT_SLUG
```

The helper aborts if the Canvas body changed after preparation. It preserves the page title and publication state, disables update notifications, saves the returned body, and validates it again. Report post-publication errors immediately; do not roll back automatically.

Rollback also requires a new explicit confirmation:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py rollback RUN_DIR --confirm-slug EXACT_SLUG
```

Do not create, rename, publish, or unpublish pages through this workflow.
