"""Read-only MATH 2551 course sources for a private ChatGPT MCP connection."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup
from canvasapi import Canvas
from dotenv import dotenv_values
from mcp.server import MCPServer
from mcp.types import ToolAnnotations

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / ".agents/skills/build-math2551-lesson/scripts/canvas_lesson.py"
CANVAS_URL = "https://gatech.instructure.com"
COURSE_ID = 588672
TOPIC_NUMBER = re.compile(r"\d+(?:\.\d+)+\Z")
READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)

spec = importlib.util.spec_from_file_location("math2551_course_sources", SOURCE_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError("MATH 2551 source script is unavailable")
sources = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sources)

mcp = MCPServer("MATH 2551 course sources")


def _token() -> str:
    """Read the host secret, falling back to the repo's ignored local .env."""
    value = os.environ.get("CANVAS_ACCESS_TOKEN") or dotenv_values(ROOT / ".env").get("CANVAS_ACCESS_TOKEN")
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError("The Canvas token is not configured on the bridge host")
    return value.strip()


def _client(session: requests.Session) -> Any:
    return sources.Math2551CanvasClient(CANVAS_URL, COURSE_ID, _token(), session=session)


def _safe_body(body: str) -> str:
    """Keep lesson markup while removing embedded media URLs and query credentials."""
    soup = BeautifulSoup(body or "", "lxml")
    for tag in soup.find_all(["script", "form"]):
        tag.decompose()
    for frame in soup.find_all("iframe"):
        label = soup.new_tag("p")
        label.string = f"[Video: {frame.get('title', 'Untitled video')}]"
        frame.replace_with(label)
    for tag in soup.find_all(True):
        for attribute in ("href", "src", "data-api-endpoint"):
            value = tag.get(attribute)
            if isinstance(value, str):
                parts = urlsplit(value)
                tag[attribute] = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return sources.base.redact(str(soup))


def _page_record(page: dict[str, Any]) -> dict[str, str]:
    slug = str(page["url"])
    return {
        "title": str(page.get("title", "")),
        "slug": slug,
        "url": f"{CANVAS_URL}/courses/{COURSE_ID}/pages/{quote(slug, safe='')}",
        "body_html": _safe_body(str(page.get("body", ""))),
    }


def _resolve_numeric_topic(client: Any, topic: str) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    if not TOPIC_NUMBER.fullmatch(topic):
        raise ValueError("Use a course topic number such as 4.3")
    index = client.list_pages()
    topic_pages = [page for page in index if sources.is_source_page(page)]
    preferred = [page for page in topic_pages if topic in sources.parenthetical_title_numbers(str(page.get("title", "")))]
    candidates = preferred or [
        page for page in topic_pages
        if re.match(rf"\s*topic\s+{re.escape(topic)}\b", str(page.get("title", "")), re.I)
    ]
    targets = [
        page for page in index
        if sources.is_target_page(page) and topic in sources.title_numbers(str(page.get("title", "")))
    ]
    pages = [client.get_page(str(page["url"])) for page in candidates + targets]
    return sources.resolve_topic(pages, topic)


@mcp.tool(title="Read MATH 2551 course outline", annotations=READ_ONLY)
def get_course_outline() -> dict[str, Any]:
    """Read the live module order and page titles before deciding a lesson's scope."""
    course = Canvas(CANVAS_URL, _token()).get_course(COURSE_ID)
    modules: list[dict[str, Any]] = []
    for module in course.get_modules():
        items = [
            {
                "title": str(getattr(item, "title", "")),
                "type": str(getattr(item, "type", "")),
                "page_slug": getattr(item, "page_url", None),
            }
            for item in module.get_module_items()
        ]
        modules.append({"name": str(module.name), "items": items})
    return {"course_id": COURSE_ID, "course_name": str(course.name), "modules": modules}


@mcp.tool(title="Read a MATH 2551 course page", annotations=READ_ONLY)
def get_course_page(page_slug: str) -> dict[str, str]:
    """Read a live Topic or Lesson page from this course to check nearby scope."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,180}", page_slug):
        raise ValueError("Invalid Canvas page slug")
    with requests.Session() as session:
        page = _client(session).get_page(page_slug)
    if not (sources.is_source_page(page) or sources.is_target_page(page)):
        raise ValueError("Only Topic and Lesson pages are available through this tool")
    return _page_record(page)


@mcp.tool(title="Read MATH 2551 topic and captions", annotations=READ_ONLY)
def get_topic_source_bundle(topic: str) -> dict[str, Any]:
    """Read the live Topic and Lesson pages plus every video's complete English captions."""
    with requests.Session() as session:
        client = _client(session)
        source, target, frames = _resolve_numeric_topic(client, topic.strip())
        videos: list[dict[str, Any]] = []
        for index, frame in enumerate(frames, start=1):
            video: dict[str, Any] = {"index": index, "title": frame["title"]}
            try:
                raw, metadata = sources.download_kaltura_caption(client, frame)
                transcript = sources.base.normalize_caption_text(raw)
                video.update({
                    "status": "complete",
                    "caption_text": transcript,
                    "caption_sha256": hashlib.sha256(transcript.encode("utf-8")).hexdigest(),
                    "language": metadata.get("language", "English"),
                })
            except (sources.base.PipelineError, requests.RequestException):
                video.update({
                    "status": "needs_caption_export",
                    "reason": "Automatic Kaltura retrieval failed; supply this video's complete English caption export.",
                })
            videos.append(video)
    return {
        "course_id": COURSE_ID,
        "topic": topic.strip(),
        "topic_page": _page_record(source),
        "lesson_page": _page_record(target),
        "videos": videos,
        "captions_complete": all(video["status"] == "complete" for video in videos),
    }
