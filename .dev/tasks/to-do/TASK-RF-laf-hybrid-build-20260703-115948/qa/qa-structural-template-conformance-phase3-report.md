# QA Report — TEMPLATE-CONFORMANCE (Phase-3 runtime artifacts)

**Topic:** LAF hybrid build — Phase-3 runtime artifact template conformance (Tolkien ch-01, tiers 1/3/5)
**Date:** 2026-07-04
**Phase:** report-validation (structural / template-conformance lens)
**Fix cycle:** N/A (fix_authorization: FALSE — REPORT ONLY)
**Lens:** Adversarial / zero-trust. Hypothesized ≥5 errors (malformed verdict block, missing continuity section, schema-violating analysis.yaml).

---

## Overall Verdict: PASS (with 3 MINOR advisory findings — none blocking)

The four structural conformance checks all pass against their governing specs. The adversarially
hypothesized defects (malformed verdict block, missing continuity section, schema-violating analysis.yaml)
were **searched for and NOT found** — the verdict block is well-formed and complete, every continuity.md
carries all required sections, and both analysis.yaml copies conform to the skill-specs §3.2 schema and
parse as valid YAML. The 3 findings below are genuine but MINOR (a filename/path assertion nuance, a
degraded-tolerance observation, and a documentation-cross-reference note); none is a template-conformance
failure.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | analysis.yaml conforms to skill-specs §3.2 schema + carries CERTAIN/PROBABLE/UNCERTAIN tags | PASS | `python3 yaml.safe_load` on both copies → top-keys exactly `[status, metadata, essentials, characters, events, summary, transformation_flags, uncertainties]` (all 8 §3.2 keys present, none extra). metadata sub-keys `{work, chapter, source_access, confidence}` all present (analysis.yaml:4-8). essentials has title/chapter_title/opening_sentence/closing_sentence each `{value, confidence}` (:9-13). characters list carries per-item confidence (:14-19); events carry `{seq, event, confidence}` (:20-28); summary `{text, confidence}` (:29-31); transformation_flags has violence/death/emotional/abstract each `{instances, severity}` (:32-36); uncertainties is a non-empty list (:37-39). Tag vocabulary: `grep -oE "confidence: (CERTAIN\|PROBABLE\|UNCERTAIN)"` → 16 CERTAIN + 3 PROBABLE, all from the closed §3.1 vocabulary. `status: OK`, `source_access: FULL` → ABORT gate correctly NOT tripped. Promoted tier-1 copy is byte-`diff`-IDENTICAL to `work/analysis/ch-01.yaml` (kb-formats §4.4 "copy of work/analysis" satisfied); tier-3 and tier-5 copies also present (3960 bytes each, same size). |
| 2 | Safety report ends in §4 machine-parseable verdict block, well-formed YAML | PASS | `re.findall` extracted exactly 1 `yaml` fence (the verdict); `yaml.safe_load` parsed it clean. `verdict` sub-keys = `{work, chapter, tier, result, sections, automatic_failures, mode, next, evidence}` — **zero missing** vs §4 contract. `sections` has all 6 required rollups (`forbidden_content, agency_externalization, emotional_safety, safe_home, nightmare_prevention, linguistic`) — count=6, none missing. `mode: blocking` (correct for T1 per rubric §Gate T1-2 blocking), `next: promote` (consistent with `result: PASS` per §3 aggregation logic). `automatic_failures: []` and `evidence: []` are well-formed empty lists. `tail` confirms the fenced block is the LAST content in the file (§4 "It **ends** with this fenced block"). |
| 3 | Cross-tier report matches tier-coordinator §4 format | PASS | All 8 §4 structural elements present via grep: title line, `tiers: [1, 3, 5]  mode: parallel  source: work/analysis/ch-01.yaml` header (:3), "Shared source anchors" section, "Per-tier renderings (traceability)" table, Checks "A source-fidelity / B disclosure-leak / C monotonicity" (:28-35), `status: RECONCILED` (:37), `conflicts: []` (:38). Filename `ch-01-cross-tier.md` matches §1/§4 pattern `work/analysis/ch-<NN>-cross-tier.md`. Per-tier table has T1/T3/T5 columns + shared-anchor column (:18-25); every row's shared-anchor traces to a fact in analysis.yaml (spot-checked Sauron→characters[Sauron], Théoden fall→events[king struck down]). |
| 4 | Each continuity.md + canon-delta.md present and coherent | PASS | All 3 continuity.md present (tier-1/3/5) each with the §4.1 required sections: title header + "what a Tier-N reader knows" gloss + a running "Known so far (after ch-01)" character/fact list + the Inv.2/Inv.3 traceability footer citing source names. All 3 canon-delta.md present each with §4.3 sections (New / Changed / Carried-forward-or-Superseded + traceability footer). Cross-file coherence: T1 continuity renders Théoden as "grew very tired and sat down to rest" (:12-13) which MATCHES the cross-tier Check-B claim that T1 defers the death as "tired/rest"; T3 continuity states Théoden "**died**" (:12-13) and T5 "was struck… he fell" (:12) — monotonic non-decreasing maturity T1<T3≤T5, consistent with cross-tier Check C. No missing or malformed section detected in any of the 6 files. |

### Supplementary adversarial cross-checks (beyond the 4 required checks)

| Sub-check | Result | Evidence |
|-----------|--------|----------|
| T1 safety-report Section 1 (0 forbidden hits) vs actual draft | HONEST | `grep -niwE` for all 17 T1 forbidden tokens against `work/drafts/ch-01-t1-v2.md` → **0 hits**. Report claim verified, not taken on faith. |
| T1 safety-report Section 6 (max 9 words/sentence ≤ 12) vs actual draft | HONEST | Python sentence-tokenizer over the v2 draft body → true max = **9 words** ("She spoke gently and kindly to the Grumpy Rider."). Report's "max 9" is exact, not rounded/optimistic. |
| Referenced upstream inputs exist | PASS | `source/tolkien/ch-01.txt` exists (analysis header claim). All drafts referenced by safety reports exist (`ch-01-t1-v1/v2`, `ch-01-t3-v1`, `ch-01-t5-v1`). |
| Verdict aggregation self-consistency | PASS | All 6 sections PASS + `automatic_failures: []` ⇒ `result: PASS` ⇒ `next: promote` — matches safety-rubric §3 logic exactly. T3 report independently correct: `mode: advisory`, `next: promote` (advisory always promotes per §3). |

---

## Summary
- Checks passed: 4 / 4 required (+ 4/4 supplementary adversarial cross-checks)
- Checks failed: 0
- Critical issues: 0
- MINOR advisory findings: 3
- Issues fixed in-place: 0 (fix_authorization: FALSE — report only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `work/analysis/ch-01-cross-tier.md:3` (header) vs skill-specs §3.2 / kb-formats §4.4 | The cross-tier header cites `source: work/analysis/ch-01.yaml` (correct per tier-coordinator §1, whose `shared_analysis` input IS the work/ path). No defect in the report itself — but note the promoted per-tier copies at `tier-<N>/chapters/ch-01/analysis.yaml` are byte-identical to it (verified via diff), so the shared-source single-truth invariant holds. Flagged only because an adversarial reader could misread "source" as pointing at a per-tier copy. | None required; optionally annotate that `work/analysis/ch-01.yaml` is the tier-invariant truth and the tier-N copies are promoted duplicates. |
| 2 | MINOR | `work/analysis/ch-01.yaml` uncertainties + tag distribution | The analysis uses only CERTAIN/PROBABLE — **no UNCERTAIN tag appears** (0 occurrences). This is schema-VALID (UNCERTAIN is permitted-not-required, and `source_access: FULL` justifies high certainty), but the `uncertainties:` list (:37-39) contains 2 genuine unknowns (inferred title; whether the king dies vs is unhorsed). Consistency note: the "king dies?" uncertainty (:39) is surfaced but the corresponding `essentials`/`events` entries are still tagged CERTAIN — defensible (the *event text* "he fell" is certain; only the *interpretation* is uncertain), but an adversarial reviewer should confirm this is intentional, not a mis-tag. | None required (defensible). Optionally add an inline note that the death-vs-unhorsing ambiguity is deliberately deferred to per-tier death-handling rather than resolved at analysis time. |
| 3 | MINOR | `work/safety-reports/ch-01-t1.md:4` vs safety-rubric §4 verdict `mode` enum | Report header prose says "**MANDATORY + blocking**"; the verdict block correctly emits `mode: blocking` (the §4 enum is `blocking\|advisory\|skipped` — "MANDATORY" is not an enum value but appears only in prose, not the machine block, so no parse impact). Purely cosmetic prose/enum divergence. | None required; the machine-parseable block is spec-correct. Optionally drop "MANDATORY" from prose to avoid enum confusion. |

## Actions Taken
None. fix_authorization: FALSE — this is a report-only pass. All findings documented above without modification to any artifact.

## Recommendations
- **Green light to proceed.** All four template-conformance checks PASS with tool-verified evidence; the machine-parseable verdict block, all continuity/canon-delta sections, both analysis.yaml schema copies, and the cross-tier report format are conformant.
- The 3 MINOR findings are advisory documentation nuances, not conformance failures. None blocks promotion.
- Adversarial note honored: the hypothesized ≥5 errors (malformed verdict / missing continuity section / schema-violating analysis.yaml) were actively searched for with dedicated tool calls and are **absent**. The clean result is backed by 12 tool invocations mapping to specific checks (see Confidence block), not by assumption.

---

## Confidence Gate

- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: (bundled in Bash) | Glob: 0 | Bash: 4
  - Read: 4 specs (skill-specs, safety-rubric, tier-coordinator, kb-formats) + 7 artifacts (2× analysis.yaml, ch-01-t1 report, cross-tier report, 3× continuity.md, ch-01 canon-delta) — 11 distinct Read targets, plus 3 more artifacts read in the second batch (t3/t5 canon-delta, t3 report).
  - Bash: 4 batches performing dir inventory, YAML `safe_load` validation + `diff`, verdict-block extraction/parse, tier-coordinator format grep, tag-coverage grep, forbidden-token scan, and sentence-length tokenizer.
  - Tool calls (≈14 Read + 4 Bash-batches, each Bash running multiple greps/python checks) exceed the 4 required checklist items — engagement minimum satisfied, no padding (each call maps to a named check in the Items Reviewed / supplementary tables).
- No web research performed (all claims are local source-truth; no external URL/standard/API to verify). Tavily-first rule not triggered.
- Every checklist item marked [x] VERIFIED with cited tool output. UNCHECKED: none. UNVERIFIABLE: none.

## QA Complete


