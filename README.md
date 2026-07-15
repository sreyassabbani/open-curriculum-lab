# Canvas WCAG 2.1 AA content audit

Read-only audit tooling for Canvas Page body content. It inventories unique module
pages through the Canvas API, scans rendered bodies with the official
`@axe-core/playwright` integration, runs a small set of Canvas-authoring checks,
and writes Markdown remediation reports.

## Run

```sh
nix develop --command npm install
nix develop --command uv sync
nix develop --command python audit_canvas.py
nix develop --command python audit_canvas.py --use-cache
```

The live API run requires `CANVAS_ACCESS_TOKEN` in `.env`; a cached run does not.
Neither mode modifies Canvas content.

Outputs:

- `reports/WCAG_2.1_AA_AUDIT.md` — status matrix, exact findings, manual checks,
  empty pages, method, and limitations.
- `reports/WCAG_2.1_AA_FIX_LIST.md` — affected-page working queue.
- `reports/axe-results.json` — ignored native axe result sets and tool/browser
  versions. Query-string access tokens and Canvas verifier values are redacted.

Automated axe failures are authoritative for the DOM scanned, but do not prove
WCAG conformance. Filename-style alt text and a fixed vocabulary of vague link
labels are deterministic HTML defects. Data-table, document, media,
layout/reading-order, keyboard, zoom, and reflow checks remain manual review.

Local fragment rendering cannot perfectly reproduce authenticated Canvas course
CSS. Before remediation, compare representative contrast, table, image-heavy,
media, and axe-clean pages in live Canvas and run the Rich Content Editor
Accessibility Checker.

## Python deps

This project uses `uv`.

- Add dependencies with `uv add <package>`
- Sync the environment with `uv sync`
- Generate or refresh the lockfile with `uv lock`

Commit `uv.lock` once you want reproducible installs across machines or CI.

## MATH 1554 Canvas lesson skill

The repo-scoped `$build-math1554-lesson` skill turns the Kaltura captions for a
topic into one validated Canvas HTML lesson. Invoke it from Codex with a Canvas
topic number, media prefix, or title, for example:

```text
Use $build-math1554-lesson to build the lesson for 4.3.
```

The skill uses the helper directly for deterministic stages:

```sh
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py prepare 4.3
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py validate RUN_DIR
nix develop --command python .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py render RUN_DIR
```

Successful validation writes the stable copy to `output/lessons/`. Preparation,
raw captions, previews, reports, and Canvas backups stay under the ignored
`.cache/lesson-pipeline/` directory.

Canvas writes are separate and guarded. `publish` requires the exact target-page
slug, aborts if the page changed after preparation, preserves its title and
publication state, and disables update notifications. The skill must obtain
explicit confirmation before it runs either `publish` or `rollback`.
