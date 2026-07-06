---
title: "LAF 0.1 Architecture Specification — CWS Hybrid Integration"
domain: architecture
decision: "C — Hybrid (adopt CWS domain-agnostic machinery, author LAF adaptation spine natively, build greenfield what is unshipped in both)"
source_decision: ../brainstorm/merged-requirements.md
status: draft
created: 2026-07-03
next_step: /sc:implement @.dev/releases/current/0.1/design/DESIGN.md
---

# LAF 0.1 Architecture Specification

This document is the concrete architecture specification for the **Path C — Hybrid** decision
recorded in [`../brainstorm/merged-requirements.md`](../brainstorm/merged-requirements.md). It turns
that decision into buildable artifacts: agent frontmatter schemas, skill bodies, kb file formats, a
boundary-contract CI check, the `/adaptation-safety` rubric, and the tier-coordinator reconciliation
algorithm.

The decision is **settled and not re-litigated here.** This spec assumes Path C and specifies *how* to
build it.

## Companion specs (this directory)

| Spec | Contents |
|---|---|
| **DESIGN.md** (this file) | System overview, component boundaries, distribution layout, data-flow, sequence diagrams, traceability, phase gates |
| [`agent-schemas.md`](agent-schemas.md) | Full frontmatter for the 2 native agents + the 6 adopted-agent integration patches (frontmatter-only) |
| [`skill-specs.md`](skill-specs.md) | `SKILL.md` bodies for the 4 native skills + 2 genre resources |
| [`kb-formats.md`](kb-formats.md) | File-format schemas for `kb/tiers/`, `kb/adaptation-mapping/`, `kb/adaptations/<work>/` (incl. per-tier canon, graft G1) |
| [`boundary-contract.md`](boundary-contract.md) | `VENDOR.md` manifest format + the pre-commit / CI check that proves vendored files are unmodified |
| [`safety-rubric.md`](safety-rubric.md) | The `/adaptation-safety` 6-section rubric as a machine-checkable verdict contract |
| [`tier-coordinator.md`](tier-coordinator.md) | The `tier-coordinator` parallel-fan-out + sequential-fallback reconciliation algorithm |

---

## 1. System Overview

LAF 0.1 is a **prompt + YAML-config framework** (ADR-006: not software — no Python/CLI runtime). It
composes three provenance classes into one single-tree distribution:

- **ADOPTED** — CWS files vendored verbatim, patch-clean, never edited. The domain-agnostic
  review/orchestration/kb machinery.
- **NATIVE** — LAF-authored files (skills + agents) carrying the irreducibly domain-specific adaptation
  spine: tier axis, source-fidelity, transformation rules, safety.
- **BUILD-NEW** — greenfield in *both* systems: tier-aware canon extraction (`chronicler`) and
  cross-tier reconciliation (`tier-coordinator`).

The load-bearing composition rule (**constraint #6, the boundary contract**): NATIVE knowledge enters
ADOPTED agents **only** as loadable skills via `skills:` frontmatter — never by editing an adopted
agent's body. This is what keeps the adopted subset patch-clean and upstream-syncable.

### 1.1 Component inventory (11 agents, 16 skills)

```
                         ADOPTED (vendored, unchanged)      NATIVE (LAF-authored)       BUILD-NEW (greenfield)
        ┌──────────────────────────────────────────────┬─────────────────────────┬──────────────────────────┐
AGENTS  │ muse  critic  editor  reader-sim               │ analyst                 │ chronicler               │
        │ continuity-checker  brainstormer  outliner     │ safety-verifier         │ tier-coordinator         │
        │ character-sim  style-creator  web-researcher   │                         │                          │
        │ writer (+ native adaptation MODE via skill)    │                         │                          │
        ├──────────────────────────────────────────────┼─────────────────────────┼──────────────────────────┤
SKILLS  │ writing-principles  creative-writing-craft     │ /adaptation-tiers       │ /adaptation-safety       │
        │ creative-writing-modes  story-review           │ /adaptation-rules       │ children.md (genre res.) │
        │ story-memory  kb-management  shared-dao         │ /source-fidelity        │ ya.md       (genre res.) │
        │ llm-writing  writing-staffing  intent-modeling │                         │                          │
        │ grill-with-docs  creative-research             │                         │                          │
        └──────────────────────────────────────────────┴─────────────────────────┴──────────────────────────┘
```

- **13 adopted agents/skills** are copied unchanged. `writer` is adopted but gains an *adaptation mode*
  purely by adding `/adaptation-rules` to its `skills:` frontmatter — no body edit (see
  [`agent-schemas.md` §3](agent-schemas.md)). `reader-sim` is adopted but fed a native persona schema as
  *data* (no code change).
- **2 native agents:** `analyst` (source analysis + v2.0 confidence protocol), `safety-verifier`
  (6-section safety gate).
- **2 build-new agents:** `chronicler` (tier-aware canon extraction), `tier-coordinator` (cross-tier
  reconciliation).
- **4 native skills** + **1 build-new skill** (`/adaptation-safety`) + **2 genre resources**.

> **Provenance note (ground-truthed 2026-07-03):** `chronicler` is unshipped vapor in *both*
> `cw/agents/` and `agents/` of the vendored CWS — it carries zero fork premium and must be built on any
> path. The CWS 11th agent is `web-researcher`, retained but dormant on the core adapt path.

### 1.2 The review lineup — quartet + fifth (constraint #4, invariant G3)

The CWS review quartet stays **four distinct agents**, none folded:

| Agent | Provenance | Review duty | Model (adopted default) |
|---|---|---|---|
| `critic` | ADOPTED | Adversarial craft critique, one focus area at a time (adaptation-quality focus loads `/adaptation-rules`) | `gpt` |
| `editor` | ADOPTED | Holistic structure→voice→line→surface priority pass — **never folded (G3)** | `gpt`, effort high |
| `reader-sim` | ADOPTED | Felt first-time-reader experience (persona = tier `developmental_basis`) | `deepseek` |
| `continuity-checker` | ADOPTED | Canon-contradiction pass (check duty only) | `gpt`, effort high |
| `safety-verifier` | **NATIVE** | 6-section safety gate — a **fifth** distinct reviewer, not a merge (constraint #4) | (native — see §schema) |

---

## 2. Distribution Layout (single tree)

CWS's Mars/plugin packaging is **cut** (no `mars.toml`, no `cw/` mirror, no `sync_cw_skills.py`, no
ADR-006 reversal). LAF ships one flat tree that Claude Code reads directly.

```
laf-adaptation/
├── CLAUDE.md                      # ADOPTED pattern + LAF conventions section + boundary-contract note
├── VENDOR.md                      # BOUNDARY CONTRACT: upstream SHA + per-file vendored manifest (Apache-2.0 attribution)
├── agents/
│   ├── muse.md                    # ADOPTED (Claude-lowered frontmatter — see §2.1)
│   ├── critic.md  editor.md  reader-sim.md  continuity-checker.md      # ADOPTED
│   ├── brainstormer.md  outliner.md  character-sim.md                  # ADOPTED (dormant on core path)
│   ├── style-creator.md  web-researcher.md                            # ADOPTED (dormant)
│   ├── writer.md                  # ADOPTED — adaptation mode via skills: frontmatter only
│   ├── analyst.md                 # NATIVE
│   ├── safety-verifier.md         # NATIVE
│   ├── chronicler.md              # BUILD-NEW
│   └── tier-coordinator.md        # BUILD-NEW
├── skills/
│   ├── writing-principles/  creative-writing-craft/  creative-writing-modes/    # ADOPTED
│   ├── story-review/  story-memory/  kb-management/  shared-dao/                # ADOPTED
│   ├── llm-writing/  writing-staffing/  intent-modeling/                        # ADOPTED
│   ├── grill-with-docs/  creative-research/                                     # ADOPTED
│   ├── adaptation-tiers/           # NATIVE  (SKILL.md + resources/tier_N.md commentary)
│   ├── adaptation-rules/           # NATIVE  (SKILL.md + resources/{thematic,character,agency}.md)
│   ├── source-fidelity/            # NATIVE  (SKILL.md — v2.0 protocol)
│   └── adaptation-safety/          # BUILD-NEW (SKILL.md + resources/{children,ya}.md genre resources)
├── source/                        # BUILD-NEW: the work being adapted (read-only reference)
├── work/                          # ADOPTED lifecycle (provisional; constraint #5)
│   ├── analysis/                  #   NATIVE subdir: per-chapter analyst output (confidence-tagged)
│   ├── drafts/                    #   adopted
│   ├── critique-reports/          #   adopted
│   └── safety-reports/            #   NATIVE subdir
├── kb/                            # ADOPTED lifecycle (work→kb promotion via kb-management)
│   ├── canon/  characters/  world/  timeline/  styles/  vocab.md  issues/       # ADOPTED layers
│   ├── tiers/                     #   NATIVE: tier_1/2/3/5 profiles (LAF configs as kb data; T4 interpolated)
│   ├── adaptation-mapping/        #   NATIVE: universal_mappings + <work>_mapping (cascade)
│   └── adaptations/<work>/        #   NATIVE (graft G1): per-tier canon state, keyed (work, tier, chapter)
│       └── tier-<N>/
│           ├── decisions.md
│           ├── continuity.md      #   per-tier running canon (what a Tier-N reader now "knows")
│           └── chapters/ch-<NN>/{analysis.yaml, adapted.md, canon-delta.md}
├── templates/
│   └── work-mapping-template.yaml # NATIVE (carried verbatim from LAF templates/)
└── scripts/
    └── check_boundary.py          # BOUNDARY CONTRACT enforcement (the only script; see boundary-contract.md)
```

### 2.1 Frontmatter dialect: Claude-lowered, not Mars

Because Mars/Meridian is cut, **all agent/skill frontmatter uses the Claude-native (cw-lowered)
dialect**, not the Mars-source dialect. Concretely, adopted agents are vendored from CWS's `cw/agents/`
(already Claude-lowered), *not* from `agents/` (Mars source with `model-policies`/`sandbox`/`effort`/
`subagents` keys that Claude Code does not read). See [`agent-schemas.md` §1](agent-schemas.md) for the
exact dialect contract. This choice removes the entire Mars dependency surface (`meridian-base`,
`meridian-prompter`, the temp-consumer sync build) that the merged decision cut.

---

## 3. Data Flow — per source chapter

The 11-step workflow (from the decision doc §2.4), rendered as a data-flow with the artifact each step
reads and writes. Steps are labeled by provenance.

```
   source/<work>/ch-<NN>.txt  (read-only reference)
            │
            ▼
 ┌────────────────────────┐
 │ 1. analyst  [NATIVE]   │  reads: source chapter, /source-fidelity
 │                        │  writes: work/analysis/ch-<NN>.yaml   (CERTAIN/PROBABLE/UNCERTAIN tags)
 │  Phase 0 ABORT gate ───┼──► if SOURCE ACCESS = NO ACCESS  →  HALT (constraint #2)
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐  reads: work/analysis, kb/tiers/tier_N, kb/adaptation-mapping
 │ 2. muse  [ADOPTED]     │  writes: scene brief (in-session; not persisted to kb)
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐  reads: brief, /adaptation-rules (adaptation mode), kb/tiers/tier_N
 │ 3. writer  [ADOPTED +  │  writes: work/drafts/ch-<NN>-t<N>-v1.md
 │    NATIVE skill]       │
 └───────────┬────────────┘
             ▼
 ┌───────────────────────────────── review quartet (constraint #4) ─────────────────────────────────┐
 │ 4. critic ×N [ADOPTED]  → work/critique-reports/   (parallel focus areas; adaptation-quality)     │
 │ 5. editor    [ADOPTED]  → editorial memo (priority order)          ← never folded (G3)            │
 │ 6. writer revision [ADOPTED] → work/drafts/ch-<NN>-t<N>-v2.md                                     │
 │ 7. continuity-checker [ADOPTED] → canon-contradiction report (reads kb/adaptations/<work>/tier-N) │
 └───────────┬───────────────────────────────────────────────────────────────────────────────────────┘
             ▼
 ┌────────────────────────┐  reads: revised draft, /adaptation-safety, kb/tiers/tier_N
 │ 8. safety-verifier     │  writes: work/safety-reports/ch-<NN>-t<N>.md  →  verdict {PASS|FAIL}
 │    [NATIVE]            │  MANDATORY Tier 1-2; runs AFTER continuity (constraint #3)
 └───────────┬────────────┘
             │ FAIL ──────────────► back to step 3 (revision loop — the loop LAF lacked, constraint #3)
             │ PASS
             ▼
 ┌────────────────────────┐  reads: draft, tier developmental_basis persona
 │ 9. reader-sim [ADOPTED]│  writes: felt-experience report (after convergence)
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐  reconciles all tier outputs for this chapter
 │ 10. tier-coordinator   │  reads: every tier-N adapted.md for this chapter
 │     [BUILD-NEW]        │  writes: cross-tier consistency report (parallel default; sequential fallback G2)
 └───────────┬────────────┘
             ▼
 ┌────────────────────────┐  ON muse-accept only (work→kb promotion, constraint #5)
 │ 11. chronicler         │  writes: kb/canon/, kb/timeline/,
 │     [BUILD-NEW]        │          kb/adaptations/<work>/tier-N/continuity.md  (per-tier, graft G1)
 └────────────────────────┘          kb/adaptations/<work>/tier-N/chapters/ch-NN/canon-delta.md
```

### 3.1 The safety revision loop (constraint #3 — the loop LAF lacked)

```
   writer(step 3) ──► critic/editor(4-5) ──► writer revise(6) ──► continuity(7) ──► safety-verifier(8)
        ▲                                                                                 │
        └──────────────────────────── FAIL (blocks promotion) ────────────────────────────┘
                                          │ PASS
                                          ▼
                                     reader-sim(9) ──► tier-coordinator(10) ──► chronicler(11)
```

The **loop is CWS's** (the writer→critic→writer cycle already exists in the adopted machinery); the
**trigger is LAF's** (`safety-verifier` FAIL). No adopted file is edited to wire this — the trigger lives
entirely in the native `safety-verifier` agent's body.

### 3.2 Multi-tier fan-out (Q1.5 / Q2.7)

`analyst` runs **once** per source chapter (tier-invariant source truth). `tier-coordinator` then fans
the transform across tiers:

```
                          ┌────► tier-1 pipeline (steps 3-9) ────┐
   analyst ch-NN ─────────┼────► tier-3 pipeline (steps 3-9) ────┼──► tier-coordinator ──► chronicler ×tier
   (once, shared)         └────► tier-5 pipeline (steps 3-9) ────┘   reconcile source-canon,
                                                                     tier-differentiated framing
   DEFAULT: parallel fan-out.
   FALLBACK (graft G2): sequential, for state-heavy works where tier-N canon must settle before tier-N+1.
```

---

## 4. Traceability — every LAF concept → concrete artifact

Extends the decision doc's integration map to the *file* that implements each concept.

| LAF concept | Concrete artifact (this spec) | Provenance |
|---|---|---|
| Five-tier axis | `skills/adaptation-tiers/SKILL.md` + `kb/tiers/tier_N.yaml`; passed as `active_tier` param | NATIVE — [`kb-formats.md §2`](kb-formats.md), [`skill-specs.md §1`](skill-specs.md) |
| Thematic + character transform rules | `skills/adaptation-rules/SKILL.md` + `resources/{thematic,character}.md` | NATIVE — [`skill-specs.md §2`](skill-specs.md) |
| Agency Externalization | `skills/adaptation-rules/resources/agency.md` (tier-conditional `mode:` ladder) | NATIVE — [`skill-specs.md §2.3`](skill-specs.md) |
| Concept mapping (universal + work) | `kb/adaptation-mapping/universal-mappings.yaml` + `<work>-mapping.yaml` (cascade) | NATIVE — [`kb-formats.md §3`](kb-formats.md) |
| v2.0 Pragmatic Verification Protocol | `skills/source-fidelity/SKILL.md` + `analyst` agent Phase 0-4 | NATIVE — [`skill-specs.md §3`](skill-specs.md), [`agent-schemas.md §2.1`](agent-schemas.md) |
| CERTAIN/PROBABLE/UNCERTAIN tags | `/source-fidelity` tag table; carried by adopted `story-memory` fact-extraction | NATIVE tag, ADOPTED carrier |
| safety_check (6-section) | `skills/adaptation-safety/SKILL.md` + `safety-verifier` agent | BUILD-NEW — [`safety-rubric.md`](safety-rubric.md), [`agent-schemas.md §2.2`](agent-schemas.md) |
| Source analysis pipeline | `analyst` → `work/analysis/ch-NN.yaml` | NATIVE — [`agent-schemas.md §2.1`](agent-schemas.md) |
| Cross-chapter canon (tier-aware) | `kb/canon/` + per-tier `kb/adaptations/<work>/tier-N/continuity.md` | ADOPTED base + BUILD-NEW populator + NATIVE per-tier ext (G1) — [`kb-formats.md §4`](kb-formats.md) |
| Quality critique | adopted critic/editor/reader-sim quartet | ADOPTED as-is |
| Revision loop on FAIL | adopted writer→critic→writer cycle, native `safety-verifier` trigger | ADOPTED loop, NATIVE trigger |
| work_mapping_template | `templates/work-mapping-template.yaml` → copied to `kb/adaptations/<work>/` at onboarding | NATIVE content, ADOPTED project-setup pattern |
| Multi-tier coordination | `tier-coordinator` agent (parallel default, sequential fallback G2) | BUILD-NEW — [`tier-coordinator.md`](tier-coordinator.md) |

---

## 5. Constraint Enforcement Map (all 6 — where each is mechanized)

| # | Constraint | Enforced by (concrete artifact) |
|---|---|---|
| 1 | LAF tier axis first-class | `active_tier` is an explicit input parameter in `analyst`, `writer`, `safety-verifier`, `tier-coordinator`, `chronicler` schemas ([`agent-schemas.md`](agent-schemas.md)); `kb/tiers/` is a native kb layer, never dissolved into persona/genre |
| 2 | Uncertainty discipline | `analyst` Phase 0 ABORT-on-NO-ACCESS in agent body; `/source-fidelity` mandates tags before transform ([`skill-specs.md §3`](skill-specs.md)) |
| 3 | safety_check | `safety-verifier` agent + `/adaptation-safety` rubric; verdict contract blocks promotion on FAIL ([`safety-rubric.md`](safety-rubric.md)) |
| 4 | Quartet (4 distinct) + 5th | 4 adopted agents vendored as distinct files; `safety-verifier` is a 5th native agent, never merged. **G3 written invariant** documented in `VENDOR.md` and asserted by `check_boundary.py` (editor.md present & unmodified) |
| 5 | work/ vs kb/ split | Adopted `kb-management` lifecycle; `chronicler` writes to `kb/` **only on muse-accept**; all native subdirs (`work/analysis`, `work/safety-reports`) live under `work/` |
| 6 | skill-vs-agent (boundary contract) | `check_boundary.py` proves adopted agent bodies are byte-identical to `VENDOR.md` manifest hashes; native knowledge enters only via `skills:` frontmatter ([`boundary-contract.md`](boundary-contract.md)) |

---

## 6. Residual Risks → Design Mitigations

| Risk (from adversarial cost analysis) | Design mitigation (specified in this pack) |
|---|---|
| Boundary drift ("just tweak an adopted agent") | `VENDOR.md` SHA-256 per-file manifest + `check_boundary.py` pre-commit/CI gate ([`boundary-contract.md`](boundary-contract.md)) |
| "Hybrid → everything half-done" | Phase 3 hard gate: full 11-step run on a real Tolkien chapter across 3 tiers before 0.1 ships (§7) |
| Two-provenance cognitive load | Every file's provenance is declared in `VENDOR.md`; frontmatter carries no ambiguity; adopted subset is deliberately small (13) |
| Upstream-sync of partial tree | Sync touches ADOPTED files only, pinned to the `VENDOR.md` SHA; NATIVE/BUILD-NEW never synced |
| Latent divergent-canon bug | Per-tier `continuity.md` + `(work, tier, chapter)` key in `chronicler` + `tier-coordinator` (graft G1) ([`kb-formats.md §4`](kb-formats.md)) |

---

## 7. Build Phases & Gates (design → implementation handoff)

| Phase | Deliverable | Gate |
|---|---|---|
| **0. Vendor** | Copy 6 adopted review/orch agents (from CWS `cw/agents/`) + 12 adopted skills + `kb/`+`work/` structure into `laf-adaptation/`. Write `VENDOR.md` with upstream SHA + per-file hashes. | `check_boundary.py --init` passes; **zero edits to vendored files** |
| **1. Native spine** | Author `/adaptation-tiers`, `/adaptation-rules`, `/source-fidelity`; build `analyst` + `safety-verifier`; add `/adaptation-rules` to `writer`'s `skills:` frontmatter (frontmatter-only). Port LAF configs verbatim into `kb/tiers/` + `kb/adaptation-mapping/`. | All native skills validate; `writer` diff is frontmatter-only; configs carried with zero rework |
| **2. Greenfield** | Build `chronicler` (tier-aware, per-tier `continuity.md`, G1) + `tier-coordinator` (parallel fan-out, sequential fallback G2). Add `/adaptation-safety` + genre resources. | Both agents block on nothing upstream; kb native layers created |
| **3. Compose & prove (HARD GATE)** | Run the full 11-step workflow on one Tolkien chapter at Tier 1; then same chapter at Tiers 1/3/5 through `tier-coordinator`. | v2.0 tags present · safety PASS · per-tier canon written · all four quartet agents ran · `check_boundary.py` green |
| **4. Upstream-sync protocol** | Document the reconcile procedure: `diff` vendored subset vs upstream SHA; apply non-conflicting patches to adopted files only. | Native files never touched by sync; SHA re-pinned in `VENDOR.md` |

---

## 8. Next Step

```
/sc:implement @.dev/releases/current/0.1/design/DESIGN.md
```

Implementation should proceed phase-by-phase (0→4) and treat the companion specs as the buildable source
of truth. The Phase 3 hard gate is the definition of "0.1 done."
