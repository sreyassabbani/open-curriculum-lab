# Canvas math: authoring and live verification

## Preserve the source notation

Author inline math as `\(f_x\)` and display math as `\[ ... \]`. Plain `(f_x)` is ordinary text, not a math delimiter. Preserve literal backslashes through every string/JSON/shell layer; for example, use Python raw strings or escape backslashes in JavaScript strings. Inspect the actual saved HTML, not just the generating code.

When repairing missing delimiters, distinguish prose parentheses from mathematical grouping. Do not blanket-replace parentheses or wrap parts of an existing display formula in inline delimiters. Preserve function arguments and nested parentheses. Review the entire lesson, including headings, objectives, tables, and collapsed answers.

## Native equation markup when needed

If raw delimiters do not render reliably in the target Canvas page, use Canvas's native equation markup. The following pattern was verified for MATH 2551 Lesson 4.3 on 2026-09-15. It is a supported fallback for that observed environment, not evidence that raw LaTeX is universally unsupported.

```python
import html
from urllib.parse import quote

def canvas_equation(tex, canvas_origin, display=False):
    tex = tex.strip()
    if display:
        tex = r'\displaystyle ' + tex
    escaped = html.escape(tex, quote=True)
    encoded = quote(quote(tex, safe=''), safe='')
    image = (
        f'<img class="equation_image" '
        f'src="{canvas_origin}/equation_images/{encoded}?scale=1" '
        f'alt="LaTeX: {escaped}" title="{escaped}" '
        f'data-equation-content="{escaped}">'
    )
    if display:
        return (
            '<div style="text-align: center; margin: 20px 0; overflow-x: auto;">'
            + image + '</div>'
        )
    return image
```

Pass only the formula as `tex`, without `\(...\)` or `\[...\]`. Inline equations belong directly in the prose. Display equations need both:

- `\displaystyle` for full-size fractions and limits beneath operators;
- a centered parent block for layout.

Canvas can replace an `img.equation_image` with MathJax elements. Centering applied only to the image can disappear during that replacement. Keep alignment, spacing, and horizontal overflow on the parent. This approach retains LaTeX in `data-equation-content` and accessible alt text.

Do not insert hidden dummy equations or page-level MathJax scripts as speculative fixes. The standalone preview helper loads MathJax itself; that does not describe how Canvas loads it.

## Verify the saved page after rendering

1. Read back the exact target page through the API. Confirm formula markup, display wrappers, and preserved publication state.
2. Reload the live page and allow its asynchronous rendering to complete. A screenshot immediately after reload may show raw text, temporary image alt text, or partially loaded equations. Inspect the resulting DOM and another screenshot before diagnosing a persistent failure. Do not repeatedly rewrite the page in response to intermediate loading states.
3. Check that inline expressions such as `f_x` have subscripts and no literal delimiter parentheses. Check that all display blocks are centered and that a limit/fraction example has full display styling.
4. Check all equations for renderer errors and unrendered source, including expanded answers. Inspect representative screenshots from the top, examples, and bottom. API success or an accessibility tree alone does not prove visual correctness.

## What actually went wrong in Lesson 4.3

The generated source lost inline delimiter backslashes, leaving `(f_x)` and similar text. A first repair converted only display formulas, leaving inline math broken. Those equation images also lacked `\displaystyle`, and alignment was placed on images that Canvas subsequently replaced. Repairing all inline formulas, adding display style, and centering parent blocks resolved the observed defects.

Earlier conclusions that MathJax failed to load or that equation URLs were malformed were not established: the same page later rendered, and the URLs returned valid SVG. Treat loading snapshots as provisional evidence, not a root-cause diagnosis.
