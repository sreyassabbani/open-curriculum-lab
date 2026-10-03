---
name: build-math2551-lesson
description: Build or revise Georgia Tech MATH 2551 Canvas lessons from course videos and the matching OpenStax Calculus Volume 3 section, with the course topic sequence controlling scope.
---

# Build a MATH 2551 Canvas Lesson

Use this skill only for the MATH 2551 course (Canvas course ID `588672`). Do not use the MATH 1554 skill or its linear-algebra writing rubric for this course.

## Resolve the source and target

MATH 2551 uses `Topic` pages as sources and blank `Lesson` pages as targets. A topic can have an internal sequence number and a textbook section in parentheses; for example, `Topic 2.3: Partial Derivatives (4.3)` supplies the source for `Lesson 4.3: Partial Derivatives`.

Run the deterministic preparation step first, replacing the example section and slug with the resolved target:

```sh
direnv exec . sh -c 'unset VIRTUAL_ENV; "$PWD/.venv/bin/python" .agents/skills/build-math2551-lesson/scripts/canvas_lesson.py prepare 4.3 --target-page-slug lesson-4-dot-3-partial-derivatives'
```

The command is read-only with respect to Canvas. It may create an ignored local source bundle only after every caption has been retrieved and normalized.

If the Canvas API launch does not expose captions but an authenticated browser player does, export or download each English caption file in page order and prepare from those files instead:

```sh
direnv exec . sh -c 'unset VIRTUAL_ENV; "$PWD/.venv/bin/python" .agents/skills/build-math2551-lesson/scripts/canvas_lesson.py prepare 4.3 --target-page-slug lesson-4-dot-3-partial-derivatives --caption-file /path/to/lesson-1.srt --caption-file /path/to/lesson-2.srt'
```

## Source requirements

Do not draft, validate, render, or return lesson HTML until preparation has produced a complete `manifest.json`, `source-bundle.md`, and nonempty raw caption file for every source video. Captions establish what the course video actually teaches; mathematical claims and examples should be checked against the video and a reliable text source, especially when a caption is ambiguous.

This course's Kaltura media is launched through a Canvas external-tool iframe, not the MATH 1554 `resource_link_lookup_uuid` format. The helper uses Canvas's token-authenticated sessionless-launch endpoint and follows its form/JavaScript handoffs. If Kaltura does not expose a caption-authorized player configuration, stop and report that a browser-authenticated Kaltura session or exported English captions are required. Do not draft from the title, page HTML, or general mathematical knowledge.

Never print or copy the Canvas token, launch URLs, Kaltura sessions, signed media URLs, or caption URLs.

## Subsequent authoring

Decide what the lesson needs to explain before choosing its layout. Use connected prose for reasoning, lists for distinct items or ordered actions, and tables for useful comparisons. Add headings and callouts only where they help the reader. Let the material determine the structure; avoid unnecessary labels, repeated summaries, or forcing every concept into the same definition/example/check template.

Read the matching section of [OpenStax Calculus Volume 3](https://openstax.org/details/books/calculus-volume-3) alongside all source captions. Treat them as parallel sources: use the captions for course emphasis and examples, and the textbook for definitions, conditions, geometric explanations, and useful checks. Do not assume a one-to-one match. Before choosing objectives and examples, inspect the neighboring Canvas Topic and Lesson titles and the relevant OpenStax sections; use [course context](references/course-context.md) as a starting map, then verify the current course. When a source video previews material assigned to a later lesson, acknowledge the connection briefly and leave the full derivation and practice to that later lesson. Resolve genuine source disagreements explicitly rather than silently copying a caption error.

Place short comprehension checks immediately after the concept or worked example they test. Space them through the lesson, with answers near each question; do not collect them in a final quiz section. Check that objectives, summary material, and study links reflect the actual lesson scope.

For math markup and rendering repairs, read the shared [Canvas math reference](../build-math1554-lesson/references/canvas-math.md). This technical reference applies to both courses; it does not import the MATH 1554 content rubric. Check inline notation as well as centered display equations on the live Canvas page after rendering completes.

Before authoring after a successful source bundle, inspect an existing MATH 2551 lesson in the same course for local formatting and accessibility conventions. Save and read back the exact target page, preserve its published state, and verify the rendered math and expanded checks. Publishing is a separate action requiring explicit authorization.
