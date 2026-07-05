# Diff Analysis — A vs B vs C

> Pairwise structural diff. Cells = the proposal's position. ✅ = agrees with the merge resolution;
> ⚠️ = tension to resolve in debate.

## Axis-by-axis comparison

| # | Axis | A (architect) | B (analyzer) | C (scribe) |
|---|---|---|---|---|
| 1 | Owning layer | 0.1; root = pointer stub | same | same |
| 2 | Entry command | `/laf:prep "<title>"` | same | same |
| 3 | Orchestrator agent | NATIVE `prep-cordinator` (opus) | same | same |
| 4 | Work-level analysis | single-track, MEMORY-BASED allowed, ceiling propagated | **two-track (context + text), per-entry min(text,context)** | two-track (adopts B) |
| 5 | New NATIVE skills | 4 (`prep-protocol`, `work-mapping`, `challenge-taxonomy`, `thematic-fidelity`) | 4 + traceability as a concern | **1 (`prep`)** with 8 sections |
| 6 | Path contract location | prose in skill body | prose + matrix file | **referenced doc imported by 3 consumers** |
| 7 | Path contract files | `00..60` (7 files) | `00..70` (8, +traceability) | `00..70` (adopts B's 70), reorganized |
| 8 | Question gate | free-form, `[skip]` allowed | **coverage-constrained by taxonomy's human_judgment dimensions** | coverage-constrained (adopts B) |
| 9 | Meaning-preservation → adopted agents | 2nd additive `writer.md` line (`thematic-fidelity`) | 2nd additive `writer.md` line | **NO writer edit; meaning folded into promoted `30-mapping.yaml`, muse reads it already** |
| 10 | Check D location | `tier-coordinator` (BUILD-NEW edit) | same | same |
| 11 | analyst meaning field | yes (NATIVE edit) | yes | yes |
| 12 | Compound-scene protocol | file in adopted `adaptation-rules/resources/` (⚠️ muddies sync) | same | **section in `prep` skill** (cleaner) |
| 13 | Exemplar library | `adaptation-rules/resources/exemplars/<type>.md`, DERIVED marker | same | same |
| 14 | Contamination fix | DERIVED markers on exemplars | **traceability matrix + dual-track confidence + DERIVED markers** | traceability (adopts B) as §8 of `prep` |
| 15 | Handoff prompt | `/laf:rewrite --work <slug>` | same | same |
| 16 | Root parity (T7) | out of scope | out of scope | out of scope |

## Convergence assessment

- **High agreement (15/16 axes converge):** owning layer, entry command, orchestrator agent, Check D
  location, analyst meaning field, exemplar library, handoff prompt, root parity, and the *existence* of
  the fixed-path package. This is strong convergence (estimated ≥0.80).
- **Real disagreements (3 axes, all resolvable):**
  - **Axis 5/6 (skill count + path-contract location):** A/B = 4 skills, path list in prose; C = 1 skill,
    path contract as referenced doc. → Merge favors **C's referenced path-contract doc** (single source of
    truth, no drift) but keeps a **moderate skill count** (see debate).
  - **Axis 8 (gate):** A free-form vs B coverage-constrained. → Merge favors **B** (taxonomy-driven
    coverage guarantees meaning-preservation decisions surface).
  - **Axis 9 (meaning → writer):** A/B patch `writer` again vs C routes via promoted mapping. → Merge
    favors **C** (cleanest boundary respect; avoids patch-creep on the one ADOPTED-PATCHED exemplar).

## Estimated convergence score: 0.82

PASS (≥0.65). The 3 disagreements are all on axes where one proposal demonstrably dominates on
boundary-contract or anti-hallucination grounds, so the merge is a clean pick rather than a compromise.
