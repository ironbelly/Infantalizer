# Path Contract

> Single source of truth for the prep-package layout, promotion targets, rewrite-phase read-set, and
> write-ownership. Imported by reference from (a) `prep` SKILL.md §1, (b) `.claude/commands/laf/prep.md`,
> and (c) `.claude/commands/laf/rewrite.md`. No path is restated anywhere else.

## 1. Package location

Every `/laf:prep` run emits one package directory:

```
work/prep/<work-slug>/
```

`<work-slug>` is the lowercase slug derived from the title (e.g. `tolkien`). It is also the `--work`
argument to `/laf:rewrite`.

**Slug rule:** lowercase; the recognizable short work name; spaces/punctuation → hyphens or dropped
(e.g. leading articles dropped). e.g. "The Lord of the Rings" → `tolkien` (recognizable short author
handle, lowercased); "The Lion, the Witch and the Wardrobe" → `narnia`.

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

## 3. Promotion targets (on greenlight — dual-form)

On `50-greenlight.md` → `CONFIRMED`, the **`prep-cordinator` itself performs the dual-form transform** on
`30-mapping.yaml` (per the rule below) and writes **two** targets, each in its layer's house style. It then
registers the kb copy via `/kb-management` (kb-lifecycle write); the transform itself is the coordinator's,
not `/kb-management`'s.

```
0.1 layer (6-key form — KEEPS top-level meaning:):
    laf-adaptation/kb/adaptation-mapping/<work-slug>-mapping.yaml      # HYPHEN, e.g. tolkien-mapping.yaml

root v1.0 (5-key form — meaning: STRIPPED to preserve the frozen schema):
    config/concept_mapping/templates/<work-slug>_mapping.yaml          # UNDERSCORE, e.g. tolkien_mapping.yaml
```

- **Underscore vs hyphen is intentional** and matches each layer's existing files.
- The **root copy is the 5-key schema** (`work_metadata, characters, concepts, key_scenes,
  master_translation_table`) with `meaning:` removed — root has no meaning concept and its schema is frozen.
  The **0.1 kb copy keeps `meaning:`** so the rewrite `muse` reads it as data.
- The `_confidence` annotation keys are 0.1-only diagnostics; the root 5-key copy also drops them, so it
  validates byte-identically against the shipped root schema shape.

**Runtime greenlight ownership note:** these two files do NOT exist before a `/laf:prep` run reaches
greenlight. They are RUNTIME outputs of the prep-cordinator STAGE 7 step — never hand-authored at build
time. The coordinator performs the §3 dual-form transform and writes both files; the `/kb-management`
call registers the kb copy (the kb-lifecycle write). See §5 (Form-transform operator).

## 4. `rewrite_phase_reads` (the hardcoded read-set)

`/laf:rewrite --work <slug>` reads **exactly** these three files, by hardcoded path, no other arguments:

```
work/prep/<slug>/30-mapping.yaml
work/prep/<slug>/40-prep-brief.md
work/prep/<slug>/10-challenges.yaml
```

It also confirms `work/prep/<slug>/50-greenlight.md` shows `status: CONFIRMED` before handing to `muse`.
It does **not** read `70-traceability.md` (human/greenlight audit only).

## 5. Write-ownership

| Path | Written by |
|---|---|
| `work/prep/<slug>/*` | `prep-cordinator` (prep phase) |
| `kb/adaptation-mapping/<slug>-mapping.yaml` | `prep-cordinator` performs the §3 dual-form transform on greenlight (prep phase); `/kb-management` registers the kb copy |
| `config/concept_mapping/templates/<slug>_mapping.yaml` | `prep-cordinator` performs the §3 dual-form transform on greenlight (prep phase) |
| `kb/canon/*`, `kb/adaptations/<slug>/tier-*/…` | `chronicler` (rewrite phase — NOT the prep phase) |

The prep phase never writes canon or per-tier adaptation state; that boundary belongs to the rewrite phase's
`chronicler`.

**Form-transform operator (greenlight).** The `prep-cordinator` — the agent that loads this contract — is
the operator that performs the §3 dual-form transform on greenlight: it applies the two-target / `meaning:`
strip / `_confidence` strip / hyphen-vs-underscore rules defined in §3, writing both promoted files itself.
`/kb-management` provides the kb-lifecycle write (the registry acceptance of the promoted mapping); it does
not itself perform the 6-key↔5-key transform.
