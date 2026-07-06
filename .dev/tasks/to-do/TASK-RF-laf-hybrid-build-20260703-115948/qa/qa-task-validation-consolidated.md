# QA Task-Validation — Consolidated Findings (A.10)

**Task file:** .dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md
**Round:** 1 (initial structural validation: B2 + phase-structure lenses)

---

## Items Reviewed

| Check / Item | Source lens | Verdict |
|---|---|---|
| B2 self-containment (all 9 checks) | b2-self-containment | PASS |
| Vendoring enumeration (23 adopted files = distinct items) | b2-self-containment | PASS |
| kb port items (6 distinct byte-faithful carries, no tier_4) | b2-self-containment | PASS |
| QA gate prompts fully embedded | b2-self-containment | PASS |
| Frontmatter completeness + well-formed | phase-structure | PASS |
| Mandatory sections present | phase-structure | PASS |
| Phase dependency DAG (no cycles) | phase-structure | PASS |
| Build-phase ordering (vendor→native→greenfield→proof→sync) | phase-structure | PASS |
| Task-completion anti-orphaning | phase-structure | PASS |
| Task Log present | phase-structure | PASS |
| M3+M4 QA-gate sizing (gates 7/10/7/7, final 6 — all ≥ floors) | phase-structure | PASS |
| TB-Add-1 placeholder scan (0 TBD/TODO/FIXME) | phase-structure | PASS |
| TB-Add-4 DAG / no circular item refs | phase-structure | PASS |
| TB-Add-8 file:line evidence binding | phase-structure | PASS |
| Template heading-level conformance (`### Phase` under `## Detailed`) | phase-structure | PASS |
| Double-mapping clarity (each phase states its DESIGN §7 build-phase) | phase-structure | PASS |
| **F-1: Reflect skip-guard form** (line 521) | phase-structure | **CRITICAL FAIL** |
| **F-2: Handoff paths missing `to-do/` segment** (~100 items) | phase-structure | **CRITICAL FAIL** |
| **F-3: Reflect exit-2 treated as non-blocking** (line 521) | phase-structure | **IMPORTANT FAIL** |
| **F-4: QA report basename collisions PG0 vs PG1** (5 reports) | b2-self-containment | **IMPORTANT FAIL** |
| F-5: Vestigial empty `template:`/`tracks:` frontmatter | b2-self-containment | MINOR |
| F-6: Execution Context `### Source Areas` vs `**Source areas:**` | phase-structure | MINOR |

---

## Fixes to apply (serialized — single fix agent, all at once)

### F-1 (CRITICAL) — Reflect skip-guard form
**Location:** line 521, the POST reflect gate item's command.
**Problem:** Uses `if [ -n "$SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" ]` — the prohibited `-n "$VAR"` form.
**Fix:** Replace with the contract-mandated form: `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi` run BEFORE the reflect command (as the recursion-breaker skip guard), then `superclaude reflect run ".dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md" --depth deep --fix --promote`. The guard must be the `:-0 = "1"` env-var-equals-"1" form, byte-exact.

### F-2 (CRITICAL) — Handoff paths missing `to-do/` segment
**Location:** ~100 checklist items + the Handoff File Convention block (~line 138) reference `.dev/tasks/TASK-RF-.../phase-outputs/` and `.../qa/`.
**Problem:** The task physically lives at `.dev/tasks/to-do/TASK-RF-.../` (the reflect gate gets this right). 100 items use the wrong root; artifacts would detach from the task's lifecycle home.
**Fix:** Replace ALL occurrences of `.dev/tasks/TASK-RF-laf-hybrid-build-20260703-115948/` with `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/` throughout the file (the reflect item's path already correct — do not double-insert). This is a mechanical global replace. After fix: grep for `.dev/tasks/TASK-RF` (without to-do) MUST return 0 hits.

### F-3 (IMPORTANT) — Reflect exit-2 handling
**Location:** line 521, exit-code handling prose.
**Problem:** Treats exit code 2 (infra error) as "proceed, non-blocking", contradicting the gate contract (only 0 proceeds; 10/11/2 FAIL).
**Fix:** Rewrite the exit-code handling so that ONLY exit 0 proceeds to the status-update item; exit codes 10, 11, AND 2 all FAIL — write the reflect verdict + report path to `reflect_post` (per wrapper write-back), log the deviation/error in `### Phase Gate Findings`, and HALT (do NOT mark the task Done; escalate). An infra error (exit 2) is surfaced as a FAIL/escalation, not silently bypassed.

### F-4 (IMPORTANT) — QA report basename collisions (PG0 vs PG1)
**Location:** Phase Gate 0 and Phase Gate 1 QA-spawn items write reports to the same 5 basenames (e.g. `qa-structural-template-conformance-report.md`), so PG1 overwrites PG0's reports — durable Phase-0 evidence lost + misattribution risk. PG2/PG3 already use phase suffixes; PG0/PG1 do not.
**Fix:** Add a phase suffix to every QA report output path in Phase Gate 0 (`-phase0`) and Phase Gate 1 (`-phase1`) items — e.g. `qa-structural-template-conformance-report-phase0.md`. Apply consistently across all 7 PG0 lens agents and all 10 PG1 lens agents (and any consolidation/fix/verify items in those gates). PG2/PG3 already differ; leave them.

### F-5 (MINOR) — Vestigial frontmatter fields
**Problem:** Empty `template:` and `tracks:` frontmatter fields (leftover from template-01 schema; template 02 doesn't use them).
**Fix:** Remove the empty `template:` and `tracks:` lines from frontmatter.

### F-6 (MINOR) — Execution Context Source Areas form
**Problem:** `### Source Areas` (heading) vs the TB-Add-7-named `**Source areas:**` (bold-line) form. Content is present and reappears in items, so this is format-only.
**Fix:** Optional — change `### Source Areas` to a `**Source areas:**` bold line for TB-Add-7 form match. Low priority; do not block on this.

---

**Post-fix verification:** Re-grep the file for: (a) `.dev/tasks/TASK-RF` without `to-do` = 0 hits; (b) `-n "$SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` = 0 hits AND `"${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1"` present; (c) exit-2 now FAILs (not "proceed"); (d) PG0/PG1 report paths carry `-phase0`/`-phase1`; (e) no empty `template:`/`tracks:`.
