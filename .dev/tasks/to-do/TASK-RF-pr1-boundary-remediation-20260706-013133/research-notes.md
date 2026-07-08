# Research Notes: PR #1 Boundary Contract Remediation

**Date:** 2026-07-06
**Scenario:** A (explicit — fixes already approved, specs already written)
**Depth Tier:** Quick-equivalent (continuation; no fresh discovery needed)
**Track Count:** 1
**Source:** troubleshoot Wave 6 handoff; full grounding already done in `.dev/troubleshoot/pr1-remediation-20260706000535/`

---

## EXISTING_FILES

All four target files were Read this turn by the troubleshoot orchestrator (real `file:line` verified):

- **laf-adaptation/scripts/check_boundary.py** (709 lines, NATIVE tooling) — the boundary-contract keystone.
  - `parse_manifest` at `:221-275` — manifest table parser; class-specific hash validation at `:266-273`; **no parse-time glob gate** (the H1 gap).
  - `manifest_covers` at `:296-302` — class-agnostic glob matching (the H1 gap).
  - `Row.is_glob` at `:177-178` (`endswith("/**")`).
  - Rule A at `:499-507` (hash-checks `is_adopted` rows only); Rule A′ at `:509-530` (excludes ADOPTED-PATCHED writer.md at `:517`); Rule D at `:603-608` (quartet only).
  - The `else:` Mode-V skip block at `:598-601` (M3: undocumented writer.md residual here).
  - Hashing: `sha256_text` `:68-69`, `read_text` `:76-77`. **8 `sha256_text` call sites** at `:382,383,396,397,403,506,526,573`.
- **laf-adaptation/scripts/test_check_boundary.py** (25 tests, all pass; ran `Ran 25 tests in 0.084s / OK`). `BoundaryTestBase` at `:56-94` patches `check_boundary.REPO`/`VENDOR_MD` to a tmp dir — the pattern for new test classes.
- **.github/workflows/boundary.yml** (54 lines) — verify-only at `:49-54`; **no test step** (the M1 gap).
- **laf-adaptation/.githooks/pre-commit** (39 lines) — runs verify at `:27`; **no test step** (the M1 gap).
- **laf-adaptation/CLAUDE.md, VENDOR.md, NOTICE** — contain "byte-identical"/"byte-faithful" claims to soften (M2 Option B).

## PATTERNS_AND_CONVENTIONS

- FAIL-LOUD parser style: see `check_boundary.py:225-247` — the parser drops nothing silently; malformed rows append to `errors`. The new H1 glob gate MUST follow this pattern (append error, `continue`).
- Comment style: block comments above the code explaining *why*, citing design doc section refs (e.g. "CH-6, M4 + CH-4, M2", "boundary-contract.md §3.3"). New comments (M3) match this.
- Tests: stdlib `unittest`, `tempfile.mkdtemp` isolated fixtures, each test writes a VENDOR.md fixture via `BoundaryTestBase`, calls `check_boundary.verify()`, asserts exit code.
- Empirical M2 evidence: `/tmp/crlf_test.py` run this turn confirmed `sha256_text` produces `3ff7e685...` for both LF and CRLF (text-mode normalization), while `sha256_bytes` distinguishes them.

## GAPS_AND_QUESTIONS

None — all four fixes are fully specified in the fix proposals. User decisions locked: M2 = Option B (docs-only); M1 = CI + pre-commit.

## RECOMMENDED_OUTPUTS

One MDTM task file at `${TASK_DIR}${TASK_ID}.md`. No fresh research files needed — the four `fix-proposals/fix-{1,2,3,4}.md` ARE the research artifacts (read them for verbatim code).

## SUGGESTED_PHASES

Single track. Phases mirror the four fixes + a verification phase:
- Phase 1: H1 — parse-time glob gate + class-aware `manifest_covers` + 3 tests
- Phase 2: M1 — CI + pre-commit test steps
- Phase 3: M2 — docs soften + CRLF normalization test
- Phase 4: M3 — writer.md/OQ-4 comment
- Phase 5: Verification (run test suite, run verify, grep byte-claims)

## TEMPLATE_NOTES

Template 02 (complex — multi-phase, build + test + verify). QA gate: FINAL_ONLY is appropriate (single small change set, <500 lines, stdlib-only; the full M3 lens-based QA sequence would be disproportionate for a 5-file, ~80-line change). The task file's own verification phase IS the quality gate.

## AMBIGUITIES_FOR_USER

None — M2 option and M1 placement both decided by user this turn.
