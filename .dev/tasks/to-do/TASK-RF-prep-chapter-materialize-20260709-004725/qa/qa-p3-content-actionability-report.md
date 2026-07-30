# QA Report — Phase-3 Content (task-qualitative)

**Topic:** prep chapter-materialize wiring — Stage-0 materialization threading through prep-cordinator / prep SKILL / laf:prep command
**Date:** 2026-07-09
**Phase:** task-qualitative (phase-gate content, Phase 3)
**Lens:** actionability
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Overall Verdict: FAIL

One IMPORTANT contradiction between two edited files (stage-count: command says "8-stage" while the coordinator now owns a "9-stage" pipeline with a prepended STAGE 0). Actionable in every other respect. Per the standing rule (any issue of any severity = FAIL), the verdict is FAIL with a single, low-effort remediation.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | STAGE 0 fenced entry + Stage-0 note give concrete ordered actions (decl ABORT-first → detect mode → dispatch inline plan/no-writes → commit CERTAIN → defer PROBABLE/UNCERTAIN) | AX-1 | PASS | prep-cordinator.md:49-53 (fenced STAGE 0) + 73-82 (Stage-0 note). Ordered verbs: "run … ABORT-on-NO-ACCESS FIRST; detect input mode; dispatch … for a boundary/normalization PLAN with NO writes; commit CERTAIN …; defer PROBABLE/UNCERTAIN … as ambiguous_splits". Maps 1:1 onto chapter-materialize SKILL.md Stages 0.1→0.5 (SKILL.md:26-109). No vague step. |
| 2 | "dispatch chapter-materialize inline (executed in the coordinator's context)" is unambiguously an inline skill load, NOT a forked Agent | AX-2 | PASS | prep-cordinator.md:52 ("inline, in this coordinator's context") + 73-74 ("dispatch the `chapter-materialize` skill *inline* (executed in this coordinator's own context, not a forked agent)"). Corroborated by chapter-materialize SKILL.md:20 ("a procedure executed by the model inline in the `prep-cordinator`'s context … adds no script"). Contrast is explicit against `Agent(web-researcher, analyst, tier-coordinator)` in frontmatter tools (prep-cordinator.md:14). No contradiction. |
| 3 | STAGE 5 / STAGE 7 extensions tell the coordinator exactly what to do | AX-3 | PASS | STAGE 5 note prep-cordinator.md:97-101 ("also receives the Stage-0 `ambiguous_splits` … folded into the same coverage-constrained question block — no new gate or HALT machinery"). STAGE 7 note :110-114 (greenlight checklist gains the ratification line; "commits the deferred `ch-NN.txt` writes"; "sets `chapter-manifest.review.status: PENDING → CONFIRMED`"). Matches chapter-materialize Stage 0.5 (SKILL.md:104-109) in intent. All concrete. |
| 4 | Command `--source-mode` doc tells the operator exactly what the flag does | AX-1 | PASS | prep.md:22-27: values `auto|folder|file|adopt`, "NEW, optional, default `auto`", "operator override for when auto-detect is ambiguous; on ambiguity `auto` raises a mode question at the gate rather than guessing". Matches chapter-materialize Stage 0.2 precedence + "`--source-mode` operator override is honored here" (SKILL.md:42-61). argument-hint frontmatter (prep.md:3) lists the same 4 values. |
| 5 | No aspirational/vague verbs; no dangling reference | none | PASS | Verbs across all four edited files are imperative-concrete (run, detect, dispatch, commit, defer, fold, write, set). Every cross-reference resolves: "path-contract §5/§6" → path-contract.md §5 exists (:76-91); "chapter-materialize skill" dir exists; "`resources/path-contract.md` §3" → path-contract.md §3 exists (:35-60); prep SKILL §1 Stage-0 note exists (SKILL.md:21-26); source-fidelity "Phase-0" exists (source-fidelity/SKILL.md:21). No "see the note below" with an absent note. |
| 6 | Stage-0-vs-Stage-1(b) "same discipline at two points" reconciliation reads clearly (not a trip-hazard contradiction) | AX-2 | PASS | prep-cordinator.md:79-82: "same discipline applied at two points (source reachability at ingest, then work-level analysis reachability) — not a contradiction." The two are genuinely distinct scopes (ingest-time file reachability in chapter-materialize Stage 0.1 vs work-level analysis reachability in §3 text track), so the reconciliation is factually correct, not hand-waving. |
| 7 | Stage-count consistency across the edited files (does the command correctly describe what the coordinator owns) | AX-2 | FAIL | prep-cordinator.md:21/27/46 consistently says "9-stage prep pipeline (STAGE 0 + the 8 below)" / "runs them as a 9-stage pipeline with a prepended STAGE 0" / "## The 9 stages". The EDITED command prep.md:11 still says "The `prep-cordinator` owns the **8-stage procedure**". Two edited files contradict on the stage count, and the command drops STAGE 0 from the ownership statement it makes about the coordinator. See Issue #1. |

<!-- axis vocabulary: {AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened-criteria, AX-5 invented-content, none}. FAIL rows carry AX-1..AX-5; PASS rows carry the surfaced axis or `none`. -->

## Summary
- Checks passed: 6 / 7
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)
- Axis lens status: drift-axis-inactive (no BUILD_REQUEST.GOAL verbatim in spawn prompt; AX-1 applied only in its citation-drift form — cross-references between edited files and referenced resources — not in its GOAL-paraphrase form)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `.claude/commands/laf/prep.md:11` (edited file) vs `laf-adaptation/agents/prep-cordinator.md:21,27,46` | Stage-count contradiction between two edited files. The command's prose (edited to add `--source-mode` and reference the Stage-0 note) still asserts the coordinator "owns the 8-stage procedure," while the coordinator now consistently describes a 9-stage pipeline (STAGE 0 + the 8 below) and owns STAGE 0. The command's ownership statement is stale: it undercounts the stages and omits STAGE 0 from what the coordinator owns. A model reading only the command to understand the coordinator's scope would form an incorrect mental model of the pipeline (no STAGE 0 in the count). Execution is NOT blocked — the command delegates the whole run to the coordinator, whose body is authoritative and internally self-consistent — which is why this is IMPORTANT, not CRITICAL. | In `.claude/commands/laf/prep.md:11`, change "owns the 8-stage procedure and the two HALT gates" to "owns the 9-stage procedure (STAGE 0 materialization + the 8 prep stages) and the two HALT gates" (or "owns the STAGE 0 + 8-stage procedure"). This aligns the command's ownership statement with prep-cordinator.md:21/27/46 and with the STAGE 0 wiring the same edit introduced. |

## Actions Taken
None. `fix_authorization: false` — report-only. Issue #1 is documented with an exact, one-line remediation above.

## Actionability Assessment (lens narrative)
The wiring IS executable by the orchestrator/model on all six requested verification points:

1. **STAGE 0 fenced entry + Stage-0 note** give the coordinator a concrete, ordered action sequence with no vague step — declaration ABORT-first, mode detect, inline dispatch for a plan (no writes), commit CERTAIN + PENDING manifest, defer PROBABLE/UNCERTAIN. Each action has a concrete target and a concrete gate. (Check 1 — PASS.)
2. **"dispatch chapter-materialize inline (executed in the coordinator's context)"** is unambiguous: two independent statements in the coordinator + one in the skill all confirm inline skill-load, explicitly "not a forked agent," and the frontmatter's `Agent(...)` list (which does not include chapter-materialize) reinforces the distinction. (Check 2 — PASS.)
3. **STAGE 5 / STAGE 7 extensions** are fully actionable: fold ambiguous_splits + needs_human_review into the existing coverage-constrained question block (no new gate), add the greenlight ratification checklist line, commit deferred writes on CONFIRM, set manifest review.status → CONFIRMED. These match chapter-materialize Stage 0.5 exactly. (Check 3 — PASS.)
4. **`--source-mode` doc** tells the operator precisely what the flag does: override auto-detect, default `auto`, ambiguity raises a mode question at the gate. Values match the skill's detection precedence. (Check 4 — PASS.)
5. **No aspirational/vague verbs; no dangling references** — every §-cross-reference resolves to an existing file/section (path-contract §3/§5, chapter-materialize skill, prep SKILL §1 note, source-fidelity Phase-0). (Check 5 — PASS.)
6. **Stage-0-vs-Stage-1(b) reconciliation** reads as a correct two-scope framing, not a contradiction a model would trip on. (Check 6 — PASS.)

The one defect (Check 7) is a documentation-consistency contradiction between two of the edited files, not an executability blocker. It is nonetheless a real, edit-introduced staleness: the same commit that threaded STAGE 0 through the coordinator left the command's stage-count and ownership statement describing the pre-STAGE-0 world.

## Adversarial-axes note
- **AX-1 (drift, citation form):** all cross-references from the edited files to their referenced resources (path-contract, chapter-materialize, source-fidelity, prep SKILL) were checked and resolve — no stale citation. The one drift-adjacent finding (stale "8-stage" count in the command) is classified AX-2 because it is a mutual contradiction between two artifacts about the same subject, which is the more-specific axis. Drift-axis GOAL-paraphrase form is INACTIVE (no BUILD_REQUEST.GOAL verbatim available).
- **AX-2 (contradictions):** one fired (Issue #1). The other two AX-2 candidates (inline-vs-fork, same-discipline-at-two-points) were checked and are NOT contradictions.
- **AX-3 (omissions):** STAGE 5/7 touchpoints (ambiguous_splits routing, deferred-write commit, manifest status flip, greenlight checklist line) are all present — no omission.
- **AX-4 (weakened-criteria):** the deferred-write safety invariant ("no ch-NN.txt for a PROBABLE/UNCERTAIN boundary committed before human resolves it") and the ABORT-on-NO-ACCESS gate are stated unconditionally in both the coordinator and the skill — not softened.
- **AX-5 (invented-content):** every named artifact (chapter-manifest.yaml, ambiguous_splits, ch-NN.txt, source/<slug>/.raw/, the two promotion targets, --source-mode) traces to chapter-materialize SKILL.md and/or path-contract.md — nothing invented.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was present in the spawn prompt. Standalone behavior applied: no structural PASS items were relied upon; all findings below rest on my own tool engagement.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Stage-count contradiction (Issue #1) — verified by `grep -rn "8-stage\|9-stage"` across the three prose files (prep-cordinator.md:21/27/46 = "9-stage"; prep.md:11 = "8-stage"). Tool: Bash grep. This is the load-bearing finding and required my own tool work, not reliance on any structural verdict.
- Inline-dispatch claim (Check 2) — verified by Read of prep-cordinator.md:52,73-74 AND chapter-materialize SKILL.md:20; cross-checked against the frontmatter `Agent(...)` tools list (prep-cordinator.md:14) to confirm chapter-materialize is NOT among the forked agents. Tool: Read.
- Cross-reference resolution (Check 5) — verified each cited §/resource exists via Read of path-contract.md (§3 at :35-60, §5 at :76-91) and source-fidelity/SKILL.md (Phase 0 at :21). Tool: Read + Bash grep.

**Self-Audit answers:**
1. Factual claims independently verified against source: 7 (each checklist row) + the 4 referenced-resource existence/section checks = ~11 discrete verifications.
2. Files read to verify claims: `laf-adaptation/agents/prep-cordinator.md`, `laf-adaptation/skills/prep/SKILL.md`, `.claude/commands/laf/prep.md`, `laf-adaptation/skills/prep/resources/path-contract.md`, `laf-adaptation/skills/chapter-materialize/SKILL.md`, `laf-adaptation/skills/source-fidelity/SKILL.md` (grep).
3. Trust basis: I did not return 0 issues — I surfaced a real edit-introduced contradiction (Issue #1) provable by a one-line grep any reviewer can rerun, and I checked the two other plausible contradiction candidates and cleared them with cited evidence.
4. No open-web research was required (all verification was local-file-bound); Tavily-first rule not triggered this review.

## Confidence Gate
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 2 (Bash) | Glob: 0 | Bash: 3
- No UNCHECKED items. No UNVERIFIABLE items. Tool-call count (11) ≥ checklist item count (7): not suspect.

## Recommendations
- Apply Issue #1's one-line fix to `.claude/commands/laf/prep.md:11` (align stage count to 9 / STAGE 0 + 8), then this gate passes. No other changes required — the STAGE 0/5/7 wiring and the `--source-mode` doc are executable as written.

## QA Complete

