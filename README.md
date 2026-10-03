# Open Curriculum Lab

This project explores how AI can help maintain Canvas course materials. It began
with supplying course captions and a writing prompt in ChatGPT to produce
lesson HTML. The repository grew out of an attempt to automate source collection,
checking, and approved Canvas updates.

For Amogh and Dr. Mayer, the [project review](docs/review.md) explains that history,
what changed when we tried MATH 2551, and what still requires manual work.
The [saved Lesson 4.3](output/lessons/4.3-partial-derivatives.html) is the current
MATH 2551 example for review.

The local MATH 1554 workflow includes preparation, validation, preview, and
separately authorized Canvas updates. The MATH 2551 helper currently prepares
sources only. A separate private ChatGPT plugin contains authoring instructions
and works from supplied materials; it has no live Canvas connection. The
connection prototype remains on `canvas-mcp-bridge`, and integration work is
deferred.

## Further reading

- [Developer guide and local setup](docs/development.md)
- [MATH 2551 authoring skill](.agents/skills/build-math2551-lesson/SKILL.md)
- [MATH 2551 course context](.agents/skills/build-math2551-lesson/references/course-context.md)
- [Historical MATH 1554 accessibility audit](reports/WCAG_2.1_AA_AUDIT.md)
