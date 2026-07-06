# Research: Native Agents + Skills (authorable content)
**Topic type:** Patterns & Conventions / Content Extraction
**Scope:** analyst, safety-verifier, /adaptation-tiers, /adaptation-rules, /source-fidelity, writer patch, reader-sim
**Status:** Complete
**Date:** 2026-07-03
---

## Summary

Content-per-file map for the 5 NATIVE files + 2 adopted-touch files this track owns. Each has a
self-contained builder checklist with verbatim frontmatter, body outlines/protocols, and hard-behavior
blocks. All claims cite agent-schemas.md / skill-specs.md line numbers.

**Files & authoring effort:**
| # | File | Provenance | Effort | Key content |
|---|---|---|---|---|
| 1 | `agents/analyst.md` | NATIVE (opus) | authored | frontmatter (story-memory prefix-rewrite); Phase-0 ABORT hard block; inputs source_path/work/chapter (NO active_tier); out `work/analysis/ch-NN.yaml` |
| 2 | `agents/safety-verifier.md` | NATIVE (sonnet) | authored | frontmatter; tier-gate (T1-2 blocking / T3 advisory / T4-5 N/A); verdict-block out; Write-only-to-safety-reports |
| 3 | `skills/adaptation-tiers/SKILL.md` + `resources/tier_1..5.md` | NATIVE | authored | frontmatter + 4-section body verbatim; 5 rationale resources (design_decisions 001 & 003); reads kb/tiers YAML (R4) |
| 4 | `skills/adaptation-rules/SKILL.md` + `resources/{thematic,character,agency}.md` | NATIVE | authored | frontmatter + body verbatim; 3 resources WRAP R4 config YAML; agency.md carries ADR-003 rationale |
| 5 | `skills/source-fidelity/SKILL.md` | NATIVE | authored | frontmatter + 5-phase protocol verbatim; §3.2 output YAML schema; story-memory tag-propagation |
| 6 | `agents/writer.md` | ADOPTED-PATCHED | vendor step | prefix-rewrite + single additive line `- laf-adaptation:adaptation-rules`; body untouched; preserve duplicate craft line; 2 hashes |
| 7 | `agents/reader-sim.md` | ADOPTED-CLEAN | no edit | byte-identical; persona `developmental_basis` is runtime DATA, not a file change |

**Boundary notes for builder:**
- Native-agent story-memory line is prefix-rewritten to `laf-adaptation:story-memory` at vendor time (analyst).
- analyst does NOT receive `active_tier` (tier-invariant); safety-verifier DOES (it gates on it).
- Files 6 & 7 are vendor/no-edit steps, not authoring — coordinate with R1 (inventory), R5 (VENDOR.md/check_boundary.py).

**Cross-track handoffs (NOT owned here):** `/adaptation-safety` skill + safety-rubric = R3; tier YAML +
adaptation-mapping port-source = R4; check_boundary.py + VENDOR.md classification = R5. This track documents
what the native files READ from those, not their content.

## Dialect contract (applies to ALL files below)

**Agent frontmatter** (agent-schemas.md:22-30) — closed permitted-key set: `name` (=filename stem),
`description` (one-line), `model` (Claude aliases ONLY: `opus`/`sonnet`/`haiku`/`inherit` — never
`opus46`/`gpt`/`deepseek`), `skills` (list of `laf-adaptation:<name>` fully-qualified), `tools`
(comma-separated Claude tool names). Mars keys (`model-policies`, `sandbox`, `effort`, `subagents`,
`approval`, `mode`) are FORBIDDEN — Claude Code does not read them (agent-schemas.md:18-20).

**Skill frontmatter** (skill-specs.md:19-25) — Claude-native: ONLY `name` + `description` (multi-line
`|` block). Mars keys (`type`, `model-invocable`, `effort`) FORBIDDEN (skill-specs.md:16-18). Structure =
`SKILL.md` + optional `resources/`. NO `rules/` or `templates/` subdirs — they don't exist in CWS
(skill-specs.md:27-29).

---

## FILE 1 — `agents/analyst.md` (NATIVE)

**Provenance:** NATIVE, fully specified. `model: opus`. (agent-schemas.md:42-77)

**Exact frontmatter YAML (verbatim, agent-schemas.md:50-61):**
```yaml
---
name: analyst
description: Source-chapter analysis for literary adaptation. Runs before the muse as the pre-orchestration phase; produces confidence-tagged (CERTAIN/PROBABLE/UNCERTAIN) structural facts and transformation flags. ABORTS on NO-ACCESS.
model: opus
skills:
  - laf-adaptation:source-fidelity
  - laf-adaptation:adaptation-tiers
  - creative-writing-skills:story-memory   # rewritten to laf-adaptation:story-memory at vendor time
tools: Read, Write, Glob, Grep
---
```
> **story-memory prefix rewrite note** (agent-schemas.md:58): the `creative-writing-skills:story-memory`
> entry is rewritten to `laf-adaptation:story-memory` at vendor time (the uniform prefix-rewrite transform,
> agent-schemas.md:32-36). The authored native file may show it either way per the vendor step; the comment
> documents the rewrite. Final vendored form = `laf-adaptation:story-memory`.

**Inputs (passed by caller, agent-schemas.md:63-64):** `source_path` (a `source/<work>/ch-<NN>.txt`),
`work`, `chapter`. **`active_tier` is NOT an input** — analysis is tier-invariant (Q1.5).

**Output contract (agent-schemas.md:66-69):** writes `work/analysis/ch-<NN>.yaml` conforming to the v2.0
schema in skill-specs.md §3.2 (see FILE 5 below). Body loads `/source-fidelity` and executes its 5-phase
procedure.

**Hard-behavior block — verbatim in agent BODY, not a skill (agent-schemas.md:71-77):**
```
Phase 0 — Source Declaration:
  Determine SOURCE ACCESS LEVEL ∈ {FULL, PARTIAL, MEMORY-BASED, NO-ACCESS}.
  IF NO-ACCESS:  emit `status: ABORTED` to work/analysis/ch-NN.yaml and HALT. Do not proceed.  ← constraint #2
  IF MEMORY-BASED: every emitted fact MUST carry confidence: UNCERTAIN.
```

**Builder checklist for this file:** create `agents/analyst.md` with the frontmatter block above (apply
story-memory prefix rewrite to `laf-adaptation:story-memory`); body must (a) contain the Phase-0 ABORT
hard-behavior block verbatim, (b) instruct loading `/source-fidelity` and executing its 5 phases, (c)
declare inputs source_path/work/chapter and NOT active_tier, (d) declare output `work/analysis/ch-NN.yaml`.

---

## FILE 2 — `agents/safety-verifier.md` (NATIVE)

**Provenance:** NATIVE, fully specified. `model: sonnet`. The DISTINCT fifth review agent (constraint #4:
never a critic focus, never a continuity mode). Runs AFTER continuity-checker (step 8). (agent-schemas.md:79-122)

**Exact frontmatter YAML (verbatim, agent-schemas.md:87-97):**
```yaml
---
name: safety-verifier
description: Post-generation safety gate for Tier 1-2 children's adaptations. Runs the 6-section safety rubric and emits a PASS/FAIL verdict. A FAIL blocks kb promotion and re-enters the writer revision loop. Read-only.
model: sonnet
skills:
  - laf-adaptation:adaptation-safety
  - laf-adaptation:adaptation-tiers
tools: Read, Write, Glob, Grep
---
```
> `/adaptation-safety` skill + its safety-rubric are owned by R3 (build-new). This file only LOADS it.

**Inputs (passed by caller, agent-schemas.md:99-100):** `draft_path` (a `work/drafts/ch-NN-t<N>-v<M>.md`),
`active_tier`, `work`, `chapter`. NOTE: unlike analyst, safety-verifier RECEIVES `active_tier` (it gates on it).

**Tier gate — verbatim in agent BODY (agent-schemas.md:102-107):**
```
IF active_tier ∈ {1, 2}:  run the full 6-section rubric — verdict is MANDATORY and blocking.
IF active_tier == 3:      run rubric in ADVISORY mode (report only; does not block).
IF active_tier ∈ {4, 5}:  SKIP — emit verdict: N/A (safety_check does not apply). ← ground-truth: safety_check.md is T1-2 only
```

**Output contract (agent-schemas.md:109-119):** writes `work/safety-reports/ch-<NN>-t<N>.md` ending in a
machine-parseable verdict block (full contract in safety-rubric.md §4 — owned by R3):
```yaml
verdict:
  result: PASS | FAIL | N/A
  tier: <N>
  sections: { forbidden_content: PASS, agency_externalization: PASS, emotional_safety: PASS,
              safe_home: PASS, nightmare_prevention: PASS, linguistic: PASS }
  automatic_failures: []          # non-empty ⇒ result: FAIL regardless of sections
  next: promote | revise          # revise ⇒ caller returns to workflow step 3
```

**Write-only constraint (agent-schemas.md:121-122):** the `Write` tool is granted ONLY to emit the report
to `work/safety-reports/`. The agent NEVER edits a draft (it is a reviewer, not a writer).

**Builder checklist for this file:** create `agents/safety-verifier.md` with the frontmatter above; body
must (a) contain the tier-gate block verbatim (T1-2 full+blocking / T3 advisory / T4-5 SKIP N/A), (b)
declare inputs draft_path/active_tier/work/chapter, (c) declare output `work/safety-reports/ch-NN-t<N>.md`
with the verdict-block schema, (d) state Write-only-to-safety-reports / never-edit-draft constraint.

---

## FILE 3 — `skills/adaptation-tiers/SKILL.md` (NATIVE)

**Provenance:** NATIVE skill. Directory `skills/adaptation-tiers/`. The tier axis (constraint #1).
Loaded by: analyst, chronicler, safety-verifier, tier-coordinator (skill-specs.md:33-45, 293).

**Exact frontmatter YAML (verbatim, skill-specs.md:37-45):**
```yaml
---
name: adaptation-tiers
description: |
  The five-tier developmental adaptation axis (Piaget/Kohlberg grounded). Load whenever choosing or
  applying tier-appropriate constraints: vocabulary, sentence limits, permitted violence/emotion/moral
  ambiguity, and the transformation-mode ladder. Tier 4 is interpolated from tiers 3 and 5.
---
```

**Body outline — verbatim (skill-specs.md:49-78):** SKILL.md body has 4 sections. Author verbatim:
```markdown
# Adaptation Tiers

One axis, five tiers, grounded in developmental psychology. The active tier is always passed as an
explicit `active_tier` parameter — never inferred from genre or persona.

| Tier | Ages | Piaget | Kohlberg | Paradigm |
|------|------|--------|----------|----------|
| 1 | 3-5   | preoperational          | 1 | Maximum transformation, maximum safety |
| 2 | 6-8   | early concrete operational | 2 | Conflict as contest/competition |
| 3 | 9-11  | concrete operational    | 3 | TRANSITION — complexity unlocked |
| 4 | 12-14 | early formal (interpolated) | 4 | Interpolated from T3+T5 (see §Interpolation) |
| 5 | 15-17 | formal operational      | 5 | Minimal transformation — preserve author intent |

## Loading a tier profile
Read `kb/tiers/tier_<N>.yaml` for the full profile (thresholds, linguistic limits, transformation_rules).
The profile is the authoritative per-tier constraint set. See `resources/tier_<N>.md` for the design
commentary on WHY each threshold is set where it is.

## The transformation-mode ladder (cross-cutting)
Every transformation rule uses a per-tier `mode:` enum. The Agency-Externalization ladder is the
signature case: MANDATORY (T1-2) → OPTIONAL (T3) → FORBIDDEN (T4-5). Full rules live in
`/adaptation-rules`; this skill only supplies the tier definitions they key against.

## Interpolation (Tier 4)
Tier 4 has no stored profile. Interpolate at request time: take T3's permitted set as the floor and T5's
as the ceiling; for each threshold, choose the value at the T3→T5 midpoint, rounding toward the more
conservative (lower) bound when ambiguous. `agency_externalization` at T4 = FORBIDDEN (inherits the T4_5
bucket). Emit interpolated T4 constraints as a derived profile; never persist them as a stored tier file.
```

**`resources/tier_1.md` … `tier_5.md` (5 files) — commentary sourcing (skill-specs.md:80-83):** design
commentary carried from `docs/design_decisions/001-five-tier-system.md` and `003-agency-externalization.md`.
Content = the *rationale* (e.g. "externalization prevents self-blame per Piagetian egocentrism"), NOT the
data. The DATA lives in `kb/tiers/*.yaml` (R4 owns YAML; kb-formats.md §2). Skill resources hold reasoning.

**Builder checklist:** create `skills/adaptation-tiers/SKILL.md` (frontmatter + 4-section body verbatim) +
`skills/adaptation-tiers/resources/tier_1.md`..`tier_5.md` (rationale from design_decisions 001 & 003).
The skill READS `kb/tiers/tier_<N>.yaml` at runtime but does NOT contain that YAML (that's R4's data).

---

## FILE 4 — `skills/adaptation-rules/SKILL.md` (NATIVE)

**Provenance:** NATIVE skill. Directory `skills/adaptation-rules/`. Grafted onto adopted `writer`
(frontmatter line) + adopted `critic` (situational, via muse dispatch brief). Where LAF's
`config/transformation_rules/` lands. (skill-specs.md:87-160, 294)

**Exact frontmatter YAML (verbatim, skill-specs.md:92-100):**
```yaml
---
name: adaptation-rules
description: |
  Thematic and character transformation rules for literary adaptation, keyed by tier. Covers violence,
  conflict, death, villain motivation, heroism, and character-archetype mapping. Includes Agency
  Externalization (the signature rule). Load when writing or critiquing an adaptation draft.
---
```

**Body outline — verbatim (skill-specs.md:104-126):**
```markdown
# Adaptation Rules

Transform source content to the active tier using these rules. Every rule is keyed by tier and carries a
`mode:` value. Read the active tier's row; apply MANDATORY rules, honor OPTIONAL ones per editorial
judgment, and never apply FORBIDDEN ones.

Resources:
- `resources/thematic.md`  — violence, conflict, death, villain, heroism (carried from thematic.yaml)
- `resources/character.md` — archetype mapping + heroism-translation subroutine (carried from character.yaml)
- `resources/agency.md`    — Agency Externalization, the signature rule (§2.3)

## Applying a rule
1. Identify the source element's category (violence | conflict | death | villain | heroism | character).
2. Look up `<category>.tier_<N>.mode`.
3. Apply the tier's `translations`/`target`/`strategy` for that category.
4. For characters, run the heroism-translation subroutine (§character): IDENTIFY intent → LOOKUP
   tier-appropriate expression → TRANSLATE action preserving intent.

## Cascade with work mappings
Work-specific overrides in `kb/adaptation-mapping/<work>-mapping.yaml` take precedence over these
universal rules (most-specific-wins). See `/source-fidelity` and kb-formats for the cascade order.
```

**resources/ — 3 files. These WRAP config YAML VERBATIM (R4 owns the YAML content; you own the wrapper structure):**

- **`resources/thematic.md`** (skill-specs.md:128-133): wraps `config/transformation_rules/thematic.yaml`
  in a fenced block, unchanged. Six rule groups: `violence_transformation`, `conflict_transformation`,
  `agency_externalization`, `death_handling`, `villain_motivation`, `heroism_definition` — each with
  `tier_1/2/3/tier_4_5` buckets and `mode:` enums. No key renamed.
- **`resources/character.md`** (skill-specs.md:135-141): wraps `config/transformation_rules/character.yaml`:
  `archetype_system`, `tier_1_archetypes`, `tier_2_additions` (rival), `tier_3_unlocks`
  (hero_with_flaws / complex_villain / morally_ambiguous), `tier_4_5.approach: preserve_original`, the
  `heroism_translation.subroutine` (literal 3-step IDENTIFY/LOOKUP/TRANSLATE algorithm — ported as an
  executable procedure), and `special_handling` (per-character overrides, e.g. gollum, denethor).
- **`resources/agency.md`** — Agency Externalization / ADR-003 (skill-specs.md:143-160): carried verbatim
  from `thematic.yaml → agency_externalization` PLUS ADR-003 rationale. Sample YAML shape (skill-specs.md:148-155):
  ```yaml
  agency_externalization:
    core_principle: "Badness is always a STATE or ACCIDENT, never innate."
    tier_1: {mode: mandatory, examples: [{source: "Dark Lord, evil", target: "Grumpy King, no sunshine"}, …]}
    tier_2: {mode: mandatory, softening: "permits_misunderstanding_as_cause"}
    tier_3: {mode: optional}
    tier_4_5: {mode: forbidden}   # "Patronizing; undermines character complexity" (tier_5 profile)
  ```
  **ADR-003 rationale you must include (skill-specs.md:157-160):** it lives in native `/adaptation-rules`,
  NOT bolted onto adopted `writing-principles`, because grafting native content onto an adopted skill would
  break the boundary contract (adopted files stay patch-clean). It rides in the native skill, loaded
  additively by adopted writer/critic. Enforced by `writer` (applies), audited by `safety-verifier`
  (rubric Section 2) and `critic` (adaptation-quality focus).

**Builder checklist:** create `skills/adaptation-rules/SKILL.md` (frontmatter + body verbatim) +
`resources/thematic.md`, `resources/character.md`, `resources/agency.md`. The three resource files are
verbatim YAML wrappers around R4-supplied config YAML; agency.md additionally carries the ADR-003 prose
rationale. You author the wrapper structure + fences + agency rationale; R4 supplies the YAML payload.

---

## FILE 5 — `skills/source-fidelity/SKILL.md` (NATIVE)

**Provenance:** NATIVE skill. Directory `skills/source-fidelity/`. Owned by native `analyst` (also loaded
by build-new tier-coordinator). Carries `prompts/analysis/chapter_analysis.md`. v2.0 Pragmatic
Verification Protocol (constraint #2). (skill-specs.md:164-247, 295)

**Exact frontmatter YAML (verbatim, skill-specs.md:169-178):**
```yaml
---
name: source-fidelity
description: |
  The v2.0 anti-hallucination protocol for source analysis. Mandates CERTAIN/PROBABLE/UNCERTAIN
  confidence tags on every extracted fact, a source-access declaration with ABORT-on-NO-ACCESS, and a
  dual-pass documentation procedure. Load before any source transform. Transparent uncertainty > false
  certainty.
---
```

**Body — the 5-phase protocol, VERBATIM (skill-specs.md:182-212):**
```markdown
# Source Fidelity — v2.0 Pragmatic Verification Protocol

Principle: **Transparent uncertainty > false certainty.** Every fact you extract carries a confidence tag.

## Confidence tags
| Tag | Meaning |
|-----|---------|
| CERTAIN   | Directly quoted from text |
| PROBABLE  | Multiple observations support |
| UNCERTAIN | Inferred or reconstructed |

## Phase 0 — Source Declaration
Declare SOURCE ACCESS LEVEL (exactly one):
  FULL ACCESS · PARTIAL ACCESS · MEMORY-BASED · NO ACCESS
- MEMORY-BASED ⇒ every output item MUST be tagged UNCERTAIN.
- NO ACCESS   ⇒ ABORT. Do not produce analysis.        ← constraint #2 hard gate

## Phase 1 — Essential Verification
Title, chapter number, chapter title (each: value + confidence). Opening & closing sentence + confidence.

## Phase 2 — Dual-Pass Documentation
PASS ONE (structure/events): major characters (role + confidence); 5-10 sequential events (+ confidence).
PASS TWO (summary): 100-150 word summary with overall confidence.

## Phase 3 — Transformation Flags
Flag categories present: violence, death, emotional intensity, abstraction — each with instances + severity.

## Phase 4 — Consistency Check
Characters logical · timeline coherent · locations consistent.
```

**Output schema §3.2 — `work/analysis/ch-<NN>.yaml`, VERBATIM (skill-specs.md:219-243):** the `analyst`
emits this (carried from chapter_analysis.md's YAML output block, extended with `status` for the ABORT gate):
```yaml
status: OK | ABORTED            # ABORTED ⇒ NO-ACCESS; downstream halts
metadata:
  work: <work>
  chapter: <NN>
  source_access: FULL | PARTIAL | MEMORY-BASED | NO-ACCESS
  confidence: CERTAIN | PROBABLE | UNCERTAIN     # overall
essentials:
  title:   {value: "...", confidence: CERTAIN}
  chapter_title: {value: "...", confidence: PROBABLE}
  opening_sentence: {value: "...", confidence: CERTAIN}
  closing_sentence: {value: "...", confidence: CERTAIN}
characters:
  - {name: "...", role: "...", confidence: CERTAIN}
events:
  - {seq: 1, event: "...", confidence: CERTAIN}
summary: {text: "...", confidence: PROBABLE}
transformation_flags:
  violence:  {instances: N, severity: low|med|high}
  death:     {instances: N, severity: low|med|high}
  emotional: {instances: N, severity: low|med|high}
  abstract:  {instances: N, severity: low|med|high}
uncertainties:
  - "list of items the analyst could not verify"
```

**Tag-propagation note (skill-specs.md:245-247):** the CERTAIN/PROBABLE/UNCERTAIN tags flow downstream
through the *adopted* `story-memory` fact-extraction carrier (native tag, adopted carrier) — NO edit to
`story-memory`; the tags are just data in the facts it extracts.

**Builder checklist:** create `skills/source-fidelity/SKILL.md` (frontmatter + 5-phase body verbatim). The
§3.2 output YAML schema is the CONTRACT the analyst agent emits — document it in the skill (or analyst body)
so both agree. No `resources/` subdir specified for this skill.

---

## FILE 6 — `agents/writer.md` (ADOPTED-PATCHED, frontmatter-only)

**Provenance:** ADOPTED-PATCHED. The canonical demonstration of constraint #6: native knowledge enters an
adopted agent ONLY as a loadable skill. **The body is NOT touched.** (agent-schemas.md:126-184)

**Two mechanical vendor-time transforms, both recorded in VENDOR.md (agent-schemas.md:152-156):**
1. **Prefix rewrite** (uniform, applies to every adopted file): `creative-writing-skills:` → `laf-adaptation:`.
2. **Adaptation-mode graft — THE SINGLE ADDITIVE LINE:** append `- laf-adaptation:adaptation-rules`.

**Upstream baseline** (CWS `cw/agents/writer.md`, verified 2026-07-03, agent-schemas.md:136-150) — NOTE the
upstream file already lists `creative-writing-craft` TWICE; that duplication is PRESERVED VERBATIM, not
"fixed", to keep the file patch-clean (agent-schemas.md:132-134).

**LAF vendored form — verbatim (agent-schemas.md:157-172):**
```yaml
---
name: writer
description: Production prose from scene briefs, revision notes, and style references; uses progressive mode guidance for fresh drafts, revisions, bridges, alternate takes, and line polish.
model: opus
skills:
  - laf-adaptation:creative-writing-modes
  - laf-adaptation:creative-writing-craft
  - laf-adaptation:creative-writing-craft
  - laf-adaptation:writing-principles
  - laf-adaptation:llm-writing
  - laf-adaptation:story-memory
  - laf-adaptation:adaptation-rules        # ← the ONLY LAF-added line; body untouched
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

**Boundary-contract classification (agent-schemas.md:174-178):** `ADOPTED-PATCHED` in VENDOR.md — stores
TWO hashes: `upstream_sha256` (original cw file) and `laf_sha256` (vendored-with-graft file).
`check_boundary.py` (R5) asserts vendored file matches `laf_sha256` AND the diff from upstream is
**frontmatter-only and additive** (boundary-contract.md §3.2). Any body byte-change FAILS the gate.

**Mode activation — no body logic (agent-schemas.md:180-184):** when muse dispatches writer on adapt path,
the scene brief carries `active_tier` + "adaptation mode." Presence of `/adaptation-rules` in context
(loaded via the frontmatter entry) supplies transform rules; writer's existing body already routes on the
brief. The tier-conditional `mode:` ladder lives in the SKILL, not the agent.

**Builder checklist:** this is a VENDOR step, not authoring. Take upstream `cw/agents/writer.md`, apply
(1) prefix rewrite to all 6 existing skill lines, (2) append the single line `- laf-adaptation:adaptation-rules`.
Preserve the duplicate `creative-writing-craft` line. Body byte-identical to upstream. Record BOTH hashes
in VENDOR.md as ADOPTED-PATCHED (R5 owns VENDOR.md + check_boundary.py). Coordinate with R1 (inventory) /R5.

---

## FILE 7 — `agents/reader-sim.md` (ADOPTED-CLEAN, no file edit — persona is DATA)

**Provenance:** ADOPTED-CLEAN. Body verified = just `Use /reader-sim.` — it already accepts a
caller-specified reader persona. LAF supplies the persona as structured DATA at dispatch time; ZERO change
to the agent file OR the reader-sim skill. (agent-schemas.md:188-207)

**Persona-as-data payload — constructed by muse/tier-coordinator from `kb/tiers/tier_N.yaml`
(verbatim, agent-schemas.md:196-204):**
```yaml
persona:
  label: "Tier 1 reader (ages 3-5)"
  developmental_basis:
    piaget_stage: preoperational
    kohlberg_stage: 1
  knowledge_boundary: "Has read tier-1 chapters 1..N-1 only (per kb/adaptations/<work>/tier-1/continuity.md)"
  felt_experience_focus: ["Is it scary? (must not be)", "Does the ending feel safe?", "Is anyone 'bad'? (should read as grumpy/silly)"]
```

**Classification (agent-schemas.md:206-207):** `reader-sim.md` stays **byte-identical** to upstream =
`ADOPTED-CLEAN` in VENDOR.md. The persona is a RUNTIME ARGUMENT, not a code path. The `developmental_basis`
sub-block is the tier-derived payload.

**Builder checklist:** NO file authoring for reader-sim itself — vendor it byte-identical (ADOPTED-CLEAN,
single upstream hash, R5). The persona payload above is DATA emitted by the dispatcher (muse/tier-coordinator,
R3) at runtime; document it as the contract but do NOT edit reader-sim.md or the reader-sim skill.

---
