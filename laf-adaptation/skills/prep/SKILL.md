---
name: prep
description: |
  The native adaptation-prep procedure: two-track work-level research + source-fidelity-gated analysis,
  challenge-taxonomy classification, derived confidence-scored work-mapping, a coverage-constrained
  question gate, greenlight, handoff, and traceability. Load when onboarding a new literary work via the
  prep-cordinator. Emits the fixed-path work/prep/<slug>/ package.
---

# Adaptation Prep

Onboard a new work: research it, analyze its source (text-required), classify its adaptation challenges,
derive a scored work-mapping, ask only what needs human judgment, package it, greenlight it, hand off.

## §1 Path contract (single source of truth)

All output paths and the rewrite-phase read-set are defined ONCE in `resources/path-contract.md`. Import it
by reference; never restate a path literally in this skill, in a command, or in the agent body. The package
lives at `work/prep/<work-slug>/` and contains the 8 fixed-name files `00`–`70` defined there.

> **Stage 0 note.** A new **Stage 0: Source Materialization** (owned by `prep-cordinator`, procedure in
> `laf-adaptation:chapter-materialize`) precedes the §3 two-track analysis: it materializes the canonical
> `source/<slug>/ch-<NN>.txt` set from a folder / monolith / adopt-set and emits a confidence-tagged
> `source/<slug>/chapter-manifest.yaml`. The manifest is a `source/` **sidecar** — NOT a 9th package file
> and NOT a `rewrite_phase_reads` member (the 8 fixed-name `00`–`70` files above are unchanged). Non-CERTAIN
> splits route to the existing §5 question gate and §6 greenlight; no new gate is added.

## §2 Challenge taxonomy

The typed challenge set, each with: `type`, `governing_rule` (the `/adaptation-rules` or tier-profile rule
that governs it), `per_tier_strategy` (for tiers {1,2,3,5}), `human_judgment_dimension` (bool — drives §5),
and `compound_scene_eligible` (bool). Classification writes `10-challenges.yaml`.

Confirmed `human_judgment_dimension` defaults — the gate asks iff `true`:

| Challenge type | `human_judgment_dimension` | Rationale |
|---|---|---|
| `sacrifice-and-return` (death honor) | true | how much of the death to imply is an authorial-taste call |
| allegory-stance | true | "neither add nor strip the allegory" is a stance decision |
| omission-honor-set | true | what must be omitted vs preserved is judgment |
| target-age-nuance | true | precise age band within a tier shifts many calls |
| mass-warfare / battle-scope | true | how much battle to show is judgment |
| petrification-body-horror | true | reframe vs restore is a taste threshold |
| psychological-collapse | true | how much despair to imply |
| violence-level | false | deterministic tier-profile threshold |
| death-euphemism | false | deterministic (`journey_or_sleep` at T1) |

### §2.1 Compound-scene reconciliation protocol

When the analyst sets `compound_scene: true` (≥2 high-severity `transformation_flags` co-occur in one scene),
apply this reconciliation method and BAKE the result into that challenge's entry in `10-challenges.yaml`:

1. Find the emotional core (what the scene MUST make the reader feel).
2. Decompose the surface into its co-occurring flagged elements.
3. Convert / name / preserve each element by tier (per `/adaptation-rules` + the work mapping).
4. Verify the meaning survived (`/thematic-fidelity`) — the reconciled rendering still means what the source
   scene means.

This protocol lives HERE (not inside `adaptation-rules/resources/`) so the adopted-sync boundary stays clean.

## §3 Two-track work-level analysis (anti-hallucination)

- **Context track:** dispatch `web-researcher` (secondary sources) → `00-work-context.md`; ceiling
  PARTIAL/MEMORY.
- **Text track:** dispatch `analyst` (granularity=work; the novel text is a REQUIRED input) →
  `20-analysis-work-level.yaml`; apply `/source-fidelity` Phase-0 — **NO-ACCESS ABORTS the prep**.

Every mapping entry later carries `text_confidence` AND `context_confidence`; effective = `min(text, context)`.
Because the text track is mandatory, MEMORY-BASED is never acceptable at work level.

## §4 Mapping authoring (derive + score)

Derive `30-mapping.yaml` from `20-analysis-work-level.yaml` + `10-challenges.yaml`, reusing the shipped
`<work>_mapping` schema (`work_metadata`, `characters`, `concepts`, `key_scenes`, `master_translation_table`)
and ADD the top-level `meaning:` key (`/thematic-fidelity`). Every entry traces to a confidence-tagged fact;
entries derived from MEMORY-BASED/UNCERTAIN facts INHERIT that confidence (`min(text, context)`). This turns
the mapping from a hand-authored prerequisite into a scored pipeline output.

The 6-key form (with `meaning:`) is what lives at `work/prep/<slug>/30-mapping.yaml`. On greenlight it is
promoted in dual form (see §6 and the path contract §3): a 6-key hyphen copy that keeps `meaning:` and a
5-key underscore copy that strips it.

## §5 Question-gate coverage rule

After §3–§4, emit `## Questions for the user` and HALT. The question set is CONSTRAINED by the taxonomy:

- MUST ask about every challenge whose governing rule has `human_judgment_dimension: true` (e.g. allegory
  stance, omission honor-set, target-age nuance, battle-scope, death honor).
- MUST NOT ask about deterministic rules (violence-level, death-euphemism).

Each question allows `[skip]` → recorded DEFAULTED in `70-traceability.md`. The gate = a prompt block + halt
(interrupt semantics; no runtime).

## §6 Greenlight

Write `50-greenlight.md` (checklist: source-access declared, mapping confidence ceiling acknowledged, tier
set confirmed, key decisions ratified). Emit a confirmation request; HALT until confirmed. Author the
mapping for ALL four tiers {1,2,3,5} by default; greenlight may narrow the active set.

On confirm: **the `prep-cordinator` itself performs the §3 dual-form transform on `30-mapping.yaml`
(writing both promotion targets) and registers the kb copy via `/kb-management`**; set status
`PENDING → CONFIRMED`. The two promotion targets named in the path contract §3 are:

- `laf-adaptation/kb/adaptation-mapping/<slug>-mapping.yaml` (0.1, hyphen, 6-key, `meaning:` KEPT), and
- `config/concept_mapping/templates/<slug>_mapping.yaml` (root, underscore, 5-key, `meaning:` STRIPPED).

This is the only step that produces those two files; nothing hand-authors them.

**Operator clarity (mechanism).** The `prep-cordinator` itself owns the dual-form transform —
`/kb-management` does NOT. The coordinator reads the transform rule from `resources/path-contract.md` §3
(the two targets, the `meaning:` strip for the root 5-key underscore copy, the `_confidence` strip for
it, the hyphen-vs-underscore naming), derives both target files from `30-mapping.yaml`, and writes each
target with its own `Write` tool. The `/kb-management` invocation is for the kb-lifecycle write (the
registry acceptance of the promoted mapping); its body has no awareness of the dual form. The coordinator
is the transform operator; `/kb-management` is the kb-lifecycle write.

## §7 Handoff

Write `60-handoff-prompt.md` containing the literal paste-able text `/laf:rewrite --work <slug>`. The rewrite
command reads `[30-mapping, 40-prep-brief, 10-challenges]` by hardcoded path (path-contract §4
`rewrite_phase_reads`).

## §8 Traceability

Write `70-traceability.md`: every artifact + every mapping entry → its derived-from facts, gap-closed, and
confidence. Consumer = HUMAN review + the greenlight decision only; the rewrite-phase `muse` does NOT consume
it (`muse` reads `30-mapping.yaml`'s inline per-entry confidence).

## Resources

- `resources/path-contract.md` — the single source of truth for the package layout, promotion targets,
  rewrite-phase read-set, and write-ownership.
- `laf-adaptation:chapter-materialize` — the Stage-0 boundary-detection + normalization procedure that
  materializes `source/<slug>/ch-<NN>.txt` + the `chapter-manifest.yaml` sidecar (dispatched inline by
  `prep-cordinator` before §3).
