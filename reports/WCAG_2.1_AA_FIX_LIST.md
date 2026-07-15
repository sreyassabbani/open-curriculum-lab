# Canvas WCAG 2.1 AA remediation checklist

Generated: 2026-07-14 21:44 EDT

Use this as the working queue. It contains **83 automated findings across 20 pages**. Check an item only after editing Canvas and rerunning `python audit_canvas.py`.

## Recommended order

1. Critical and High automated findings (access blocked or WCAG A failures).
2. Medium automated findings (structure, navigation clarity, and other material defects).
3. Low automated findings.
4. Manual reviews for media, linked documents, complex images, reflow, keyboard use, and reading order.

## High: Image alt text is a filename

Rule: `filename-alt` · 54 occurrence(s) on 18 page(s) · WCAG 1.1.1 (A)

**General pattern:** Replace the filename-style alt text with a concise description of the image's purpose. If the image is only decorative, use empty alt text instead.

- [ ] **[Module 1 Description and Learning Outcomes](https://gatech.instructure.com/courses/563104/pages/module-1-description-and-learning-outcomes/edit)** — `module-1-description-and-learning-outcomes` (4 occurrence(s))
  - Find `img`: `<img alt="medium1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119135" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119135/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="medium1.png"` with `alt="Medium difficulty"`.
  - Find `img`: `<img alt="description1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119163" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119163/preview?verifier=REDACTED" width="37"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="description1.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="objectives4.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119141" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119141/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="objectives4.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="task3.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119149" data-api-returntype="File" height="44" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119149/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="task3.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 2 Module 1: Linear Equations (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-2-module-1-linear-equations-cont-dot/edit)** — `week-2-module-1-linear-equations-cont-dot` (1 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 3 Module 1: Linear Equations (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-3-module-1-linear-equations-cont-dot/edit)** — `week-3-module-1-linear-equations-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Module 2 Description and Learning Outcomes ](https://gatech.instructure.com/courses/563104/pages/module-2-description-and-learning-outcomes/edit)** — `module-2-description-and-learning-outcomes` (6 occurrence(s))
  - Find `img`: `<img alt="easy1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119145" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119145/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="easy1.png"` with `alt="Easy difficulty"`.
  - Find `img`: `<img alt="medium1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119135" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119135/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="medium1.png"` with `alt="Medium difficulty"`.
  - Find `img`: `<img alt="hard1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119147" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119147/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="hard1.png"` with `alt="Hard difficulty"`.
  - Find `img`: `<img alt="description1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119163" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119163/preview?verifier=REDACTED" width="37"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="description1.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="objectives4.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119141" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119141/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="objectives4.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="task3.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119149" data-api-returntype="File" height="44" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119149/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="task3.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 6 Module 2: Matrix Algebra (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-6-module-2-matrix-algebra-cont-dot/edit)** — `week-6-module-2-matrix-algebra-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Module 3 Description and Learning Outcomes](https://gatech.instructure.com/courses/563104/pages/module-3-description-and-learning-outcomes/edit)** — `module-3-description-and-learning-outcomes` (6 occurrence(s))
  - Find `img`: `<img alt="easy1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119145" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119145/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="easy1.png"` with `alt="Easy difficulty"`.
  - Find `img`: `<img alt="medium1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119135" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119135/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="medium1.png"` with `alt="Medium difficulty"`.
  - Find `img`: `<img alt="hard1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119147" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119147/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="hard1.png"` with `alt="Hard difficulty"`.
  - Find `img`: `<img alt="description1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119163" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119163/preview?verifier=REDACTED" width="37"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="description1.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="objectives4.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119141" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119141/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="objectives4.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="task3.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119149" data-api-returntype="File" height="44" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119149/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="task3.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 7 Module 3: Determinants and Eigenvalues](https://gatech.instructure.com/courses/563104/pages/week-7-module-3-determinants-and-eigenvalues/edit)** — `week-7-module-3-determinants-and-eigenvalues` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 8 Module 3: Determinants and Eigenvalues (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-8-module-3-determinants-and-eigenvalues-cont-dot/edit)** — `week-8-module-3-determinants-and-eigenvalues-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 9 Module 3: Determinants and Eigenvalues (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-9-module-3-determinants-and-eigenvalues-cont-dot/edit)** — `week-9-module-3-determinants-and-eigenvalues-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Module 4 Description and Learning Outcomes](https://gatech.instructure.com/courses/563104/pages/module-4-description-and-learning-outcomes/edit)** — `module-4-description-and-learning-outcomes` (6 occurrence(s))
  - Find `img`: `<img alt="easy1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119145" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119145/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="easy1.png"` with `alt="Easy difficulty"`.
  - Find `img`: `<img alt="medium1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119135" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119135/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="medium1.png"` with `alt="Medium difficulty"`.
  - Find `img`: `<img alt="hard1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119147" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119147/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="hard1.png"` with `alt="Hard difficulty"`.
  - Find `img`: `<img alt="description1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119163" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119163/preview?verifier=REDACTED" width="37"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="description1.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="objectives4.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119141" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119141/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="objectives4.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="task3.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119149" data-api-returntype="File" height="44" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119149/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="task3.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 10 Module 4: Orthogonality](https://gatech.instructure.com/courses/563104/pages/week-10-module-4-orthogonality/edit)** — `week-10-module-4-orthogonality` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 11 Module 4: Orthogonality (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-11-module-4-orthogonality-cont-dot/edit)** — `week-11-module-4-orthogonality-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 12 Module 4: Orthogonality (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-12-module-4-orthogonality-cont-dot/edit)** — `week-12-module-4-orthogonality-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[4.5 Lecture Video](https://gatech.instructure.com/courses/563104/pages/4-dot-5-lecture-video/edit)** — `4-dot-5-lecture-video` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Module 5 Description and Learning Outcomes ](https://gatech.instructure.com/courses/563104/pages/module-5-description-and-learning-outcomes/edit)** — `module-5-description-and-learning-outcomes` (7 occurrence(s))
  - Find `img`: `<img alt="compass.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119143" data-api-returntype="File" height="89" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119143/download?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="compass.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="easy1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119145" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119145/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="easy1.png"` with `alt="Easy difficulty"`.
  - Find `img`: `<img alt="medium1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119135" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119135/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="medium1.png"` with `alt="Medium difficulty"`.
  - Find `img`: `<img alt="hard1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119147" data-api-returntype="File" height="45" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119147/preview?verifier=REDACTED" width="40"/>`
    - Change: Replace `alt="hard1.png"` with `alt="Hard difficulty"`.
  - Find `img`: `<img alt="description1.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119163" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119163/preview?verifier=REDACTED" width="37"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="description1.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="objectives4.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119141" data-api-returntype="File" height="40" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119141/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="objectives4.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="task3.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119149" data-api-returntype="File" height="44" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119149/preview?verifier=REDACTED" width="40"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="task3.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 13 Module 5: Symmetric Matrices and the SVD](https://gatech.instructure.com/courses/563104/pages/week-13-module-5-symmetric-matrices-and-the-svd/edit)** — `week-13-module-5-symmetric-matrices-and-the-svd` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 14 Module 5: Symmetric Matrices and the SVD (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-14-module-5-symmetric-matrices-and-the-svd-cont-dot/edit)** — `week-14-module-5-symmetric-matrices-and-the-svd-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.
- [ ] **[Week 15 Module 5: Symmetric Matrices and the SVD (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-15-module-5-symmetric-matrices-and-the-svd-cont-dot/edit)** — `week-15-module-5-symmetric-matrices-and-the-svd-cont-dot` (2 occurrence(s))
  - Find `img`: `<img alt="read.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119139" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119139/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="read.png"` with empty decorative alt text: `alt=""`.
  - Find `img`: `<img alt="watchvideo.png" data-api-endpoint="https://gatech.instructure.com/api/v1/courses/563104/files/75119151" data-api-returntype="File" height="50" loading="lazy" src="https://gatech.instructure.com/courses/563104/files/75119151/preview?verifier=REDACTED" width="50"/>`
    - Change: This icon repeats adjacent visible text; replace `alt="watchvideo.png"` with empty decorative alt text: `alt=""`.

## High: Link text is not descriptive out of context: 'link'

Rule: `vague-link-text` · 28 occurrence(s) on 1 page(s) · WCAG 2.4.4 (A)

**General pattern:** Replace vague link text with wording that makes sense out of context, such as `Download the Exam 1 review (PDF)` instead of `click here`.

- [ ] **[Studio Worksheets, Schedule, Recordings](https://gatech.instructure.com/courses/563104/pages/studio-worksheets-schedule-recordings/edit)** — `studio-worksheets-schedule-recordings` (28 occurrence(s))
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+08-18-2025/1_d1myzweb/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — August 18, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+08-20-2025/1_6ml3hx74/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — August 20, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+08-25-2025/1_jbwi32d5/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — August 25, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+08-27-2025/1_01s6kz67/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — August 27, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-03-2025/1_ol623ke3/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 3, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-08-2025/1_b8on2c7y/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 8, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-10-2025/1_s3238ev1/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 10, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-15-2025/1_c569sdsv/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 15, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-17-2025/1_nj58hgvd/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 17, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-22-2025/1_0peodtcq/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 22, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-24-2025/1_e05fl7sk/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 24, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+09-29-2025/1_igw02d4x/377263782" target="_blank">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — September 29, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-01-2025/1_8oyzk7ar/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 1, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-08-2025/1_fcvae58i/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 8, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-13-2025/1_g44u4akt/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 13, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-15-2025/1_qaxmg2x2/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 15, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-20-2025/1_6oj8840x/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 20, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-22-2025/1_rbio57lb/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 22, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-27-2025/1_3j65jkbg/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 27, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+10-29-2025/1_fup1f0ln/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — October 29, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+11-03-2025/1_tdsasdi6/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 3, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+11-05-2025/1_byu4hiu4/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 5, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+11-10-2025/1_fssp4xyu/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 10, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+11-12-2025/1_657smqnf/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 12, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+11-17-2025/1_kn529dqg/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 17, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554A+11-19-2025/1_7z6l47qy/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 19, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+11-24-2025/1_862cfcei/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — November 24, 2025`. Keep the existing Kaltura URL.
  - Find `a`: `<a class="inline_disabled" href="https://canvasgatechtest.kaf.kaltura.com/media/MATH+1554+12-01-2025/1_i2226mbk/377263782" target="_blank" title="Link">Link</a>`
    - Change: Replace the visible text `Link` with `Studio recording — December 1, 2025`. Keep the existing Kaltura URL.

## High: Elements must meet minimum color contrast ratio thresholds

Rule: `color-contrast` · 1 occurrence(s) on 1 page(s) · WCAG 1.4.3 (AA)

**General pattern:** Change the foreground or background color until normal text reaches 4.5:1 and large text reaches 3:1. Preserve the meaning without relying on color alone.

- [ ] **[2.4 Lecture Notes: Application: Partitioned Matrices](https://gatech.instructure.com/courses/563104/pages/2-dot-4-lecture-notes-application-partitioned-matrices/edit)** — `2-dot-4-lecture-notes-application-partitioned-matrices` (1 occurrence(s))
  - Find `div:nth-child(2) > h4`: `<h4 style="margin-top: 0; color: #27ae60;">Correct ✓</h4>`
    - Change: Change the heading color from `#27ae60` to `#1e7e45`; against its `#eafaf1` background this raises contrast from 2.66:1 to 4.71:1. Keep the checkmark so the status is not communicated by color alone.

## Manual-review queue

These are not automatically confirmed failures. Review the evidence and fix only when the content does not meet the stated requirement.

- [ ] **[Course Policies](https://gatech.instructure.com/courses/563104/pages/course-policies/edit)** — `course-policies`
  - Probable data table has no header cells (3)
- [ ] **[Distance Math Program Introduction (Kickoff)](https://gatech.instructure.com/courses/563104/pages/distance-math-program-introduction-kickoff/edit)** — `distance-math-program-introduction-kickoff`
  - <video> elements must have captions (1)
  - Embedded media accessibility requires manual verification (1)
- [ ] **[Studio Worksheets, Schedule, Recordings](https://gatech.instructure.com/courses/563104/pages/studio-worksheets-schedule-recordings/edit)** — `studio-worksheets-schedule-recordings`
  - Probable data table has no header cells (1)
- [ ] **[Recommended Study Strategies](https://gatech.instructure.com/courses/563104/pages/recommended-study-strategies/edit)** — `recommended-study-strategies`
  - Embedded media accessibility requires manual verification (1)
- [ ] **[Module 1 Description and Learning Outcomes](https://gatech.instructure.com/courses/563104/pages/module-1-description-and-learning-outcomes/edit)** — `module-1-description-and-learning-outcomes`
  - Probable layout table requires reading-order and reflow review (3)
- [ ] **[Week 3 Module 1: Linear Equations (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-3-module-1-linear-equations-cont-dot/edit)** — `week-3-module-1-linear-equations-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Module 2 Description and Learning Outcomes ](https://gatech.instructure.com/courses/563104/pages/module-2-description-and-learning-outcomes/edit)** — `module-2-description-and-learning-outcomes`
  - Probable layout table requires reading-order and reflow review (3)
- [ ] **[Week 6 Module 2: Matrix Algebra (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-6-module-2-matrix-algebra-cont-dot/edit)** — `week-6-module-2-matrix-algebra-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Module 3 Description and Learning Outcomes](https://gatech.instructure.com/courses/563104/pages/module-3-description-and-learning-outcomes/edit)** — `module-3-description-and-learning-outcomes`
  - Probable layout table requires reading-order and reflow review (3)
- [ ] **[Week 7 Module 3: Determinants and Eigenvalues](https://gatech.instructure.com/courses/563104/pages/week-7-module-3-determinants-and-eigenvalues/edit)** — `week-7-module-3-determinants-and-eigenvalues`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Week 8 Module 3: Determinants and Eigenvalues (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-8-module-3-determinants-and-eigenvalues-cont-dot/edit)** — `week-8-module-3-determinants-and-eigenvalues-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[3.4 Lecture Notes: Markov Chains ](https://gatech.instructure.com/courses/563104/pages/3-dot-4-lecture-notes-markov-chains/edit)** — `3-dot-4-lecture-notes-markov-chains`
  - Elements must meet minimum color contrast ratio thresholds (6)
- [ ] **[Week 9 Module 3: Determinants and Eigenvalues (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-9-module-3-determinants-and-eigenvalues-cont-dot/edit)** — `week-9-module-3-determinants-and-eigenvalues-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Module 4 Description and Learning Outcomes](https://gatech.instructure.com/courses/563104/pages/module-4-description-and-learning-outcomes/edit)** — `module-4-description-and-learning-outcomes`
  - Probable layout table requires reading-order and reflow review (3)
- [ ] **[Week 10 Module 4: Orthogonality](https://gatech.instructure.com/courses/563104/pages/week-10-module-4-orthogonality/edit)** — `week-10-module-4-orthogonality`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Week 11 Module 4: Orthogonality (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-11-module-4-orthogonality-cont-dot/edit)** — `week-11-module-4-orthogonality-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Week 12 Module 4: Orthogonality (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-12-module-4-orthogonality-cont-dot/edit)** — `week-12-module-4-orthogonality-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[4.5 Lecture Video](https://gatech.instructure.com/courses/563104/pages/4-dot-5-lecture-video/edit)** — `4-dot-5-lecture-video`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Module 5 Description and Learning Outcomes ](https://gatech.instructure.com/courses/563104/pages/module-5-description-and-learning-outcomes/edit)** — `module-5-description-and-learning-outcomes`
  - Probable layout table requires reading-order and reflow review (3)
- [ ] **[Week 13 Module 5: Symmetric Matrices and the SVD](https://gatech.instructure.com/courses/563104/pages/week-13-module-5-symmetric-matrices-and-the-svd/edit)** — `week-13-module-5-symmetric-matrices-and-the-svd`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Week 14 Module 5: Symmetric Matrices and the SVD (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-14-module-5-symmetric-matrices-and-the-svd-cont-dot/edit)** — `week-14-module-5-symmetric-matrices-and-the-svd-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)
- [ ] **[Week 15 Module 5: Symmetric Matrices and the SVD (Cont.)](https://gatech.instructure.com/courses/563104/pages/week-15-module-5-symmetric-matrices-and-the-svd-cont-dot/edit)** — `week-15-module-5-symmetric-matrices-and-the-svd-cont-dot`
  - Probable layout table requires reading-order and reflow review (2)

## Completion

- [ ] Rerun `python audit_canvas.py` after Canvas edits.
- [ ] Confirm the automated finding count is zero or document reviewed exceptions.
- [ ] Complete every applicable manual check in the full audit report.
- [ ] Record reviewer, review date, assistive technologies/browsers used, and any accepted exceptions.
