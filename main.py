import os
from pprint import pprint

from canvasapi import Canvas
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://gatech.instructure.com"
COURSE_ID = 563104
API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")


def get_module_pages(course):
    """Return unique Canvas Page module items in dashboard order."""
    pages = []
    seen_slugs = set()

    for module in course.get_modules(include=["items"]):
        for item in module.items:
            if item["type"] != "Page":
                continue

            slug = item.get("page_url")
            if not slug or slug in seen_slugs:
                continue

            seen_slugs.add(slug)
            pages.append(
                {
                    "module": module.name,
                    "title": item["title"],
                    "slug": slug,
                    "published": item["published"],
                }
            )

    return pages


def main():
    if not API_KEY:
        raise SystemExit("CANVAS_ACCESS_TOKEN is missing from .env")

    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_ID)
    module_pages = get_module_pages(course)
    page_slugs = [page["slug"] for page in module_pages]
    lecture_note_slugs = [
        page["slug"]
        for page in module_pages
        if "lecture notes" in page["title"].lower()
    ]

    print(f"All page slugs ({len(page_slugs)}):")
    pprint(page_slugs, sort_dicts=False)

    print(f"\nLecture-note slugs ({len(lecture_note_slugs)}):")
    pprint(lecture_note_slugs, sort_dicts=False)


if __name__ == "__main__":
    main()
