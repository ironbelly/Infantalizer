# Findings & Evaluation: the hand-authored LWW prep package vs. native capability

> Standalone context for a fresh session. This records an evaluation of a hand-authored preparatory
> document set for *The Lion, the Witch and the Wardrobe* (LWW) against what the Literary Adaptation
> Framework (LAF) already does natively. It exists so the brainstorm can reason about *which* prep
> results are worth internalizing and *which* are already native. All claims are grounded in the
> framework files mapped in `30-current-framework-map.md`.

## The artifact under evaluation

A prep package was hand-authored for LWW:

- `config/concept_mapping/templates/narnia_mapping.yaml` — a per-work mapping (characters, concepts,
  key scenes, master translation table).
- `docs/guides/lion-witch-wardrobe/README.md`, `ADAPTATION_GUIDE.md`, `STONE_TABLE.md` — prose guides:
  the adaptation challenges, each key challenge across Tier 1/3/5, and a deep-dive on the hardest scene
  (Aslan's death + resurrection).

## Necessary split: two different kinds of artifact

| Artifact | Type | Native status |
|---|---|---|
| `narnia_mapping.yaml` | A **native input format** (a work mapping) | Legitimate. `config/concept_mapping/templates/` (root) and `kb/adaptation-mapping/` (0.1) are exactly for this. |
| The three prose docs | **Documentation**: pre-computed decisions + worked exemplars + a curated cross-tier view | Not a native artifact. This is the "document set brought to the table" whose function should be internalized. |

The mapping YAML is a normal framework citizen. The prose docs are the crutch worth scrutinizing.

## Q1 — The prose set vs. what the framework does natively

| What the prose supplies | Native equivalent | Verdict |
|---|---|---|
| **Cross-tier T1/T3/T5 spine** (`ADAPTATION_GUIDE.md`) | `tier-coordinator` emits `work/analysis/ch-NN-cross-tier.md` with a per-tier renderings table + three formal checks (source-fidelity consistency, disclosure-leak, framing monotonicity) | **Native already does this dynamically and more rigorously** (0.1 layer). The doc is a static hand-curated version of the coordinator's output. Root v1.0 has no equivalent. |
| **Hard-case holistic reasoning** (`STONE_TABLE.md`) | Emergent from the 11-step loop (writer→critic→editor→writer→continuity→safety-verifier→reader-sim) + `character.yaml`'s ad-hoc `special_handling` (Gollum, Denethor) | **Partially native.** No explicit "this scene trips multiple rules at once" protocol — quality emerges from the critique loop, so it is high-variance. The doc pre-bakes the method as an exemplar. |
| **Per-work decisions** (Stone Table -> "big rest", Edmund -> "silly mistake") | `narnia_mapping.yaml` is the native carrier; `ADDING_NEW_WORKS.md` is the native process | **Form is native, content is not.** The framework supplies the process and the rule tables but not the decisions; nothing scores their quality. |
| **"Neither add nor strip the allegory"** (`README.md`) | `source-fidelity` = factual fidelity; `adaptation-rules` = surface transforms | **Genuine gap in both layers.** Nothing preserves or checks thematic/meaning fidelity. |
| **Before -> after example pairs** | Transform prompts carry one tiny example each; the 0.1 `writer` produces real drafts | Native produces actual drafts, not illustrative snippets. The pairs are teaching aids. |

**Headline:** roughly 80% of the prose set duplicates, in static form, capability the 0.1 native
pipeline already has dynamically (cross-tier reconciliation, safety, fidelity). Two things are not
redundant: (a) the consistency/quality of per-work decisions, which native leaves to unassisted agent
reasoning; and (b) the meaning-preservation discipline, a true gap. Against root v1.0 *alone* the docs
add a great deal, because root has no orchestration, no cross-tier tool, and ships only T1+T3.

## Q2 — Impact of the prose docs on an agent rewriting LWW

**Lift (real):** decision short-circuit (lower cost, lower run-to-run variance, consistent framing);
few-shot exemplar for compound scenes the pipeline does not explicitly teach; a cross-tier prior that
helps keep framing monotonic (the property `tier-coordinator` Check C polices); and it names the
allegory constraint the framework otherwise lacks.

**Risk (also real):**
- **Anti-hallucination contamination.** The renderings are labelled "illustrative / not canonical," but
  an agent holding them in-context can treat invented phrasings as verified source, undermining
  `source-fidelity`'s rule that every fact trace to the actual book with a confidence tag. The docs are
  not analyst output, are not tagged, and sit outside the `work/`->`kb/` lifecycle; in the 0.1 layer
  this quietly bypasses the boundary contract's clean provenance.
- **Anchoring / collapsed exploration.** A strong prior doc can collapse "adapt this scene" into "copy
  the doc," suppressing the adversarial critique that is the pipeline's main quality engine.
- **Authority confusion.** The docs assert one interpretation (specific omissions, one allegory stance)
  as if settled.

**Net:** the docs raise the floor for a weak or one-shot agent, but for the full 0.1 pipeline they are
partly redundant and carry a fidelity-contamination cost. The single durable value-add is
meaning-preservation.

## Q3 — What the framework needs to produce this natively (no bespoke doc set)

Each change internalizes something the docs currently supply. In the 0.1 layer these must be added as
NATIVE skills / additive frontmatter or edits to the BUILD-NEW bodies only — never edits to adopted
bodies (boundary contract).

1. **Thematic-fidelity invariant (highest value — closes the real gap).** A NATIVE `thematic-fidelity`
   skill (or an extension of `source-fidelity`) that captures each scene's meaning during analysis
   ("love that outlasts the worst thing"; the substitution logic), a `theme`/`meaning` field added to
   the analyst output schema (`work/analysis/ch-NN.yaml`), and a **Check D (meaning-preservation)** in
   `tier-coordinator` asserting every tier preserves the meaning while the surface transforms.
   Generalizes "neither add nor strip the allegory." Attach via `skills:` frontmatter to `analyst`,
   `tier-coordinator`, `writer`.
2. **Explicit compound-scene protocol (internalizes `STONE_TABLE.md`).** Promote `character.yaml`'s
   ad-hoc `special_handling` into a first-class procedure: when the analyst's `transformation_flags`
   show >=2 high-severity categories co-occurring (violence+death+emotional), flag a "compound scene"
   and hand the writer a documented reconciliation method (find emotional core -> decompose surface ->
   convert/name/preserve by tier -> verify meaning survived). Ship as
   `adaptation-rules/resources/compound-scenes.md` + an analyst flag.
3. **Native work-mapping authoring (internalizes `narnia_mapping.yaml` quality).** A pipeline pre-step
   that derives `<work>-mapping.yaml` from the confidence-tagged analysis + `key_challenges` (challenge
   -> governing rule -> per-tier strategy), with a challenge taxonomy so "sacrificial death +
   resurrection" reliably routes to `death_handling` + the compound-scene machinery. Turns the mapping
   from a hand-authored prerequisite into a pipeline output.
4. **Retrievable hard-case exemplar library (internalizes the few-shot benefit generically).** A small
   set of challenge-typed exemplars (sacrifice-and-return, betrayal-and-redemption,
   petrification/body-horror) under `adaptation-rules`, loaded by the writer when the analyst flags that
   challenge type. Structurally marked as method-illustration and kept outside the analyst's
   source-truth path so the CERTAIN/PROBABLE/UNCERTAIN discipline stays intact — this is the fix for the
   Q2 contamination risk.
5. **Root v1.0 parity (only if the simple layer must match).** Root ships only `tier_1_transform.md` +
   `tier_3_transform.md` and has no cross-tier tool. To produce the T5 column and the coherent spine
   natively in root, add `tier_5_transform.md` (or a generic `tier_N_transform.md`) + a lightweight
   cross-tier reconciliation prompt mirroring the coordinator's three checks. Note: ADR-006 shipped only
   T1+T3 deliberately — this is a scope decision to revisit, not a bug.

**Bottom line:** the 0.1 pipeline is already most of the way there — with #1 and #2 it would produce
Stone-Table-quality output natively, and #3-#4 would eliminate the need to hand it a bespoke doc set at
all. The root v1.0 pipeline cannot reach this level without #5.

## Relevance to the prep-phase objective

The user story in `20-objective-user-story.md` asks for a **preparation phase** that produces this kind
of package natively and better-organized. Changes #3 (native mapping authoring) and #4 (exemplar
library) are the direct engine of that prep phase; #1 and #2 raise the quality ceiling of what the prep
phase can hand downstream. The prep phase is, in effect, "run analysis + research + mapping authoring +
challenge classification up front, then present it to the user for greenlight."
