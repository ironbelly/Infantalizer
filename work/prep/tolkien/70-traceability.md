# Traceability — The Lord of the Rings (tolkien)

> Consumer: HUMAN review + the greenlight decision only (Q2). The rewrite-phase `muse` does NOT
> read this; `muse` reads `30-mapping.yaml`'s inline per-entry confidence.

## Artifact provenance

| Artifact | Derived from | Gap closed | Confidence |
|---|---|---|---|
| `00-work-context.md` | web-researcher dispatch (secondary sources) + fixture metadata | context track (R6 ceiling) | PROBABLE ceiling |
| `20-analysis-work-level.yaml` | `laf-adaptation/source/tolkien/ch-01.txt` (FULL access, Phase-0 PASSED) | text track (Q1) | PROBABLE (min across essentials) |
| `10-challenges.yaml` | derived from `20` + prep §2 taxonomy | challenge classification (R7) | per-type, see flag column |
| `30-mapping.yaml` | derived from `20` + `10` | scored mapping (eval gap #3) | per-entry `eff` |
| `40-prep-brief.md` | synthesis over `10/20/30` + greenlight | — | n/a (synthesis) |
| `50-greenlight.md` | checklist over the package | gate (Q4) | CONFIRMED |
| `60-handoff-prompt.md` | `path-contract.md §4` `rewrite_phase_reads` | handoff | n/a |
| `70-traceability.md` | this file | provenance matrix (R13) | n/a |
| kb 6-key promoted copy | `30-mapping.yaml` (dual-form §3) | dual-form promotion (C2) | per-entry `eff` |
| root 5-key promoted copy | `30-mapping.yaml` minus `meaning:`/`_confidence` | dual-form promotion (C2) | frozen 5-key schema |

## Mapping entry ledger

One row per `30-mapping.yaml` entry → derived-from facts + effective confidence + any DEFAULTED question.

| Mapping entry | Derived from (fact) | text | context | eff | DEFAULTED? |
|---|---|---|---|---|---|
| `meaning:` | 20 §meaning + 20 §summary + the sun-returns event (seq 7) | PROBABLE | PROBABLE | PROBABLE | no — ANSWERED (allegory-stance gate) |
| `work_metadata.title` | declared input | CERTAIN | CERTAIN | CERTAIN | no |
| `work_metadata.author` | declared input | CERTAIN | CERTAIN | CERTAIN | no |
| `work_metadata.key_challenges[*]` | 10-challenges types | CERTAIN | PROBABLE | PROBABLE | no |
| `characters.sauron.*` | 20 §characters (Sauron, offstage will) | CERTAIN | PROBABLE | PROBABLE | no |
| `characters.denethor.*` | 20 §characters + 20 events seq 2 | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (psychological-collapse gate) |
| `characters.theoden.*` | 20 §characters + 20 events seq 3,4 | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (sacrifice-and-return gate) |
| `characters.eowyn.*` | 20 §characters + 20 events seq 5 | CERTAIN | PROBABLE | PROBABLE | no |
| `characters.nazgul.*` | 20 §characters + 20 events seq 4 | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (petrification-body-horror gate) |
| `concepts.the_grey_city.*` | 20 §events seq 6,7 | CERTAIN | PROBABLE | PROBABLE | no |
| `concepts.saurons_shadow.*` | 20 §events seq 1 + 20 §transformation_flags.abstract | CERTAIN | PROBABLE | PROBABLE | no |
| `concepts.the_host.*` | 20 §events seq 1 | CERTAIN | PROBABLE | PROBABLE | no |
| `concepts.the_long_dark.*` | 20 §events seq 2 + 20 §uncertainties | CERTAIN | PROBABLE | PROBABLE | no |
| `key_scenes.siege_of_the_grey_city.*` | 20 §events seq 1–7 + 10 compound_scenes | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (mass-warfare + omission-honor-set gates) |
| `key_scenes.theodens_fall_and_eowyns_stand.*` | 20 §events seq 3–5 + 10 compound_scenes | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (sacrifice-and-return gate) |
| `key_scenes.denethors_collapse.*` | 20 §events seq 2 | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (psychological-collapse gate) |
| `key_scenes.the_sun_returns.*` | 20 §events seq 7 | CERTAIN | PROBABLE | PROBABLE | no — ANSWERED (allegory-stance gate) |
| `master_translation_table[*]` | 20 §events + 10 per_tier_strategy | CERTAIN | PROBABLE | PROBABLE | no |
| `compound_scenes[Siege].reconciliation` | §2.1 protocol applied to 20 §compound_scenes | CERTAIN | PROBABLE | PROBABLE | no |
| `compound_scenes[Théoden/Éowyn].reconciliation` | §2.1 protocol applied to 20 §compound_scenes | CERTAIN | PROBABLE | PROBABLE | no |

## DEFAULTED questions

None. The Phase-3 SMOKE PROVE auto-answers the gate; every human-judgment question is recorded as
ANSWERED in `40-prep-brief.md § Answered questions`. No `[skip]` was taken.

## Promotion provenance

| Target | Form | `meaning:` | Source |
|---|---|---|---|
| `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` | 6-key, hyphen (0.1) | KEPT | `30-mapping.yaml` (verbatim copy) |
| `config/concept_mapping/templates/tolkien_mapping.yaml` | 5-key, underscore (root) | STRIPPED | `30-mapping.yaml` minus top-level `meaning:` and per-entry `_confidence` |

Both targets are RUNTIME outputs of this STAGE 7 transform; neither was hand-authored at build time
(per `path-contract.md` §3 runtime-ownership note). The kb copy keeps `meaning:` so `muse` reads it
as data; the root copy drops `meaning:` and `_confidence` so it validates byte-identically against
the shipped 5-key root schema shape.
