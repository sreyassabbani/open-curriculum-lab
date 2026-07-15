#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, quote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv


DEFAULT_API_URL = "https://gatech.instructure.com"
DEFAULT_COURSE_ID = 563104
REQUEST_TIMEOUT = 45
SKILL_DIR = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RUN_ROOT = ROOT / ".cache" / "lesson-pipeline"
DEFAULT_OUTPUT_ROOT = ROOT / "output" / "lessons"
AXE_RUNNER = ROOT / "axe_runner.mjs"
RENDER_RUNNER = SKILL_DIR / "scripts" / "render_lesson.mjs"
CHROME_PATH = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

REQUIRED_INNER_STYLE = {
    "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    "line-height": "1.6",
    "color": "#333333",
    "padding": "20px",
    "border-radius": "8px",
    "border": "1px solid #e1e1e1",
}
REQUIRED_H2 = [
    "Motivating Questions and Objectives",
    "Summary of Key Concepts",
    "Comprehension Checks",
]
BANNED_TEXT = {
    r"\b(?:the|this|these|in the) videos?\b": "Do not refer to videos.",
    r"\b(?:the|this|these|in the) lectures?\b": "Do not refer to lectures.",
    r"\btranscripts?\b": "Do not refer to transcripts.",
    r"\btimestamps?\b": "Do not refer to timestamps.",
    r"\bcaptions?\b": "Do not refer to captions.",
    r"\bhow to prove\b": "Use assessment-aligned language instead of proof language.",
    r"\bproof strategy\b": "Use assessment-aligned language instead of proof language.",
    r"\bwe proved\b": "Avoid proof-focused narration.",
    r"\bactually[,]? wait\b": "Remove self-correction remnants.",
    r"\bi made a mistake\b": "Remove self-correction remnants.",
    r"\bobviously\b": "Avoid 'obviously'.",
    r"\btrivial(?:ly)?\b": "Avoid 'trivial'.",
    r"\bjust\b": "Avoid 'just'.",
}


class PipelineError(RuntimeError):
    pass


class TopicResolutionError(PipelineError):
    pass


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "lesson"


def parse_style(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for declaration in value.split(";"):
        if ":" not in declaration:
            continue
        key, item = declaration.split(":", 1)
        result[key.strip().lower()] = item.strip()
    return result


def redact(value: str) -> str:
    value = re.sub(
        r"([?&](?:access_token|session_token|verifier|ks|token)=)[^&\s\"'>]+",
        r"\1REDACTED",
        value,
        flags=re.I,
    )
    value = re.sub(r"(/ks/)[^/?#\s\"'>]+", r"\1REDACTED", value, flags=re.I)
    return value


def relative_to_root(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def paginate(session: requests.Session, url: str, **kwargs: Any) -> Iterable[requests.Response]:
    while url:
        response = session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        response.raise_for_status()
        yield response
        url = response.links.get("next", {}).get("url", "")


class CanvasClient:
    def __init__(
        self,
        api_url: str,
        course_id: int,
        token: str,
        session: requests.Session | None = None,
    ) -> None:
        self.api_url = api_url.rstrip("/")
        self.course_id = course_id
        self.session = session or requests.Session()
        self.headers = {"Authorization": f"Bearer {token}"}

    def api(self, path: str) -> str:
        return f"{self.api_url}/api/v1/courses/{self.course_id}/{path.lstrip('/')}"

    def list_pages(self) -> list[dict[str, Any]]:
        pages: list[dict[str, Any]] = []
        for response in paginate(
            self.session,
            self.api("pages"),
            headers=self.headers,
            params={"per_page": 100, "sort": "title"},
        ):
            pages.extend(response.json())
        return pages

    def get_page(self, slug: str) -> dict[str, Any]:
        response = self.session.get(
            self.api(f"pages/{quote(slug, safe='')}"),
            headers=self.headers,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def hydrate_lesson_pages(self) -> list[dict[str, Any]]:
        pages = self.list_pages()
        candidates = [
            page
            for page in pages
            if "lecture video" in page.get("title", "").lower()
            or "lecture notes" in page.get("title", "").lower()
        ]
        return [self.get_page(page["url"]) for page in candidates]

    def sessionless_launch(self, resource_uuid: str) -> str:
        response = self.session.get(
            self.api("external_tools/sessionless_launch"),
            headers=self.headers,
            params={"resource_link_lookup_uuid": resource_uuid},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("url"):
            raise PipelineError("Canvas returned no sessionless Kaltura launch URL.")
        return str(data["url"])

    def update_page_body(self, slug: str, body: str) -> dict[str, Any]:
        response = self.session.put(
            self.api(f"pages/{quote(slug, safe='')}"),
            headers=self.headers,
            data={
                "wiki_page[body]": body,
                "wiki_page[notify_of_update]": "false",
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()


def title_number(title: str) -> str | None:
    match = re.match(r"\s*(\d+(?:\.\d+)+)\b", title)
    return match.group(1) if match else None


def iframe_metadata(body: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(body or "", "lxml")
    results: list[dict[str, str]] = []
    for frame in soup.find_all("iframe"):
        source = html.unescape(frame.get("src", ""))
        resource_uuid = parse_qs(urlsplit(source).query).get("resource_link_lookup_uuid", [""])[0]
        if resource_uuid:
            results.append(
                {
                    "title": frame.get("title", "").strip() or "Untitled Kaltura video",
                    "resource_link_lookup_uuid": resource_uuid,
                }
            )
    return results


def resolve_topic(
    pages: list[dict[str, Any]], topic: str, target_override: str | None = None
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    topic = topic.strip()
    if not topic:
        raise TopicResolutionError("Topic cannot be empty.")
    videos = [page for page in pages if "lecture video" in page.get("title", "").lower()]
    notes = [page for page in pages if "lecture notes" in page.get("title", "").lower()]
    topic_lower = topic.lower()
    numeric = re.fullmatch(r"\d+(?:\.\d+)+", topic)
    code = re.search(r"m\d+w\d+t\d+", topic_lower)

    if numeric:
        source_candidates = [page for page in videos if title_number(page.get("title", "")) == topic]
    elif code:
        source_candidates = [page for page in videos if code.group(0) in page.get("body", "").lower()]
    else:
        words = [word for word in re.findall(r"[a-z0-9]+", topic_lower) if len(word) > 1]

        def matches(page: dict[str, Any]) -> bool:
            body = page.get("body", "")
            haystack = (
                f"{page.get('title', '')} {BeautifulSoup(body, 'lxml').get_text(' ')} {body}"
            ).lower()
            return bool(words) and all(word in haystack for word in words)

        source_candidates = [page for page in videos if matches(page)]

    if len(source_candidates) != 1:
        names = ", ".join(f"{page.get('title')} ({page.get('url')})" for page in source_candidates)
        if not names:
            names = "none"
        raise TopicResolutionError(
            f"Expected one lecture-video page for {topic!r}; found {len(source_candidates)}: {names}"
        )

    source = source_candidates[0]
    frames = iframe_metadata(source.get("body", ""))
    if code:
        frames = [frame for frame in frames if code.group(0) in frame["title"].lower()]
    if not frames:
        raise TopicResolutionError(f"The matched page {source.get('title')!r} has no matching Kaltura videos.")

    if target_override:
        targets = [page for page in notes if page.get("url") == target_override]
    else:
        number = title_number(source.get("title", ""))
        targets = [page for page in notes if number and title_number(page.get("title", "")) == number]
    if len(targets) != 1:
        names = ", ".join(f"{page.get('title')} ({page.get('url')})" for page in targets) or "none"
        raise TopicResolutionError(
            f"Expected one existing lecture-notes target; found {len(targets)}: {names}. "
            "Supply --target-page-slug to select an existing page."
        )
    return source, targets[0], frames


def hidden_form(form: Tag) -> dict[str, str]:
    return {
        str(item["name"]): str(item.get("value", ""))
        for item in form.find_all("input", attrs={"name": True})
    }


def submit_first_form(session: requests.Session, response: requests.Response) -> requests.Response:
    soup = BeautifulSoup(response.text, "lxml")
    form = soup.find("form")
    if not isinstance(form, Tag) or not form.get("action"):
        raise PipelineError("The Kaltura launch did not provide the expected authentication form.")
    return session.post(
        urljoin(response.url, str(form["action"])),
        data=hidden_form(form),
        timeout=REQUEST_TIMEOUT,
    )


def select_english_caption(objects: list[dict[str, Any]]) -> dict[str, Any]:
    ready = [
        item
        for item in objects
        if str(item.get("status")) == "2"
        and (
            str(item.get("languageCode", "")).lower().startswith("en")
            or str(item.get("language", "")).lower() == "english"
            or str(item.get("label", "")).lower() == "english"
        )
    ]
    if not ready:
        raise PipelineError("No ready English caption asset was found for this Kaltura video.")
    ready.sort(
        key=lambda item: (
            str(item.get("format")) != "1",
            str(item.get("label", "")).lower() != "english",
            str(item.get("id", "")),
        )
    )
    return ready[0]


def download_kaltura_caption(
    canvas: CanvasClient, frame: dict[str, str]
) -> tuple[str, dict[str, Any]]:
    session = canvas.session
    launch_url = canvas.sessionless_launch(frame["resource_link_lookup_uuid"])
    response = session.get(launch_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    response = submit_first_form(session, response)
    response.raise_for_status()
    response = submit_first_form(session, response)
    response.raise_for_status()

    redirect_match = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+)", response.text)
    if not redirect_match:
        raise PipelineError("The Kaltura launch did not expose its media redirect.")
    media_page = session.get(html.unescape(redirect_match.group(1)), timeout=REQUEST_TIMEOUT)
    media_page.raise_for_status()

    entry_match = re.search(r"loadMedia\(\{entryId:['\"]([^'\"]+)", media_page.text)
    if not entry_match:
        entry_match = re.search(r"/entryid/([a-z0-9_]+)", media_page.text, flags=re.I)
    if not entry_match:
        raise PipelineError("The Kaltura media entry ID could not be determined.")
    entry_id = entry_match.group(1)

    config_match = re.search(
        r"var config\s*=\s*(\{.+?\});.*?KalturaPlayer\.setup\(config\)",
        media_page.text,
        flags=re.S,
    )
    if not config_match:
        raise PipelineError("The Kaltura player configuration could not be determined.")
    provider = json.loads(config_match.group(1))["provider"]
    ks = provider.get("ks")
    if not ks:
        raise PipelineError("The Kaltura player did not provide a caption-authorized session.")

    api_url = str(provider.get("env", {}).get("serviceUrl", "https://www.kaltura.com/api_v3"))
    api_url = api_url.rstrip("/") + "/index.php"
    list_response = session.get(
        api_url,
        params={
            "service": "caption_captionasset",
            "action": "list",
            "ks": ks,
            "filter:objectType": "KalturaCaptionAssetFilter",
            "filter:entryIdEqual": entry_id,
            "format": 1,
        },
        timeout=REQUEST_TIMEOUT,
    )
    list_response.raise_for_status()
    payload = list_response.json()
    if payload.get("objectType") == "KalturaAPIException":
        raise PipelineError(f"Kaltura caption lookup failed: {payload.get('message', 'unknown error')}")
    asset = select_english_caption(payload.get("objects", []))

    url_response = session.get(
        api_url,
        params={
            "service": "caption_captionasset",
            "action": "getUrl",
            "ks": ks,
            "id": asset["id"],
            "format": 1,
        },
        timeout=REQUEST_TIMEOUT,
    )
    url_response.raise_for_status()
    caption_url = url_response.json()
    if not isinstance(caption_url, str):
        raise PipelineError("Kaltura did not return a caption download URL.")
    caption_response = session.get(caption_url, timeout=REQUEST_TIMEOUT)
    caption_response.raise_for_status()
    caption_text = caption_response.content.decode("utf-8-sig", errors="replace")
    metadata = {
        "title": frame["title"],
        "resource_link_lookup_uuid": frame["resource_link_lookup_uuid"],
        "entry_id": entry_id,
        "caption_asset_id": asset.get("id"),
        "language": asset.get("language") or asset.get("languageCode") or "English",
        "format": asset.get("format"),
    }
    return caption_text, metadata


def normalize_caption_text(value: str) -> str:
    if "<tt" in value[:1000].lower() or "<transcript" in value[:1000].lower():
        soup = BeautifulSoup(value, "xml")
        cues = [item.get_text(" ", strip=True) for item in soup.find_all(["p", "text"])]
    else:
        value = value.replace("\r\n", "\n").replace("\r", "\n").strip()
        cues = []
        for block in re.split(r"\n\s*\n", value):
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if lines and lines[0].upper() == "WEBVTT":
                lines.pop(0)
            if lines and re.fullmatch(r"\d+", lines[0]):
                lines.pop(0)
            if lines and "-->" in lines[0]:
                lines.pop(0)
            if lines:
                cue = BeautifulSoup(" ".join(lines), "lxml").get_text(" ", strip=True)
                cues.append(cue)
    cleaned: list[str] = []
    for cue in cues:
        cue = re.sub(r"\s+", " ", cue).strip()
        if cue and (not cleaned or cue != cleaned[-1]):
            cleaned.append(cue)
    return "\n".join(cleaned).strip() + "\n"


def caption_extension(value: str) -> str:
    prefix = value.lstrip()[:1000].lower()
    if prefix.startswith("webvtt"):
        return ".vtt"
    if "<tt" in prefix or "<transcript" in prefix:
        return ".dfxp"
    return ".srt"


def lesson_filename(source: dict[str, Any], target: dict[str, Any]) -> str:
    number = title_number(source.get("title", "")) or "topic"
    title = re.sub(r"^\s*\d+(?:\.\d+)+\s+Lecture Notes:?\s*", "", target.get("title", ""), flags=re.I)
    return f"{number}-{slugify(title)}.html"


def prepare(args: argparse.Namespace) -> int:
    load_dotenv(ROOT / ".env")
    token = os.getenv("CANVAS_ACCESS_TOKEN")
    if not token:
        raise PipelineError("CANVAS_ACCESS_TOKEN is missing from .env.")
    canvas = CanvasClient(args.api_url, args.course_id, token)
    pages = canvas.hydrate_lesson_pages()
    source, target, frames = resolve_topic(pages, args.topic, args.target_page_slug)
    run_slug = slugify(f"{title_number(source.get('title', '')) or args.topic}-{target.get('title', '')}")
    run_dir = Path(args.run_dir).resolve() if args.run_dir else (
        DEFAULT_RUN_ROOT / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{run_slug}"
    )
    raw_dir = run_dir / "transcripts" / "raw"
    normalized_dir = run_dir / "transcripts" / "normalized"
    raw_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)

    videos: list[dict[str, Any]] = []
    for number, frame in enumerate(frames, start=1):
        print(f"Downloading captions {number}/{len(frames)}: {frame['title']}", file=sys.stderr)
        raw, metadata = download_kaltura_caption(canvas, frame)
        stem = f"{number:02d}-{slugify(frame['title'])}"
        raw_path = raw_dir / f"{stem}{caption_extension(raw)}"
        normalized_path = normalized_dir / f"{stem}.txt"
        raw_path.write_text(raw, encoding="utf-8")
        normalized_path.write_text(normalize_caption_text(raw), encoding="utf-8")
        metadata.update(
            {
                "raw_path": relative_to_root(raw_path),
                "normalized_path": relative_to_root(normalized_path),
                "raw_sha256": sha256_text(raw),
            }
        )
        videos.append(metadata)

    before_path = run_dir / "canvas-before.html"
    before_body = target.get("body") or ""
    before_path.write_text(before_body, encoding="utf-8")
    output_path = DEFAULT_OUTPUT_ROOT / lesson_filename(source, target)
    manifest = {
        "version": 1,
        "prepared_at": now_iso(),
        "topic_input": args.topic,
        "api_url": args.api_url.rstrip("/"),
        "course_id": args.course_id,
        "source_page": {
            "title": source.get("title"),
            "slug": source.get("url"),
            "updated_at": source.get("updated_at"),
        },
        "target_page": {
            "title": target.get("title"),
            "slug": target.get("url"),
            "page_id": target.get("page_id"),
            "published": bool(target.get("published")),
            "updated_at": target.get("updated_at"),
            "body_sha256": sha256_text(before_body),
            "backup_path": relative_to_root(before_path),
        },
        "videos": videos,
        "lesson_path": relative_to_root(run_dir / "lesson.html"),
        "output_path": relative_to_root(output_path),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    bundle_lines = [
        f"# Source bundle: {target.get('title')}",
        "",
        "Synthesize these sources into one unified lesson; do not summarize them separately.",
    ]
    for item in videos:
        normalized_path = ROOT / item["normalized_path"]
        bundle_lines.extend(
            [
                "",
                f"## {item['title']}",
                "",
                normalized_path.read_text(encoding="utf-8").strip(),
            ]
        )
    (run_dir / "source-bundle.md").write_text("\n".join(bundle_lines) + "\n", encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), "manifest": manifest}, indent=2))
    return 0


def direct_child(parent: Tag, name: str) -> Tag | None:
    for child in parent.children:
        if isinstance(child, Tag) and child.name == name:
            return child
    return None


def validate_html_text(value: str) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if "```" in value:
        errors.append("Remove Markdown code fences; the file must contain only the Canvas HTML fragment.")
    if re.search(r"[]|filecite|turn\d+(?:file|search|view)\d+", value, flags=re.I):
        errors.append("Remove tool citation tokens from the lesson HTML.")
    soup = BeautifulSoup(value, "lxml")
    body_root = soup.body or soup
    top_level_tags = [child for child in body_root.children if isinstance(child, Tag)]
    if len(top_level_tags) != 1 or top_level_tags[0].get("id") != "dp-wrapper":
        errors.append("The Canvas fragment must contain only the single dp-wrapper element.")
    for forbidden in ["script", "style", "iframe", "form", "object", "embed"]:
        if soup.find(forbidden):
            errors.append(f"Canvas lesson bodies must not contain <{forbidden}> elements.")
    if soup.find("h1"):
        errors.append("Start Canvas page-body headings at h2; Canvas supplies the page h1.")

    wrapper = soup.find("div", id="dp-wrapper")
    if not isinstance(wrapper, Tag) or "dp-wrapper" not in wrapper.get("class", []):
        errors.append("Use the exact outer <div id=\"dp-wrapper\" class=\"dp-wrapper\"> wrapper.")
        inner = None
    else:
        inner = direct_child(wrapper, "div")
        if not inner:
            errors.append("The dp-wrapper must contain the required styled inner div.")
        else:
            styles = parse_style(inner.get("style", ""))
            for key, expected in REQUIRED_INNER_STYLE.items():
                if styles.get(key, "").lower() != expected.lower():
                    errors.append(f"Inner wrapper style {key!r} must be {expected!r}.")

    h2_titles = [heading.get_text(" ", strip=True) for heading in soup.find_all("h2")]
    if h2_titles != REQUIRED_H2:
        errors.append(f"Use exactly these h2 sections in order: {', '.join(REQUIRED_H2)}.")
    for heading in soup.find_all("h2"):
        styles = parse_style(heading.get("style", ""))
        if (
            styles.get("color", "").lower() != "#003057"
            or styles.get("border-bottom", "").lower() != "2px solid #b3a369"
            or styles.get("padding-bottom", "").lower() != "10px"
        ):
            errors.append(f"Heading {heading.get_text(' ', strip=True)!r} does not use the required navy/gold h2 style.")

    h3_titles = [heading.get_text(" ", strip=True) for heading in soup.find_all("h3")]
    numbers = [int(match.group(1)) for title in h3_titles if (match := re.match(r"(\d+)\.\s+", title))]
    if len(numbers) < 3:
        errors.append("Include multiple numbered concept sections using h3 headings.")
    elif numbers != list(range(1, len(numbers) + 1)):
        errors.append("Number h3 concept sections sequentially starting at 1.")
    if not any(re.match(r"\d+\.\s+Summary:", title, flags=re.I) for title in h3_titles):
        errors.append("End the numbered concepts with a 'Summary:' h3 section.")

    summary_tables = []
    for table in soup.find_all("table"):
        headers = [cell.get_text(" ", strip=True) for cell in table.find_all("th")]
        if headers == ["Concept", "Meaning", "Main Check"]:
            summary_tables.append(table)
    if not summary_tables:
        errors.append("Include the required summary table with Concept, Meaning, and Main Check columns.")
    for table in soup.find_all("table"):
        if not table.find("th"):
            errors.append("Every instructional table must use header cells.")
        parent = table.parent
        if not isinstance(parent, Tag) or "dp-table-scroll" not in parent.get("class", []):
            errors.append("Wrap each table in <div class=\"dp-table-scroll\">.")

    question_nodes: list[Tag] = []
    for strong in soup.find_all("strong"):
        if re.fullmatch(r"Question\s+\d+:?", strong.get_text(" ", strip=True)):
            question_nodes.append(strong)
    question_numbers = [int(re.search(r"\d+", item.get_text()).group()) for item in question_nodes]
    if not 4 <= len(question_numbers) <= 7:
        errors.append("Include 4 to 6 comprehension checks by default, or at most 7 when justified.")
    if question_numbers != list(range(1, len(question_numbers) + 1)):
        errors.append("Number comprehension checks sequentially starting at 1.")
    if len(question_numbers) == 7:
        warnings.append("Seven comprehension checks are allowed only when the extra check is pedagogically useful.")
    for strong in question_nodes:
        block = strong.find_parent("div")
        while isinstance(block, Tag) and "background-color: #f0f4f7" not in block.get("style", ""):
            block = block.find_parent("div")
        if not isinstance(block, Tag):
            errors.append(f"{strong.get_text(strip=True)} is not inside the required light-blue check block.")
            continue
        details = block.find("details")
        summary = details.find("summary") if isinstance(details, Tag) else None
        if not isinstance(summary, Tag) or summary.get_text(" ", strip=True) != "Click to reveal the answer":
            errors.append(f"{strong.get_text(strip=True)} must use the required collapsible answer summary.")
        block_text = block.get_text(" ", strip=True)
        if "Answer:" not in block_text or "Explanation:" not in block_text:
            errors.append(f"{strong.get_text(strip=True)} must include both Answer and Explanation.")

    visible_text = soup.get_text(" ", strip=True)
    for pattern, message in BANNED_TEXT.items():
        if re.search(pattern, visible_text, flags=re.I):
            errors.append(message)
    if "After completing the exercises in this topic, you should be able to" not in visible_text:
        errors.append("Use the required topic-based objective sentence.")

    for block in re.findall(r"\\\[(.*?)\\\]", value, flags=re.S):
        if "\\begin{" in block and "&" in block.replace("&amp;", ""):
            errors.append("Escape ampersands in displayed matrices as &amp;.")
            break
    ids = [str(tag["id"]) for tag in soup.find_all(attrs={"id": True})]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"Duplicate HTML ids: {', '.join(duplicates)}.")
    return {"errors": sorted(set(errors)), "warnings": sorted(set(warnings))}


def standalone_document(title: str, body: str, include_mathjax: bool = False) -> str:
    mathjax = ""
    if include_mathjax:
        mathjax = (
            '<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"],["$","$"]],'
            'displayMath:[["\\\\[","\\\\]"]]}};</script>'
            '<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{html.escape(title)}</title>{mathjax}"
        "<style>body{background:#fff;color:#2d3b45;font:16px/1.5 Arial,sans-serif;margin:0;padding:24px;}"
        "#canvas-page{max-width:1100px;margin:0 auto;}</style></head>"
        f'<body><main id="canvas-page">{body}</main></body></html>'
    )


def node_command(script: Path, *arguments: str) -> list[str]:
    node = shutil.which("node")
    if node:
        return [node, str(script), *arguments]
    nix = shutil.which("nix")
    if nix:
        return [nix, "develop", "--command", "node", str(script), *arguments]
    raise PipelineError("Node.js is required for browser validation and rendering.")


def run_axe(run_dir: Path, title: str, body: str) -> list[str]:
    if not AXE_RUNNER.exists():
        raise PipelineError(f"Missing axe runner: {AXE_RUNNER}")
    input_path = run_dir / "axe-input.json"
    output_path = run_dir / "axe-results.json"
    input_path.write_text(
        json.dumps(
            {
                "chromePath": str(CHROME_PATH) if CHROME_PATH.exists() else None,
                "pages": [{"slug": "generated-lesson", "document": standalone_document(title, body)}],
            }
        ),
        encoding="utf-8",
    )
    subprocess.run(
        node_command(AXE_RUNNER, str(input_path), str(output_path)),
        cwd=ROOT,
        check=True,
    )
    result = json.loads(output_path.read_text(encoding="utf-8"))["pages"][0]
    if result.get("error"):
        return [f"axe browser scan failed: {result['error']}"]
    return [
        f"axe: {rule.get('help', rule.get('id'))} ({rule.get('id')})"
        for rule in result.get("axe", {}).get("violations", [])
    ]


def read_manifest(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "manifest.json"
    if not path.exists():
        raise PipelineError(f"Missing run manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    manifest = read_manifest(run_dir)
    lesson_path = Path(args.html).resolve() if args.html else run_dir / "lesson.html"
    if not lesson_path.exists():
        raise PipelineError(f"Missing generated lesson: {lesson_path}")
    body = lesson_path.read_text(encoding="utf-8")
    result = validate_html_text(body)
    if not args.skip_axe:
        result["errors"].extend(run_axe(run_dir, manifest["target_page"]["title"], body))
        result["errors"] = sorted(set(result["errors"]))
    result.update(
        {
            "validated_at": now_iso(),
            "lesson_path": relative_to_root(lesson_path),
            "lesson_sha256": sha256_text(body),
        }
    )
    validation_path = run_dir / "validation.json"
    validation_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if not result["errors"]:
        output_path = ROOT / manifest["output_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(body, encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


def render(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    manifest = read_manifest(run_dir)
    lesson_path = run_dir / "lesson.html"
    if not lesson_path.exists():
        raise PipelineError(f"Missing generated lesson: {lesson_path}")
    preview_path = run_dir / "preview.html"
    screenshot_path = run_dir / "preview.png"
    preview_path.write_text(
        standalone_document(
            manifest["target_page"]["title"],
            lesson_path.read_text(encoding="utf-8"),
            include_mathjax=True,
        ),
        encoding="utf-8",
    )
    subprocess.run(
        node_command(
            RENDER_RUNNER,
            str(preview_path),
            str(screenshot_path),
            str(CHROME_PATH) if CHROME_PATH.exists() else "",
        ),
        cwd=ROOT,
        check=True,
    )
    print(json.dumps({"preview": str(preview_path), "screenshot": str(screenshot_path)}, indent=2))
    return 0


def require_confirmation(args: argparse.Namespace, slug: str, action: str) -> None:
    confirmation = args.confirm_slug
    if confirmation is None and sys.stdin.isatty():
        confirmation = input(f"Type {slug!r} to confirm {action}: ").strip()
    if confirmation != slug:
        raise PipelineError(f"{action.capitalize()} canceled: exact page-slug confirmation was not provided.")


def load_canvas_for_manifest(manifest: dict[str, Any]) -> CanvasClient:
    load_dotenv(ROOT / ".env")
    token = os.getenv("CANVAS_ACCESS_TOKEN")
    if not token:
        raise PipelineError("CANVAS_ACCESS_TOKEN is missing from .env.")
    return CanvasClient(manifest["api_url"], int(manifest["course_id"]), token)


def verified_local_lesson(run_dir: Path) -> tuple[dict[str, Any], str]:
    manifest = read_manifest(run_dir)
    validation_path = run_dir / "validation.json"
    if not validation_path.exists():
        raise PipelineError("Run validate successfully before publishing.")
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    lesson_path = run_dir / "lesson.html"
    if not lesson_path.exists():
        raise PipelineError(f"Missing generated lesson: {lesson_path}")
    body = lesson_path.read_text(encoding="utf-8")
    if validation.get("errors") or validation.get("lesson_sha256") != sha256_text(body):
        raise PipelineError("The lesson is unvalidated or changed after validation; validate it again.")
    return manifest, body


def publish(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    manifest, body = verified_local_lesson(run_dir)
    slug = manifest["target_page"]["slug"]
    canvas = load_canvas_for_manifest(manifest)
    current = canvas.get_page(slug)
    current_body = current.get("body") or ""
    if (
        sha256_text(current_body) != manifest["target_page"]["body_sha256"]
        or current.get("updated_at") != manifest["target_page"].get("updated_at")
    ):
        raise PipelineError("Canvas target changed after preparation; prepare again before publishing.")
    print(
        json.dumps(
            {
                "action": "publish",
                "title": current.get("title"),
                "slug": slug,
                "published": current.get("published"),
                "old_characters": len(current_body),
                "new_characters": len(body),
                "diff_path": str(run_dir / "canvas-diff.patch"),
            },
            indent=2,
        )
    )
    diff = difflib.unified_diff(
        current_body.splitlines(keepends=True),
        body.splitlines(keepends=True),
        fromfile=f"canvas/{slug}/before",
        tofile=f"canvas/{slug}/generated",
    )
    (run_dir / "canvas-diff.patch").write_text("".join(diff), encoding="utf-8")
    require_confirmation(args, slug, "publish")
    canvas.update_page_body(slug, body)
    stored = canvas.get_page(slug)
    stored_body = stored.get("body") or ""
    post_validation = validate_html_text(stored_body)
    post_validation["errors"].extend(
        run_axe(run_dir, str(stored.get("title") or slug), stored_body)
    )
    post_validation["errors"] = sorted(set(post_validation["errors"]))
    publication = {
        "published_at": now_iso(),
        "updated_at": stored.get("updated_at"),
        "body_sha256": sha256_text(stored_body),
        "post_validation": post_validation,
    }
    manifest["publication"] = publication
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (run_dir / "canvas-after.html").write_text(stored_body, encoding="utf-8")
    (run_dir / "post-publish-validation.json").write_text(
        json.dumps(post_validation, indent=2), encoding="utf-8"
    )
    print(json.dumps(publication, indent=2))
    return 1 if post_validation["errors"] else 0


def rollback(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    manifest = read_manifest(run_dir)
    publication = manifest.get("publication")
    if not publication:
        raise PipelineError("This run has no recorded publication to roll back.")
    slug = manifest["target_page"]["slug"]
    backup_path = ROOT / manifest["target_page"]["backup_path"]
    if not backup_path.exists():
        raise PipelineError(f"Missing Canvas backup: {backup_path}")
    canvas = load_canvas_for_manifest(manifest)
    current = canvas.get_page(slug)
    if sha256_text(current.get("body") or "") != publication["body_sha256"]:
        raise PipelineError("Canvas target changed after publication; refusing to overwrite newer edits.")
    require_confirmation(args, slug, "rollback")
    canvas.update_page_body(slug, backup_path.read_text(encoding="utf-8"))
    restored = canvas.get_page(slug)
    result = {
        "rolled_back_at": now_iso(),
        "body_sha256": sha256_text(restored.get("body") or ""),
        "matches_backup": sha256_text(restored.get("body") or "")
        == manifest["target_page"]["body_sha256"],
    }
    manifest["rollback"] = result
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["matches_backup"] else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Prepare, validate, preview, and publish transcript-grounded MATH 1554 lessons."
    )
    subparsers = root.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Resolve a topic and download its captions.")
    prepare_parser.add_argument("topic")
    prepare_parser.add_argument("--api-url", default=DEFAULT_API_URL)
    prepare_parser.add_argument("--course-id", type=int, default=DEFAULT_COURSE_ID)
    prepare_parser.add_argument("--target-page-slug")
    prepare_parser.add_argument("--run-dir")
    prepare_parser.set_defaults(function=prepare)

    validate_parser = subparsers.add_parser("validate", help="Validate a generated lesson.html.")
    validate_parser.add_argument("run_dir")
    validate_parser.add_argument("--html")
    validate_parser.add_argument("--skip-axe", action="store_true")
    validate_parser.set_defaults(function=validate)

    render_parser = subparsers.add_parser("render", help="Render a browser preview and screenshot.")
    render_parser.add_argument("run_dir")
    render_parser.set_defaults(function=render)

    for name, function in (("publish", publish), ("rollback", rollback)):
        action_parser = subparsers.add_parser(name)
        action_parser.add_argument("run_dir")
        action_parser.add_argument("--confirm-slug")
        action_parser.set_defaults(function=function)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.function(args))
    except requests.RequestException as exc:
        print(f"Network error: {redact(str(exc))}", file=sys.stderr)
        return 2
    except (PipelineError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {redact(str(exc))}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
