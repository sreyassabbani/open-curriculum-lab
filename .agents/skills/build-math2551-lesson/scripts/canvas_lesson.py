#!/usr/bin/env python3
"""MATH 2551 source preparation, isolated from the MATH 1554 workflow."""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup, Tag


COURSE_ID = 588672
SKILL_DIR = Path(__file__).resolve().parents[1]
ROOT = SKILL_DIR.parents[2]
BASE_SCRIPT = ROOT / ".agents" / "skills" / "build-math1554-lesson" / "scripts" / "canvas_lesson.py"

SPEC = importlib.util.spec_from_file_location("math1554_canvas_lesson", BASE_SCRIPT)
if not SPEC or not SPEC.loader:
    raise RuntimeError(f"Unable to load shared Canvas helpers from {BASE_SCRIPT}")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)


def title_numbers(title: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\b\d+(?:\.\d+)+\b", title)))


def parenthetical_title_numbers(title: str) -> list[str]:
    return re.findall(r"\(\s*(\d+(?:\.\d+)+)\s*\)", title)


def is_source_page(page: dict[str, Any]) -> bool:
    return bool(re.match(r"\s*topic\s+\d+(?:\.\d+)+\b", str(page.get("title", "")), re.I))


def is_target_page(page: dict[str, Any]) -> bool:
    return bool(re.match(r"\s*lesson\s+\d+(?:\.\d+)+\b", str(page.get("title", "")), re.I))


class Math2551CanvasClient(base.CanvasClient):
    def hydrate_lesson_pages(self) -> list[dict[str, Any]]:
        pages = self.list_pages()
        return [
            self.get_page(page["url"])
            for page in pages
            if is_source_page(page) or is_target_page(page)
        ]

    def external_tool_sessionless_launch(self, external_tool_url: str) -> str:
        response = self.session.get(
            self.api("external_tools/sessionless_launch"),
            headers=self.headers,
            params={"url": external_tool_url},
            timeout=base.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("url"):
            raise base.PipelineError("Canvas returned no sessionless Kaltura launch URL.")
        return str(payload["url"])


def iframe_metadata(body: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(body or "", "lxml")
    frames: list[dict[str, str]] = []
    for frame in soup.find_all("iframe"):
        source = html.unescape(frame.get("src", ""))
        parts = urlsplit(source)
        external_tool_url = parse_qs(parts.query).get("url", [""])[0]
        if parts.path.endswith("/external_tools/retrieve") and external_tool_url:
            frames.append(
                {
                    "title": frame.get("title", "").strip() or "Untitled Kaltura video",
                    "external_tool_url": external_tool_url,
                }
            )
            continue
        entry_id = parse_qs(parts.query).get("entry_id", [""])[0]
        if entry_id and "kaltura" in parts.netloc.lower():
            frames.append(
                {
                    "title": frame.get("title", "").strip() or "Untitled Kaltura video",
                    "entry_id": entry_id,
                    "embed_url": source,
                }
            )
    return frames


def resolve_topic(
    pages: list[dict[str, Any]], topic: str, target_override: str | None = None
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    topic = topic.strip()
    if not topic:
        raise base.TopicResolutionError("Topic cannot be empty.")
    sources = [page for page in pages if is_source_page(page)]
    targets = [page for page in pages if is_target_page(page)]
    numeric = re.fullmatch(r"\d+(?:\.\d+)+", topic)

    if numeric:
        # Prefer the textbook section explicitly shown in parentheses. This avoids
        # confusing an internal Topic number with the assigned Lesson number.
        candidates = [
            page
            for page in sources
            if topic in parenthetical_title_numbers(str(page.get("title", "")))
        ]
        if not candidates:
            candidates = [
                page
                for page in sources
                if re.match(rf"\s*topic\s+{re.escape(topic)}\b", str(page.get("title", "")), re.I)
            ]
    else:
        words = [word for word in re.findall(r"[a-z0-9]+", topic.lower()) if len(word) > 1]

        def matches(page: dict[str, Any]) -> bool:
            body = str(page.get("body", ""))
            haystack = f"{page.get('title', '')} {BeautifulSoup(body, 'lxml').get_text(' ')} {body}".lower()
            return bool(words) and all(word in haystack for word in words)

        candidates = [page for page in sources if matches(page)]

    if len(candidates) != 1:
        names = ", ".join(f"{page.get('title')} ({page.get('url')})" for page in candidates) or "none"
        raise base.TopicResolutionError(
            f"Expected one MATH 2551 Topic source for {topic!r}; found {len(candidates)}: {names}"
        )
    source = candidates[0]
    frames = iframe_metadata(str(source.get("body", "")))
    if not frames:
        raise base.TopicResolutionError(
            f"The matched Topic page {source.get('title')!r} has no Canvas external-tool Kaltura video."
        )

    if target_override:
        selected_targets = [page for page in targets if page.get("url") == target_override]
    else:
        expected = [topic] if numeric else title_numbers(str(source.get("title", "")))
        selected_targets = [
            page
            for page in targets
            if set(expected).intersection(title_numbers(str(page.get("title", ""))))
        ]
    if len(selected_targets) != 1:
        names = ", ".join(f"{page.get('title')} ({page.get('url')})" for page in selected_targets) or "none"
        raise base.TopicResolutionError(
            f"Expected one MATH 2551 Lesson target; found {len(selected_targets)}: {names}. "
            "Supply --target-page-slug to select an existing Lesson page."
        )
    return source, selected_targets[0], frames


def complete_kaltura_launch(session: requests.Session, launch_url: str) -> requests.Response:
    response = session.get(launch_url, timeout=base.REQUEST_TIMEOUT)
    response.raise_for_status()
    for _ in range(4):
        soup = BeautifulSoup(response.text, "lxml")
        form = soup.find("form")
        if not isinstance(form, Tag) or not form.get("action"):
            return response
        data = {
            str(item["name"]): str(item.get("value", ""))
            for item in form.find_all("input", attrs={"name": True})
        }
        response = session.post(
            urljoin(response.url, str(form["action"])), data=data, timeout=base.REQUEST_TIMEOUT
        )
        response.raise_for_status()
    raise base.PipelineError("The Kaltura launch exceeded the supported number of authentication handoffs.")


def javascript_redirect(response: requests.Response) -> str | None:
    match = re.search(r"window\.location(?:\.href)?\s*=\s*['\"]([^'\"]+)", response.text, re.I)
    return urljoin(response.url, html.unescape(match.group(1))) if match else None


def download_kaltura_caption(
    canvas: Math2551CanvasClient, frame: dict[str, str]
) -> tuple[str, dict[str, Any]]:
    if "external_tool_url" not in frame:
        raise base.PipelineError(
            "This Topic page includes a direct Kaltura embed whose captions require a browser-authenticated "
            "player. Export every English caption file and rerun prepare with --caption-file for each video."
        )
    launch_url = canvas.external_tool_sessionless_launch(frame["external_tool_url"])
    media_page = complete_kaltura_launch(canvas.session, launch_url)
    entry_id = ""
    config_match: re.Match[str] | None = None
    for _ in range(4):
        entry_match = re.search(r"loadMedia\(\{entryId:['\"]([^'\"]+)", media_page.text)
        if not entry_match:
            entry_match = re.search(r"/entryid/([a-z0-9_]+)", media_page.text, flags=re.I)
        if entry_match:
            entry_id = entry_match.group(1)
        config_match = re.search(
            r"var config\s*=\s*(\{.+?\});.*?KalturaPlayer\.setup\(config\)",
            media_page.text,
            flags=re.S,
        )
        if config_match:
            break
        redirect = javascript_redirect(media_page)
        if not redirect:
            break
        media_page = canvas.session.get(redirect, timeout=base.REQUEST_TIMEOUT)
        media_page.raise_for_status()

    if not entry_id:
        raise base.PipelineError("The Kaltura media entry ID could not be determined.")
    if not config_match:
        raise base.PipelineError(
            "The Kaltura external-tool launch did not expose a caption-authorized configuration. "
            "Use a browser-authenticated Kaltura session or obtain exported English captions."
        )
    provider = json.loads(config_match.group(1))["provider"]
    ks = provider.get("ks")
    if not ks:
        raise base.PipelineError("The Kaltura player did not provide a caption-authorized session.")
    api_url = str(provider.get("env", {}).get("serviceUrl", "https://www.kaltura.com/api_v3")).rstrip("/") + "/index.php"
    listing = canvas.session.get(
        api_url,
        params={
            "service": "caption_captionasset",
            "action": "list",
            "ks": ks,
            "filter:objectType": "KalturaCaptionAssetFilter",
            "filter:entryIdEqual": entry_id,
            "format": 1,
        },
        timeout=base.REQUEST_TIMEOUT,
    )
    listing.raise_for_status()
    payload = listing.json()
    if payload.get("objectType") == "KalturaAPIException":
        raise base.PipelineError(f"Kaltura caption lookup failed: {payload.get('message', 'unknown error')}")
    asset = base.select_english_caption(payload.get("objects", []))
    url_response = canvas.session.get(
        api_url,
        params={"service": "caption_captionasset", "action": "getUrl", "ks": ks, "id": asset["id"], "format": 1},
        timeout=base.REQUEST_TIMEOUT,
    )
    url_response.raise_for_status()
    caption_response = canvas.session.get(url_response.json(), timeout=base.REQUEST_TIMEOUT)
    caption_response.raise_for_status()
    return caption_response.content.decode("utf-8-sig", errors="replace"), {
        "title": frame["title"],
        "entry_id": entry_id,
        "caption_asset_id": asset.get("id"),
        "language": asset.get("language") or asset.get("languageCode") or "English",
        "format": asset.get("format"),
        "launch_source": "Canvas external tool",
    }


def lesson_filename(source: dict[str, Any], target: dict[str, Any]) -> str:
    number = (title_numbers(str(target.get("title", ""))) or ["topic"])[0]
    title = re.sub(r"^\s*lesson\s+\d+(?:\.\d+)+\s*:\s*", "", str(target.get("title", "")), flags=re.I)
    return f"{number}-{base.slugify(title)}.html"


def imported_caption_downloader(paths: list[str]):
    """Create a caption downloader backed by user-exported local files."""
    position = 0

    def download(_: Math2551CanvasClient, frame: dict[str, str]) -> tuple[str, dict[str, Any]]:
        nonlocal position
        if position >= len(paths):
            raise base.PipelineError(
                "Fewer --caption-file values were supplied than Kaltura videos on the Topic page."
            )
        path = Path(paths[position]).expanduser().resolve()
        position += 1
        if not path.is_file():
            raise base.PipelineError(f"Imported caption file does not exist: {path}")
        raw = path.read_bytes().decode("utf-8-sig", errors="replace")
        if not raw.strip():
            raise base.PipelineError(f"Imported caption file is empty: {path}")
        return raw, {
            "title": frame["title"],
            "entry_id": None,
            "caption_asset_id": None,
            "language": "English",
            "format": base.caption_extension(raw).lstrip("."),
            "launch_source": "Imported browser-authenticated caption export",
        }

    return download


def prepare(args: Any) -> int:
    def resolve_with_caption_count(
        pages: list[dict[str, Any]], topic: str, target_override: str | None = None
    ) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
        resolved = resolve_topic(pages, topic, target_override)
        if args.caption_file and len(args.caption_file) != len(resolved[2]):
            raise base.PipelineError(
                f"Expected {len(resolved[2])} --caption-file values, one for each Kaltura video; "
                f"received {len(args.caption_file)}."
            )
        return resolved

    originals = (base.CanvasClient, base.resolve_topic, base.download_kaltura_caption, base.lesson_filename)
    base.CanvasClient = Math2551CanvasClient
    base.resolve_topic = resolve_with_caption_count
    base.download_kaltura_caption = (
        imported_caption_downloader(args.caption_file)
        if args.caption_file
        else download_kaltura_caption
    )
    base.lesson_filename = lesson_filename
    try:
        return base.prepare(args)
    finally:
        base.CanvasClient, base.resolve_topic, base.download_kaltura_caption, base.lesson_filename = originals


def main() -> int:
    base.DEFAULT_COURSE_ID = COURSE_ID
    parser = base.parser()
    parser.description = "Prepare transcript-grounded MATH 2551 lessons from Canvas Kaltura sources."
    prepare_parser = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    ).choices["prepare"]
    prepare_parser.add_argument(
        "--caption-file",
        action="append",
        default=[],
        metavar="PATH",
        help="Use an exported English caption file for each Topic video, in page order.",
    )
    args = parser.parse_args()
    if args.command != "prepare":
        raise base.PipelineError(
            "This MATH 2551 skill currently supports only caption-source preparation; "
            "establish its course-specific writing rubric before validation, rendering, or publishing."
        )
    return prepare(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except base.PipelineError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(2)
