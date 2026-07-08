# Refactor Plan — Assembling the Merged Decision from Base C + Grafts

Base = Proposal C (Hybrid). Transformations applied to reach `merged-requirements.md`:

1. **Adopt C's three-column classification** (agents, skills, kb) verbatim as the architecture skeleton.
2. **Graft G1 (from B):** replace C's underspecified "shared analysis object + tier-coordinator" canon
   handling with B's per-tier canon model — add `kb/adaptations/<work>/tier-N/{decisions,continuity}.md`
   and the (work, tier, chapter) three-part key to the kb layout; assign it to the greenfield chronicler
   + tier-coordinator.
3. **Graft G2 (from B):** annotate C's parallel multi-tier fan-out with a documented sequential
   degradation mode for state-heavy works.
4. **Graft G3 (from A):** add the explicit written invariant "review quartet is 4 distinct modes; editor
   is never folded" to §2.1 and constraint-check row #4.
5. **Reject A's fork packaging + ADR-006 reversal:** keep C's "cut plugin/Mars, single-tree" decision.
6. **Reject B's editor-drop + continuity/chronicler merge:** keep four distinct review agents.
7. **Carry forward all admitted costs** into §7 Residual Risks with required mitigations (boundary
   contract CI check, Phase-3 hard gate).

Result: a base whose grafts are additive (data-model + written invariant), not corrective — no graft
reopens C's cost structure.
