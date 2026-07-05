---
title: "Native LAF Adaptation-Prep Phase — Design Specification"
domain: architecture
source_requirements: ../brainstorm-out/merged-requirements.md
status: draft
created: 2026-07-04
boundary_contract: laf-adaptation/scripts/check_boundary.py
next_step: /sc:implement @docs/native-prep/design/DESIGN.md
companions:
  - prep-agent-schemas.md
  - prep-skill-specs.md
  - path-contract.md
  - package-schemas.md
  - boundary-verification.md
---

# Native LAF Adaptation-Prep Phase — Design Specification

This is the concrete, buildable design for the **native adaptation-prep phase** whose requirements are
fixed in [`../brainstorm-out/merged-requirements.md`](../brainstorm-out/merged-requirements.md) (R1–R14).
It turns those requirements into agent/skill/command schemas, package file formats, a path contract, and a
boundary-check verification plan — the artifacts `/sc:implement` will build.

The requirements are **settled and not re-litigated here.** This pack specifies *how* to build the phase
against the **live** `laf-adaptation/` 0.1 tree (ground-truthed 2026-07-04), and records — precisely —
the small set of places where a literal reading of the spec collides with the real code, together with the
grounded resolution for each.

## Companion specs (this directory)

| Spec | Contents |
|---|---|
| **DESIGN.md** (this file) | System overview, component boundaries, distribution layout, 8-stage data-flow, sequence, R-traceability, phase gates, spec-correction log |
| [`prep-agent-schemas.md`](prep-agent-schemas.md) | `prep-cordinator` frontmatter + I/O + 8-stage body outline; the `analyst` (NATIVE) and `tier-coordinator` (BUILD-NEW) body-edit diffs; the two `.claude/commands/laf/` command specs |
| [`prep-skill-specs.md`](prep-skill-specs.md) | `SKILL.md` body outlines for the two new NATIVE skills: `prep` (8 sections) and `thematic-fidelity` |
| [`path-contract.md`](path-contract.md) | The single-source-of-truth path layout resource shipped at `skills/prep/resources/path-contract.md` |
| [`package-schemas.md`](package-schemas.md) | File-format schemas for all 8 package files `00..70`, incl. the `10-challenges.yaml` taxonomy + `human_judgment_dimension` flags, the `30-mapping.yaml` `meaning:` extension + dual-form promotion, and the seed exemplar set |
| [`boundary-verification.md`](boundary-verification.md) | The corrected boundary-checked change-list, `VENDOR.md` row deltas, and the `check_boundary.py` verification plan |

---

## 1. System Overview

The prep phase sits **upstream of the existing per-chapter 11-step workflow** (`analyst → muse → writer →
… → chronicler`). It takes a novel title, autonomously researches and analyzes the work at **work
granularity**, derives a confidence-scored `<work>_mapping.yaml`, classifies the work's adaptation
challenges, asks only the human-judgment questions the taxonomy flags, emits a fixed-path package, gates on
greenlight, and prints the exact `/laf:rewrite` prompt for the next session.

It is composed **entirely** of boundary-safe additions to the **0.1 layer** — no adopted-agent body is
edited, and root v1.0 gets only a documentation pointer (R14).

### 1.1 What is added (provenance-classified)

```
                     NEW NATIVE                          NATIVE-BODY EDIT        BUILD-NEW-BODY EDIT
        ┌──────────────────────────────────────────┬──────────────────────┬──────────────────────┐
AGENTS  │ prep-cordinator            (new file)     │ analyst  (+meaning,  │ tier-coordinator     │
        │                                           │  +compound_scene,    │  (+Check D            │
        │                                           │  +work-level mode)   │  meaning-preservation)│
        ├──────────────────────────────────────────┼──────────────────────┴──────────────────────┤
SKILLS  │ prep            (new dir, 8 sections)      │  (adaptation-rules gains seed exemplars      │
        │ thematic-fidelity (new dir)               │   under its resources/ — NATIVE, glob-covered)│
        ├──────────────────────────────────────────┴──────────────────────────────────────────────┤
COMMANDS│ .claude/commands/laf/prep.md  ·  .claude/commands/laf/rewrite.md   (harness surface, NOT  │
        │                                                                     in the VENDOR manifest)│
        ├───────────────────────────────────────────────────────────────────────────────────────────┤
DOCS    │ docs/guides/ADDING_NEW_WORKS.md   (+ one pointer paragraph → "use 0.1's /laf:prep")         │
        └───────────────────────────────────────────────────────────────────────────────────────────┘
```

- **`writer.md` is NOT touched** (D6). The meaning-preservation concept reaches the rewrite-phase `muse`
  as **data** — the `meaning:` top-level key in the promoted `30-mapping.yaml` — with **zero** adopted-body
  edits. `muse` is `ADOPTED-CLEAN` and cannot receive a skill line (`ADOPTED-PATCHED` is reserved for
  `writer.md` only, enforced by `check_boundary.py` Rule C′).
- The `analyst` and `tier-coordinator` edits are boundary-safe because both files carry **NO_HASH (`—`)**
  rows in `VENDOR.md` (NATIVE / BUILD-NEW respectively — `VENDOR.md` lines 111 & 117); their bodies are not
  hash-pinned.

### 1.2 The NATIVE spine it reuses, unchanged

The `prep-cordinator` orchestrates the existing spine rather than reinventing it:

| Reused component | Provenance | Role in prep |
|---|---|---|
| `web-researcher` agent | ADOPTED | Context track (secondary sources) → `00-work-context.md` |
| `analyst` agent | NATIVE | Text track at work granularity → `20-analysis-work-level.yaml` |
| `tier-coordinator` agent | BUILD-NEW | (rewrite phase) cross-tier reconciliation, now with Check D |
| `/source-fidelity` skill | NATIVE | Phase-0 access gate + CERTAIN/PROBABLE/UNCERTAIN tags |
| `/adaptation-tiers` skill | NATIVE | Tier axis + T4 interpolation vocabulary |
| `/adaptation-rules` skill | NATIVE | Transform rules + (new) seed exemplars |
| `/kb-management` skill | ADOPTED | Promotion of the mapping into `kb/` + root `templates/` |

---

## 2. Distribution Layout (where every new file lands)

```
laf-adaptation/
├── agents/
│   └── prep-cordinator.md                     # NEW — NATIVE orchestrator (R4)
├── skills/
│   ├── prep/                                  # NEW — NATIVE skill (R5)
│   │   ├── SKILL.md                           #   8 sections (prep-skill-specs.md)
│   │   └── resources/
│   │       └── path-contract.md               #   single source of truth for paths (R3)
│   ├── thematic-fidelity/                     # NEW — NATIVE skill (R5)
│   │   └── SKILL.md                           #   meaning-preservation concept
│   └── adaptation-rules/                      # EXISTING NATIVE skill
│       └── resources/
│           └── exemplars/                     # NEW — NATIVE seed exemplars (R13)
│               ├── sacrifice-and-return.md
│               ├── betrayal-and-redemption.md
│               └── petrification-body-horror.md
├── agents/analyst.md                          # EDIT — NATIVE body (R10, R11)
├── agents/tier-coordinator.md                 # EDIT — BUILD-NEW body (R10 Check D)
└── VENDOR.md                                  # 3 new rows auto-written by --init (§5)

.claude/commands/laf/                          # NEW — harness surface (outside boundary contract)
├── prep.md                                    #   /laf:prep    (R1)
└── rewrite.md                                 #   /laf:rewrite (R9)

work/prep/<work-slug>/                         # RUNTIME output — the 8-file package (R2, path-contract.md)
└── {00-work-context.md … 70-traceability.md}

config/concept_mapping/templates/<work>_mapping.yaml   # ROOT promotion target (5-key form, meaning stripped)
laf-adaptation/kb/adaptation-mapping/<work>-mapping.yaml # 0.1 promotion target (6-key form, meaning kept)

docs/guides/ADDING_NEW_WORKS.md                # EDIT — one pointer paragraph (R14)
```

> **Path fidelity note.** Root templates use `<work>_mapping.yaml` (**underscore**, e.g.
> `tolkien_mapping.yaml` — verified in `config/concept_mapping/templates/`). The 0.1 kb layer uses
> `<work>-mapping.yaml` (**hyphen**, e.g. `tolkien-mapping.yaml` — verified in
> `kb/adaptation-mapping/`). The promotion step honors each layer's house style; do not normalize.

---

## 3. Data Flow — the 8-stage prep pipeline

Rendered as a data-flow with the agent that owns each stage and the artifact it reads/writes. HALT points
are prompt-emitted blocks (LangGraph-interrupt semantics — **no runtime**; enrichment §2).

```
   /laf:prep "<novel>" [--source <path>]        [.claude/commands/laf/prep.md]
            │  delegates to prep-cordinator (opus)
            ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 1 — RESEARCH                                             [prep-cord]  │
 │  a. Elicit/confirm source path as a REQUIRED input (Q1) — not a question.  │
 │  b. Apply /source-fidelity Phase-0 at work level:                          │
 │        SOURCE ACCESS = NO-ACCESS  →  ABORT the whole prep (hard gate, R6). │
 │  c. Dispatch web-researcher (context track) → 00-work-context.md           │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 2 — ROADMAP                                             [prep-cord]  │
 │  Read 00 + prep-skill §2 taxonomy skeleton → prep task list;               │
 │  EXECUTE stages 3-4 autonomously (no user interaction yet).                │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 3 — ANALYZE + CLASSIFY                        [prep-cord → analyst]  │
 │  Dispatch analyst at WORK granularity (text track):                        │
 │     → 20-analysis-work-level.yaml  (confidence-tagged; +meaning;           │
 │        +compound_scene flags)                                              │
 │  Apply prep-skill §2 challenge taxonomy:                                    │
 │     → 10-challenges.yaml  (typed challenges + governing rule +             │
 │        per-tier strategy + human_judgment_dimension + compound_scene)      │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 4 — AUTHOR MAPPING                                       [prep-cord]  │
 │  prep-skill §4 derives 30-mapping.yaml from 20 + 10:                        │
 │     per-entry effective confidence = min(text_confidence, context_conf.)   │
 │     top-level meaning: key added (work-level meaning + confidence)          │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 5 — QUESTION GATE                                        [prep-cord]  │
 │  Emit `## Questions for the user` — coverage-constrained by                 │
 │  human_judgment_dimension (MUST ask flagged; MUST NOT ask deterministic).  │
 │  HALT. Resume on reply. [skip] → recorded DEFAULTED in 70-traceability.md. │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 6 — PACKAGE                                              [prep-cord]  │
 │  Write 40-prep-brief.md + 70-traceability.md; fold answers into 10/20/30.  │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 7 — GREENLIGHT                              [prep-cord → kb-mgmt]     │
 │  Write 50-greenlight.md (checklist); emit confirmation; HALT until CONFIRM.│
 │  On CONFIRM: promote 30-mapping.yaml (dual-form) via /kb-management →       │
 │     kb/adaptation-mapping/<work>-mapping.yaml  (6-key, meaning kept)        │
 │     config/concept_mapping/templates/<work>_mapping.yaml (5-key, stripped) │
 │  status: PENDING → CONFIRMED.                                               │
 └───────────┬────────────────────────────────────────────────────────────────┘
             ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ STAGE 8 — HANDOFF                                             [prep-cord]  │
 │  Write 60-handoff-prompt.md containing the literal:  /laf:rewrite --work <slug> │
 └───────────────────────────────────────────────────────────────────────────┘
             │
 ═══════════ NEXT SESSION ════════════════════════════════════════════════════
             ▼
   /laf:rewrite --work <slug>                    [.claude/commands/laf/rewrite.md]
     reads [30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml] by HARDCODED path
        (path-contract.md §rewrite_phase_reads — no arguments beyond --work)
     → hands to muse for chapter 1 (existing 11-step workflow; meaning-aware mapping in context)
```

### 3.1 The two-track anti-hallucination model (R6)

```
                     ┌──────────────── context track ─────────────────┐
   /laf:prep  ──────►│ web-researcher (ADOPTED)                        │──► 00-work-context.md
                     │   secondary sources; ceiling = PARTIAL/MEMORY   │    context_confidence
                     └─────────────────────────────────────────────────┘
                     ┌──────────────── text track ────────────────────┐
                     │ analyst (NATIVE) @ work granularity             │──► 20-analysis-work-level.yaml
                     │   novel TEXT (required input, Q1);              │    text_confidence
                     │   Phase-0 NO-ACCESS → ABORT; ceiling FULL/PARTIAL│    (MEMORY-BASED not acceptable
                     └─────────────────────────────────────────────────┘     at work level — source mandatory)

   Every 30-mapping.yaml entry carries text_confidence AND context_confidence.
   Effective confidence = min(text, context).  Because the text track is mandatory (never MEMORY),
   every mapping entry is at least text-grounded.
```

### 3.2 The two HALT gates (prompt-emitted, no runtime)

Both gates are **a prompt block the `prep-cordinator` emits, followed by a stop** — the same
"interrupt-and-resume" shape the enrichment (§2) grounds in LangGraph-interrupt semantics, implemented with
**no code**. Stage 5 halts for human-judgment answers; Stage 7 halts for greenlight confirmation. Neither
introduces a runtime, satisfying ADR-006 ("not software").

---

## 4. Traceability — every requirement → concrete artifact

| Req | What it demands | Concrete artifact (this pack) |
|---|---|---|
| R1 | Thin entry point; source required (Q1) | `.claude/commands/laf/prep.md` → delegates to `prep-cordinator`; Stage 1a elicits source as required input ([prep-agent-schemas.md](prep-agent-schemas.md)) |
| R2 | Fixed-path 8-file package + dual promotion | [`path-contract.md`](path-contract.md) + [`package-schemas.md`](package-schemas.md) |
| R3 | One path-contract doc, imported by reference | `skills/prep/resources/path-contract.md` referenced by prep §1, both commands |
| R4 | NATIVE orchestrator agent (opus) | `agents/prep-cordinator.md` ([prep-agent-schemas.md §1](prep-agent-schemas.md)) |
| R5 | Two NATIVE skills | `skills/prep/` + `skills/thematic-fidelity/` ([prep-skill-specs.md](prep-skill-specs.md)) |
| R6 | Two-track work-level analysis | §3.1 above; `web-researcher` + `analyst` work-level mode ([prep-agent-schemas.md §2](prep-agent-schemas.md)) |
| R7 | Coverage-constrained question gate | prep §5 rule + `human_judgment_dimension` flag table ([package-schemas.md §2](package-schemas.md)) |
| R8 | Greenlight gate + dual promotion | Stage 7; `50-greenlight.md` schema; `/kb-management` promotion ([package-schemas.md §6](package-schemas.md)) |
| R9 | Handoff prompt emission | `60-handoff-prompt.md`; `.claude/commands/laf/rewrite.md` ([prep-agent-schemas.md §5](prep-agent-schemas.md)) |
| R10 | Gap #1 meaning-preservation | `thematic-fidelity` skill + `analyst` `meaning:` field + `tier-coordinator` Check D + `meaning:` in promoted mapping ([prep-agent-schemas.md §3-4](prep-agent-schemas.md)) |
| R11 | Gap #2 compound-scene protocol | prep §2.1 + `analyst` `compound_scene` flag, baked into `10-challenges.yaml` ([package-schemas.md §2](package-schemas.md)) |
| R12 | Gap #3 derive+score the mapping | prep §4 derives `30-mapping.yaml`; per-entry `min(text,context)` scores quality ([package-schemas.md §4](package-schemas.md)) |
| R13 | Gap #4 exemplar library + contamination fix | `skills/adaptation-rules/resources/exemplars/*.md` (DERIVED-marked) + `70-traceability.md` ([package-schemas.md §7-8](package-schemas.md)) |
| R14 | Root parity OUT OF SCOPE | `ADDING_NEW_WORKS.md` pointer only; no root machinery; root promotion is a 5-key file, no `meaning:` ([boundary-verification.md](boundary-verification.md)) |

---

## 5. VENDOR.md manifest delta (auto-generated, not hand-edited)

`check_boundary.py --init` regenerates the manifest from disk (`agents/*.md` + `skills/*`). After the new
files land, `--init` deterministically writes **exactly three** new rows and touches nothing else:

> **Upstream-availability note (reconciles with [`boundary-verification.md §2`](boundary-verification.md)).**
> `--init` **hard-requires** `--upstream <checkout>` (it exits early otherwise). When a CWS upstream
> checkout at the pinned SHA is **not available** (the common case in this repo), do **not** run `--init`:
> instead **hand-add the three NATIVE rows** below to `VENDOR.md` and verify with plain Mode-V
> `check_boundary.py` (which PASSES — Rule F covers the new rows; Rules B/C are upstream-only). The rows
> are identical either way; `--init` is just the mechanized path when an upstream tree exists.

```
| agents/prep-cordinator.md       | NATIVE | — | — |     # classify(): agents/, not BUILD_NEW_AGENTS → NATIVE
| skills/prep/**                  | NATIVE | — | — |     # new skill dir, not upstream → NATIVE /** glob
| skills/thematic-fidelity/**     | NATIVE | — | — |     # new skill dir, not upstream → NATIVE /** glob
```

- `skills/prep/resources/path-contract.md` and `skills/adaptation-rules/resources/exemplars/*.md` need **no
  new rows** — they are covered by the `skills/prep/**` and existing `skills/adaptation-rules/**` NATIVE
  glob rows respectively.
- `agents/analyst.md` and `agents/tier-coordinator.md` rows are **unchanged** (`—` / `—`): editing a
  NO_HASH body does not alter its manifest row.
- The two commands are **NOT** in `VENDOR.md` (they live outside `laf-adaptation/`).

Full change-list, per-rule expectations, and the corrected boundary reasoning are in
[`boundary-verification.md`](boundary-verification.md).

---

## 6. Spec-correction log (literal spec vs. live code)

Four places where a literal reading of `merged-requirements.md` collides with the ground-truthed 0.1 tree.
Each resolution is grounded in a cited file and is the minimal boundary-respecting fix.

| # | Spec text | Ground truth | Resolution (this design) |
|---|---|---|---|
| C1 | Change-list #13: "VENDOR.md manifest rows for #1-#6" (incl. the two commands) | `VENDOR.md` governs only `laf-adaptation/`; `--init` regenerates rows solely from `agents/*.md` + `skills/*`, and `/laf:` slash commands only resolve from `.claude/commands/laf/` | **Commands live at `.claude/commands/laf/`, outside the boundary contract; NOT VENDOR-manifested.** Only 3 NATIVE rows are added (§5), all auto-generated. *(User-confirmed 2026-07-04.)* |
| C2 | R2 + R10: `30-mapping.yaml` carries a top-level `meaning:` key and is promoted to **both** root `templates/` and 0.1 `kb/` | Root's `<work>_mapping.yaml` is a frozen **5-key** schema (`work_metadata, characters, concepts, key_scenes, master_translation_table` — `ADDING_NEW_WORKS.md` step 6); R14 says root has **no** meaning concept | **Dual-form promotion.** The 0.1 `kb/` copy is the 6-key form (keeps `meaning:`). The root copy is the schema-conformant 5-key form (**`meaning:` stripped**) — preserving root's frozen schema and R14's "no root machinery." ([package-schemas.md §4](package-schemas.md)) |
| C3 | Q5 / change-list #7: exemplars go "inside the **adopted** `adaptation-rules/resources/`" | `adaptation-rules` is **NATIVE**, not adopted (`VENDOR.md` line 113: `skills/adaptation-rules/** | NATIVE`) | The concern about "muddying an adopted tree" is **moot**: exemplars are plain NATIVE additions under a NATIVE skill, covered by the existing `skills/adaptation-rules/**` glob row. **No new VENDOR row, no adopted-body risk.** ([boundary-verification.md](boundary-verification.md)) |
| C4 | R13: path `laf-adaptation/adaptation-rules/resources/exemplars/` | The skill dir is `laf-adaptation/skills/adaptation-rules/` (all skills live under `skills/`) | Corrected path: **`laf-adaptation/skills/adaptation-rules/resources/exemplars/<type>.md`** (matches change-list #7). |

Two additional design decisions internal to the code (not spec contradictions):

- **D-analyst-work-mode.** The `analyst` currently hardcodes chapter-granularity (`work/analysis/ch-<NN>.yaml`).
  Its NATIVE body edit (already required by R10/R11) additionally accepts `granularity ∈ {chapter, work}`
  and an explicit `out_path`, **both defaulting to today's behavior** so every existing per-chapter caller
  is byte-for-byte unaffected. Work mode writes `20-analysis-work-level.yaml`. ([prep-agent-schemas.md §3](prep-agent-schemas.md))
- **D-muse-untouched.** The rewrite `muse` reads `meaning:` as **data** from the promoted mapping; no skill
  line, no frontmatter change (D6). `muse` stays `ADOPTED-CLEAN`; the `/laf:rewrite` command body carries the
  "read the package, don't ask the user to restate" instruction.

---

## 7. Build phases & gates (design → implementation handoff)

| Phase | Deliverable | Gate |
|---|---|---|
| **P0. Skeleton** | Create `skills/prep/` (SKILL.md + resources/path-contract.md), `skills/thematic-fidelity/SKILL.md`, `agents/prep-cordinator.md`, `skills/adaptation-rules/resources/exemplars/*.md`. | Files parse; the 3 NATIVE rows in §5 are present in `VENDOR.md` — written by `check_boundary.py --init` when an upstream checkout is available, else **hand-added** (see §5 note) — and plain Mode-V `check_boundary.py` prints `PASS` with `--report` NATIVE = 8 |
| **P1. Body edits** | Apply `analyst` NATIVE diff (`meaning`, `compound_scene`, work-mode) and `tier-coordinator` BUILD-NEW diff (Check D). | Per-chapter `analyst`/`tier-coordinator` defaults unchanged; `check_boundary.py` (Mode V) green — Rules A/A′/C′/D still pass (no adopted body drift) |
| **P2. Commands** | Author `.claude/commands/laf/prep.md` + `rewrite.md`. | `/laf:prep` resolves and delegates to `prep-cordinator`; `/laf:rewrite` reads the 3 hardcoded paths |
| **P3. Prove (HARD GATE)** | Run `/laf:prep "The Lion, the Witch and the Wardrobe"` end-to-end (source = a readable text), through greenlight + handoff. | 8-file package written; `20` carries `meaning` + `compound_scene`; `30-mapping.yaml` per-entry `min(text,context)`; dual-form promotion (root 5-key, kb 6-key); `/laf:rewrite --work narnia` reads the package by hardcoded path; `check_boundary.py` green |
| **P4. Root pointer** | Add the `ADDING_NEW_WORKS.md` paragraph (R14). | No root machinery added; pointer only |

The **P3 hard gate** is the definition of "prep phase done."

## 8. Next step

```
/sc:implement @docs/native-prep/design/DESIGN.md
```

Implement P0→P4 in order; treat the five companion specs as the buildable source of truth. Run
`uv run python laf-adaptation/scripts/check_boundary.py` after P0, P1, and P3.
