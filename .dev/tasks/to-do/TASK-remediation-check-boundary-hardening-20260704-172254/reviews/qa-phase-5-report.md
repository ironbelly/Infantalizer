# QA Report — Phase 5 (CH-8 Doc Alignment)

**Topic:** Doc/code alignment for `check_boundary.py` remediation (PR-1 review, CH-8 REQUIRED doc part)
**Date:** 2026-07-04
**Phase:** fix-cycle / report-validation (adversarial doc-vs-code gate for Phase 5 output)
**Fix cycle:** N/A (initial Phase-5 verification)

---

## Overall Verdict: PASS

The three remediated docs (`boundary.yml` header, `CLAUDE.md` §2, `VENDOR.md` header) accurately describe what the gate actually does. No over-claiming of absolute guarantees. Every factual claim matches the code, empirically verified. No fixes required.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Rule A′ (CH-1) exists in `verify()` and asserts `sha256(prefix_unrewrite(disk)) == upstream_sha256` for ADOPTED-CLEAN | PASS | `check_boundary.py:481-491`. Empirically confirmed on `agents/brainstormer.md`: `sha256(prefix_unrewrite(disk)) = aa736c5d... = pinned upstream_sha256` (Bash, 2026-07-04). The doc-corrected INVERSE formula is used (not the spec §4.1 ambiguous original); OQ-1 resolution recorded in Task Log corrects the spec. |
| 2 | "Mode V is a malicious-drift gate against single-field `laf_sha256` forgery" — claim holds AND does not overstate to "absolute" | PASS | Built an independent attack fixture (mutated body + forged `laf_sha256` only) → `verify()` returned 1 with the CH-1 error. The doc qualifier "against single-field `laf_sha256` forgery" is the precise, scoped claim — it does NOT say "absolute malicious-drift gate." Honest. |
| 3 | Doc honestly states Mode V does NOT run Rules B/C and does NOT give the absolute guarantee for ADOPTED-PATCHED (writer.md) | PASS | Code: Rules B/C inside `if upstream_dir:` block (`check_boundary.py:500-550`); A′ skips ADOPTED-PATCHED (`:482`). `boundary.yml:23-29` explicitly: "What Mode V does NOT do... Rules B/C... do not run here. ADOPTED-PATCHED (writer.md) and any literal-bearing body's ABSOLUTE guarantee requires Mode U." Matches code exactly. |
| 4 | C′ (CH-3): ADOPTED-PATCHED reserved for `agents/writer.md`; enforced outside the `if upstream_dir:` block | PASS | `check_boundary.py:493-497` — Rule C′ loop is positioned BEFORE `if upstream_dir:` (which opens at `:500`). Runs in BOTH Mode V and Mode U. CLAUDE.md §2 bullet C′ (`:107`) and VENDOR.md Invariants (`:29`) both match. |
| 5 | F′ (CH-2): adopted-skill `resources/**` coverage | PASS | `check_boundary.py:586-600` computes `adopted_skill_dirs` from manifest rows and asserts each `disk_skill_files(skdir)` is `manifest_covers`. Empirically ran the F′ derivation against the real manifest: all 12 adopted skill dirs show 0 uncovered files (creative-writing-craft=10, story-review=16, story-memory=7, etc.). |
| 6 | VENDOR.md hash-semantics: `upstream_sha256` = RAW upstream hash; `laf_sha256` = on-disk (already-rewritten) hash | PASS | `--init` line 249: `up_sha = sha256_text(up_raw)` (RAW). Empirically on brainstormer.md: `sha256(disk) = 5c827eff... = laf_sha256` (rewritten), `sha256(prefix_unrewrite(disk)) = aa736c5d... = upstream_sha256` (raw). VENDOR.md `:10-17` describes exactly this. |
| 7 | VENDOR.md format constraint: paths/hashes must not contain `\|`; `parse_manifest` rejects `\|`-shifted rows | PASS | Tested `parse_manifest` with a row `| agents/foo.md \| ADOPTED-CLEAN \| aa\|bb \| cc |` → produced 5 cells → rejected with `manifest line 7: expected 4 cells, got 5`. VENDOR.md `:21-23` matches. |
| 8 | No claim of an ABSOLUTE guarantee the gate doesn't deliver (spec §9.6) | PASS | `grep -iE "absolute\|guarantee\|malicious\|forge"` across all three docs. Every "absolute guarantee" mention is correctly attributed to **Mode U** (`CLAUDE.md:116` "Mode U is the absolute guarantee; it is not (yet) run in CI"; `boundary.yml:24-29` "ABSOLUTE guarantee requires Mode U... branch protection + human review backstop the residual absolute-guarantee gap"). Mode V is described only as a scoped "malicious-drift gate against single-field laf_sha256 forgery." No over-claiming. |

### Gate-green invariant

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| G1 | `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 | PASS | `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` `EXIT_CODE=0` |
| G2 | `uv run python laf-adaptation/scripts/check_boundary.py --report` exits 0 | PASS | 64 rows (55 ADOPTED-CLEAN, 1 ADOPTED-PATCHED, 5 NATIVE, 3 BUILD-NEW). `EXIT_CODE=0` |
| G3 | Test suite green | PASS | `Ran 21 tests in 0.060s — OK` (21/21 pass) |
| G4 | File-scope invariant: only the 5 permitted files changed under `laf-adaptation/` + `.github/` | PASS | `git status --short` filtered to `laf-adaptation/` + `.github/` shows exactly: `.github/workflows/boundary.yml` (M), `laf-adaptation/CLAUDE.md` (M), `laf-adaptation/VENDOR.md` (M), `laf-adaptation/scripts/check_boundary.py` (M), `laf-adaptation/scripts/test_check_boundary.py` (??). No adopted body or carried-verbatim payload touched. (Other modified/untracked files at repo root — README.md, docs/, .claude/, .dev/, config/ — are outside the file-scope invariant's jurisdiction and pre-date this phase.) |

## Summary

- Checks passed: 12 / 12 (8 doc-alignment + 4 gate-green)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (none needed — docs match code)

## Confidence

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 3 | Glob: 0 | Bash: 9 (gate runs + empirical hash/attack/coverage/parse verifications) | Tavily: 0 | Web fallback: 0

## Notes

- **Spec-vs-code correction handled correctly.** The remediation spec §4.1/§6 Q1 carried an acknowledged-ambiguous formula (`sha256(prefix_rewrite(disk)) == upstream_sha256`). The executor resolved OQ-1 empirically and implemented the INVERSE formula (`sha256(prefix_unrewrite(disk)) == upstream_sha256`), recording the correction in the Task Log. The Phase-5 docs describe the CORRECTED formula, not the wrong spec formula. This is the right outcome — the spec was a Phase-A artifact, the code is the source of truth, and the docs track the code.
- **"Malicious-drift gate" phrasing is scoped, not absolute.** CLAUDE.md:105-106 and boundary.yml:13-14 both read "Mode V is therefore a malicious-drift gate against single-field `laf_sha256` forgery." The qualifier "against single-field `laf_sha256` forgery" defines the precise scope of the claim, and the mechanism genuinely catches that exact attack (verified). This is not over-claiming.
- **VENDOR.md is the most conservative doc** — it contains zero "absolute" or "guarantee" language, only factual hash-semantics and invariants, all of which are code-enforced.

## QA Complete
