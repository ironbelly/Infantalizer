# QA Report — Phase-Gate (Phase 2), Internal-Consistency Lens

**Topic:** chapter-materialize skill (SKILL.md + resources/boundary-rules.yaml)
**Date:** 2026-07-09
**Phase:** phase-gate (Phase 2) — internal-consistency lens
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Mode:** ADVERSARIAL (assume ≥5 errors within lens)

---

## Overall Verdict: PASS

One MINOR dangling-reference finding; no CRITICAL/IMPORTANT internal-consistency defects.
The MINOR item is faithful to the blueprint's own naming and non-blocking. No CERTAIN/PROBABLE
threshold drift, no schema/prose field mismatch, no count contradiction, no mode-naming
contradiction, no failure-table/stage-prose contradiction.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Confidence rule consistent across SKILL.md §6 ↔ boundary-rules.yaml mirror | PASS | SKILL.md L74–76: "**CERTAIN requires ≥2 independent agreeing signals and no contradiction**" (bolded), "**Single-signal boundaries are capped at PROBABLE**". YAML L75–77: `CERTAIN_requires_min_agreeing_signals: 2`, `single_signal_cap: PROBABLE`, `uncertain_triggers: [missing_signal, contradictory_signal, manual_repair, pdf_garble]`. UNCERTAIN triggers map exactly to prose L75 ("Missing/contradictory signals, manual repair, or PDF garble"). Zero numeric drift; grep for alternate signal counts found none. |
| 2 | Five evidence layers: SKILL.md §6 table (5 rows) ↔ YAML five top-level layer keys, same set & order | PASS | SKILL.md L66–70: TOC/anchor → Body-heading → Filename → Content sanity → Count reconciliation. YAML L9/25/44/59/66: `toc_anchor_map` → `body_heading_map` → `filename_map` → `content_sanity` → `count_reconciliation` (then `confidence_rule` mirror). Identical set, identical order. |
| 3 | Manifest schema fields named in prose all present in v1 schema block (and vice-versa) | PASS | `raw_sources[]`+role enum: prose L36–37 == schema L164–166 (byte-identical `monolith \| chapter_file \| front_matter \| ignored_duplicate`). `provenance.class: ADOPTED` prose L117 ↔ schema enum `MATERIALIZED \| ADOPTED` L182. `review.status PENDING/CONFIRMED` prose L88/97/120 ↔ schema L202. `ambiguous_splits` prose L89/94 ↔ schema L200. `normalization_event`/`source_fidelity_risk` prose L107 ↔ schema `normalization_events` L189–192 (singular concept / plural list-field — standard, not a mismatch). `needs_human_review` prose L94 ↔ schema L193/199. No field named in prose is absent from schema; no orphan schema field named in the lens. |
| 4 | Mode-detect precedence (adopt>folder>file>ambiguity) consistent between Stage 0.2 and input_mode Mode A/B/C mapping | PASS | Stage 0.2 L44–47: adopt(Mode C) → folder(Mode A) → file(Mode B) → ambiguity-HALT. Schema `input_mode: folder \| single-file \| adopt-existing` L162. Mapping is 1:1 (file→single-file, adopt→adopt-existing, folder→folder). Same dual naming appears verbatim in the driving spec (§3 uses `file`, §5 schema uses `single-file`) and the description line L4 ("adopt/folder/file"). Naming variance is carried faithfully, not a contradiction. |
| 5 | 16-row failure table does not contradict stage prose | PASS | Table byte-identical to driving spec (`diff` = IDENTICAL). "Monolith duplicates → …`ignored_duplicate`" (L143) matches Stage 0.1 `raw_sources` role enum (L37). "Existing source collision → adopt if hash matches; else explicit overwrite plan at gate" (L144) matches §Idempotency "Collision: …never clobbered → HALT-and-ask at the gate" (L123–124) and Mode C adopt (L116–119). "Mode ambiguity → `mode_confidence: UNCERTAIN`" (L147) matches Stage 0.2 ambiguity clause (L47–52). |
| 6 | No count contradictions ("five" layers, 16 failure modes, chapter_count) | PASS | SKILL.md `### The five evidence layers` table = exactly 5 rows. Failure table = exactly 16 data rows (header + separator excluded; awk count = 16). YAML header comment L4 "Five top-level keys mirror the five evidence layers … plus a confidence_rule mirror" is precisely worded (5 layer keys + 1 mirror = 6 keys, correctly disambiguated). `chapter_count: 17` L173 is an illustrative narnia example value, not a count-of-layers/modes claim — no collision. No prose states a divergent number. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | boundary-rules.yaml L72 | Comment says "The AUTHORITATIVE copy lives in SKILL.md **§B6**", but SKILL.md uses named-stage headers, not a `§B`/`§B6` numbering scheme — the closest anchor is `### Confidence rule (load-bearing)` (SKILL.md L72). "§B6" is the blueprint's internal section id (blueprint §2 item 6, §E note L330), so the mirror is faithful to its authoring source, but the cross-reference does not resolve to any literal `§B6` string in the shipped SKILL.md. Non-blocking dangling reference; the substantive rule (≥2 signals / PROBABLE cap / UNCERTAIN triggers) is fully in sync. | Change the YAML comment to reference SKILL.md's `### Confidence rule (load-bearing)` section by name rather than "§B6" (or add a matching `§B6`-labelled anchor to SKILL.md). Cosmetic only. |

## Actions Taken
None — report-only (fix_authorization: false). The single MINOR finding is documented for the
orchestrator; it is a within-file cross-reference and is faithful to the blueprint's own §B6 id.

## Confidence Gate
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 5
  - Note: all substring/count checks were run through Bash (grep/awk/diff) rather than the standalone Grep tool; each Bash call mapped to a specific lens item (row-count, cross-reference, schema diff, failure-table diff, confidence-rule mirror). Tool calls (9) ≥ checklist items (6). No web research performed (all claims intra-file; no external URL/standard/API to verify).
- **Verbatim anchors confirmed by `diff`:** manifest v1 schema block SKILL.md↔spec = IDENTICAL; 16-row failure table SKILL.md↔spec = IDENTICAL.
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
- PASS the internal-consistency gate. The two output files are mutually consistent: the confidence
  rule, five evidence layers, manifest schema fields, mode naming, failure table, and all counts agree
  between SKILL.md and boundary-rules.yaml with no contradictions.
- Optionally address the single MINOR "§B6" dangling reference in a cosmetic cleanup pass (not gating).
- Note for other lenses (out of this lens's scope): the `file`↔`single-file` and `adopt`↔`adopt-existing`
  naming variance is *internally consistent* here but a reviewer on a naming-hygiene/UX lens may still want
  to confirm the operator-facing `--source-mode` token set aligns with the schema enum.

## QA Complete
