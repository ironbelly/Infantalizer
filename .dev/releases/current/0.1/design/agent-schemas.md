---
title: "Agent Frontmatter Schemas — LAF 0.1"
parent: DESIGN.md
status: draft
---

# Agent Frontmatter Schemas

Concrete, copy-paste-ready frontmatter for every agent in LAF 0.1. Two native agents and two build-new
agents are fully specified. The six adopted agents are vendored **unchanged**; only `writer` receives a
frontmatter-only patch (§3), and `reader-sim` receives a *data* extension (§4) with **no file edit**.

---

## 1. Frontmatter dialect contract (Claude-native / cw-lowered)

All LAF agents use the **Claude Code native** frontmatter dialect — the same one CWS emits into
`cw/agents/`. This is deliberate: Mars/Meridian is cut ([DESIGN.md §2.1](DESIGN.md)), so Mars-only keys
(`model-policies`, `sandbox`, `effort`, `subagents`, `approval`, `mode`) are **not** used. Claude Code
does not read them.

**Permitted keys** (closed set for LAF):

| Key | Type | Notes |
|---|---|---|
| `name` | string | Must equal the filename stem |
| `description` | string | One-line role statement (drives auto-delegation) |
| `model` | string | `opus` \| `sonnet` \| `haiku` \| `inherit` (Claude aliases only — never Mars aliases like `opus46`/`gpt`/`deepseek`) |
| `skills` | list | `laf-adaptation:<skill-name>` fully-qualified entries, one per line |
| `tools` | string | Comma-separated Claude tool names: `Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch` |

> **Adopted-agent rule:** adopted files are copied from CWS `cw/agents/` verbatim. Their `model:` values
> (`opus`/`sonnet`) and `skills:` package prefix are rewritten from `creative-writing-skills:` to
> `laf-adaptation:` **once, at vendor time**, and that rewritten form is what `VENDOR.md` hashes. After
> that, they are frozen (see [`boundary-contract.md`](boundary-contract.md)). The prefix rewrite is the
> *only* permitted transformation at vendor time; it is applied uniformly and recorded.

---

## 2. Native agents (fully specified)

### 2.1 `analyst` — source analysis + v2.0 verification protocol

**Role:** The native entry point of the adaptation pipeline. Runs **once per source chapter** (before
muse), producing confidence-tagged source truth. Enforces constraint #2 (uncertainty discipline) and the
Phase-0 ABORT gate.

**File:** `agents/analyst.md`

```yaml
---
name: analyst
description: Source-chapter analysis for literary adaptation. Runs before the muse as the pre-orchestration phase; produces confidence-tagged (CERTAIN/PROBABLE/UNCERTAIN) structural facts and transformation flags. ABORTS on NO-ACCESS.
model: opus
skills:
  - laf-adaptation:source-fidelity
  - laf-adaptation:adaptation-tiers
  - creative-writing-skills:story-memory   # rewritten to laf-adaptation:story-memory at vendor time
tools: Read, Write, Glob, Grep
---
```

**Inputs (passed by caller):** `source_path` (a `source/<work>/ch-<NN>.txt`), `work`, `chapter`.
`active_tier` is **not** an input — analysis is tier-invariant (Q1.5).

**Output contract:** writes `work/analysis/ch-<NN>.yaml` conforming to the v2.0 schema in
[`skill-specs.md §3.2`](skill-specs.md). Body procedure (5 phases: Source Declaration → Essential
Verification → Dual-Pass Documentation → Transformation Flags → Consistency Check) is specified in
[`skill-specs.md §3`](skill-specs.md); the agent body loads `/source-fidelity` and executes it.

**Hard behavior (in agent body, not a skill):**
```
Phase 0 — Source Declaration:
  Determine SOURCE ACCESS LEVEL ∈ {FULL, PARTIAL, MEMORY-BASED, NO-ACCESS}.
  IF NO-ACCESS:  emit `status: ABORTED` to work/analysis/ch-NN.yaml and HALT. Do not proceed.  ← constraint #2
  IF MEMORY-BASED: every emitted fact MUST carry confidence: UNCERTAIN.
```

### 2.2 `safety-verifier` — the fifth reviewer (6-section gate)

**Role:** A **distinct fifth review agent** (constraint #4 — never a critic focus, never a continuity
mode). Runs **after** `continuity-checker` (step 8). MANDATORY for Tier 1-2 output; emits a machine
verdict that gates promotion and triggers the revision loop on FAIL (constraint #3).

**File:** `agents/safety-verifier.md`

```yaml
---
name: safety-verifier
description: Post-generation safety gate for Tier 1-2 children's adaptations. Runs the 6-section safety rubric and emits a PASS/FAIL verdict. A FAIL blocks kb promotion and re-enters the writer revision loop. Read-only.
model: sonnet
skills:
  - laf-adaptation:adaptation-safety
  - laf-adaptation:adaptation-tiers
tools: Read, Write, Glob, Grep
---
```

**Inputs (passed by caller):** `draft_path` (a `work/drafts/ch-NN-t<N>-v<M>.md`), `active_tier`, `work`,
`chapter`.

**Tier gate (in agent body):**
```
IF active_tier ∈ {1, 2}:  run the full 6-section rubric — verdict is MANDATORY and blocking.
IF active_tier == 3:      run rubric in ADVISORY mode (report only; does not block).
IF active_tier ∈ {4, 5}:  SKIP — emit verdict: N/A (safety_check does not apply). ← ground-truth: safety_check.md is T1-2 only
```

**Output contract:** writes `work/safety-reports/ch-<NN>-t<N>.md` ending in a machine-parseable verdict
block (full contract in [`safety-rubric.md §4`](safety-rubric.md)):
```yaml
verdict:
  result: PASS | FAIL | N/A
  tier: <N>
  sections: { forbidden_content: PASS, agency_externalization: PASS, emotional_safety: PASS,
              safe_home: PASS, nightmare_prevention: PASS, linguistic: PASS }
  automatic_failures: []          # non-empty ⇒ result: FAIL regardless of sections
  next: promote | revise          # revise ⇒ caller returns to workflow step 3
```

`Write` tool is granted **only** to emit the report to `work/safety-reports/`; the agent never edits a
draft (it is a reviewer, not a writer).

---

## 3. Adopted `writer` — adaptation mode via frontmatter (the boundary contract in action)

`writer` is **adopted**. Its adaptation capability is added by appending **one** `skills:` entry —
`laf-adaptation:adaptation-rules`. **The body is not touched.** This is the canonical demonstration of
constraint #6: native knowledge enters an adopted agent only as a loadable skill.

**Ground-truth baseline** (CWS `cw/agents/writer.md`, verified 2026-07-03 — note the upstream file
already lists `creative-writing-craft` twice; that duplication is preserved verbatim, not "fixed", to
keep the file patch-clean):

```yaml
---
name: writer
description: Production prose from scene briefs, revision notes, and style references; uses progressive mode guidance for fresh drafts, revisions, bridges, alternate takes, and line polish.
model: opus
skills:
  - creative-writing-skills:creative-writing-modes
  - creative-writing-skills:creative-writing-craft
  - creative-writing-skills:creative-writing-craft
  - creative-writing-skills:writing-principles
  - creative-writing-skills:llm-writing
  - creative-writing-skills:story-memory
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

**LAF vendored form** — two mechanical transforms, both recorded in `VENDOR.md`:
1. **Prefix rewrite** (uniform vendor-time transform, applies to every adopted file):
   `creative-writing-skills:` → `laf-adaptation:`.
2. **Adaptation-mode graft** (the single additive line): append `laf-adaptation:adaptation-rules`.

```yaml
---
name: writer
description: Production prose from scene briefs, revision notes, and style references; uses progressive mode guidance for fresh drafts, revisions, bridges, alternate takes, and line polish.
model: opus
skills:
  - laf-adaptation:creative-writing-modes
  - laf-adaptation:creative-writing-craft
  - laf-adaptation:creative-writing-craft
  - laf-adaptation:writing-principles
  - laf-adaptation:llm-writing
  - laf-adaptation:story-memory
  - laf-adaptation:adaptation-rules        # ← the ONLY LAF-added line; body untouched
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

**Boundary-contract classification:** `writer.md` is `ADOPTED-PATCHED` in `VENDOR.md` — it stores *two*
hashes: `upstream_sha256` (the original cw file) and `laf_sha256` (the vendored-with-graft file).
`check_boundary.py` asserts the vendored file matches `laf_sha256` and that the diff from upstream is
**frontmatter-only and additive** (see [`boundary-contract.md §3.2`](boundary-contract.md)). Any body
byte-change fails the gate.

**How the mode activates (no body logic needed):** when `muse` dispatches `writer` on the adapt path, the
scene brief carries `active_tier` and instructs "adaptation mode." The presence of `/adaptation-rules`
in context (loaded via the frontmatter entry) supplies the transform rules; `writer`'s existing body
("Read the brief, critique notes … style files say how it should sound") already routes on the brief.
The tier-conditional `mode:` ladder lives in the skill, not the agent.

---

## 4. Adopted `reader-sim` — native persona as data (no file edit)

`reader-sim`'s body (verified: it is just `Use /reader-sim.`) already accepts a **caller-specified reader
persona** ("pass the persona, draft, and knowledge boundary"). LAF supplies the persona as structured
*data* in the dispatch call — the tier's `developmental_basis` — with **zero change** to the agent file
or the `reader-sim` skill.

**Persona payload** (constructed by `muse`/`tier-coordinator` from `kb/tiers/tier_N.yaml`):
```yaml
persona:
  label: "Tier 1 reader (ages 3-5)"
  developmental_basis:
    piaget_stage: preoperational
    kohlberg_stage: 1
  knowledge_boundary: "Has read tier-1 chapters 1..N-1 only (per kb/adaptations/<work>/tier-1/continuity.md)"
  felt_experience_focus: ["Is it scary? (must not be)", "Does the ending feel safe?", "Is anyone 'bad'? (should read as grumpy/silly)"]
```

`reader-sim.md` stays byte-identical to upstream (`ADOPTED-CLEAN` in `VENDOR.md`). The persona is a
runtime argument, not a code path.

---

## 5. Build-new agents (fully specified)

### 5.1 `chronicler` — tier-aware canon extraction (greenfield, graft G1)

**Role:** Populates durable canon **after a chapter settles and muse accepts** (step 11, constraint #5:
promotion only on accept). Unlike a generic canon extractor, it is **tier-partitioned**: the same
character can hold divergent canonical state per tier (Sauron is "Grumpy King" in tier-1 canon, "the Dark
Lord" in tier-5 canon). This closes the latent divergent-canon bug (graft G1).

**File:** `agents/chronicler.md`

```yaml
---
name: chronicler
description: Tier-aware canon extraction. After a chapter is accepted, promotes durable facts into shared kb/canon and per-tier kb/adaptations/<work>/tier-N/continuity.md. Keys all per-tier state by (work, tier, chapter).
model: sonnet
skills:
  - laf-adaptation:story-memory
  - laf-adaptation:kb-management
  - laf-adaptation:adaptation-tiers
tools: Read, Write, Glob, Grep
---
```

**Inputs:** `work`, `chapter`, `active_tier`, `adapted_path`
(`kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/adapted.md`), `analysis_path`
(`work/analysis/ch-<NN>.yaml`).

**Write targets (dual-layer, per [`kb-formats.md §4`](kb-formats.md)):**
```
SHARED (tier-invariant source truth):
  kb/canon/<work>/ch-<NN>.md        — hard source facts (append; tier-neutral)
  kb/timeline/<work>.md             — chronological source entries

PER-TIER (graft G1 — the divergent layer):
  kb/adaptations/<work>/tier-<N>/continuity.md                      — running "what a Tier-N reader now knows"
  kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/canon-delta.md    — what THIS chapter changed at THIS tier
  kb/adaptations/<work>/tier-<N>/decisions.md                       — adaptation decisions log (append)
```

**Invariant (in body):** every per-tier write is keyed `(work, tier, chapter)`. The chronicler MUST NOT
write a tier-N fact into another tier's `continuity.md`, and MUST NOT promote a tier-transformed name
(e.g. "Grumpy King") into shared `kb/canon/` — shared canon holds source truth; transformed names live
only in the per-tier layer.

### 5.2 `tier-coordinator` — cross-tier reconciliation (greenfield, graft G2)

**Role:** Fans the transform across tiers and reconciles their outputs against shared source-canon while
preserving tier-differentiated framing (step 10). Parallel fan-out by default; documented sequential
fallback for state-heavy works (graft G2). Full algorithm in [`tier-coordinator.md`](tier-coordinator.md).

**File:** `agents/tier-coordinator.md`

```yaml
---
name: tier-coordinator
description: Coordinates multi-tier adaptation of one source chapter. Fans transforms across tiers (parallel default; sequential fallback for state-heavy works) and reconciles them against shared source-canon while preserving tier-differentiated framing.
model: opus
skills:
  - laf-adaptation:adaptation-tiers
  - laf-adaptation:source-fidelity
  - laf-adaptation:kb-management
tools: Read, Write, Glob, Grep, Bash
---
```

**Inputs:** `work`, `chapter`, `tiers` (subset of `{1,2,3,5}`; T4 interpolated on demand), `mode`
(`parallel` | `sequential`, default `parallel`).

**Output contract:** writes `work/analysis/ch-<NN>-cross-tier.md` — a reconciliation report asserting
(a) source-fidelity consistency: every tier's transform traces to the same shared source fact; (b) no
tier leaked a higher-tier disclosure downward (a tier-1 chapter must not reveal what only tier-5 readers
should know); (c) monotonic framing: tier-N framing is never *more* mature than tier-(N+1). Emits
`status: RECONCILED | CONFLICT` with a conflict list the caller must resolve before chronicler runs.

---

## 6. Dispatch parameter summary (constraint #1 — tier axis is an explicit param everywhere)

| Agent | Provenance | Receives `active_tier`? | Notes |
|---|---|---|---|
| `analyst` | NATIVE | **No** (tier-invariant) | Source truth is shared across tiers (Q1.5) |
| `muse` | ADOPTED | Yes — in the brief it builds | Reads `kb/tiers/tier_N` |
| `writer` | ADOPTED-PATCHED | Yes — in the scene brief | Adaptation mode via `/adaptation-rules` |
| `critic` | ADOPTED | Yes — as focus-area context | Adaptation-quality focus loads `/adaptation-rules` |
| `editor` | ADOPTED | Yes — as context | Never folded (G3) |
| `reader-sim` | ADOPTED | Yes — as persona data | `developmental_basis` payload (§4) |
| `continuity-checker` | ADOPTED | Yes — selects per-tier canon | Reads `kb/adaptations/<work>/tier-N` |
| `safety-verifier` | NATIVE | **Yes — gating** | T1-2 blocking, T3 advisory, T4-5 N/A |
| `chronicler` | BUILD-NEW | **Yes — partitioning key** | `(work, tier, chapter)` |
| `tier-coordinator` | BUILD-NEW | Yes — the set of tiers | Owns the fan-out |

`active_tier` being a first-class, explicitly-passed parameter across the whole lineup — never dissolved
into persona or genre — is the mechanism that keeps constraint #1 alive.
