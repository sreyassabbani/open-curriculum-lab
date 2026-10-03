# Developer guide

For the current project status and review questions, start with the [project review](review.md).
This guide covers the local repository tools; it is not setup required of ChatGPT users.

This repository explores how the Canvas API and agent workflows can reduce the
manual work involved in maintaining online course content. It began as a proof
of concept for MATH 1554, but the underlying ideas—course-content inventory,
accessibility auditing, transcript-grounded authoring, and guarded publishing—
are intended to be useful across Canvas courses.

The project currently contains three related pieces:

1. **Canvas API proof of concept:** inventory the unique Canvas pages used in a
   course and identify lecture-note pages in module order.
2. **Automated accessibility audit:** scan Canvas page bodies for detectable
   WCAG 2.1 A/AA issues and produce remediation reports.
3. **End-to-end lecture-notes experiment:** collect Kaltura captions for a topic,
   use an agent workflow to draft and review a unified lesson, validate the
   resulting HTML, render a preview, and optionally publish it to an existing
   Canvas page.

These are experiments, not a replacement for instructor review or a complete
accessibility evaluation. Test write operations against a course copy whenever
possible.

## Setup

The development environment uses Nix, Python 3.12, `uv`, Node.js, Playwright,
and axe-core.

```sh
nix develop --command uv sync
nix develop --command npm install
```

Create a `.env` file containing a Canvas access token:

```dotenv
CANVAS_ACCESS_TOKEN=your_token_here
```

The current scripts default to the Georgia Tech Canvas instance and the MATH
1554 course used during development. Override the API URL or course ID through
the relevant command-line options when working with another course. Never
commit `.env`, Canvas access tokens, Kaltura sessions, or signed media URLs.

## Canvas API proof of concept

[`main.py`](../main.py) uses `canvasapi` to list unique Page items from the course
modules and print the subset whose titles contain “lecture notes.” It is a small
reference for authentication, course access, module traversal, and page lookup.

```sh
nix develop --command python main.py
```

This command is read-only.

## Experiment 1: automated WCAG checks

[`audit_canvas.py`](../audit_canvas.py) inventories unique module pages, renders
their HTML, runs the official `@axe-core/playwright` integration, and applies a
small set of deterministic Canvas-authoring checks.

```sh
# Fetch current page content from Canvas and run the audit
nix develop --command python audit_canvas.py

# Repeat the audit using the locally cached Canvas responses
nix develop --command python audit_canvas.py --use-cache
```

Neither mode modifies Canvas. The audit produces:

- [`reports/WCAG_2.1_AA_AUDIT.md`](../reports/WCAG_2.1_AA_AUDIT.md): findings,
  status matrix, manual checks, methodology, and limitations.
- [`reports/WCAG_2.1_AA_FIX_LIST.md`](../reports/WCAG_2.1_AA_FIX_LIST.md): a working
  remediation queue grouped by affected page.
- `reports/axe-results.json`: raw axe results and tool/browser versions, with
  query-string tokens and Canvas verifier values redacted.

Automated results cover only issues detectable in the rendered DOM. Data-table
semantics, documents, media, reading order, keyboard behavior, zoom, reflow,
and other contextual checks still require manual review. Local rendering also
cannot reproduce every detail of an authenticated Canvas course theme, so
representative pages should be checked in Canvas and with the Rich Content
Editor Accessibility Checker before remediation is considered complete.

## Experiment 2: agent-driven lecture-note building

The repo-scoped [`$build-math1554-lesson`](../.agents/skills/build-math1554-lesson/SKILL.md)
skill turns the Kaltura captions associated with a lecture topic into one
reviewed, Canvas-ready HTML lesson. A topic can be supplied as a section number,
media prefix, or title:

```text
Use $build-math1554-lesson to build the lesson for 4.3.
```

The skill coordinates the agent’s drafting and review passes. Its helper script
handles the deterministic stages:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py prepare 4.3
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py validate RUN_DIR
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py render RUN_DIR
```

Preparation resolves the relevant Canvas video and notes pages, performs an
authenticated Kaltura launch, downloads ready English captions, and creates a
source bundle. Successful validation copies the final HTML fragment to
`output/lessons/`. Raw captions, previews, validation reports, and Canvas
backups remain under the ignored `.cache/lesson-pipeline/` directory.

Canvas writes are deliberately separate from content generation. Publishing:

- requires explicit user approval and the exact target-page slug;
- aborts if the Canvas page changed after preparation;
- updates only the body while preserving the title and publication state;
- disables update notifications; and
- runs validation again on the body returned by Canvas.

Rollback requires a separate explicit confirmation. The workflow does not
create, rename, publish, or unpublish pages.

## MATH 2551 source preparation

The [MATH 2551 skill](../.agents/skills/build-math2551-lesson/SKILL.md) is separate
from the MATH 1554 content rubric. Its helper currently implements **preparation
only**: it resolves the course Topic and target Lesson, retrieves captions where
possible, and accepts authenticated caption exports when automatic retrieval
fails. It does not provide MATH 2551 `validate`, `render`, or `publish` commands.
The earlier Lesson 4.3 Canvas update was a separate authorized operation.

After complete sources are available, the authoring instructions require
reading all captions and the relevant OpenStax sections in parallel, checking
the actual course sequence, and distributing comprehension checks through the
lesson. See the [course context map](../.agents/skills/build-math2551-lesson/references/course-context.md).
Shared HTML validation and preview helpers may assist an operator, but the
MATH 1554 writing rubric must not be imposed on MATH 2551. A local preview does
not verify the saved Canvas page.

The [ChatGPT plugin](https://chatgpt.com/plugins/plugins_6ab86870d7b881919c72a9eef0635517)
is a separate, currently private instruction package. Users supply source
materials to it; it has no live Canvas connection and does not load repository
scripts automatically. The [Canvas connection prototype](https://github.com/sreyassabbani/open-curriculum-lab/tree/canvas-mcp-bridge/canvas_bridge)
is on an experimental branch and is deferred, not deployed.

## Development

Python dependencies are managed with `uv`:

```sh
uv add <package>
uv sync
uv lock
```

Run the lesson-pipeline tests and lint checks with:

```sh
nix develop --command python -m unittest discover -s tests -v
nix develop --command ruff check .
```
