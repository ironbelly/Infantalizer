# Phase 2 QA — Serialized Fix Report

**Date:** 2026-07-09
**Role:** serialized fix agent (Phase 2 phase-gate QA)
**fix_authorization:** true
**Files touched:**
- A = `laf-adaptation/skills/chapter-materialize/SKILL.md`
- B = `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml`

All 8 findings (I-1..I-4, M-1..M-4) applied in-place. Edits are surgical (added clauses/lines only);
no section was rewritten.

---

## IMPORTANT findings

### I-1 (F1) — Mode-C "exists and validates" now defined — FILE A, Stage 0.2 item 1
Added a bolded testable definition inline after "already exists and validates":
> **`validates` = every file matches the canonical `ch-<NN>.txt` name (zero-padded, contiguous ordinals
> from 01, no gaps), each is non-empty, and `order == numeric id`.** Adopt only when validation passes;
> otherwise fall through to `folder` / ambiguity.

### I-2 (F2) — "non-canonical per-chapter files" predicate surfaced — FILE A, Stage 0.2 item 2
Added inline after "≥2 non-canonical per-chapter files":
> **`non-canonical` = a per-chapter file whose name does NOT already match the canonical
> `source/<slug>/ch-<NN>.txt` form (i.e. it needs materialization, not adoption)** — this distinguishes
> Mode A input from an already-adopted Mode C set.

### I-3 (F3) — CERTAIN rule "AND no contradiction" operationalized — FILE A, §"Confidence rule (load-bearing)"
The bolded sentence `**"CERTAIN requires ≥2 independent agreeing signals and no contradiction."**` was
NOT modified. A non-bolded operationalization clause was inserted ADJACENT (immediately after the bolded
sentence, before the existing "One strong signal" text):
> A *contradiction* = two independent signals disagree on the same fact — different boundary offsets for
> the same chapter, different chapter counts (TOC vs body-heading vs filename), or different
> titles/ordinals. Any contradiction caps the affected boundary at UNCERTAIN regardless of signal count.

Verified: the three bolded sentences in this section (CERTAIN rule, "Single-signal boundaries are capped
at PROBABLE", "No writes in this stage") remain byte-identical.

### I-4 (F5) — PDF extraction mechanism named under ADR-006 — FILE A, §"Format normalization & fidelity"
Extended the `**PDF**` bullet with the mechanism:
> PDF text is obtained by the model reading the PDF directly (the executing model's native PDF-read
> capability); NO extraction script is added (ADR-006). PDF sources are inherently lower-fidelity:
> extraction garble (broken words, ligatures, repeated page headers) caps the affected boundaries at
> UNCERTAIN and blocks greenlight until a human accepts the result or supplies a cleaner source (per the
> PDF failure-mode row).

---

## MINOR findings

### M-1 (F4) — dangling `§B6` anchor fixed — FILE B, confidence_rule comment
Changed the reference from `SKILL.md §B6 ("Confidence rule (load-bearing)")` to the real heading:
> The AUTHORITATIVE copy lives in SKILL.md `### Confidence rule (load-bearing)`.

Verified the target heading `### Confidence rule (load-bearing)` exists in SKILL.md (line 80).

### M-2 (F6) — hash-identical monolith tie-break made deterministic — FILE A, §"Idempotency, collisions, backward-compat"
Added a new bullet before the "Collision" bullet:
> **Duplicate-monolith canonical pick (deterministic):** when duplicates are byte-identical (same
> sha256), pick the canonical by the shortest filename, tie-broken by lexicographic order (so the
> un-suffixed base name wins over `... copy N`); the rest are `role: ignored_duplicate`.

### M-3 (F7) — Stage 0.1 role assignment marked PROVISIONAL — FILE A, Stage 0.1 item 4
Appended to the `Populate raw_sources[]` item:
> This `raw_sources[].role` is a PROVISIONAL classification finalized after the Stage 0.3 evidence pass
> (e.g. `front_matter` vs `chapter_file` can flip once headings are mapped).

### M-4 (domain O2) — base monolith without `copy` token — FILE B, `ignore_globs` comment
Added a 4-line comment above `ignore_globs` clarifying it is a HINT only; byte-identical duplicates
(incl. a base monolith named without "copy") are resolved by the sha256 tie-break (M-2), not glob alone;
the hash rule is authoritative.

---

## DO-NOT-TOUCH verification (all confirmed unchanged)

| Frozen item | Location | Status |
|---|---|---|
| 16-row failure-modes table | A §11 (lines 149–166) | byte-identical — 16 data rows intact |
| `chapter-manifest.yaml` v1 schema fenced block | A §12 (from line 176) | byte-identical — untouched, all edits above it |
| Bolded CERTAIN confidence-rule sentence | A §"Confidence rule" | byte-identical (I-3 added adjacent, not modified) |
| Bolded deferred-write invariant sentence | A Stage 0.4 (line 95) | byte-identical |
| Frontmatter (name + description) | A lines 1–8 | byte-identical |

## Parse / integrity check

`python3 -c "import yaml; yaml.safe_load(open('.../boundary-rules.yaml'))"` → **YAML OK** (parses clean
after M-1 + M-4 edits).

---

## VERDICT: FIXED (all applied)

All 4 IMPORTANT (I-1..I-4) and all 4 MINOR (M-1..M-4) findings applied in-place and re-verified. All
DO-NOT-TOUCH frozen content confirmed byte-identical. `boundary-rules.yaml` parses.
