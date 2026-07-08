---
title: "Native LAF Adaptation-Prep Phase — Design Spec (merged requirements)"
topic: "Design the native LAF adaptation-prep phase"
domain: architecture
strategy: systematic
depth: deep
proposals_merged: 3
convergence_score: 0.85
adversarial_status: PASS
base_proposal: A (architect)
grafts: [B (analyzer rigor), C (scribe consolidation)]
handoff_target: design
created: 2026-07-04
standardized_inputs:
  - docs/native-prep/00-seed-brief.md
  - docs/native-prep/10-findings-and-evaluation.md
  - docs/native-prep/20-objective-user-story.md
  - docs/native-prep/30-current-framework-map.md
enrichment:
  - docs/native-prep/brainstorm-out/enrichment/research-deep.md
boundary_contract: laf-adaptation/scripts/check_boundary.py
---

# Native LAF Adaptation-Prep Phase — Merged Design Spec

> This is the merged output of a 3-proposal adversarial brainstorm (architect / analyzer / scribe). It is
> a REQUIREMENTS SPECIFICATION for the design phase, not implementation. Every change is classified
> ADOPTED-safe / NATIVE / BUILD-NEW and checked against the boundary contract. Grounded in the four
> standardized inputs + the research enrichment.

## 0. Executive summary

The prep phase is **a new NATIVE command + a new NATIVE orchestrator agent + 2 new NATIVE skills + a
referenced path-contract doc + a small set of additive edits to NATIVE/BUILD-NEW bodies**, grafted onto
the **0.1 layer only**. Root v1.0 gets a pointer stub and no new machinery (ADR-006). The orchestrator
reuses the existing NATIVE spine (`analyst`, `web-researcher`, `tier-coordinator`, `kb-management`)
unchanged except for NATIVE/BUILD-NEW body edits where new capability attaches. **No ADOPTED agent body
is edited** — meaning-preservation reaches adopted agents via the promoted mapping file, not via new
skill lines (D6).

**One sentence:** *The user runs `/laf:prep "<novel>"`; a NATIVE `prep-cordinator` agent autonomously
researches the work (two-track), classifies its adaptation challenges, derives a confidence-tagged
work-mapping, asks only the questions the challenge taxonomy flags as human-judgment, emits a fixed-path
package, confirms greenlight, and prints the exact `/laf:rewrite` prompt for the next session — which
reads that package by hardcoded path.*

## 1. Requirements (enumerated)

### R1 — Thin entry point
A NATIVE command `/laf:prep "<novel title>" [--source <path>]` whose body delegates to the
`prep-cordinator` agent. The user types only the title (and optionally a source path). The novel **text
is a required input** (decision Q1 = Yes): if `--source` is omitted, the orchestrator's FIRST act is to
elicit the source path/URL from the user as a **required input** (not a clarifying question — it is on
the same footing as the title), then proceeds. This preserves "gather maximum context BEFORE asking
clarifying questions" (the source path is an input, not a direction question) while making text access
mandatory. (constraint #5, #6)

### R2 — Standardized path contract (the core deliverable)
Every `/laf:prep` run emits a fixed-path package at `work/prep/<work-slug>/`:

| File | Kind | Confidence track | Purpose |
|---|---|---|---|
| `00-work-context.md` | RESEARCH | context | author, era, genre, reception, source-access declaration |
| `10-challenges.yaml` | DERIVED | derived from 20 | typed challenge taxonomy + governing rule + per-tier strategy + compound-scene flags |
| `20-analysis-work-level.yaml` | SOURCE | text + context | work-level source-fidelity analysis, every fact confidence-tagged |
| `30-mapping.yaml` | DERIVED | min(text,context) | the derived `<work>-mapping.yaml` (native input format) + top-level `meaning:` key |
| `40-prep-brief.md` | SYNTHESIS | — | human-readable package: decisions, cross-tier spine summary, answered questions |
| `50-greenlight.md` | GATE | — | greenlight checklist + user confirmations (PENDING → CONFIRMED) |
| `60-handoff-prompt.md` | HANDOFF | — | the EXACT paste-able `/laf:rewrite` prompt |
| `70-traceability.md` | DERIVED | — | every artifact + mapping entry → derived-from facts + gap-closed + confidence |

On greenlight, `30-mapping.yaml` is **promoted** (via `kb-management`) to both
`config/concept_mapping/templates/<work>_mapping.yaml` (root) and
`kb/adaptation-mapping/<work>_mapping.yaml` (0.1). The rewrite phase reads
`[30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]` by **hardcoded path** — no arguments.

### R3 — Referenced path-contract doc
The path layout lives in ONE file — `laf-adaptation/skills/prep/resources/path-contract.md` — imported
by reference from (a) the `prep` skill §1, (b) `commands/prep.md`, (c) `commands/rewrite.md`. Single
source of truth; no drift. (D2)

### R4 — NATIVE orchestrator agent
New agent `laf-adaptation/agents/prep-cordinator.md` (sibling to `muse`, but for onboarding). Model:
**`opus`** (user-confirmed Q6; matches `muse` and `tier-coordinator`). Skills: `source-fidelity`,
`adaptation-tiers`, `adaptation-rules`, `kb-management`, `prep`, `thematic-fidelity`. Tools:
`Agent(web-researcher, analyst, tier-coordinator)`, Read, Write, Glob, Grep, WebSearch, WebFetch. Owns
the 8-stage procedure (§3 below). (D1, T3)

### R5 — Two NATIVE skills
- `laf-adaptation/skills/prep/SKILL.md` — the phase procedure (8 sections: path-contract ref, challenge
  taxonomy, two-track work-level analysis, mapping authoring, question-gate coverage rule, greenlight,
  handoff, traceability). Includes the compound-scene protocol as §2.1. (D1, D7)
- `laf-adaptation/skills/thematic-fidelity/SKILL.md` — the meaning-preservation concept (analyst
  `meaning`-field spec, Check D definition, exemplar DERIVED-marking rules). Cross-phase: attaches to
  `prep-cordinator` (prep) and is referenced by the `tier-coordinator` body (rewrite, Check D). (D1, D9)

### R6 — Two-track work-level analysis (anti-hallucination)
Work-level analysis runs on TWO tracks: (a) a `web-researcher` **context track** (secondary sources;
PARTIAL/MEMORY ceiling) and (b) a `source-fidelity` **text track** (the novel text — **required input per
Q1**; FULL or PARTIAL access; MEMORY-BASED is NOT acceptable at work level because the source is
mandatory). Every mapping entry carries `text_confidence` AND `context_confidence`; the entry's effective
confidence = `min(text, context)`. Because the source text is mandatory, the text-track ceiling is
FULL/PARTIAL (not MEMORY), so every mapping entry is at least text-grounded. The orchestrator applies
`source-fidelity` Phase-0 at the work level: if the elicited source path resolves to NO-ACCESS (missing /
empty / unreadable), the prep phase ABORTs (same hard gate as per-chapter analysis) and tells the user to
supply a readable source. (D4, decision Q1 = source required)

### R7 — Coverage-constrained question gate
After autonomous gathering (stages 1-4), the orchestrator emits a `## Questions for the user` block and
HALTs. The question set is **constrained by the challenge taxonomy's `human_judgment_dimension` flag**:
the gate MUST ask about every challenge type whose governing rule has a human-judgment dimension
(allegory stance, omission honor-set, target-age nuance, battle-scope) and MUST NOT ask about
deterministic rules (violence-level, death-euphemism). Each question allows `[skip]`, recorded in
`70-traceability.md` as DEFAULTED. The gate is a prompt-emitted block + halt (LangGraph-interrupt
semantics, no runtime — enrichment §2). (D5)

### R8 — Greenlight gate
After the package is written, the orchestrator writes `50-greenlight.md` (checklist: source-access
declared, mapping confidence ceiling acknowledged, tier set confirmed, key decisions ratified) and emits
a confirmation request; HALTs until the user confirms. The prep phase authors the mapping for **all four
tiers {1,2,3,5}** by default (decision Q4); greenlight may narrow the active tier set. On confirmation:
promote `30-mapping.yaml` to kb/ + root templates/ via `kb-management`, set status CONFIRMED.

### R9 — Handoff prompt emission
On greenlight, the orchestrator writes `60-handoff-prompt.md` containing the literal paste-able text:

```
/laf:rewrite --work <work-slug>
```

The `rewrite` command's body reads the fixed paths (`path-contract.md` §rewrite_phase_reads) and hands
control to `muse` for chapter 1 with the instruction "the prep package is your only context; do not ask
the user to restate anything." (D11, spec-kit pattern — enrichment §3)

### R10 — Closes evaluation gap #1 (thematic/meaning-preservation)
- `analyst` (NATIVE body edit) emits `meaning: {value, confidence}` per chapter/scene.
- `tier-coordinator` (BUILD-NEW body edit) gains **Check D (meaning-preservation)**: every tier's
  rendering preserves the work-level `meaning` while the surface transforms; status
  Meaning-PRESERVED | Meaning-DIFF. Grounded in Hutcheon/Bortolotti "meaning preserved under surface
  transformation, environment = target tier" (enrichment §5).
- Work-level `meaning` is a top-level key in `30-mapping.yaml`, promoted with it, so the rewrite-phase
  `muse` reads it with **zero adopted-body edits** (D6).

### R11 — Closes evaluation gap #2 (compound-scene protocol)
The compound-scene protocol ships as **§2.1 of the `prep` skill** (not a file inside the adopted
`adaptation-rules/resources/`, avoiding sync-boundary muddying). When `analyst` flags
`compound_scene: true` (≥2 high-severity `transformation_flags` co-occurring), the `prep` skill's
reconciliation method (find emotional core → decompose surface → convert/name/preserve by tier → verify
meaning survived) is baked into the per-challenge entry of `10-challenges.yaml`. (D7)

### R12 — Closes evaluation gap #3 (native work-mapping authoring)
`prep` skill §4 derives `30-mapping.yaml` from `20-analysis-work-level.yaml` + `10-challenges.yaml`,
reusing the existing `<work>_mapping.yaml` schema (`work_metadata`, `key_challenges`, character
archetype maps, concept translations, master translation table — per `ADDING_NEW_WORKS.md`). Every
mapping entry traces to a confidence-tagged fact; entries derived from MEMORY-BASED/UNCERTAIN facts
inherit that confidence. This turns the mapping from a hand-authored prerequisite into a pipeline output
and **scores its quality** (closes Q1 row 3 "form native, content not, nothing scores quality").

### R13 — Closes evaluation gap #4 (exemplar library + contamination fix)
A small set of challenge-typed **verified** exemplars at
`laf-adaptation/adaptation-rules/resources/exemplars/<challenge-type>.md` (sacrifice-and-return,
betrayal-and-redemption, petrification/body-horror). Each carries a structural marker
`<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->`. The
writer loads the matching exemplar via `adaptation-rules` when `analyst` flags that challenge type.
**Plus** `70-traceability.md` proves the whole package's provenance (B's belt-and-suspenders). Exemplars
live OUTSIDE `work/` + `kb/canon/` (the source-truth path), so a downstream agent cannot present them as
verified source (closes the Q2 contamination risk). (D8, D3)

### R14 — Root-layer parity explicitly OUT OF SCOPE
ADR-006 deliberately shipped only T1+T3 in root. The prep phase lives in 0.1. Root v1.0 gets only a
pointer in `docs/guides/ADDING_NEW_WORKS.md` ("to produce a mapping automatically, use 0.1's
`/laf:prep`"). No new root machinery. (D10, T7)

## 2. Change-list (boundary-checked)

| # | Change | Class | Boundary-safe? | Source |
|---|---|---|---|---|
| 1 | `commands/prep.md` (`/laf:prep`) | NATIVE (new command) | ✅ new file | R1 |
| 2 | `commands/rewrite.md` (`/laf:rewrite`) | NATIVE (new command) | ✅ new file | R9 |
| 3 | `agents/prep-cordinator.md` | NATIVE (new agent) | ✅ new file, no upstream collision | R4 |
| 4 | `skills/prep/SKILL.md` | NATIVE (new skill) | ✅ | R5 |
| 5 | `skills/prep/resources/path-contract.md` | NATIVE resource | ✅ | R3 |
| 6 | `skills/thematic-fidelity/SKILL.md` | NATIVE (new skill) | ✅ | R5 |
| 7 | `skills/adaptation-rules/resources/exemplars/<type>.md` | NATIVE files in adopted resources/ | ✅ user-confirmed (Q5); permitted per CLAUDE.md §1; loaded by `adaptation-rules` which `writer` already imports; DERIVED-marked | R13 |
| 8 | `agents/analyst.md` body edit (compound_scene flag, meaning field) | NATIVE-body edit | ✅ analyst is NATIVE | R10, R11 |
| 9 | `agents/tier-coordinator.md` body edit (Check D) | BUILD-NEW-body edit | ✅ tc is BUILD-NEW | R10 |
| 10 | `writer.md` | **NO CHANGE** (stays 1 additive line) | ✅ cleanest boundary respect | D6 |
| 11 | `docs/guides/ADDING_NEW_WORKS.md` pointer | NATIVE doc edit | ✅ | R14 |
| 12 | root v1.0 new machinery | NONE | ✅ out of scope | R14 |
| 13 | `VENDOR.md` manifest rows for #1-#6, #8-#9 | NATIVE update | ✅ (NATIVE/BUILD-NEW rows, no hash-pin) | contract |

**Boundary contract verification:** run `uv run python laf-adaptation/scripts/check_boundary.py` after
implementation. Expected: all Rules A-F pass (no adopted-body drift; `writer.md` remains exactly its
current 1-line patch; new NATIVE/BUILD-NEW files have no upstream name collision; all managed files
manifested).

## 3. The prep-phase pipeline (which agent owns each stage)

```
/laf:prep "<novel>"                              [user types only this]
   │
   ▼  commands/prep.md delegates to:
STAGE 1  RESEARCH        prep-cordinator FIRST elicits/confirms the source path (required input, Q1);
                          applies source-fidelity Phase-0 → if NO-ACCESS, ABORT; else dispatches
                          web-researcher → 00-work-context.md (context track)
STAGE 2  ROADMAP          prep-cordinator reads 00 + taxonomy skeleton → emits prep task list; EXECUTES
                          stages 3-4 autonomously (no user interaction)
STAGE 3  ANALYZE+CLASSIFY prep-cordinator dispatches analyst at WORK level
                          → 20-analysis-work-level.yaml (text track, confidence-tagged)
                          + prep-skill §2 challenge taxonomy → 10-challenges.yaml
                          (compound_scene flags; governing rule per challenge; per-tier strategy)
STAGE 4  AUTHOR MAPPING   prep-skill §4 derives 30-mapping.yaml (per-entry min(text,context);
                          top-level meaning: key)
STAGE 5  QUESTION GATE    prep-cordinator emits ## Questions for the user (coverage-constrained by
                          human_judgment_dimension); HALT; resume on reply; [skip] recorded
STAGE 6  PACKAGE          write 40-prep-brief.md + 70-traceability.md; update 10/20/30 with answers
STAGE 7  GREENLIGHT       write 50-greenlight.md; emit confirmation; HALT until confirmed;
                          on confirm: promote 30-mapping.yaml → kb/adaptation-mapping/ + root templates/
STAGE 8  HANDOFF          write 60-handoff-prompt.md (literal /laf:rewrite --work <slug>)
                          ─────────────────────────────────────────────────────────────────
NEXT SESSION: user pastes /laf:rewrite --work <slug>
   → commands/rewrite.md reads [30-mapping, 40-prep-brief, 10-challenges] by hardcoded path
   → hands to muse for chapter 1 (existing per-chapter 11-step workflow, now with meaning-aware mapping)
```

## 4. How each evaluation gap is closed natively (traceability to `10-findings-and-evaluation.md`)

| Gap (from eval) | Native closure | Requirement |
|---|---|---|
| #1 thematic/meaning-preservation ("neither add nor strip the allegory") | `thematic-fidelity` skill + analyst `meaning` field + tier-coordinator Check D + meaning folded into promoted mapping | R10 |
| #2 compound-scene protocol (multi-rule scenes) | `prep` skill §2.1 reconciliation method + analyst `compound_scene` flag, baked into `10-challenges.yaml` | R11 |
| #3 native work-mapping authoring (form native, content not, nothing scores) | `prep` skill §4 derives `30-mapping.yaml` from confidence-tagged analysis; per-entry confidence scores quality | R12 |
| #4 retrievable exemplar library (few-shot, contamination-safe) | `adaptation-rules/resources/exemplars/<type>.md` with DERIVED markers + `70-traceability.md` provenance | R13 |
| contamination risk (Q2) | two-track confidence (R6) + traceability matrix (R3/R13) + DERIVED markers + exemplars outside source-truth path | R6, R13 |
| root parity (Q3 #5) | OUT OF SCOPE (ADR-006 deliberate) | R14 |

## 5. The 8 Open Tensions — resolved positions (compact)

- **T1 (which layer):** 0.1 owns the phase; root = pointer stub. ✅
- **T2 (work vs chapter):** dedicated work-level pass by `prep-cordinator` dispatching `analyst` at work
  granularity, two-track. ✅
- **T3 (orchestrator shape):** NATIVE `prep-cordinator` agent; gate = prompt-emitted block + halt +
  greenlight rule, no runtime. ✅
- **T4 (derived content topology):** exemplars in `adaptation-rules/resources/exemplars/` (DERIVED
  marked, outside source-truth path); traceability matrix proves whole-package provenance. ✅
- **T5 (path contract):** `work/prep/<work-slug>/{00..70}` fixed files; referenced path-contract doc. ✅
- **T6 (mechanize mapping):** `prep` skill §4 derives + scores the mapping from analysis + taxonomy. ✅
- **T7 (root parity):** OUT OF SCOPE. ✅
- **T8 (handoff command):** `/laf:rewrite --work <slug>` hardcoded-path handoff. ✅

## 6. Out of scope

- Any runtime/CLI/scripts beyond the existing `check_boundary.py` (ADR-006).
- Edits to any ADOPTED agent body (`writer.md` stays at its current 1-line patch; meaning routes via the
  promoted mapping, D6).
- Producing the actual rewritten novel in this phase (only the prep package + handoff prompt).
- Root v1.0 new machinery (T5 transform, cross-tier tool) — out of scope per ADR-006 (R14).
- A persistent exemplar-authoring workflow (the seed exemplar set ships once; expanding it is future work).

## 7. Resolved decisions (user-confirmed 2026-07-04)

All six open questions resolved. Five confirm merged defaults; **Q1 changes the design** (source text now
mandatory, see R1/R6/Stage 1).

1. **Source-text requirement (Q1 = Yes):** work-level analysis REQUIRES the source text. The entry point
   elicits a source path as a mandatory input (not a clarifying question); MEMORY-BASED is not acceptable
   at work level; Phase-0 ABORT-on-NO-ACCESS applies. → updated R1, R6, Stage 1.
2. **Traceability consumer (Q2 = Human+Greenlight audit):** `70-traceability.md` is for human review +
   the greenlight decision only. The rewrite-phase muse does NOT consume it; muse reads `30-mapping.yaml`'s
   inline per-entry confidence. → confirms R13/B.9-Q1 default.
3. **`human_judgment_dimension` defaults (Q3 = Yes):** the shipped per-challenge-type flag set is accepted
   (death→yes, allegory→yes, violence-level→no, petrification→yes, battle-scope→yes). → confirms R7.
4. **Tier set (Q4 = All four, greenlight narrows):** prep authors the mapping for {1,2,3,5} by default;
   greenlight may narrow. → confirms R8 default.
5. **Exemplar placement (Q5 = inside adopted `adaptation-rules/resources/`):** exemplars ship inside the
   adopted skill's resources tree (loaded by `adaptation-rules`, which `writer` already imports), with
   DERIVED markers. Accepted despite CLAUDE.md §1's "prefer NATIVE skill" guidance, because the loading
   path is cleaner. → confirms change-list #7; revisit only if upstream-sync friction appears.
6. **`prep-cordinator` model (Q6 = opus):** matches `muse` and `tier-coordinator`. → confirms R4 default.

## 8. Success-criteria check (from the seed brief)

- ✅ Named entry command (`/laf:prep`) + standardized path contract (R2/R3).
- ✅ Concrete agent/skill/kb change list, each classified + boundary-checked (§2).
- ✅ Prep-phase pipeline with per-stage agent ownership (§3).
- ✅ Every evaluation gap closed natively (§4).
- ✅ Greenlight + next-phase-prompt emission mechanism (R8/R9).
- ✅ Explicit out-of-scope + open questions (§6/§7).

## 9. Handoff (design)

**Next step:** `/sc:design @docs/native-prep/brainstorm-out/merged-requirements.md`

The design phase should produce, from this spec:
- Final skill/agent body drafts (`prep`, `thematic-fidelity`, `prep-cordinator`, the two commands).
- The `path-contract.md` resource.
- The `10-challenges.yaml` schema with the `human_judgment_dimension` flag and seeded exemplar set.
- The `analyst.md` and `tier-coordinator.md` diff (NATIVE/BUILD-NEW body edits only).
- A boundary-check verification plan (`uv run python laf-adaptation/scripts/check_boundary.py`).
