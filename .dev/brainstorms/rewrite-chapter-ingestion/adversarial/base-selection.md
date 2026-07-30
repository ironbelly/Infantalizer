# Base Selection — Hybrid Scoring

> Step 3 of the adversarial pipeline. Quantitative + qualitative scoring → base selection for the merge.

## Scoring rubric (each 0-10)

| Dimension | Weight | A (architect) | B (analyzer) | C (refactorer) |
|---|---|---|---|---|
| **Constraint fidelity** (C1-C7, ADR-006, boundary contract, zero adopted edits) | ×3 | 9 | 9 | 10 |
| **Correctness / failure-mode safety** (silent-corruption avoidance, canon integrity) | ×3 | 8 | **10** | 6 |
| **Maintainability / extensibility** (single source of truth, extension channel) | ×2 | **9** | 8 | 8 |
| **Minimalism / reuse** (smallest moving parts, no scope creep) | ×2 | 7 | 6 | **10** |
| **Operational runnability** (works on today's narnia 4-of-17, no manifest) | ×2 | 8 | 6 | **9** |
| **Resume rigor** (formal DONE predicate + false-positive analysis) | ×1 | 7 | **10** | 7 |
| **Concrete grounding** (validated against live filesystem, real ACs) | ×1 | 8 | **9** | 8 |

**Weighted totals:**
- A: (9×3)+(8×3)+(9×2)+(7×2)+(8×2)+(7×1)+(8×1) = 27+24+18+14+16+7+8 = **114**
- B: (9×3)+(10×3)+(8×2)+(6×2)+(6×2)+(10×1)+(9×1) = 27+30+16+12+12+10+9 = **116**
- C: (10×3)+(6×3)+(8×2)+(10×2)+(9×2)+(7×1)+(8×1) = 30+18+16+20+18+7+8 = **117**

## Qualitative assessment

Three near-tied scores reflect genuine, defensible trade-offs — not a runaway winner:

- **C edges the weighted total** on minimalism + constraint fidelity + runnability. C's reframing of RQ1
  (category distinction: prep-package reads vs source-side enumeration) is the single most *clarifying*
  contribution and must be preserved as the contract's structure. C's weakness: its silent convention-fallback
  on a missing manifest (risk #1) under-delivers on S5 drift and is the design's honest blind spot.
- **B is the strongest on correctness** — the canon-cumativity framing and the uncertainty-propagation mechanism
  (force analyst→PARTIAL) are the design's load-bearing safety innovations. B's weakness: D3 hard-halt on
  partial sets would block the day-one narnia pilot unless the operator knows the flag; richest command surface.
- **A is the most balanced** — strong extensibility framing, but its drift behavior (NOTICE-only degrade) is
  weaker than B's and its provenance treatment weaker than C's.

## Decision: **B as merge base**, restructured by C's category distinction, with grafts.

**Why B as base, not C:** B's weighted score is within 1 of C, and on the *load-bearing* dimension
(correctness / canon integrity — ×3 weight) B scores 10 to C's 6. The rewrite phase's defining property is that
it writes **cumulative canon**; a design that under-weights that (C's silent fallback) is riskier than one that
over-weights runnability (B's strictness), because the latter's strictness is *softened* (see Round 4) while the
former's silence is *structural*. B is the safer base to soften than C is to harden.

**Why C's structure is preserved anyway:** C's category distinction is correct and should *frame* the merged
contract — it resolves the RQ1 seam by making the prep-package/source-side distinction explicit rather than
glossing it. The merge adopts C's two-group framing of `rewrite_phase_reads` (prep-package reads + source-side
enumeration reads), even though it grafts B's and A's mechanisms on top.

**Grafts (carried into the merge):**
1. From **C**: two-group read-set structure (prep-package reads frozen-3 + source-side enumeration group); minimal default command surface; provenance NOTE that the manifest is not Rule-F hash-pinned.
2. From **B**: uncertainty-propagation (`--allow-no-manifest` and accepted-drift force analyst→PARTIAL, facts ≤ PROBABLE); formal three-way AND DONE predicate + false-positive analysis; T4/T5-safety-SKIP discovery; per-chapter accept flags as auditable escape hatches; `scope: partial` downstream stamping.
3. From **A**: extension-channel framing for the manifest schema; per-chapter (not run-level) drift halt blast radius; WARN-on-partial default.

**Softened from B:** D3 partial-set behavior defaults to WARN+intersect (A/C) rather than hard-halt (B); hard-halt only on an explicitly-requested-but-absent chapter.

## Convergence

Resolved convergence: **0.86** (PASS, > 0.75). No unresolved conflicts. The merge proceeds to Step 4 (refactor plan) and Step 5 (merge execution).
