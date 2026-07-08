# QA Report — Post-Completion Evidence-Quality Lens

**Topic:** laf-adaptation/ hybrid build — evidence-quality audit across all 4 phases
**Date:** 2026-07-04
**Phase:** report-validation (evidence-quality lens)
**Fix cycle:** N/A (fix_authorization: FALSE — REPORT ONLY)
**Stance:** ADVERSARIAL — assume >=10 evidence-quality errors exist; verify by reading + recomputing.

---

## Scope

- `/config/workspace/Infantalizer/laf-adaptation/` (full tree)
- Specs: `/config/workspace/Infantalizer/.dev/releases/current/0.1/design/`
- Port-source: `/config/workspace/Infantalizer/config/`

## Checks

1. Spec-derived claims cite real spec lines (native/build-new bodies).
2. Carried-verbatim files byte-faithful to port-source (sha256/cmp).
3. VENDOR.md boundary hashes computed, not hand-authored (recompute 3 adopted files).
4. No fabricated paths/SHAs/examples; children.md worked examples trace byte-faithfully.

_Findings appended incrementally below._

---

## Check 2 — Carried-verbatim byte-faithfulness (sha256/cmp)

| File | Port-source | Result |
|------|-------------|--------|
| kb/tiers/tier_1.yaml | config/age_profiles/tier_1_preschool.yaml | IDENTICAL (cmp) |
| kb/tiers/tier_2.yaml | config/age_profiles/tier_2_early_elementary.yaml | IDENTICAL (cmp) |
| kb/tiers/tier_3.yaml | config/age_profiles/tier_3_middle_elementary.yaml | IDENTICAL (cmp) |
| kb/tiers/tier_5.yaml | config/age_profiles/tier_5_young_adult.yaml | IDENTICAL (cmp) |
| kb/adaptation-mapping/universal-mappings.yaml | config/concept_mapping/universal_mappings.yaml | IDENTICAL (cmp) |
| kb/adaptation-mapping/tolkien-mapping.yaml | config/concept_mapping/templates/tolkien_mapping.yaml | IDENTICAL (cmp) |
| resources/thematic.md fenced payload (md L4-93) | config/transformation_rules/thematic.yaml | IDENTICAL (cmp) |
| resources/character.md fenced payload (md L4-80) | config/transformation_rules/character.yaml | IDENTICAL (cmp) |
| resources/agency.md fenced payload (md L10-24) | config/transformation_rules/thematic.yaml §agency_externalization (L33-47) | IDENTICAL, 512B=512B (cmp) |

**Result: PASS.** All 9 carried-verbatim payloads byte-faithful. The agency.md self-citation ("carried
VERBATIM from `config/transformation_rules/thematic.yaml`'s `agency_externalization` section, byte-identical")
is TRUE and correctly names its true source (NOT a nonexistent `agency.yaml`).

**Note (not a defect):** `templates/work-mapping-template.yaml` was named in the spawn prompt as a
carried-verbatim target, but it has **no** port-source in `config/` — it is NATIVE-authored per
CLAUDE.md §4 ("templates/ — NATIVE (carried verbatim)" is a loose label; there is no upstream file to
byte-compare). This is consistent with VENDOR.md (templates are not manifested/hash-pinned). No fabricated
source-claim is made inside the template file itself, so this is not an evidence-quality error — just a
scope note that the byte-compare is inapplicable (no source exists).

## Check 3 — VENDOR.md boundary hashes computed (recompute 3 adopted)

| File | VENDOR laf_sha256 | Recomputed sha256 | Match |
|------|-------------------|-------------------|-------|
| agents/editor.md | 2645f358…82410e3 | 2645f358…82410e3 | YES |
| agents/critic.md | 9a0078e9…026ec21b | 9a0078e9…026ec21b | YES |
| agents/writer.md (ADOPTED-PATCHED) | c1b3e12f…9e52e09534 | c1b3e12f…9e52e09534 | YES |

**Result: PASS.** All 3 spot-checked laf_sha256 values are the real sha256 of the file bytes — computed,
not hand-authored/fabricated.

## Check 4 — No fabricated paths/SHAs/examples; children.md worked examples byte-faithful

**Source location correction (not a defect):** children.md cites `prompts/transformation/tier_1_transform.md`
and `tier_3_transform.md`. These live at the **repo root** (`/config/workspace/Infantalizer/prompts/transformation/`),
NOT under `config/`. children.md's paths are relative-from-repo-root and correct; both files exist.

children.md is explicitly self-labeled *"Authored craft guidance (not a verbatim carry)"* (L3), so the
evidence standard is that its **worked examples** trace faithfully to the cited prompts.

| Example | children.md | Source prompt | Byte-faithful? |
|---------|-------------|---------------|----------------|
| Éowyn T1 (Source line) | L35 | tier_1_transform.md L71 | YES — exact |
| Éowyn T1 (Tier 1 rendering) | L36-37 | tier_1_transform.md L73 | YES — exact |
| Denethor T1 (Tier 1 rendering) | L68-69 | tier_3_transform.md L61 | YES — exact |
| Denethor T3 (Tier 3 rendering) | L70-73 | tier_3_transform.md L63 | YES — exact |

Cross-check of quantitative carries: T1 ceilings in children.md L44-45 (12 words/sentence, 1 clause, no
passive, ~800-word) match tier_1_transform.md L54-57 exactly; T3 params L63 (grade 3-5, 20 words/sentence,
~2,500-word) match tier_3_transform.md L54-56 exactly.

**Result: PASS.** Both named worked examples are byte-faithful to the transform prompts; no fabricated
example, path, or SHA found in Checks 2-4.

## Check 1 — Spec-derived claims cite real spec lines (native/build-new bodies)

Every spec-citation in the native/build-new bodies was resolved to the actual spec section and the section
was read to confirm it says what the body claims. All anchors verified to EXIST and MATCH.

| Body | Cited anchor | Anchor exists? | Body faithful to anchor? |
|------|-------------|----------------|--------------------------|
| adaptation-tiers/SKILL.md | skill-specs §1 (body outline) | YES (L33) | YES — tier table, loading, ladder, interpolation all realize §1 (L50-77); frontmatter byte-matches |
| source-fidelity/SKILL.md | skill-specs §3 (5-phase + §3.2 schema) | YES (L164/214) | YES — Phase 0-4 + output schema byte-match §3.1/§3.2 |
| chronicler.md | agent-schemas §5.1 + kb-formats §4 | YES (L213/188) | YES — frontmatter/inputs/invariants match §5.1; the extra `analysis.yaml` write target is grounded in kb-formats §4.4 (cited), not fabricated |
| tier-coordinator.md | tier-coordinator.md §3 (reconcile) | YES (L67) | YES — Checks A/B/C pseudocode + conflict types + maturity() byte-match §3 |
| adaptation-safety/SKILL.md | safety-rubric §1-§4 | YES (L19/62/74/91) | YES — Sections 1-6, auto-fails, aggregation, verdict contract all byte-faithful to §1-§4 |
| analyst.md | skill-specs §3.2 | YES (L214) | YES — output-contract fields match; self-labeled "build-time provenance pointer" |
| safety-verifier.md | safety-rubric §4 | YES (L91) | YES — verdict block matches §4 contract |
| agency.md | skill-specs §2.3 | YES (L143) | YES — "bolting onto adopted skill breaks boundary contract" is verbatim in §2.3 (L157-158) |
| thematic.md | kb-formats §2.3 | YES (L107) | YES — §2.3 declares thematic.md "canonical for rule application" |
| adaptation-rules/SKILL.md | kb-formats §2.2 (schema drift) | YES (L91) | YES — drift confirmed present in tier YAMLs |

**Schema-drift cross-check (adversarial):** The key-tolerant read claim in tier-coordinator.md L119-126
("`death_euphemism`|`death_handling`, `conflict_to_cooperation`|`conflict_handling`") was independently
verified against the tier YAMLs: T1/T2/T3 use `conflict_to_cooperation`+`death_euphemism`; T5 uses
`conflict_handling`+`death_handling`. The claimed drift is REAL, not invented. `thresholds.violence` and
`thresholds.moral_ambiguity` (grounding `maturity()`) exist in all four tier profiles.

**Cross-reference integrity (adversarial):** adaptation-safety/SKILL.md L78-85 claims safety-verifier.md
carries a matching "Deterministic `next` rule." Verified: safety-verifier.md L79-83 contains that exact
rule (`next = revise` iff `mode == blocking AND result == FAIL`). The two files genuinely agree — the
apparent shorthand/rule tension is explicitly and correctly reconciled, not a silent contradiction.

**Result: PASS.** No spec-derived claim cites a nonexistent line; no citation misrepresents its source.

---

## Confidence Gate

Checklist items (the 4 assigned evidence-quality checks + the sub-verifications each required):

- [x] Check 1 — spec citations real & faithful (10 body→anchor pairs read + 2 adversarial cross-checks) — VERIFIED
- [x] Check 2 — 9 carried-verbatim payloads byte-faithful (cmp) — VERIFIED
- [x] Check 3 — 3 VENDOR laf_sha256 recomputed & matched (sha256sum) — VERIFIED
- [x] Check 4 — 4 worked-example lines + 2 quantitative carries byte-faithful (Read cross-compare) — VERIFIED

- **Confidence:** "Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 9 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 11"
  (No web research performed — all claims were local/spec-bound; Tavily not required.)
- No UNCHECKED items. No UNVERIFIABLE items.

Note: tool-call count (20) exceeds the 4 top-level checks; each check was decomposed into per-file
tool-backed verifications (cmp/sha256/Read of specific spec sections), so engagement is real, not padding.

---

## Overall Verdict: PASS

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Evidence-quality errors found: **0** (adversarial target was >=10; none substantiated on recompute)
- Issues fixed in-place: N/A (fix_authorization: FALSE — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None substantiated. See "Adversarial notes" for two scope clarifications that are NOT defects. | — |

## Adversarial notes (investigated, found NOT to be evidence-quality errors)
1. **`templates/work-mapping-template.yaml` has no `config/` port-source.** The spawn prompt listed it as
   a carried-verbatim target, but there is no upstream file to byte-compare — it is NATIVE-authored per
   CLAUDE.md §4 and not manifested/hash-pinned in VENDOR.md. The template makes no false source-claim
   inside itself, so no fabrication exists. Byte-compare is simply inapplicable (no source).
2. **children.md `prompts/transformation/*` paths resolve to repo ROOT, not `config/`.** The paths are
   correct relative-from-repo-root and both files exist; the worked examples are byte-faithful. Not an
   error — just a location worth noting for a reader who assumed `config/`.

## Recommendations
- None blocking. The laf-adaptation tree passes the evidence-quality lens: every spec-derived claim is
  anchored to a real, matching spec line; every carried-verbatim payload is byte-faithful to its
  port-source; every spot-checked VENDOR hash is computed (not hand-authored); and both children.md worked
  examples trace byte-faithfully to their transform prompts. No fabricated path, SHA, or example found.

## QA Complete

