---
name: build-math2551-lesson
description: Prepare a source bundle for a Georgia Tech MATH 2551 Canvas Topic-to-Lesson assignment. Use when the user names a MATH 2551 textbook section such as 4.3 and wants to inspect, retrieve captions for, or draft the matching Canvas lesson.
---

# Build a MATH 2551 Canvas Lesson

Use this skill only for the MATH 2551 course (Canvas course ID `588672`). Do not use the MATH 1554 skill or its linear-algebra writing rubric for this course.

## Resolve the source and target

MATH 2551 uses `Topic` pages as sources and blank `Lesson` pages as targets. A topic can have an internal sequence number and a textbook section in parentheses; for example, `Topic 2.3: Partial Derivatives (4.3)` supplies the source for `Lesson 4.3: Partial Derivatives`.

Run the deterministic preparation step first:

```sh
direnv exec . sh -c 'unset VIRTUAL_ENV; "$PWD/.venv/bin/python" .agents/skills/build-math2551-lesson/scripts/canvas_lesson.py prepare 4.3 --target-page-slug lesson-4-dot-3-partial-derivatives'
```

The command is read-only with respect to Canvas. It may create an ignored local source bundle only after every caption has been retrieved and normalized.

If the Canvas API launch does not expose captions but an authenticated browser player does, export or download each English caption file in page order and prepare from those files instead:

```sh
direnv exec . sh -c 'unset VIRTUAL_ENV; "$PWD/.venv/bin/python" .agents/skills/build-math2551-lesson/scripts/canvas_lesson.py prepare 4.3 --target-page-slug lesson-4-dot-3-partial-derivatives --caption-file /path/to/lesson-1.srt --caption-file /path/to/lesson-2.srt'
```

## Source requirements

Do not draft, validate, render, or return lesson HTML until preparation has produced a complete `manifest.json`, `source-bundle.md`, and nonempty raw caption file for every source video. Captions are the mathematical source of truth.

This course's Kaltura media is launched through a Canvas external-tool iframe, not the MATH 1554 `resource_link_lookup_uuid` format. The helper uses Canvas's token-authenticated sessionless-launch endpoint and follows its form/JavaScript handoffs. If Kaltura does not expose a caption-authorized player configuration, stop and report that a browser-authenticated Kaltura session or exported English captions are required. Do not draft from the title, page HTML, or general mathematical knowledge.

Never print or copy the Canvas token, launch URLs, Kaltura sessions, signed media URLs, or caption URLs.

## Subsequent authoring

Before authoring after a successful source bundle, inspect a published MATH 2551 lesson in the same course and establish a course-specific writing and validation rubric. Keep Canvas publishing separate and require explicit user confirmation of the exact target-page slug immediately before any update.
