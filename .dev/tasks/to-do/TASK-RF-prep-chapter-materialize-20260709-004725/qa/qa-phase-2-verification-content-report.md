# QA Report — Phase 2 Verification (Actionability Lens Re-run)

**Topic:** chapter-materialize Stage-0 skill — actionability fix verification
**Date:** 2026-07-09
**Phase:** task-qualitative (fix-cycle re-verification, actionability lens)
**Fix cycle:** verification of cycle-1 fixes (7 findings)
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS

All 7 previously-FAILing findings (I-1..I-4, M-1..M-4) are now executable-by-a-model.
No DO-NOT-TOUCH frozen content was altered. A fresh adversarial actionability sweep
surfaced no NEW vagueness introduced by the fixes.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| I-1 | Mode-C "validates" testable | none | PASS | SKILL.md L46-49: `validates` = canonical `ch-<NN>.txt` name (zero-padded, contiguous ordinals from 01, no gaps) + non-empty + `order==numeric id`. Model can enumerate `ch-*.txt`, regex-match, check contiguity/non-empty/order. Fall-through to folder/ambiguity is a finite ordered list — no loop. Decidable. |
| I-2 | "non-canonical" decidable predicate | none | PASS | SKILL.md L50-53: non-canonical = per-chapter file whose name does NOT match `source/<slug>/ch-<NN>.txt`. Regex-decidable; correctly distinguishes Mode A (needs materialization) from adopted Mode C set. |
| I-3 | CERTAIN "no contradiction" operationalized, bolded sentence unaltered | none | PASS | SKILL.md L82 bolded sentence byte-verbatim (`grep 'CERTAIN requires'`). Adjacent non-bolded op-line L82-85: contradiction = signals disagree on boundary offset / count (TOC vs body-heading vs filename) / titles-ordinals; any contradiction caps at UNCERTAIN regardless of signal count. Comparison is post-normalization (yaml Layer 2 captures roman/arabic/spelled → common ordinal), so spelled-vs-roman of same ordinal is not falsely flagged. Consistent with failure-table L156. |
| I-4 | PDF mechanism named, no-runtime consistent | none | PASS | SKILL.md L114-118: PDF text via model's native PDF-read; NO extraction script (ADR-006); garble (broken words, ligatures, repeated page headers) → UNCERTAIN + blocks greenlight. Real PDF exists (`Books/LWW/...Wardrobe.pdf`, 589651 bytes). Consistent with failure-table PDF row L159 (same detection column, same resolution). Executable: the executing model reads PDFs natively via multimodal input. |
| M-1 | boundary-rules.yaml cross-ref points at real SKILL.md heading | none | PASS | yaml L77 references `### Confidence rule (load-bearing)`; that heading exists at SKILL.md L80 (`grep '^#'`). No `§B6` anywhere (`grep B6` → none). Remaining `spec §6.x`/`§7` refs are build-time provenance per SKILL.md L227-229 + CLAUDE.md, out of M-1 scope. |
| M-2 | deterministic duplicate-monolith tie-break | none | PASS | SKILL.md L138-141: byte-identical (same sha256) → shortest filename, tie-broken lexicographic → un-suffixed base wins. Verified against real data: 5 large monoliths all sha256 `8d2cf54...`; base `...Lewis.html` is shortest → wins deterministically. Two distinct files can't share a name → lexicographic tie always resolves. Fully deterministic. |
| M-3 | provisional-role note | none | PASS | SKILL.md L36-39: `raw_sources[].role` is PROVISIONAL, finalized after Stage 0.3 evidence pass (front_matter↔chapter_file can flip). Resolves the 0.1-before-0.3 ordering concern. |
| M-4 | ignore_globs HINT-only clarification | none | PASS | yaml L51-54: ignore_globs is a HINT; byte-identical BASE monolith without "copy" token is de-duped by sha256 tie-break (points at real SKILL.md "Duplicate-monolith canonical pick" bullet L138), NOT glob. Verified real: base `...Lewis.html` (no copy token) is byte-identical to `copy*.html` → glob can't catch it → hash rule is the load-bearing resolver. Cross-ref target exists. |
| S1 | frozen content unaltered | none | PASS | Confidence bolded sentence L82 verbatim; deferred-write bolded sentence L95 verbatim; manifest v1 schema block L176 present; 16-row failure table intact (16 data rows). New bold on I-1 `validates` def is a newly-added clause, not a frozen sentence — permitted. |
| S2 | fresh adversarial sweep for NEW vagueness | none | PASS | Probed: I-1 fall-through loop risk (none — finite ordered precedence); M-2 equal-length-name tie (lexicographic resolves; distinct files never equal); M-2↔M-4 circularity (hash groups first via 0.1 step-1 sha256, then shortest-name within group — non-circular); I-3 title-case false positive (post-normalization ordinal compare avoids it); I-4 "garble" concreteness (exemplified, matches failure-table detection column). No new undecidable predicate. |

<!-- task-qualitative phase; all rows PASS → axis = none (five-axis lens applied, nothing fired). AX-1 Drift active: BUILD_REQUEST.GOAL surrogate = consolidated-findings fix directives, captured verbatim from qa-phase-2-consolidated-findings.md. -->

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
None. All 7 findings remediated; no new actionability gaps.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | (no remaining or new gaps) | — |

## Actions Taken
None (report-only; fix_authorization: false).

## Self-Audit
**(a) Reliance list — rf-qa structural PASS items skipped for structural re-check:**
- Relied on prior structural PASS (template-conformance, internal-consistency, evidence+completeness, domain-accuracy — the 5 non-actionability lenses). Did not re-run structural section-numbering/template checks.

**(b) Independent semantic checks (≥1 required, INV-019):**
- I-4 PDF mechanism verified against real filesystem: `find Books/LWW -iname '*.pdf'` confirmed a real 589651-byte PDF exists, so the mechanism clause is grounded in an actual input, not hypothetical — tool: Bash `find`/`ls`.
- M-2/M-4 byte-identity claim independently verified: `sha256sum` on the 5 large monoliths returned identical hash `8d2cf54...`, proving the base-monolith-without-copy-token de-dup scenario is real and the glob-alone approach genuinely fails — tool: Bash `sha256sum`. This is the load-bearing check rf-qa's structural PASS could not reach (it verifies the fix text exists; only running sha256 proves the fix resolves a real duplicate group).
- M-1 dangling-anchor resolution verified by grepping SKILL.md headings (`grep '^#'`) and confirming `### Confidence rule (load-bearing)` at L80 is the exact string the yaml L77 now cites — tool: Bash `grep`.

## Self-Audit answers
1. Factual claims independently verified against source: 12+ (5 heading anchors, 5 file sha256 identities, 1 real PDF existence, failure-table row count, both frozen bolded sentences byte-check, both cross-file heading-reference resolutions).
2. Files read: `qa-phase-2-consolidated-findings.md`, `SKILL.md` (full + targeted re-reads L41-60), `resources/boundary-rules.yaml` (full), plus filesystem grounding via `ls`/`find`/`sha256sum`/`grep` on `Books/LWW/` and `scripts/`.
3. Trust basis for the PASS: I did not accept "the fix text is present" as sufficient. For every finding I traced the fix to a decidable predicate a model could execute, and for M-2/M-4/I-4 I verified the *real-world scenario the fix must resolve* exists (byte-identical monoliths via sha256, a real PDF). I ran an explicit adversarial sweep (S2) hunting for new vagueness and found none — the PASS is evidence-backed, not benefit-of-the-doubt.
4. Web research: none required (all verification was local-file / filesystem bound). Tavily not invoked; no fallback occurred.

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 4 | Grep: 6 | Glob/find: 1 | Bash(sha256/ls): 3

## Recommendations
- Green light to proceed. The actionability gate now PASSES; all 7 findings are executable-by-a-model and no frozen content was disturbed.

## QA Complete
