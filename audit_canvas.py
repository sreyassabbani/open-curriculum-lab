from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from canvasapi import Canvas
from dotenv import load_dotenv

DEFAULT_API_URL = "https://gatech.instructure.com"
DEFAULT_COURSE_ID = 563104
ROOT = Path(__file__).resolve().parent
CACHE_PATH = ROOT / ".cache" / "canvas_pages.json"
AXE_RUNNER_PATH = ROOT / "axe_runner.mjs"
CHROME_PATH = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
REPORT_DIR = ROOT / "reports"
RAW_AXE_PATH = REPORT_DIR / "axe-results.json"

WCAG_LEVELS = {
    "1.1.1": "A",
    "1.2.1": "A",
    "1.2.2": "A",
    "1.2.3": "A",
    "1.2.4": "AA",
    "1.2.5": "AA",
    "1.3.1": "A",
    "1.3.2": "A",
    "1.3.3": "A",
    "1.3.4": "AA",
    "1.3.5": "AA",
    "1.4.1": "A",
    "1.4.2": "A",
    "1.4.3": "AA",
    "1.4.4": "AA",
    "1.4.5": "AA",
    "1.4.10": "AA",
    "1.4.11": "AA",
    "1.4.12": "AA",
    "1.4.13": "AA",
    "2.1.1": "A",
    "2.1.2": "A",
    "2.1.4": "A",
    "2.2.1": "A",
    "2.2.2": "A",
    "2.3.1": "A",
    "2.4.1": "A",
    "2.4.2": "A",
    "2.4.3": "A",
    "2.4.4": "A",
    "2.4.5": "AA",
    "2.4.6": "AA",
    "2.4.7": "AA",
    "2.5.1": "A",
    "2.5.2": "A",
    "2.5.3": "A",
    "2.5.4": "A",
    "3.1.1": "A",
    "3.1.2": "AA",
    "3.2.1": "A",
    "3.2.2": "A",
    "3.2.3": "AA",
    "3.2.4": "AA",
    "3.3.1": "A",
    "3.3.2": "A",
    "3.3.3": "AA",
    "3.3.4": "AA",
    "4.1.1": "A",
    "4.1.2": "A",
    "4.1.3": "AA",
}

IMPACT_TO_SEVERITY = {
    "critical": "Critical",
    "serious": "High",
    "moderate": "Medium",
    "minor": "Low",
    None: "Medium",
}
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

FIXES = {
    "image-alt": "Edit the image in Canvas and add concise alternative text that communicates its purpose. If it is purely decorative, set an empty alt attribute (`alt=\"\"`) instead.",
    "input-image-alt": "Give the image button alternative text that describes the action it performs.",
    "link-name": "Give the link visible, descriptive text (or an accessible name when no visible text is possible) that identifies its destination or action.",
    "button-name": "Give the button visible text or an `aria-label` that describes its action.",
    "frame-title": "Add a short, unique `title` attribute to the iframe describing the embedded content, such as `title=\"Lecture 4.3 video\"`.",
    "color-contrast": "Change the foreground or background color until normal text reaches 4.5:1 and large text reaches 3:1. Preserve the meaning without relying on color alone.",
    "heading-order": "Retag headings so levels do not skip (for example, change an H4 following an H2 to H3). Do not choose heading levels for visual size.",
    "empty-heading": "Delete the empty heading or add meaningful heading text.",
    "list": "Wrap list items in a semantic `<ul>` or `<ol>` element using the Canvas list controls.",
    "listitem": "Place this `<li>` inside a semantic `<ul>` or `<ol>`.",
    "definition-list": "Use valid `<dt>` and `<dd>` children inside the definition list.",
    "dlitem": "Place the definition term/description inside a `<dl>`.",
    "table-fake-caption": "Use a real table `<caption>` or nearby heading instead of a table cell styled to look like a caption.",
    "td-has-header": "Add appropriate row or column header cells (`<th>`) so each data cell has a programmatic header association.",
    "td-headers-attr": "Correct the cell's `headers` attribute so it references valid table-header IDs.",
    "th-has-data-cells": "Remove the unused header cell or associate it with the data cells it labels.",
    "aria-required-attr": "Add the ARIA attributes required by this role, or replace the custom role with the correct native HTML element.",
    "aria-valid-attr-value": "Replace the invalid ARIA value with a value allowed for that attribute.",
    "aria-valid-attr": "Correct or remove the misspelled/unsupported ARIA attribute.",
    "aria-roles": "Use a valid ARIA role, preferably replacing it with the equivalent native HTML element.",
    "aria-prohibited-attr": "Remove the prohibited ARIA attribute or use an element/role that supports it.",
    "duplicate-id-aria": "Give every referenced element a unique `id`, then update `aria-labelledby`, `aria-describedby`, or table header references accordingly.",
    "select-name": "Associate the select menu with a visible `<label>` or an equivalent accessible name.",
    "label": "Associate the form control with a visible `<label for=\"...\">` whose `for` value matches the control ID.",
    "html-has-lang": "Set the document language. This is normally controlled by Canvas rather than page-body content.",
    "canvas-h1": "Change this H1 to H2. Canvas already supplies the page title as the page-level H1; content headings should begin at H2.",
    "vague-link-text": "Replace vague link text with wording that makes sense out of context, such as `Download the Exam 1 review (PDF)` instead of `click here`.",
    "data-table-headers": "In the Canvas table editor, mark the first row and/or first column as header cells. Use `scope=\"col\"` or `scope=\"row\"` for simple tables.",
    "filename-alt": "Replace the filename-style alt text with a concise description of the image's purpose. If the image is only decorative, use empty alt text instead.",
}

VAGUE_LINK_TEXT = {
    "click here",
    "here",
    "learn more",
    "more",
    "read more",
    "link",
    "this link",
    "website",
    "go here",
}
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
MEDIA_HOST_MARKERS = ("youtube", "youtu.be", "kaltura", "mediaspace", "vimeo", "panopto")
ALT_REPLACEMENTS = {
    "compass.png": "",
    "description1.png": "",
    "objectives4.png": "",
    "task3.png": "",
    "read.png": "",
    "watchvideo.png": "",
    "easy1.png": "Easy difficulty",
    "medium1.png": "Medium difficulty",
    "hard1.png": "Hard difficulty",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Canvas page bodies for WCAG 2.1 AA issues.")
    parser.add_argument("--course-id", type=int, default=DEFAULT_COURSE_ID)
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--use-cache", action="store_true", help="Use the last downloaded Canvas page cache.")
    parser.add_argument("--workers", type=int, default=8)
    return parser.parse_args()


def markdown_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def code_snippet(value: str, limit: int = 360) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    compact = re.sub(
        r"([?&](?:verifier|access_token|token)=)[^&\"'\s>]+",
        r"\1REDACTED",
        compact,
        flags=re.I,
    )
    if len(compact) > limit:
        compact = compact[: limit - 1].rstrip() + "…"
    return compact.replace("```", "` ` `")


def page_url(api_url: str, course_id: int, slug: str) -> str:
    return f"{api_url.rstrip('/')}/courses/{course_id}/pages/{quote(slug, safe='')}"


def page_edit_url(api_url: str, course_id: int, slug: str) -> str:
    return f"{page_url(api_url, course_id, slug)}/edit"


def wcag_criteria(tags: list[str]) -> list[str]:
    criteria = []
    for tag in tags:
        match = re.fullmatch(r"wcag(\d)(\d)(\d+)", tag)
        if match:
            criterion = ".".join(match.groups())
            if criterion in WCAG_LEVELS and criterion not in criteria:
                criteria.append(criterion)
    return criteria


def criterion_label(criteria: list[str]) -> str:
    if not criteria:
        return "WCAG 2.1 A/AA"
    return ", ".join(f"{item} ({WCAG_LEVELS[item]})" for item in criteria)


def get_module_page_index(api_url: str, course_id: int, token: str) -> list[dict[str, Any]]:
    canvas = Canvas(api_url, token)
    course = canvas.get_course(course_id)
    pages = []
    seen = set()
    for module in course.get_modules(include=["items"]):
        for item in module.items:
            slug = item.get("page_url")
            if item.get("type") != "Page" or not slug or slug in seen:
                continue
            seen.add(slug)
            pages.append(
                {
                    "module": module.name,
                    "module_id": module.id,
                    "title": item.get("title", slug),
                    "slug": slug,
                    "module_published": bool(item.get("published")),
                }
            )
    return pages


def fetch_one_page(
    meta: dict[str, Any], api_url: str, course_id: int, token: str
) -> dict[str, Any]:
    endpoint = f"{api_url.rstrip('/')}/api/v1/courses/{course_id}/pages/{quote(meta['slug'], safe='')}"
    try:
        response = requests.get(
            endpoint,
            headers={"Authorization": f"Bearer {token}"},
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        return {
            **meta,
            "title": payload.get("title") or meta["title"],
            "page_id": payload.get("page_id"),
            "published": bool(payload.get("published")),
            "updated_at": payload.get("updated_at"),
            "body": payload.get("body") or "",
            "error": None,
        }
    except Exception as exc:  # the report records page-specific API failures
        return {**meta, "body": "", "error": f"{type(exc).__name__}: {exc}"}


def download_pages(
    api_url: str, course_id: int, token: str, workers: int
) -> list[dict[str, Any]]:
    index = get_module_page_index(api_url, course_id, token)
    print(f"Found {len(index)} unique Canvas page module items.", flush=True)
    results: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(fetch_one_page, item, api_url, course_id, token): item
            for item in index
        }
        for number, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results[result["slug"]] = result
            if number % 10 == 0 or number == len(index):
                print(f"Downloaded {number}/{len(index)} pages…", flush=True)
    pages = [results[item["slug"]] for item in index]
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps(
            {
                "api_url": api_url,
                "course_id": course_id,
                "downloaded_at": datetime.now(UTC).isoformat(),
                "pages": pages,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return pages


def load_cached_pages(api_url: str, course_id: int) -> list[dict[str, Any]]:
    data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    if data.get("api_url") != api_url or data.get("course_id") != course_id:
        raise ValueError("The cache belongs to a different Canvas instance or course.")
    return data["pages"]


def fix_for(rule_id: str, fallback: str) -> str:
    return FIXES.get(rule_id, re.sub(r"^Fix (?:any|all) of the following:\s*", "", fallback).strip())


def axe_findings(result: dict[str, Any], page: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    failures = []
    reviews = []
    for result_key, destination in (("violations", failures), ("incomplete", reviews)):
        for rule in result.get(result_key, []):
            criteria = wcag_criteria(rule.get("tags", []))
            for node in rule.get("nodes", []):
                summary = node.get("failureSummary") or rule.get("description") or rule.get("help", "")
                target = " | ".join(
                    " > ".join(part) if isinstance(part, list) else str(part)
                    for part in node.get("target", [])
                )
                fix = fix_for(rule["id"], summary)
                if rule["id"] == "color-contrast" and "#27ae60" in node.get("html", "").lower():
                    fix = "Change the heading color from `#27ae60` to `#1e7e45`; against its `#eafaf1` background this raises contrast from 2.66:1 to 4.71:1. Keep the checkmark so the status is not communicated by color alone."
                destination.append(
                    {
                        "kind": "automated" if result_key == "violations" else "manual",
                        "rule_id": rule["id"],
                        "severity": IMPACT_TO_SEVERITY.get(rule.get("impact"), "Medium"),
                        "criteria": criteria,
                        "criterion_label": criterion_label(criteria),
                        "issue": rule.get("help", rule["id"]),
                        "impact": rule.get("description", ""),
                        "selector": target,
                        "evidence": code_snippet(node.get("html", "")),
                        "fix": fix,
                        "help_url": rule.get("helpUrl", ""),
                        "message": code_snippet(summary, 500),
                        "page_slug": page["slug"],
                    }
                )
    return failures, reviews


def is_probable_data_table(table: Tag) -> bool:
    if table.get("role") in {"presentation", "none"}:
        return False
    rows = table.find_all("tr")
    cells = [row.find_all(["th", "td"], recursive=False) for row in rows]
    populated_rows = [row for row in cells if len(row) >= 2]
    text_length = len(table.get_text(" ", strip=True))
    if len(populated_rows) < 2 or text_length < 20:
        return False
    if table.find("th") or table.find("thead"):
        return True
    border = str(table.get("border", "")).strip().lower()
    if border and border not in {"0", "0px", "none"}:
        return True
    first_row = populated_rows[0]
    emphasized = sum(bool(cell.find(["strong", "b"])) for cell in first_row)
    return bool(first_row) and emphasized / len(first_row) >= 0.6


def custom_checks(page: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    soup = BeautifulSoup(page["body"], "lxml")
    failures: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []

    def add(
        destination: list[dict[str, Any]],
        *,
        rule_id: str,
        severity: str,
        criteria: list[str],
        issue: str,
        impact: str,
        element: Tag,
        fix: str | None = None,
    ) -> None:
        destination.append(
            {
                "kind": "automated" if destination is failures else "manual",
                "rule_id": rule_id,
                "severity": severity,
                "criteria": criteria,
                "criterion_label": criterion_label(criteria),
                "issue": issue,
                "impact": impact,
                "selector": element.name,
                "evidence": code_snippet(str(element)),
                "fix": fix or FIXES[rule_id],
                "help_url": "",
                "message": "",
                "page_slug": page["slug"],
            }
        )

    for link in soup.find_all("a", href=True):
        text = " ".join(link.get_text(" ", strip=True).lower().split())
        href = str(link.get("href") or "").strip()
        if text in VAGUE_LINK_TEXT:
            link_fix = FIXES["vague-link-text"]
            date_match = re.search(r"(\d{2})-(\d{2})-(\d{4})", unquote(href))
            if text == "link" and date_match:
                month, day, year = map(int, date_match.groups())
                recording_date = datetime(year, month, day).strftime("%B %-d, %Y")
                link_fix = f"Replace the visible text `Link` with `Studio recording — {recording_date}`. Keep the existing Kaltura URL."
            add(
                failures,
                rule_id="vague-link-text",
                severity="High",
                criteria=["2.4.4"],
                issue=f"Link text is not descriptive out of context: {text!r}",
                impact="Screen-reader users often navigate by listing links; vague labels conceal the destination or purpose.",
                element=link,
                fix=link_fix,
            )
        path = urlparse(href).path.lower()
        if any(path.endswith(extension) for extension in DOCUMENT_EXTENSIONS):
            add(
                reviews,
                rule_id="linked-document-review",
                severity="Medium",
                criteria=["1.1.1", "1.3.1", "1.4.3", "2.4.2"],
                issue="Linked document requires a separate accessibility audit",
                impact="Accessible Canvas HTML does not make an inaccessible PDF, Word, PowerPoint, or spreadsheet attachment conformant.",
                element=link,
                fix="Audit the linked file in its native format. Ensure tagged structure, reading order, document title/language, alt text, table headers, and sufficient contrast; replace it with accessible HTML when practical.",
            )

    for image in soup.find_all("img"):
        if not image.has_attr("alt"):
            continue  # axe-core reports this as a failure
        alt = " ".join(str(image.get("alt") or "").split())
        if re.search(r"\.(?:png|jpe?g|gif|svg|webp)$", alt, re.I):
            replacement = ALT_REPLACEMENTS.get(alt.lower())
            if replacement is None:
                alt_fix = FIXES["filename-alt"]
            elif replacement:
                alt_fix = f"Replace `alt=\"{alt}\"` with `alt=\"{replacement}\"`."
            else:
                alt_fix = f"This icon repeats adjacent visible text; replace `alt=\"{alt}\"` with empty decorative alt text: `alt=\"\"`."
            add(
                failures,
                rule_id="filename-alt",
                severity="High",
                criteria=["1.1.1"],
                issue="Image alt text is a filename",
                impact="A filename usually does not provide the equivalent purpose or information available to sighted users.",
                element=image,
                fix=alt_fix,
            )
        elif re.fullmatch(
            r"(?:image|photo|picture|graphic|screenshot|diagram|chart|figure)(?:\s*\d+)?",
            alt,
            re.I,
        ) or len(alt) > 180:
            add(
                reviews,
                rule_id="alt-quality-review",
                severity="High",
                criteria=["1.1.1"],
                issue="Image alternative text may not communicate the image's purpose",
                impact="An alt attribute can technically exist while still withholding the information available visually.",
                element=image,
                fix="Rewrite the alt text to convey the same purpose or information as the image in this context. For a complex chart or derivation, add a nearby long description and keep the alt text concise.",
            )

    for table in soup.find_all("table"):
        if is_probable_data_table(table) and not table.find("th"):
            add(
                reviews,
                rule_id="data-table-headers",
                severity="High",
                criteria=["1.3.1"],
                issue="Probable data table has no header cells",
                impact="Screen readers cannot announce the row/column context of individual data cells.",
                element=table,
            )
        elif not is_probable_data_table(table) and len(table.find_all("tr")) >= 2:
            add(
                reviews,
                rule_id="layout-table-review",
                severity="Medium",
                criteria=["1.3.1", "1.3.2", "1.4.10"],
                issue="Probable layout table requires reading-order and reflow review",
                impact="A table used only for visual layout can expose misleading table semantics, create a confusing reading order, or prevent mobile reflow.",
                element=table,
                fix="If this table only positions icons/text, replace it with headings, paragraphs, and lists (or a responsive `<div>` layout). If retained, verify logical cell reading order and 320 CSS px reflow; use `role=\"presentation\"` only when it contains no tabular relationships.",
            )

    for media in soup.find_all(["video", "audio"]):
        add(
            reviews,
            rule_id="media-alternative-review",
            severity="High",
            criteria=["1.2.1", "1.2.2", "1.2.3", "1.2.5"],
            issue="Audio/video alternatives require manual verification",
            impact="Automated HTML inspection cannot determine whether captions, transcripts, and audio description are accurate and complete.",
            element=media,
            fix="Verify synchronized, accurate captions; provide a transcript; and provide audio description or an equivalent alternative when important visual information is not conveyed in the audio.",
        )

    for frame in soup.find_all("iframe"):
        src = str(frame.get("src") or "").lower()
        if any(marker in src for marker in MEDIA_HOST_MARKERS):
            add(
                reviews,
                rule_id="embedded-media-review",
                severity="High",
                criteria=["1.2.1", "1.2.2", "1.2.3", "1.2.5", "2.1.1"],
                issue="Embedded media accessibility requires manual verification",
                impact="The page source cannot confirm caption accuracy, transcript availability, audio description, or keyboard operation inside the third-party player.",
                element=frame,
                fix="Open the embedded player and verify keyboard operation, accurate synchronized captions, a transcript, and audio description/equivalent treatment for meaningful visuals.",
            )

    return failures, reviews


def render_document(page_data: dict[str, Any]) -> str:
    soup = BeautifulSoup(page_data["body"], "lxml")
    for script in soup.find_all("script"):
        script.decompose()
    fragment = soup.body.decode_contents() if soup.body else str(soup)
    title = escape(page_data["title"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>body {{ background: #fff; color: #2d3b45; font: 16px/1.5 Arial, sans-serif; }} #canvas-page {{ max-width: 1100px; margin: 0 auto; }}</style>
</head>
<body><main id="canvas-page">{fragment}</main></body>
</html>"""


def audit_pages(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not AXE_RUNNER_PATH.exists() or not (ROOT / "node_modules" / "@axe-core" / "playwright").exists():
        raise FileNotFoundError("Node audit dependencies are missing. Run `nix develop --command npm install`.")
    scan_pages = [page for page in pages if page.get("body") and not page.get("error")]
    payload = {
        "chromePath": str(CHROME_PATH) if CHROME_PATH.exists() else None,
        "pages": [{"slug": page["slug"], "document": render_document(page)} for page in scan_pages],
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8") as input_file:
        json.dump(payload, input_file)
        input_file.flush()
        subprocess.run(
            ["node", str(AXE_RUNNER_PATH), input_file.name, str(RAW_AXE_PATH)],
            cwd=ROOT,
            check=True,
        )
    raw_artifact = json.loads(RAW_AXE_PATH.read_text(encoding="utf-8"))
    raw_by_slug = {item["slug"]: item for item in raw_artifact["pages"]}
    audited = []
    completed = 0
    for page in pages:
        output = {**page, "findings": [], "manual_reviews": [], "axe_error": None}
        if page.get("error") or not page.get("body"):
            audited.append(output)
            continue
        completed += 1
        raw = raw_by_slug[page["slug"]]
        if raw.get("error"):
            output["axe_error"] = raw["error"]
        else:
            try:
                axe_result = raw["axe"]
                failures, reviews = axe_findings(axe_result, page)
                custom_failures, custom_reviews = custom_checks(page)
                output["findings"] = failures + custom_failures
                output["manual_reviews"] = reviews + custom_reviews
                output["axe_passes"] = len(axe_result.get("passes", []))
            except Exception as exc:
                output["axe_error"] = f"{type(exc).__name__}: {exc}"
        audited.append(output)
        if completed % 10 == 0 or completed == len(scan_pages):
            print(f"Audited {completed}/{len(scan_pages)} non-empty pages…", flush=True)
    return audited


def finding_sort_key(finding: dict[str, Any]) -> tuple[Any, ...]:
    return (
        SEVERITY_ORDER.get(finding["severity"], 99),
        finding["rule_id"],
        finding["selector"],
    )


def page_status(page: dict[str, Any]) -> str:
    if page.get("error") or page.get("axe_error"):
        return "Scan error"
    if not page.get("body"):
        return "Empty"
    if page["findings"]:
        return "Needs changes"
    if page["manual_reviews"]:
        return "Manual review"
    return "No automated failures"


def report_summary(audited: list[dict[str, Any]]) -> dict[str, Any]:
    findings = [finding for page in audited for finding in page["findings"]]
    reviews = [finding for page in audited for finding in page["manual_reviews"]]
    return {
        "pages": len(audited),
        "nonempty": sum(bool(page.get("body")) for page in audited),
        "empty": sum(not page.get("body") and not page.get("error") for page in audited),
        "errors": sum(bool(page.get("error") or page.get("axe_error")) for page in audited),
        "pages_with_findings": sum(bool(page["findings"]) for page in audited),
        "pages_with_reviews": sum(bool(page["manual_reviews"]) for page in audited),
        "findings": findings,
        "reviews": reviews,
        "severity": Counter(finding["severity"] for finding in findings),
        "rules": Counter(finding["rule_id"] for finding in findings),
    }


def finding_markdown(finding: dict[str, Any], number: int) -> list[str]:
    lines = [
        f"{number}. **{finding['severity']} — {finding['issue']}**",
        f"   - Type: {'axe failure' if finding['kind'] == 'automated' and finding['rule_id'] not in {'filename-alt', 'vague-link-text'} else ('deterministic HTML defect' if finding['kind'] == 'automated' else 'manual review')}",
        f"   - WCAG: {finding['criterion_label']}",
        f"   - Impact: {finding['impact']}",
    ]
    if finding.get("selector"):
        lines.append(f"   - Find: `{finding['selector']}`")
    if finding.get("evidence"):
        lines.append(f"   - Evidence: `{finding['evidence']}`")
    lines.append(f"   - Change: {finding['fix']}")
    lines.append("   - Rerun status: Not rerun after remediation")
    if finding.get("help_url"):
        lines.append(f"   - Reference: [{finding['rule_id']}]({finding['help_url']})")
    return lines


def generate_audit_report(
    audited: list[dict[str, Any]], api_url: str, course_id: int, generated_at: datetime
) -> str:
    summary = report_summary(audited)
    severity = summary["severity"]
    lines = [
        "# Canvas page-content accessibility audit — WCAG 2.1 AA",
        "",
        f"Generated: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "> **Scope:** HTML inside Canvas Page bodies for the course Modules list. Canvas global navigation/theme, quizzes, assignments, discussions, linked documents, and the internals of embedded media players are outside the automated scan.",
        "",
        "> **Conformance note:** Automated testing cannot prove WCAG conformance. Items under “Automated findings” are reproducible DOM failures or high-confidence content defects. Items under “Manual review” require human judgment before being called a failure.",
        "",
        "## Executive summary",
        "",
        f"- Module pages discovered: **{summary['pages']}**",
        f"- Non-empty pages audited: **{summary['nonempty']}**",
        f"- Empty pages excluded from testing: **{summary['empty']}**",
        f"- Pages with automated findings: **{summary['pages_with_findings']}**",
        f"- Pages with manual-review items: **{summary['pages_with_reviews']}**",
        f"- Scan errors: **{summary['errors']}**",
        f"- Automated findings: **{len(summary['findings'])}** — Critical {severity['Critical']}, High {severity['High']}, Medium {severity['Medium']}, Low {severity['Low']}",
        f"- Manual-review items: **{len(summary['reviews'])}**",
        "",
        "## Positive results",
        "",
        f"- **{summary['nonempty'] - summary['pages_with_findings']}** non-empty pages had no automated failures in the scoped page body.",
        f"- **{summary['pages'] - summary['nonempty']}** empty pages were inventoried without being misclassified as accessibility failures.",
        "- The inventory and browser scan completed with zero errors.",
        "",
        "## Findings by rule",
        "",
        "| Priority | Rule | Occurrences | Pages | Primary fix |",
        "|---|---|---:|---:|---|",
    ]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for page in audited:
        for finding in page["findings"]:
            grouped[finding["rule_id"]].append({**finding, "page": page})
    grouped_items = sorted(
        grouped.items(),
        key=lambda item: (
            min(SEVERITY_ORDER.get(f["severity"], 99) for f in item[1]),
            -len(item[1]),
            item[0],
        ),
    )
    for rule_id, items in grouped_items:
        priority = min(items, key=lambda f: SEVERITY_ORDER.get(f["severity"], 99))["severity"]
        page_count = len({item["page"]["slug"] for item in items})
        fix = markdown_text(items[0]["fix"])
        lines.append(f"| {priority} | `{rule_id}` | {len(items)} | {page_count} | {fix} |")

    lines.extend(
        [
            "",
            "## Page status index",
            "",
            "| Status | Published | Page | Module | Critical | High | Medium | Low | Manual |",
            "|---|---|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for page in audited:
        counts = Counter(finding["severity"] for finding in page["findings"])
        link = page_edit_url(api_url, course_id, page["slug"])
        lines.append(
            "| "
            + " | ".join(
                [
                    page_status(page),
                    "Yes" if page.get("published") else "No",
                    f"[{markdown_text(page['title'])}]({link}) (`{page['slug']}`)",
                    markdown_text(page["module"]),
                    str(counts["Critical"]),
                    str(counts["High"]),
                    str(counts["Medium"]),
                    str(counts["Low"]),
                    str(len(page["manual_reviews"])),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Affected page details", ""])
    for page in audited:
        if not page.get("body") or page.get("error") or not (page["findings"] or page["manual_reviews"] or page.get("axe_error")):
            continue
        link = page_edit_url(api_url, course_id, page["slug"])
        lines.extend(
            [
                f"### {page['title']}",
                "",
                f"- Canvas edit: [{page['slug']}]({link})",
                f"- Module: {page['module']}",
                f"- Published: {'Yes' if page.get('published') else 'No'}",
                f"- Last updated: {page.get('updated_at') or 'Unknown'}",
                f"- Status: **{page_status(page)}**",
                "",
            ]
        )
        if page.get("axe_error"):
            lines.extend([f"**Scan error:** `{page['axe_error']}`", ""])
            continue
        if page["findings"]:
            lines.extend(["#### Automated findings", ""])
            for number, finding in enumerate(sorted(page["findings"], key=finding_sort_key), start=1):
                lines.extend(finding_markdown(finding, number))
                lines.append("")
        else:
            lines.extend(["**No automated WCAG 2.1 A/AA failures detected in the page body.**", ""])
        if page["manual_reviews"]:
            lines.extend(["#### Manual review", ""])
            for number, review in enumerate(sorted(page["manual_reviews"], key=finding_sort_key), start=1):
                lines.extend(finding_markdown(review, number))
                lines.append("")

    empty_pages = [page for page in audited if not page.get("body") and not page.get("error")]
    lines.extend(["## Empty pages", "", "These pages contain no body HTML and were not assigned WCAG failures:", ""])
    for page in empty_pages:
        link = page_url(api_url, course_id, page["slug"])
        lines.append(f"- [{page['title']}]({link}) — `{page['slug']}`")

    error_pages = [page for page in audited if page.get("error") or page.get("axe_error")]
    if error_pages:
        lines.extend(["", "## Scan errors", ""])
        for page in error_pages:
            lines.append(f"- `{page['slug']}` — `{page.get('error') or page.get('axe_error')}`")

    lines.extend(
        [
            "",
            "## Manual completion checklist",
            "",
            "Complete these checks before claiming WCAG 2.1 AA conformance:",
            "",
            "- [ ] Keyboard-only: all links, controls, embeds, and disclosure widgets are reachable, operable, visibly focused, and free of traps (2.1.1, 2.1.2, 2.4.7).",
            "- [ ] Zoom/reflow: content works at 200% text zoom and at 320 CSS px without two-dimensional scrolling, except legitimately two-dimensional content (1.4.4, 1.4.10).",
            "- [ ] Images: every non-decorative image's alt text conveys its purpose in context; complex diagrams have an adjacent long description (1.1.1).",
            "- [ ] Color: information is not communicated by color alone; rendered text/non-text contrast is verified in every state (1.4.1, 1.4.3, 1.4.11).",
            "- [ ] Reading order: visual order matches DOM/screen-reader order, including tables and multi-column layouts (1.3.2).",
            "- [ ] Media: captions are accurate and synchronized; transcripts and audio description/equivalent alternatives are available where required (1.2.x).",
            "- [ ] Linked files: every PDF/Office file is separately audited for tags, reading order, title/language, alt text, tables, and contrast.",
            "- [ ] Math: equations expose meaningful MathML/LaTeX or equivalent text to assistive technology, not only an image without an equivalent (1.1.1).",
            "- [ ] Instructions do not rely only on shape, location, sound, or sensory characteristics (1.3.3).",
            "",
            "## Method",
            "",
            "- Exact page slugs and HTML were retrieved from the Canvas API.",
            "- Duplicate module references were deduplicated by slug while preserving Modules order.",
            "- Each non-empty body was rendered in local Chrome and tested through the official `@axe-core/playwright` integration using `wcag2a`, `wcag2aa`, `wcag21a`, and `wcag21aa` tags.",
            "- Native axe violations, incomplete results, passes, selectors, HTML evidence, help URLs, and tool/browser versions are retained in the ignored `reports/axe-results.json` artifact.",
            "- Additional Canvas-authoring checks cover filename-style image alt text and vague link text as deterministic defects; likely data tables, linked documents, media, layout tables, and contextual alt quality remain manual review.",
            "- Images/media were not downloaded; linked and embedded resources are represented as manual-review tasks.",
            "- Local fragment rendering does not reproduce every Canvas course-theme style. Contrast and layout findings must be parity-checked on representative authenticated live pages before remediation.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_fix_list(
    audited: list[dict[str, Any]], api_url: str, course_id: int, generated_at: datetime
) -> str:
    summary = report_summary(audited)
    lines = [
        "# Canvas WCAG 2.1 AA remediation checklist",
        "",
        f"Generated: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        f"Use this as the working queue. It contains **{len(summary['findings'])} automated findings across {summary['pages_with_findings']} pages**. Check an item only after editing Canvas and rerunning `python audit_canvas.py`.",
        "",
        "## Recommended order",
        "",
        "1. Critical and High automated findings (access blocked or WCAG A failures).",
        "2. Medium automated findings (structure, navigation clarity, and other material defects).",
        "3. Low automated findings.",
        "4. Manual reviews for media, linked documents, complex images, reflow, keyboard use, and reading order.",
        "",
    ]

    grouped: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    for page in audited:
        for finding in page["findings"]:
            grouped[finding["rule_id"]].append((page, finding))
    grouped_items = sorted(
        grouped.items(),
        key=lambda item: (
            min(SEVERITY_ORDER.get(f[1]["severity"], 99) for f in item[1]),
            -len(item[1]),
            item[0],
        ),
    )
    for rule_id, items in grouped_items:
        severity = min(items, key=lambda pair: SEVERITY_ORDER.get(pair[1]["severity"], 99))[1]["severity"]
        page_count = len({page["slug"] for page, _ in items})
        lines.extend(
            [
                f"## {severity}: {items[0][1]['issue']}",
                "",
                f"Rule: `{rule_id}` · {len(items)} occurrence(s) on {page_count} page(s) · WCAG {items[0][1]['criterion_label']}",
                "",
                f"**General pattern:** {FIXES.get(rule_id, items[0][1]['fix'])}",
                "",
            ]
        )
        by_page: dict[str, list[dict[str, Any]]] = defaultdict(list)
        page_lookup = {}
        for page, finding in items:
            by_page[page["slug"]].append(finding)
            page_lookup[page["slug"]] = page
        for slug, page_findings in by_page.items():
            page = page_lookup[slug]
            link = page_edit_url(api_url, course_id, slug)
            lines.append(f"- [ ] **[{page['title']}]({link})** — `{slug}` ({len(page_findings)} occurrence(s))")
            for finding in page_findings:
                lines.append(f"  - Find `{finding['selector']}`: `{finding['evidence']}`")
                lines.append(f"    - Change: {finding['fix']}")
        lines.append("")

    manual_pages = [page for page in audited if page["manual_reviews"]]
    lines.extend(
        [
            "## Manual-review queue",
            "",
            "These are not automatically confirmed failures. Review the evidence and fix only when the content does not meet the stated requirement.",
            "",
        ]
    )
    for page in manual_pages:
        link = page_edit_url(api_url, course_id, page["slug"])
        lines.append(f"- [ ] **[{page['title']}]({link})** — `{page['slug']}`")
        grouped_reviews = Counter(review["issue"] for review in page["manual_reviews"])
        for issue, count in grouped_reviews.items():
            lines.append(f"  - {issue} ({count})")

    lines.extend(
        [
            "",
            "## Completion",
            "",
            "- [ ] Rerun `python audit_canvas.py` after Canvas edits.",
            "- [ ] Confirm the automated finding count is zero or document reviewed exceptions.",
            "- [ ] Complete every applicable manual check in the full audit report.",
            "- [ ] Record reviewer, review date, assistive technologies/browsers used, and any accepted exceptions.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    load_dotenv(ROOT / ".env")
    if args.use_cache:
        print(f"Using cached Canvas HTML from {CACHE_PATH}.", flush=True)
        pages = load_cached_pages(args.api_url, args.course_id)
    else:
        token = os.getenv("CANVAS_ACCESS_TOKEN")
        if not token:
            print("CANVAS_ACCESS_TOKEN is missing from .env.", file=sys.stderr)
            return 2
        pages = download_pages(args.api_url, args.course_id, token, args.workers)

    nonempty = sum(bool(page.get("body")) for page in pages)
    empty = sum(not page.get("body") and not page.get("error") for page in pages)
    errors = sum(bool(page.get("error")) for page in pages)
    print(f"Content inventory: {nonempty} non-empty, {empty} empty, {errors} API errors.", flush=True)

    audited = audit_pages(pages)
    generated_at = datetime.now().astimezone()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    audit_path = REPORT_DIR / "WCAG_2.1_AA_AUDIT.md"
    fix_path = REPORT_DIR / "WCAG_2.1_AA_FIX_LIST.md"
    audit_path.write_text(
        generate_audit_report(audited, args.api_url, args.course_id, generated_at),
        encoding="utf-8",
    )
    fix_path.write_text(
        generate_fix_list(audited, args.api_url, args.course_id, generated_at),
        encoding="utf-8",
    )

    summary = report_summary(audited)
    print(f"Wrote {audit_path}", flush=True)
    print(f"Wrote {fix_path}", flush=True)
    print(
        f"Result: {len(summary['findings'])} automated findings on "
        f"{summary['pages_with_findings']} pages; {len(summary['reviews'])} manual-review items.",
        flush=True,
    )
    return 0 if summary["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
