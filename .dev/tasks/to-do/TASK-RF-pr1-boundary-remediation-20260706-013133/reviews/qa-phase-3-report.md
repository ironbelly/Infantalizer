# QA Report — Phase 3 Gate (M2 Option B: docs-align + CRLF normalization test)

**Topic:** PR #1 boundary-remediation — Phase 3 (Items 3.1, 3.2)
**Date:** 2026-07-06
**Phase:** fix-cycle / phase-gate (Phase 3 of executed MDTM task)
**Fix cycle:** 1 (this is the Phase-3-specific gate; not a re-run of an earlier Phase-3 QA)

---

## Overall Verdict: PASS (after 1 in-place fix)

The Phase 3 contract (Option B: keep the text pipeline, document the LF-normalization as INTENDED, no `--init`, no manifest rehash) is honored. All three CRITICAL constraints hold: no `--init` was run, no manifest row/hash/upstream_sha changed, no adopted body or adopted SKILL.md was edited. The CRLF test is genuine (non-tautological). One MINOR defect (tmp-dir leak in the new test) was found and fixed in-place; re-verified green.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | CRLFNormalizationTests present with test_crlf_and_lf_hash_identically_under_text_pipeline | PASS | Read test file lines 766-783; class + method present |
| 2 | Test passes; total now 30 | PASS | `uv run python scripts/test_check_boundary.py` → `Ran 30 tests` / `OK` (25 base + 4 GlobSafety + 1 CRLF = 30; reconciles with the qa-phase-2 note) |
| 3 | CRLF test genuinely asserts CRLF/LF hash-equal under text pipeline (not tautological) | PASS | read_text = `p.read_text(encoding="utf-8")` (newline=None, universal newlines) at check_boundary.py:76-77; test writes raw CRLF bytes via write_bytes then reads via read_text. A switch to read_bytes (Option A) would make the assertion fail — pinning is real |
| 4 | `byte-identical`/`byte-faithful`/`byte-accurate`/`byte-equality` grep returns ONLY the honest descriptor | PASS | grep across CLAUDE.md/VENDOR.md/NOTICE → single match: VENDOR.md:21 "text-normalized, not byte-accurate" inside the new Hash-semantics bullet. CLAUDE.md and NOTICE are clean. No live byte-level integrity claim remains |
| 5 | 5 "byte-*" occurrences in CLAUDE.md softened to "text-normalized (LF)" | PASS | `git diff --cached laf-adaptation/CLAUDE.md` shows all 5 (writer body, kb/tiers+adaptation-mapping, adopted-count line, writer-contract demo, kb/tiers in conventions). No remaining live byte-* claim |
| 6 | VENDOR.md "Hash semantics" has a sentence about LF-normalized hashing | PASS | VENDOR.md:20-24 new bullet: "Hashes are computed over the LF-normalized text form (`Path.read_text`), so CRLF and LF versions of the same content hash identically; the contract is text-normalized, not byte-accurate." Accurate |
| 7 | NO manifest row / hash / upstream_sha changed (Option B contract) | PASS | `git diff --cached laf-adaptation/VENDOR.md` shows ONLY a +5-line purely-additive bullet inserted at line 20. The 64-row manifest table (line 58 onward) and the `upstream_sha: 3338495...` header (line 4) are byte-identical to before. NO `--init` was run |
| 8 | NO adopted agent body or adopted SKILL.md body edited (boundary contract) | PASS | `git status --porcelain laf-adaptation/agents/ laf-adaptation/skills/` → empty. Only dirty files: `.githooks/pre-commit`, `CLAUDE.md`, `VENDOR.md`, `scripts/check_boundary.py`, `scripts/test_check_boundary.py` — all NATIVE |
| 9 | NOTICE not edited by Phase 3 (no byte-* claim there; Phase 3 scope was 3 files) | PASS | `git diff --cached --name-only laf-adaptation/NOTICE` → empty. NOTICE contains NO byte-* claim to soften (read full file: only "carried UNMODIFIED except for ... prefix rewrite" — which is accurate under text-normalization since the rewrite is content-preserving) |
| 10 | Live verify still exits 0 / PASS after prose edits | PASS | `uv run python laf-adaptation/scripts/check_boundary.py` → "BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied." exit=0 |
| 11 | Adversarial: did the rewording weaken a true guarantee? | PASS | The reworded prose still accurately describes the ADOPTED/ADOPTED-PATCHED contract: bodies ARE integrity-protected (Rule A hash-match + Rule A′ upstream-anchor for ADOPTED-CLEAN), just via the LF-normalized hash not raw bytes. No guarantee was dropped; the prose was made MORE honest (the byte-accurate wording was an over-claim the real text pipeline did not deliver) |
| 12 | Adversarial: did the rewording make a claim STRONGER than reality? | PASS | No. The new VENDOR.md bullet explicitly states "not byte-accurate" and documents the residual (CRLF/LF hash identically). The CLAUDE.md Mode-V description retains the two-field-forgery residual disclosure. No over-claim introduced |
| 13 | CRLF test does not leak tmp dir (durability / good citizenship) | FAIL → FIXED | ORIGINAL: `CRLFNormalizationTests(unittest.TestCase)` created `tempfile.mkdtemp(prefix="crlf_test_")` with no cleanup (unlike BoundaryTestBase which has tearDown). Leaked a /tmp/crlf_test_* dir per run. FIX: added `self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)` (shutil already imported at line 17) and removed the redundant local `import tempfile`. Re-verified: 30 tests OK; live verify exit 0 |

## Summary
- Checks passed: 12 / 13 (one FAIL found and fixed in-place; now passes)
- Checks failed: 0 remaining
- Critical issues: 0
- Issues fixed in-place: 1 (MINOR — tmp-dir leak in CRLFNormalizationTests)
- CRITICAL-constraint violations (Option B contract): 0

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | test_check_boundary.py:774-776 (CRLFNormalizationTests.test_crlf_and_lf_hash_identically_under_text_pipeline) | New test created a tmp dir via `tempfile.mkdtemp` with no cleanup — leaked `/tmp/crlf_test_*` every run. Unlike `BoundaryTestBase` (which `tearDown`s), this class extends `unittest.TestCase` directly and had no cleanup hook. | Add `self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)` after the mkdtemp call; drop the redundant local `import tempfile` (tempfile already imported at module top, line 19). DONE — applied, re-verified green. |

## Actions Taken
- **Fixed** tmp-dir leak in `laf-adaptation/scripts/test_check_boundary.py` (CRLFNormalizationTests) by adding `self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)` and removing the redundant `import tempfile` (module-level import already present).
- **Verified fix** by re-running `uv run python scripts/test_check_boundary.py` → `Ran 30 tests` / `OK`; and `uv run python laf-adaptation/scripts/check_boundary.py` → exit 0 / PASS.

## Recommendations
- Phase 3 is complete and correct. The Option B contract is honored: the text pipeline is kept, the LF-normalization is documented as INTENDED in both CLAUDE.md and VENDOR.md, the new VENDOR.md bullet accurately describes the semantics and the path to a future Option-A switch (manifest-wide `--init`), and the CRLF test pins the behavior so a future switch is deliberate.
- **None of the three CRITICAL constraints were violated** — no `--init`, no manifest-row/hash/upstream_sha change, no adopted body touched. The only fix was a MINOR durability issue in the new test itself (now resolved).
- Green light to proceed to Phase 4 (M3 — writer.md Mode-V comment). The Phase-3 QA fix does not touch any Phase-4 surface.

## Confidence
- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 1 | Glob: 0 | Bash: 9 (test run x3, grep x1, git diff x2, git status x2, verify x2 — several re-runs post-fix). Tavily/web: 0 (no external claims to verify — all checks were local source-truth: file contents, git diffs, test exit codes).

## QA Complete
