# Proposal A — Architect voice ("minimal-additive, reuse the spine")

> Persona: architect. Lens: boundary-contract-safe, minimal-additive, maximal reuse of the existing
> NATIVE spine. Token-budget-conscious. This proposal resolves every Open Tension (T1–T8) toward the
> **least-new-surface-area** answer that still satisfies the user story.

## A.1 Headline shape

The prep phase is **a new NATIVE command + a new NATIVE prep-orchestrator agent + a small set of NATIVE
skills/additive frontmatter**, grafted onto the **0.1 layer only**. Root v1.0 gets a one-paragraph stub
pointing at 0.1 (T1, T7). The orchestrator reuses `web-researcher`, `analyst`, `kb-management`, and
`tier-coordinator` unchanged except for additive `skills:` lines where a new capability must attach to an
ADOPTED agent (only `writer` is patchable; the rest attach to NATIVE/BUILD-NEW bodies).

**One sentence:** *The prep phase is a new `prep` command that drives a new NATIVE `prep-cordinator`
agent (sibling to `muse`, but for onboarding) through research → roadmap → question-gate → package →
greenlight → handoff, reusing the existing spine and emitting a fixed-path package the rewrite phase
reads by hardcoded name.*

## A.2 The thin entry point (T1, T8)

- **Entry command:** `/laf:prep "<novel title>"` (a NATIVE command in `laf-adaptation/commands/`, or a
  Claude-Code slash command). The user types only the title. The command's body is one line:
  *"Hand control to the `prep-cordinator` agent with `work=<slug>`. Do not ask the user anything until the
  agent emits its `## Questions for the user` block."*
- **Why a command, not a prompt:** constraint #6 — the user never puts instructions in the paste. The
  command IS the only thing the user types in the prep session.
- **Root stub:** `docs/guides/ADDING_NEW_WORKS.md` gets a pointer: "To produce a work mapping
  automatically, use the 0.1 `/laf:prep` command." Root v1.0 itself gains NO new machinery (T7: out of
  scope).

## A.3 The standardized path contract (T5) — the core deliverable

Every run of `/laf:prep "<title>"` emits, at **fixed paths** (the next phase hardcodes these verbatim):

```
work/prep/<work-slug>/
  00-work-context.md          # high-level research: author, era, genre, reception, source-access declaration
  10-challenges.yaml          # typed challenge taxonomy (CSM-shaped) + governing rule per challenge
  20-analysis-work-level.yaml # WORK-level source-fidelity analysis (whole-novel), confidence-tagged
  30-mapping.yaml             # the derived <work>-mapping.yaml (the native input format)
  40-prep-brief.md            # the standardized package a human reads: decisions, cross-tier spine summary,
                              #   open questions answered, greenlight status
  50-greenlight.md            # the greenlight checklist + the user's confirmations
  60-handoff-prompt.md        # the EXACT one-time paste-able prompt for the rewrite phase
```

**Why this layout:** mirrors spec-kit's fixed-path handoff (enrichment §3). The next phase's command
reads `30-mapping.yaml` + `40-prep-brief.md` by hardcoded path — no argument, no re-interpretation. The
`work/prep/` prefix places it in the in-flight `work/` tree (constraint #5); promotion to `kb/` happens
only after greenlight via `kb-management` (the `30-mapping.yaml` is copied to
`config/concept_mapping/templates/<work>_mapping.yaml` (root) and `kb/adaptation-mapping/` (0.1) on
greenlight — that is the "promotion" event).

## A.4 The prep-orchestrator agent (T2, T3)

**New NATIVE agent: `prep-cordinator.md`** (sibling to `muse`, but for the prep phase). It is the only
new agent.

```
name: prep-cordinator
description: Owns the adaptation-prep phase. From a novel title, drives research → work-level analysis →
  challenge classification → mapping authoring → question gate → package → greenlight → handoff. Runs
  BEFORE the per-chapter muse; reuses web-researcher, analyst, kb-management, tier-coordinator.
model: opus
skills:
  - laf-adaptation:source-fidelity       # anti-hallucination discipline on work-level analysis
  - laf-adaptation:adaptation-tiers      # tier vocabulary for challenge→rule routing
  - laf-adaptation:adaptation-rules      # governing rules
  - laf-adaptation:kb-management         # promotion of the package on greenlight
  - laf-adaptation:prep-protocol         # NEW NATIVE skill — the phase procedure (see A.5)
  - laf-adaptation:work-mapping          # NEW NATIVE skill — derive <work>-mapping.yaml (see A.7)
  - laf-adaptation:challenge-taxonomy    # NEW NATIVE skill — typed challenge→rule routing (see A.6)
tools: Agent(web-researcher, analyst, tier-coordinator), Read, Write, Glob, Grep, WebSearch, WebFetch
```

**The phase procedure (lives in the `prep-protocol` skill, not the agent body — keeps the agent thin and
the procedure reusable/editable):**

```
STAGE 1 RESEARCH       dispatch web-researcher → 00-work-context.md (source-access declared; if the
                       novel text is not available, declare MEMORY-BASED per source-fidelity Phase 0 and
                       tag every downstream fact accordingly — NO ABORT at work level, unlike chapter
                       level, because research CAN proceed from secondary sources, but every derived
                       mapping decision inherits the work-level confidence ceiling)
STAGE 2 ROADMAP        read 00-work-context + 10-challenges (built in stage 3, but the roadmap references
                       the challenge taxonomy skeleton) → emit the prep task list inline; EXECUTE it
                       (stages 3-4) autonomously, no user interaction yet
STAGE 3 ANALYZE+CLASSIFY
                       dispatch analyst at WORK level → 20-analysis-work-level.yaml (confidence-tagged);
                       run challenge-taxonomy skill → 10-challenges.yaml (each challenge → governing rule
                       → per-tier strategy; flag compound scenes where ≥2 high-severity categories
                       co-occur)
STAGE 4 AUTHOR MAPPING run work-mapping skill → derive 30-mapping.yaml from 20-analysis + 10-challenges
STAGE 5 QUESTION GATE  emit ## Questions for the user block (only questions whose answers change the
                       work: allegory stance, tier emphasis, omissions to honor, target audience nuance).
                       HALT. Resume on user reply. Allow [skip] per spec-kit clarify semantics.
STAGE 6 PACKAGE        write 40-prep-brief.md (the readable synthesis) + update 10/20/30 with answers
STAGE 7 GREENLIGHT     write 50-greenlight.md; emit confirmation request; HALT until user confirms
STAGE 8 HANDOFF        write 60-handoff-prompt.md — the exact paste-able command for the rewrite phase
                       (see A.9); promote 30-mapping.yaml to kb/ + root templates/ via kb-management
```

The "question gate" (T3) is a **prompt-emitted block + a halt**, exactly the LangGraph-interrupt semantics
realized without a runtime (enrichment §2). No code.

## A.5 New NATIVE skill: `prep-protocol`

A NATIVE skill (`laf-adaptation/skills/prep-protocol/SKILL.md`) encoding the 8-stage procedure above, the
fixed-path contract (A.3), and the anti-hallucination rules for work-level analysis (work-level research
may be MEMORY-BASED without aborting, but the derived mapping's confidence ceiling propagates). Attached
to `prep-cordinator` via frontmatter. **Boundary-safe:** it is a new NATIVE skill, not an adopted-body
edit.

## A.6 Closing gap #2 — compound-scene protocol (T6)

**New NATIVE resource + analyst additive frontmatter.** The compound-scene protocol ships as
`adaptation-rules/resources/compound-scenes.md` (a NATIVE file inside an adopted skill's resources tree —
permitted by CLAUDE.md §1 "New files inside an ADOPTED skill's resources/ tree are NATIVE additions," but
the cleaner move is a new NATIVE skill — see proposal C for the disagreement). The `analyst` (NATIVE
body, editable) gets a flag in its output schema: when `transformation_flags` show ≥2 high-severity
categories co-occurring, set `compound_scene: true` and emit a `reconciliation_method`. The writer loads
the compound-scene resource via `adaptation-rules` (already in writer's additive frontmatter). This is a
**NATIVE-body edit to `analyst`** (allowed — analyst is NATIVE) + a **NATIVE resource**.

## A.7 Closing gap #3 — native work-mapping authoring (T6)

**New NATIVE skill `work-mapping`**: derives `30-mapping.yaml` from `20-analysis-work-level.yaml` +
`10-challenges.yaml`. Schema reuses the existing `<work>_mapping.yaml` form (`work_metadata`,
`key_challenges`, character archetype maps, concept translations, master translation table — exactly what
`ADDING_NEW_WORKS.md` documents and `narnia_mapping.yaml` instantiates). **Quality scoring:** the skill
asserts every mapping entry traces to a confidence-tagged analysis fact; entries derived from
MEMORY-BASED/UNCERTAIN facts are flagged `confidence: UNCERTAIN` in the mapping itself, so the rewrite
phase inherits the discipline. This closes the "form is native, content is not, nothing scores quality"
finding (Q1 row 3).

## A.8 Closing gap #1 — thematic/meaning-preservation (Check D)

**Extend `tier-coordinator` (BUILD-NEW body, editable) with Check D** + extend the analyst output schema
with a `theme`/`meaning` field per scene.

- `analyst` (NATIVE) emits `meaning: {value, confidence}` per chapter/scene (the substitution logic, e.g.
  "love that outlasts the worst thing").
- `tier-coordinator.reconcile()` gains **Check D (meaning-preservation)**: every tier's rendering
  preserves the `meaning` while the surface transforms; status Meaning-PRESERVED | Meaning-DIFF. Grounded
  in Hutcheon/Bortolotti "meaning preserved under surface transformation, environment = target tier"
  (enrichment §5).
- Attached via a **new NATIVE skill `thematic-fidelity`** wired into `analyst`, `tier-coordinator`,
  `writer` frontmatter (writer is ADOPTED-PATCHED — this is a SECOND additive line; the boundary contract
  permits multiple additive frontmatter lines, the constraint is body-byte-identity, not line-count — but
  see the debate, because proposal C argues one patch line per adopted agent is cleaner).

## A.9 Closing gap #4 — exemplar library + the contamination fix (T4)

**New NATIVE kb layer: `laf-adaptation/adaptation-rules/resources/exemplars/<challenge-type>.md`** — a
small set of challenge-typed, **verified** exemplars (sacrifice-and-return, betrayal-and-redemption,
petrification/body-horror). Each exemplar is structurally marked `<!-- @kind method-illustration;
source-fidelity: DERIVED; do-not-treat-as-source-truth -->`. The writer loads the matching exemplar when
`analyst` flags that challenge type. **This is the contamination fix:** exemplars live OUTSIDE the
source-truth path (`work/`, `kb/canon/`) and carry an explicit DERIVED marker, so a downstream agent
cannot present them as verified source (closes Q2 risk). Distinct from the CSM "didn't-rate vs zero"
distinction: here it's "verified-source vs method-illustration."

## A.10 The handoff prompt (T8)

`60-handoff-prompt.md` contains the literal text the user pastes in a NEW session:

```
/laf:rewrite --work <work-slug>
```

And the `rewrite` command's body is: *"Read `work/prep/<work-slug>/30-mapping.yaml`,
`40-prep-brief.md`, `10-challenges.yaml`. Hand control to `muse` for chapter 1. Do not ask the user to
restate anything — the prep package is the only context you need."* This is the spec-kit handoff pattern
verbatim (enrichment §3): the next phase reads fixed paths by hardcoded name.

## A.11 Change-list classification (boundary-checked)

| Change | Class | Boundary-safe? |
|---|---|---|
| `/laf:prep` command | NATIVE (new command) | ✅ new file |
| `prep-cordinator` agent | NATIVE (new agent) | ✅ new file, no upstream collision |
| `prep-protocol` skill | NATIVE (new skill) | ✅ |
| `work-mapping` skill | NATIVE | ✅ |
| `challenge-taxonomy` skill | NATIVE | ✅ |
| `thematic-fidelity` skill | NATIVE | ✅ |
| `compound-scenes.md` resource | NATIVE file in adopted `adaptation-rules/resources/` | ⚠️ permitted but muddies sync boundary (debate) |
| `exemplars/<type>.md` | NATIVE kb layer | ✅ |
| `analyst` body edit (compound flag, meaning field) | NATIVE-body edit | ✅ analyst is NATIVE |
| `tier-coordinator` Check D | BUILD-NEW-body edit | ✅ tc is BUILD-NEW |
| `writer` 2nd additive `skills:` line (`thematic-fidelity`) | ADOPTED-PATCHED additive | ⚠️ debatable — see C |
| `ADDING_NEW_WORKS.md` pointer | NATIVE doc edit | ✅ |
| root v1.0 new machinery | NONE (out of scope, T7) | ✅ |

## A.12 Positions on T1–T8 (compact)

- **T1:** 0.1 owns it; root gets a pointer stub only.
- **T2:** a dedicated work-level pass run by `prep-cordinator` dispatching `analyst` at work granularity.
- **T3:** `prep-cordinator` is a NATIVE agent; the gate is a prompt-emitted block + halt + greenlight rule.
- **T4:** separate `exemplars/` kb layer with DERIVED markers, outside `work/`+`kb/canon/`.
- **T5:** the `work/prep/<work-slug>/{00..60}` fixed-path contract (A.3).
- **T6:** `work-mapping` + `challenge-taxonomy` skills derive + score the mapping; compound-scenes
  resource + analyst flag.
- **T7:** root parity OUT OF SCOPE (ADR-006 deliberate).
- **T8:** `/laf:rewrite --work <slug>` hardcoded-path handoff.

## A.13 Open questions this proposal leaves

1. Is a SECOND additive `skills:` line on `writer.md` (for `thematic-fidelity`) acceptable, or must
   meaning-preservation attach only to NATIVE/BUILD-NEW agents? (Debate with C.)
2. Does work-level MEMORY-BASED analysis (no novel text in hand) produce a useful mapping, or should the
   prep phase require the user to supply the source text? (A says: allow MEMORY-BASED, propagate the
   ceiling.)
3. Should `prep-cordinator` be `opus` (cost) or `sonnet`? (A: opus, matching muse/tier-coordinator.)
