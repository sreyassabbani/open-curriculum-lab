# Open Curriculum Lab

Experiments in making Canvas course materials easier to maintain and study:
course inventories, accessibility checks, and lessons built from course videos
and textbook readings.

**For Amogh and Dr. Mayer:** start with the [project review](docs/review.md).
It explains what exists, what needs review, and why live Canvas access from
ChatGPT remains deferred.

## Current pieces

| Piece | Current status |
| --- | --- |
| Canvas inventory and accessibility audit | Local tools and a dated MATH 1554 audit; human review is still required. |
| MATH 1554 lesson workflow | Local caption preparation, drafting instructions, validation, preview, and separately authorized Canvas updates. |
| MATH 2551 lesson workflow | Source preparation and authoring instructions; a revised Lesson 4.3 is saved in this repository. |
| ChatGPT lesson plugin | Version 0.3.0, currently private. Works from supplied course pages and captions; no GitHub connection is required. |
| Live Canvas connection for ChatGPT | Experimental prototype on `canvas-mcp-bridge`; not deployed or connected. Further integration work is deferred. |

For MATH 2551, the actual course sequence controls lesson scope. Complete video
captions and OpenStax are read in parallel, and comprehension checks belong
beside the concepts they test.

## Links

- [Project review and review questions](docs/review.md)
- [Lesson 4.3: Partial Derivatives — HTML source](output/lessons/4.3-partial-derivatives.html)
- [MATH 2551 course context](.agents/skills/build-math2551-lesson/references/course-context.md)
- [Developer guide and local setup](docs/development.md)
- [Historical accessibility audit](reports/WCAG_2.1_AA_AUDIT.md)

The developer guide is for people operating the repository tools. ChatGPT users
do not need to install these tools. The private plugin's availability to other
reviewers has not been established.
