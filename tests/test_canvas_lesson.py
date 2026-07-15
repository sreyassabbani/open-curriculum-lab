from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "build-math1554-lesson"
    / "scripts"
    / "canvas_lesson.py"
)
SPEC = importlib.util.spec_from_file_location("canvas_lesson", SCRIPT)
assert SPEC and SPEC.loader
canvas_lesson = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(canvas_lesson)


H2_STYLE = "color: #003057; border-bottom: 2px solid #B3A369; padding-bottom: 10px;"
CHECK_STYLE = "background-color: #f0f4f7; padding: 20px; border-radius: 8px; margin-bottom: 15px;"


def valid_lesson() -> str:
    checks = []
    for number in range(1, 5):
        checks.append(
            f"""
<div style="{CHECK_STYLE}">
<p style="margin-top: 0;"><strong>Question {number}:</strong> Calculate a value for this complete exercise.</p>
<details style="cursor: pointer; background: white; padding: 10px; border-radius: 5px; border: 1px solid #cccccc;">
<summary style="color: #003057;">Click to reveal the answer</summary>
<div style="margin-top: 10px; padding-top: 10px; border-top: 1px dashed #ccc;">
<p><strong>Answer:</strong> {number}</p>
<p style="margin-bottom: 0;"><strong>Explanation:</strong> The calculation gives {number}.</p>
</div>
</details>
</div>"""
        )
    return f"""<div id="dp-wrapper" class="dp-wrapper">
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333333; padding: 20px; border-radius: 8px; border: 1px solid #e1e1e1;">
<h2 style="{H2_STYLE}">Motivating Questions and Objectives</h2>
<p>This topic connects a vector to its closest representative in a subspace.</p>
<ul><li>What is a projection?</li><li>How is it calculated?</li><li>What does the residual mean?</li></ul>
<p>After completing the exercises in this topic, you should be able to calculate a projection and interpret its residual.</p>
<h2 style="{H2_STYLE}">Summary of Key Concepts</h2>
<h3 style="color: #003057;">1. Projection</h3><p>A projection belongs to the target subspace.</p>
<h3 style="color: #003057;">2. Residual</h3><p>The residual is perpendicular to that subspace.</p>
<h3 style="color: #003057;">3. Summary: Projection and Residual</h3>
<div class="dp-table-scroll"><table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
<thead><tr style="background-color: #003057; color: white;"><th>Concept</th><th>Meaning</th><th>Main Check</th></tr></thead>
<tbody><tr><td>Projection</td><td>Subspace component</td><td>Membership</td></tr></tbody></table></div>
<h2 style="{H2_STYLE}">Comprehension Checks</h2>
{''.join(checks)}
</div></div>"""


def lesson_pages() -> list[dict[str, object]]:
    return [
        {
            "title": "4.3 Lecture Video",
            "url": "4-dot-3-lecture-video",
            "body": """<iframe title="Math1554_M4W11T1L1_The_Orthogonal_Decomposition_Theorem" src="https://example.test/retrieve?resource_link_lookup_uuid=first"></iframe>
<iframe title="Math1554_M4W11T1L2_The_Best_Approximation_Theorem" src="https://example.test/retrieve?resource_link_lookup_uuid=second"></iframe>""",
        },
        {
            "title": "4.3 Lecture Notes: Orthogonal Projections",
            "url": "4-dot-3-lecture-notes-orthogonal-projections",
            "body": "old body",
        },
        {
            "title": "4.4 Lecture Video",
            "url": "4-dot-4-lecture-video",
            "body": '<iframe title="Math1554_M4W11T2L1_Gram_Schmidt" src="https://example.test/retrieve?resource_link_lookup_uuid=third"></iframe>',
        },
        {
            "title": "4.4 Lecture Notes: Gram-Schmidt",
            "url": "4-dot-4-lecture-notes-gram-schmidt",
            "body": "",
        },
    ]


class TopicResolutionTests(unittest.TestCase):
    def test_numeric_code_and_title_resolve_the_same_topic(self) -> None:
        for topic in ("4.3", "M4W11T1", "Orthogonal Decomposition"):
            source, target, frames = canvas_lesson.resolve_topic(lesson_pages(), topic)
            self.assertEqual(source["url"], "4-dot-3-lecture-video")
            self.assertEqual(target["url"], "4-dot-3-lecture-notes-orthogonal-projections")
            self.assertGreaterEqual(len(frames), 1)

    def test_media_prefix_filters_unrelated_frames(self) -> None:
        _, _, frames = canvas_lesson.resolve_topic(lesson_pages(), "M4W11T1")
        self.assertEqual([item["resource_link_lookup_uuid"] for item in frames], ["first", "second"])

    def test_missing_topic_fails_without_guessing(self) -> None:
        with self.assertRaises(canvas_lesson.TopicResolutionError):
            canvas_lesson.resolve_topic(lesson_pages(), "9.9")


class CaptionTests(unittest.TestCase):
    def test_caption_selection_prefers_ready_english_srt(self) -> None:
        selected = canvas_lesson.select_english_caption(
            [
                {"id": "draft", "status": 1, "languageCode": "en", "format": "1"},
                {"id": "vtt", "status": 2, "languageCode": "en", "format": "3"},
                {"id": "srt", "status": 2, "language": "English", "format": "1"},
            ]
        )
        self.assertEqual(selected["id"], "srt")

    def test_srt_normalization_removes_timing_and_duplicate_cues(self) -> None:
        raw = """1
00:00:00,000 --> 00:00:02,000
The first line
continues here.

2
00:00:02,000 --> 00:00:04,000
The first line continues here.

3
00:00:04,000 --> 00:00:05,000
Next idea.
"""
        self.assertEqual(
            canvas_lesson.normalize_caption_text(raw),
            "The first line continues here.\nNext idea.\n",
        )

    def test_redaction_hides_signed_values(self) -> None:
        value = "https://example.test/path/ks/secret?session_token=other&verifier=third"
        redacted = canvas_lesson.redact(value)
        self.assertNotIn("secret", redacted)
        self.assertNotIn("other", redacted)
        self.assertNotIn("third", redacted)

    def test_caption_extension_detects_supported_formats(self) -> None:
        self.assertEqual(canvas_lesson.caption_extension("WEBVTT\n\n"), ".vtt")
        self.assertEqual(canvas_lesson.caption_extension("<?xml?><tt></tt>"), ".dfxp")
        self.assertEqual(canvas_lesson.caption_extension("1\n00:00:00,000 -->"), ".srt")


class ValidationTests(unittest.TestCase):
    def test_valid_fragment_passes(self) -> None:
        result = canvas_lesson.validate_html_text(valid_lesson())
        self.assertEqual(result["errors"], [])

    def test_banned_source_language_and_raw_matrix_ampersand_fail(self) -> None:
        broken = valid_lesson().replace(
            "A projection belongs to the target subspace.",
            "In this video, use \\[\\begin{pmatrix}1 & 0\\end{pmatrix}\\].",
        )
        errors = canvas_lesson.validate_html_text(broken)["errors"]
        self.assertTrue(any("videos" in item.lower() for item in errors))
        self.assertTrue(any("ampersands" in item.lower() for item in errors))

    def test_seventh_check_is_warning_not_error(self) -> None:
        fragment = valid_lesson()
        extra = fragment[fragment.index(f'<div style="{CHECK_STYLE}">') : fragment.rindex("</div></div>")]
        # Reusing the full sequence would duplicate numbers, so append three renamed copies.
        single = extra[: extra.index(f'<div style="{CHECK_STYLE}">', 1) if f'<div style="{CHECK_STYLE}">' in extra[1:] else len(extra)]
        for number in (5, 6, 7):
            fragment = fragment.replace("</div></div>", single.replace("Question 1", f"Question {number}") + "</div></div>")
        result = canvas_lesson.validate_html_text(fragment)
        self.assertFalse(any("4 to 6" in item for item in result["errors"]))
        self.assertTrue(any("Seven" in item for item in result["warnings"]))


class FakeCanvas:
    def __init__(self, current: dict[str, object], stored: dict[str, object] | None = None) -> None:
        self.current = current
        self.stored = stored or current
        self.updated: tuple[str, str] | None = None
        self.reads = 0

    def get_page(self, slug: str) -> dict[str, object]:
        self.reads += 1
        return self.current if self.reads == 1 else self.stored

    def update_page_body(self, slug: str, body: str) -> dict[str, object]:
        self.updated = (slug, body)
        return self.stored


class PublishTests(unittest.TestCase):
    def make_run(self, directory: Path, old_body: str = "old") -> dict[str, object]:
        lesson = valid_lesson()
        (directory / "lesson.html").write_text(lesson, encoding="utf-8")
        manifest = {
            "api_url": "https://canvas.example.test",
            "course_id": 1,
            "target_page": {
                "slug": "target-page",
                "title": "Target Page",
                "updated_at": "before",
                "body_sha256": canvas_lesson.sha256_text(old_body),
                "backup_path": str(directory / "canvas-before.html"),
            },
        }
        (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (directory / "canvas-before.html").write_text(old_body, encoding="utf-8")
        (directory / "validation.json").write_text(
            json.dumps(
                {
                    "errors": [],
                    "lesson_sha256": canvas_lesson.sha256_text(lesson),
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def test_publish_aborts_when_canvas_changed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            self.make_run(run_dir)
            fake = FakeCanvas({"body": "newer", "updated_at": "after"})
            args = argparse.Namespace(run_dir=str(run_dir), confirm_slug="target-page")
            with patch.object(canvas_lesson, "load_canvas_for_manifest", return_value=fake):
                with self.assertRaises(canvas_lesson.PipelineError):
                    canvas_lesson.publish(args)
            self.assertIsNone(fake.updated)

    def test_publish_updates_body_after_exact_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            self.make_run(run_dir)
            current = {
                "title": "Target Page",
                "body": "old",
                "updated_at": "before",
                "published": True,
            }
            stored = {**current, "body": valid_lesson(), "updated_at": "after"}
            fake = FakeCanvas(current, stored)
            args = argparse.Namespace(run_dir=str(run_dir), confirm_slug="target-page")
            with (
                patch.object(canvas_lesson, "load_canvas_for_manifest", return_value=fake),
                patch.object(canvas_lesson, "run_axe", return_value=[]),
            ):
                self.assertEqual(canvas_lesson.publish(args), 0)
            self.assertEqual(fake.updated, ("target-page", valid_lesson()))
            updated_manifest = json.loads((run_dir / "manifest.json").read_text())
            self.assertIn("publication", updated_manifest)


if __name__ == "__main__":
    unittest.main()
