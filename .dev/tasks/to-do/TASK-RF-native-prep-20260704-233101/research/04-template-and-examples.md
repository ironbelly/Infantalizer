# R4: MDTM Template & Examples — Rules the Task-File Builder Must Follow

**Track goal:** Build an MDTM Template-02 task file to implement the LAF adaptation-prep phase.
**Global template path (builder MUST read this):** `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md`
**Prior example task folder:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/`

Status: Complete

---

## 1. Template Path (builder MUST read this exact file)

The project has **no** `.claude/templates/` directory. The builder MUST read the GLOBAL template:

`/config/.claude/templates/workflow/02_mdtm_template_complex_task.md`

This file is **1516 lines**, split into **PART 1** (build instructions, lines 1–1131, Sections A–M) and **PART 2** (the actual task-file template body, lines 1155–1463). All rule IDs below are quoted from PART 1 with line numbers.

---

## 2. Required Frontmatter Fields (PART 2 frontmatter, lines 1–61)

The frontmatter block at the top of the template IS part of the template (PART 2 note, line 1150). Required/populated fields:

- `id` (format `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS`), `title`, `description`, `version`
- `status` (enum: 🔵 Backlog | 🟡 To Do | 🟠 Doing | 🔴 Blocked | 🟢 Done | ⚪ Cancelled) — start at "🟡 To Do"
- `type` (enum incl. ✨ Feature, 🧩 Integration, 📚 Documentation, etc.), `priority` (🔥/🔼/▶️/🔽/🧊)
- `created_date`, `updated_date`, `assigned_to`, `coordinator: orchestrator`
- `parent_task`, `depends_on` (list), `spec_path` (line 23 — "driving spec/PRD/TDD path; populated by task-builder (A.2), empty if none")
- `reflect_pre` (line 24, block: verdict / coverage_pct / depth / tcs / run_id / report / reviewed_at — "PRE reflect-gate sign-off; populated by task-builder at A.10.7")
- `reflect_post` (line 32 — "POST reflect verdict; recorded by the executor after the final-phase reflect subagent runs")
- `related_docs` (list of path+description), `related_prd`, `related_tdd`, `tags`, `task_type: static` (line 60; `dynamic` only if runtime item-adding needed per I6)

The prior example populated `version`, `spec_path`, and both `reflect_pre`/`reflect_post` blocks fully — see §7.

---

## 3. Required Sections (PART 2 body, lines 1157–1463)

In order, every task file MUST contain:

1. `# [Task Title]` (line 1157)
2. `## Task Overview` (1159)
3. `## Key Objectives` (1163) — numbered concrete outcomes
4. `## Prerequisites & Dependencies` (1171) — Parent Task & Dependencies + **Previous Stage Outputs (MANDATORY INPUTS)** subsection, INFORMATIONAL ONLY, NO checklist items
5. `## Execution Context` (1193) — see §4 below (builder MUST populate)
6. `## Detailed Task Instructions` (1233) → `### Phase 1: Preparation and Setup` (1291) → subsequent phases → `### Phase Gate` blocks
7. `## Post-Completion Actions` (1423)
8. `## Task Log / Notes 📋` (1443) with `### Task Summary`, findings subsections, `### Execution Log`

**Rule D3 (line 286) — CRITICAL:** NO checklist items may appear before Phase 1 begins. Order is: Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (first executable items). All context-review / previous-stage-input checklist items live IN Phase 1, Steps 1.2–1.4.

---

## 4. `## Execution Context` Section Requirement (lines 1193–1231)

Line 1195 directive: *"BUILDER: Populate this section as a required build step. Every generated task file MUST have this section populated before the task file is marked ready."* Three required sub-blocks:

- **`### References`** (1197) — governing docs/specs/workflow files. Format: `- [Document Name](path/to/doc.md): [one-line purpose]`
- **`### Source Areas`** (1201) — codebase dirs/modules/file sets the task reads or modifies. Format: `- \`path/to/area/\`: [what it contains / why relevant]`
- **`### Key Constraints`** (1205) — top governing constraints: QA intensity, scope limits, known blockers, standing prohibitions.

Plus the boilerplate sub-blocks the template already carries: `### Handoff File Convention` (1209), `### Frontmatter Update Protocol` (1223).

**NO `file:line` in the block header:** the References/Source-Areas format uses document paths and section anchors (e.g. `§7`, `§3.2`), NOT `file:line`. The example task's Execution Context (§7 below) cites section markers only, never line numbers, in this block. (`file:line` evidence belongs inside checklist-item "ensuring…" clauses and in QA reports, not in the Execution Context header block.)

**Anti-orphaning rule:** Task-completion items (frontmatter status→Done, completion_date, Task Summary, post-completion QA/fidelity gates) MUST live inside the **final phase / `## Post-Completion Actions` section** (lines 1423–1441), NOT floating loose. C4 (242) + I13 (616) + I17 (675): post-completion validation items appear in `## Post-Completion Actions` BEFORE the frontmatter-update item. Do NOT create a separate "Task Completion and Handoff Protocol" section (C4 line 246, I13 line 620) — handoff info lives in `ib_agent_core.md`, not individual task files.

---

## 5. The B2 Self-Contained Item Pattern (Section B, lines 148–213)

**Why (B1, 151):** Rigorflow runs tasks in batches across sessions; context loaded in batch 1 is LOST by batch 3+. So EVERY checklist item must be self-contained. Standalone "read context" items are USELESS.

**B2 (159) — every checklist item is a COMPLETE, SELF-CONTAINED PROMPT with 6 elements:**
1. **Context Reference with WHY** — what file(s) to read and why needed for THIS action
2. **Action with WHY** — what to do with that context and why
3. **Output Specification** — exact output file name, location, content, template to follow
4. **Integrated Verification** — an "ensuring…" clause (DO NOT assume/hallucinate; 100% accuracy from source; document negative evidence on failure)
5. **Evidence on Failure Only** — log to task notes ONLY if blocked (success is evidenced by the output file)
6. **Explicit Completion Gate** — *"This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."*

**B3 (167):** ONE FULL PARAGRAPH per item — verbose, explanatory, executable independently. Not bullets/multi-line.

**B5 FORBIDDEN (181):** standalone "read context" items; missing context reference; multi-line/bulleted items; separate verification/confirmation items; overly-granular items ("create directory" alone); separate REMINDER blocks between items.

**J1 error clause (850)** embedded in every item: *"If unable to complete due to missing information, file access issues, or unclear requirements, log the specific blocker using the templated format in the ### Phase [N] Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete."*

---

## 6. Core Granularity & Structure Rules (exact IDs + one-line meanings)

- **A3 (108) — COMPLETE GRANULAR BREAKDOWN:** individual checklist item for EVERY file/component/iteration; NO high-level/bulk operations; exact file paths + measurable outcomes. (One item per file — no batch items.)
- **A4 (114) — ITERATIVE PROCESS STRUCTURE:** for any multi-item process: (X.1) pre-enumerate ALL items in an initial scan step, (X.2) one checklist item per specific item, (X.3) consolidation step only AFTER all items complete.
- **E1 (295) — CHECKBOX FORMAT:** every actionable item is `- [ ]`; flat structure only, NO nested/parent checkboxes; `**Step X.Y:**` headers group (not checkboxes); items in completion order.
- **E2 (311):** summary/parent checkboxes come AFTER their components, never before; no parent-before-children.
- **E3 (367):** sequential top-to-bottom only; never require marking items above current position; each phase completes all its checkboxes before the next.
- **E4 (384):** no checkboxes next to step numbers; NO separate REMINDER blocks (integrate reminders into the item).
- **C1–C3 (223–239):** Outputs/Success-Criteria/Verification are EMBEDDED in items (via the "ensuring…" clause), never separate sections or separate items.
- **I12 (609):** verification is integrated, NO separate verification items — QA process handles inter-batch verification (phase-gate rules I15–I16).
- **F1 (411):** worker execution loop = READ → IDENTIFY → EXECUTE → UPDATE → REPEAT (one item at a time).
- **F2a (431):** item-execution discipline — one item per F1 loop; parallel-spawning exception (447) for INDEPENDENT same-phase subagents.
- **I18 (688):** code-modifying tasks MUST include ≥1 testing item (test command + pass criteria + results capture) using the L3 pattern.

---

## 7. L1–L6 Handoff / Subagent Patterns (Section L, lines 902–1027)

Handoff files persist across batches at `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/` (convention lines 909–921). Use these ONLY when items depend on earlier items' outputs (else use template 01).

- **L1 Discovery (928):** an item explores codebase/data and writes a structured, machine-readable findings file — the discovery file IS the deliverable; later items read it directly. → `phase-outputs/discovery/`
- **L2 Build-from-Discovery (940):** reads the discovery file (WHAT to process) AND the original source file (the CONTENT), then creates the deliverable. Always reference both paths.
- **L3 Test/Execute (952):** runs a command/script/test; captures BOTH raw output (`.txt`) AND a structured summary (`.md`) → `phase-outputs/test-results/`.
- **L4 Review/QA (964):** assesses a prior output vs source/spec; MUST emit a structured PASS/FAIL verdict with specific findings → `phase-outputs/reviews/`.
- **L5 Conditional-Action (976):** branches on a prior result file; MUST handle BOTH success AND failure branches; output file always created → `phase-outputs/plans/`.
- **L6 Aggregation (990):** consolidates multiple prior outputs (discover via Glob, don't hardcode lists) into one report → `phase-outputs/reports/`. Typically the final item of a phase / the aggregation step of a QA gate.
- **L7 (1002)** = pattern-selection guide. Common structures: `L1→L2→L4→L6`; `build→L3→L5`; full lifecycle `L1→L2→L3→L5→L4→L6`; with QA gates `L1→L2→[M3 gate]→L3→L5→L4→L6→[M3 gate]`.

**Subagent boundary rule (F2 line 427):** a subagent receives work from a SINGLE checklist item only; MUST NOT delegate the F1 loop or span multiple phases.

---

## 8. M3 / M4 / I19 / I20 / I21 / I22 QA-Gate Encoding Rules (exact IDs + one-line meanings)

- **I15 (635) — PHASE-GATE QA ENFORCEMENT:** every task with 2+ phases MUST have ≥1 phase-gate QA checkpoint between the primary execution phase and any dependent later phase. Gates with only 1–2 agents are PROHIBITED. Floors: FINAL/assembled-output gate = **min 6 agents** (3 rf-qa structural + 3 rf-qa-qualitative content); INTERMEDIATE gate = **min 5 agents** (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). Every gate step is an explicit `- [ ]` item — no implicit/prose QA (651).
- **I16 (653) — VERDICT & FIX CYCLES:** binary PASS/FAIL; ANY issue of ANY severity → FAIL. Consolidated verdict FAILs if any agent found any issue. Max fix cycles per gate type: research-gate 3, synthesis-gate 2, report-validation 3, task-integrity 2, qualitative 3, source-fidelity 3 → after max, HALT/escalate (or Open Questions for synthesis/task-integrity).
- **I19 (699) — LENS-BASED QA MINIMUM AGENTS (FULL intensity):** size-scaled floors — <500 lines: 3+3=6; 500–1500: 4+4=8; 1500–3000: 5+5=10; >3000: 6+6=12. Standard structural lenses (rf-qa): template-conformance, internal-consistency, evidence-quality, completeness. Standard content lenses (rf-qa-qualitative): actionability, numbers-and-metrics, crossref-chain-integrity, domain-accuracy. Adversarial framing MANDATORY: *"Assume this document has at least N errors focused on [lens]. Find them"* (N: 5/10/15/20 by size). Intermediate-gate table (733): research/synthesis/task-integrity gates = 5 agents each with named agent types.
- **I20 (745) — SERIALIZED FIX AUTHORIZATION:** any gate with 3+ agents on the same file MUST serialize fixes. Protocol: (1) all lens agents report with `fix_authorization: false`, (2) consolidate to `${TASK_DIR}qa/qa-consolidated-findings.md`, (3) ONE rf-qa agent applies ALL fixes with `fix_authorization: true`, (4) verification round (min 2 agents, `fix_authorization: false`), (5) repeat from consolidation only if verification fails. Parallel fix authorization PROHIBITED.
- **I21 (759) — SOURCE-DOCUMENT FIDELITY GATE REQUIREMENT:** every task whose outputs derive from source docs MUST include an M4 fidelity gate. Mandatory for PRD/TDD/roadmap/tech-reference/tech-research/README/repo-cleanup and any task that reads source docs to produce output. Checks: semantic coverage, detail preservation, cross-source contradiction, phantom-coverage detection, operational/compliance completeness. Min 2 fidelity agents (partition to 3–4 if sources >1000 lines); each reads its assigned source-section range + the FULL output. Runs AFTER the M3 lens gate.
- **I22 (793) — QA INTENSITY LEVELS:** scales agent counts. **lite** (small <300 lines): intermediate 2, final 3, fidelity 1, 1 fix cycle, 1 verifier, no partition, double-QA disabled. **standard** (300–1500 lines): intermediate 3, final 7 (3 structural + 3 content + 1 domain), fidelity 2, 2 fix cycles, 2 verifiers, partition only >10 files. **full** (>1500 lines / critical): full I19/I20/I21 tables unchanged. Default map: Quick→lite, Standard→standard, Deep→full; user may override. **Serialized fix protocol (I20) applies at ALL intensities** — never bypassed, only simplified.
- **M3 (1059) — LENS-BASED QA SEQUENCE (mandatory; replaces deprecated M1):** 8 steps, each an explicit `- [ ]` item — (1) L6 aggregate; (2) structural lens agents PARALLEL, one per lens, `fix_authorization:false`, reports to `${TASK_DIR}qa/qa-structural-[lens]-report.md`; (3) content lens agents PARALLEL to `qa-content-[lens]-report.md`; (4) domain lenses if any; (5) consolidate to `qa-consolidated-findings.md`; (6) ONE fix agent `fix_authorization:true`; (7) verification round min 2 PARALLEL; (8) L5 conditional proceed / cycle per I16. Steps 2+3 may share one parallel batch. Partitioning is WITHIN a lens (full-doc coverage per lens), increasing agent count.
- **M4 (1098) — SOURCE-DOCUMENT FIDELITY GATE:** runs AFTER M3. Steps: (1) identify source docs (explicit, not discovered); (2) fidelity agents PARALLEL (min 2, partitioned 3–4 if >1000 lines) each reading assigned source range + FULL output → `qa-source-fidelity-report-[N].md`; (3) cross-source contradiction agent (reads all sources, not output) if multiple sources; (4) consolidate; (5) ONE fix agent `fix_authorization:true`; (6) verification round min 2; same cycle control as M3 (max 3, then HALT). Every step an explicit `- [ ]` item.
- **M2 (1047) — PHASE-GATE APPLICABILITY:** maps task type → where gates are required. All gates use M3 (M1 deprecated) + I20 serialized fixes; every spawn/consolidation/fix/verification is an explicit `- [ ]` item.

---

## 9. Reusable Patterns from the Prior Example Task (THIS repo)

**File:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md` (704 lines, `status: 🟢 Done`, `type: 🧩 Integration`, `qa_intensity=full`).

**Effective structure the builder should mirror:**

- **Phase naming maps design phases to task phases:** `### Phase 2: Phase 0 — Vendor …`, `### Phase 3: Phase 1 — Native Spine …`, etc. Each build phase is immediately followed by its own `### Phase Gate N: Quality Verification (M3 Lens-Based QA)` (and `+ M4 Source-Document Fidelity Gate` after Phase 1, where verbatim-carry content had to be verified byte-faithful). This is the recommended template for adaptation-prep: build phase → M3 gate (→ M4 gate if content is carried/derived from source).

- **Execution Context (lines 126–177) is fully populated** with `### References` (8 doc links with §-anchors, e.g. `[DESIGN.md](...): … build phases & gates §7`), **`Source areas`** (design-spec dir, port-source config dirs, upstream checkout, greenfield target tree), and **`### Key Constraints`** as a NUMBERED list of 8 hard constraints (ADR references, boundary contract #6, carried-verbatim=zero-rework, no tier_4.yaml, Tolkien-not-PD, `QA intensity = full`, reconciled counts). No `file:line` anywhere in this block — only `§` section anchors. Reuse this exact shape.

- **Per-file / per-item granularity (A3/A4 in practice):** vendoring is split into per-artifact steps — Step 2.3 "Vendor the 11 adopted agents (per-file granularity — provenance grouped, manifest rows per-file)", Step 2.4 per-skill, and Phase-1 has one Step per file (3.1…3.18: one skill/agent/kb-port each). Each `kb/tiers/tier_N.yaml` port is its OWN step (3.11–3.15). This is the "one item per file/component" pattern the adaptation-prep builder must follow.

- **Boundary-check gate items (L3 test/execute + embedded fix loop):** Steps 2.13, 2.14, 3.19, 4.8, 5.10, 6.3 all run `uv run python laf-adaptation/scripts/check_boundary.py [--init]`, capture raw `.txt` + structured `.md` summary to `phase-outputs/test-results/`, and embed an IF-PASS-proceed / IF-FAIL-fix-and-rerun loop with **max 3 fix cycles then HALT + log to `### Phase 2 Findings`**. The gate is GREEN only on exit 0, with explicit enumeration of the boundary rules A–F checked. This is the reusable "boundary-check gate item" for any adaptation-prep task that must stay inside the vendor boundary.

- **Hard-gate / L4-verdict items:** Phase 5 (Phase 3) decomposes an integration test into per-condition L4 verdict items (Steps 5.6–5.10 = five HARD-GATE conditions, each its own `- [ ]`), then Step 5.11 L6-aggregates the 5 verdicts into one GREEN-only-if-all-5-PASS report (else HALT). Pattern: split a multi-condition gate into one verdict item per condition + one aggregation item.

- **QA gate encoding (M3) is fully expanded per-agent:** each Phase Gate has `PGn.1` aggregate (L6), `PGn.2` structural lens agents PARALLEL `fix_authorization: false`, `PGn.3` content lens agents PARALLEL, `PGn.4` consolidate + ONE fix agent (serialized I20), `PGn.5` verification round PARALLEL. Every agent spawn is its own `- [ ]` item — matching M3/I15.

- **Post-Completion Actions (lines 510–548)** contains: a full **final assembled-output M3 QA gate** (PC.1–PC.5) on the complete tree, then **Step PC.6 POST reflect gate** (penultimate item, runs `superclaude reflect run … --depth deep --fix` audit-only, exit-0-only proceeds, exit 10/11/2 = FAIL→HALT, `reflect_post` left for the wrapper to write back), then the Task Summary item, then the frontmatter status→Done item **gated on all three** (POST reflect PASS + final QA gate PASS + Phase-3 hard gate GREEN). This is the anti-orphaning completion structure in practice — all completion items live inside `## Post-Completion Actions`.

- **Task Log / Notes** has per-phase `### Phase N - … Findings` subsections + `### Phase Gate Findings` for J1 blocker logging, plus `### Task Summary` and `### Execution Log`.

---

## Summary

- **Builder MUST read:** `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` (global; no project-local template exists). PART 1 = rules (A–M), PART 2 = the body to copy/fill.
- **Core rules:** B2 6-element self-contained one-paragraph items (context+why / action+why / output / integrated "ensuring…" verification / failure-only logging / completion gate); A3/A4 one-item-per-file granularity + enumerate-then-process; D3 no items before Phase 1; Execution Context (References/Source Areas/Key Constraints, `§`-anchors NOT file:line) is a required build step; anti-orphaning = all completion items inside `## Post-Completion Actions`. QA gates: M3 lens-based (I19 floors, I22 intensity), I20 serialized fixes, M4/I21 fidelity gate when outputs derive from source docs.
- **Example to mirror:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/…md` — build-phase→M3(→M4) cadence, per-file steps, `check_boundary.py` L3 fix-loop gate items (max 3 cycles→HALT), per-condition L4 verdict + L6 aggregation, and the PC.1–PC.6 post-completion QA + POST-reflect completion structure.

Status: Complete



