# Phase-3 — Multi-Tier Fan-Out T1/3/5 — Run Summary (Step 5.4)

**Work:** tolkien | **Chapter:** ch-01 | **tiers:** [1, 3, 5] | **mode:** parallel (default) | **Run:** 2026-07-03
**Raw capture:** `phase-outputs/test-results/phase3-fanout-raw.txt`

## Fan-out topology
`analyst` ran **once** (tier-invariant shared truth: `work/analysis/ch-01.yaml`). The full review quartet
(critic + editor + reader-sim + continuity-checker) ran **once at T1** per the gate's quartet-condition
scope; the quartet was not re-run per tier. `tier-coordinator` fanned the transform across T1/T3/T5 — T1
ran the full 11-step pipeline (transform + quartet + safety(blocking) + reconcile + chronicle), while
T3/T5 ran the transform + safety (advisory/N-A) path and were reconciled by `tier-coordinator` and
promoted by `chronicler` (parallel default; sequential G2 fallback not needed — the proof work is not
state-heavy). Then `chronicler` ran per tier on muse-accept. The fan-out proves tier-differentiation +
cross-tier reconciliation, not that every tier independently re-ran the quartet.

## Per-tier convergence

| Tier | adapted.md | safety | continuity.md | canon-delta.md | analysis.yaml (promoted) | decisions.md |
|------|-----------|--------|---------------|----------------|--------------------------|--------------|
| T1 | ✓ | PASS (blocking) | ✓ | ✓ | ✓ | ✓ |
| T3 | ✓ | PASS (advisory) | ✓ | ✓ | ✓ | ✓ |
| T5 | ✓ | N/A (skipped) | ✓ | ✓ | ✓ | ✓ |

## tier-coordinator status
`work/analysis/ch-01-cross-tier.md`: **status: RECONCILED · conflicts: []** — the empty conflict list is
the precondition that let chronicler run. reconcile() checks:
- **A source-fidelity:** PASS (every tier rendering traces to a shared analysis fact).
- **B disclosure-leak:** PASS (T1 defers the death via journey/rest; T3/T5 disclose it, as permitted).
- **C monotonicity:** PASS (maturity T1 ≤ T3 ≤ T5 for every shared element: mandatory-transform < optional < preserve).

## Tier-differentiation (proof the axis works)
The same source element renders differently per tier and stays partitioned:
- Sauron → "The Grumpy King" (T1) / "Sauron" menace (T3) / "Sauron" near-source (T5).
- Théoden's fall → "grew very tired and sat right down" (T1) / "Théoden died" (T3) / "did not rise again" (T5).

## Chronicler invariant (verified across all tiers)
**No tier-transformed name was promoted to shared `kb/canon/`.** Grep confirms "Grumpy King" appears
**only** under the per-tier tier-1 canon `kb/adaptations/tolkien/tier-1/` (continuity, canon-delta,
adapted, decisions) and the work-mapping config `kb/adaptation-mapping/tolkien-mapping.yaml`, and is
**absent** from shared `kb/canon/` and `kb/timeline/`. Shared canon holds source names only (Sauron,
Denethor, Théoden, Éowyn, Nazgûl). No cross-tier bleed.

## Overall fan-out result
**CONVERGED / RECONCILED** — T1 ran the full 11-step pipeline (incl. the quartet); T3/T5 ran the
transform + safety + reconcile + chronicle path; tier-coordinator returned RECONCILED with empty
conflicts, chronicler wrote per-tier canon keyed (work, tier, ch-01), and the (work,tier,chapter)
partitioning + no-shared-canon-leak invariants hold. Ready for gate-condition evaluation (Steps 5.6-5.11).
