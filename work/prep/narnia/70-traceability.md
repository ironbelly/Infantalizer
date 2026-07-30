# Traceability — The Lion, the Witch and the Wardrobe (narnia)

> Consumer: HUMAN review + the greenlight decision only (Q2). The rewrite-phase `muse` does NOT
> read this; `muse` reads `30-mapping.yaml`'s inline per-entry confidence.

## Artifact provenance

| Artifact | Derived from | Gap closed | Confidence |
|---|---|---|---|
| `00-work-context.md` | web-researcher dispatch (secondary sources) + novel metadata | context track (R6 ceiling) | PROBABLE ceiling |
| `20-analysis-work-level.yaml` | `Books/LWW/...Wardrobe...html` (FULL access, Phase-0 PASSED, read end-to-end) | text track (Q1) | CERTAIN (min across essentials) |
| `10-challenges.yaml` | derived from `20` + prep §2 taxonomy | challenge classification (R7) | per-type (text CERTAIN, context PROBABLE) |
| `30-mapping.yaml` | derived from `20` + `10` | scored mapping (eval gap #3) | per-entry `eff` |
| `40-prep-brief.md` | synthesis over `10/20/30` + gate answers | — | n/a (synthesis) |
| `50-greenlight.md` | checklist over the package | gate (Q4) | PENDING → (CONFIRMED on user action) |
| `60-handoff-prompt.md` | `path-contract.md §4` `rewrite_phase_reads` | handoff | n/a |
| `70-traceability.md` | this file | provenance matrix (R13) | n/a |
| kb 6-key promoted copy | `30-mapping.yaml` (dual-form §3) | dual-form promotion (C2) | per-entry `eff` (on greenlight) |
| root 5-key promoted copy | `30-mapping.yaml` minus `meaning:`/`_confidence` | dual-form promotion (C2) | frozen 5-key schema (on greenlight) |

## Mapping entry ledger

One row per `30-mapping.yaml` entry → derived-from facts + effective confidence + any DEFAULTED question.

| Mapping entry | Derived from (fact) | text | context | eff | DEFAULTED? |
|---|---|---|---|---|---|
| `meaning:` | 20 §meaning + 20 §summary + the Stone Table events (seq 13–14) + Deep/Deeper Magic | CERTAIN | PROBABLE | PROBABLE | resolved — allegory-stance gate skipped (DEFAULTED), then OVERRIDDEN at greenlight to allegory-as-reception |
| `work_metadata.title` | declared input + 20 §essentials.title | CERTAIN | CERTAIN | CERTAIN | no |
| `work_metadata.author` | declared input + 20 §metadata.author | CERTAIN | CERTAIN | CERTAIN | no |
| `work_metadata.key_challenges[*]` | 10-challenges types | CERTAIN | PROBABLE | PROBABLE | resolved — see `meaning:` row (allegory-stance overridden) |
| `characters.aslan.*` | 20 §characters (Aslan) + 20 events seq 12–16 | CERTAIN | PROBABLE | PROBABLE | resolved — sacrifice-and-return ANSWERED; allegory-stance overridden (reception) |
| `characters.white_witch.*` | 20 §characters (White Witch) + 20 events seq 8,12,13,16 | CERTAIN | PROBABLE | PROBABLE | no — petrification ANSWERED |
| `characters.edmund.*` | 20 §characters (Edmund) + 20 events seq 4,8,11,16,17 | CERTAIN | PROBABLE | PROBABLE | no — psychological-collapse ANSWERED (default) |
| `characters.lucy.*` | 20 §characters (Lucy) + 20 events seq 2,3,13,17 | CERTAIN | PROBABLE | PROBABLE | no |
| `characters.peter.*` | 20 §characters (Peter) + 20 events seq 11,16,17 | CERTAIN | PROBABLE | PROBABLE | no — mass-warfare ANSWERED |
| `characters.susan.*` | 20 §characters (Susan) + 20 events seq 13,17 | CERTAIN | PROBABLE | PROBABLE | no |
| `characters.mr_tumnus.*` | 20 §characters (Tumnus) + 20 events seq 2,6,15 | CERTAIN | PROBABLE | PROBABLE | no |
| `concepts.the_wardrobe_threshold.*` | 20 §essentials.structure + 20 events seq 2,5,17 | CERTAIN | PROBABLE | PROBABLE | no |
| `concepts.eternal_winter.*` | 20 §summary + 20 §transformation_flags.abstract | CERTAIN | PROBABLE | PROBABLE | no |
| `concepts.the_deep_magic.*` | 20 events seq 12 + 20 §transformation_flags.abstract | CERTAIN | PROBABLE | PROBABLE | resolved — allegory-stance overridden (reception) |
| `concepts.the_deeper_magic.*` | 20 events seq 14 + 20 §transformation_flags.abstract | CERTAIN | PROBABLE | PROBABLE | resolved — allegory-stance overridden (reception) |
| `concepts.petrification_to_stone.*` | 20 §transformation_flags.death + 20 events seq 8,10,15 | CERTAIN | PROBABLE | PROBABLE | no — petrification ANSWERED |
| `key_scenes.lucy_enters_narnia.*` | 20 events seq 2,3 | CERTAIN | PROBABLE | PROBABLE | no — omission-honor-set ANSWERED |
| `key_scenes.edmunds_betrayal.*` | 20 events seq 4 + 20 §characters.edmund | CERTAIN | PROBABLE | PROBABLE | no — psychological-collapse ANSWERED |
| `key_scenes.aslans_sacrifice.*` | 20 events seq 13 + 10 compound_scenes | CERTAIN | PROBABLE | PROBABLE | resolved — sacrifice-and-return ANSWERED; allegory-stance overridden (reception) |
| `key_scenes.aslans_resurrection.*` | 20 events seq 14 + 10 compound_scenes | CERTAIN | PROBABLE | PROBABLE | resolved — allegory-stance overridden (reception) |
| `key_scenes.the_battle_of_beruna.*` | 20 events seq 16 + 10 compound_scenes | CERTAIN | PROBABLE | PROBABLE | no — mass-warfare ANSWERED |
| `key_scenes.coronation_and_return.*` | 20 events seq 17 | CERTAIN | PROBABLE | PROBABLE | no — omission-honor-set ANSWERED |
| `master_translation_table[*]` | 20 §events + 10 per_tier_strategy | CERTAIN | PROBABLE | PROBABLE | per-row, see allegory/sacrifice rows |
| `compound_scenes[Stone Table sacrifice].reconciliation` | §2.1 protocol on 20 §compound_scenes | CERTAIN | PROBABLE | PROBABLE | resolved (sacrifice ANSWERED; allegory overridden) |
| `compound_scenes[Stone Table resurrection].reconciliation` | §2.1 protocol on 20 §compound_scenes | CERTAIN | PROBABLE | PROBABLE | resolved — allegory-stance overridden (reception) |
| `compound_scenes[Battle of Beruna].reconciliation` | §2.1 protocol on 20 §compound_scenes | CERTAIN | PROBABLE | PROBABLE | no — mass-warfare ANSWERED |

## DEFAULTED questions (resolved at greenlight)

**One question was skipped at the Stage-5 gate → recorded DEFAULTED, then OVERRIDDEN at greenlight.
No question remains DEFAULTED in the promoted package:**

| Challenge | Question (abridged) | Gate outcome | Greenlight resolution |
|---|---|---|---|
| allegory-stance | How should the adaptation treat the allegory vs Lewis's "supposal" across tiers? | DEFAULTED (skipped) → supposal default applied provisionally | **OVERRIDDEN to allegory-as-reception.** The allegorical reading is surfaced openly at T3+ (Aslan=Christ; Stone Table=Passion/Resurrection; Deep/Deeper Magic=Law/Gospel), kept implicit at T1–T2, never stripped. The package (`10/30/40/70`) was re-folded for this stance before promotion. |

All six other human-judgment questions (sacrifice-and-return, mass-warfare, omission-honor-set,
petrification-body-horror, target-age-nuance, psychological-collapse) were **ANSWERED** in
`40-prep-brief.md § Answered questions` — each confirmed the coordinator default.

## Promotion provenance

> Executed by the coordinator itself at STAGE 7 **only on greenlight CONFIRM** (status: PENDING now).

| Target | Form | `meaning:` | `_confidence` | Source |
|---|---|---|---|---|
| `laf-adaptation/kb/adaptation-mapping/narnia-mapping.yaml` | 6-key, hyphen (0.1) | KEPT | KEPT | `30-mapping.yaml` (verbatim copy) |
| `config/concept_mapping/templates/narnia_mapping.yaml` | 5-key, underscore (root) | STRIPPED | STRIPPED | `30-mapping.yaml` minus top-level `meaning:` and per-entry `_confidence` |

Both targets are RUNTIME outputs of the STAGE 7 transform; neither is hand-authored at build time
(per `path-contract.md` §3 runtime-ownership note). The kb copy keeps `meaning:` so `muse` reads it
as data; the root copy drops `meaning:` and `_confidence` so it validates byte-identically against the
shipped 5-key root schema shape. The root target **overwrites** the existing build-time placeholder
`narnia_mapping.yaml`; the kb target is **created** (no prior `narnia-mapping.yaml` existed).
