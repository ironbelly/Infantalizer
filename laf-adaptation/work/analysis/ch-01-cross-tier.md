# Cross-Tier Reconciliation — Tolkien ch-01

tiers: [1, 3, 5]     mode: parallel     source: work/analysis/ch-01.yaml

*Produced by tier-coordinator (step 10). Parallel fan-out (default) against the single shared analysis
(analyst ran once): T1 ran the full 11-step pipeline (incl. the review quartet); T3/T5 ran the transform +
safety (advisory/N-A) path. This report reconciles their `adapted.md` outputs before chronicler promotes
canon.*

## Shared source anchors (from analysis)
- Sauron (antagonist; acts from afar) — CERTAIN
- Denethor (the Steward; despairs and withdraws) — CERTAIN
- Théoden (old king; leads the riders, is struck down) — CERTAIN
- Éowyn (destroys the Nazgûl rider over the fallen king) — CERTAIN
- The Nazgûl (rider whose cry unmans brave men) — CERTAIN
- The Grey City holds; the host withdraws east — CERTAIN

## Per-tier renderings (traceability)
| Element | T1 | T3 | T5 | shared anchor |
|---------|----|----|----|---------------|
| Sauron | "The Grumpy King" (no sunshine) | "Sauron" (cold will, true menace) | "Sauron" (as source) | characters[Sauron] |
| the siege/battle | "The Big Tidy-Up" | "the fighting … stakes were real" | "The battle was terrible" | events[siege/clash] |
| Théoden's fall | "grew very tired and sat right down" | "struck the king down … Théoden died" | "Théoden fell, and did not rise again" | events[king struck down] |
| the Nazgûl | "Grumpy Riders" (shy shadow, smiles) | "the Nazgûl … cry drained courage" | "the Nazgûl … cry unmanned brave men" | characters[Nazgûl] |
| Denethor | "Sad Leader" (closed windows, reopened) | "Denethor … had given way … despair" | "Denethor … something had already broken" | characters[Denethor] |
| soldiers fallen | "tired and needed a rest" | "many soldiers had died … grief" | "many good soldiers had fallen and would not rise" | events[soldiers fall] |

## Checks
- **A source-fidelity:** PASS — every T1/T3/T5 rendering above traces to a fact present in
  `work/analysis/ch-01.yaml`; no tier introduced an unsourced fact.
- **B disclosure-leak:** PASS — T1 does NOT disclose the death (renders it as "tired/rest", per its
  `death_euphemism: journey_or_sleep` rule); T3 and T5 disclose it plainly, which their profiles permit.
  No lower tier reveals what only a higher tier should.
- **C monotonicity:** PASS — for every shared element, maturity(T1) ≤ maturity(T3) ≤ maturity(T5): T1 is
  `mandatory`-transform (Grumpy King / Big Tidy-Up / rest), T3 is `optional`-transform (named, direct
  death, weight-not-gore), T5 is `preserve` (near-source). Non-decreasing by tier for all elements.

status: RECONCILED
conflicts: []
