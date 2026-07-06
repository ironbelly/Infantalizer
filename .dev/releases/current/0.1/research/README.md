# Research Directory — v0.1 Spec / CWS Integration Brainstorm Input

> **Purpose:** empower a separate brainstorming agent to decide whether to (A) fork `creative-writing-skills` and graft LAF's domain theory into it, or (B) write a 0.1 spec that incorporates CWS strategies natively.

## Reports (read both, in order)

| # | File | Subject | Posture |
|---|------|---------|---------|
| 1 | `INFANTALIZER_ANALYSIS.md` | The Infantalizer / LAF project + v0.1 SPEC | Domain theory + thin artifact. Configs + prompts, no agents, no state. |
| 2 | `CREATIVE_WRITING_SKILLS_ANALYSIS.md` | The vendored CWS package | Operational machinery + no adaptation theory. 11 agents, 16 skills, durable kb. |

Both reports use the **same 12-category structure** so you can cross-reference cell-by-cell. The category map is at the bottom of each report (§12 in Report 1, §14 in Report 2).

## The decision in one table

The two systems are *complementary*:

| LAF has | CWS has |
|---------|---------|
| Developmental-psychology tier theory | Multi-agent orchestration (muse + 10 specialists) |
| Transformation rules engine (thematic, character) | Durable kb (canon, characters, timeline, world, styles, vocab, issues) |
| v2.0 source-fidelity protocol (CERTAIN/PROBABLE/UNCERTAIN) | Draft→critique→revise loop (writer, critic, editor, reader-sim) |
| 6-section safety_check for Tier 1–2 | Voice consistency via style-creator + style files |
| Agency Externalization signature rule | Intentional language discipline (llm-writing) |
| Concept mapping (universal + work-specific) | Continuity-checker agent + chronicler for canon extraction |
| **Nothing operational** | **No adaptation domain theory** |

## Where to look in each report

- **The bridge section** — Report 1 §11, Report 2 §11. Each frames the fork-vs-spec decision from its own posture.
- **The integration map** — Report 2 §13. Maps every LAF weakness to the CWS primitive that fills it, and every CWS gap to the LAF primitive that fills it. This is the single highest-signal artifact for brainstorming.
- **The failure-mode table** — Report 2 §12. LLM-fiction failure modes that CWS is engineered to counter. Any brainstorming output must preserve these countermeasures.
- **The category cross-reference** — Report 1 §12 + Report 2 §14. Cell-by-cell comparison across 12 categories.
- **Open questions** — Report 1 §8.3, Report 2 §8.3. The unresolved design questions the brainstorming agent must answer.

## Critical constraints to preserve

Whatever the brainstorming agent decides, these must survive:

1. **LAF's tier axis** — the single-parameter design is its core innovation. Don't dissolve it into CWS's multi-axis model.
2. **LAF's uncertainty discipline** — CERTAIN/PROBABLE/UNCERTAIN tagging is non-negotiable for source adaptation.
3. **LAF's safety_check** — required for any tier producing children's content.
4. **CWS's critic/editor/reader-sim/continuity quartet** — these four review modes are genuinely distinct and must not collapse into one.
5. **CWS's work/ vs kb/ split** — provisional vs durable knowledge discipline prevents brainstorms from hardening into canon.
6. **CWS's skill-vs-agent distinction** — passive knowledge (skills) vs active stances (agents) is foundational.

## Verification notes for the brainstorming agent

- CWS's `chronicler` agent is referenced in README/architecture but its file presence in `cw/agents/` should be verified before depending on it (Report 2 §4.1.11 note).
- CWS ships **no children's/YA genre resources** in `resources/genre/` (Report 2 §4.2.2 note). This is LAF's opening.
- LAF's v1.0 shipped **4 of 5 tiers and 2 of 5 transform prompts** — Tier 4 is deferred as interpolation (Report 1 §8.1).
- The v0.1 SPEC (314 lines) is *more architecturally complete* than the v1.0 condensed SPEC (131 lines) — it describes subsystems v1.0 cut. Use v0.1 as the design-rationale reference, v1.0 as the shipped-state reference.
- CWS is Apache 2.0; LAF is MIT. Both permit fork + modification with attribution.

## Output expected from the brainstorming agent

A decision document covering:

1. **Path chosen** — (A) fork CWS, (B) native 0.1 spec, or (C) hybrid.
2. **Architecture** — what agents, skills, configs, kb structure, and workflow result.
3. **Integration map** — which LAF concepts land where in the chosen structure.
4. **Migration plan** — what carries over from each source system, what gets cut.
5. **Open questions resolved** — answers to Report 1 §8.3 + Report 2 §8.3.
6. **Critical constraints check** — confirmation that all 6 constraints above survive.
