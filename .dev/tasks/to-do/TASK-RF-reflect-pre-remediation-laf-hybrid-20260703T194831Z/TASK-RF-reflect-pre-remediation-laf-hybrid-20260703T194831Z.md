---
id: "TASK-RF-reflect-pre-remediation-laf-hybrid-20260703T194831Z"
title: "Apply PRE-reflect remediations to TASK-RF-laf-hybrid-build-20260703-115948 (3 blocking findings)"
description: "Corrective task authored by sc:reflect PRE gate (run_id pre-20260703192947-793c0654). The PRE reflect gate against TASK-RF-laf-hybrid-build-20260703-115948.md returned status: partial with 3 blocking findings (all DRIFT or NECESSARY-WITH-RISK — no REGRESSION). This task applies the prescriptive fixes to the driving tasklist so it becomes execution-ready. AUTO-FIXABLE under --remediate headless auto-accept (FR-9)."
version: "0.1"
status: "🟡 To Do"
type: "🔧 Fix"
priority: "🔼 High"
created_date: "2026-07-03"
updated_date: "2026-07-03"
assigned_to: "orchestrator"
autogen: false
coordinator: orchestrator
spec_path: ".dev/releases/current/0.1/design/DESIGN.md"
parent_task: "TASK-RF-laf-hybrid-build-20260703-115948"
depends_on: []
reflect_pre:
  verdict: ""
  coverage_pct: null
  depth: ""
  tcs: 0
  run_id: ""
  report: ""
  reviewed_at: ""
reflect_post: ""
related_docs:
- path: ".dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/reflect/pre/adversarial/merged-verdict.md"
  description: "Source of the 3 blocking findings + 3 non-blocking recommendations (the reflect merge verdict)"
- path: ".dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/reflect/pre/return-contract.yaml"
  description: "Reflect return contract (status: partial, coverage_pct_union: 0.97)"
tags:
- "reflect-remediation"
- "pre-gate"
- "laf-hybrid"
template_schema_doc: ""
estimation: "small (3 prescriptive edits to a tasklist file + 1 optional softening pass)"
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
---

## Task Overview

The PRE reflect gate (`sc-reflect-protocol --mode pre --depth deep`) audited `TASK-RF-laf-hybrid-build-20260703-115948.md` (151 items, 6 phases) against the LAF 0.1 design pack. The verdict was **status: partial** — the tasklist is spec-complete (coverage_pct_union: 0.97) and faithful to DESIGN.md §7 Phases 0-4, but 3 blocking findings must be remediated before execution. **No REGRESSION was upheld** — all three regression candidates raised by T2 reviewers were downgraded after adversarial debate (A1→NECESSARY, A2→DRIFT, Q1→NECESSARY-WITH-RISK).

This task applies the 3 prescriptive blocking fixes + the 3 non-blocking recommendations to the driving tasklist. It is AUTO-FIXABLE (solely Drift/Necessary registers — no HUMAN-REQUIRED register per FR-9 headless auto-accept rules).

## Key Objectives

1. Fix Finding A2 (blocking DRIFT): `--init` wording in Step 2.2.
2. Fix Finding Q2 (blocking DRIFT): verifier cwd/path-rooting in Step 2.2 + verifier commands.
3. Fix Finding Q1 (blocking NECESSARY-WITH-RISK): PC.6 auto-mutation posture.
4. Apply 3 non-blocking recommendations (A1 PATH tightening, R2 adversarial-framing softening, F2 spec-author note).

## Prerequisites & Dependencies

- **Parent task:** TASK-RF-laf-hybrid-build-20260703-115948 (the tasklist being remediated — NOT yet executed).
- **Source of truth:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/reflect/pre/adversarial/merged-verdict.md` (the merge verdict with full evidence + rationale for each finding).

## Detailed Task Instructions

### Step 1: Fix Finding A2 — `--init` wording (BLOCKING, DRIFT)

**Target file:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md`

**Locate** Step 2.2 (line ~182), the bullet describing the `--init` mode. Current text contains:
> "the --init mode (requires `--upstream <dir>`: ... applies the writer additive graft before hashing its laf_sha256)"

**Replace** the phrase "applies the writer additive graft before hashing its laf_sha256" with:
> "hashes the writer.md that Step 2.3 already grafted (it does NOT apply the graft itself — the script never transforms the framework per boundary-contract.md:17-19; the graft is a vendoring-time transform performed in Step 2.3, and --init records the laf_sha256 of the already-grafted file per boundary-contract.md:85-86)"

**Verification:** re-read boundary-contract.md:17-19 and :85-86 and confirm the new wording is consistent with both (script never transforms; laf_sha256 computed on the file "after the additive graft" = the file Step 2.3 produced). Confirm no other Step in the tasklist says --init applies the graft.

### Step 2: Fix Finding Q2 — verifier cwd/path-rooting (BLOCKING, DRIFT)

**Target file:** same tasklist.

**Option 2a (PREFERRED — script-internal rooting, cwd-independent):** In Step 2.2, add a requirement to the `check_boundary.py` authoring spec:
> "The script MUST resolve all framework-relative paths (VENDOR.md, `glob("agents/*.md")`, `glob("skills/**/SKILL.md")`, `upstream_blob()`) from `Path(__file__).resolve().parents[1]` (the laf-adaptation/ root derived from the script's own location at scripts/check_boundary.py), NOT from the current working directory. This makes the verifier cwd-independent and consistent with boundary-contract.md:109-150 regardless of whether it is invoked from the repo root or from laf-adaptation/."

**Option 2b (alternative — explicit cd in every command):** change every verifier command in Steps 2.13, 2.14, 3.19, 4.8, 5.10, 6.3, and the Post-Completion items from `uv run python laf-adaptation/scripts/check_boundary.py ...` to `cd laf-adaptation && uv run python scripts/check_boundary.py ...` (and the .githooks/pre-commit + CI workflow must likewise `cd` or set `working-directory: laf-adaptation`).

**Pick ONE option and apply consistently.** Option 2a is preferred (one place to maintain; cwd-independent). If 2a, also update the .githooks/pre-commit (Step 2.10) and CI workflow (Step 2.11) notes to reflect that the script self-roots.

**Verification:** after the fix, the verifier command `uv run python laf-adaptation/scripts/check_boundary.py` run from `/config/workspace/Infantalizer` (repo root) must work identically to running `uv run python scripts/check_boundary.py` from `/config/workspace/Infantalizer/laf-adaptation`.

### Step 3: Fix Finding Q1 — PC.6 auto-mutation posture (BLOCKING, NECESSARY-WITH-RISK)

**Target file:** same tasklist.

**Option 3a (PREFERRED for 0.1 — audit-only):** In Step PC.6 (line ~524), change the command:
> `superclaude reflect run "...TASK...md" --depth deep --fix --promote`
to:
> `superclaude reflect run "...TASK...md" --depth deep --no-promote`
(Preserve the recursion-breaker wrapper guard and the exit-code handling: exit 0 proceeds; exit 10/11/2 FAILs and HALTs. The `--no-promote` flag makes the gate audit-only — no auto-fix mutation, no work-unit relocation. Promotion (if desired) becomes a separate explicit operator step after the audit passes.)

**Option 3b (alternative — retain --fix/--promote but add a re-verification step):** keep `--fix --promote` BUT insert a new **Step PC.7** after PC.6:
> "Step PC.7: Post-reflect re-verification. IF Step PC.6 reflect run applied any auto-fix (exit 0 with `citations_dropped` changed OR any artifact mutated per the reflect report), re-run the 5 Phase-3 hard-gate condition files (Step 5.6-5.10 verdicts) AND `check_boundary.py` (Step 6.3) on the post-reflect tree. Only if all 5 conditions + boundary gate still PASS does the status flip to Done. If PC.6 made no mutations, skip PC.7."

**Pick ONE option.** Option 3a is recommended for a 0.1 release (simpler, audit-only, no auto-mutation risk); 3b preserves auto-fix power but adds ceremony.

**Verification:** re-read DESIGN.md:296 (5 hard-gate conditions) and :308 ("Phase 3 hard gate is the definition of '0.1 done'") and confirm the chosen option ensures all 5 conditions hold on the FINAL tree state before status flips to Done.

### Step 4: Apply non-blocking recommendations (OPTIONAL but recommended)

**4a (Finding A1, recommendation):** In Step 5.1, tighten PATH A as the gate-faithful default and explicitly mark PATH B as a mechanics-only proof that satisfies the §7 mechanical gate but NOT the §6 "real Tolkien chapter" residual-risk mitigation. Add a note that if PATH B is used, the §6 mitigation is only partially addressed and should be flagged in the Phase-3 hard-gate report.

**4b (Finding R2, LOW):** Soften the fixed-count adversarial framing in PG0.2-PC.3 prompts from "Assume at least N errors... Find them." to "Find any errors present (bias toward recall over precision)." This avoids priming QA reviewers toward false positives.

**4c (Finding F2, spec-author note — NOT a tasklist edit):** Open a separate spec-issue note (or PR against DESIGN.md) recommending §5 #1 remove "analyst" from the active_tier recipient list, since §3.2 + agent-schemas §2.1 establish analyst as tier-invariant. This is OUT OF SCOPE for the tasklist (the tasklist already resolves the tension correctly).

## Post-Completion Actions

- After Steps 1-3 (blocking fixes) are applied, the driving tasklist `TASK-RF-laf-hybrid-build-20260703-115948.md` is execution-ready.
- Re-run the PRE reflect gate (optional) to confirm the 3 blocking findings are resolved and status flips to `success`. Command: `Skill sc-reflect-protocol` with `--mode pre --spec .dev/releases/current/0.1/design/DESIGN.md --tasklist .dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md --depth standard`.
- Then proceed to execute the (now-remediated) parent task.

## Task Log / Notes 📋

### Task Summary
**Completion Date:** [YYYY-MM-DD]
**Work Completed:**
- [3 blocking fixes applied to parent tasklist]
**Challenges Encountered:** None anticipated (prescriptive edits)
**Deviations from Process:** None
**Blockers Logged:** None
**Follow-Up Required:** Yes — re-run PRE reflect gate to confirm status flips to success.

### Execution Log
<!-- TEMPLATE: **[YYYY-MM-DD HH:MM]** - [Action]: [description] -->
**[2026-07-03 19:48]** - Remediation task authored by sc:reflect PRE gate (run_id pre-20260703192947-793c0654). NOT yet executed — reflect authors but does not run /task per the protocol's "Will Not" invariant.
