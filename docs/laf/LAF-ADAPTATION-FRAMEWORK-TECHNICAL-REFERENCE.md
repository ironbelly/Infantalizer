---
id: "LAF-ADAPTATION-FRAMEWORK-TECHREF"
title: "LAF Adaptation Framework - Technical Reference"
description: "Post-implementation technical reference documenting the architecture, subsystems, pipelines, tier axis, kb layer, and boundary contract of the LAF (Literary Adaptation Framework) as currently built."
version: "1.0"
status: "🟡 Draft"
type: "📖 Technical Reference"
priority: "🔼 High"
created_date: "2026-07-08"
updated_date: "2026-07-08"
assigned_to: "adaptation-framework"
autogen: true
autogen_method: "tech-reference skill (direct build) — code-verified against laf-adaptation/ @ feature/laf-0.1-artifacts-and-docs"
coordinator: "orchestrator"
parent_doc: ""
related_prd: ""
related_tdd: ""
depends_on:
- "laf-adaptation/CLAUDE.md"
- "laf-adaptation/VENDOR.md"
related_docs:
- "docs/design_decisions/001-five-tier-system.md"
- "docs/design_decisions/003-agency-externalization.md"
- "docs/native-prep/design/path-contract.md"
tags:
- technical-reference
- laf-adaptation
- post-implementation
- architecture
- framework
template_schema_doc: "/config/.claude/templates/documents/technical_reference_template.md"
verified_against_code:
  last_verified_date: "2026-07-08"
  verified_by: "tech-reference skill (direct build)"
  code_version: "feature/laf-0.1-artifacts-and-docs"
---

# LAF Adaptation Framework - Technical Reference

> **WHAT:** Post-implementation technical reference for the LAF (Literary Adaptation Framework) under `laf-adaptation/` — a prompt + YAML-config framework (ADR-006: *not software*) that adapts a source novel into developmentally-graded renditions across Tiers 1/2/3/5 via two pipelines (prep → rewrite), a multi-agent review workflow, a native knowledge-base layer, and a hash-pinned boundary contract.
> **WHY:** Canonical source of truth for AI agents and human contributors who need to run, understand, or extend the framework without reading every agent body and skill. Where in-tree prose (e.g. `CLAUDE.md` counts) diverges from the actual tree, **this document is authoritative and records the drift** (§14).
> **HOW TO USE:** Consult before adding a work, a tier, an agent, or a skill; before touching the boundary contract; or when onboarding to the two pipelines.

### Document Information

| Field | Value |
|-------|-------|
| **Feature Name** | LAF (Literary Adaptation Framework) |
| **Feature Type** | Framework / Prompt-and-Config System (no runtime binary) |
| **Source Location** | `laf-adaptation/` |
| **Last Verified Against Code** | 2026-07-08 (branch `feature/laf-0.1-artifacts-and-docs`) |
| **Implementation Status** | Stable (0.1 DONE — Phases 0–2 complete) |
| **Tier** | Standard |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Directory Structure](#3-directory-structure)
4. [Data Flow](#4-data-flow)
5. [Subsystem Reference](#5-subsystem-reference)
6. [State Management](#6-state-management)
7. [Component Inventory](#7-component-inventory)
8. [API & Integration Points](#8-api--integration-points)
9. [Configuration & Environment](#9-configuration--environment)
10. [Error Handling & Edge Cases](#10-error-handling--edge-cases)
11. [Performance Characteristics](#11-performance-characteristics)
12. [Conventions & Patterns](#12-conventions--patterns)
13. [Extension Guide](#13-extension-guide)
14. [Known Limitations & Technical Debt](#14-known-limitations--technical-debt)
15. [Verification & Accuracy](#15-verification--accuracy)
16. [Glossary](#16-glossary)

---

## 1. Overview

**What it does:** LAF takes a source literary work and produces **tier-graded adaptations** of it — the same story rendered for four developmental audiences (Tier 1 ages 3–5, Tier 2 ages 6–8, Tier 3 ages 9–11, Tier 5 ages 15–17; Tier 4 is interpolated on demand, never stored). It does this through two pipelines: **prep** (onboard a work → derive a confidence-scored adaptation mapping → greenlight) and **rewrite** (per-chapter 11-step multi-agent workflow → cross-tier reconciliation → canon promotion).

**Who uses it:** AI agents driven by two slash commands (`/laf:prep`, `/laf:rewrite`) run inside Claude Code, plus human authors who review at the two HALT gates (question gate, greenlight). There is no server and no end-user runtime.

**Where it lives:** `laf-adaptation/` — 16 agents, 18 skills, a native `kb/` layer, one enforcement script (`scripts/check_boundary.py`), plus `source/`, `work/`, and `templates/`. Pipeline entry points live at the repo root under `.claude/commands/laf/`.

**Key numbers:** 16 agents (11 adopted-provenance incl. 1 ADOPTED-PATCHED, 2 NATIVE, 2 BUILD-NEW, + supporting adopted); 18 skills (12 ADOPTED CWS, 3 NATIVE, 1 BUILD-NEW, + prep/thematic-fidelity NATIVE); 4 stored tier profiles (T4 interpolated); 1 runtime script (`check_boundary.py`, 737 lines) + its test; a 67-row per-file vendor manifest; an 11-step per-chapter rewrite workflow; an 8-stage prep procedure emitting an 8-file package. *(Counts verified against the live tree 2026-07-08; note the CLAUDE.md drift recorded in §14.)*

**Design paradigm (ADR-006):** LAF is a **prompt + YAML-config framework, not software**. There is exactly one script and it is a *validation tool*, not a runtime. "Behavior" lives in agent bodies (`*.md`) and skill bodies (`SKILL.md`) that Claude Code reads and executes; "configuration" lives in YAML under `kb/`.

---

## 2. Architecture

### 2.1 High-Level Architecture

LAF is a **provenance-partitioned, tier-aware adaptation pipeline**. It vendors a domain-agnostic creative-writing toolkit (CWS) verbatim and grafts a native adaptation spine on top, held apart by a hash-pinned boundary contract.

```
                         ┌──────────────────────────────────────────────┐
   /laf:prep  ─────────► │  PREP PIPELINE  (prep-cordinator, opus)       │
   "<title>" --source    │  8 stages: research→analysis→challenges→      │
                         │  mapping→[question gate HALT]→[greenlight HALT]│
                         │  →dual-form promotion→handoff                 │
                         └───────────────┬──────────────────────────────┘
                                         │ emits work/prep/<slug>/ (8 files)
                                         │ + promotes <work>-mapping.yaml
                                         ▼
   /laf:rewrite ───────► ┌──────────────────────────────────────────────┐
   --work <slug>         │  REWRITE PIPELINE  (muse orchestrates)        │
                         │  per chapter, 11 steps:                       │
                         │  analyst→muse→writer→critic→editor→writer(rev)│
                         │  →continuity-checker→safety-verifier→reader-  │
                         │  sim→tier-coordinator→chronicler              │
                         └───────┬───────────────────────┬──────────────┘
                                 │ reads                  │ writes on accept
                                 ▼                        ▼
   ┌─────────────────────────────────────┐   ┌───────────────────────────────┐
   │  TIER AXIS + KB (config + canon)     │   │  BOUNDARY CONTRACT             │
   │  kb/tiers/*.yaml (1,2,3,5; T4 interp)│   │  scripts/check_boundary.py     │
   │  kb/adaptation-mapping/<work>.yaml   │   │  VENDOR.md manifest (67 rows)  │
   │  kb/canon/ (shared) + kb/adaptations/│   │  Rules A–F, Modes V/U          │
   │  <work>/tier-<N>/ (per-tier, graft G1)│  │  .githooks/pre-commit + CI     │
   └─────────────────────────────────────┘   └───────────────────────────────┘
```

### 2.2 Subsystem Map

| Subsystem | Purpose | Primary Directory | Key Files |
|-----------|---------|-------------------|-----------|
| Rewrite pipeline & 11-step workflow | Per-chapter multi-agent adaptation → reconcile → promote canon | `agents/`, `.claude/commands/laf/rewrite.md` | `muse.md`, `tier-coordinator.md`, `chronicler.md` |
| Prep pipeline | Onboard a work → derive mapping → greenlight → handoff | `agents/prep-cordinator.md`, `skills/prep/` | `prep-cordinator.md`, `prep/SKILL.md`, `path-contract.md` |
| Tier axis | 5-tier Piaget/Kohlberg developmental model + transform-mode ladder | `kb/tiers/`, `skills/adaptation-tiers/` | `tier_1.yaml`…`tier_5.yaml` |
| Transform rules & meaning-preservation | Violence/conflict/death/villain/heroism transforms; Agency Externalization; source-fidelity; safety rubric; meaning invariant | `skills/adaptation-rules,adaptation-safety,source-fidelity,thematic-fidelity/` | `adaptation-rules/SKILL.md`, `adaptation-safety/SKILL.md` |
| KB layer & work/kb split | Dual-layer canon (shared + per-tier graft G1); mapping cascade; work/ staging vs kb/ durable | `kb/`, `work/` | `kb/canon/`, `kb/adaptations/<work>/tier-<N>/` |
| Boundary contract & provenance | Keep the vendored CWS subset patch-clean; enforce ADOPTED/NATIVE/BUILD-NEW split | `scripts/`, `VENDOR.md`, `CLAUDE.md` | `check_boundary.py`, `VENDOR.md`, `UPSTREAM-SYNC.md` |

### 2.3 Key Design Decisions (As Built)

| Decision | What Was Built | Rationale |
|----------|---------------|-----------|
| Framework, not software (ADR-006) | Exactly one script (`check_boundary.py`), a *validator* not a runtime | Behavior belongs in prompts/YAML; a runtime would drift from the prompt layer |
| Five-tier axis (ADR-001) | Tiers 1/2/3/5 stored as YAML profiles; T4 interpolated at request time | Discrete Piaget/Kohlberg bands; T4 is a conservative T3↔T5 midpoint, not a maintained file |
| Agency Externalization (ADR-003) | Signature transform rule: badness is a STATE/accident (T1-2 mandatory) → optional (T3) → forbidden (T4-5) | Protects youngest readers without patronizing older ones |
| Boundary contract (constraint #6) | NATIVE knowledge enters ADOPTED agents ONLY via `skills:` frontmatter; `check_boundary.py` proves adopted bodies match `VENDOR.md` hashes | Keeps the vendored CWS subset a clean 3-way-merge fast-forward against upstream |
| Quartet-of-4 + 5th (constraint #4) | critic/editor/reader-sim/continuity-checker vendored as 4 distinct files; `safety-verifier` a distinct native 5th reviewer; `editor.md` never folded (Rule D) | Independent review stances; distinctness asserted mechanically |
| Meaning preservation (R10) | `meaning:` field + tier-coordinator Check D; surface transforms but never add/strip the work's allegory/theme | Adaptation changes *how* a thing reads, not *what it means* |

### 2.4 Technology Stack (Feature-Specific)

| Technology | Version | Purpose in This Feature |
|------------|---------|------------------------|
| Claude Code harness | current | Reads `laf-adaptation/` directly; runs agents/skills/commands |
| Python (stdlib only) | UV-invoked | `check_boundary.py` — sha256 hashing + manifest verification; no third-party deps (ADR-006) |
| YAML | — | Tier profiles, work mappings, per-chapter analysis, the vendor manifest |
| Markdown + frontmatter | Claude-native dialect | Agent/skill bodies; `name`/`description`/`model`/`skills`/`tools` (agents), `name`/`description` (skills) |

---

## 3. Directory Structure

```
laf-adaptation/
├── CLAUDE.md            # NATIVE; provenance model, boundary summary, 6 constraints, tree map (not hash-pinned)
├── VENDOR.md            # BOUNDARY CONTRACT: pinned upstream SHA + 67-row per-file sha256 manifest
├── UPSTREAM-SYNC.md     # the 6-step upstream-sync procedure for the vendored CWS subset
├── NOTICE, LICENSE-CWS  # Apache-2.0 attribution for the vendored files
├── agents/              # 16 agent bodies (rewrite workflow + prep-cordinator + supporting adopted)
├── skills/              # 18 skill dirs (12 ADOPTED CWS + 3 NATIVE + 1 BUILD-NEW + prep/thematic-fidelity NATIVE)
├── kb/
│   ├── tiers/           # NATIVE: tier_1/2/3/5.yaml (T4 interpolated, never stored)
│   ├── adaptation-mapping/   # NATIVE: universal-mappings.yaml + <work>-mapping.yaml (cascade)
│   ├── adaptations/<work>/tier-<N>/   # NATIVE graft G1: per-tier divergent canon, keyed (work,tier,chapter)
│   ├── canon/ characters/ world/ timeline/ styles/ issues/ vocab.md   # ADOPTED scaffold (runtime-populated)
├── scripts/             # check_boundary.py (737 lines, the ONLY script) + test_check_boundary.py
├── source/<work>/       # BUILD-NEW: the work being adapted (read-only reference), ch-<NN>.txt
├── work/                # ADOPTED lifecycle: analysis/ (NATIVE) drafts/ critique-reports/ safety-reports/ (NATIVE); prep/<slug>/
├── templates/           # work-mapping-template.yaml (NATIVE, carried verbatim)
└── .githooks/pre-commit # opt-in boundary-check enforcement wrapper

.claude/commands/laf/    # (repo root, NOT under laf-adaptation/) prep.md + rewrite.md — the two entry points
```

### 3.1 File Naming Conventions

| Pattern | Convention | Example |
|---------|-----------|---------|
| Skill reference | fully-qualified `laf-adaptation:<slug>` in agent `skills:` frontmatter | `laf-adaptation:adaptation-rules` |
| Work mapping (kb, 0.1) | hyphen + `meaning:` kept | `kb/adaptation-mapping/narnia-mapping.yaml` |
| Work mapping (root, v1.0) | underscore + `meaning:` stripped (frozen 5-key schema) | `config/concept_mapping/templates/narnia_mapping.yaml` |
| Per-chapter analysis | `work/analysis/ch-<NN>.yaml` (+ `ch-<NN>-cross-tier.md`) | `work/analysis/ch-01.yaml` |
| Prep package | fixed names `00-…`…`70-…` under `work/prep/<slug>/` | `work/prep/narnia/30-mapping.yaml` |

---

## 4. Data Flow

### 4.1 Prep Flow (onboard → greenlight → handoff)

```
"<title>" --source <path>
   → prep-cordinator (opus) runs the 8-stage /prep procedure:
     Stage 1 two-track research (context + text)
     Stage 2 source-fidelity analysis  (analyst, granularity: work) → 20-analysis-work-level.yaml
     Stage 3 challenge-taxonomy classification → 10-challenges.yaml
     Stage 4 derive confidence-scored <work>-mapping → 30-mapping.yaml (+ top-level meaning:)
     Stage 5 QUESTION GATE (HALT — ask only human-judgment challenges)
     Stage 6 GREENLIGHT GATE (HALT — user confirms; status PENDING→CONFIRMED)
     Stage 7 dual-form promotion (6-key kb copy keeps meaning:; 5-key root copy strips it)
     Stage 8 handoff → prints the /laf:rewrite paste-able prompt
   → work/prep/<slug>/ = 8 fixed files (00-work-context … 70-traceability)
```

### 4.2 Rewrite Flow (per-chapter 11-step workflow)

The rewrite phase reads the prep package by **hardcoded path** (path-contract §4: `30-mapping.yaml`, `40-prep-brief.md`, `10-challenges.yaml`), confirms `50-greenlight.md` = `CONFIRMED`, then hands chapter 1 to `muse`. Per chapter:

```
 1 analyst            → work/analysis/ch-NN.yaml (tier-invariant source truth; ABORT on NO-ACCESS)
 2 muse               (orchestrates; owns the verdict)
 3 writer             → work/drafts/ch-NN-tN-vM.md   (per tier)
 4 critic     ┐ adversarial craft review (read-only)
 5 editor     ┘ holistic editorial memo (read-only)
 6 writer (revision)  → v2
 7 continuity-checker (read-only; vs source truth + prior per-tier continuity)
 8 safety-verifier    (T1-2 BLOCKING, T3 advisory, T4-5 skip) → work/safety-reports/ch-NN-tN.md
 9 reader-sim         (experiential read for the tier persona; read-only)
10 tier-coordinator   → work/analysis/ch-NN-cross-tier.md; Checks A/B/C/D; RECONCILED|CONFLICT
11 chronicler         (ON muse-accept + RECONCILED) → promotes canon (shared + per-tier)
```

Steps 3–9 run per tier; step 10 fans across the `tiers` set (parallel default); step 11 runs per tier on accept.

### 4.3 Data Sources

| Source | Type | Location | Description |
|--------|------|----------|-------------|
| Source work | Static text | `source/<work>/ch-NN.txt` | The novel being adapted (read-only reference) |
| Tier profiles | Static YAML | `kb/tiers/tier_{1,2,3,5}.yaml` | Thresholds, linguistic limits, transformation_rules per tier |
| Work mapping | Derived YAML | `kb/adaptation-mapping/<work>-mapping.yaml` | Per-entry tier renderings + top-level `meaning:` (6-key form) |
| Prep package | Derived | `work/prep/<slug>/` | The onboarding artifacts the rewrite phase consumes |
| Vendor manifest | Static | `VENDOR.md` | Pinned upstream SHA + per-file hashes (integrity trust root) |

### 4.4 Data Transformations

| Transformation | Input | Output | Location |
|---------------|-------|--------|----------|
| Source analysis | `source/<work>/ch-NN.txt` | confidence-tagged `ch-NN.yaml` (+ `meaning`, `compound_scene`) | analyst + `/source-fidelity` |
| Tier transform | analysis + tier profile + mapping | per-tier `adapted.md` | writer + `/adaptation-rules` |
| Cross-tier reconcile | per-tier `adapted.md` set | `ch-NN-cross-tier.md` + RECONCILED/CONFLICT | tier-coordinator |
| Canon promotion | accepted `adapted.md` + analysis | shared `kb/canon/` + per-tier `kb/adaptations/<work>/tier-<N>/` | chronicler |
| Dual-form promotion | 6-key `30-mapping.yaml` | 6-key kb copy + 5-key root copy | prep-cordinator (greenlight) |

---

## 5. Subsystem Reference

### 5.1 Rewrite Pipeline & the 11-Step Workflow

**Purpose:** Adapt one source chapter into per-tier renderings, reconcile them for cross-tier consistency, and promote durable canon — under a single author-facing orchestrator (`muse`).

**Key Files:**

| File | Purpose |
|------|---------|
| `.claude/commands/laf/rewrite.md` | `/laf:rewrite --work <slug>` entry point; reads prep package by hardcoded path, greenlight-gates, hands ch.1 to `muse` |
| `agents/muse.md` (opus) | Author-facing orchestrator; spawns specialists, judges results, owns the verdict |
| `agents/analyst.md` (opus) | Step 1 — tier-invariant source analysis; **ABORTS on NO-ACCESS** (constraint #2) |
| `agents/{critic,editor,reader-sim,continuity-checker}.md` | The distinct review quartet (constraint #4; graft G3) |
| `agents/safety-verifier.md` (sonnet) | The distinct native 5th reviewer; T1-2 blocking gate |
| `agents/tier-coordinator.md` (opus) | Step 10 — fans tiers, runs Checks A/B/C/D, emits RECONCILED/CONFLICT |
| `agents/chronicler.md` (sonnet) | Step 11 — promotes canon on accept, keyed `(work, tier, chapter)` |

**How It Works:** `muse` interprets author intent and routes each step to the most specific specialist, keeping stances in separate spawns so critique never contaminates drafting. The workflow order is `analyst → muse → writer → critic → editor → writer(rev) → continuity-checker → safety-verifier → reader-sim → tier-coordinator → chronicler` (proven end-to-end by the Phase-3 hard gate; agents branch on this order but do not renumber it). Two mechanical gates govern promotion: **safety-verifier** (a blocking FAIL at T1-2 re-enters the writer loop with `verdict.evidence` as revision notes — constraint #3) and **tier-coordinator** (`chronicler` runs only after `status: RECONCILED` with an empty `conflicts:` list). Analyst is **tier-invariant** — it runs once per chapter and every tier's transform reads the same source truth.

**Agent I/O contract (models + write-capability):**

| Agent | Model | Writes? | Gate/role |
|-------|-------|---------|-----------|
| analyst | opus | Write (analysis) | pre-orchestration; ABORT on NO-ACCESS |
| muse | opus | Write/Edit | orchestrator |
| writer | opus | Write/Edit | production prose (ADOPTED-PATCHED, +1 skills line) |
| critic | sonnet | **read-only** | adversarial craft critique |
| editor | sonnet | **read-only** | editorial memo (never folded — Rule D) |
| continuity-checker | inherit | **read-only** (+Bash) | canon-contradiction check |
| safety-verifier | sonnet | Write (report only) | T1-2 blocking / T3 advisory / T4-5 skip |
| reader-sim | opus | **read-only** | experiential per-tier read |
| tier-coordinator | opus | Write (report) | reconcile; never writes canon |
| chronicler | sonnet | Write (canon) | promote on accept |

**Consumers:** produces `kb/canon/<work>/` and `kb/adaptations/<work>/tier-<N>/` consumed by later chapters (running continuity) and downstream tooling.

**Conventions:** Read-only reviewers (`critic`, `editor`, `reader-sim`, `continuity-checker`) return findings inline — the orchestrator persists their reports. The write-capable agents are `analyst`, `muse`, `writer`, `safety-verifier` (report only), `tier-coordinator` (report only), and `chronicler` (canon).

### 5.2 Prep Pipeline

**Purpose:** Onboard a *new* work: research it, analyze the source (text required), classify its adaptation challenges, derive a confidence-scored `<work>-mapping`, gate on human judgment + greenlight, and hand off to rewrite.

**Key Files:**

| File | Purpose |
|------|---------|
| `.claude/commands/laf/prep.md` | `/laf:prep "<title>" [--source <path>]` — delegates entirely to `prep-cordinator` |
| `agents/prep-cordinator.md` (opus) | Owns the 8-stage procedure + two HALT gates; edits no adopted body |
| `skills/prep/SKILL.md` | The 8-stage procedure spec |
| `skills/prep/resources/path-contract.md` | **Single source of truth** for package layout, promotion targets, `rewrite_phase_reads`, and write-ownership |

**How It Works:** The coordinator runs two-track research (context + text), gates the source through `/source-fidelity` (ABORT if no text), classifies challenges into a typed taxonomy, and derives `30-mapping.yaml` with per-entry `confidence = min(text, context)` plus a top-level `meaning:`. It then HALTs twice: the **question gate** asks only human-judgment challenges (deterministic ones — violence-level, death-euphemism — are never asked); the **greenlight gate** takes the user's confirmation (`status: PENDING → CONFIRMED`). On greenlight the coordinator performs the **dual-form transform** itself, writing two mapping copies (see §5.5), then prints the paste-able `/laf:rewrite` handoff.

**Public Interface (the 8-file package, fixed names/order):** `00-work-context.md`, `10-challenges.yaml`, `20-analysis-work-level.yaml`, `30-mapping.yaml`, `40-prep-brief.md`, `50-greenlight.md`, `60-handoff-prompt.md`, `70-traceability.md`.

**Consumers:** the rewrite pipeline reads exactly three of these by hardcoded path (`30`, `40`, `10`) and confirms `50` = CONFIRMED; it never reads `70` (human/greenlight audit only).

**Conventions:** the prep phase **never** writes canon or per-tier adaptation state — that boundary belongs to the rewrite phase's `chronicler` (path-contract §5).

### 5.3 Tier Axis

**Purpose:** A single developmental axis, five tiers, grounded in Piaget/Kohlberg, that parameterizes every transform.

**Key Files:** `kb/tiers/tier_{1,2,3,5}.yaml` (profiles); `skills/adaptation-tiers/SKILL.md` (axis vocabulary + interpolation rule).

**How It Works:** Each profile carries `thresholds` (violence/emotional/moral-ambiguity/narrative levels), `linguistic` limits (max words/sentence, vocab grade, chapter max), and `transformation_rules`. The **transformation-mode ladder** is the signature cross-cutting case — Agency Externalization is `mandatory` (T1-2) → `optional` (T3) → `forbidden` (T4-5). Agents consume the tier differently: `active_tier` is an explicit param for `safety-verifier`/`chronicler`; `tier-coordinator` fans a `tiers` set; `writer` receives the tier via its scene brief + `/adaptation-rules`; `analyst` takes **no** tier (tier-invariant).

| Tier | Ages | Paradigm | Agency-Ext | Safety gate |
|------|------|----------|-----------|-------------|
| 1 | 3–5 | Maximum transformation, maximum safety | mandatory | blocking |
| 2 | 6–8 | Conflict as contest/competition | mandatory | blocking |
| 3 | 9–11 | TRANSITION — complexity unlocked | optional | advisory |
| 4 | 12–14 | Interpolated (T3 floor, T5 ceiling, midpoint) | forbidden | skip |
| 5 | 15–17 | Minimal transformation — preserve author intent | forbidden | skip |

**Tier 4 note:** never stored as a file. It is interpolated at request time (conservative midpoint; `agency_externalization = FORBIDDEN`). No `tier_4.yaml` exists — the axis is `{1,2,3,5}` on disk.

**Consumers:** every transform, safety check, and reconciliation reads a tier profile.

### 5.4 Transformation Rules & Meaning-Preservation

**Purpose:** The domain logic that changes a scene's *surface* per tier while preserving its *meaning*.

**Key Files:**

| File | Purpose |
|------|---------|
| `skills/adaptation-rules/SKILL.md` | violence/conflict/death/villain/heroism/character transforms; Agency Externalization; **key-tolerant** schema-drift reader |
| `skills/source-fidelity/SKILL.md` | v2.0 anti-hallucination protocol: CERTAIN/PROBABLE/UNCERTAIN tags, ABORT-on-NO-ACCESS, the analysis v2.0 schema |
| `skills/adaptation-safety/SKILL.md` | 6-section safety rubric (forbidden-content, agency-ext, emotional-safety, safe-home, nightmare-prevention, linguistic) |
| `skills/thematic-fidelity/SKILL.md` | meaning-preservation invariant; defines the analyst `meaning` field and tier-coordinator Check D |

**How It Works:** A source element is categorized (violence | conflict | death | villain | heroism | character), the active tier's rule row is looked up, and its `translations`/`target`/`strategy` applied. **Intentional schema drift** is absorbed in the reader, never the data: T1-3 use `conflict_to_cooperation`/`death_euphemism`, T5 uses `conflict_handling`/`death_handling`; skills read key-tolerantly (`profile.get(a) or profile.get(b)`). Source-fidelity mandates a confidence tag on every extracted fact and a Phase-0 ABORT gate (no source text ⇒ `status: ABORTED`, nothing downstream proceeds). The safety rubric emits a machine-parseable verdict that gates kb promotion at T1-2. Meaning-preservation (R10) rides the reconcile gate: Check D flags a `Meaning-DIFF` as a `conflicts:` entry, blocking `chronicler` exactly as an A/B/C conflict does.

**Consumers:** `writer` (transforms), `safety-verifier` (rubric), `analyst` (fidelity + meaning), `tier-coordinator` (Check D).

**Conventions:** never normalize the schema-drift keys in the vendored YAML; never strip a work's asserted allegory or add one the source withholds.

### 5.5 KB Layer & the work/ vs kb/ Split

**Purpose:** Persist adaptation state in two layers — shared tier-neutral source truth and per-tier divergent canon — with a staging area (`work/`) separate from durable knowledge (`kb/`).

**Key Files:** `kb/canon/<work>/ch-NN.md` (shared), `kb/timeline/<work>.md` (shared), `kb/adaptations/<work>/tier-<N>/{continuity.md,decisions.md,chapters/ch-NN/{adapted.md,analysis.yaml,canon-delta.md}}` (per-tier, **graft G1**), `kb/adaptation-mapping/<work>-mapping.yaml` (cascade).

**How It Works:** `chronicler` writes canon **only on muse-accept** and **after** RECONCILED (constraint #5). It holds three load-bearing invariants: (1) key every per-tier write with `(work, tier, chapter)` — work/tier via directory path, chapter via per-chapter path + stamped entries; (2) never bleed a tier-N fact into another tier's `continuity.md`; (3) **never** promote a tier-transformed name (e.g. a T1 gloss) into shared `kb/canon/` — shared canon holds source names only, with `analysis.yaml`'s source name as the reference oracle. The **dual-form promotion** (prep phase) writes two mapping copies: the 0.1 kb copy (hyphen, keeps `meaning:`, keeps `_confidence` diagnostics) and the root v1.0 copy (underscore, strips `meaning:` and `_confidence` to validate against the frozen 5-key schema). `work/` (analysis, drafts, critique-reports, safety-reports, prep) is staging; `kb/` is durable.

**Consumers:** later chapters read running `continuity.md`; `tier-coordinator` Check D reads the 6-key mapping's `meaning:`.

**Conventions:** the ADOPTED kb scaffold (`canon/`, `characters/`, `world/`, `timeline/`, `styles/`, `issues/`, `vocab.md`) is runtime-populated; the NATIVE layers (`tiers/`, `adaptation-mapping/`, `adaptations/<work>/`) are the adaptation spine.

### 5.6 Boundary Contract & Provenance

**Purpose:** Keep the vendored CWS subset patch-clean and upstream-syncable while allowing a native adaptation spine to live alongside it.

**Key Files:** `scripts/check_boundary.py` (737 lines — the ONLY script), `scripts/test_check_boundary.py`, `VENDOR.md` (67-row per-file manifest), `CLAUDE.md` (provenance model), `UPSTREAM-SYNC.md`, `.githooks/pre-commit`.

**How It Works:** Every file is **ADOPTED** (vendored CWS, body never edited), **ADOPTED-PATCHED** (exactly one: `agents/writer.md`, adopted body + 1 additive `skills:` line), **NATIVE** (LAF-authored spine), or **BUILD-NEW** (greenfield). NATIVE knowledge enters ADOPTED agents **only** via `skills:` frontmatter — never by editing an adopted body (constraint #6). `check_boundary.py` enforces this against `VENDOR.md` hashes:

| Rule | What it asserts |
|------|-----------------|
| A | every adopted file matches its recorded `laf_sha256` |
| A′ (CH-1) | every ADOPTED-CLEAN body re-derives (inverse prefix rewrite) to its pinned `upstream_sha256` |
| B / C | (Mode U) full upstream diff of adopted bodies |
| C′ (CH-3) | ADOPTED-PATCHED reserved for `agents/writer.md` only |
| D | review quartet intact + `editor.md` never folded |
| E | no NATIVE/BUILD-NEW name collides with an upstream filename |
| F / F′ (CH-2) | every `agents/*.md` + `skills/**/SKILL.md` (and adopted `resources/**`) is manifested |

**Modes:** `Mode V` (verify, default — the single-field `laf_sha256`-forgery gate; runs in CI + the opt-in pre-commit hook) and `Mode U` (`--upstream <checkout>` — the absolute guarantee: Rules B/C diff + CH-5 asserts checkout HEAD == pinned `upstream_sha`). Hashes are computed over **LF-normalized text** (text-normalized, not byte-accurate — by design for a prompt+YAML framework). `Mode V` honestly does **not** catch a two-field forgery (rewriting BOTH hashes self-consistently) — that is Mode U's job plus branch protection + human review of any `upstream_sha256` diff.

**Consumers:** CI (`.github/workflows/boundary.yml`, run with `working-directory: laf-adaptation`) and the opt-in pre-commit hook.

**Conventions:** invoke via `uv run python scripts/check_boundary.py` (UV-only); adding NATIVE knowledge = add a skill + attach via frontmatter, never edit an adopted body.

---

## 6. State Management

**N/A — not applicable.** LAF is a prompt + YAML-config framework with no client-side runtime and no in-memory store. All "state" is durable on-disk artifacts (per-chapter analysis, drafts, per-tier canon, running `continuity.md`) covered in §5.5 (KB Layer) and §4 (Data Flow). There is no Zustand/Redux/Context-style store to document.

---

## 7. Component Inventory

**N/A — not applicable.** There are no UI components. The framework's "components" are agents (§5.1 table) and skills (§5.4), documented in the Subsystem Reference rather than a component tree.

---

## 8. API & Integration Points

### 8.1 Entry Points (slash commands)

| Command | Arguments | Purpose | Delegates to |
|---------|-----------|---------|--------------|
| `/laf:prep` | `"<title>" [--source <path>]` | Onboard a new work → prep package + greenlight | `prep-cordinator` (opus) |
| `/laf:rewrite` | `--work <slug>` | Begin the per-chapter rewrite phase | reads prep package → hands ch.1 to `muse` |

`--source` is a **required** input for prep (the novel text is mandatory; no memory-based work-level analysis). A URL is fetched to a local file first; the resolved local path is what `/source-fidelity` runs against.

### 8.2 Internal Integration Points (the load-bearing contracts)

| Integration | Direction | Mechanism | Description |
|-------------|-----------|-----------|-------------|
| prep → rewrite handoff | outbound | `path-contract.md` §4 `rewrite_phase_reads` | rewrite reads `30`/`40`/`10` by hardcoded path; confirms `50` = CONFIRMED |
| safety gate → writer loop | inbound | `verdict.evidence` | T1-2 blocking FAIL re-enters writer (constraint #3) |
| reconcile → chronicler | outbound | `status: RECONCILED`, empty `conflicts:` | chronicler promotes only after reconcile passes (constraint #5) |
| boundary check → commit/CI | gate | `check_boundary.py` exit code | non-zero exit blocks the pre-commit hook / CI |
| skill → agent | inbound | `skills:` frontmatter | the ONLY channel for NATIVE knowledge into ADOPTED agents (constraint #6) |

### 8.3 External Service Dependencies

None. The framework has no network runtime. The only external reference is the vendored upstream repo (`haowjy/creative-writing-skills` @ pinned SHA `3338495f…`), consumed at *vendor time* (Mode U diff), not at runtime.

---

## 9. Configuration & Environment

### 9.1 Configuration Files

| File | Purpose | Key Settings |
|------|---------|-------------|
| `kb/tiers/tier_{1,2,3,5}.yaml` | Per-tier constraint set | `thresholds`, `linguistic` (max words/sentence, vocab grade, chapter max), `transformation_rules` |
| `kb/adaptation-mapping/<work>-mapping.yaml` | Per-work overrides (cascade, most-specific-wins) | per-entry tier renderings + `meaning:` + `_confidence` |
| `VENDOR.md` | Boundary manifest | `upstream_repo`, `upstream_sha`, `prefix_rewrite`, 67 per-file `laf_sha256`/`upstream_sha256` rows |
| `work/prep/<slug>/50-greenlight.md` | Rewrite gate | `status: PENDING | CONFIRMED`, `tiers_active` |

### 9.2 Environment / Invocation

| Variable/Setting | Purpose | Notes |
|----------|---------|-------|
| UV | Python invocation | `uv run python scripts/check_boundary.py` — never bare `pip`/`python -m` (ADR-006) |
| `core.hooksPath` | Enable pre-commit gate | `git config core.hooksPath laf-adaptation/.githooks` (opt-in); `--no-verify` to bypass once |
| Active tier set | Which tiers a run adapts | default `{1,2,3,5}`; T4 interpolated at request time, never stored |

There are no environment variables or feature flags in the traditional sense — configuration is the YAML profiles + the greenlight gate.

---

## 10. Error Handling & Edge Cases

### 10.1 Error Handling Patterns (the gates)

| Gate | Trigger | Behavior | Recovery |
|------|---------|----------|----------|
| Phase-0 ABORT | analyst finds NO-ACCESS (missing/empty source) | `status: ABORTED`; nothing downstream proceeds (constraint #2) | supply source text and re-run |
| Safety FAIL→revise | T1-2 draft fails the 6-section rubric | blocks kb promotion; re-enters writer with `verdict.evidence` (constraint #3) | writer revises; re-verify (loop) |
| CONFLICT | tier-coordinator Check A/B/C/D fails (incl. Meaning-DIFF) | `status: CONFLICT`, non-empty `conflicts:`; blocks chronicler | muse re-dispatches offending tier's writer |
| Greenlight PENDING | `50-greenlight.md` not CONFIRMED | rewrite surfaces and stops | complete prep greenlight |
| Boundary FAIL | adopted body edited / hash mismatch / quartet folded | `check_boundary.py` exits non-zero | restore adopted body; add a skill instead of editing |

### 10.2 Known Edge Cases

| Scenario | Current Behavior | Notes |
|----------|-----------------|-------|
| MEMORY-BASED source | every extracted fact tagged UNCERTAIN | source-fidelity decision rule; prep forbids it (source required) |
| Compound scene (≥2 HIGH-severity flags co-occur) | `compound_scene: true`; per-tier reconciliation (the `/prep` §2.1 compound-scene protocol) | e.g. a Stone-Table-style sacrifice scene |
| T5 "preserve" of copyrighted text | preservation *record* pointing to in-repo source + supplementary scaffolding | reproducing the text verbatim is neither needed nor safe |
| Read-only reviewer output | returned inline, persisted by the orchestrator | `critic`/`reader-sim`/`continuity-checker` have no Write tool |

### 10.3 Graceful Degradation

Mode V runs without `--upstream` and prints a NOTE that Rules B/C are skipped — integrity still covered by Rule A hash-match + Rules D/E/F. The absolute guarantee (Mode U) is available on demand and in a dedicated CI path.

---

## 11. Performance Characteristics

> **Note:** LAF has no runtime binary, so "performance" is not a measured latency/throughput profile. The relevant cost shape is **agent parallelism and token spend**, controlled by the pipeline structure, not code optimization.

- **Parallel fan-out:** `tier-coordinator` fans tiers in parallel by default (sequential fallback, graft G2, only for state-heavy works). Independent review agents (critic + editor; the tier writers) run concurrently.
- **Single-script constraint (ADR-006):** exactly one Python script, stdlib-only, so `check_boundary.py` is O(files) sha256 hashing — trivial cost, run in the pre-commit hook and CI.
- **Token shape:** the dominant cost is the per-chapter × per-tier agent spawns of the rewrite workflow; reviewers write reports to disk incrementally rather than accumulating in context.

---

## 12. Conventions & Patterns

### 12.1 Code / Authoring Conventions

| Convention | Description |
|------------|-------------|
| Provenance discipline | Every file is ADOPTED / ADOPTED-PATCHED / NATIVE / BUILD-NEW; never edit an adopted body — add a skill and attach via `skills:` frontmatter |
| Frontmatter dialect | Claude-native only: agents use `name`/`description`/`model`/`skills`/`tools`; skills use `name`/`description`. **Never** introduce Mars keys (`type`, `model-invocable`, `effort`, `sandbox`, …) |
| Key-tolerant reads | Absorb the deliberate T1-3 vs T5 schema drift in the *reader* skill (`.get(a) or .get(b)`), never by normalizing the vendored YAML |
| UV-only Python | `uv run python …` — never `python -m` / bare `pip` |
| Carried-verbatim YAML | Port-source YAMLs are LF-normalized faithful copies of LAF's `config/`, including the deliberate schema drift |

### 12.2 Architectural Patterns

| Pattern | Where Used | Description |
|---------|-----------|-------------|
| Tier axis first-class | everywhere | `active_tier` explicit param; `kb/tiers/` a native layer, never dissolved into persona/genre |
| Adopt-and-graft | agents/, skills/ | vendor CWS verbatim; graft native spine held apart by the boundary contract |
| Gate-on-verdict | safety, reconcile, greenlight | machine-parseable verdicts gate promotion; no editorial judgment in the gate emission |
| Dual-layer canon (graft G1) | kb/ | shared source truth + per-tier divergent state keyed `(work, tier, chapter)` |

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead |
|-------------|----------------|-----------------|
| Editing an adopted agent body | breaks the clean 3-way merge; fails Rule A/A′ | add a NATIVE skill; attach via `skills:` frontmatter |
| Adding a second script | violates ADR-006 (framework, not software) | extend a skill or the YAML config |
| Normalizing the schema-drift keys | breaks the byte-faithful carry | read key-tolerantly in the skill |
| Promoting a tier-transformed name into shared canon | corrupts source truth (Inv.3) | keep tier renderings in the per-tier layer only |

---

## 13. Extension Guide

### 13.1 Common Extension Tasks

| Task | Steps | Files to Touch | Pitfalls |
|------|-------|---------------|----------|
| **Adapt a new work** | 1) `/laf:prep "<title>" --source <path>`; 2) answer the question gate; 3) confirm greenlight; 4) `/laf:rewrite --work <slug>` | `work/prep/<slug>/*` (created by prep); `kb/adaptation-mapping/<slug>-mapping.yaml` (promoted) | source text is mandatory; do not skip greenlight |
| **Add a NATIVE skill** | 1) create `skills/<name>/SKILL.md` (+ `resources/`); 2) attach via an agent's `skills:` frontmatter; 3) add a NATIVE row to `VENDOR.md` (NO_HASH `—`); 4) name must not collide with an upstream file (Rule E) | `skills/<name>/`, agent frontmatter, `VENDOR.md` | do NOT edit an adopted agent body to add behavior |
| **Adjust / add a tier** | edit `kb/tiers/tier_<N>.yaml` thresholds/linguistic/rules; T4 stays interpolated (never create `tier_4.yaml`) | `kb/tiers/tier_<N>.yaml`, `skills/adaptation-tiers/` | preserve monotonicity (T1 ≤ … ≤ T5 maturity) — the tier-coordinator Check C enforces it |
| **Bring a new agent under the boundary** | vendor the adopted body verbatim (prefix rewrite only); OR author a NATIVE/BUILD-NEW agent; add its `VENDOR.md` row; keep `writer.md` the sole ADOPTED-PATCHED | `agents/<name>.md`, `VENDOR.md` | Rule C′ reserves ADOPTED-PATCHED for `writer.md` only |
| **Sync from upstream** | follow `UPSTREAM-SYNC.md` (6 steps); run `check_boundary.py --upstream <checkout>` (Mode U) | vendored bodies, `VENDOR.md` pins | a two-field hash forgery is only caught in Mode U + human review |

### 13.2 Verification for Changes

| Change Type | Required Check |
|-------------|---------------|
| Any adopted-file / manifest change | `uv run python scripts/check_boundary.py` (Mode V) must PASS; Mode U for an upstream sync |
| New skill/agent | Rules E (no name collision) + F (manifested) must PASS |
| Tier profile change | re-run a chapter through `tier-coordinator` (Check C monotonicity) |
| Script change | `test_check_boundary.py` (the framework's own test) |

---

## 14. Known Limitations & Technical Debt

### 14.1 Current Limitations

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| Mode V ≠ two-field forgery proof | a self-consistent double-hash edit passes Mode V | Mode U in CI + branch protection + human review of any `upstream_sha256` diff |
| T4 not independently authored | T4 is a conservative interpolation, not a bespoke band | acceptable by design; escalate to a stored profile only if a work needs it |
| Copyright at T5 | cannot reproduce protected source verbatim | T5 emits a *preservation record* pointing to the in-repo source + supplementary scaffolding |

### 14.2 Technical Debt

| Item | Severity | Description | Evidence |
|------|----------|-------------|----------|
| **CLAUDE.md provenance counts stale** `[CODE-CONTRADICTED]` | Medium | `laf-adaptation/CLAUDE.md` §1 states **"15 agent files"** and **"16 skill dirs"**, but the live tree has **16 agents** and **18 skills** (the `prep-cordinator` agent and prep-era skills were added after that text). This is **doc-vs-doc drift**, NOT an unwired-capability defect (C8 does not apply — no ADR/spec declares a capability that is missing from code). | `CLAUDE.md:31,33,178,179` vs `ls agents/` (16) / `ls -d skills/*/` (18), verified 2026-07-08 |
| `prep-cordinator` spelling | Low | The agent file/name is `prep-cordinator` (one "o"), an intentional-looking historical spelling carried consistently | `agents/prep-cordinator.md` |

### 14.3 Future Considerations

| Item | Deferred Because | Revisit When |
|------|-----------------|-------------|
| Mode U in CI | OQ-4 — deferred; Mode V + hook is the current CI gate | an upstream-sync cadence is established |
| Byte-level hashing | current contract is LF-normalized text (correct for a prompt+YAML framework) | a deliberate manifest-wide re-vendor is undertaken |

---

## 15. Verification & Accuracy

### 15.1 Verification Log

| Date | Verified By | Code Version | Sections Verified | Issues Found |
|------|------------|--------------|-------------------|-------------|
| 2026-07-08 | tech-reference skill (direct build) | `feature/laf-0.1-artifacts-and-docs` | All (1–16); §5 subsystems + §14 debt code-verified against source | CLAUDE.md count drift (recorded §14) |

### 15.2 Spot-Check Protocol

1. **File existence:** every path in this doc resolves (`ls laf-adaptation/agents/` = 16, `ls -d laf-adaptation/skills/*/` = 18, `wc -l scripts/check_boundary.py` = 737).
2. **Agent contract:** spot-check 3–5 agent frontmatters (`grep '^model:' agents/<name>.md`) against the §5.1 table.
3. **Tier thresholds:** compare §5.3 table against `kb/tiers/tier_<N>.yaml`.
4. **Boundary rules:** `uv run python scripts/check_boundary.py` PASS; the printed NOTE names Rules B/C skipped in Mode V.
5. **Convention check:** confirm no adopted agent body carries NATIVE domain prose (the boundary is intact).

---

## 16. Glossary

| Term | Definition |
|------|------------|
| **Tier** | One of five developmental bands (1/2/3/5 stored, 4 interpolated) parameterizing every transform |
| **`active_tier`** | Explicit tier parameter (for `safety-verifier`/`chronicler`); `analyst` is tier-invariant (takes none) |
| **ADOPTED / ADOPTED-PATCHED / NATIVE / BUILD-NEW** | The four provenance classes; ADOPTED-PATCHED is exactly `agents/writer.md` |
| **Graft G1 / G2 / G3** | G1 = per-tier divergent canon layer; G2 = sequential fan-out fallback; G3 = the review quartet |
| **Agency Externalization** | Signature rule: badness is a STATE/accident, not innate — mandatory T1-2, optional T3, forbidden T4-5 |
| **Meaning / Meaning-DIFF** | The work's allegory/theme to neither add nor strip (R10); a divergence is a Check-D `conflicts:` entry |
| **Compound scene** | A scene where ≥2 HIGH-severity transformation flags co-occur; gets per-tier reconciliation via the `/prep` §2.1 compound-scene protocol (a source-side spec, not a section of this doc) |
| **Mode V / Mode U** | Boundary-check verify mode (single-field forgery gate) vs upstream-diff mode (absolute guarantee) |
| **`rewrite_phase_reads`** | The hardcoded 3-file read-set the rewrite phase consumes from the prep package |
| **Dual-form promotion** | Greenlight writes two mapping copies: 6-key kb (keeps `meaning:`) + 5-key root (strips it) |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-08 | tech-reference skill (direct build) | Initial reference, code-verified against `laf-adaptation/` @ `feature/laf-0.1-artifacts-and-docs` |
