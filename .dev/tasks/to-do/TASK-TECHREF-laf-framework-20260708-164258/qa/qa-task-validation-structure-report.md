# QA Report — Task Integrity (Phase Structure Lens)

**Topic:** LAF Adaptation Framework Technical Reference
**Date:** 2026-07-08
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: FAIL

## Phase Structure Checklist — Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1a | Frontmatter well-formed + `reflect_post_mode: skill` present | PASS | Line 28 `reflect_post_mode: skill`. Frontmatter parses; all core fields (id/title/status/type/created_date) present. |
| 1b | `start_commit` / `executor_model_class` ABSENT (skill mode) | PASS | Grepped full frontmatter (lines 1-58); neither key present. Matches SKILL.md L2312 "skill ⇒ frontmatter MUST carry NEITHER". Not a hybrid. |
| 2 | All mandatory sections present (Overview, Objectives, Prereqs, Exec Context, phases, Task Log) | PASS | Task Overview (L62), Key Objectives (L70), Prerequisites & Dependencies (L79), Execution Context (L95), Phases 1-7, Task Log / Notes (L383). |
| 3 | Phase dependencies logical, no circular/missing | PASS | research (P2) → research-gate (P3) → web (P4) → synth+gate (P5) → assembly+lens QA+fidelity (P6) → present+complete (P7). Gate 4 explicitly after Gate 3 (L285). No cycles. |
| 4 | Phase ordering follows tech-reference pipeline | PASS | P1 Prep → P2 Investigation (6 agents) → P3 Research Gate → P4 Web (conditional) → P5 Synthesis+Gate → P6 Assembly+Lens QA(Gate3)+Fidelity(Gate4) → P7 Present+Complete. Exact match. |
| 5 | Completion items INSIDE Phase 7 (anti-orphaning), no separate Post-Completion section | PASS | L361 ANTI-ORPHANING note; Steps 7.1-7.5 (verify outputs, present, Task Log summary, POST reflect, status→Done) all inside Phase 7. No orphaned Post-Completion section. |
| 6 | Task Log section present at bottom | PASS | `## Task Log / Notes 📋` at L383 with Task Summary, Execution Log, per-phase Findings, Phase Gate Findings, Follow-Up, Deviations, Builder Notes. |
| 7 | QA gates follow MDTM M3 (parallel report-only → consolidate → single fix → verify); agent counts | PASS | P3 gate = 3 report agents (3.1 rf-analyst, 3.2 rf-qa, 3.3 rf-qa-qualitative). P5 gate = 3 (5.6/5.7/5.8) → 1 serialized fix (5.10). P6 Gate 3 = 7 lens (6.2-6.8) → 1 fix (6.10). P6 Gate 4 = 2 rf-qa (6.13/6.14). All fix agents singular + serialized. |
| 8 | POST reflect item is PENULTIMATE + dedicated-subagent-runner (Skill-tool) form | **FAIL** | Step 7.4 is penultimate (before 7.5 status→Done) ✓ BUT it is NOT the dedicated-subagent-runner form — it is a hand-rolled/direct-audit form. See CRITICAL finding #1. |
| 9 | Open Questions / remaining gaps documented if any | PARTIAL | Builder Notes (L455-461) document build assumptions; no `### Open Questions` heading exists, though Step 7.4 references appending to "### Open Questions" — see finding #4. Follow-Up Items section present (L438). |

## CRITICAL Finding #1 — Step 7.4 POST reflect item is MALFORMED (wrong form)

Primary lens focus (Checklist item 8); FAILS against the authoritative SKILL.md skill-arm contract.

**What the contract requires** (SKILL.md Rule 20 skill arm L2371; validation checklist L2310; canonical runner item L2217-2233):
- The executor spawns EXACTLY ONE subagent that **invokes `sc-reflect-protocol` via the Skill tool** and runs it end-to-end.
- The subagent MUST be passed the **COMPLETE VERBATIM runner prompt** (L2221-2229), whose first instruction is: *"You MUST run the actual skill via the Skill tool; you must NOT hand-roll, paraphrase, simulate, or partially run a reflection of your own."*
- The item MUST carry the hard **completion contract** ("a verdict was recorded does NOT satisfy this job") and require a **waves-attestation**.
- Checklist L2310 declares MALFORMED "if it uses the direct-self-run form ... if the embedded runner prompt is paraphrased or abbreviated rather than the full verbatim block, if it lacks the completion contract."

**What Step 7.4 actually does** (task file L377):
- The embedded prompt instructs the subagent to *"Perform a POST-execution reflection (UC-2 deviation audit)... read the task file... audit whether the completed work adheres... Classify every divergence under the 4-category deviation taxonomy... Return a structured verdict of PASS... or FLAGGED."*
- This is a **hand-rolled / self-run audit** — the subagent conducts the reflection ITSELF. It NEVER invokes the Skill tool, NEVER runs `sc-reflect-protocol`; there is no reviewer ensemble, no blind calibration, no adversarial merge, no evidence-validator gate.
- There is **no completion contract** ("verdict recorded is insufficient" clause absent) and **no waves-attestation** requirement.
- The verbatim runner block (L2221-2229) is entirely absent — replaced by a paraphrased custom audit prompt.

**Severity: CRITICAL.** Per Rule 20 this is explicitly "a MALFORMED output." The gate's executor-independence guarantee is defeated: instead of a fresh instance orchestrating the full `sc-reflect-protocol` pipeline, a single subagent produces a subjective one-shot audit — the precise failure mode Rule 20 exists to prevent.

**Required fix:** Replace the Step 7.4 embedded prompt with the COMPLETE VERBATIM dedicated-subagent-runner block from SKILL.md L2221-2229 (resolve `{TASK_FILE}`, `{BASE}`, `{DEPTH}`, `{OUTPUT_DIR}`; OMIT `[--spec {SPEC_PATH}]` since spec_path is empty — finding #4; NO `--executor-model`). The Action must direct the executor to spawn the subagent via the Agent tool passing that verbatim block; the item must carry the completion contract + EV-3 on-disk verification + waves-attestation.

