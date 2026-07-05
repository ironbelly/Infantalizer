---
topic: "Design the native LAF adaptation-prep phase: a thin entry point where a user names a novel and the framework autonomously researches it, builds and executes a prep roadmap, gathers context, asks a focused round of clarifying questions, produces a standardized initial document-and-guide package, confirms greenlight, and emits the next-phase kickoff prompt. Brainstorm every framework change needed to produce this natively."
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: design
created: 2026-07-04
standardized_inputs:
  - docs/native-prep/00-seed-brief.md
  - docs/native-prep/10-findings-and-evaluation.md
  - docs/native-prep/20-objective-user-story.md
  - docs/native-prep/30-current-framework-map.md
---

# Seed Brief: Native LAF Adaptation-Prep Phase

> This brief is the synthesis of the four standardized inputs in `docs/native-prep/`. The dialogue phase
> was pre-resolved by those inputs: the user story, the gap evaluation, and the grounded framework map
> together fix the problem, the constraints, and the success criteria. This document restates them as a
> debatable design seed and adds the open design tensions that the three proposals must take a position on.

## Problem Statement

The Literary Adaptation Framework (LAF) can adapt a chapter once handed a per-work mapping and a target
tier. It has **no native preparation phase**: today a human must research the novel, decide the per-work
adaptation strategy, author the mapping, and organize guidance *before* the pipeline can run.

A hand-authored LWW prep package (`narnia_mapping.yaml` + three prose guides) was evaluated
(`10-findings-and-evaluation.md`). Findings: ~80% of the prose duplicates capability the 0.1 native
pipeline already has dynamically (cross-tier reconciliation via `tier-coordinator`, safety via
`safety-verifier`, factual fidelity via `source-fidelity`/`analyst`). Two things are NOT redundant:
(a) the **consistency/quality of per-work decisions** (native leaves these to unassisted agent
reasoning — high variance), and (b) **meaning/thematic preservation** (a true gap in both layers).

Worse, feeding the hand-authored prose to an agent as if it were source truth carries an
**anti-hallucination contamination risk**: the renderings are labelled "illustrative" but an in-context
agent can treat invented phrasings as verified source, breaking `source-fidelity`'s
CERTAIN/PROBABLE/UNCERTAIN discipline.

**Objective:** make the framework produce that preparatory package **natively and better**, from a thin
entry point, with no bespoke document set brought to the table.

## The end-state user story (verbatim intent, from 20-objective-user-story.md)

1. **Thin entry.** User names the novel — nothing else. Framework begins researching high-level context +
   adaptation challenges.
2. **Autonomous prep.** Builds and executes the prep roadmap/tasks, gathering maximum context BEFORE asking
   the user anything.
3. **Focused question gate.** Only after gathering, asks the user only questions whose answers change the
   work.
4. **Standardized package.** Produces a set of initial documents + guides — more nuanced and better
   organized than the hand-authored set — at fixed names/paths.
5. **Greenlight.** Asks final confirmations.
6. **Handoff prompt.** Emits the exact one-time prompt for the next session (rewrite phase 1).

Structural constraints: the kickoff prompt is just a custom command (no instructions in the prompt); the
prep phase's *outputs* become the next phase's hardcoded *inputs* (same name, same path, every run).

## Implied phase pipeline (to be designed, not assumed)

```
[thin entry: user names a novel]
   → RESEARCH     high-level context + adaptation-challenge discovery (source-fidelity gated)
   → ROADMAP      build the prep task list, then execute (gather maximum context)
   → QUESTION GATE  ask the user only what changes the work — after gathering, not before
   → PACKAGE      emit standardized initial documents + guides (fixed names/paths)
   → GREENLIGHT   final confirmations
   → HANDOFF      emit the exact one-time prompt for the next session (rewrite phase 1)
```

## Known Context (grounded facts)

### Two-layer framework
- **Layer A — Root v1.0** (`config/`, `prompts/`, `templates/`, `docs/`): prompt + YAML, no code. Pipeline:
  `chapter_analysis.md → tier_{1,3}_transform.md → safety_check.md`. Ships ONLY T1+T3 (ADR-006). No
  orchestration, no cross-tier tool, no meaning concept, no research/prep phase.
- **Layer B — LAF 0.1 CWS Hybrid** (`laf-adaptation/`): agents + skills. Vendors CWS machinery, grafts LAF
  domain spine under a hard boundary contract. 15 agents (11 adopted-provenance incl. `writer`
  ADOPTED-PATCHED; 2 NATIVE `analyst`/`safety-verifier`; 2 BUILD-NEW `chronicler`/`tier-coordinator`),
  16 skills (12 ADOPTED; 3 NATIVE `adaptation-tiers`/`adaptation-rules`/`source-fidelity`; 1 BUILD-NEW
  `adaptation-safety`).

### Provenance classes + the load-bearing boundary contract
- ADOPTED-CLEAN: vendored byte-identical (after prefix rewrite) — **never edit body**.
- ADOPTED-PATCHED: only `writer.md` — adopted body + one additive `skills:` line.
- NATIVE: LAF domain spine (`analyst`, `safety-verifier`, `adaptation-tiers`, `adaptation-rules`,
  `source-fidelity`).
- BUILD-NEW: greenfield in both systems (`chronicler`, `tier-coordinator`, `adaptation-safety`).
- **New capability MUST be: a NATIVE skill, additive `skills:` frontmatter, a new NATIVE agent/command, or
  an edit to a BUILD-NEW body. Never an adopted-body edit.** Enforced by `check_boundary.py` (Rules A–F).

### Existing reusable spine (the prep phase should reuse, not reinvent)
- `analyst` (NATIVE, tier-invariant) + `/source-fidelity`: 5-phase anti-hallucination protocol, Phase-0
  ABORT-on-NO-ACCESS, emits `work/analysis/ch-NN.yaml` with confidence tags. **Reuse for work-level
  analysis.**
- `web-researcher` (ADOPTED) + `/creative-research`: web research specialist. **Reuse for autonomous
  research stage** (it is a specialist today, not an onboarding stage).
- `tier-coordinator` (BUILD-NEW): fans a chapter across {1,2,3,5}, runs Check A (source-fidelity
  consistency), Check B (disclosure-leak), Check C (framing monotonicity). **The place to add Check D
  (meaning-preservation).**
- `kb-management` (ADOPTED): lifecycle for promoting in-flight `work/` → canon `kb/`. **Reuse for package
  storage.**
- `ADDING_NEW_WORKS.md`: documents the HUMAN process for authoring `<work>-mapping.yaml`. **This is the
  process to mechanize.**
- `config/concept_mapping/templates/<work>_mapping.yaml` (root) + `kb/adaptation-mapping/` (0.1): native
  input format — legitimate target for the prep package's mapping output.

## Hard Constraints (carry into every proposal)

1. **Boundary contract (0.1 layer):** native knowledge enters ADOPTED agents ONLY via `skills:` frontmatter
   — never by editing an adopted body. New capability = NATIVE skill / additive frontmatter / edit to
   BUILD-NEW bodies / new NATIVE agent or command. Enforced by `check_boundary.py`.
2. **Not software (ADR-006):** prompt + YAML + skills/agents only. No new runtime/CLI/scripts beyond the
   single existing boundary checker.
3. **Anti-hallucination discipline:** any generated prep artifact must preserve the CERTAIN/PROBABLE/UNCERTAIN
   source-fidelity protocol; illustrative/derived content must NEVER be presentable to a downstream agent as
   verified source truth.
4. **Standardized reference-doc contract:** the prep package the framework emits MUST live at fixed,
   hardcodable names/paths so the next phase's command/skill can reference them without arguments.
5. **Thin, zero-instruction entry:** the user supplies only the novel; all behavior lives in
   command/skill/reference docs.
6. **The kickoff prompt is a custom command**, not a prompt with instructions baked into the user's paste.
   The prep phase's outputs (fixed paths) become the next phase's hardcoded inputs.

## Success Criteria for the design spec (handoff = design)

- A **named entry command/skill** and the **standardized prep-package path contract** (fixed file list).
- A **concrete agent/skill/kb change list**, each item classified ADOPTED-safe / NATIVE / BUILD-NEW and
  checked against the boundary contract.
- The **prep-phase pipeline** (research → roadmap → execute → question-gate → package → greenlight →
  handoff-prompt), naming which existing/new agent owns each stage.
- How each evaluation gap is closed natively: thematic/meaning-preservation invariant (Check D),
  compound-scene protocol, native work-mapping authoring, retrievable exemplar library, root-layer parity.
- A **greenlight + next-phase-prompt emission** mechanism (the exact paste-able command).
- Explicit **out-of-scope** + **open questions** for the user.

## Open Design Tensions (the three proposals must take a position)

These are the irreducible design choices. Each proposal resolves them differently; the adversarial debate
scores the resolutions.

- **T1 — Which layer owns the prep phase?** Root v1.0 (no orchestration, T1+T3 only) vs. 0.1 (full
  machinery, all tiers). Likely 0.1 is the only viable substrate, but the spec must say so explicitly and
  address whether root gets a thin entry stub.
- **T2 — Work-level vs. chapter-level analysis.** `analyst` runs per-chapter today. Prep needs a
  WORK-level research/analysis pass (whole-novel context, challenge taxonomy) BEFORE any chapter is
  analyzed. Is that a new work-analyst agent, a new skill attached to `analyst`, or a prep-orchestrator
  that calls `web-researcher` + `analyst`?
- **T3 — Prep orchestrator shape.** The user story implies a multi-stage autonomous flow
  (research→roadmap→execute→question-gate→package→greenlight→handoff). In a prompt+YAML+agents world, is
  the orchestrator a new NATIVE agent (analogous to `muse` for the rewrite phase), a new skill, or a
  command/skill that drives an existing agent? How is the "question gate" (interactive pause) expressed?
- **T4 — Where does derived/illustrative content live?** The contamination risk (Q2) demands that
  illustrative renderings / few-shot exemplars / cross-tier priors sit OUTSIDE the source-truth path with
  explicit method-illustration marking. What kb topology separates "verified source truth" from "method
  illustration" so a downstream agent cannot confuse them?
- **T5 — Standardized package path contract.** Exactly which fixed files/paths does the prep phase emit?
  (mapping yaml, challenge taxonomy, work-context, greenlight doc, handoff prompt — names + locations.)
  These must be hardcodable into the next-phase command.
- **T6 — Mechanizing work-mapping authoring.** `ADDING_NEW_WORKS.md` is a human process. Native authoring
  means deriving `<work>-mapping.yaml` from confidence-tagged analysis + a challenge taxonomy, with
  challenges routing to governing rules. What schema/agent produces it, and how is its quality scored?
- **T7 — Root parity scope.** ADR-006 deliberately shipped only T1+T3. Does the prep phase need T5 (and a
  cross-tier tool) in root to "match" the hand-authored set? Or is root parity explicitly out of scope?
- **T8 — Reusability of the prep package as next-phase input.** The handoff must produce a paste-able
  command that hardcodes the package paths. What is the command's name, and which skill does it load?

## Non-Goals

- Not building a runtime/CLI (ADR-006 — prompt + YAML + skills/agents only).
- Not editing any ADOPTED (vendored) agent body (boundary contract).
- Not producing the actual rewritten novel in this phase — only the preparation package + handoff prompt.
