# Research: File Inventory + Target-Tree Mapping
**Topic type:** File Inventory
**Scope:** laf-adaptation/ complete target-tree file map
**Status:** Complete
**Date:** 2026-07-03

**Summary:** Master file→provenance→source→spec map for the complete `laf-adaptation/` target tree.
15 `agents/*.md` (11 adopted [10 clean + writer patched], 2 native, 2 build-new) · 16 skill dirs
(12 adopted, 3 native, 1 build-new + 2 genre resources) · kb (7 adopted scaffold, 5 native ported
[4 tier yaml + universal-mappings], per-tier G1 canon at runtime) · templates/ (1) · scripts/check_boundary.py ·
CLAUDE.md · VENDOR.md · source/ + work/ scaffolds. ~47 named build-time files + full upstream adopted
`resources/**` subtrees (count resolved at Phase-0 vendor). Per-phase checklists in Section F.
Three numeric discrepancies reconciled in Section E: "11 agents"=adopted count only (true=15);
"13 adopted"=imprecise prose (authoritative=boundary-contract manifest, 11 agents+12 skills=23 files);
Phase-0 "6 agents"=core-active only (must vendor all 11 incl. 5 dormant).
---

## Legend — Provenance Classes

Per `boundary-contract.md §1` (lines 23–32):

| Class | Meaning | Source origin |
|---|---|---|
| `ADOPTED-CLEAN` | Vendored from CWS, byte-identical to baseline after uniform prefix rewrite | upstream CWS `cw/agents/` or `cw/skills/` |
| `ADOPTED-PATCHED` | Vendored + prefix rewrite + one additive frontmatter graft (only `writer.md`) | upstream CWS `cw/agents/writer.md` |
| `NATIVE` | LAF-authored adaptation spine | authored per spec / ported from LAF `config/` & `templates/` |
| `BUILD-NEW` | Greenfield (unshipped in both systems) | authored per spec |

Uniform vendor-time transform: prefix rewrite `creative-writing-skills:` → `laf-adaptation:` (`boundary-contract.md:34`).
Adopted agents are vendored from CWS **`cw/agents/`** (already Claude-lowered), NOT `agents/` (Mars source) — `DESIGN.md:147-154`, `agent-schemas.md:31-36`.

---

## SECTION A — `agents/` (11 agent files)

Root distribution tree: `DESIGN.md:104-145`. Component inventory: `DESIGN.md:52-83`. Frontmatter fully specified in `agent-schemas.md`.

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| A1 | `agents/muse.md` | ADOPTED-CLEAN | CWS `cw/agents/muse.md` (prefix rewrite) | `DESIGN.md:106`, `boundary-contract.md:60` |
| A2 | `agents/critic.md` | ADOPTED-CLEAN | CWS `cw/agents/critic.md` | `DESIGN.md:109`, `boundary-contract.md:61` |
| A3 | `agents/editor.md` | ADOPTED-CLEAN | CWS `cw/agents/editor.md` (G3: never folded/modified) | `DESIGN.md:109`, `boundary-contract.md:52,62` |
| A4 | `agents/reader-sim.md` | ADOPTED-CLEAN | CWS `cw/agents/reader-sim.md` (native persona as *data*, no file edit) | `DESIGN.md:109`, `agent-schemas.md:188-208`, `boundary-contract.md:63` |
| A5 | `agents/continuity-checker.md` | ADOPTED-CLEAN | CWS `cw/agents/continuity-checker.md` | `DESIGN.md:109`, `boundary-contract.md:64` |
| A6 | `agents/brainstormer.md` | ADOPTED-CLEAN | CWS `cw/agents/brainstormer.md` (dormant on core path) | `DESIGN.md:110`, `boundary-contract.md:65` |
| A7 | `agents/outliner.md` | ADOPTED-CLEAN | CWS `cw/agents/outliner.md` (dormant) | `DESIGN.md:110`, `boundary-contract.md:66` |
| A8 | `agents/character-sim.md` | ADOPTED-CLEAN | CWS `cw/agents/character-sim.md` (dormant) | `DESIGN.md:110`, `boundary-contract.md:67` |
| A9 | `agents/style-creator.md` | ADOPTED-CLEAN | CWS `cw/agents/style-creator.md` (dormant) | `DESIGN.md:111`, `boundary-contract.md:68` |
| A10 | `agents/web-researcher.md` | ADOPTED-CLEAN | CWS `cw/agents/web-researcher.md` (dormant; the CWS 11th agent) | `DESIGN.md:111`, `DESIGN.md:82`, `boundary-contract.md:69` |
| A11 | `agents/writer.md` | **ADOPTED-PATCHED** | CWS `cw/agents/writer.md` + prefix rewrite + 1 additive line `laf-adaptation:adaptation-rules` | `DESIGN.md:112`, `agent-schemas.md:126-178`, `boundary-contract.md:70` |
| A12 | `agents/analyst.md` | NATIVE | authored per `agent-schemas.md §2.1` | `DESIGN.md:114`, `agent-schemas.md:42-77`, `boundary-contract.md:74` |
| A13 | `agents/safety-verifier.md` | NATIVE | authored per `agent-schemas.md §2.2` | `DESIGN.md:115`, `agent-schemas.md:79-122`, `boundary-contract.md:75` |
| A14 | `agents/chronicler.md` | BUILD-NEW | authored per `agent-schemas.md §5.1` | `DESIGN.md:116`, `agent-schemas.md:213-254`, `boundary-contract.md:76` |
| A15 | `agents/tier-coordinator.md` | BUILD-NEW | authored per `agent-schemas.md §5.2` | `DESIGN.md:116`, `agent-schemas.md:256-284`, `boundary-contract.md:77` |

**Agent count reconciliation:** the tree lists 15 rows above, but this is **11 distinct agents** + note that A1–A11 = the 11 adopted-slot agents? NO — recount below.

- ADOPTED agents (A1–A11): 11 files → muse, critic, editor, reader-sim, continuity-checker, brainstormer, outliner, character-sim, style-creator, web-researcher, writer. **11 adopted agents.**
- NATIVE agents (A12–A13): 2 → analyst, safety-verifier.
- BUILD-NEW agents (A14–A15): 2 → chronicler, tier-coordinator.
- **TOTAL AGENTS = 11 + 2 + 2 = 15.**

> ⚠️ DISCREPANCY FLAG #1 ("11 agents"): `DESIGN.md:52` header says "**11 agents**, 16 skills". The ASCII diagram `DESIGN.md:55-67` lists 11 ADOPTED (muse, critic, editor, reader-sim, continuity-checker, brainstormer, outliner, character-sim, style-creator, web-researcher, writer) + 2 NATIVE (analyst, safety-verifier) + 2 BUILD-NEW (chronicler, tier-coordinator) = **15 distinct agents / 15 `agents/*.md` files**. The "11" in the header equals the ADOPTED count only; it is NOT the total. **Build target: 15 agent files.** This discrepancy is a labelling artifact, not a design conflict — the tree at `DESIGN.md:106-116` unambiguously lists all 15. See the consolidated Adopted-Count reconciliation section near the end.

---

## SECTION B — `skills/` (16 skill packages)

Tree: `DESIGN.md:117-125`. Each skill is a directory containing at minimum a `SKILL.md`. Adopted skills also carry `resources/**` (all recursively hashed — `boundary-contract.md:87-88`). Native/build-new skills' `SKILL.md` bodies + resources are authored (content owned by R2/R3 — this section owns only the STRUCTURAL file list).

### B.1 ADOPTED skills (12) — `SKILL.md` each (+ upstream `resources/**` carried verbatim)

Vendored from CWS `cw/skills/<name>/` with prefix rewrite (`DESIGN.md:118-121`, `boundary-contract.md:71-73`). Manifest hashes **every** file under each skill's `resources/` recursively (`boundary-contract.md:87-88`).

| # | Target path (SKILL.md) | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| B1 | `skills/writing-principles/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/writing-principles/` | `DESIGN.md:118`, `boundary-contract.md:71` |
| B2 | `skills/creative-writing-craft/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/creative-writing-craft/` | `DESIGN.md:118`, `boundary-contract.md:72` |
| B3 | `skills/creative-writing-modes/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/creative-writing-modes/` | `DESIGN.md:118` |
| B4 | `skills/story-review/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/story-review/` | `DESIGN.md:119` |
| B5 | `skills/story-memory/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/story-memory/` | `DESIGN.md:119` |
| B6 | `skills/kb-management/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/kb-management/` | `DESIGN.md:119` |
| B7 | `skills/shared-dao/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/shared-dao/` | `DESIGN.md:119` |
| B8 | `skills/llm-writing/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/llm-writing/` | `DESIGN.md:120` |
| B9 | `skills/writing-staffing/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/writing-staffing/` | `DESIGN.md:120` |
| B10 | `skills/intent-modeling/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/intent-modeling/` | `DESIGN.md:120` |
| B11 | `skills/grill-with-docs/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/grill-with-docs/` | `DESIGN.md:121` |
| B12 | `skills/creative-research/SKILL.md` (+ resources/**) | ADOPTED-CLEAN | CWS `cw/skills/creative-research/` | `DESIGN.md:121` |

> NOTE (adopted-skill resources): the exact per-skill `resources/**` file list is NOT enumerable from the design pack — it is whatever the upstream CWS repo ships at `upstream_sha`. The build must vendor the full subtree verbatim and `check_boundary.py --init` records a manifest row per file (`boundary-contract.md:87-88`, `boundary-contract.md:147-148`). **Per-file resource paths: Unverified from specs — resolved at Phase-0 vendor time from the pinned upstream checkout.** Checklist item granularity for these = one item per adopted skill directory (vendor whole tree), not per resource file.

### B.2 NATIVE skills (3) — content owned by R2

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| B13 | `skills/adaptation-tiers/SKILL.md` | NATIVE | authored per `skill-specs.md §1` | `DESIGN.md:122`, `DESIGN.md:248`, `boundary-contract.md:78` |
| B13r | `skills/adaptation-tiers/resources/tier_<N>.md` commentary (per-tier) | NATIVE | authored per skill-specs | `DESIGN.md:122` ("resources/tier_N.md commentary") |
| B14 | `skills/adaptation-rules/SKILL.md` | NATIVE | authored per `skill-specs.md §2` | `DESIGN.md:123`, `DESIGN.md:249`, `boundary-contract.md:79` |
| B14a | `skills/adaptation-rules/resources/thematic.md` | NATIVE | ported from `config/transformation_rules/thematic.yaml` (canonical) | `DESIGN.md:123,249`, `kb-formats.md:107-114` |
| B14b | `skills/adaptation-rules/resources/character.md` | NATIVE | authored per `skill-specs.md §2` | `DESIGN.md:123,249` |
| B14c | `skills/adaptation-rules/resources/agency.md` | NATIVE | authored per `skill-specs.md §2.3` (tier-conditional mode ladder) | `DESIGN.md:123`, `DESIGN.md:250` |
| B15 | `skills/source-fidelity/SKILL.md` | NATIVE | authored per `skill-specs.md §3` (v2.0 protocol) | `DESIGN.md:124`, `DESIGN.md:252`, `boundary-contract.md:80` |

> NOTE: `DESIGN.md:122` says adaptation-tiers carries "resources/tier_N.md commentary" (plural tiers). Exact count of commentary files (per tier 1/2/3/5, or one combined) = **content decision owned by R2** — flagged for R2, not counted rigidly here. `DESIGN.md:123` names adaptation-rules resources explicitly: `{thematic,character,agency}.md` = 3 files.

### B.3 BUILD-NEW skill (1) + genre resources — content owned by R3

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| B16 | `skills/adaptation-safety/SKILL.md` | BUILD-NEW | authored per `safety-rubric.md` | `DESIGN.md:125`, `DESIGN.md:254`, `boundary-contract.md:81` |
| B16a | `skills/adaptation-safety/resources/children.md` (genre resource) | BUILD-NEW | authored per spec (genre res.) | `DESIGN.md:63`, `DESIGN.md:125` |
| B16b | `skills/adaptation-safety/resources/ya.md` (genre resource) | BUILD-NEW | authored per spec (genre res.) | `DESIGN.md:64`, `DESIGN.md:125` |

**Skill count reconciliation:**
- ADOPTED skills (B1–B12): **12**.
- NATIVE skills (B13–B15): **3** → adaptation-tiers, adaptation-rules, source-fidelity.
- BUILD-NEW skills (B16): **1** → adaptation-safety.
- **TOTAL SKILLS = 12 + 3 + 1 = 16** ✓ matches `DESIGN.md:52` "16 skills".

The 2 genre resources (children.md, ya.md) are `resources/` files INSIDE the adaptation-safety skill, not standalone skills — `DESIGN.md:78` counts them separately ("+ 2 genre resources") but `DESIGN.md:125` places them under `adaptation-safety/resources/`. They do NOT change the 16-skill total.

---

## SECTION C — `kb/` (knowledge-base layers)

Tree: `DESIGN.md:132-140`, `kb-formats.md:22-39`. The native kb layers ride *inside* the adopted `kb/` container (`kb-formats.md:9`). Content of native kb files owned by **R4** (LAF port-source mapping); this section owns the STRUCTURAL file list + provenance.

### C.1 ADOPTED kb layers (directory scaffolding + CWS md formats, unchanged)

Per `DESIGN.md:133`, `kb-formats.md:24`. These are adopted-lifecycle containers; their internal files are created at runtime by adopted machinery (chronicler/kb-management), NOT vendored as fixed content. The BUILD creates the **directory scaffold**.

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| C1 | `kb/canon/` (dir) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |
| C2 | `kb/characters/` (dir) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |
| C3 | `kb/world/` (dir) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |
| C4 | `kb/timeline/` (dir) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |
| C5 | `kb/styles/` (dir) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |
| C6 | `kb/vocab.md` (file) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |
| C7 | `kb/issues/` (dir) | ADOPTED (scaffold) | CWS kb layout | `DESIGN.md:133`, `kb-formats.md:24` |

> NOTE: `kb-formats.md:11-12` states adopted layers "keep their CWS markdown formats unchanged and are not re-specified here." Whether these ship as empty scaffolds or with seed content is **Unverified from specs** — treat as scaffold-only (empty dirs / placeholder) at build; populated at runtime. `vocab.md` is listed as a file (`DESIGN.md:133`, `kb-formats.md:24`).

### C.2 NATIVE kb layer — `kb/tiers/` (ported verbatim from LAF config — R4)

Per `kb-formats.md:43-89`. Ported unchanged from `config/age_profiles/tier_<N>_*.yaml` (`kb-formats.md:45`). T4 interpolated at runtime, never stored (`kb-formats.md:116-120`).

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| C8 | `kb/tiers/tier_1.yaml` | NATIVE | port `config/age_profiles/tier_1_*.yaml` verbatim | `DESIGN.md:134`, `kb-formats.md:26,45` |
| C9 | `kb/tiers/tier_2.yaml` | NATIVE | port `config/age_profiles/tier_2_*.yaml` verbatim | `DESIGN.md:134`, `kb-formats.md:26,45` |
| C10 | `kb/tiers/tier_3.yaml` | NATIVE | port `config/age_profiles/tier_3_*.yaml` verbatim | `DESIGN.md:134`, `kb-formats.md:26,45` |
| C11 | `kb/tiers/tier_5.yaml` | NATIVE | port `config/age_profiles/tier_5_*.yaml` verbatim | `DESIGN.md:134`, `kb-formats.md:26,45` |
| — | `kb/tiers/tier_4.yaml` | **DO NOT CREATE** | interpolated at runtime, never stored | `kb-formats.md:27,116-120` |

### C.3 NATIVE kb layer — `kb/adaptation-mapping/` (ported verbatim — R4)

Per `kb-formats.md:124-184`.

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| C12 | `kb/adaptation-mapping/universal-mappings.yaml` | NATIVE | port `config/concept_mapping/universal_mappings.yaml` verbatim (9 concepts) | `DESIGN.md:135`, `kb-formats.md:30,126-142` |
| C13 | `kb/adaptation-mapping/<work>-mapping.yaml` (e.g. `tolkien-mapping.yaml`) | NATIVE | copied per-work from `templates/work-mapping-template.yaml` at onboarding | `DESIGN.md:135`, `kb-formats.md:31,144-147` |

> NOTE: C13 is created **per work at onboarding** (`kb-formats.md:146-147`), not at framework build time. For the Phase-3 proof (Tolkien), a `tolkien-mapping.yaml` is instantiated. Its authored/ported source may also derive from `config/concept_mapping/templates/<author>_mapping.yaml` (`kb-formats.md:145`).

### C.4 NATIVE + graft G1 — `kb/adaptations/<work>/tier-<N>/` (per-tier canon state)

Per `kb-formats.md:188-263`, `DESIGN.md:136-140`. Written by `chronicler` at runtime on muse-accept (keyed by `(work, tier, chapter)`). The BUILD does not pre-create content; these appear during the Phase-3 proof run. Structural template per (work, tier):

| # | Target path (template) | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| C14 | `kb/adaptations/<work>/tier-<N>/decisions.md` | NATIVE (G1, runtime) | chronicler-authored per `kb-formats.md §4.2` | `DESIGN.md:139`, `kb-formats.md:33,221-230` |
| C15 | `kb/adaptations/<work>/tier-<N>/continuity.md` | NATIVE (G1, runtime) | chronicler-authored per `kb-formats.md §4.1` | `DESIGN.md:140`, `kb-formats.md:34,194-213` |
| C16 | `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/analysis.yaml` | NATIVE (G1, runtime) | promoted copy of `work/analysis/ch-NN.yaml` on accept | `DESIGN.md:140`, `kb-formats.md:37,250-252` |
| C17 | `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/adapted.md` | NATIVE (G1, runtime) | accepted tier-N adaptation prose | `DESIGN.md:140`, `kb-formats.md:38,253` |
| C18 | `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/canon-delta.md` | NATIVE (G1, runtime) | chronicler-authored per `kb-formats.md §4.3` | `DESIGN.md:140`, `kb-formats.md:39,232-246` |

> Also runtime: `kb/canon/<work>/ch-<NN>.md` (shared source truth) and `kb/timeline/<work>.md` — written by chronicler (`agent-schemas.md:241-243`, `kb-formats.md:269`). These are runtime outputs under the adopted `kb/canon` + `kb/timeline` scaffolds (C1, C4), not build-time files.

**kb structural build target (Phase 0/1):** create scaffold dirs C1–C7; port native files C8–C12 (5 files: 4 tier yaml + universal-mappings). C13–C18 are runtime/proof-time artifacts (Phase 3), not framework-build files.

---

## SECTION D — `source/`, `work/`, `templates/`, `scripts/`, root files

### D.1 `source/` — BUILD-NEW (read-only reference tree)

Per `DESIGN.md:126`. The work being adapted. For Phase-3 proof: a real Tolkien chapter at `source/<work>/ch-<NN>.txt` (`DESIGN.md:164`, `agent-schemas.md:63`).

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| D1 | `source/` (dir scaffold) | BUILD-NEW | authored per `DESIGN.md §2` | `DESIGN.md:126` |
| D2 | `source/<work>/ch-<NN>.txt` (proof input) | BUILD-NEW (proof data) | provided at proof time (Tolkien chapter) | `DESIGN.md:164,296`, `agent-schemas.md:63` |

### D.2 `work/` — ADOPTED lifecycle + NATIVE subdirs

Per `DESIGN.md:127-131`. Provisional; constraint #5. Runtime output dirs — build creates scaffold.

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| D3 | `work/analysis/` (dir) | NATIVE subdir | per-chapter analyst output (confidence-tagged) | `DESIGN.md:128`, `DESIGN.md:169`, `agent-schemas.md:66` |
| D4 | `work/drafts/` (dir) | ADOPTED | adopted lifecycle | `DESIGN.md:129`, `DESIGN.md:178` |
| D5 | `work/critique-reports/` (dir) | ADOPTED | adopted lifecycle | `DESIGN.md:130`, `DESIGN.md:183` |
| D6 | `work/safety-reports/` (dir) | NATIVE subdir | safety-verifier output | `DESIGN.md:131`, `DESIGN.md:190`, `agent-schemas.md:109` |

> Runtime files under these (not build-time): `work/analysis/ch-<NN>.yaml`, `work/drafts/ch-<NN>-t<N>-v<M>.md`, `work/safety-reports/ch-<NN>-t<N>.md`, `work/analysis/ch-<NN>-cross-tier.md` (tier-coordinator output, `agent-schemas.md:280`).

### D.3 `templates/` — NATIVE

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| D7 | `templates/work-mapping-template.yaml` | NATIVE | carried verbatim from LAF `templates/` | `DESIGN.md:142`, `DESIGN.md:259`, `kb-formats.md:147` |

### D.4 `scripts/` — BOUNDARY CONTRACT (the only script — R5)

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| D8 | `scripts/check_boundary.py` | BUILD-NEW (validation tool) | authored per `boundary-contract.md §3` | `DESIGN.md:144`, `boundary-contract.md:11,92-167` |

> `boundary-contract.md:17-19`: this is the ONLY script LAF 0.1 ships (validation, not runtime — stays inside ADR-006). Content owned by **R5**.

### D.5 Root files

| # | Target path | Class | Source | Spec § (file:line) |
|---|---|---|---|---|
| D9 | `CLAUDE.md` | ADOPTED-PATCHED (pattern + LAF section) | adopted CWS pattern + LAF conventions section + boundary-contract note | `DESIGN.md:105` |
| D10 | `VENDOR.md` | BUILD-NEW (boundary contract manifest) | authored per `boundary-contract.md §2` | `DESIGN.md:106`, `boundary-contract.md:40-88` |

> NOTE (CLAUDE.md provenance): `DESIGN.md:105` describes it as "ADOPTED pattern + LAF conventions section + boundary-contract note" — i.e. an adopted base with LAF additions. It is NOT hash-pinned like agents/skills (not under `agents/` or `skills/`, so outside `check_boundary.py` rule F glob at `boundary-contract.md:147`). Classify as authored-from-adopted-pattern. **Provenance nuance flagged** — content owned by R5 (boundary) / general.
> NOTE (NOTICE file): `boundary-contract.md:48` references "attribution retained per NOTICE" and `DESIGN.md:106` "(Apache-2.0 attribution)". A `NOTICE` file for Apache-2.0 attribution is implied but NOT explicitly placed in the tree at `DESIGN.md:104-145`. **Unverified — needs decision** whether attribution lives in `VENDOR.md` (license line `boundary-contract.md:48`) or a separate `NOTICE` file.
> NOTE (`.githooks/pre-commit`): `boundary-contract.md:175` references `.githooks/pre-commit` (opt-in per clone) invoking check_boundary.py. Not in the DESIGN tree; optional infra. **Flagged as optional Phase-0/4 infra file — needs decision.**

---

## SECTION E — ⚠️ CRITICAL RECONCILIATION: "12 vs 13 adopted" + "6 adopted agents"

The user flagged an apparent conflict. Full evidence:

**Evidence pulled:**
- `DESIGN.md:52` header: "(11 agents, 16 skills)".
- `DESIGN.md:70`: "**13 adopted agents/skills** are copied unchanged."
- `DESIGN.md:283`: "adopted subset is deliberately small (**13**)".
- `DESIGN.md:293` Phase 0 deliverable: "Copy **6 adopted review/orch agents** (from CWS `cw/agents/`) + **12 adopted skills** + `kb/`+`work/` structure".
- ASCII diagram `DESIGN.md:55-67`: **11 adopted agents** (muse, critic, editor, reader-sim, continuity-checker, brainstormer, outliner, character-sim, style-creator, web-researcher, writer) + **12 adopted skills**.
- `boundary-contract.md:60-73`: manifest lists **11 adopted agent rows** (muse…writer, writer=ADOPTED-PATCHED) + "all **12** adopted skills".
- `agent-schemas.md:9-11`: "The **six adopted agents** are vendored unchanged; only `writer` receives a frontmatter-only patch".

### E.1 Resolving the numbers — three different denominators are in play

The specs use **THREE distinct counts** that each measure a different thing. They are NOT contradictory once separated:

**(a) "6 adopted review/orch agents" (`DESIGN.md:293`, `agent-schemas.md:9`) = the CORE-PATH active adopted agents.**
These are the 6 that the fully-specified integration touches on the core adapt pipeline: `muse` (orch), `critic`, `editor`, `reader-sim`, `continuity-checker` (review quartet + muse), `writer` (patched). Count the agents given explicit integration treatment in `agent-schemas.md`: writer §3, reader-sim §4, + the quartet critic/editor/reader-sim/continuity-checker + muse orchestrator. `agent-schemas.md:9-11` says "six adopted agents… only writer receives a patch" → the SIX = {muse, critic, editor, reader-sim, continuity-checker, writer}. (writer patched; the other 5 clean.)

**(b) "11 adopted agents" (ASCII diagram + `boundary-contract.md` manifest) = ALL vendored adopted agents.**
The 6 core-path (a) PLUS 5 dormant-but-still-vendored: `brainstormer, outliner, character-sim, style-creator, web-researcher` (`DESIGN.md:110-111` "dormant on core path" / "dormant"; `DESIGN.md:82` web-researcher "retained but dormant"). Dormant ≠ not-vendored — they are ADOPTED-CLEAN rows in the manifest (`boundary-contract.md:65-69`) and MUST be vendored in Phase 0.

**(c) "13 adopted agents/skills" (`DESIGN.md:70`, `:283`) — the "copied unchanged" count.**
`DESIGN.md:70` reads "13 adopted agents/skills are copied unchanged. `writer` is adopted but gains a mode…; `reader-sim` is adopted but fed a native persona…". The number 13 here is a **prose approximation of the small-adopted-subset headline**, NOT a literal file count (11 adopted agents + 12 adopted skills = 23 files, not 13). Reading it charitably: it appears to intend "the adopted subset is a small, bounded set" and is echoed at `:283` ("deliberately small (13)").

> ⚠️ DISCREPANCY FLAG #2 ("13"): The literal "13 adopted agents/skills copied unchanged" (`DESIGN.md:70`) does **not** reconcile to any clean file count:
> - 11 adopted agents + 12 adopted skills = **23** adopted files (the true vendor count).
> - Core-path active: 6 agents + 12 skills = **18**.
> - Neither equals 13. The "13" is best read as an **imprecise headline figure** for "the adopted subset is small/bounded", possibly a stale early-draft number. **RESOLUTION: treat the AUTHORITATIVE adopted inventory as the `boundary-contract.md` manifest (11 agent rows + 12 skill entries = 23 files/dirs), NOT the "13".** The manifest (`boundary-contract.md:60-81`) is machine-checked by `check_boundary.py`; the "13" is prose. **Flag for design-owner confirmation, but build to the manifest.**

### E.2 The "12 adopted skills" is consistent everywhere ✓

`DESIGN.md:293` "12 adopted skills", `DESIGN.md:118-121` lists 12, `boundary-contract.md:73` "all 12 adopted skills". **No conflict on skills.** Build target = 12 adopted skill dirs (B1–B12).

### E.3 Phase-0 vendor set — DEFINITIVE list (what `--init` hashes)

Per `DESIGN.md:293` + `boundary-contract.md:60-73`, Phase 0 vendors:
- **11 adopted agents** (A1–A11): 10 ADOPTED-CLEAN + `writer.md` ADOPTED-PATCHED. (`DESIGN.md:293`'s "6" undercounts — it names only the core review/orch set; the 5 dormant agents are still vendored per the manifest. **The 6-vs-11 gap = dormant agents. Build must vendor all 11.**)
- **12 adopted skills** (B1–B12), each with full `resources/**` subtree.
- `kb/` adopted scaffold (C1–C7) + `work/` adopted scaffold (D4, D5).

> ⚠️ DISCREPANCY FLAG #3 ("6 vs 11 agents in Phase 0"): `DESIGN.md:293` says Phase 0 copies "6 adopted review/orch agents" but the manifest (`boundary-contract.md:60-70`) requires 11 adopted agent rows present & hashed, and rule F (`boundary-contract.md:147`) fails if any `agents/*.md` is unmanaged. **RESOLUTION: Phase 0 must vendor all 11 adopted agents** (the 5 dormant ones included), else `check_boundary.py --init` cannot record them and the quartet/manifest completeness checks are moot. The "6" is the *actively-integrated* subset; the dormant 5 are vendored-but-unwired. **Build to 11.**

---

## SECTION F — PER-PHASE FILE-CREATION CHECKLISTS (one row → one checklist item)

Grouped per `DESIGN.md §7` phases. **This is the primary artifact for the task builder** — each row below maps to ONE granular MDTM checklist item. Note: `check_boundary.py` (D8) is authored in Phase 0 (needed by `--init`); root files (D9, D10) are Phase 0. VENDOR.md manifest is populated by `--init` in Phase 0.

### Phase 0 — VENDOR (adopted acquisition; user-locked: clone/pin CWS at SHA, then vendor)
Gate: `check_boundary.py --init` passes; zero edits to vendored files (`DESIGN.md:293`).

- [ ] P0.0  Clone upstream CWS repo, pin at target SHA (user-locked decision #1); local checkout for `--upstream` (`boundary-contract.md:102`)
- [ ] P0.1  Author `scripts/check_boundary.py` (D8) — required before `--init` (`boundary-contract.md:92-167`) [R5 content]
- [ ] P0.2–P0.11  Vendor 11 adopted agents A1–A11 (prefix rewrite; `writer.md` also +1 additive line) — 11 items, one per agent file
- [ ] P0.12–P0.23  Vendor 12 adopted skill dirs B1–B12 (each: SKILL.md + resources/** verbatim) — 12 items, one per skill dir
- [ ] P0.24  Create adopted `kb/` scaffold: C1–C7 (canon, characters, world, timeline, styles, vocab.md, issues)
- [ ] P0.25  Create adopted `work/` scaffold: D4 drafts, D5 critique-reports
- [ ] P0.26  Author `CLAUDE.md` (D9) — adopted pattern + LAF section + boundary note
- [ ] P0.27  Author `VENDOR.md` (D10) header + invariants; run `check_boundary.py --init --upstream <dir>` to populate manifest hash rows
- [ ] P0.28  GATE: run `check_boundary.py` → green; verify zero edits

### Phase 1 — NATIVE SPINE
Gate: native skills validate; `writer` diff frontmatter-only; configs carried zero-rework (`DESIGN.md:294`).

- [ ] P1.1  Author `skills/adaptation-tiers/SKILL.md` (B13) [R2]
- [ ] P1.2  Author `skills/adaptation-tiers/resources/tier_<N>.md` commentary (B13r; count = R2 decision) [R2]
- [ ] P1.3  Author `skills/adaptation-rules/SKILL.md` (B14) [R2]
- [ ] P1.4  Author `skills/adaptation-rules/resources/thematic.md` (B14a; port thematic.yaml) [R2/R4]
- [ ] P1.5  Author `skills/adaptation-rules/resources/character.md` (B14b) [R2]
- [ ] P1.6  Author `skills/adaptation-rules/resources/agency.md` (B14c) [R2]
- [ ] P1.7  Author `skills/source-fidelity/SKILL.md` (B15) [R2]
- [ ] P1.8  Author `agents/analyst.md` (A12) [R2]
- [ ] P1.9  Author `agents/safety-verifier.md` (A13) [R2 — note: loads adaptation-safety which is Phase 2; sequence check needed]
- [ ] P1.10 Patch `agents/writer.md` (A11) — add `laf-adaptation:adaptation-rules` line (already vendored P0; this is the additive graft — may be done at vendor time as ADOPTED-PATCHED)
- [ ] P1.11 Port `kb/tiers/tier_1.yaml` (C8) [R4]
- [ ] P1.12 Port `kb/tiers/tier_2.yaml` (C9) [R4]
- [ ] P1.13 Port `kb/tiers/tier_3.yaml` (C10) [R4]
- [ ] P1.14 Port `kb/tiers/tier_5.yaml` (C11) [R4]
- [ ] P1.15 Port `kb/adaptation-mapping/universal-mappings.yaml` (C12) [R4]
- [ ] P1.16 Add native `work/analysis/` + `work/safety-reports/` subdirs (D3, D6)
- [ ] P1.17 Author `templates/work-mapping-template.yaml` (D7) [R4]
- [ ] P1.18 Update VENDOR.md manifest with NATIVE rows (analyst, safety-verifier, native skills) (`boundary-contract.md:74-80`)
- [ ] P1.19 GATE: native skills validate; `check_boundary.py` confirms writer diff frontmatter-only

### Phase 2 — GREENFIELD
Gate: both agents block on nothing upstream; kb native layers created (`DESIGN.md:295`).

- [ ] P2.1  Author `agents/chronicler.md` (A14) [R3]
- [ ] P2.2  Author `agents/tier-coordinator.md` (A15) [R3]
- [ ] P2.3  Author `skills/adaptation-safety/SKILL.md` (B16) [R3]
- [ ] P2.4  Author `skills/adaptation-safety/resources/children.md` (B16a genre resource) [R3]
- [ ] P2.5  Author `skills/adaptation-safety/resources/ya.md` (B16b genre resource) [R3]
- [ ] P2.6  Create `kb/adaptations/` + `kb/adaptation-mapping/` native layer scaffold (dirs)
- [ ] P2.7  Update VENDOR.md manifest with BUILD-NEW rows (chronicler, tier-coordinator, adaptation-safety) (`boundary-contract.md:76-81`)
- [ ] P2.8  GATE: `check_boundary.py` green; native kb layers present

### Phase 3 — COMPOSE & PROVE (HARD GATE)
Gate (5 conditions, `DESIGN.md:296`): v2.0 tags present · safety PASS · per-tier canon written · all four quartet agents ran · `check_boundary.py` green.

- [ ] P3.1  Create `source/` scaffold (D1) + place proof Tolkien chapter `source/<work>/ch-<NN>.txt` (D2)
- [ ] P3.2  Instantiate `kb/adaptation-mapping/<work>-mapping.yaml` (C13) from template (D7) for the proof work
- [ ] P3.3  Run full 11-step workflow on one Tolkien chapter at Tier 1 (`DESIGN.md:158-224`, 11-step data-flow) [R6]
- [ ] P3.4  Run same chapter at Tiers 1/3/5 through `tier-coordinator` (`DESIGN.md:226-238`) [R6]
- [ ] P3.5  Verify runtime artifacts produced: work/analysis/*.yaml, work/drafts/*, work/safety-reports/*, kb/adaptations/<work>/tier-N/{continuity,decisions}.md + chapters/*/{analysis.yaml,adapted.md,canon-delta.md} (C14–C18)
- [ ] P3.6  GATE: assert all 5 hard-gate conditions

### Phase 4 — UPSTREAM-SYNC PROTOCOL (documentation deliverable)
Gate: native files never touched by sync; SHA re-pinned (`DESIGN.md:297`, `boundary-contract.md:185-198`).

- [ ] P4.1  Document reconcile procedure (3-way merge adopted-only) [R5]
- [ ] P4.2  (optional) `.githooks/pre-commit` wiring (`boundary-contract.md:175`) — **needs decision**
- [ ] P4.3  Verify NATIVE/BUILD-NEW never touched by sync flow

---

## SECTION G — TOTAL FILE COUNT & SUMMARY

### Build-time files (framework distribution — Phases 0–2)

| Group | Count | Notes |
|---|---|---|
| Adopted agents (A1–A11) | 11 | 10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED (writer) |
| Native agents (A12–A13) | 2 | analyst, safety-verifier |
| Build-new agents (A14–A15) | 2 | chronicler, tier-coordinator |
| **agents/*.md total** | **15** | |
| Adopted skill dirs (B1–B12) | 12 | each = SKILL.md + resources/** (resource count = upstream, unverified) |
| Native skill SKILL.md (B13–B15) | 3 | adaptation-tiers, adaptation-rules, source-fidelity |
| Native skill resources (B14a–c + B13r) | 3+ | thematic/character/agency.md (3) + tier commentary (≥1, R2-decided) |
| Build-new skill (B16) | 1 | adaptation-safety SKILL.md |
| Build-new genre resources (B16a–b) | 2 | children.md, ya.md |
| **skills total** | **16 skill dirs** | (~22+ discrete files incl. named resources) |
| kb adopted scaffold (C1–C7) | 7 | 6 dirs + vocab.md |
| kb native ported (C8–C12) | 5 | 4 tier yaml + universal-mappings.yaml |
| kb native scaffold dirs (adaptations/, adaptation-mapping/) | 2 | |
| work/ dirs (D3–D6) | 4 | analysis, drafts, critique-reports, safety-reports |
| templates (D7) | 1 | work-mapping-template.yaml |
| scripts (D8) | 1 | check_boundary.py |
| root files (D9–D10) | 2 | CLAUDE.md, VENDOR.md |
| source/ scaffold (D1) | 1 | dir |

**DISCRETE BUILD-TIME FILE COUNT (named, framework):**
- 15 agent `.md` files
- 16 skill `SKILL.md` files + at least 5 named native/build-new resource files (thematic, character, agency, children, ya) + ≥1 tier commentary + N upstream adopted resources (unverified count)
- 5 ported kb yaml files + `kb/vocab.md`
- 1 template + 1 script + `CLAUDE.md` + `VENDOR.md`
- **Minimum discrete authored/vendored files ≈ 15 + 16 + 6 (named resources) + 6 (kb) + 4 = ~47 named files**, PLUS the full upstream `resources/**` subtrees of 12 adopted skills (count unverified — resolved at vendor time), PLUS scaffold directories (~13 dirs).

### Runtime / proof-time files (Phase 3, per work/tier/chapter — NOT framework build)
C13–C18 + work/ runtime outputs + kb/canon,timeline runtime outputs. Generated by agents during the proof run; templated, not authored.

### Provenance rollup
| Class | Agents | Skills | kb | other |
|---|---|---|---|---|
| ADOPTED-CLEAN | 10 | 12 | 7 scaffold | — |
| ADOPTED-PATCHED | 1 (writer) | — | — | CLAUDE.md (pattern) |
| NATIVE | 2 | 3 (+resources) | 5 ported | templates/ |
| BUILD-NEW | 2 | 1 (+2 genre res) | — | check_boundary.py, VENDOR.md, source/ |

### Open items requiring decision (flagged, not resolved from specs)
1. **DISCREPANCY #1** — "11 agents" header = adopted count only; true total 15 agent files. (Resolved: build 15.)
2. **DISCREPANCY #2** — "13 adopted agents/skills" (`DESIGN.md:70,283`) reconciles to no clean count; authoritative source = `boundary-contract.md` manifest (11 agents + 12 skills = 23 adopted files). Build to manifest. **Confirm with design owner.**
3. **DISCREPANCY #3** — Phase-0 "6 adopted agents" (`DESIGN.md:293`) vs 11 in manifest = the 5 dormant agents. Build all 11.
4. Adopted skills `resources/**` per-file list — **Unverified**, resolved at Phase-0 vendor from pinned SHA.
5. Tier commentary file count in adaptation-tiers/resources/ — R2 content decision.
6. `NOTICE` file for Apache-2.0 attribution — **needs decision** (VENDOR.md line vs separate NOTICE).
7. `.githooks/pre-commit` — optional infra, **needs decision**.
8. `CLAUDE.md` provenance precision (adopted-pattern vs authored) — minor, flagged.
9. kb adopted scaffolds: empty vs seeded — treat as scaffold-only.
