"""Focused checks for the read-only Canvas bridge."""
import unittest
from unittest.mock import patch

from canvas_bridge import server as bridge


class CanvasBridgeTests(unittest.TestCase):
    def test_topic_lookup_fetches_only_matching_pages(self):
        index = [
            {"title": "Topic 4.3: Partial Derivatives (4.3)", "url": "topic-4-3"},
            {"title": "Lesson 4.3: Partial Derivatives", "url": "lesson-4-3"},
            {"title": "Topic 4.5: Chain Rule (4.5)", "url": "topic-4-5"},
        ]
        pages = {
            "topic-4-3": {
                **index[0],
                "body": '<iframe title="Video 1" src="/external_tools/retrieve?url=https%3A%2F%2Fkaltura.example%2Flaunch"></iframe>',
            },
            "lesson-4-3": {**index[1], "body": ""},
        }

        class Client:
            fetched = []

            def list_pages(self):
                return index

            def get_page(self, slug):
                self.fetched.append(slug)
                return pages[slug]

        client = Client()
        source, target, frames = bridge._resolve_numeric_topic(client, "4.3")
        self.assertEqual(source["url"], "topic-4-3")
        self.assertEqual(target["url"], "lesson-4-3")
        self.assertEqual(len(frames), 1)
        self.assertEqual(client.fetched, ["topic-4-3", "lesson-4-3"])
        with self.assertRaises(ValueError):
            bridge._resolve_numeric_topic(client, "../other-course")

    def test_page_output_removes_embedded_credentials(self):
        body = '<a href="https://example.org/read?token=secret">Read</a><iframe title="V1" src="https://kaltura.example/?ks=secret"></iframe>'
        safe = bridge._safe_body(body)
        self.assertIn("Read", safe)
        self.assertIn("[Video: V1]", safe)
        self.assertNotIn("secret", safe)
        self.assertNotIn("iframe", safe)

    def test_missing_caption_is_reported_without_partial_success(self):
        source = {"url": "topic-4-3", "title": "Topic 4.3", "body": ""}
        target = {"url": "lesson-4-3", "title": "Lesson 4.3", "body": ""}
        frames = [{"title": "V1"}, {"title": "V2"}]
        side_effect = [
            ("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nFirst idea", {"language": "English"}),
            bridge.sources.base.PipelineError("session token secret"),
        ]
        with patch.object(bridge, "_client"), patch.object(
            bridge, "_resolve_numeric_topic", return_value=(source, target, frames)
        ), patch.object(bridge.sources, "download_kaltura_caption", side_effect=side_effect):
            bundle = bridge.get_topic_source_bundle("4.3")
        self.assertFalse(bundle["captions_complete"])
        self.assertEqual([v["status"] for v in bundle["videos"]], ["complete", "needs_caption_export"])
        self.assertNotIn("secret", str(bundle))


if __name__ == "__main__":
    unittest.main()
