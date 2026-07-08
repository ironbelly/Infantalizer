# Diff Analysis — A vs B vs C

## Convergence points (all three agree)
- `analyst` runs as a pre-orchestration phase (source analysis before generation).
- `safety-verifier` is a distinct agent (not a critic focus, not a continuity mode).
- Workflow is chapter-driven, executed through session machinery.
- `chronicler`/canon-extraction must be BUILT (unshipped vapor in CWS on every path).
- Confidence tagging (v2.0) owned by the analyst via a source-fidelity discipline.
- CWS plugin/Mars packaging is rejected/avoided (even A admits it as a pure cost).
- safety_check promoted to an agent with an explicit FAIL→revise loop.

## Divergence axes (genuine architectural choices)
| Axis | A | B | C | Resolution in merge |
|------|---|---|---|---------------------|
| Provenance | fork CWS | native rebuild | hybrid adopt+native+greenfield | **C** |
| Tier axis role | skill on generative spine (demoted) | native spine | native spine + adopted machinery | C (native spine) |
| Review quartet | kept (4) | editor dropped, continuity+chronicler merged (collapse) | kept (4) + safety 5th | C, reinforced by A's invariant (G3) |
| Multi-tier | parallel | sequential | parallel | parallel default + **sequential fallback (G2 from B)** |
| Per-tier canon | implicit/underspecified | explicit (work,tier,chapter) | implicit/underspecified | **B's per-tier model grafted (G1)** |
| ADR-006 | reversed (cost) | untouched | untouched | C (untouched) |
| Agent-file edits | yes (grafted muse) | n/a (all native) | forbidden (boundary contract) | C (forbidden) |

## Contradictions resolved
- **A's reuse claim vs vapor fact:** A's "adopt mature machinery" is discounted — the most-needed agent
  (canon-extraction) is missing. Merge treats canon-extraction as greenfield (agrees with all three).
- **B's coherence vs quartet collapse:** B's tier-as-spine is adopted; B's editor-drop is rejected in
  favor of A's quartet-intact invariant.
