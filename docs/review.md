# Open Curriculum Lab: how the workflow has changed

For Amogh and Dr. Mayer · Updated October 3, 2026

## Where we started

The starting point was a transcript-and-prompt workflow in ChatGPT. Course
captions and a lesson-writing prompt were supplied in a conversation to produce
HTML for Canvas. Someone still had to gather the material, guide revisions,
review the result, and move it into the course.

The next idea was to make that process reusable: name a topic, collect its
video captions, follow the same authoring instructions, and produce a lesson
that could be checked and, with approval, saved to Canvas. That became the
repository workflow, first for MATH 1554 and then as an experiment for MATH 2551.

## What the repository added

The local tools find the course pages, retrieve English captions from Kaltura
when access permits, and save the sources together. The agent uses those
sources and the writing instructions to draft and revise a lesson. For MATH
1554, the tools also check the HTML, make a preview, and support a separately
approved update to an existing Canvas page.

This still requires someone operating the project with course access and a
local development setup. It reduces repeated work, but it does not remove
mathematical review or the need to inspect the actual Canvas page. Caption
retrieval is also imperfect: some MATH 2551 videos needed exports from an
already signed-in browser. The MATH 2551 helper currently prepares sources
only; the earlier lesson update was a separate authorized operation.

The project also produced a [MATH 1554 accessibility audit](../reports/WCAG_2.1_AA_AUDIT.md).
That July 14 report identifies problems detectable in page content. It is a
historical scan, and it does not establish that the findings have been fixed.

## What changed for MATH 2551

The initial MATH 2551 instructions treated captions as the primary source and
asked for a textbook cross-check. We revised that approach to read all video
captions and the relevant OpenStax sections in parallel. The captions establish
course emphasis and examples; the textbook contributes definitions, conditions,
geometric explanations, and useful additional examples. Errors or substantive
disagreements need to be checked explicitly.

The actual course sequence determines what belongs in each lesson. MATH 2551
is not a one-to-one copy of OpenStax: Topic 2.3 maps to Lesson 4.3, Topic 2.4 to
4.5, and Topic 2.6 to 4.4. Lesson 4.3 covers partial derivatives; the full
multivariable chain rule and implicit differentiation belong in 4.5. Tangent
planes and linear approximation belong in 4.4. A video can preview a later
method without making its full treatment part of the current lesson. Compare
OpenStax [4.3](https://openstax.org/books/calculus-volume-3/pages/4-3-partial-derivatives),
[4.4](https://openstax.org/books/calculus-volume-3/pages/4-4-tangent-planes-and-linear-approximations),
and [4.5](https://openstax.org/books/calculus-volume-3/pages/4-5-the-chain-rule).

We also moved short comprehension checks beside the concepts and examples they
test, with answers nearby. The lesson should develop as a connected explanation;
its layout should follow the material rather than force every idea into a
list, table, or callout. These changes are recorded in the
[authoring skill](../.agents/skills/build-math2551-lesson/SKILL.md) and
[course context map](../.agents/skills/build-math2551-lesson/references/course-context.md).

Lesson 4.3 was written to Canvas on September 15. The original chat reported
checking the repaired equation rendering and leaving the page unpublished.
The September 22 [saved revision](../output/lessons/4.3-partial-derivatives.html)
narrows the scope and distributes the checks. That saved revision is the
reference for this review; its agreement with the current
[Canvas page](https://gatech.instructure.com/courses/588672/pages/lesson-4-dot-3-partial-derivatives)
has not been rechecked. The Canvas link requires course access.

## The ChatGPT plugin and the remaining practical question

The plugin was an attempt to make the authoring guidance usable in ordinary
ChatGPT Chat without asking everyone to install the repository or connect
GitHub. The current [MATH 2551 Lesson Builder](https://chatgpt.com/plugins/plugins_6ab86870d7b881919c72a9eef0635517)
is private, and access for other reviewers has not been confirmed. It can guide
drafting and review from supplied sources. It cannot retrieve the live Canvas
course or save a lesson there. Someone still has to provide the Topic-page
contents, course context, and every video's complete captions, then transfer
the reviewed result into Canvas. Missing sources must be identified before
course-aligned drafting begins.

We explored a live connection to remove that manual source-gathering step. A
[local prototype](https://github.com/sreyassabbani/open-curriculum-lab/tree/canvas-mcp-bridge/canvas_bridge)
exists, but it uses one operator's personal token. A shared version would need
a maintained service, institutional support for a Canvas sign-in flow, and
permission checks for each user. [Canvas's multi-user access requirements](https://developerdocs.instructure.com/services/canvas/oauth2/file.oauth)
and [OpenAI's plugin authentication requirements](https://developers.openai.com/plugins/build/auth)
explain why a personal token alone is insufficient. Nothing has been deployed,
and no administrator request has been sent. This integration work is deferred.

For now, the useful review is whether Lesson 4.3 has the right scope, explanations,
and checks, and whether the remaining manual work makes this approach practical.
We have an authoring experiment and a lesson to examine; we have not established
a workflow that anyone with ChatGPT can use against the live course. Technical
setup and implementation details are in the [developer guide](development.md).
