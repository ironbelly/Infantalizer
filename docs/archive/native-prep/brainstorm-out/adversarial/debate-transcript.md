# Debate Transcript — A vs B vs C on the 3 contested axes

> Adversarial debate. Each proposal defends its position; the merge resolution is decided on
> boundary-contract safety, anti-hallucination rigor, and scope discipline (framework rules #6, #8).

## DEBATE 1 — Skill count: 4 skills (A/B) vs 1 skill (C)

**A defends 4:** "Each concern (protocol, mapping, taxonomy, thematic-fidelity) is independently reusable.
`thematic-fidelity` could attach to multiple agents; splitting enables that."

**C rebuts:** "Reusability is speculative (rule #8 — scope discipline). In practice `thematic-fidelity`
attaches to exactly the prep phase + the tier-coordinator body. Four skills for one phase recreate the
'curated document set' the prep phase exists to replace. One cohesive skill with clear sections is
easier to sync, classify in VENDOR.md, and reference (`- laf-adaptation:prep`)."

**B's position:** "I don't care strongly about skill COUNT; I care that the traceability matrix exists.
Whether it's a separate skill or a section is secondary. But I note C's single-skill size risk."

**Resolution:** **C wins the structural argument** — but with a modification. One monolithic `prep` skill
risks the "single-skill size" failure C itself flagged (C.8). The merge adopts: **two NATIVE skills** —
`prep` (the phase procedure: path contract, taxonomy, mapping authoring, gate, greenlight, handoff,
traceability) and `thematic-fidelity` (the meaning-preservation concept: analyst meaning-field spec,
Check D definition, exemplar-marking rules). Justification for keeping `thematic-fidelity` separate: it
is the ONE piece that crosses into the rewrite phase (Check D runs in tier-coordinator during rewriting),
so it is genuinely cross-phase reusable, unlike the purely-prep concerns. This is A's reusability
argument, but scoped to the ONE skill where it actually holds. Net: 2 new skills, not 4, not 1.

**Why not 4:** `work-mapping`, `challenge-taxonomy`, and `prep-protocol` are all prep-only and cohesive →
fold into `prep`. **Why not 1:** `thematic-fidelity` is cross-phase → keep separate.

## DEBATE 2 — Question gate: free-form (A) vs coverage-constrained (B)

**A defends free-form:** "Simpler. The orchestrator asks what it thinks matters; `[skip]` handles the
rest. Less machinery."

**B rebuts:** "Free-form risks MISSING the allegory/meaning decision — the single highest-value question
(the evaluation's 'one durable value-add'). The taxonomy ALREADY knows which challenge types have a
human-judgment dimension (allegory → yes, violence-level → no). Making the gate coverage-constrained
GUARANTEES the meaning-preservation question surfaces when the work demands it, and GUARANTEES we don't
pester the user about deterministic rules. This is spec-kit's clarify-coverage pattern made rigorous
(enrichment §1)."

**C's position:** "Agrees with B, but the coverage rule lives in the `prep` skill §6, and the
`human_judgment_dimension` flag must ship pre-set per challenge type in the taxonomy (B.7 mitigation)."

**Resolution:** **B wins.** The gate is coverage-constrained by the taxonomy's `human_judgment_dimension`
flag. The flag ships pre-set (death → yes, allegory → yes, violence-level → no, petrification → yes,
battle-scope → yes). `[skip]` is allowed per question but RECORDED in `70-traceability.md` so the rewrite
phase knows a decision was defaulted, not made. This is the rigorous version of "ask only what changes
the work."

## DEBATE 3 — Meaning-preservation → adopted agents: patch writer again (A/B) vs route via mapping (C)

**A/B defend patching writer:** "The writer is ADOPTED-PATCHED; one more additive `skills:` line is
permitted. Attaching `thematic-fidelity` directly is the most reliable way to ensure the writer obeys
meaning-preservation."

**C rebuts:** "The boundary contract's DEMONSTRATION is that `writer` gets exactly ONE additive line
(`adaptation-rules`). A second line weakens the minimal-patch exemplar and sets a patch-creep precedent —
exactly what the boundary contract exists to prevent. Worse, it's UNNECESSARY: the muse builds the scene
brief and already reads `kb/adaptation-mapping/`. If the work-level `meaning` map is folded into the
promoted mapping file (the promoted `30-mapping.yaml`), the muse picks it up with ZERO adopted-body edits,
and injects 'preserve this meaning' into the scene brief. The writer obeys the brief. No writer edit
needed."

**B's concern:** "Does muse actually scan `kb/adaptation-mapping/` generically, or does it read specific
files? If specific, folding meaning into the mapping file is correct (C.8 resolution); a separate
`meaning.yaml` would NOT be picked up."

**Resolution:** **C wins.** Meaning-preservation reaches adopted agents via the **promoted mapping file**:
the work-level `meaning:` is a top-level key in `30-mapping.yaml`, promoted to
`config/concept_mapping/templates/<work>_mapping.yaml` + `kb/adaptation-mapping/<work>_mapping.yaml` on
greenlight. Muse already reads the mapping; no adopted-body edit. The `writer.md` patch stays at exactly
ONE line (the existing `adaptation-rules`). This is the cleanest possible boundary respect and resolves
A.13 Q1 definitively. **The merge adopts C.5's refinement: `meaning` is folded INTO the mapping file, not
a separate file** (handles B's concern about muse's read granularity).

## Cross-cutting: anti-hallucination topology (B's traceability matrix)

All three now agree the contamination fix needs more than DERIVED markers on exemplars. **B's
traceability matrix is adopted** (`70-traceability.md`), auto-emitted by the `prep` skill's §8. It maps
every package artifact + every mapping entry to its derived-from facts + gap-closed + confidence. The
rewrite phase's muse reads `30-mapping.yaml` (which carries per-entry confidence) — the traceability
matrix itself is for human audit + the greenlight decision, not necessarily in the rewrite's hardcoded
read path (resolves B.9 Q1).

## Convergence after debate

All 3 disagreements resolved by clean picks (no compromises that weaken any proposal). Convergence:
**0.85** (up from 0.82). PASS. Proceed to merge.
