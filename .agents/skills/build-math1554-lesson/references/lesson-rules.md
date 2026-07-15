# MATH 1554 Lecture-Lesson Rules

These rules normalize the public **MATH 1554 Lecture Notes Prompt** supplied for this project and the refinements made while producing Topic 4.3. Treat them as the canonical writing and review rubric.

## Source handling

- Combine all captions for one topic into one unified lesson.
- Treat the supplied captions as the source of truth for mathematical content.
- Ignore sequence numbers, timestamps, caption artifacts, repeated speech, false starts, and self-corrections.
- Clean grammar and reconstruct obvious caption errors only when the surrounding mathematics makes the intent clear.
- Use the clearest transcript examples. Do not invent unnecessary specifics when a detail is ambiguous.
- Produce a polished student page, not notes about the recordings.
- Never mention videos, lectures, transcripts, captions, timestamps, the professor, or what students watched.

## Required corrections

Use **Comprehension Checks** when there is more than one question.

Do not call mathematical properties “methods.” Prefer direct descriptions such as “A linearly independent set has no redundant vectors.” Properties requiring care include linear independence, spanning, onto, one-to-one, invertibility, being a subspace, rank, and dimension.

Remove incorrect content followed by a correction. Do not retain phrases such as “actually wait,” “I made a mistake,” or contradictory explanations.

Avoid proof-focused assessment language. Replace “How to Prove,” “Proof Strategy,” “Prove that,” and similar wording with “Checking,” “Determining,” “Process,” “Construction Method,” “Key Idea,” or “Quick Check.”

Give construction questions a complete object and property. For example, ask students to “Construct a 3 × 3 matrix with a pivot in every column but not every row,” not to “make a matrix with certain properties.”

## Mathematical guardrails

- A subset is any collection of vectors from \(\mathbb{R}^n\).
- A subspace is a subset closed under scalar multiplication and vector addition.
- Every subspace contains the zero vector; that fact alone is insufficient.
- \(\operatorname{Col} A\) is the span of the columns of \(A\).
- For an \(m\times n\) matrix, \(\operatorname{Col} A\subseteq\mathbb{R}^m\) and \(\operatorname{Nul} A\subseteq\mathbb{R}^n\).
- \(\operatorname{Nul} A\) is the solution set of \(A\mathbf{x}=\mathbf{0}\).
- A basis spans the subspace and is linearly independent.
- \(\dim H\) is the number of vectors in a basis for \(H\).
- \(\operatorname{rank} A=\dim(\operatorname{Col} A)\), equal to the number of pivot columns.
- Nullity is \(\dim(\operatorname{Nul} A)\), equal to the number of free variables.
- For an \(m\times n\) matrix, \(\operatorname{rank} A+\dim(\operatorname{Nul} A)=n\).
- A square \(n\times n\) matrix is invertible exactly when its rank is \(n\), equivalently when it has a pivot in every row and column.
- Identify a column-space basis by row reduction, then use the corresponding columns of the original matrix. Row operations can change column space.
- The zero subspace \(\{\mathbf{0}\}\) has dimension zero; the zero vector is not a basis vector.

## Tone

Write directly to MATH 1554 students. Be clear, polished, concise, student-friendly, mathematically accurate, and not proof-heavy or overly casual.

Useful labels include **Key Idea**, **Quick Check**, **Important**, **Example**, **Process**, and **Summary**. Use a label only when the box adds information. Delete a Process box that repeats the adjacent formula or worked example.

Avoid “obviously,” “trivial,” “just,” “we proved,” “how to prove,” and references to the source medium.

## Exact HTML frame and styling

Return only a single Canvas HTML fragment with this outer frame:

```html
<div id="dp-wrapper" class="dp-wrapper">
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333333; padding: 20px; border-radius: 8px; border: 1px solid #e1e1e1;">
...
</div>
</div>
```

Use these colors:

- Navy: `#003057`
- Gold: `#B3A369`
- Light-gray callout: `#f9f9f9`
- Light-blue comprehension block: `#f0f4f7`

Use exactly these top-level sections in order:

1. Motivating Questions and Objectives
2. Summary of Key Concepts
3. Comprehension Checks

The first section contains one connection sentence, three or four motivating questions, and this objective construction:

```html
<p>After completing the exercises in this topic, you should be able to ...</p>
```

Use this exact h2 style:

```html
<h2 style="color: #003057; border-bottom: 2px solid #B3A369; padding-bottom: 10px;">Section Title</h2>
```

Inside Summary of Key Concepts, use sequential navy h3 headings such as `1. Definition`, then finish with a numbered `Summary: Topic` h3 and the summary table.

Use this callout structure only when it adds a concise takeaway or example:

```html
<div style="background-color: #f9f9f9; padding: 15px; border-left: 5px solid #B3A369; margin: 20px 0;">
<strong>Key Idea:</strong>
<p style="margin-bottom: 0;">...</p>
</div>
```

Wrap every table in `<div class="dp-table-scroll">`. Use `width: 100%; border-collapse: collapse; margin: 20px 0;` on the table, navy/white header rows, and `padding: 10px; border: 1px solid #dddddd;` on cells. The final summary table has exactly these columns: **Concept**, **Meaning**, **Main Check**.

## Mathematical formatting

- Use `\(...\)` for short inline expressions and `\[...\]` for important displayed formulas.
- Use bold vectors consistently: `\mathbf{x}`, `\mathbf{b}`, and `\mathbf{0}`.
- Use `\mathbb{R}^n`, `\operatorname{Col} A`, `\operatorname{Nul} A`, `\dim H`, and `\operatorname{rank} A` consistently.
- Escape every matrix alignment ampersand as `&amp;` inside HTML.
- Do not put scripts, stylesheets, iframes, Markdown fences, citations, or a complete HTML document in the Canvas fragment.

## Topic-specific coverage

For homogeneous coordinates and transformations, include source-supported coverage of why ordinary translations are not linear, homogeneous coordinates in \(\mathbb{R}^2\), translation and data matrices, composition and rightmost-first order, rotation about a non-origin point, and three-dimensional homogeneous coordinates. Say that moving to homogeneous coordinates represents translations by matrix multiplication; do not claim they become linear in the original space.

For subsets, subspaces, column space, null space, and bases, include source-supported definitions, closure, the zero-vector condition, set-builder notation, nonexamples, ambient spaces, membership tests, basis construction, and the original-column warning.

For coordinate systems, dimension, rank, and invertibility, include source-supported basis coordinates, coefficient solving, dimension, the zero subspace, rank/nullity, rank-nullity, maximum rank, square-matrix invertibility, and equivalent invertibility conditions.

Do not force a topic-specific item that is absent from the supplied captions; flag the omission for review instead of fabricating content.

## Comprehension checks

Default to four to six short assessment-style checks. A seventh is acceptable only when it assesses a distinct, useful idea. Prefer identification, computation, interpretation, or construction over proof.

When a useful formula simplification or inference follows immediately from the lesson, consider asking students to derive it in a check rather than revealing it just beforehand.

Each check uses this structure, numbered sequentially:

```html
<div style="background-color: #f0f4f7; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
<p style="margin-top: 0;"><strong>Question 1:</strong> [Complete question]</p>
<details style="cursor: pointer; background: white; padding: 10px; border-radius: 5px; border: 1px solid #cccccc;">
<summary style="color: #003057;">Click to reveal the answer</summary>
<div style="margin-top: 10px; padding-top: 10px; border-top: 1px dashed #ccc;">
<p><strong>Answer:</strong> [Answer]</p>
<p style="margin-bottom: 0;"><strong>Explanation:</strong> [Explanation]</p>
</div>
</details>
</div>
```

The last block may omit `margin-bottom: 15px`. Avoid proof prompts, long algebra, vague construction tasks, and questions that duplicate one another.

## Final review

Confirm that the result is one unified lesson, uses the required section order and styles, contains no source-medium references or correction remnants, states every mathematical claim accurately, uses correct spaces/dimensions, discusses invertibility carefully, selects original columns for a column-space basis, uses collapsible checks, escapes matrix ampersands, and contains only the copy-ready Canvas fragment.
