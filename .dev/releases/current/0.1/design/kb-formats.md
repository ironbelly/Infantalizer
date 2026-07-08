---
title: "Knowledge-Base File Formats — LAF 0.1"
parent: DESIGN.md
status: draft
---

# Knowledge-Base File Formats

The native kb layers ride **inside** the adopted `kb/` container under adopted `kb-management` lifecycle
rules ([DESIGN.md §2](DESIGN.md)). This spec defines the file formats for the three native layers plus
the per-tier canon layer (graft G1). Adopted layers (`canon/`, `characters/`, `world/`, `timeline/`,
`styles/`, `vocab.md`, `issues/`) keep their CWS markdown formats unchanged and are not re-specified here.

**Format policy:** native tier/mapping data is **YAML** (carried verbatim from LAF `config/` — zero
rework, ADR-006). Native canon-state (`continuity.md`, `decisions.md`, `canon-delta.md`) is **markdown**,
matching the adopted `kb/canon/` convention so `chronicler` and `continuity-checker` read one prose format.

---

## 1. Layout recap

```
kb/
├── canon/  characters/  world/  timeline/  styles/  vocab.md  issues/   # ADOPTED — CWS md formats, unchanged
├── tiers/                          # NATIVE §2
│   ├── tier_1.yaml  tier_2.yaml  tier_3.yaml  tier_5.yaml
│   └── (tier_4 interpolated at runtime — never stored)
├── adaptation-mapping/             # NATIVE §3
│   ├── universal-mappings.yaml
│   └── <work>-mapping.yaml         # e.g. tolkien-mapping.yaml
└── adaptations/<work>/             # NATIVE + graft G1 §4
    └── tier-<N>/
        ├── decisions.md
        ├── continuity.md
        └── chapters/ch-<NN>/
            ├── analysis.yaml        # copy of work/analysis/ch-NN.yaml, promoted on accept
            ├── adapted.md           # the accepted tier-N adaptation of this chapter
            └── canon-delta.md
```

---

## 2. `kb/tiers/tier_<N>.yaml` — tier profiles (carried verbatim)

Ported **unchanged** from `config/age_profiles/tier_<N>_*.yaml`. The `analyst`, `writer`,
`safety-verifier`, `continuity-checker`, and `chronicler` read the active tier's profile as the
authoritative constraint set. **No schema rework** — the LAF profile schema is adopted as the kb schema.

### 2.1 Canonical profile schema (union of all tier keys)

```yaml
profile:
  id: tier_<N>_<label>            # e.g. tier_1_preschool
  name: <display>
  age_range: [<min>, <max>]
  description: <string>

developmental_basis:
  piaget_stage: <string>
  piaget_characteristics: [ {<characteristic>: <desc>}, ... ]   # T1 uses this list form
  kohlberg_stage: <int>
  kohlberg_description: <string>
  moral_capabilities: [ ... ]     # T3+ only

thresholds:
  violence:            {level: <int>, description, permitted: [...], forbidden: [...], transformation_target}
  emotional_complexity:{level: <int>, permitted_emotions|permitted: [...], forbidden_states: [...]}
  moral_ambiguity:     {level: <int>, requires_clear_good_bad: <bool>, permits_hero_failure: <bool>, ...}
  narrative_complexity:{parallel_plotlines: <bool>, flashbacks: <bool>, max_named_characters: <int>, timeline}

linguistic:
  vocabulary:        {target_grade_level, max_syllables, forbidden: [...], additions|can_introduce: [...]}
  sentence_structure:{max_clauses: <int>, passive_voice: <bool>, max_words_per_sentence: <int>}
  chapter_structure: {max_words: <int>, episodic: <bool>, requires_positive_resolution: <bool>}

transformation_rules:              # per-tier instantiation; commentary only — thematic.yaml is canonical
  agency_externalization: {mode, principle?|reason?|softening?}
  conflict_to_cooperation|conflict_handling: {mode, translations?|strategy?}
  death_euphemism|death_handling:  {mode, strategy?, translations?|can_use?|can_say?}
  villain_motivation:     {mode, description?|villains_are?|always_redeemable?|requirements?}
  heroism_definition:     {mode, heroic_acts?|heroic?}

# tier-specific optional blocks (present only where relevant):
safety:               {safe_home_schema, nightmare_prevention}          # T1 only
contest_paradigm:     {principles: [...]}                               # T2 only
tier_transition_summary: {major_changes: [{from, to}, ...]}             # T3 only
adaptation_philosophy:{core_principle, when_to_intervene, when_not_to_intervene}   # T5 only
supplementary_approach:{recommended: [...]}                            # T5 only
```

### 2.2 Schema-drift handling (design decision)

The source profiles drift: T1-T3 use `conflict_to_cooperation`/`death_euphemism`; T5 uses
`conflict_handling`/`death_handling`. **Decision: preserve the drift verbatim** (zero rework), and make
readers key-tolerant. Skills that read these keys accept either name:
```
conflict_rule = profile.transformation_rules.get("conflict_to_cooperation")
             or profile.transformation_rules.get("conflict_handling")
death_rule    = profile.transformation_rules.get("death_euphemism")
             or profile.transformation_rules.get("death_handling")
```
This keeps the port a pure copy and localizes the drift to a two-line lookup in the consuming skill body,
rather than editing the vendored-from-LAF config. (Rationale: the config files are LAF's crown jewels;
rewriting their keys at port time invites transcription error and forfeits "carried verbatim, zero
rework.")

### 2.3 Canonicity: two rule sources reconciled

Rules appear in **both** `config/transformation_rules/thematic.yaml` (cross-work, canonical) and each
`tier_N.transformation_rules` block (per-tier instantiation with `# KEY CHANGE` commentary). **Decision:**
- `thematic.yaml` → `/adaptation-rules/resources/thematic.md` is **canonical** for rule application.
- `tier_N.yaml.transformation_rules` is **commentary/cross-check** — readable, but the writer applies the
  thematic.md version. `check_boundary.py` does not police agreement (they are both native); a Phase-3
  spot check confirms they don't contradict.

### 2.4 Tier 4 (interpolated, never stored)

No `tier_4.yaml` exists. `/adaptation-tiers` interpolates it at request time (T3 floor, T5 ceiling,
conservative midpoint; `agency_externalization = forbidden`). The interpolated profile is a derived
in-memory object, never written to `kb/tiers/`.

---

## 3. `kb/adaptation-mapping/` — concept cascade (carried verbatim)

### 3.1 `universal-mappings.yaml` — cross-work defaults (least specific)

Ported unchanged from `config/concept_mapping/universal_mappings.yaml`. Flat dict keyed by concept slug;
each concept has `tier_1`, `tier_2`, `tier_3`, `tier_4_5` buckets. Fields per bucket are **not uniform**
across concepts (by design): `death` uses `framing`, `evil` uses `agency`, `war` nests `components`,
`despair` uses `cause`/`approach`, `injury` uses `healing`, `betrayal` uses `approach`. `tier_4_5` always
collapses to `{translation: "[preserve]"}`.

```yaml
<concept-slug>:
  tier_1:   {translation: <str>, <framing|agency|cause|healing|components|approach>?}
  tier_2:   {translation: <str>, ...?}
  tier_3:   {translation: <str>, ...?}
  tier_4_5: {translation: "[preserve]"}
```
Concepts present (9): `death`, `evil`, `war`, `despair`, `injury`, `betrayal`, `burden`,
`supernatural_terror`, `martial_heroism`.

### 3.2 `<work>-mapping.yaml` — work-specific overrides (most specific)

Ported from `config/concept_mapping/templates/<author>_mapping.yaml`; created per work at onboarding by
copying `templates/work-mapping-template.yaml`. Four top-level keys:

```yaml
work_metadata:  {title, author, key_challenges: [...]}
characters:                                 # keyed by character slug
  <slug>:
    original: {name, role, complexity?}
    tier_1:   {name, archetype, traits?|cause?}
    tier_3:   {can_show: [...]}
    tier_4_5: {approach: "preserve_original"}
concepts:                                    # keyed by concept slug
  <slug>:
    original: <str>
    tier_1: <str>   tier_2: <str>   tier_3: <str>   tier_4_5: "[preserve]"
key_scenes:                                  # keyed by scene slug
  <slug>:
    challenges: [violence|death|...]
    tier_1: {name, framing, omit?}
    tier_3: {approach}
master_translation_table:                    # flat LIST (illustrative, not a lookup)
  - {original: <str>, tier_1: <str>, principle: <str>}
```

### 3.3 Cascade resolution (most-specific-wins)

When the writer/analyst resolves how to translate an element at `active_tier`, precedence is:

```
1. <work>-mapping.yaml : key_scenes.<scene>.tier_<N>          ← MOST specific (scene-level)
2. <work>-mapping.yaml : characters.<slug>.tier_<N>
3. <work>-mapping.yaml : concepts.<slug>.tier_<N>
4. universal-mappings.yaml : <concept>.tier_<N>               ← LEAST specific (cross-work default)
5. /adaptation-rules universal rule (thematic.md) for the category
```
First hit wins. `master_translation_table` is **illustrative only** — never a resolution source (it's a
list, not a keyed map). For tiers with no explicit bucket (e.g. a character has only `tier_1`/`tier_3`),
fall through to the next-less-specific layer; `tier_2` and `tier_4_5` commonly resolve at the universal
layer.

---

## 4. `kb/adaptations/<work>/tier-<N>/` — per-tier canon state (graft G1)

The layer that closes the divergent-canon bug: the same character holds **different canonical state per
tier**. Keyed `(work, tier, chapter)` throughout. Written by `chronicler` on accept; read by
`continuity-checker` (per-tier canon pass) and `reader-sim` (knowledge boundary).

### 4.1 `continuity.md` — running per-tier canon ("what a Tier-N reader now knows")

Markdown, append-mostly, one file per (work, tier). Format matches adopted `kb/canon/` prose style:

```markdown
# Continuity — <Work>, Tier <N> (<age range>)

_What a Tier-<N> reader knows after each accepted chapter. Names/facts here are TIER-TRANSFORMED
(e.g. "Grumpy King"), NOT source truth. Source truth lives in kb/canon/<work>/._

## Characters (as this tier knows them)
- **Grumpy King** (source: Sauron) — the character who makes the sky grey when he's cross. Wants
  everyone's shiny things tidied into one place. _First seen: ch-01. Redeemable: yes (tier-1 rule)._

## Established facts
- ch-01: The shiny ring makes people want to keep it and not share. (CERTAIN, from analysis ch-01)

## Open threads
- Where did the ring come from? (not yet disclosed at this tier)
```

**Invariants:**
- Every entry cites the source character/fact it derives from (traceability to `kb/canon/`).
- No fact appears here that a Tier-N reader could not know (respects tier disclosure — see
  `tier-coordinator` monotonicity, [`tier-coordinator.md §3`](tier-coordinator.md)).
- Tier-transformed names live **only** here, never promoted to shared `kb/canon/`.

### 4.2 `decisions.md` — adaptation decision log (append)

```markdown
# Adaptation Decisions — <Work>, Tier <N>

## ch-<NN>
- **Sauron → "Grumpy King"** — agency_externalization MANDATORY (T1). Source "Dark Lord" reframed to
  external state ("makes the sky grey when cross"). Ref: /adaptation-rules agency.md.
- **Battle of Pelennor → "The Big Tidy-Up"** — conflict_to_cooperation MANDATORY (T1). Ref: tolkien-mapping key_scenes.battle_pelennor.tier_1.
```

### 4.3 `chapters/ch-<NN>/canon-delta.md` — per-chapter, per-tier change record

```markdown
# Canon Delta — <Work> ch-<NN>, Tier <N>

## New at this tier this chapter
- Introduced: "Grumpy King" (source: Sauron)
- Fact: shiny ring wants to be kept, not shared

## Changed
- (none)

## Superseded / corrected
- (none)
```

### 4.4 `chapters/ch-<NN>/analysis.yaml` and `adapted.md`

- `analysis.yaml` — the promoted copy of `work/analysis/ch-<NN>.yaml` (schema in
  [`skill-specs.md §3.2`](skill-specs.md)); promoted only on muse-accept (constraint #5). It is
  tier-invariant but copied under each tier for locality.
- `adapted.md` — the accepted tier-N adaptation prose for this chapter.

### 4.5 The (work, tier, chapter) key — enforced everywhere

| Writer | Key use |
|---|---|
| `chronicler` | Never writes a tier-N fact into tier-M continuity; never promotes transformed names to shared canon |
| `continuity-checker` | Loads **only** `tier-<active>/continuity.md` for the per-tier contradiction pass |
| `tier-coordinator` | Reconciles across `tier-<N>/` dirs; asserts no cross-tier disclosure leak |
| `reader-sim` | `knowledge_boundary` = "read tier-N chapters 1..K-1" resolves against `tier-<N>/continuity.md` |

---

## 5. Shared vs per-tier canon (the G1 split, restated)

```
kb/canon/<work>/ch-NN.md              ← SHARED source truth. "Sauron is the Dark Lord." Tier-neutral.
                                         Written by chronicler; source facts only; never transformed.
        │
        │ derives (per tier, transformed)
        ▼
kb/adaptations/<work>/tier-1/continuity.md   ← "Grumpy King makes the sky grey."
kb/adaptations/<work>/tier-3/continuity.md   ← "Sauron, a dark lord who wants the ring's power."
kb/adaptations/<work>/tier-5/continuity.md   ← (minimal transform — near source)
```

This split is the whole point of graft G1: one source truth, N tier-divergent canonical states, no
cross-contamination. Without it, a Tier-1 "Grumpy King" fact could leak into Tier-5 canon (or vice
versa) — the latent bug Path C was chosen to close.
