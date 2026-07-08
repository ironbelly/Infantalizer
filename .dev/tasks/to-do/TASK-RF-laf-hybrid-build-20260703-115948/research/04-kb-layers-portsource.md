# Research: kb Layers + Port-Source Verbatim Mapping
**Topic type:** Data / File-Format + Integration
**Scope:** kb/tiers, kb/adaptation-mapping, per-tier canon graft-G1, LAF port-source carry
**Status:** Complete
**Date:** 2026-07-03

**Sources read (verbatim, on-disk):**
- Spec: `.dev/releases/current/0.1/design/kb-formats.md` (282 lines, full)
- Port-sources under `/config/workspace/Infantalizer/` (line counts via `wc -l`):
  - `config/age_profiles/tier_1_preschool.yaml` — 94 lines (file has no trailing NL count quirk; content lines 1-95)
  - `config/age_profiles/tier_2_early_elementary.yaml` — 84 lines
  - `config/age_profiles/tier_3_middle_elementary.yaml` — 87 lines
  - `config/age_profiles/tier_5_young_adult.yaml` — 87 lines
  - `config/concept_mapping/universal_mappings.yaml` — 56 lines
  - `config/concept_mapping/templates/tolkien_mapping.yaml` — 81 lines
  - `config/transformation_rules/thematic.yaml` — 90 lines
  - `config/transformation_rules/character.yaml` — 77 lines
  - `templates/work_mapping_template.yaml` — 60 lines
  - **Total: 716 lines of verbatim carry** across 9 files.

> **Malware note:** all port-source files are benign narrative-adaptation config
> (children's-content age-tiering). No executable code, no malware.

---

## 0. Port-source → native kb target map (the verbatim carry)

Every LAF port-source is copied **byte-for-byte** into a native kb/skill-resource
target. Zero rework (ADR-006; kb-formats.md:14, :45-47, :128). The only content-side
change ever applied is at *read* time in the consuming skill body (key-tolerant lookup,
§2 below), never at copy time.

| # | LAF port-source (`/config/workspace/Infantalizer/`) | Lines | Native target | Carry mode |
|---|---|---|---|---|
| P1 | `config/age_profiles/tier_1_preschool.yaml` | 94 | `kb/tiers/tier_1.yaml` | verbatim copy + rename |
| P2 | `config/age_profiles/tier_2_early_elementary.yaml` | 84 | `kb/tiers/tier_2.yaml` | verbatim copy + rename |
| P3 | `config/age_profiles/tier_3_middle_elementary.yaml` | 87 | `kb/tiers/tier_3.yaml` | verbatim copy + rename |
| P4 | `config/age_profiles/tier_5_young_adult.yaml` | 87 | `kb/tiers/tier_5.yaml` | verbatim copy + rename |
| — | *(no tier_4 source)* | — | *(interpolated at runtime — never stored)* | §2.4 |
| P5 | `config/concept_mapping/universal_mappings.yaml` | 56 | `kb/adaptation-mapping/universal-mappings.yaml` | verbatim copy + rename (`_`→`-`) |
| P6 | `config/concept_mapping/templates/tolkien_mapping.yaml` | 81 | `kb/adaptation-mapping/tolkien-mapping.yaml` (created at onboarding by copying template) | verbatim copy + rename |
| P7 | `config/transformation_rules/thematic.yaml` | 90 | `/adaptation-rules/resources/thematic.md` (fenced verbatim inside md) | wrap-in-fence (R2 owns wrapper) |
| P8 | `config/transformation_rules/character.yaml` | 77 | `/adaptation-rules/resources/character.md` (fenced verbatim inside md) | wrap-in-fence (R2 owns wrapper) |
| P9 | `templates/work_mapping_template.yaml` | 60 | `templates/work-mapping-template.yaml` | verbatim copy + rename (`_`→`-`) |

**Rename pattern:** file names lose the `_<label>` suffix (tier profiles) and switch
`snake_case`→`kebab-case` (`universal_mappings`→`universal-mappings`,
`tolkien_mapping`→`tolkien-mapping`, `work_mapping_template`→`work-mapping-template`).
Content is unchanged. Builder should create **one carry item per file** (9 items).

---

## 1. `kb/tiers/tier_<N>.yaml` — tier profiles (P1-P4)

Spec: kb-formats.md §2 (lines 43-120). Ported unchanged from
`config/age_profiles/tier_<N>_*.yaml`; the LAF profile schema **is** adopted as the
kb schema (kb-formats.md:47). Read by `analyst`, `writer`, `safety-verifier`,
`continuity-checker`, `chronicler` as the authoritative constraint set (kb-formats.md:45-46).

### 1.1 Top-level keys actually present per file (verified on-disk)

Canonical schema §2.1 (kb-formats.md:51-89) is the **union** of tier keys. Each real
file uses only a subset. Verified top-level keys:

| Top-level key | T1 | T2 | T3 | T5 | Notes |
|---|:-:|:-:|:-:|:-:|---|
| `profile` | ✓ | ✓ | ✓ | ✓ | id/name/age_range/description |
| `developmental_basis` | ✓ | ✓ | ✓ | ✓ | piaget + kohlberg; `moral_capabilities` T3 only (tier_3:18-20) |
| `thresholds` | ✓ | ✓ | ✓ | ✓ | violence/emotional_complexity/moral_ambiguity/narrative_complexity |
| `linguistic` | ✓ | ✓ | ✓ | ✓ | vocabulary/sentence_structure/chapter_structure |
| `transformation_rules` | ✓ | ✓ | ✓ | ✓ | **drift here — see §1.3** |
| `safety` | ✓ | ✗ | ✗ | ✗ | T1 only (tier_1:88-95) |
| `contest_paradigm` | ✗ | ✓ | ✗ | ✗ | T2 only (tier_2:80-85) |
| `tier_transition_summary` | ✗ | ✗ | ✓ | ✗ | T3 only (tier_3:82-88) |
| `adaptation_philosophy` | ✗ | ✗ | ✗ | ✓ | T5 only (tier_5:71-80) |
| `supplementary_approach` | ✗ | ✗ | ✗ | ✓ | T5 only (tier_5:82-87) |

Matches §2.1 tier-specific optional-block annotations (kb-formats.md:83-88) **exactly**.

### 1.2 `profile.id` values (drive the `active_tier` selection)
- `tier_1_preschool` (tier_1:5), age_range [3,5]
- `tier_2_early_elementary` (tier_2:5), age_range [6,8]
- `tier_3_middle_elementary` (tier_3:5), age_range [9,11]
- `tier_5_young_adult` (tier_5:5), age_range [15,17]

### 1.3 Schema drift — CONFLICT/DEATH key names (VERIFIED against actual files)

Spec §2.2 (kb-formats.md:91-105) claims T1-T3 use `conflict_to_cooperation`/`death_euphemism`,
T5 uses `conflict_handling`/`death_handling`. **Confirmed by reading every file:**

| File | conflict key (actual line) | death key (actual line) |
|---|---|---|
| tier_1 | `conflict_to_cooperation` (tier_1:66) | `death_euphemism` (tier_1:73) |
| tier_2 | `conflict_to_cooperation` (tier_2:60) | `death_euphemism` (tier_2:68) |
| tier_3 | `conflict_to_cooperation` (tier_3:66) | `death_euphemism` (tier_3:69) |
| tier_5 | `conflict_handling` (tier_5:58) | `death_handling` (tier_5:61) |

**[SPEC-CONFIRMED]** — the drift is real and exactly as §2.2 describes. Decision:
**preserve verbatim; readers are key-tolerant** (kb-formats.md:95-101). The consuming
skill body (R2's `/adaptation-rules`) does a two-line `.get(a) or .get(b)` fallback:
```
conflict_rule = tr.get("conflict_to_cooperation") or tr.get("conflict_handling")
death_rule    = tr.get("death_euphemism")        or tr.get("death_handling")
```
Rationale (kb-formats.md:102-105): config files are "LAF's crown jewels"; rewriting
keys at port time invites transcription error and forfeits "carried verbatim, zero rework."
**Builder implication:** carry items MUST NOT normalize these keys; any normalization
belongs in the reader skill, not the kb file.

Other verified per-tier `transformation_rules` sub-key variance (all preserved verbatim):
- `agency_externalization.mode`: mandatory (T1:63, T2:57) → optional (T3:64) → forbidden (T5:55, with `reason`)
- `agency_externalization` extra keys: `principle` (T1:64), `softening` (T2:58), `reason` (T5:56)
- conflict `mode`: mandatory (T1:67) / contest (T2:61) / optional (T3:67) / preserve (T5:59)
- death `mode`/`strategy`: journey_or_sleep (T1:75) / gentle_acknowledgment (T2:69) / direct_but_gentle (T3:70) / preserve (T5:62)
- `villain_motivation.mode`: external_state / misunderstanding / can_be_internal / preserve
- `heroism_definition.mode`: prosocial_only / prosocial_with_competition / includes_defense / full_spectrum

### 1.4 No `tier_4.yaml` — interpolated (§2.4)

Spec §2.4 (kb-formats.md:116-120): **no `tier_4.yaml` exists**; confirmed no
`config/age_profiles/tier_4_*.yaml` in the port-source set. `/adaptation-tiers`
interpolates it at request time (T3 floor, T5 ceiling, conservative midpoint;
`agency_externalization = forbidden`). Derived in-memory object, **never written** to
`kb/tiers/`. **Builder implication:** do NOT create a tier_4 carry item; the
interpolation logic is a skill responsibility (R2), not a kb file.

### 1.5 Canonicity: two rule sources reconciled (§2.3)

Rules appear in **both** `thematic.yaml` (cross-work) and each `tier_N.transformation_rules`
(per-tier, with `# KEY CHANGE`/`# KEY PARADIGM` comments — e.g. tier_3:37,64,66,69).
**Decision (kb-formats.md:107-114):**
- `thematic.yaml` → `/adaptation-rules/resources/thematic.md` is **CANONICAL** for rule application.
- `tier_N.yaml.transformation_rules` is **commentary / cross-check** — readable, but the
  writer applies the thematic.md version.
- `check_boundary.py` does **not** police agreement (both are native); a Phase-3 spot
  check confirms they don't contradict.

---

## 2. `kb/adaptation-mapping/` — concept cascade (P5, P6)

Spec: kb-formats.md §3 (lines 124-184).

### 2.1 `universal-mappings.yaml` (P5) — cross-work defaults, LEAST specific

Ported unchanged from `config/concept_mapping/universal_mappings.yaml`. Flat dict keyed
by concept slug; each concept has `tier_1`, `tier_2`, `tier_3`, `tier_4_5` buckets
(kb-formats.md:128-132).

**9 concepts confirmed on-disk** (matches §3.1 line 141-142):
`death` (uni:4), `evil` (uni:10), `war` (uni:16), `despair` (uni:22), `injury` (uni:28),
`betrayal` (uni:34), `burden` (uni:40), `supernatural_terror` (uni:46),
`martial_heroism` (uni:52).

**Per-bucket field NON-uniformity confirmed** (§3.1 line 130-132 — "not uniform by design"):
| Concept | tier_1 extra field(s) beyond `translation` | evidence |
|---|---|---|
| `death` | `framing` | uni:5 |
| `evil` | `agency` | uni:11 |
| `war` | `components: {battle, army}` (nested) | uni:17 |
| `despair` | `cause` (t1), `approach` (t3) | uni:23, uni:25 |
| `injury` | `healing` | uni:29 |
| `betrayal` | `approach` (t3 only) | uni:37 |
| `burden` | `framing` (t1) | uni:41 |
| `supernatural_terror` | *(translation only)* | uni:47-50 |
| `martial_heroism` | *(translation only)* | uni:53-55 |

**`tier_4_5` collapse confirmed:** every concept's `tier_4_5` is exactly
`{translation: "[preserve]"}` (uni:8,14,20,26,32,38,44,50,56). **[SPEC-CONFIRMED]** §3.1:139.

### 2.2 `<work>-mapping.yaml` (P6) — work-specific overrides, MOST specific

Ported from `config/concept_mapping/templates/tolkien_mapping.yaml`; per work it is
**created at onboarding by copying `templates/work-mapping-template.yaml`** (kb-formats.md:146-147).
The Tolkien file is a pre-populated instance.

**Top-level keys — [SPEC vs FILE discrepancy, resolved]:** spec §3.2 line 147 says
"**Four** top-level keys" but then lists **five** blocks (work_metadata/characters/
concepts/key_scenes/master_translation_table, kb-formats.md:149-167). The **actual file
has 5 top-level keys** (tolkien:4 `work_metadata`, :13 `characters`, :43 `concepts`,
:64 `key_scenes`, :77 `master_translation_table`). **[SPEC-CONTRADICTED — count]:** the
prose word "Four" is wrong; the file and the spec's own enumeration both give 5. The task
prompt also lists 5. **Builder: treat as 5 top-level keys.**

Verified structure (Tolkien instance):
- `work_metadata`: title/author/`key_challenges` (list of 4) — tolkien:4-11
- `characters` (keyed by slug): 8 chars (frodo, sam, aragorn, gandalf, sauron, gollum, eowyn, denethor).
  Buckets are **sparse/non-uniform** — e.g. `frodo` has tier_1+tier_3 (tolkien:14-16);
  `sam`/`aragorn`/`gandalf` have tier_1 only (tolkien:18-25). Per-char tier fields vary
  (`archetype`, `name`, `cause`, `can_show`, `omit`, `ring_claim`, etc.). NB: the Tolkien
  instance does **not** use the template's `original:` sub-block or `tier_4_5:` for chars —
  those are template scaffolding (see §2.3).
- `concepts` (keyed by slug): the_one_ring, mordor, mount_doom, nazgul, army_of_dead —
  each with `tier_1`/`tier_3` string values (tolkien:44-62). No `tier_2`/`tier_4_5` in the
  instance → those tiers fall through the cascade (§2.4).
- `key_scenes` (keyed by slug): battle_pelennor, mount_doom_climax, grey_havens —
  each `tier_1: {…}` + `tier_3: {approach}` (tolkien:65-75). NB the instance omits the
  `challenges:` list the template shows (template:49); it is optional.
- `master_translation_table`: flat **LIST** of 4 `{original, tier_1, principle}` rows
  (tolkien:77-81). **Illustrative only — NEVER a resolution source** (§3.3:181).

### 2.3 `work-mapping-template.yaml` (P9) — the onboarding scaffold

Ported unchanged from `templates/work_mapping_template.yaml` (60 lines). Placeholder
skeleton with `[Bracketed]` fill-ins. Same 5 top-level keys as §2.2. It **does** show the
fuller per-character schema §3.2:151-156 documents:
`original: {name, role, complexity}`, `tier_1: {name, archetype, traits}`,
`tier_3: {can_show}`, `tier_4_5: {approach: "preserve_original"}` (template:12-24,26-37).
Two example character slots (`protagonist_name`, `antagonist_name`). Onboarding copies
this → `kb/adaptation-mapping/<work>-mapping.yaml`, then the operator fills it in (the
Tolkien file is what a filled-in copy looks like, minus some optional scaffolding).

### 2.4 Cascade resolution order (§3.3 — 5 levels, most-specific-wins)

Spec §3.3 (kb-formats.md:170-184). When writer/analyst resolves how to translate an
element at `active_tier`, precedence (first hit wins):

```
1. <work>-mapping.yaml : key_scenes.<scene>.tier_<N>     ← MOST specific (scene-level)
2. <work>-mapping.yaml : characters.<slug>.tier_<N>
3. <work>-mapping.yaml : concepts.<slug>.tier_<N>
4. universal-mappings.yaml : <concept>.tier_<N>          ← LEAST specific (cross-work default)
5. /adaptation-rules universal rule (thematic.md) for the category
```
Invariants:
- `master_translation_table` is **NEVER** a resolution source (list, not a keyed map) — §3.3:181.
- For tiers with no explicit bucket (e.g. a char with only tier_1/tier_3), **fall through**
  to the next-less-specific layer; `tier_2` and `tier_4_5` commonly resolve at the universal
  layer (§3.3:182-184). This is exactly why the Tolkien instance can omit tier_2/tier_4_5.
- `tier_4` resolution rides the interpolated profile (§1.4) + falls to universal `tier_4_5`
  buckets / `[preserve]`.

**Builder implication:** the cascade is a **reader-side algorithm** (owned by R2's skills);
the kb layer only supplies the data at 4 of the 5 levels (levels 1-4 are these YAMLs;
level 5 is thematic.md). No cascade code lives in the kb files themselves.

---

## 3. Transformation-rule DATA (P7 thematic, P8 character)

These carry into `/adaptation-rules/resources/{thematic,character}.md` fenced **verbatim**
(R2 owns the md wrapper; I own the DATA schema below). thematic.md is **canonical** for
rule application (§1.5 / kb-formats.md:111).

### 3.1 `thematic.yaml` (P7, 90 lines) — 6 rule groups × 4 tier buckets

Verified top-level rule groups (each keyed `tier_1/tier_2/tier_3/tier_4_5`):
| Rule group | line | tier bucket keys | notable mode/field enums |
|---|---|---|---|
| `violence_transformation` | thematic:4 | tier_1..tier_4_5 | per-element `{battle,attack,injury,death,weapons}: {target, example?, action?}`; t4_5 `mode: minimal_transformation` |
| `conflict_transformation` | thematic:21 | tier_1..tier_4_5 | `mode`: mandatory/mandatory/optional/preserve; `translations: {war,siege,enemy_army}` |
| `agency_externalization` | thematic:33 | +`core_principle` + tier_1..tier_4_5 | `mode`: mandatory/mandatory/optional/**forbidden** (t4_5:47); t1 `examples` list |
| `death_handling` | thematic:49 | tier_1..tier_4_5 | `strategy`: journey_or_sleep/gentle_acknowledgment/direct_but_gentle/preserve_original; `never_use`/`can_use` lists |
| `villain_motivation` | thematic:64 | tier_1..tier_4_5 | `mode`: external_state/misunderstanding/can_be_internal/complex_internal |
| `heroism_definition` | thematic:78 | tier_1..tier_4_5 | `mode`: prosocial_only/prosocial_with_competition/includes_defense/full_spectrum |

**Mode enums the writer keys against** (union across groups):
`mandatory, contest, optional, preserve, forbidden, external_state, misunderstanding,
can_be_internal, complex_internal, minimal_transformation, prosocial_only,
prosocial_with_competition, includes_defense, full_spectrum, direct_but_gentle,
gentle_acknowledgment, journey_or_sleep, preserve_original`.

> **[Cross-check note]:** thematic.yaml uses `death_handling` (thematic:49) — the SAME
> key name T5's profile uses, but DIFFERENT from T1-T3 profiles' `death_euphemism`.
> This is the second appearance of the drift (§1.3). thematic.md is canonical, so the
> writer keys on thematic's `death_handling` group regardless of the tier-profile key name.

### 3.2 `character.yaml` (P8, 77 lines) — archetype system + heroism translation

Verified top-level keys:
| Key | line | content |
|---|---|---|
| `archetype_system` | character:4 | `{description}` header only |
| `tier_1_archetypes` | character:7 | 6 archetypes: protagonist, hero_leader, mentor, antagonist, female_hero, loyal_companion — each `{name, permitted_traits[], forbidden_traits[]?, …}` |
| `tier_2_additions` | character:40 | `rival` archetype |
| `tier_3_unlocks` | character:46 | hero_with_flaws / complex_villain / morally_ambiguous `{permitted: true}` |
| `tier_4_5` | character:51 | `{approach: "Preserve original complexity"}` |
| `heroism_translation` | character:54 | `subroutine` (3-step block scalar) + `examples` keyed by phrase, each with tier_1..tier_4_5 |
| `special_handling` | character:71 | per-character overrides (gollum, denethor) with tier_1/tier_3 |

**Tier buckets present:** tier_1 (archetypes), tier_2 (additions), tier_3 (unlocks),
tier_4_5 (preserve). `heroism_translation.examples` entries use tier_1/tier_2/tier_3/tier_4_5
keys with `[preserve]` sentinel at t4_5 (character:65) and sometimes t3 (character:69).

**Builder implication (P7,P8):** these two are DATA the R2 skill fences inside a `.md`.
Carry item = "copy YAML body verbatim into a fenced ```yaml block in the resource md."
R2 supplies the surrounding skill/resource prose; do not duplicate.

---

## 4. `kb/adaptations/<work>/tier-<N>/` — per-tier canon (graft G1)

Spec: kb-formats.md §4 (lines 188-262) + §5 (266-281). This is the **native, NOT ported**
layer — no LAF source file; the FILE FORMATS below are authored fresh for LAF 0.1. Written
by `chronicler` on accept (R3 owns the agent body; **I own these file-format schemas**).
Read by `continuity-checker` (per-tier canon pass) and `reader-sim` (knowledge boundary).
**Keyed `(work, tier, chapter)` throughout** (kb-formats.md:192).

Directory shape (kb-formats.md:31-39):
```
kb/adaptations/<work>/tier-<N>/
├── decisions.md                 # §4.2 — per (work,tier), append
├── continuity.md                # §4.1 — per (work,tier), append-mostly
└── chapters/ch-<NN>/
    ├── analysis.yaml            # §4.4 — promoted copy of work/analysis/ch-NN.yaml
    ├── adapted.md               # §4.4 — accepted tier-N adaptation prose
    └── canon-delta.md           # §4.3 — per (work,tier,chapter)
```

### 4.1 `continuity.md` (§4.1, kb-formats.md:194-219) — running per-tier canon
Markdown, append-mostly, **one file per (work, tier)**. Matches adopted `kb/canon/` prose.
Sections: `# Continuity — <Work>, Tier <N> (<age range>)`, an italic banner reminding that
names/facts are TIER-TRANSFORMED (not source truth), `## Characters (as this tier knows them)`,
`## Established facts`, `## Open threads`.
**Invariants (kb-formats.md:215-219):**
- (I-1) Every entry **cites the source** character/fact it derives from → traceability to `kb/canon/`.
- (I-2) **No fact a Tier-N reader could not know** (respects tier disclosure / monotonicity;
  see `tier-coordinator.md §3`).
- (I-3) **Tier-transformed names live ONLY here** — never promoted to shared `kb/canon/`.

### 4.2 `decisions.md` (§4.2, kb-formats.md:221-230) — adaptation decision log
Append; one per (work, tier). `# Adaptation Decisions — <Work>, Tier <N>`, then per-chapter
`## ch-<NN>` bullets. Each bullet: `**<source> → "<transformed>"** — <rule> <mode> (T<N>).
… Ref: <rule-source or mapping key>.` (e.g. "Ref: /adaptation-rules agency.md",
"Ref: tolkien-mapping key_scenes.battle_pelennor.tier_1").

### 4.3 `chapters/ch-<NN>/canon-delta.md` (§4.3, kb-formats.md:232-246) — per-chapter, per-tier delta
`# Canon Delta — <Work> ch-<NN>, Tier <N>` with three sections:
`## New at this tier this chapter` (Introduced / Fact bullets),
`## Changed`, `## Superseded / corrected` (both may be `(none)`).

### 4.4 `chapters/ch-<NN>/analysis.yaml` + `adapted.md` (§4.4, kb-formats.md:248-253)
- `analysis.yaml` — **promoted copy** of `work/analysis/ch-<NN>.yaml` (schema in
  skill-specs.md §3.2, owned elsewhere); promoted **only on muse-accept** (constraint #5).
  Tier-invariant but copied under each tier for locality.
- `adapted.md` — the accepted tier-N adaptation prose for this chapter.

### 4.5 The (work, tier, chapter) key — enforced per writer (§4.5, kb-formats.md:255-262)
| Writer | Key discipline |
|---|---|
| `chronicler` | Never writes a tier-N fact into tier-M continuity; never promotes transformed names to shared canon |
| `continuity-checker` | Loads **only** `tier-<active>/continuity.md` for the per-tier contradiction pass |
| `tier-coordinator` | Reconciles across `tier-<N>/` dirs; asserts no cross-tier disclosure leak |
| `reader-sim` | `knowledge_boundary` = "tier-N ch 1..K-1" resolves against `tier-<N>/continuity.md` |

### 4.6 Shared-vs-per-tier split (§5, the whole point of G1, kb-formats.md:266-281)
```
kb/canon/<work>/ch-NN.md            ← SHARED source truth ("Sauron is the Dark Lord"),
                                       tier-neutral, source facts only, NEVER transformed.
        │ derives (per tier, transformed)
        ▼
kb/adaptations/<work>/tier-1/continuity.md  ← "Grumpy King makes the sky grey."
kb/adaptations/<work>/tier-3/continuity.md  ← "Sauron, a dark lord who wants the ring's power."
kb/adaptations/<work>/tier-5/continuity.md  ← (minimal transform — near source)
```
One source truth → N tier-divergent canonical states → no cross-contamination. This closes
the latent divergent-canon bug Path C was chosen to fix (kb-formats.md:279-281).
**Three format invariants that gate correctness:** source-cite (I-1), no-disclosure-beyond-tier
(I-2), transformed-names-only-here (I-3). These are what R6's proof gate / `check_boundary.py`
will assert against.

**Builder implication:** graft-G1 files are **native authored templates/scaffolds**, not
carries. Builder creates: (a) format templates/examples for the 5 file types, (b) the
directory-creation logic in `chronicler` (R3), (c) invariant checks (R5/R6). No LAF port-source.

---

## 5. Summary & builder hand-off

### 5.1 Zero-rework carry CONFIRMED
All 9 port-source files are **pure verbatim copies** (only file rename + `_`→`-`). No content
edits at port time. The **only** transformation is a rename; the ONE schema issue (conflict/
death key drift) is deliberately preserved and absorbed by a **reader-side** key-tolerant
`.get(a) or .get(b)` lookup, never by editing the vendored file (§1.3). This satisfies
ADR-006 "carried verbatim, zero rework."

### 5.2 Verified findings vs spec
- **[SPEC-CONFIRMED]** conflict/death drift (T1-T3 `conflict_to_cooperation`/`death_euphemism`;
  T5 `conflict_handling`/`death_handling`) — read every file, exact lines cited (§1.3).
- **[SPEC-CONFIRMED]** 9 universal concepts, non-uniform buckets, tier_4_5 `[preserve]` collapse (§2.1).
- **[SPEC-CONFIRMED]** no tier_4 source; interpolated only (§1.4).
- **[SPEC-CONTRADICTED — minor]** §3.2 prose says "Four top-level keys" for `<work>-mapping.yaml`
  but the file (and the spec's own list, and the task prompt) has **5**
  (work_metadata/characters/concepts/key_scenes/master_translation_table). Builder: use 5.
- Note: thematic.yaml itself uses `death_handling` (the T5-style key), reinforcing that
  thematic.md is the canonical rule source regardless of tier-profile key drift (§3.1).

### 5.3 Port-source → target carry table (builder creates one item per row)

| Item | Source (verbatim) | Lines | Target | Owner of wrapper |
|---|---|---|---|---|
| CARRY-01 | tier_1_preschool.yaml | 94 | kb/tiers/tier_1.yaml | R4 (data) |
| CARRY-02 | tier_2_early_elementary.yaml | 84 | kb/tiers/tier_2.yaml | R4 |
| CARRY-03 | tier_3_middle_elementary.yaml | 87 | kb/tiers/tier_3.yaml | R4 |
| CARRY-04 | tier_5_young_adult.yaml | 87 | kb/tiers/tier_5.yaml | R4 |
| CARRY-05 | universal_mappings.yaml | 56 | kb/adaptation-mapping/universal-mappings.yaml | R4 |
| CARRY-06 | tolkien_mapping.yaml | 81 | kb/adaptation-mapping/tolkien-mapping.yaml (via onboarding copy of template) | R4 |
| CARRY-07 | thematic.yaml | 90 | /adaptation-rules/resources/thematic.md (fenced) | R2 wraps, R4 data |
| CARRY-08 | character.yaml | 77 | /adaptation-rules/resources/character.md (fenced) | R2 wraps, R4 data |
| CARRY-09 | work_mapping_template.yaml | 60 | templates/work-mapping-template.yaml | R4 |
| — | (native, no source) | — | kb/adaptations/<work>/tier-N/{continuity,decisions,canon-delta}.md + analysis.yaml/adapted.md | R3 writes, R4 format |

### 5.4 Cross-track boundaries (no duplication)
- **R2** owns the reader skills (`/adaptation-tiers`, `/adaptation-rules`, `/source-fidelity`)
  incl. the key-tolerant lookup (§1.3), tier_4 interpolation (§1.4), cascade algorithm (§2.4),
  and the md wrappers for P7/P8. **R4 supplies only the DATA those skills key against.**
- **R3** owns the `chronicler` agent body; **R4 owns the graft-G1 file FORMATS** it writes (§4).
- **R5/R6** own boundary contract + proof gate; **R4 supplies the invariants (I-1/I-2/I-3)**
  they enforce (§4.6).

**Status:** Complete.
