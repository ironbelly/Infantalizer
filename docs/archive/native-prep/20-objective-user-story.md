# Objective & User Story: the native adaptation-prep phase

> Standalone context for a fresh session. This is the end-state the brainstorm must design toward.

## The user story (verbatim intent)

- **Thin entry point.** The user specifies the novel they want to rewrite — and nothing else. The
  framework begins researching the high-level context of the novel and what needs to be done in
  preparation for the rewrite.
- **Autonomous prep.** It builds and then executes the initial preparation roadmap and tasks, gathering
  as much information as possible **before** asking the user anything.
- **Focused question round.** Only after gathering does it ask the user a series of questions needed to
  clarify important points about the direction they want to take, or nuances they might have input on.
- **Standardized initial package.** Once done, the framework produces a set of initial documents and
  guides — at an even more nuanced and better-organized level than the hand-authored LWW set — and then
  asks the user any final questions or confirmations valuable to greenlight the first real phase of
  rewriting.
- **Greenlight -> next-phase prompt.** Once final questions are answered and confirmations received, the
  agent gives the user the prompt to paste in a new session to kick off the next phase.

## Structural constraints (how it must be built)

- **The kickoff prompt is nothing more than a custom command / one-time prompt.** The user never puts
  actual instructions in the prompt. All instructions are baked into the command, the skills, and the
  reference documents the next agent knows to reference.
- **Reference documents are standardized** — same name, same path, every run — so they can be hardcoded
  into the skill and pipeline of the next phase. The prep phase's *outputs* become the next phase's
  hardcoded *inputs*.

## Implied phase pipeline (to be designed, not assumed)

```
[thin entry: user names a novel]
        v
RESEARCH        high-level context + adaptation-challenge discovery (source-fidelity gated)
        v
ROADMAP         build the prep task list, then execute it (gather maximum context)
        v
QUESTION GATE   ask the user only what changes the work — after gathering, not before
        v
PACKAGE         emit the standardized initial documents + guides (fixed names/paths)
        v
GREENLIGHT      final confirmations
        v
HANDOFF         emit the exact one-time prompt for the next session (rewrite phase 1)
```

## What "better than the hand-authored set" means here

The hand-authored LWW package (evaluated in `10-findings-and-evaluation.md`) was static, partly
redundant with native capability, and carried a source-fidelity contamination risk. "Better" means the
native prep phase:

- derives per-work decisions from a **confidence-tagged** analysis rather than asserting them,
- keeps derived/illustrative content **out of the source-truth path**,
- is **standardized and regenerable** (same paths every run), and
- is **organized as a package** the next phase can consume by hardcoded path, not prose a human must
  re-read.

## Non-goals (keep the brainstorm honest)

- Not building a runtime/CLI (ADR-006 — prompt + YAML + skills/agents only).
- Not editing any ADOPTED (vendored) agent body (boundary contract).
- Not producing the actual rewritten novel in this phase — only the preparation package and the handoff
  prompt.
