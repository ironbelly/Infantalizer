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

## Problem statement

The Literary Adaptation Framework (LAF) can adapt a chapter once it has been handed a per-work mapping
and a target tier. It has **no native "preparation" phase**: today a human (or an ad-hoc doc set) has to
research the novel, decide the per-work adaptation strategy, author the mapping, and organize the
guidance *before* the adaptation pipeline can produce good output.

A recent experiment produced that preparatory package **by hand** for *The Lion, the Witch and the
Wardrobe* (a `narnia_mapping.yaml` plus prose guides). An evaluation
(`10-findings-and-evaluation.md`) found that most of that hand-authored package **either duplicates
capability the native pipeline already has, or fills a small number of genuine gaps** — and, worse,
carries an anti-hallucination contamination risk when fed to an agent as if it were source truth.

The objective is to make the framework produce that preparatory package **natively and better**, from a
thin entry point, with no bespoke document set brought to the table.

## What to brainstorm

Every framework change required to deliver the user story in `20-objective-user-story.md`, grounded in
the current two-layer framework mapped in `30-current-framework-map.md` and the evaluation in
`10-findings-and-evaluation.md`. Cover at minimum:

- The **thin entry point** (how a user names a novel and starts the prep phase with no instructions).
- The **autonomous research + context-gathering** stage (high-level context, adaptation challenges).
- The **prep roadmap/task build-and-execute** stage.
- The **clarifying-question gate** (ask the user only what changes the work, after gathering).
- The **standardized initial document/guide package** the framework emits (fixed names/paths).
- The **greenlight + next-phase-prompt emission** (the command the user pastes to start rewriting).
- The **quality gaps** the evaluation identified (thematic/meaning-preservation invariant,
  compound-scene protocol, native work-mapping authoring, retrievable exemplar library, root-layer
  parity).

## Hard constraints (carry into every proposal)

1. **Boundary contract (0.1 layer):** native knowledge enters ADOPTED agents ONLY via `skills:`
   frontmatter — never by editing an adopted body. New capability = NATIVE skill or edits to the
   BUILD-NEW bodies (`chronicler`, `tier-coordinator`) or new NATIVE agents/commands. Enforced by
   `laf-adaptation/scripts/check_boundary.py`.
2. **Not software (ADR-006):** prompt + YAML + skills/agents only. No new runtime/CLI/scripts beyond the
   single existing boundary checker.
3. **Anti-hallucination discipline (constraint #2):** any generated prep artifact must preserve the
   CERTAIN/PROBABLE/UNCERTAIN source-fidelity protocol; illustrative/derived content must never be
   presentable to a downstream agent as verified source truth.
4. **Standardized reference-doc contract:** the prep package the framework emits must live at **fixed,
   hardcodable names and paths**, so the next phase's command/skill can reference them without
   arguments.
5. **Thin, zero-instruction entry:** the user supplies only the novel; all behavior lives in the
   command/skill/reference docs.

## Success criteria for the design spec (handoff = design)

- A named entry command/skill and the standardized prep-package path contract.
- A concrete agent/skill/kb change list, each item classified ADOPTED-safe / NATIVE / BUILD-NEW and
  checked against the boundary contract.
- The prep-phase pipeline (research → roadmap → execute → question-gate → package → greenlight).
- How each evaluation gap is closed natively.
- Explicit out-of-scope + open questions for the user.
