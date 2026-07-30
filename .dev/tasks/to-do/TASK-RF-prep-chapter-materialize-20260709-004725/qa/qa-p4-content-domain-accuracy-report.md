# QA Report — Phase-4 Content (doc-qualitative / domain-accuracy lens)

**Topic:** LAF prep chapter-materialize — Phase-4 content (VENDOR row, path-contract §12 deltas, source/README)
**Date:** 2026-07-09
**Phase:** doc-qualitative (lens: domain-accuracy)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: FAIL

One real domain-accuracy defect: the VENDOR.md manifest row count (now 68) contradicts the
`CLAUDE.md` claim of "64", and the edit under review touches the exact line that changed the count
(67 → 68). The defect's *fix* lives in `CLAUDE.md`, which is a GROUND-AGAINST reference, not one of the
three EDITED files — so it is tagged `[OUT-OF-SCOPE]` for in-place fixing, but per the "ANY issue = FAIL,
no severity exempt, contradictions are never minor" rule it drives the verdict to FAIL. Claims 1, 2, 3, 4,
and 6 are fully verified TRUE against source.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | VENDOR row form + placement (one `skills/<name>/**` glob, NATIVE auto-classified, no script edit) | PASS | VENDOR.md:124 has exactly one `\| skills/chapter-materialize/** \| NATIVE \| — \| — \|` row; disk has only 2 files (SKILL.md + resources/boundary-rules.yaml) both glob-covered; `classify()` (check_boundary.py:363-368) returns NATIVE by fall-through — chapter-materialize is NOT in `NATIVE_SKILLS`/`BUILD_NEW_SKILLS` and needs no script edit; `--init` emits exactly one `/**` row for non-adopted skills (check_boundary.py:411,428-430); Rule F glob-coverage at :322. Matches spec release-blocker #7. |
| 2 | path-contract §12 deltas faithfully realized | PASS | §1/§2 unchanged (8-file table intact, path-contract.md:22-33); §4 read-set still exactly 3 files (:67-70) + explicit source/sidecar-not-in-read-set note (:75-77); §5 +3 source-side rows present (:84-86); §6 NEW "Source-side chapter manifest" present (:100-117). All four §12 deltas realized; read-set byte-unchanged. |
| 3 | source/README read-only-after-materialize / new-files-only matches CLAUDE.md provenance + spec §8/§9 | PASS | source/README.md:20-22 "read-only-after-materialize: adds NEW files, never edits existing bodies" ≡ spec §8/§9 (:200-221) and §5 §6 write-ownership; CLAUDE.md:50,185 `source/`=BUILD-NEW; README assigns no conflicting provenance class to the manifest (describes it as a sidecar). `.raw/` + manifest correctly described as materialization outputs (none exist yet — hand-provisioned narnia/tolkien were Mode-C adopted, not materialized). No aspirational claim. |
| 4 | Mode-C zero-re-split adopt (narnia/tolkien untouched) TRUE against actual files | PASS | narnia/ch-01..04 carry real `CHAPTER I/II/III/IV` headings (validating Mode-C adopt precondition, chapter-materialize SKILL.md:47); tolkien/ch-01 is the ORIGINAL SYNTHETIC "The Siege at the Grey City" PATH-B fixture matching source/README:33-38 and `kb/adaptation-mapping/tolkien-mapping.yaml` (exists, 9445 B). narnia dir untracked (new, never re-split); no in-place body edits. Matches spec G5 / AC3. |
| 5 | No aspirational claim; nothing contradicting CLAUDE.md, boundary contract, or spec non-goals | FAIL | VENDOR.md now has 68 data rows (was 67 at HEAD; the edit added the chapter-materialize row → 68), but CLAUDE.md:68 asserts "VENDOR.md has more rows (64)". The edit widens a pre-existing CLAUDE.md staleness (already wrong at HEAD: 67≠64) by one. This is a stale-count contradiction between an EDITED file (VENDOR.md) and a GROUND-AGAINST doc (CLAUDE.md). All other sub-checks pass: no aspirational claims; boundary contract green; spec non-goals (N1-N4) respected (no 4th read-entry, no 9th package file, no second script, no adopted-body edit). |
| 6 | check_boundary.py exits 0 / PASS (boundary genuinely preserved, not asserted) | PASS | `cd laf-adaptation && uv run python scripts/check_boundary.py` → "BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.", exit code 0. Rule F/F′ coverage of chapter-materialize's resources/boundary-rules.yaml proven by the green run (an unmanifested resources file would FAIL loud). |

## Summary
- Checks passed: 5 / 6
- Checks failed: 1
- Critical issues: 0
- Important issues: 1 (contradiction — VENDOR row count vs CLAUDE.md "64")
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false; and the fix target is out-of-scope)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `CLAUDE.md:68` vs `VENDOR.md` manifest (68 rows) | `[OUT-OF-SCOPE]` CLAUDE.md states "VENDOR.md has more rows (64)"; actual manifest has 68 data rows. The Phase-4 VENDOR edit (adding `skills/chapter-materialize/**`) moved the count 67→68, widening a mismatch that was already stale at HEAD (67≠64). Contradiction between an edited file and a ground-truth doc. | Update `CLAUDE.md:68` parenthetical from "(64)" to "(68)" (the current true manifest data-row count). The "31" Rule-F glob-coverage-set number on the same line is correct and unaffected (adding a NATIVE glob row does not change the agents/*.md + skills/**/SKILL.md coverage set). NOT fixed here: CLAUDE.md is a GROUND-AGAINST reference outside the three EDITED files (path-contract.md, source/README.md, VENDOR.md) — tagged OUT-OF-SCOPE per the scope constraint. Refer to Phase-4 orchestrator to fold CLAUDE.md into the edit set or open a follow-up. |

## Actions Taken
None — `fix_authorization: false`, and the sole finding's fix target (`CLAUDE.md`) is out of the
edited-file scope for this phase.

## Notes on claim 1 (spec §11 "per-file" vs actual glob row) — verified NOT a defect
Spec §11 BOM (merged-requirements.md:238-239, 245) lists SKILL.md and resources/boundary-rules.yaml as
two NEW NATIVE rows / "+1 NATIVE row for chapter-materialize/SKILL.md". The actual VENDOR.md uses ONE
`skills/chapter-materialize/**` glob row. This is FAITHFUL, not a deviation: `check_boundary.py --init`
itself emits exactly one `/**` glob row for any non-adopted (NATIVE/BUILD-NEW) skill dir
(check_boundary.py:411 comment + :428-430), and Rule F glob-coverage (:322) covers all files beneath it.
The task's claim 1 correctly asserts the glob form is the right realization per Rule F/F′. The spec's
"per-file" phrasing described design intent; the machine-generated form is the single glob row, which the
green boundary run confirms is contract-valid.

## Self-Audit
1. **Factual claims independently verified against source:** 14 — VENDOR glob-row form/placement;
   `classify()` fall-through + NATIVE_SKILLS/BUILD_NEW_SKILLS membership; `--init` one-glob-row emission;
   Rule F glob coverage; path-contract §1/§2/§4/§5/§6 delta realization + read-set byte-count; source/README
   read-only wording vs spec §8/§9; narnia ch-01..04 headings; tolkien ch-01 synthetic fixture +
   tolkien-mapping.yaml existence; git-tracking state of source/; VENDOR row count at HEAD (67) vs WT (68);
   CLAUDE.md "64"/"31" claims; absence of `.raw/`/manifest; `source/`=BUILD-NEW in CLAUDE.md; live
   `check_boundary.py` exit 0.
2. **Files read to verify:** VENDOR.md, source/README.md, skills/prep/resources/path-contract.md, CLAUDE.md,
   skills/chapter-materialize/SKILL.md, scripts/check_boundary.py (lines 349-368, 405-459),
   .dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md (§5/§8/§9/§11/§12/§14),
   source/narnia/ch-01..04.txt, source/tolkien/ch-01.txt; plus git status/diff/show and find on source/.
3. **Why trust this (not a rubber-stamp):** I did NOT accept the "boundary preserved" domain claim on
   assertion — I ran `check_boundary.py` live (exit 0). I did NOT accept claim 1's "no script edit" on
   assertion — I traced `classify()` and confirmed chapter-materialize hits the NATIVE fall-through without
   any hardcoded-set membership. I found a real contradiction (VENDOR 68 vs CLAUDE 64) by counting rows two
   ways (grep vs awk, resolving a 69/68 header artifact) and comparing HEAD (67) to working tree (68), which
   is what let me correctly scope it as pre-existing-but-widened rather than newly-introduced.
4. **Web research performed:** none. All checks were local-file/code-bound; no external lookup required, so
   no Tavily/fallback engagement.

## Confidence
Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(All 6 spawn-prompt checks resolved with tool evidence; the single FAIL is a positively-verified
contradiction, not an unknown.)

## Tool engagement
Read: 5 | Grep: (folded into Bash) | Glob: 0 | Bash: 8
(Tool-call count ≥ checklist items: 6 checks, 13 tool invocations. check_boundary.py executed live.)

## Recommendations
- Before Phase-4 completion, correct `CLAUDE.md:68` "(64)" → "(68)" so the VENDOR manifest row count and
  the CLAUDE.md narrative agree. Either add CLAUDE.md to this phase's edit set or open a follow-up edit —
  it is a one-token doc fix, but it is a genuine cross-file contradiction and must be resolved (no severity
  is exempt).
- Everything else is green: the boundary contract passes live, the path-contract §12 deltas are faithful,
  the source/README provenance is honest and non-aspirational, and Mode-C zero-re-split holds against the
  actual narnia/tolkien files.

## QA Complete
