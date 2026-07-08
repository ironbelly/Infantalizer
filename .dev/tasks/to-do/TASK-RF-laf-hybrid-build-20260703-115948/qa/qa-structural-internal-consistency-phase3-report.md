# QA Report — Structural Internal-Consistency Lens (Phase 3)

**Topic:** laf-adaptation Phase-3 hybrid build — internal consistency of cross-tier renderings, chronicler keying, safety verdict rollups, hard-gate verdict propagation
**Date:** 2026-07-04
**Phase:** report-validation (INTERNAL-CONSISTENCY lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY

---

## Overall Verdict: FAIL

Internal-consistency defects found across all four check families. None are fabrications of fact (every rendering traces to a real source anchor and every gate-cond source verdict is genuinely PASS), but there is a cluster of **quotation-drift**, **keying-label**, and **scope-overstatement** inconsistencies where a rollup/summary artifact does not match its own source. Under zero-tolerance these are real internal-consistency failures. Fix authorization was FALSE — all findings are REPORT-ONLY.

---

## Confidence Gate

**Confidence:** Verified: 4/4 check-families | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 8 (each targeting a specific rendering/verdict/keying claim). No web research required (all claims are local-artifact-internal).

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cross-tier renderings trace to shared analysis anchors | FAIL (traces, but 3 quote/label defects) | Every T1/T3/T5 cell maps to a real fact in ch-01.yaml (semantic trace holds), BUT (a) T1 Théoden cell mis-quotes the rendering; (b) all 6 anchor-key labels are nominal, not the real YAML keys; (c) one anchor key names a nonexistent event. Bash diff of table cells vs adapted.md lines. |
| 2 | Chronicler per-tier writes consistently keyed; no cross-tier bleed; shared canon = source names only | PASS | grep: no T1 transformed name in kb/canon or kb/timeline; T3/T5 files contain no T1 tokens; T1 rendering body contains no source names (Sauron/Nazgûl appear ONLY as `(source: …)` provenance + mapping arrows in decisions.md — legitimate, not bleed); kb/canon/tolkien/ch-01.md holds only source names. |
| 3 | Safety verdict section rollups agree with overall result | PASS | ch-01-t1.md: all 6 sections PASS, result PASS, automatic_failures []. Independently re-verified: 0 forbidden tokens in v2 draft, max 9 words/sentence (≤12). Safety-checked draft body IDENTICAL to promoted kb adapted.md. |
| 4 | Hard-gate rollup verdicts match individual gate-cond source files | PASS (rollup), FAIL (evidence-string drift) | All 5 gate-cond*.md source files independently show ✅ PASS; hard-gate rolls all 5 as PASS — no PASS-in-rollup-that-isnt-PASS-in-source. Gate-cond1 "16 CERTAIN + 3 PROBABLE" independently confirmed by count. BUT hard-gate §"Tier differentiation" quotes a THIRD non-matching variant of the T1 Théoden rendering. |

## Summary
- Check families passed: 2 / 4 (Checks 2 and 3)
- Check families failed: 2 / 4 (Checks 1 and 4 — quotation/keying/scope drift, not verdict fabrication)
- Total distinct findings: 6
- Critical: 0 | Important: 3 | Minor: 3
- Issues fixed in-place: 0 (fix_authorization FALSE — REPORT ONLY)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `work/analysis/ch-01-cross-tier.md` line 22, T1 cell of "Théoden's fall" | Table quotes the T1 rendering as **"grew very tired and sat down to rest"**. The actual T1 `adapted.md` line 7 reads **"He grew very tired and sat right down."** The word "rest" is NOT in that sentence ("rest" appears only later, in a different sentence). The traceability quote does not match the rendering it claims to render. | Change the cell to the verbatim rendering `"grew very tired and sat right down"` (or mark it as paraphrase). |
| 2 | IMPORTANT | `reports/phase-3-hard-gate-report.md` line 27, "Tier differentiation proven" | Introduces a THIRD variant of the same T1 rendering: **"grew tired and rested"**. This matches neither the cross-tier table ("sat down to rest") NOR the actual adapted.md ("sat right down"). Three artifacts describing the same rendering, three different strings — an internal-consistency failure across the rollup chain. | Align the hard-gate summary string to the actual rendering `"grew very tired and sat right down"`, and reconcile with the cross-tier table (Finding 1). |
| 3 | MINOR | `work/analysis/ch-01-cross-tier.md` line 22, "shared anchor" column, `events[siege/clash]` | The anchor key `events[siege/clash]` names an event label that does not exist in `ch-01.yaml`. Actual `events[]` are keyed by numeric `seq:` (1–8); there is no single "siege/clash" event — the siege is `seq:1` and the clash is `seq:4`. The row still traces semantically, but the cited key is not resolvable. | Cite real keys, e.g. `events[seq:1,seq:4]`, or relabel the anchor column as "semantic anchor" to signal it is not a literal key lookup. |
| 4 | MINOR | `work/analysis/ch-01-cross-tier.md` "shared anchor" column (all 6 rows) | Anchor labels `characters[Sauron]`, `characters[Nazgûl]`, `characters[Denethor]`, `events[king struck down]`, `events[soldiers fall]` use short nominal keys. The real `characters[]` entries are keyed by full `name:` values (`"Sauron (the dark lord)"`, `"the Nazgûl (a rider of the host)"`, `"Denethor (the Steward)"`) and `events[]` by `seq:`. Keying is nominal/semantic, not literal — a reader cannot mechanically resolve these anchors against the YAML. | Normalize anchor keys to the actual YAML keys, or state explicitly that the column is a human-readable anchor, not a machine key. |
| 5 | MINOR | `reviews/gate-cond2-safety.md` vs hard-gate Condition 2 | Gate-cond2 scopes its PASS strictly to **T1** (`work/safety-reports/ch-01-t1.md`, `tier: 1`, blocking). A T3 safety report (`ch-01-t3.md`, ADVISORY, PASS) also exists but is not referenced by the gate. This is not a wrong verdict (T1 blocking PASS is the gate condition), but the gate rollup's "safety PASS" is narrower than a reader of the hard-gate might assume. Flagged for completeness: no over-claim, but the T3/T5 safety posture is undocumented in the gate chain. | Optional: note in gate-cond2 that T3 is advisory-PASS and T5 safety is N/A, so the scope of "safety PASS" is explicit. |
| 6 | MINOR | Cross-tier Check C, line 33-35 (`monotonicity`) vs tier YAML labels | Check C labels T1 as "`mandatory`-transform". The tier_1.yaml mechanism for death is `death_euphemism` (strategy `journey_or_sleep`); the "mandatory/optional/preserve" axis in tier_3.yaml/tier_5.yaml applies to `agency_externalization`/`conflict_to_cooperation`, not uniformly to "transform". The three-tier maturity ordering is correct in substance, but the single-word rule labels conflate distinct YAML keys. Verified against tier_1.yaml:75, tier_3.yaml:64, tier_5.yaml:59-62. | Optional: qualify which rule axis each label refers to (agency vs death vs conflict) to avoid implying one uniform "mandatory→optional→preserve" key. |

## Checks That Held (evidence)
- **Check 2 (keying / no bleed):** `grep -rli "grumpy king" kb/canon/ kb/timeline/` → NONE (gate-cond3's own grep claim reproduced). T3/T5 files contain zero T1 tokens (`grumpy`/`tidy`). T1 `adapted.md` body contains zero source names. Source names in T1 `continuity.md`/`decisions.md` are `(source: Sauron)` provenance annotations and `Sauron → "Grumpy King"` mapping arrows — the by-design provenance mechanism, NOT cross-tier bleed. `kb/canon/tolkien/ch-01.md` holds only source names (no `grumpy`/`tired`/`rest`). Per-tier `analysis.yaml` files are byte-identical to the shared `work/analysis/ch-01.yaml` (analyst is tier-invariant per CLAUDE.md §3) — correct, not a bleed.
- **Check 3 (safety rollup):** ch-01-t1.md verdict block: 6/6 sections PASS ⇒ result PASS, `automatic_failures: []`. Independently re-derived: forbidden-token scan = 0 hits; longest sentence = 9 words (≤12 threshold). Safety-checked `work/drafts/ch-01-t1-v2.md` body is byte-identical to promoted `kb/…/tier-1/…/adapted.md`. Rollup is internally consistent.
- **Check 4 (verdict propagation):** All 5 `gate-cond{1..5}-*.md` independently read as ✅ PASS; hard-gate table rolls all 5 as ✅ PASS ⇒ GREEN. No PASS in the rollup that is not PASS in its source. Gate-cond1's "16 CERTAIN + 3 PROBABLE" count independently confirmed (16 + 3, 0 UNCERTAIN). The only Check-4 defect is the evidence-string drift in Finding 2 (not a verdict mismatch).

## Actions Taken
None. `fix_authorization: FALSE` — REPORT ONLY. All six findings are documented above with specific locations and required fixes for the orchestrator/author to apply.

## Recommendations
- Fix Findings 1 & 2 before any downstream artifact quotes the T1 Théoden rendering — three artifacts currently carry three different strings for the same sentence, which will propagate.
- Findings 3-6 are advisory keying/scope-precision issues; resolve them to make the traceability column machine-resolvable and the gate scope explicit.
- The core gate outcome (GREEN, all 5 conditions genuinely PASS) is sound; the defects are in the rendering/quotation/keying layer, not in the pass/fail decisions.

## QA Complete
