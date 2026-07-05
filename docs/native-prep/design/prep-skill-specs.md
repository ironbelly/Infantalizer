---
title: "Prep-Phase Native Skill Specifications"
parent: DESIGN.md
status: draft
---

# Prep-Phase Native Skill Specifications

`SKILL.md` body outlines for the two new NATIVE skills: `prep` (the phase procedure) and
`thematic-fidelity` (the meaning-preservation concept). Both use the Claude-native skill dialect
(`name` + `description` only — `laf-adaptation/CLAUDE.md §3`, 0.1 `skill-specs.md §0`). Structure is
`SKILL.md` + optional `resources/`; **no `rules/` or `templates/` subdirs** (match the vendored
convention). Per the house convention for design specs, this file gives **full frontmatter + section
outlines/contracts**; full prose is authored by `/sc:implement`.

---

## 1. `/prep` — the phase procedure (R5, R3, R7, R11, R12)

**Directory:** `laf-adaptation/skills/prep/`  ·  **Resource:** `resources/path-contract.md` (R3, see
[`path-contract.md`](path-contract.md))

```yaml
---
name: prep
description: |
  The native adaptation-prep procedure: two-track work-level research + source-fidelity-gated analysis,
  challenge-taxonomy classification, derived confidence-scored work-mapping, a coverage-constrained
  question gate, greenlight, handoff, and traceability. Load when onboarding a new literary work via the
  prep-cordinator. Emits the fixed-path work/prep/<slug>/ package.
---
```

**Body (`SKILL.md`) — 8 sections:**

```markdown
# Adaptation Prep

Onboard a new work: research it, analyze its source (text-required), classify its adaptation challenges,
derive a scored work-mapping, ask only what needs human judgment, package it, greenlight it, hand off.

## §1 Path contract (single source of truth)
All output paths and the rewrite-phase read-set are defined ONCE in `resources/path-contract.md`. Import it
by reference; never restate a path literally in this skill, in a command, or in the agent body. (R3)

## §2 Challenge taxonomy
The typed challenge set, each with: `type`, `governing_rule` (the /adaptation-rules or tier-profile rule
that governs it), `per_tier_strategy` ({1,2,3,5}), `human_judgment_dimension` (bool — drives §5),
`compound_scene_eligible` (bool). The authoritative table + flag defaults are in
[`package-schemas.md §2`](package-schemas.md); classification writes `10-challenges.yaml`.

### §2.1 Compound-scene reconciliation protocol (R11)
When the analyst sets `compound_scene: true` (≥2 high-severity transformation_flags co-occur), apply the
reconciliation method, and BAKE the result into that challenge's entry in `10-challenges.yaml`:
  1. Find the emotional core (what the scene MUST make the reader feel).
  2. Decompose the surface into its co-occurring flagged elements.
  3. Convert / name / preserve each element by tier (per /adaptation-rules + the work mapping).
  4. Verify the meaning survived (/thematic-fidelity) — the reconciled rendering still means what the
     source scene means.
This protocol lives HERE (not inside adaptation-rules/resources/) so the adopted-sync boundary stays clean.

## §3 Two-track work-level analysis (anti-hallucination, R6)
Context track: dispatch web-researcher (secondary sources) → 00-work-context.md; ceiling PARTIAL/MEMORY.
Text track:   dispatch analyst (granularity=work; the novel text is a REQUIRED input, Q1) →
              20-analysis-work-level.yaml; apply /source-fidelity Phase-0 — NO-ACCESS ABORTS the prep.
Every mapping entry later carries text_confidence AND context_confidence; effective = min(text, context).
Because the text track is mandatory, MEMORY-BASED is never acceptable at work level.

## §4 Mapping authoring (derive + score, R12)
Derive 30-mapping.yaml from 20-analysis-work-level.yaml + 10-challenges.yaml, reusing the shipped
<work>_mapping schema (work_metadata, characters, concepts, key_scenes, master_translation_table —
ADDING_NEW_WORKS.md). ADD the top-level `meaning:` key (/thematic-fidelity). Every entry traces to a
confidence-tagged fact; entries derived from MEMORY-BASED/UNCERTAIN facts INHERIT that confidence
(min(text,context)). This turns the mapping from a hand-authored prerequisite into a scored pipeline output.
Schema + the dual-form promotion rule: [`package-schemas.md §4`](package-schemas.md).

## §5 Question-gate coverage rule (R7)
After §3-§4, emit `## Questions for the user` and HALT. The question set is CONSTRAINED by the taxonomy:
  MUST ask about every challenge whose governing rule has human_judgment_dimension: true
        (e.g. allegory stance, omission honor-set, target-age nuance, battle-scope, death honor).
  MUST NOT ask about deterministic rules (violence-level, death-euphemism).
Each question allows `[skip]` → recorded DEFAULTED in 70-traceability.md. Gate = prompt block + halt
(LangGraph-interrupt semantics; NO runtime).

## §6 Greenlight (R8)
Write 50-greenlight.md (checklist: source-access declared, mapping confidence ceiling acknowledged, tier
set confirmed, key decisions ratified). Emit a confirmation request; HALT until confirmed. Author the
mapping for ALL four tiers {1,2,3,5} by default (Q4); greenlight may narrow the active set. On confirm:
promote 30-mapping.yaml (dual-form) via /kb-management; set status PENDING → CONFIRMED.

## §7 Handoff (R9)
Write 60-handoff-prompt.md containing the literal paste-able text `/laf:rewrite --work <slug>`. The rewrite
command reads [30-mapping, 40-prep-brief, 10-challenges] by hardcoded path (path-contract §rewrite_phase_reads).

## §8 Traceability (R13)
Write 70-traceability.md: every artifact + every mapping entry → its derived-from facts, gap-closed, and
confidence. Consumer = HUMAN review + the greenlight decision only (Q2); the rewrite-phase muse does NOT
consume it (muse reads 30-mapping.yaml's inline per-entry confidence).
```

**Skill → consumer map:** `/prep` is loaded by `prep-cordinator` only. It references `/thematic-fidelity`
(§2.1, §4), `/source-fidelity` (§3), `/adaptation-rules` (§2, §4), and `/kb-management` (§6) — all already
in the coordinator's `skills:` list.

---

## 2. `/thematic-fidelity` — the meaning-preservation concept (R5, R10)

**Directory:** `laf-adaptation/skills/thematic-fidelity/`  ·  **Cross-phase:** attaches to
`prep-cordinator` (prep) and is *referenced by* the `tier-coordinator` body (rewrite, Check D).

```yaml
---
name: thematic-fidelity
description: |
  The meaning-preservation invariant for adaptation: a work's meaning (allegory, theme, moral center) is
  preserved under surface transformation — neither added where the source withholds it nor stripped where
  the source asserts it. Defines the analyst `meaning` field, the tier-coordinator Check D, and the
  DERIVED-marking rule for method exemplars. Load whenever authoring or reconciling tier renderings.
---
```

**Body (`SKILL.md`) outline:**

```markdown
# Thematic Fidelity

Principle (Hutcheon / Bortolotti): **meaning is preserved under surface transformation; the environment is
the target tier.** Source-fidelity guards the FACTS; thematic-fidelity guards the MEANING. A faithful
adaptation transforms the surface (names, violence, vocabulary) while carrying the same meaning at the
tier's altitude — and neither invents an allegory the source lacks nor deletes one it has.

## The `meaning` field (analyst output)
Every analyzed unit (work / chapter / scene) emits:
    meaning: {value: "<the theme/allegory beneath the surface>", confidence: CERTAIN|PROBABLE|UNCERTAIN}
Tagged like any source fact. At work level it is the top-level `meaning:` promoted with the mapping (D6);
the rewrite-phase muse reads it as data — no adopted-body edit.

## Check D (tier-coordinator, rewrite phase)
For each element shared across tiers, assert every tier's rendering preserves the work-level meaning:
status Meaning-PRESERVED | Meaning-DIFF. A Meaning-DIFF is a conflict that blocks chronicler (rides the
existing RECONCILED|CONFLICT gate). Agency Externalization is meaning-preserving ("external cause, not
innate evil"); silently dropping or inventing an allegory is Meaning-DIFF. (See prep-agent-schemas.md §4.)

## Exemplar DERIVED-marking rule (contamination safety, R13)
Method-illustration exemplars are NOT source truth. Every exemplar file MUST open with the structural
marker:
    <!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->
and MUST live OUTSIDE the source-truth path (work/, kb/canon/). This prevents a downstream agent from
presenting an exemplar as verified source (closes the Q2 contamination risk).

## Relationship to source-fidelity
source-fidelity: is this FACT true to the text? (CERTAIN/PROBABLE/UNCERTAIN)
thematic-fidelity: is this MEANING preserved under the transform? (Meaning-PRESERVED/DIFF)
Both are required; neither substitutes for the other.
```

**Boundary note.** `thematic-fidelity` is a **standalone NATIVE skill**, not an edit to adopted
`writing-principles` — bolting meaning-preservation onto an adopted skill would break the boundary
contract. It rides in a native skill, loaded by the (native) `prep-cordinator` and read as data by the
(build-new) `tier-coordinator`.
