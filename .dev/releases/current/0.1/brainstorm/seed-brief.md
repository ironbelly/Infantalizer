---
topic: "Decide whether to (A) fork creative-writing-skills and graft LAF's domain theory into it, (B) write a 0.1 spec that incorporates CWS strategies natively, or (C) hybrid — for the Infantalizer/LAF (Literary Adaptation Framework) project."
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: design
created: 2026-07-03T04:37:28Z
---

# Seed Brief: LAF × CWS Integration Decision (A / B / C)

## Problem Statement

The Infantalizer / Literary Adaptation Framework (LAF) is a **domain theory with a thin
artifact**: config-driven, age-tiered literary adaptation grounded in developmental
psychology (Piaget/Kohlberg), but shipping no agents, no orchestration, no cross-chapter
state, and no critique/revision loop. The vendored `creative-writing-skills` (CWS) package
is the **inverse posture**: rich operational machinery (11 shipped agents, 16 skills, durable
`kb/`, draft→critique→revise quartet, style extraction, intentional-language discipline) with
**no adaptation domain theory**. The two are complementary, not competing.

The decision: for LAF's 0.1 release, do we
- **(A)** fork CWS and graft LAF's domain theory into it as add-on skills/agents/kb, or
- **(B)** author a native 0.1 spec that re-implements CWS's proven strategies ground-up for adaptation, or
- **(C)** a hybrid that adopts CWS's proven primitives selectively while keeping a purpose-built adaptation spine?

## Known Context (established facts)

**From grounding research (Reports 1 & 2) + codebase verification 2026-07-03:**

- LAF ships: 4 age-profile configs (tier_1/2/3/5; tier_4 deferred as interpolation),
  2 transformation-rule files (thematic, character), 2 concept maps (universal + tolkien),
  4 prompts (chapter_analysis, tier_1_transform, tier_3_transform, safety_check), 1 work template.
- LAF's crown jewels: the **single tier axis**, the **v2.0 Pragmatic Verification Protocol**
  (CERTAIN/PROBABLE/UNCERTAIN source-fidelity tagging), the **6-section safety_check**,
  and the **Agency Externalization** signature rule.
- CWS ships (VERIFIED on disk, not just docs): agents = brainstormer, character-sim,
  continuity-checker, critic, editor, muse, outliner, reader-sim, style-creator,
  **web-researcher**, writer (11 total). Skills = 16. Slash commands = 4 (bs/write/critique/kb).
  kb/ = canon, characters, world, timeline, styles, vocab.md, issues.
- **CRITICAL CORRECTION to the reports:** `chronicler.md` does **NOT** exist in either
  `cw/agents/` or `agents/`. Canon-extraction is referenced in CWS docs but **unshipped**.
  The 11th agent is `web-researcher`, not `chronicler`. Any plan that "adopts chronicler as-is"
  is adopting vapor — canon-extraction must be BUILT regardless of path.
- CWS has **no `childrens.md`/`ya.md`** genre resources (VERIFIED). LAF's tier profiles fill this.
- Licenses: CWS Apache-2.0, LAF MIT — both permit fork+modify with attribution. No legal blocker.
- ADR 006 (LAF) explicitly cut Python/CLI scaffolding as "wrong abstraction — this is a prompt
  framework, not software." Adopting CWS's plugin architecture reopens that decision.

## Constraints (the 6 that MUST survive — non-negotiable)

1. **LAF tier axis** — single-parameter design is the core innovation; must not dissolve into
   CWS's multi-axis (persona/genre/taste) model.
2. **LAF uncertainty discipline** — CERTAIN/PROBABLE/UNCERTAIN tagging non-negotiable for source adaptation.
3. **LAF safety_check** — required for any tier producing children's content (Tier 1–2 mandatory).
4. **CWS critic/editor/reader-sim/continuity quartet** — four genuinely distinct review modes;
   must not collapse into one.
5. **CWS work/ vs kb/ split** — provisional vs durable knowledge discipline; prevents brainstorms
   hardening into canon.
6. **CWS skill-vs-agent distinction** — passive knowledge (skills) vs active stances (agents) is foundational.

## Success Criteria

The output decision document must deliver:
1. Path chosen (A / B / C) with explicit justification against the 6 constraints.
2. Resulting architecture: agents, skills, configs, kb structure, workflow.
3. Integration map: which LAF concept lands where in the chosen structure.
4. Migration plan: what carries over from each source, what gets cut, ordered by phase.
5. Resolved open questions: answers to Report 1 §8.3 (5 Qs) + Report 2 §8.3 (7 Qs).
6. Constraints check: confirmation all 6 survive, with the mechanism for each.

## Open Questions (to resolve in the merged output)

**Report 1 §8.3:**
- Q1.1 Continuity: how is cross-chapter canon tracked?
- Q1.2 Quality assurance: how is adaptation quality (not just safety) verified?
- Q1.3 Iteration: what is the revision loop on safety_check FAIL?
- Q1.4 Knowledge persistence: where does per-work / per-chapter state live?
- Q1.5 Multi-tier coordination: one source chapter → all 5 tiers coordinated, or 5 independent runs?

**Report 2 §8.3:**
- Q2.1 Where does LAF's tier system live in the chosen structure?
- Q2.2 How is the source-adaptation workflow modeled (analyst agent? pre-muse phase?)?
- Q2.3 Where do LAF's transformation rules live?
- Q2.4 How to integrate confidence tagging?
- Q2.5 Who runs safety_check (new agent? continuity mode? critic focus?)?
- Q2.6 Chapter-driven (LAF) or session-driven (CWS) workflow?
- Q2.7 Multi-tier output: parallel fan-out or sequential?

## Enrichment Context

Codebase enrichment (quality_tier: primary) verified the two decisive facts above:
**chronicler is unshipped** (canon-extraction is a build item on every path) and **no children's
genre resources exist** (LAF tiers are the unique fill). Both narrow the decision: pure Path A
"adopt machinery as-is" is partly illusory because a load-bearing CWS agent is missing.
