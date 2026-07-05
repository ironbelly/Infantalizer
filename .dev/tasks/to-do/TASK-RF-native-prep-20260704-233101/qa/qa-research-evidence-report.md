# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** LAF adaptation-prep phase (docs/native-prep/design/DESIGN.md)
**Date:** 2026-07-04
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false
**Assigned files:** 01–06 (all 6 research files) — single instance, full scope

---

## Overall Verdict: PASS

All six research files are densely evidence-based. Every claim carries a `file:line`, a real
command, or an explicit `[VERIFIED]/[UNVERIFIED]` tag. I spot-checked well over 20% of the cited
paths/line-numbers against the live repo and **independently re-ran both commands R6 claims to have
run** — every checked claim reproduced exactly, including verbatim command output. Zero fabrications,
zero unsupported assertions-as-fact, zero mis-cited line numbers found.

---

## Items Reviewed (evidence-quality lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Claims are evidence-based (file:line / real command) | PASS | Every table row in R1–R6 carries a `path:line`. R5 is a pure claim→verdict→`file:line` table. R6 pastes verbatim command output for every gate. |
| 2 | No unsupported assertions stated as fact | PASS | Speculative items are explicitly hedged: R3 Q2 ("Unverified whether the task intends to acquire an upstream checkout"), R5 §I Rule-E row tagged `[UNVERIFIED]`, R6 marks unrun items "Unverified". |
| 3a | VENDOR.md:111/113/117 (+60/65/64) | PASS | Read VENDOR.md directly. L111 `agents/analyst.md \| NATIVE \| — \| —`; L113 `skills/adaptation-rules/** \| NATIVE`; L117 `agents/tier-coordinator.md \| BUILD-NEW`; L60 muse ADOPTED-CLEAN `c8819ec8…/18cafdc2…`; L65 writer ADOPTED-PATCHED `373e605b…/c1b3e12f…`; L64 web-researcher ADOPTED-CLEAN `0219d3d2…/fe371680…`. **All exact.** |
| 3b | check_boundary.py classify() ~326-345 | PASS | classify() at 326-345 verbatim. `parts[0]=="agents"`→BUILD_NEW_AGENTS check (337) else NATIVE (339); `parts[0]=="skills"`→BUILD_NEW_SKILLS (342) else NATIVE (344). Matches R1 Q1 / R3 Q1 / R5 §B. |
| 3c | do_init early-return ~350-354 | PASS | Lines 350-354: `if not upstream_dir: print("ERROR: --init requires --upstream …") … return 2`. Second guard at 355-358 (cw/ subtree). Matches R3 Q2 exactly. |
| 3d | do_init skill else-branch 405-407 | PASS | Lines 405-407: `else: cls = classify(…SKILL.md…); rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))`. Matches R3 line 32-33 / R5 §B. |
| 3e | BUILD_NEW sets + NO_HASH | PASS | `BUILD_NEW_AGENTS = {"chronicler.md","tier-coordinator.md"}` (45); `BUILD_NEW_SKILLS = {"adaptation-safety"}` (47); `NO_HASH = "—"` (50). Matches R3/R5. |
| 3f | analyst.md edit anchors (18/21/23/33/34-39/51/52/54) | PASS | Read analyst.md in full (66 lines). L18 `## Inputs (passed by the caller)`; L19-21 source_path/work/chapter; L23 `**active_tier is NOT an input.**`; L33 `## Hard behavior…`; L34-39 Phase-0 fence (open 34, close 39); L37 `IF NO-ACCESS: emit status: ABORTED…HALT`; L51 `## Output contract`; L52 `Write work/analysis/ch-<NN>.yaml`; L54 lists `transformation_flags, uncertainties`. **All R1-E1/R5-§E anchors exact.** |
| 3g | tier-coordinator.md anchors (59/70/82/85-90/93/95/128/145-148/150/153-155) | PASS | Read directly. L59 Check A; L70 Check B; L82 `### Check C — Framing monotonicity`; Check C fence open 85/close 90; trailing prose 91-93; L95 `## Operational reading…` (boundary E2a must not cross); L128 `## Output report format`; L145 `## Checks`; L146-148 `- A/- B/- C`; L150 `status: RECONCILED`; L153-155 `On CONFLICT, conflicts:…`. **All R1-E2/R5-§F anchors exact.** |
| 3h | tolkien_mapping.yaml 5 keys @ L4/13/43/64/77 | PASS | `grep -nE '^[a-zA-Z_]+:'` → `4:work_metadata 13:characters 43:concepts 64:key_scenes 77:master_translation_table`. **Exact match to R2 §5.1 / R5 §C line refs.** |
| 3i | New-file ABSENCE claims | PASS | `.claude/commands/laf/` absent; `skills/prep/` absent; `skills/thematic-fidelity/` absent; `resources/exemplars/` absent but parent `resources/` present (agency/character/thematic.md). `.claude/commands/` exists-but-empty (matches R2:139). Matches R1 Cat-1 + Cat-1 caveat. |
| 3j | writer.md upstream-duplicate skill line | PASS | writer.md head shows `- laf-adaptation:creative-writing-craft` twice (L6-7). Confirms R1 U1 "carries the upstream duplicate…verbatim". |
| 3k | muse tools `>` folded Agent(...) form | PASS | muse.md:22-26 = `tools: >` + `Agent(writer, critic, …web-researcher), Read, Write, …`. Verbatim to R2 §1.4. |
| 4 | [CODE-CONTRADICTED]/[UNVERIFIED] properly flagged in R5 | PASS | R5 tags every checkable claim `[CODE-VERIFIED]`; the ONE non-code-checkable item (Rule E upstream-name collision) is correctly `[UNVERIFIED]` with a precise blocker ("cannot confirm absence in upstream CWS without an --upstream checkout") and a non-blocking rationale (Rule E upstream arm only runs under Mode U). Zero `[CODE-CONTRADICTED]` — I independently confirmed the underlying claims, so absence of contradictions is genuine, not overlooked. |
| 5 | R6 actually RAN boundary check + yaml validation (real output) | PASS | I **independently re-ran both** commands. `check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` exit 0 — byte-identical to R6:30-33. `uv run --with pyyaml … tolkien_mapping.yaml` → `['characters','concepts','key_scenes','master_translation_table','work_metadata']` exit 0 — byte-identical to R6:87. `--report` → NATIVE=5/ADOPTED-CLEAN=55/ADOPTED-PATCHED=1/BUILD-NEW=3/TOTAL=64 — exact to R6:50-54. `git diff --stat writer.md muse.md` → empty, exit 0 — matches R6 Gate 2. R6 RAN, did not assert. |
| 6 | R6 Narnia/Tolkien P3 mismatch flag is accurate | PASS | DESIGN.md:315 P3 names `"The Lion, the Witch and the Wardrobe"` + `/laf:rewrite --work narnia`. Repo ships only `source/tolkien/ch-01.txt`; `find … -iname '*narnia*'` → no results; `kb/adaptation-mapping/` has only tolkien + universal. R6's WORK-MISMATCH flag is a **correct, load-bearing finding** the task author must resolve. |
| 7 | Exemplar DERIVED marker source-of-truth | PASS | `package-schemas.md:267` = `<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->`. Byte-exact to R1:191 / R2:190 (both cite :267). |
| 8 | Status/Summary completeness per file | PASS | R1/R2/R4/R5/R6 marked `Status: Complete` with a Summary. **R3 header says `Status: In progress` (line 5) but its footer says `## Status: Complete` (line 204).** See Issues (MINOR). |

## Summary
- Checks passed: 8 / 8 lens checks (18 discrete sub-verifications, all PASS)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (R3 header/footer status inconsistency — cosmetic, does not affect evidence quality)
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence Gate
- **Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 5 (2 of which independently re-ran R6's exact commands)
- No web research required — all claims are repo-internal (source-truth-first). Tavily not invoked.
- Tool-call count (13 Read+Bash) ≥ 8 lens checks → engagement floor satisfied; each call targeted a specific cited claim, no padding.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 03-boundary-integration.md:5 vs :204 | Header declares `**Status:** In progress` but the file is fully populated (Q1–Q6 all resolved) and the footer declares `## Status: Complete`. The header status line was never updated after completion. | Change line 5 `**Status:** In progress` → `**Status:** Complete` for internal consistency. Evidence quality of R3's content is unaffected — all Q1–Q6 claims are `file:line`-cited and independently confirmed (classify 326-345, do_init 349-354/405-407, VENDOR rows). |

## Adversarial Self-Audit
I began from the assumption the research was wrong and actively hunted for: (a) mis-cited line
numbers, (b) claims of "ran a command" that were actually asserted, (c) fabricated file paths, (d)
doc-sourced claims presented as code-truth. I checked 18 distinct cited facts across all 6 files —
5 of them by executing commands, not just reading. **The only defect found is a one-word stale
status header in R3.** Could I be reporting a false PASS? To claim 0 substantive issues I can point
to: 8 direct Reads of cited source files, 5 Bash runs (2 reproducing R6's outputs verbatim), and
line-exact confirmation of every VENDOR row, classifier branch, and edit anchor the downstream task
builder will depend on. The evidence trail is real and independently reproducible.

## Recommendations
- **Proceed to synthesis / task-building.** The research pack is a trustworthy build spec on
  evidence-quality grounds. Every VENDOR line ref, classifier branch, edit anchor, schema key, and
  boundary-command baseline is exact and independently reproduced.
- **Carry R6's Narnia/Tolkien P3 mismatch into the task file** as a design-vs-repo gap the author
  must resolve (substitute Tolkien in the P3 gate, or add a "provision Narnia source+mapping"
  pre-step). This is a *correct research finding*, not a research defect — flagged here so it is not
  lost.
- Fix the one MINOR R3 status-header inconsistency at authoring time (non-blocking).

## QA Complete

VERDICT: PASS
