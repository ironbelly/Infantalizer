---
title: "Native Skill Specifications — LAF 0.1"
parent: DESIGN.md
status: draft
---

# Native Skill Specifications

`SKILL.md` bodies for the four native skills plus the build-new `/adaptation-safety` skill (its rubric is
in [`safety-rubric.md`](safety-rubric.md); its genre resources are here). All native skills carry the LAF
domain theory ported **verbatim** from `config/` and `prompts/` (zero rework — ADR-006: this is a prompt +
config framework, not software).

## 0. Skill dialect contract

Native skills use the **Claude-native** frontmatter dialect (ground-truth: adopted `cw/skills/*/SKILL.md`
carry only `name` + `description`). Mars keys (`type`, `model-invocable`, `effort`) are **not** used.

```yaml
---
name: <skill-name>
description: |
  <one to three sentences; states WHAT the skill provides and WHEN to load it>
---
```

Structure: `SKILL.md` + optional `resources/` subdirectory. **No `rules/` or `templates/` subdirs** (they
don't exist in CWS; we match the vendored convention). The tier-conditional rule data lives as YAML
*inside* `resources/` markdown fences, carried verbatim from `config/`.

---

## 1. `/adaptation-tiers` — the tier axis (constraint #1)

**Directory:** `skills/adaptation-tiers/`

```yaml
---
name: adaptation-tiers
description: |
  The five-tier developmental adaptation axis (Piaget/Kohlberg grounded). Load whenever choosing or
  applying tier-appropriate constraints: vocabulary, sentence limits, permitted violence/emotion/moral
  ambiguity, and the transformation-mode ladder. Tier 4 is interpolated from tiers 3 and 5.
---
```

**Body (`SKILL.md`) outline:**

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

**`resources/tier_1.md` … `tier_5.md`:** design commentary carried from
`docs/design_decisions/001-five-tier-system.md` and `003-agency-externalization.md` — the *rationale*
(e.g. "externalization prevents self-blame per Piagetian egocentrism"). The *data* lives in
`kb/tiers/*.yaml` ([`kb-formats.md §2`](kb-formats.md)); the skill's resources hold the reasoning.

---

## 2. `/adaptation-rules` — thematic + character transforms + Agency Externalization

**Directory:** `skills/adaptation-rules/`. This is the skill grafted onto adopted `writer` and adopted
`critic` (adaptation-quality focus). It is where LAF's `config/transformation_rules/` lands.

```yaml
---
name: adaptation-rules
description: |
  Thematic and character transformation rules for literary adaptation, keyed by tier. Covers violence,
  conflict, death, villain motivation, heroism, and character-archetype mapping. Includes Agency
  Externalization (the signature rule). Load when writing or critiquing an adaptation draft.
---
```

**Body outline:**

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

### 2.1 `resources/thematic.md` — carried verbatim

Wraps `config/transformation_rules/thematic.yaml` in a fenced block, unchanged. The six rule groups
(`violence_transformation`, `conflict_transformation`, `agency_externalization`, `death_handling`,
`villain_motivation`, `heroism_definition`), each with `tier_1/2/3/tier_4_5` buckets and `mode:` enums,
port exactly as-is. No key is renamed.

### 2.2 `resources/character.md` — carried verbatim

Wraps `config/transformation_rules/character.yaml`: `archetype_system`, `tier_1_archetypes`,
`tier_2_additions` (rival), `tier_3_unlocks` (hero_with_flaws / complex_villain / morally_ambiguous),
`tier_4_5.approach: preserve_original`, the `heroism_translation.subroutine` (the literal 3-step
IDENTIFY/LOOKUP/TRANSLATE algorithm — ported as an executable procedure), and `special_handling`
(per-character overrides, e.g. gollum, denethor).

### 2.3 `resources/agency.md` — Agency Externalization (ADR-003)

The signature rule, carried verbatim from `thematic.yaml → agency_externalization` plus the ADR-003
rationale:

```yaml
agency_externalization:
  core_principle: "Badness is always a STATE or ACCIDENT, never innate."
  tier_1: {mode: mandatory, examples: [{source: "Dark Lord, evil", target: "Grumpy King, no sunshine"}, …]}
  tier_2: {mode: mandatory, softening: "permits_misunderstanding_as_cause"}
  tier_3: {mode: optional}
  tier_4_5: {mode: forbidden}   # "Patronizing; undermines character complexity" (tier_5 profile)
```

**Why it lives here, not in adopted `writing-principles`:** bolting it onto an adopted skill would break
the boundary contract (adopted files stay patch-clean). It rides in the native `/adaptation-rules`,
loaded additively by the adopted `writer`/`critic`. Enforced by `writer` (applies), audited by
`safety-verifier` (Section 2 of the rubric) and `critic` (adaptation-quality focus).

---

## 3. `/source-fidelity` — v2.0 Pragmatic Verification Protocol (constraint #2)

**Directory:** `skills/source-fidelity/`. Owned by the native `analyst` agent. Carries
`prompts/analysis/chapter_analysis.md`.

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

### 3.1 Body — the 5-phase protocol (carried verbatim)

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

### 3.2 Output schema — `work/analysis/ch-<NN>.yaml`

The `analyst` agent emits this (carried from `chapter_analysis.md`'s YAML output block, extended with the
`status` field for the ABORT gate):

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

**Tag propagation:** these tags flow downstream through the *adopted* `story-memory` fact-extraction
carrier (native tag, adopted carrier) — no edit to `story-memory`; the tags are just data in the facts it
extracts.

---

## 4. `/adaptation-safety` — the 6-section gate (build-new; constraint #3)

**Directory:** `skills/adaptation-safety/`. Owned by native `safety-verifier`. Carries
`prompts/verification/safety_check.md`. The full machine-checkable rubric is in
[`safety-rubric.md`](safety-rubric.md); this section specifies the skill wrapper and genre resources.

```yaml
---
name: adaptation-safety
description: |
  The 6-section post-generation safety rubric for Tier 1-2 children's adaptations: forbidden-content
  scan, agency-externalization check, emotional safety, safe-home schema, nightmare prevention, and
  linguistic compliance. Emits a PASS/FAIL verdict. Load when verifying children's-tier output before
  delivery. Runs on ALL Tier 1 and Tier 2 output.
---
```

**Body:** the 6 sections + Automatic-Failures list + verdict contract, carried verbatim from
`safety_check.md`. Detailed rubric → [`safety-rubric.md`](safety-rubric.md).

### 4.1 Genre resources (build-new — CWS ships none for children/YA)

CWS ships genre resources for litfic/thriller/horror/fantasy/mystery/romance but **none for children or
YA** (verified). LAF fills this gap:

- **`resources/children.md`** — children's-fiction craft for Tiers 1-3: prosocial centering, episodic
  structure, positive resolution, safe-home schema, nightmare-prevention framing, vocabulary/sentence
  ceilings. Sourced from the tier-1/tier-3 transform prompts and tier profiles.
- **`resources/ya.md`** — young-adult craft for Tier 5: meaning-not-sanitization, unreliable narrator and
  full irony range permitted, when-to-intervene (archaic language, historical context) vs
  when-not-to-intervene (difficult themes, moral complexity, character deaths). Sourced from the tier-5
  profile's `adaptation_philosophy` + `supplementary_approach`.

These are genre *reference* resources (how to write these age bands well), distinct from the safety
*rubric* (the pass/fail gate). The rubric gates; the genre resources inform the writer.

---

## 5. Skill → consumer map

| Native skill | Loaded by (agent) | Provenance of loader |
|---|---|---|
| `/adaptation-tiers` | analyst, chronicler, safety-verifier, tier-coordinator (+ muse reads `kb/tiers`) | native + build-new |
| `/adaptation-rules` | **writer (adopted-patched)**, **critic (adopted, adaptation focus)** | adopted |
| `/source-fidelity` | analyst, tier-coordinator | native + build-new |
| `/adaptation-safety` | safety-verifier | native |

The two rows where an **adopted** agent loads a **native** skill (`writer`, `critic`) are the boundary
contract's whole purpose — and neither requires editing the adopted agent body beyond the single
frontmatter line for `writer` ([`agent-schemas.md §3`](agent-schemas.md)). `critic` loads
`/adaptation-rules` situationally via the muse's dispatch brief (focus-area context), needing no
frontmatter change at all.
