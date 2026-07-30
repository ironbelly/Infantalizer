# QA Report — Phase-Gate (Phase 3: wire chapter-materialize into prep spine)

**Topic:** Wire the `chapter-materialize` skill into the prep spine (agent + skill + command)
**Date:** 2026-07-09
**Phase:** phase-gate (structural: edit-conformance + numbering-stability)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Lens:** edit-conformance + numbering-stability (structural)
**Adversarial stance:** Assumed ≥5 errors; searched for them.

---

## Overall Verdict: FAIL

Two genuine defects found — one broken cross-reference introduced by the edit, one stale
stage-count restatement the edit failed to update. Both are within the numbering-stability /
edit-conformance lens. The core edits are otherwise correct, additive, and byte-stable.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | skills block: `- laf-adaptation:chapter-materialize` present, additive, 2-space indent matching siblings | PASS | `cat -A` of lines 5–16: line 12 `  - laf-adaptation:chapter-materialize$` — identical 2-space `  - ` indent to the 6 sibling lines (6–11); the other 6 lines unchanged (git diff shows a single `+` line insertion after `thematic-fidelity`). |
| 2 | STAGE 0 MATERIALIZE is FIRST in the fenced block; STAGE 1–8 byte-identical; Q-gate still STAGE 5, greenlight still STAGE 7 | PASS | `grep '^STAGE'`: order is 0,1,2,3,4,5,6,7,8 (lines 49→68). `STAGE 5 Q-GATE`, `STAGE 7 GREENLIGHT` intact. Byte-diff of `git show HEAD:` STAGE 1–8 lines + fenced continuation lines (STAGE-0 block removed) vs working tree: IDENTICAL. No renumber, no reword. |
| 3 | Stage-count prose updated for AGENT pipeline; SKILL §-count "8-section procedure" preserved as 8 | PASS | Heading `## The 9 stages` (was `## The 8 stages`); intro `Owns the 9-stage prep pipeline (STAGE 0 + the 8 below)` (was `8-stage`). `execute its 8-section procedure` still reads **8** (line 26) — correctly preserved (refers to prep SKILL §1–§8). |
| 4 | All six 3.1 sub-edits present | PASS | (a) skills line ✓ L12; (b) STAGE 0 fenced entry ✓ L49–53; (c) count prose ✓ L21/L26/L46 heading; (d) Stage 0 note bullet ✓ L73–82; (e) STAGE 5 note "also receives … Stage-0 `ambiguous_splits`" ✓ L99–101; (f) STAGE 7 note w/ greenlight checklist line + deferred commit + `PENDING → CONFIRMED` ✓ L110–114. |
| 5 | prep/SKILL.md: "8 fixed-name files 00–70" UNCHANGED; Stage-0 note additive, sidecar (not 9th file, not rewrite_phase_reads); Resources bullet → chapter-materialize; §1–§8 labels unchanged | PASS | L19 "8 fixed-name files `00`–`70`" unchanged. Note L21–26 says manifest is a `source/` **sidecar** — "NOT a 9th package file and NOT a `rewrite_phase_reads` member". Resources bullet ✓ L133–135. §-headers grep: §1..§8 all present, unchanged labels. |
| 6 | command: argument-hint gains `[--source-mode auto\|folder\|file\|adopt]` w/ `<path-or-url>` verbatim; body documents --source-mode + dir/file/adopt; still delegates to prep-cordinator; no pipeline stages / literal package paths restated | **FAIL** | argument-hint ✓ (L3, `<path-or-url>` verbatim). Body §--source-mode + Mode A/B/C ✓ (L22–27). Delegates to prep-cordinator ✓ (L8). **BUT** body L11 restates a stage-count: "owns the **8-stage** procedure" — now stale (coordinator is 9-stage) AND violates the "no pipeline stages restated" constraint. See Issue #2. |
| 7 | No adopted file touched; all three NATIVE/canonical | PASS | VENDOR.md L121: `prep-cordinator.md \| NATIVE`. prep skill + command are not in the adopted/hash-pinned set (Rule-F glob covers only adopted `agents/*.md` + `skills/**/SKILL.md` bodies; these are native/command). `git diff --name-only`: only the 3 target files (+ pre-existing unrelated repo changes: Books/, work/, config/narnia — not part of this edit). |
| 8 | (adversarial) Cross-reference integrity of newly-introduced pointers | **FAIL** | prep-cordinator Stage-0 note L82 asserts "Chapter paths and the manifest path are owned by **path-contract §5/§6**." path-contract.md tops out at **§5 (Write-ownership)**; **§6 does not exist** (grep count 0), and `chapter-manifest` / `ch-<NN>` / `source/<slug>` appear **nowhere** in path-contract.md. Dangling reference. See Issue #1. |

---

## Summary

- Checks passed: 6 / 8
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `laf-adaptation/agents/prep-cordinator.md:82` (Stage 0 note) | The note states chapter/manifest paths are "owned by path-contract §5/§6", but `path-contract.md` has **no §6** (it ends at §5 = Write-ownership), and defines **no** `chapter-manifest.yaml` / `source/<slug>/ch-<NN>.txt` path at all. This is a broken §-cross-reference introduced by this edit — the SKILL.md §1 note (correctly) says the manifest is a `source/` sidecar and the coordinator note tells authors "never restate them here", deferring path ownership to a contract section that doesn't exist. The companion path-contract.md edit that should define these paths (a §6, or an extension of §1/§5) was not made. | Either (a) add a `## 6. Source materialization paths (Stage 0)` section to `path-contract.md` defining `source/<slug>/ch-<NN>.txt`, `source/<slug>/.raw/`, and `source/<slug>/chapter-manifest.yaml`, then keep the §5/§6 pointer; OR (b) if path ownership is intentionally deferred to the `chapter-materialize` skill, change L82 to point at that skill's path section instead of "path-contract §5/§6". Do not leave a pointer to a non-existent §6. **NOTE:** the fix lives in `path-contract.md`, which is outside this task's 3-file EDITED set — tag `[OUT-OF-SCOPE for in-place fix]`; the broken *pointer* itself is in-scope (introduced by the prep-cordinator edit). |
| 2 | IMPORTANT | `.claude/commands/laf/prep.md:11` | Body still reads "The `prep-cordinator` owns the **8-stage** procedure…". The coordinator was renumbered to a **9-stage** pipeline in this same edit (STAGE 0 prepended). This is (a) a stale count and (b) a restatement of a pipeline stage-count, which criterion 6 explicitly disallows ("no pipeline stages … restated"). Numbering drift between command and agent. | Change "owns the 8-stage procedure" to "owns the 9-stage procedure" to match the coordinator; OR, preferably per the "don't restate pipeline" rule, reword to a count-free form (e.g., "owns the prep pipeline and the two HALT gates"). This file IS in the EDITED set, so the fix is in-scope. |

---

## Actions Taken

None. `fix_authorization: false` — report-only mode. Both issues documented with specific
locations and required fixes above.

---

## Adversarial self-audit

If I told the user I found 0 issues, would they believe me? No — and they'd be right not to.
I can cite exactly what I checked: `grep -oE '^## [0-9]+\.' path-contract.md | tail -1` returns
`## 5.` and `grep -cE '§6|## 6\.' path-contract.md` returns `0`, proving the §6 pointer at
prep-cordinator.md:82 is dangling. `grep -n '8-stage' .claude/commands/laf/prep.md` returns
L11, proving the command's stage-count is stale against the coordinator's new `## The 9 stages`.
The STAGE 1–8 byte-identity claim is backed by a `diff` of `git show HEAD:` vs working tree that
returned no differences after excluding the STAGE-0 insertion.

## Confidence

Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 4 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 8

(Tool-call count ≥ 8 checklist items — not padding: each Bash call targeted a specific
check — skills-indent `cat -A`, STAGE grep, byte-diff, path-contract section scan, VENDOR.md
provenance, chapter-materialize existence, §6-absence count. No web research performed; Tavily
line N/A.)

## Recommendations

1. Fix Issue #2 in-place in the command file (in-scope): correct/remove the "8-stage" count.
2. Escalate Issue #1: the Phase-3 edit set is incomplete — `path-contract.md` needs a companion
   edit defining the Stage-0 `source/<slug>/` paths, otherwise the prep-cordinator's §5/§6
   pointer stays broken. Do not merge Phase 3 until the pointer resolves to real content.
3. Everything else (skills wiring, STAGE-0 insertion, byte-stability of STAGE 1–8, SKILL.md
   sidecar note, §1–§8 preservation, adopted-body untouched) is correct and additive.

## QA Complete
