# QA Report — doc-qualitative (ACTIONABILITY lens)

**Topic:** laf-adaptation/ contributor-facing framework docs
**Date:** 2026-07-04
**Phase:** doc-qualitative
**Fix cycle:** N/A
**Fix authorization:** FALSE — report only
**Lens:** ACTIONABILITY (adversarial, zero-trust; assumed ≥10 gaps)

**Scope:**
- `laf-adaptation/CLAUDE.md`
- `laf-adaptation/VENDOR.md`
- `laf-adaptation/UPSTREAM-SYNC.md`
- `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/phase-outputs/reports/phase-3-hard-gate-report.md`

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | New contributor can unambiguously classify ANY file | FAIL | §1 table + non-manifested note read; 3 hypotheticals run — Hypo-2 (new adopted-tree resource) and Hypo-3 (source/) are ambiguous |
| 2 | VENDOR.md + UPSTREAM-SYNC.md give EXECUTABLE commands | PASS (with gaps) | `check_boundary.py --help` confirms `--init/--report/--upstream/verify`; hook path + CI verified; 6-step procedure maps to real flags. Gaps noted below are actionability polish, not broken commands |
| 3 | Boundary-contract note tells contributor what to do if they must edit an adopted file | PASS | CLAUDE.md:27, :34 "STOP. Add a skill instead" present and actionable |
| 4 | Phase-3 hard-gate RED path is actionable (names failing condition + remediation) | PASS | report:36-40 D8-equivalent failure paragraph names cond-2/cond-5 remediations |

## Summary
- Checks passed: 2 / 4 fully (Checks 3, 4); Check 2 passes with actionability gaps; Check 1 FAILS
- Checks failed: 1 fully (Check 1), plus material actionability gaps elsewhere
- Critical issues: 0
- Important issues: see table
- Minor issues: see table
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | CLAUDE.md:132 vs filesystem | **Contradicted state: `source/` is documented as absent but is present.** Line 132 says `source/` is "created when the first work is adapted (later phase; not present at Phase 0)". But `source/README.md` and `source/tolkien/ch-01.txt` both exist NOW (the proof fixture the hard-gate report:22-23 depends on). A contributor classifying `source/tolkien/ch-01.txt` reads two conflicting statements: §1 L48 says `source/` = BUILD-NEW (so classify it), L132 says it doesn't exist yet (so ignore it). Unactionable — the doc's Phase-0 framing no longer matches the completed tree it now lives in. | Update L132 (and the L118-137 tree, L30-33 Phase-0 present-state note, L124-126) to describe the COMPLETED tree state, since the hard gate declares "0.1 is DONE" (report:44). Or add one line: "As of 0.1-done, `source/tolkien/ch-01.txt` (synthetic proof fixture) is present; classify as BUILD-NEW." |
| 2 | IMPORTANT | CLAUDE.md:36-53 (non-manifested note) | **Classification ambiguity for a NEW file added under an ADOPTED tree (Hypo-2).** A contributor who adds `skills/creative-writing-craft/resources/genre/scifi.md` (a brand-new genre resource, sibling to the 6 adopted genre files at VENDOR.md:36-41) has no rule that fits. §1 says ADOPTED = "vendored verbatim from upstream" — but this file is NOT in upstream. It's a new file inside an adopted skill's `resources/` tree. It is not agents/*.md or skills/**/SKILL.md, so Rule-F doesn't hash-pin it (CLAUDE.md:37-38), and the non-manifested list (L41-50) enumerates `scripts/`, `kb/…`, `templates/`, `source/`, `NOTICE/LICENSE`, and the 3 docs — but says nothing about "new files inside an adopted skill dir." Result: unclassifiable. | Add an explicit rule to the non-manifested note: "New files authored inside an ADOPTED skill's `resources/` tree are NATIVE additions and MUST NOT collide with an upstream filename (Rule E); they are not hash-pinned. Do not add new files to an adopted skill dir if a native skill would do (boundary contract)." |
| 3 | IMPORTANT | CLAUDE.md:118-137 (tree diagram) | **The primary orientation artifact (the tree) is written in aspirational Phase-0 tense, not current state.** The tree annotates `agents/` as "11 ADOPTED present now; +2 NATIVE +2 BUILD-NEW authored in Phases 1-2" and `skills/` as "12 ADOPTED present now; +3 NATIVE +1 BUILD-NEW". But the filesystem shows all 15 agents and 16 skills present now (verified: `ls agents/` = 15, `ls skills/` = 16). A new contributor reading the tree to orient themselves is told components are unwritten that in fact exist. Actionability failure: the map contradicts the territory. | Rewrite the tree + the L30-33 "Phase-0 present-state" note to reflect the completed 15-agent/16-skill tree. Keep the Phase-authoring history as a one-line footnote if desired, but the live counts must be current since 0.1 is done. |
| 4 | MINOR | CLAUDE.md:32 vs VENDOR.md:23-78 | **ADOPTED count is stated as "11 ADOPTED agents" but 10 are ADOPTED-CLEAN + 1 ADOPTED-PATCHED.** L32 "11 ADOPTED agents + 12 ADOPTED skills present now" folds `writer.md` (ADOPTED-PATCHED) into the ADOPTED count without distinguishing it. §1 treats ADOPTED-PATCHED as its own class (L23). A contributor counting adopted-clean files against the manifest (10 ADOPTED-CLEAN agent rows + 1 ADOPTED-PATCHED) hits an off-by-one. | Clarify: "11 adopted-provenance agents (10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED = writer.md)". |
| 5 | MINOR | UPSTREAM-SYNC.md:1-4 vs filesystem | **UPSTREAM-SYNC.md is described as "authored in Phase 4… present in the completed tree, not at Phase 0" (CLAUDE.md:124) but the file exists and is being read now.** Same aspirational-tense problem as #1/#3: the doc self-describes as not-yet-existing while existing. A contributor following CLAUDE.md:62's parenthetical "(authored in Phase 4; present in the completed tree)" is told the sync procedure may not be available yet — undermining trust that the 6-step procedure is executable today. | Drop the "authored in Phase 4 / not at Phase 0" hedges now that the tree is complete (report:44 "0.1 is DONE"). |
| 6 | IMPORTANT | UPSTREAM-SYNC.md:63-67 + report references to "11-step workflow" | **Step 6 tells the contributor to "Re-run the Phase-3 hard gate (the full 11-step workflow on a chapter…)" but the 11-step workflow is not documented anywhere a contributor can open.** grep for "11-step" across `laf-adaptation/` returns only UPSTREAM-SYNC.md itself and a stray mention in `agents/tier-coordinator.md` / `work/analysis/…` — no enumerated 11-step procedure exists in the shipped tree. A contributor cannot execute Step 6 without knowing the 11 steps. This is the single most action-blocking gap in the sync procedure: the final "re-prove before shipping" gate is unrunnable from the docs alone. | Either enumerate the 11-step workflow inline (or in a `WORKFLOW.md` shipped under `laf-adaptation/`), or replace the reference with the concrete re-run command(s) + the 5 gate conditions (which ARE listed at UPSTREAM-SYNC.md:64-66) so Step 6 is self-contained. |
| 7 | IMPORTANT | UPSTREAM-SYNC.md:4, :35; scripts/check_boundary.py comments; CLAUDE.md:105; hard-gate:8 | **Dangling references to design authorities that are NOT shipped in the contributor-facing tree.** UPSTREAM-SYNC.md:4 says it is "faithful to `boundary-contract.md §5`" and :35 cites `boundary-contract.md §3.2`; CLAUDE.md:105 cites "DESIGN §5"; hard-gate:8 cites "DESIGN.md §7 line 296". None of `boundary-contract.md` or `DESIGN.md` exist under `laf-adaptation/` — they live in `.dev/releases/current/0.1/design/DESIGN.md`, outside the shipped framework a contributor works in. A contributor told the sync procedure is "faithful to boundary-contract.md §5" cannot open that file to check faithfulness or resolve ambiguity. For a *contributor-facing* framework these are unactionable pointers. | Either (a) ship the relevant spec sections into `laf-adaptation/` (e.g., a `docs/` or inline appendix), or (b) make the doc self-contained so no external `.dev/` reference is load-bearing for a contributor action, or (c) explicitly state these are design-provenance references not required for day-to-day contribution. |
| 8 | MINOR | UPSTREAM-SYNC.md:14 (Step 1) | **Step 1 "Fetch upstream; pick new target SHA" gives no concrete command.** Steps 2/3/5 give runnable `check_boundary.py` invocations, but Step 1 is prose — no `git fetch`/`git checkout`/`git clone` of the upstream repo (whose URL is in VENDOR.md:3). The 6-step procedure was asked to be "executable"; Step 1 and Step 6 (see #6) are the two non-executable steps. | Add the concrete command, e.g. `git clone https://github.com/haowjy/creative-writing-skills <checkout>` (or `git fetch`), and note that `<checkout>` is the `--upstream DIR` passed to Steps 2/5. |
| 9 | MINOR | CLAUDE.md:12, VENDOR.md, UPSTREAM-SYNC.md | **ADR-006 is cited as the authority for "prompt + YAML-config, NOT software / one script only" (CLAUDE.md:12-14) but ADR-006 is not resolvable from the tree.** grep finds "ADR-006" only in CLAUDE.md and the script; no ADR file ships under `laf-adaptation/`. Lower impact than #7 because the rule it backs ("do not add other scripts or a CLI") is fully stated inline and actionable without opening the ADR. | Optional: drop the ADR-006 citation or ship an `ADRs/` note; the inline rule is sufficient, so this is polish only. |
| 10 | MINOR | phase-3-hard-gate-report.md:32-40 | **RED-path remediation is concrete for only 2 of the 5 gate conditions.** The failure paragraph names remediation for cond-2 (safety FAIL → re-dispatch writer at step 3) and cond-5 (boundary non-zero → revert offending adopted-body edit), plus the tier-coordinator CONFLICT path. But cond-1 (v2.0 tags missing), cond-3 (per-tier canon not written), and cond-4 (quartet didn't all run) get NO named remediation — the paragraph relies on a general "the gate HALTs, names the failing condition, and routes to its remediation" (report:34) with "e.g." illustrative examples. An operator hitting a cond-3 RED has to infer the fix. The check ("names the failing condition + remediation") is met for the illustrated conditions but not exhaustively. | Add one-line remediations for cond-1 (→ re-run analyst / restore ABORT-on-NO-ACCESS discipline), cond-3 (→ re-dispatch chronicler per-tier write), cond-4 (→ re-dispatch the missing quartet agent), so all 5 conditions have a concrete RED-path route. |

### Positive verifications (what IS actionable — not padding)
- **Check 3 fully PASSES.** CLAUDE.md:27 and :34 give the exact contributor action when tempted to edit an adopted file: "STOP. Add a skill instead" + attach via `skills:` frontmatter. The `writer.md` demonstration (CLAUDE.md:64-67) shows the pattern concretely. Unambiguous and actionable.
- **All `check_boundary.py` invocations in the docs are EXECUTABLE and correct.** Verified against `--help`: `--init`, `--report`, `--upstream DIR`, and default verify mode all exist; `--init` requires `--upstream` (script:225, 439-440). The commands at VENDOR.md:15-16, UPSTREAM-SYNC.md:56-58, CLAUDE.md:68/100 all run as written.
- **The hook-enable command is correct and disambiguated.** CLAUDE.md:73 `git config core.hooksPath laf-adaptation/.githooks`; the hook itself (.githooks/pre-commit:6-7) documents both the subdir and git-root cases; `git commit --no-verify` bypass stated. Hook file exists and is executable (`-rwxr-xr-x`).
- **CI location claim is accurate.** CLAUDE.md:75-77 says the workflow lives at repo root `.github/workflows/boundary.yml` with `working-directory: laf-adaptation` — verified: file exists at `/config/workspace/Infantalizer/.github/workflows/boundary.yml` with `working-directory: laf-adaptation` (boundary.yml:26).
- **Hypo-1 classifies cleanly.** `kb/adaptations/tolkien/tier-1/` → CLAUDE.md:44 "NATIVE graft G1." Unambiguous.

## Actions Taken
None — `fix_authorization: FALSE` (report-only). All 10 findings documented with file:line + concrete fix for the operator to apply.

## Self-Audit
1. **Factual claims independently verified against source:** 12+ — script existence, hook existence + perms, CI workflow existence + `working-directory`, `check_boundary.py --help` flag surface (`--init`/`--report`/`--upstream`/verify), `--init requires --upstream`, Rule-F glob patterns, present agent count (15) vs documented "11 present now", present skill count (16) vs "12 present now", `source/tolkien/ch-01.txt` presence vs CLAUDE.md:132 "not present at Phase 0", genre-resource manifest coverage, non-existence of `DESIGN.md`/`boundary-contract.md` under `laf-adaptation/`, "11-step workflow" undocumented, ADR-006 unresolvable.
2. **Specific files read/executed:** all 4 in-scope docs; `scripts/check_boundary.py` (grep + `--help` run); `.githooks/pre-commit`; `.github/workflows/boundary.yml`; directory listings of `agents/`, `skills/`, `source/`, `templates/`; grep sweeps across `laf-adaptation/`.
3. **Why trust this found real issues:** the review did NOT find zero issues — it found 10, of which 4 are IMPORTANT. Every finding cites a file:line AND a filesystem/`--help` verification that contradicts the doc. Findings #1/#3/#6/#7 are backed by direct filesystem evidence (files that exist while docs say absent; referenced docs that do not exist in the shipped tree). No finding rests on subjective judgment alone.
4. **Web research:** none performed — this review is entirely local-file-bound (no external vendor/standard lookup was required). Tavily-first precedence therefore did not trigger; no fallback occurred.

## Confidence Gate
- **Confidence:** Verified: 4/4 checks fully reasoned | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 5 | Grep: (within Bash) ~8 | Glob: 0 | Bash: 6
  - Tool-call count (>= checklist items) satisfied: 4 checks, 11+ verification tool invocations.
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
Before treating `laf-adaptation/` as contributor-ready:
1. **Resolve the aspirational-tense contradictions (#1, #3, #5).** The docs still describe the tree in Phase-0 "not yet present" language while the tree is complete and `0.1 is DONE`. This is the highest-frequency actionability defect — a new contributor's orientation map contradicts the filesystem. Sweep CLAUDE.md (tree L118-137, present-state note L30-33, L124-126, L132) and UPSTREAM-SYNC.md:1-4 to current-state tense.
2. **Close the two classification gaps (#1, #2)** so the "classify ANY file" guarantee (Check 1) actually holds: (a) `source/tolkien/ch-01.txt`, (b) a new file authored inside an ADOPTED skill's `resources/` tree.
3. **Make Step 6 self-contained (#6)** — the 11-step workflow it depends on is undocumented in the tree; inline it or point to the 5 gate conditions already listed.
4. **Decide the external-reference policy (#7)** — `DESIGN.md` / `boundary-contract.md` / `ADR-006` are load-bearing citations that a contributor cannot open from the shipped tree. Either ship them or make the docs self-contained.
5. Optional polish: #4 (count nuance), #8 (Step-1 git command), #9 (ADR citation), #10 (RED-path remediation for cond-1/3/4).

## QA Complete

