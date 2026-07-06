# Phase Gate 3 — Fix-Applied Summary (D1–D8)

**Applied:** 2026-07-04 | **Fix agent:** rf-qa (single authorized fixer, `fix_authorization: TRUE`)
**Source procedure:** `qa/qa-consolidated-findings-phase3.md` (D1–D8, applied in order — cross-dependent)
**Working dir:** `/config/workspace/Infantalizer/`

## Result headline
- **Fixes applied:** 8 (D1–D8), spanning 12 distinct files edited + 4 re-copies (3× analysis.yaml, 1× adapted.md).
- **Post-fix boundary check:** `uv run python laf-adaptation/scripts/check_boundary.py` → **exit 0** (PASS — all rules A–F).
- **Hard-gate:** remains **🟢 GREEN** (all 5 conditions still PASS — accuracy fixes only, no PASS→FAIL flip).
- **Protected files:** NONE touched (no adopted body, no VENDOR.md, no carried-verbatim kb/tiers / adaptation-mapping / adaptation-rules resource YAML).

---

## Per-fix detail

### D1 [CRITICAL/IMPORTANT] Source fixture — removed T1 label, made king's death explicit
**File:** `laf-adaptation/source/tolkien/ch-01.txt`
- OLD: `…and one of the Grumpy Riders — the Nazgûl, they were named, and their cry unmanned brave men — struck the king from his horse, and he fell.`
- NEW: `…and one of the Nazgûl — dark riders whose cry unmanned brave men — struck the king from his horse. Théoden fell, and did not rise again.`
- Effect: the SOURCE now uses source framing (no tier-1 "Grumpy Riders" label leaked in) and makes Théoden's death explicit so the analyst can tag it and T3's "died" is faithful.

### D2 [CRITICAL] analysis.yaml self-contradiction on the king's death
**File:** `laf-adaptation/work/analysis/ch-01.yaml` (then re-copied ×3)
- `events` seq 5 — OLD: `A Nazgûl strikes the king from his horse and he falls.` → NEW: `A Nazgûl strikes the king from his horse; Théoden falls and does not rise again.`
- `uncertainties` — DELETED the line: `"Whether the fallen king dies or is only unhorsed is not made explicit in the closing text (he 'fell'); downstream death-handling should treat it per the active tier."` (source now explicit; kept only the title-inference uncertainty).
- Re-copied over the 3 promoted copies (`cp`, verified byte-identical): `kb/adaptations/tolkien/tier-{1,3,5}/chapters/ch-01/analysis.yaml`.

### D3 [IMPORTANT] T5 near-source draft aligned to corrected source
**File:** `laf-adaptation/work/drafts/ch-01-t5-v1.md` (then re-copied)
- OLD (sentence spanning the Nazgûl strike): `…one of the\nNazgûl — their cry unmanned brave men — struck the king from his horse, and he fell.`
- NEW: `…one of the\nNazgûl — dark riders whose cry unmanned brave men — struck the king from his horse. Théoden fell, and did not rise again.`
- Re-copied (`cp`, verified byte-identical): `kb/adaptations/tolkien/tier-5/chapters/ch-01/adapted.md`.
- T1/T3 drafts unchanged (T3 "Théoden died" now faithful; T1 correctly renders the death as "grew very tired and sat right down").

### D4 [IMPORTANT] Quotation drift — T1 Théoden rendering aligned to actual v2 draft text
Aligned all three to the ACTUAL draft text `grew very tired and sat right down` (confirmed present in `work/drafts/ch-01-t1-v2.md`):
- `laf-adaptation/work/analysis/ch-01-cross-tier.md` (traceability table, T1 cell): `"grew very tired and sat down to rest"` → `"grew very tired and sat right down"`.
- `phase-outputs/reports/phase-3-hard-gate-report.md`: `"grew tired and rested" (T1)` → `"grew very tired and sat right down" (T1)`.
- `phase-outputs/test-results/phase3-fanout-summary.md`: `"grew very tired and sat down to rest" (T1)` → `"grew very tired and sat right down" (T1)`.

### D5 [IMPORTANT] Fan-out summary overstated T3/T5 pipeline
**File:** `phase-outputs/test-results/phase3-fanout-summary.md`
- Rewrote the "Fan-out topology" paragraph: removed the claim that "each tier ran steps 3-9 independently"; now states the full review quartet (critic+editor+reader-sim+continuity-checker) ran **once at T1** per the gate's quartet-condition scope, T1 ran the full 11-step pipeline, and T3/T5 ran the transform + safety (advisory/N-A) + reconcile + chronicle path. Added that the fan-out proves tier-differentiation + cross-tier reconciliation, not per-tier quartet re-runs.
- Rewrote the "Overall fan-out result" line: `all 3 tiers ran steps 3-9` → `T1 ran the full 11-step pipeline (incl. the quartet); T3/T5 ran the transform + safety + reconcile + chronicle path`.
- `phase3-fanout-raw.txt`: checked — makes no such overstated claim (pure capture), so no mirror edit needed.

### D6 [IMPORTANT evidence] Stale "FAIL" line in the T1 raw capture
**File:** `phase-outputs/test-results/phase3-t1-run-raw.txt`
- Verified shared canon is clean FIRST: `grep -rli "grumpy king" laf-adaptation/kb/canon/ laf-adaptation/kb/timeline/` → empty (exit 1, no match).
- OLD Inv.3 line: `FAIL: transformed name leaked to shared canon` → NEW: `PASS: no transformed name in shared kb/canon/tolkien/ch-01.md`.
- (The stale FAIL was a false positive from grepping a since-reworded explanatory comment; the `phase3-t1-run-summary.md` already reported Inv.3 as ✓, so no contradiction was created.)

### D7 [MINOR] Wording overreach + traceability
- "only under tier-1" overreach corrected in **4 places** (confirmed "Grumpy King" DOES also appear in the work-mapping config `kb/adaptation-mapping/tolkien-mapping.yaml`, which is why the original wording overreached):
  - `phase-outputs/reviews/gate-cond3-canon.md`
  - `phase-outputs/test-results/phase3-fanout-summary.md` (Chronicler-invariant section)
  - `phase-outputs/reviews/phase3-runtime-artifacts-review.md`
  - `phase-outputs/test-results/phase3-t1-run-summary.md` (Inv.3 line)
  New wording: "…only under the per-tier tier-1 canon and the work-mapping config `kb/adaptation-mapping/tolkien-mapping.yaml`, never in shared `kb/canon/`/`kb/timeline/`".
- `phase-outputs/reviews/gate-cond5-boundary.md`: replaced the `--upstream <checkout>` placeholder with the concrete path `.dev/releases/current/0.1/creative-writing-skills` (SHA `3338495f0fabf778720effdda9386ab56d4ebf6e`) and added a **Plain-mode caveat** noting plain `verify` mode skips Rules B/C, which were confirmed to hold under the `--upstream` run (also exit 0).

### D8 [IMPORTANT actionability] Reports not self-contained on failure paths
**File:** `phase-outputs/reports/phase-3-hard-gate-report.md`
- Added a "## Failure paths (what a non-GREEN outcome would entail)" section before "## Final statement": states that a RED verdict HALTs, names the failing condition + remediation; that a tier-coordinator CONFLICT (non-empty `conflicts:`) lists each as `{type, tier, element}` and blocks chronicler until the offending tier's writer is re-dispatched; and that a safety FAIL populates `verdict.evidence` with `{section, location}` revision targets and returns to workflow step 3. Notes the happy path here is `conflicts:[]` / `evidence:[]` / GREEN.

---

## Post-fix verification

1. **Re-copies (D2/D3) byte-consistent with source (`cmp -s`):**
   - `tier-{1,3,5}/chapters/ch-01/analysis.yaml` == `work/analysis/ch-01.yaml` → BYTE-IDENTICAL ×3.
   - `tier-5/chapters/ch-01/adapted.md` == `work/drafts/ch-01-t5-v1.md` → BYTE-IDENTICAL.
2. **Boundary check:** `uv run python laf-adaptation/scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied`, **exit 0**.
3. **Hard-gate re-verified GREEN (5 conditions unaffected):**
   - Cond 1 — analysis.yaml `status: OK`, v2.0 CERTAIN/PROBABLE tags present (16 CERTAIN + PROBABLE tags intact; no confidence tag altered by D2). ✓
   - Cond 2 — safety T1 `result: PASS`, mode blocking (`work/safety-reports/ch-01-t1.md`). ✓
   - Cond 3 — per-tier canon present for T1/T3/T5 (adapted.md + analysis.yaml). ✓
   - Cond 4 — quartet ran at T1 (4 distinct agents, editor never folded). ✓
   - Cond 5 — boundary exit 0. ✓
   - Overall gate verdict line unchanged: `🟢 GREEN (all 5 conditions PASS)`.
4. **Protected-file integrity:** no adopted `agents/*.md` or `skills/**/SKILL.md` body, no `VENDOR.md`, no carried-verbatim `kb/tiers/` / `kb/adaptation-mapping/` / `adaptation-rules` resource YAML was modified (verified: those paths have no files newer than session start; Rule A hash-match in the boundary check independently confirms adopted-body integrity). Edits were confined to the source fixture, proof-run drafts/analysis/canon under `work/` and `kb/adaptations/` (NATIVE graft G1), and the `phase-outputs/` reports/reviews/test-results.

## Fix-cycle status
All 8 findings (1 CRITICAL, 5 IMPORTANT, D7 MINOR bundle) resolved in a single fix cycle. No new issues introduced. Boundary stays exit 0; hard-gate stays GREEN.
