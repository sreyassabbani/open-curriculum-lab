# Open Curriculum Lab: project review

For Amogh and Dr. Mayer · Reconciled October 3, 2026

## The idea

Use AI to help turn course videos and textbook readings into clear Canvas
lessons, with instructor review before release. The project also includes
tools for listing course pages and finding some accessibility problems.

**A MATH 2551 lesson example exists. An automatic connection from ChatGPT to
the live course does not.** Integration work is deferred while we review the
materials and whether the workflow is practical.

## How a lesson should be built

1. Read the actual Canvas Topic page, the course outline, and relevant earlier
   and later topics. Confirm which Lesson it belongs to.
2. Read the complete English captions for **every** video on that Topic page.
3. Read the relevant OpenStax section and adjacent sections alongside those
   captions. Captions supply course emphasis and examples; OpenStax supplies
   definitions, conditions, geometric explanations, and additional checks.
4. Write one connected lesson, placing short comprehension checks throughout
   it, near the concepts or examples they test, with answers nearby.
5. Review the mathematics, source coverage, and accessibility. Check equations
   and layout in the actual Canvas page before releasing it to students.

If any source is missing, pause drafting and identify exactly what is needed.
Check caption errors and disagreements with the textbook explicitly.

### The course controls the order

MATH 2551 does **not** follow OpenStax section order exactly. For example:

| Course Topic | Lesson / OpenStax section | Scope |
| --- | --- | --- |
| 2.3: Partial Derivatives | 4.3 | First, higher, and mixed partial derivatives; geometric interpretation; brief PDE context. |
| 2.4: The Chain Rule | 4.5 | Multivariable chain rule and implicit differentiation. |
| 2.6: Tangent Planes and Differentials | 4.4 | Differentiability, tangent planes, and linear approximation. |

A preview of a later method can be mentioned briefly; its full treatment belongs
in that later lesson. Ordinary single-variable differentiation rules still
apply in 4.3. Recheck the course mapping for each lesson. Compare OpenStax
[4.3](https://openstax.org/books/calculus-volume-3/pages/4-3-partial-derivatives),
[4.4](https://openstax.org/books/calculus-volume-3/pages/4-4-tangent-planes-and-linear-approximations),
and [4.5](https://openstax.org/books/calculus-volume-3/pages/4-5-the-chain-rule).

## What exists today

| Item | Evidence and limits |
| --- | --- |
| Lesson 4.3 | Written to Canvas September 15; the original chat reported checking repaired equations and leaving the page unpublished. The September 22 [saved revision](../output/lessons/4.3-partial-derivatives.html) narrows scope and distributes checks. The current live page has not been rechecked for this review. |
| Authoring instructions | The [MATH 2551 skill](../.agents/skills/build-math2551-lesson/SKILL.md) and [course map](../.agents/skills/build-math2551-lesson/references/course-context.md) record the source and scope rules above. |
| Local tools | MATH 1554 has preparation, validation, preview, and separately authorized Canvas updates. MATH 2551's helper prepares sources only. Automatic captions can fail and require browser exports. |
| ChatGPT plugin | [MATH 2551 Lesson Builder](https://chatgpt.com/plugins/plugins_6ab86870d7b881919c72a9eef0635517), v0.3.0, supplies instructions for drafting and review. It is private; reviewer access is unconfirmed. No live Canvas access or publishing tool. |
| Accessibility audit | The [July 14 MATH 1554 report](../reports/WCAG_2.1_AA_AUDIT.md) is a historical page-body scan. It does not certify current accessibility or establish that findings were fixed. |

The [Canvas Lesson 4.3 page](https://gatech.instructure.com/courses/588672/pages/lesson-4-dot-3-partial-derivatives)
requires course access. The saved revision is the reference for this review.

## ChatGPT access: what is practical now

Supply the Topic-page contents, course context, and complete captions. The
plugin uses them with OpenStax to draft or review a lesson. An authorized editor
copies the reviewed HTML into Canvas and checks the page. End users need no
GitHub connector, API key, or local setup. Obtaining all the source files still
takes manual effort, and that burden needs review.

Chat can use code tools when available to check files and calculations. That
does not automatically give it Canvas access or run this repository's scripts.
A GitHub connection supplies repository access, not a Canvas login.

## Why live Canvas access is deferred

There is a [read-only source prototype](https://github.com/sreyassabbani/open-curriculum-lab/tree/canvas-mcp-bridge/canvas_bridge)
using one operator's personal token. It cannot provide each course member their
own access. No service or ChatGPT connection is deployed; no administrator
request has been sent.

A shared version needs a maintained service and an approved Canvas sign-in
flow. [Canvas requires multi-user applications to use OAuth](https://developerdocs.instructure.com/services/canvas/oauth2/file.oauth)
instead of collecting personal tokens; [OpenAI also requires authorization for authenticated plugin access](https://developers.openai.com/plugins/build/auth).
Hosting, institutional approval, permission checks, and reliable captions remain
unresolved. The connection proposal and unsent administrator email are deferred
references, not an agreed plan.

## Requested review

- Does Lesson 4.3 have the right scope, examples, and level of explanation?
- Are the distributed checks and Canvas presentation useful for students?
- Is supplying source files practical for a small authoring pilot, or does that
  burden make the workflow unsuitable?

This review does not assume that the rest of the course is complete or that a
live integration will proceed. [Developer details](development.md) are available
separately.
