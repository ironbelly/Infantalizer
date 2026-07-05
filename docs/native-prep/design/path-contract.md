---
title: "Path Contract (resource spec)"
parent: DESIGN.md
status: draft
ships_as: laf-adaptation/skills/prep/resources/path-contract.md
---

# Path Contract

> **This is the design spec for the resource that ships at**
> `laf-adaptation/skills/prep/resources/path-contract.md`. It is the **single source of truth** for the
> prep-package layout, imported by reference from (a) `/prep` §1, (b) `.claude/commands/laf/prep.md`, and
> (c) `.claude/commands/laf/rewrite.md`. No path is restated anywhere else (R3). The content below is the
> exact contract to author verbatim into the shipped resource.

---

## 1. Package location

Every `/laf:prep` run emits one package directory:

```
work/prep/<work-slug>/
```

`<work-slug>` is the lowercase slug derived from the title (e.g. `narnia`, `tolkien`). It is also the
`--work` argument to `/laf:rewrite`.

## 2. The 8 package files (fixed names, fixed order)

| File | Kind | Confidence track | Purpose |
|---|---|---|---|
| `00-work-context.md` | RESEARCH | context | author, era, genre, reception, source-access declaration (context track) |
| `10-challenges.yaml` | DERIVED | derived from 20 | typed challenge taxonomy + governing rule + per-tier strategy + `human_judgment_dimension` + compound-scene flags |
| `20-analysis-work-level.yaml` | SOURCE | text + context | work-level source-fidelity analysis; every fact confidence-tagged; `meaning`; `compound_scene` |
| `30-mapping.yaml` | DERIVED | `min(text,context)` | the derived `<work>` mapping (native input format) + top-level `meaning:` key |
| `40-prep-brief.md` | SYNTHESIS | — | human-readable package: decisions, cross-tier spine summary, answered questions |
| `50-greenlight.md` | GATE | — | greenlight checklist + user confirmations (`status: PENDING → CONFIRMED`) |
| `60-handoff-prompt.md` | HANDOFF | — | the exact paste-able `/laf:rewrite` prompt |
| `70-traceability.md` | DERIVED | — | every artifact + mapping entry → derived-from facts + gap-closed + confidence (human/greenlight audit only) |

File schemas are defined in [`package-schemas.md`](package-schemas.md).

## 3. Promotion targets (on greenlight — dual-form)

On `50-greenlight.md` → `CONFIRMED`, `30-mapping.yaml` is promoted via `/kb-management` to **two** targets,
each in its layer's house style:

```
0.1 layer (6-key form — KEEPS top-level meaning:):
    laf-adaptation/kb/adaptation-mapping/<work-slug>-mapping.yaml     # HYPHEN, e.g. narnia-mapping.yaml

root v1.0 (5-key form — meaning: STRIPPED to preserve the frozen schema, R14):
    config/concept_mapping/templates/<work-slug>_mapping.yaml          # UNDERSCORE, e.g. narnia_mapping.yaml
```

- **Underscore vs hyphen is intentional** and matches each layer's existing files (verified:
  `config/concept_mapping/templates/tolkien_mapping.yaml`, `kb/adaptation-mapping/tolkien-mapping.yaml`).
- The **root copy is the 5-key schema** (`work_metadata, characters, concepts, key_scenes,
  master_translation_table`) with `meaning:` removed — root has no meaning concept and its schema is frozen
  (`ADDING_NEW_WORKS.md` step 6; R14). The **0.1 kb copy keeps `meaning:`** so the rewrite `muse` reads it
  as data (D6).

## 4. `rewrite_phase_reads` (the hardcoded read-set)

`/laf:rewrite --work <slug>` reads **exactly** these three files, by hardcoded path, no other arguments:

```
work/prep/<slug>/30-mapping.yaml
work/prep/<slug>/40-prep-brief.md
work/prep/<slug>/10-challenges.yaml
```

It also confirms `work/prep/<slug>/50-greenlight.md` shows `status: CONFIRMED` before handing to `muse`.
It does **not** read `70-traceability.md` (human/greenlight audit only, Q2).

## 5. Write-ownership

| Path | Written by |
|---|---|
| `work/prep/<slug>/*` | `prep-cordinator` (prep phase) |
| `kb/adaptation-mapping/<slug>-mapping.yaml` | `/kb-management` on greenlight (prep phase) |
| `config/concept_mapping/templates/<slug>_mapping.yaml` | `/kb-management` on greenlight (prep phase) |
| `kb/canon/*`, `kb/adaptations/<slug>/tier-*/…` | `chronicler` (rewrite phase — NOT the prep phase) |

The prep phase never writes canon or per-tier adaptation state; that boundary belongs to the rewrite
phase's `chronicler`.
