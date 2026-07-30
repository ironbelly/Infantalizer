# QA Report — phase-gate content (Phase 2), LENS: actionability

**Topic:** chapter-materialize SKILL.md + resources/boundary-rules.yaml
**Date:** 2026-07-09
**Phase:** doc-qualitative (phase-gate content, actionability lens)
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Overall Verdict: FAIL

Adversarial stance held: assumed ≥5 errors within the actionability lens and found them.
The procedure is largely well-structured and executable, but several concrete
decision points a model would hit at runtime are under-specified or point at
dangling references. None of the six lens checks passes clean.

## Items Reviewed
| # | Check (actionability) | Result | Evidence |
|---|-----------------------|--------|----------|
| 1 | Each Stage 0.1–0.5 gives concrete ordered actions; 0.1 runs source-access ABORT first; 0.2 tie-break → HALT-ask | FAIL | Stage 0.1 (SKILL:26-37) ordering + ABORT-on-NO-ACCESS verified; source-fidelity access levels FULL/PARTIAL/MEMORY-BASED/NO-ACCESS confirmed (source-fidelity/SKILL.md:23-35). Stage 0.2 precedence + ambiguity→HALT verified. BUT: "adopt … and validates" (SKILL:44) has no testable "validates" criterion; "≥2 non-canonical per-chapter files" (SKILL:45) never defines "non-canonical" as a decidable test. See F1, F2. |
| 2 | Confidence rule testable (CERTAIN=≥2 agreeing signals; single→PROBABLE) — deterministic | FAIL | Rule text (SKILL:72-78) + YAML mirror (boundary-rules.yaml:74-77) verified deterministic for the signal-count clause. BUT "no contradiction" is not operationalized, and the authoritative-copy pointer is dangling. See F3, F4. |
| 3 | Deferred-write invariant actionable (WHICH defers, WHEN commits) | PASS | SKILL:80-98: CERTAIN commit immediately; PROBABLE/UNCERTAIN/collision/mode-ambiguity → ambiguous_splits[], write deferred; commit on greenlight-confirm by prep-cordinator. Concrete and unambiguous. |
| 4 | Gate routing (Stage 0.5) names concrete real artifacts, no invented machinery | PASS | SKILL:92-98 routes to existing §5 question gate, greenlight, `70-traceability.md` `[skip]→DEFAULTED`. Verified against prep/SKILL.md: §5 gate (line 76-85), greenlight `50-greenlight.md` (line 89), `70-traceability.md` `[skip]→DEFAULTED` (line 84). No invented gates. |
| 5 | Normalization rules specific (HTML strip set; PDF rejoin; UTF-8; NO reword) | FAIL | HTML/UTF-8/no-reword rules concrete (SKILL:100-112). BUT PDF "extract the text stream" (SKILL:103) is not executable under the no-runtime/no-script invariant — no method given for how a model performs the extraction. See F5. |
| 6 | No aspirational/vague verbs without concrete criteria | PASS | grep for "handle appropriately / process as needed / as appropriate / reasonable / properly / etc." → zero hits. Verbs are concrete throughout. |

## Summary
- Checks passed: 3 / 6
- Checks failed: 3
- Critical issues: 0
- Important issues: 3
- Minor issues: 3
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | SKILL.md:44 (Stage 0.2 precedence #1) | Mode-C adopt fires when `source/<slug>/ch-*.txt` "exists **and validates**", but "validates" is never defined. A model cannot deterministically decide whether an existing set validates. The idempotency section (SKILL:116-119) describes what adopt *does* (read titles/ordinals; CERTAIN-for-existence; flag provenance gaps) but not the pass/fail test that gates entry into Mode C vs falling through to re-split. | Define the "validates" test concretely, e.g.: "validates = every file matches `ch-<NN>.txt` (zero-padded, contiguous 01..N, no gaps), each is non-empty (≥ `min_body_chars`), and the count is self-consistent. If any check fails, do NOT adopt; fall through and gate the discrepancy." Cross-link to the `content_sanity` floor in boundary-rules.yaml:59-63. |
| F2 | IMPORTANT | SKILL.md:45 (Stage 0.2 precedence #2) | Mode A requires "≥2 **non-canonical** per-chapter files", but "non-canonical" is not a testable predicate in the SKILL body. The distinction (a file already matching `ch-<NN>.txt` is canonical; anything else is non-canonical) lives implicitly in boundary-rules.yaml:50 (`canonical_output_pattern`) but is never surfaced as the decision rule a model applies at 0.2. Without it, a model cannot deterministically distinguish Mode A from Mode C when a directory holds mixed names. | State the predicate inline at 0.2: "non-canonical = does NOT already match `ch-<NN>.txt`. A directory of ≥2 files that already match `ch-<NN>.txt` is Mode C (adopt), not Mode A." Reference boundary-rules.yaml:50. |
| F3 | IMPORTANT | SKILL.md:74 + boundary-rules.yaml:74-77 (confidence rule) | The CERTAIN rule is "≥2 independent agreeing signals **AND no contradiction**", but "no contradiction" is not operationalized anywhere. A model can count agreeing signals deterministically, but cannot deterministically decide what constitutes a disqualifying contradiction (e.g., does a TOC count of 17 vs 4 filenames contradict? does one out-of-order heading contradict?). Layer 5 count_reconciliation (`all_present_counts_must_agree_else_gate`) partially covers the count case but is not wired into the CERTAIN "no contradiction" clause as the operational test. | Enumerate the contradiction predicates that block CERTAIN, e.g.: "A contradiction exists when (a) present signal counts disagree (Layer 5), OR (b) an ordinal appears in one signal but is absent/duplicated in another, OR (c) heading order ≠ filename order (Layer 3). Any contradiction caps the boundary at UNCERTAIN regardless of agreeing-signal count." |
| F4 | MINOR | boundary-rules.yaml:72 | Dangling cross-reference: the YAML mirror points the authoritative confidence rule to "SKILL.md **§B6**", but SKILL.md has no `§B6` anchor (its heading is `### Confidence rule (load-bearing)` under `## Stage 0.3`; grep confirms no `B6` string in SKILL.md). A model told "SKILL.md wins on drift" cannot resolve §B6. The quoted heading text saves it, but the pointer itself is wrong. | Change "SKILL.md §B6" to the real anchor: "SKILL.md → Stage 0.3 → 'Confidence rule (load-bearing)'". |
| F5 | IMPORTANT | SKILL.md:103 (PDF normalization) | "PDF → **extract the text stream**, rejoin hyphenated wraps" is not executable under the skill's own hard invariant (SKILL:16-24, "adds no script, parser binary, or CLI; the model executes this inline"). A model cannot "extract a PDF text stream" from a binary PDF by inline reasoning, and no tool/mechanism is named. The real driving folder `Books/LWW/` contains `The Lion The Witch And The Wardrobe.pdf` (589651 bytes) alongside the HTML — so this path is reachable, not hypothetical. Contrast HTML, which a model genuinely can strip inline. | Either (a) name the concrete mechanism (e.g., "read the PDF via the Read tool's PDF page support; if the extracted stream shows garble per the failure table, mark UNCERTAIN and gate for a cleaner source"), or (b) if inline PDF extraction is out of scope, say so explicitly and route PDF sources to HALT-ask ("PDF present → require an HTML/txt source or operator-supplied extraction"). As written it is an aspirational directive with no executable procedure. |
| F6 | MINOR | SKILL.md:143 + Stage 0.1 role assignment (SKILL:36-37) | When multiple monoliths are hash-identical, the failure table says "pick one canonical; others `ignored_duplicate`" but gives no deterministic tie-break for WHICH is canonical. Verified real case: 5 files in `Books/LWW/` are byte-identical (sha256 `8d2cf541…`): `…Lewis.html`, `…copy.html`, `…copy 2/3/5.html`. A model has no rule to pick deterministically, so two runs could pick different `raw_path` provenance. | Add a deterministic tie-break, e.g. "among hash-identical monoliths, canonical = the natural-sort-first filename (the un-suffixed `…Lewis.html` before any `copy` variant); all others → `ignored_duplicate`." This also makes re-run provenance stable (relevant to the idempotency hash-match no-op at SKILL:120). |
| F7 | MINOR | SKILL.md:36-37 (Stage 0.1 step 4) vs 0.2 | Stage 0.1 step 4 assigns each raw input a `role` ∈ `monolith \| chapter_file \| front_matter \| ignored_duplicate`, but gives no criteria for the assignment — the model must already know which HTML is a monolith vs a chapter_file vs front_matter before Layer 1-5 signal analysis runs in 0.3. This is a mild ordering/actionability gap: role tagging is asked for at 0.1 but the evidence to decide it is only produced at 0.3. | Clarify that 0.1 records a *provisional* role from cheap signals (size/extension/filename-glob per boundary-rules.yaml `ignore_globs`), and roles are finalized after 0.3 boundary analysis; or move definitive role assignment to after 0.3. |

## Actions Taken
None. `fix_authorization: false` — report-only. All findings documented above with specific locations and required fixes.

## Self-Audit (INV-019)

**Factual claims independently verified against source (with tool evidence):**
1. `check_boundary.py` exists and is the sole script — verified (`ls scripts/check_boundary.py`, 35360 bytes).
2. source-fidelity access-level vocabulary (FULL/PARTIAL/MEMORY-BASED/NO-ACCESS + ABORT + MEMORY→UNCERTAIN) — verified against `skills/source-fidelity/SKILL.md:23-35`. SKILL's Stage 0.1 claim (SKILL:31-33) matches exactly.
3. §5 question gate exists in prep skill — verified `skills/prep/SKILL.md:76-85`.
4. greenlight artifact `50-greenlight.md` — verified `skills/prep/SKILL.md:89`.
5. `70-traceability.md` + `[skip]→DEFAULTED` — verified `skills/prep/SKILL.md:84`.
6. §B6 anchor does NOT exist in SKILL.md — verified via `grep '^#'` (headings are Stage 0.1-0.5 + `### Confidence rule`; no B6 string) → grounds F4.
7. Real `Books/LWW/` inventory — verified via `ls`: 4 split `-1..-4.html`, 5 monoliths, 1 `.pdf` (589651 bytes) → grounds F5, F6.
8. 5 monoliths are byte-identical — verified via `sha256sum` (all `8d2cf541…`) → grounds F6.
9. Layer-3 ordinal pattern actually matches real `-1.html` naming — verified via `grep -oE` → confirms the split-file path is real (strengthens F5/F6 reachability).
10. No aspirational verbs — verified via targeted grep (zero hits) → grounds item-6 PASS.

**Files read to verify claims:** merged-requirements.md (driving spec); chapter-materialize/SKILL.md (full); chapter-materialize/resources/boundary-rules.yaml (full); prep/SKILL.md (§5-§8); source-fidelity/SKILL.md (Phase 0); laf-adaptation/CLAUDE.md (provenance/ADR-006 context); real `Books/LWW/` + `source/narnia|tolkien/` directories.

**Why trust this review found real issues:** every finding is anchored to a file:line in the target and, where the spec supplies a concrete driving case (`Books/LWW/`), cross-checked against the actual bytes on disk (hashes, the `.pdf`, the `-1..-4` naming). The three FAILs are decision points a model would provably stall or diverge on at execution time, not stylistic nits.

**Web research:** none performed — all verification was local-file-bound. Tavily-first policy therefore not triggered; no fallback used.

## Confidence Gate

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 8 | Glob: 0 | Bash: 6
- All 6 lens checks resolved to PASS/FAIL with tool evidence; none unchecked or unverifiable.
- Tool-engagement minimum satisfied (14 read/grep/glob-class + bash verifications ≥ 6 checklist items).

## Recommendations
Resolve all 7 findings before Phase-2 gate passes. Priority order:
1. F5 (PDF path is unexecutable under the no-runtime invariant — reachable in the real driving folder).
2. F1 + F2 (Mode C-vs-A / Mode A-entry predicates undefined — first branch a model hits).
3. F3 ("no contradiction" not operationalized — the load-bearing confidence gate).
4. F4, F6, F7 (dangling §B6 ref; monolith tie-break; provisional-role ordering).

Since fix_authorization is false, hand these to the author/executor for remediation, then re-run the actionability gate.

## QA Complete
