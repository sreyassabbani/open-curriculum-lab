from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "build-math2551-lesson"
    / "scripts"
    / "canvas_lesson.py"
)
SPEC = importlib.util.spec_from_file_location("math2551_canvas_lesson", SCRIPT)
assert SPEC and SPEC.loader
math2551 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(math2551)


PAGES = [
    {
        "title": "Topic 2.3: Partial Derivatives (4.3)",
        "url": "topic-2-dot-3-partial-derivatives-4-dot-3",
        "body": """<iframe title="Visible player" src="https://cdnapisec.kaltura.com/embed?entry_id=public"></iframe>
<iframe title="Course player" src="https://canvas.example.test/courses/1/external_tools/retrieve?url=https%3A%2F%2Fkaltura.example.test%2Flaunch"></iframe>""",
    },
    {
        "title": "Lesson 4.3: Partial Derivatives",
        "url": "lesson-4-dot-3-partial-derivatives",
        "body": "",
    },
    {
        "title": "Topic 4.3: Conservative Fields (6.3)",
        "url": "topic-4-dot-3-conservative-fields-6-dot-3",
        "body": "",
    },
]


class Math2551TopicResolutionTests(unittest.TestCase):
    def test_parenthetical_textbook_section_selects_the_correct_topic_and_lesson(self) -> None:
        source, target, frames = math2551.resolve_topic(PAGES, "4.3")

        self.assertEqual(source["url"], "topic-2-dot-3-partial-derivatives-4-dot-3")
        self.assertEqual(target["url"], "lesson-4-dot-3-partial-derivatives")
        self.assertEqual(frames[0]["external_tool_url"], "https://kaltura.example.test/launch")


if __name__ == "__main__":
    unittest.main()
