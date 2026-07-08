# Base Selection & Merge Log

## Base
**Proposal C (Hybrid)** — score 41/50; wins constraint-fidelity (9) and cost-realism (8).

## Scoring summary
| | A (Fork) | B (Native) | C (Hybrid) |
|---|---|---|---|
| Sum | 29 | 33 | **41** |

## Grafts applied to base C
| # | Source | Graft | Rationale | Status |
|---|--------|-------|-----------|--------|
| G1 | B | Per-tier canon state: per-tier `continuity.md` + (work,tier,chapter) three-part key, injected into C's greenfield chronicler + tier-coordinator | Closes C's latent "same character, divergent canonical state per tier" bug (Gandalf OMIT@T1 / passed-on@T2 / died@T3) | NON-OPTIONAL — applied |
| G2 | B | Sequential multi-tier as documented degradation mode (parallel default) | Hedges C's cross-tier reconciliation risk for state-heavy works | applied |
| G3 | A | Quartet-intact written invariant ("never fold editor; 4 review modes are load-bearing") | Inoculates against C's own boundary-drift temptation AND B's editor-collapse | applied |

## Rejected
- **From A:** fork packaging inheritance (mars.toml, cw/ dual trees, CI sync) + ADR-006 reversal.
  C's "cut plugin/Mars, single-tree" decision holds.
- **From B:** editor-drop + continuity/chronicler merge (violates constraint #4 and #6).

## Merge principle
C is the only base whose grafts are additive, not corrective. B's per-tier canon is data-model advice
that drops into C's greenfield chronicler. A's quartet-discipline is a zero-cost written invariant.
Building on B would force re-litigating the quartet; building on A would force re-litigating ADR-006.
