---
title: "Prep-Phase Agent & Command Schemas"
parent: DESIGN.md
status: draft
---

# Prep-Phase Agent & Command Schemas

Copy-paste-ready frontmatter and body contracts for the new `prep-cordinator` agent, the two boundary-safe
body edits (`analyst` NATIVE, `tier-coordinator` BUILD-NEW), and the two `.claude/commands/laf/` commands.
All frontmatter uses the **Claude-native (cw-lowered)** dialect per `laf-adaptation/CLAUDE.md §3` and the
0.1 `agent-schemas.md §1` permitted-key set (`name`, `description`, `model`, `skills`, `tools`). No Mars
keys.

---

## 1. `prep-cordinator` — the NATIVE orchestrator (R4)

**Role:** Owns the 8-stage prep pipeline. Autonomously researches a novel (two-track), classifies its
adaptation challenges, derives a confidence-scored work-mapping, asks only human-judgment questions, emits
the fixed-path package, gates on greenlight, and prints the `/laf:rewrite` handoff. Sibling to `muse`
(author-facing orchestrator) but for **onboarding** a new work rather than writing chapters.

**File:** `laf-adaptation/agents/prep-cordinator.md`

```yaml
---
name: prep-cordinator
description: Autonomous onboarding orchestrator for a new literary work. Given a novel title and a required source path, researches it two-track (context + text), classifies adaptation challenges, derives a confidence-scored <work>-mapping, asks only human-judgment questions, emits the fixed-path work/prep/<slug>/ package, gates on greenlight, and prints the /laf:rewrite handoff. Reuses the NATIVE spine; edits no adopted body.
model: opus
skills:
  - laf-adaptation:source-fidelity
  - laf-adaptation:adaptation-tiers
  - laf-adaptation:adaptation-rules
  - laf-adaptation:kb-management
  - laf-adaptation:prep
  - laf-adaptation:thematic-fidelity
tools: >
  Agent(web-researcher, analyst, tier-coordinator),
  Read, Write, Glob, Grep, WebSearch, WebFetch
---
```

> **Model = `opus`** (Q6): matches `muse` and `tier-coordinator`. **Name spelling `prep-cordinator`** is
> intentional and matches the merged spec (R4) verbatim — `name:` must equal the filename stem, so the file
> is `prep-cordinator.md`. Do not "correct" it to `prep-coordinator` without updating every reference
> (spec, VENDOR row, command delegation) in lockstep.

### 1.1 Inputs

| Input | Source | Required | Notes |
|---|---|---|---|
| `title` | `/laf:prep "<title>"` positional | Yes | The only thing the user must type |
| `source_path` | `--source <path>` OR Stage-1a elicitation | **Yes (Q1)** | Elicited as a required input, **not** a clarifying question, if `--source` omitted |
| `work_slug` | derived from `title` | — | lowercase; the `work/prep/<work-slug>/` key and `--work` value (e.g. `narnia`) |

### 1.2 The 8-stage body (procedure — full prose authored at implement time)

The body loads `/prep` and executes its 8-section procedure. Stage ownership (details in
[`DESIGN.md §3`](DESIGN.md) and [`prep-skill-specs.md`](prep-skill-specs.md)):

```
STAGE 1 RESEARCH   (a) require source_path (Q1); (b) /source-fidelity Phase-0 @ work level →
                   NO-ACCESS ABORTS the whole prep; (c) Agent(web-researcher) → 00-work-context.md
STAGE 2 ROADMAP    read 00 + /prep §2 taxonomy skeleton → prep task list; run 3-4 autonomously
STAGE 3 ANALYZE    Agent(analyst, granularity=work, out_path=…/20-analysis-work-level.yaml) [text track]
        +CLASSIFY  apply /prep §2 taxonomy → 10-challenges.yaml (governing rule, per-tier strategy,
                   human_judgment_dimension, compound_scene)
STAGE 4 MAPPING    /prep §4 derive 30-mapping.yaml (per-entry min(text,context); top-level meaning:)
STAGE 5 Q-GATE     emit `## Questions for the user` (coverage-constrained, /prep §5); HALT; resume on reply
STAGE 6 PACKAGE    write 40-prep-brief.md + 70-traceability.md; fold answers into 10/20/30
STAGE 7 GREENLIGHT write 50-greenlight.md; emit confirmation; HALT; on CONFIRM promote 30 via /kb-management
STAGE 8 HANDOFF    write 60-handoff-prompt.md (literal `/laf:rewrite --work <slug>`)
```

**Write-scope discipline.** `prep-cordinator` writes only under `work/prep/<work-slug>/` and (on greenlight,
via `/kb-management`) to the two promotion targets. It never writes into `kb/canon/` or the per-tier
`kb/adaptations/` layer — those belong to the rewrite phase's `chronicler`.

---

## 2. `analyst` work-level dispatch contract

The `prep-cordinator` dispatches the **existing** `analyst` agent — it does not fork a new analyzer. Work
mode is a small additive branch of the analyst's NATIVE body (§3). Dispatch payload:

```yaml
# Agent(analyst, …) call from prep-cordinator, STAGE 3
inputs:
  work: <work-slug>
  granularity: work                 # NEW input; default 'chapter' preserves all existing callers
  source_path: <the required novel source, from Q1>
  out_path: work/prep/<work-slug>/20-analysis-work-level.yaml   # NEW input; default = work/analysis/ch-<NN>.yaml
```

Work-mode analysis runs the **same** `/source-fidelity` 5-phase protocol, scoped to the whole work rather
than one chapter, and emits the work-level schema (`20-analysis-work-level.yaml`, defined in
[`package-schemas.md §3`](package-schemas.md)) — every fact confidence-tagged, plus the new `meaning:` and
`compound_scene:` outputs. Phase-0 NO-ACCESS still ABORTS (the prep-cordinator surfaces the abort to the
user and stops).

---

## 3. `analyst` — NATIVE body edit (R10, R11 + work mode)

`agents/analyst.md` is **NATIVE** (`VENDOR.md` line 111: `agents/analyst.md | NATIVE | — | —`). Its body is
**not** hash-pinned, so this edit is boundary-safe and requires **no** VENDOR change. Three additive
changes, each preserving current per-chapter behavior by default.

### 3.1 New inputs (additive to the "Inputs" section)

```diff
  ## Inputs (passed by the caller)
  - `source_path` — a `source/<work>/ch-<NN>.txt` file to analyze.
  - `work` — the work label.
  - `chapter` — the chapter number `<NN>`.
+ - `granularity` — `chapter` (default) | `work`. `work` runs the 5-phase protocol over the whole-work
+   source declaration and emits the work-level schema. **Default `chapter` reproduces today's behavior
+   exactly.**
+ - `out_path` — output file path. Default `work/analysis/ch-<NN>.yaml` (chapter mode);
+   `work/prep/<work-slug>/20-analysis-work-level.yaml` when `granularity: work`.
```

### 3.2 New output fields — `meaning` and `compound_scene` (R10, R11)

Extend the output schema (both the in-body "Output contract" and the mirrored `/source-fidelity` schema —
see [`prep-skill-specs.md`](prep-skill-specs.md) and [`package-schemas.md §3`](package-schemas.md)):

```diff
  transformation_flags:
    violence:  {instances: N, severity: low|med|high}
    death:     {instances: N, severity: low|med|high}
    emotional: {instances: N, severity: low|med|high}
    abstract:  {instances: N, severity: low|med|high}
+ meaning:                       # R10 — the meaning-preservation invariant (per work/chapter/scene)
+   value: "<what this unit MEANS beneath its surface — the allegory/theme to neither add nor strip>"
+   confidence: CERTAIN | PROBABLE | UNCERTAIN
+ compound_scene: true|false     # R11 — true iff ≥2 HIGH-severity transformation_flags co-occur in one scene
+ compound_scenes:               # present only when compound_scene: true — one entry per flagged scene
+   - {scene: "<name>", cooccurring_flags: [death, emotional], severity: high}
  uncertainties:
    - "list of items the analyst could not verify"
```

- **`meaning`** is grounded in the `/thematic-fidelity` skill (Hutcheon/Bortolotti: *meaning preserved
  under surface transformation*). At `granularity: work` it is the top-level work meaning; at
  `granularity: chapter` it is per-chapter (and, where the analyst decomposes a scene, per-scene).
- **`compound_scene`** fires the prep-skill §2.1 reconciliation protocol. Definition (spec R11): **≥2
  high-severity `transformation_flags` co-occurring** in one scene.

### 3.3 Body-note addition (analyst § "Hard behavior")

Add one paragraph after the Phase-0 block:

```markdown
**Meaning & compound-scene passes (additive; do not gate the ABORT).** After Phase 4, emit `meaning:`
for the analyzed unit (the theme/allegory to be neither added nor stripped — `/thematic-fidelity`), tagged
with its own confidence. Then scan for co-occurrence: any scene where ≥2 transformation_flags are
`severity: high` sets `compound_scene: true` and is listed under `compound_scenes:`. These passes never
relax the Phase-0 NO-ACCESS ABORT gate; on ABORT the file still carries only `status: ABORTED`.
```

**Back-compat assertion (P1 gate):** with `granularity` defaulting to `chapter` and `out_path` defaulting
to `work/analysis/ch-<NN>.yaml`, every existing per-chapter dispatch is unchanged except for two **additive**
output keys (`meaning`, `compound_scene`) that downstream readers may ignore.

---

## 4. `tier-coordinator` — BUILD-NEW body edit: Check D (R10)

`agents/tier-coordinator.md` is **BUILD-NEW** (`VENDOR.md` line 117: `agents/tier-coordinator.md | BUILD-NEW
| — | —`). Body not hash-pinned → boundary-safe, no VENDOR change. Add a **fourth** reconciliation check
alongside A/B/C.

### 4.1 New check (insert after "Check C — Framing monotonicity")

```markdown
### Check D — Meaning preservation (R10; /thematic-fidelity)
Every tier's rendering must **preserve the work-level `meaning`** while its surface transforms. Read the
top-level `meaning:` from `<work>-mapping.yaml` (and the per-unit `meaning` in `shared_analysis`). For each
element shared across tiers, assert the tier's rendering still carries that meaning — the allegory/theme is
neither added where the source withholds it nor stripped where the source asserts it.
```
for element shared across tiers:
    m = meaning_of(element, shared_analysis | mapping)
    for tier in tiers:
        if not preserves_meaning(render(element, tier), m):
            conflicts += {type: "meaning_diff", tier, element, meaning: m}
status_meaning: Meaning-PRESERVED | Meaning-DIFF
```
`preserves_meaning()` is an ordinal judgment, not a score: does the transformed surface still *mean* what
the source unit means at the target tier's altitude? A tier-1 "Grumpy King" preserves the meaning "an
external corrupting force, not innate evil" (Agency Externalization is meaning-preserving); a rendering that
silently drops the allegory, or invents one the source never had, is `Meaning-DIFF`.
```

### 4.2 Wire Check D into the report + status

```diff
  ## Checks
  - A source-fidelity: PASS …
  - B disclosure-leak:  PASS …
  - C monotonicity:     PASS …
+ - D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)
```

`Meaning-DIFF` contributes a `{type: "meaning_diff", …}` entry to the existing `conflicts:` list, so a
meaning divergence blocks `chronicler` exactly as an A/B/C conflict does — **no new control flow**, it
rides the existing `RECONCILED | CONFLICT` gate. The `tier-coordinator` already loads `/adaptation-tiers`,
`/source-fidelity`, `/kb-management`; Check D reads `meaning` as **data** from the mapping/analysis, so
**no new skill line** is required (keeps the frontmatter diff empty).

---

## 5. Command specs (`.claude/commands/laf/`)

Both commands are **thin delegators** living outside `laf-adaptation/` (harness surface; not in
`VENDOR.md`). They reference `skills/prep/resources/path-contract.md` for all paths (R3) — never restate a
path literally.

### 5.1 `.claude/commands/laf/prep.md` → `/laf:prep` (R1)

```markdown
---
description: Onboard a new literary work — research, analyze, and derive its adaptation prep package.
argument-hint: "<novel title>" [--source <path-or-url>]
---

# /laf:prep

Delegate the entire run to the `prep-cordinator` agent (opus). Pass the positional `"<title>"` and, if
present, `--source <path>`.

The `prep-cordinator` owns the 8-stage procedure and the two HALT gates (question gate, greenlight). Do not
restate the pipeline here — it lives in `laf-adaptation/skills/prep/SKILL.md`. The output package path
layout is fixed by `laf-adaptation/skills/prep/resources/path-contract.md`.

If `--source` is omitted, the FIRST thing the coordinator does is elicit the source path as a **required
input** (Q1) — the novel text is mandatory; there is no memory-based work-level analysis.
```

### 5.2 `.claude/commands/laf/rewrite.md` → `/laf:rewrite` (R9)

```markdown
---
description: Begin the chapter rewrite phase for a work already prepped by /laf:prep.
argument-hint: --work <work-slug>
---

# /laf:rewrite

Read the prep package for `--work <slug>` by **hardcoded path** — no other arguments. Per
`laf-adaptation/skills/prep/resources/path-contract.md` §rewrite_phase_reads, read exactly:

1. `work/prep/<slug>/30-mapping.yaml`      (the derived mapping, incl. top-level `meaning:`)
2. `work/prep/<slug>/40-prep-brief.md`     (decisions, cross-tier spine, answered questions)
3. `work/prep/<slug>/10-challenges.yaml`   (challenge taxonomy + per-tier strategy)

Then hand control to the `muse` agent for chapter 1 of the existing per-chapter 11-step workflow, with the
instruction: **"The prep package is your only context; do not ask the user to restate anything already
decided in it."** `muse` reads the mapping's inline per-entry confidence and top-level `meaning:` as data —
no muse edit, no new skill (D6).
```

> **Guard.** `/laf:rewrite` must confirm `50-greenlight.md` for `<slug>` shows `status: CONFIRMED` before
> handing to `muse`. A `PENDING` (un-greenlit) package is not ready for rewrite — surface that and stop.
