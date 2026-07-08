# QA Report — Phase 2 Gate (CH-6 parser hardening + CH-4 path safety)

**Topic:** Remediation of PR #1 — `laf-adaptation/scripts/check_boundary.py` boundary-contract enforcement layer
**Date:** 2026-07-04
**Phase:** research-gate-style phase-gate (Phase 2 verification, not a synthesis gate)
**Fix cycle:** N/A (this is the gate, not a re-verification of a prior fix cycle)

---

## Overall Verdict: PASS (after 2 in-place fixes applied during this gate)

**Pre-fix state:** All 14 acceptance criteria met; all 8 required tests passed; both gate invariants green; file-scope clean. On the surface, 0 issues.

**Adversarial probing found 2 latent defects** (both CH-4 hardening gaps), which I fixed in-place under `fix_authorization: true`. After fixes: all 10 tests pass (8 required + 2 new regression tests for the gaps), both gates green, file-scope clean. Verdict PASS.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `parse_manifest` returns `(rows, errors)` tuple — `list[Row]`, `list[str]` | PASS | check_boundary.py:182-227; signature returns `rows, errors`; verified via direct call (`cb.parse_manifest(...)` → `(rows, errors)`) |
| 2 | `CLASSES` closed set validated | PASS | check_boundary.py:53 + parse_manifest line 215-217 (`cls.upper() not in CLASSES` → error); probed with bogus class → error |
| 3 | Strict `len(cells) != 4` check (loud, not silent) | PASS | check_boundary.py:209-211; probed 3-cell and 5-cell rows → "expected 4 cells" error, NOT skipped |
| 4 | `_is_hex64` correct (len==64 and all hex) | PASS | check_boundary.py:161-163; probed 9 edge cases (64-zeros, 64-f, uppercase, 63-char, 65-char, 'g'+63, empty, em-dash, 64 em-dashes) — all correct |
| 5 | Adopted rows require BOTH hashes 64-hex | PASS | check_boundary.py:218-221; verified `_is_hex64(up) or _is_hex64(laf)` → error |
| 6 | NATIVE/BUILD-NEW rows require BOTH hashes == NO_HASH | PASS | check_boundary.py:222-225; verified `up != NO_HASH or laf != NO_HASH` → error |
| 7 | Duplicate-path detection with first line number | PASS | check_boundary.py:207-209 + `seen_paths` dict; error message includes "(first at line N)" |
| 8 | All 3 call sites updated for tuple return | PASS | verify (line 398, errors → FAIL exit 1 line 486-490), do_init (line 313, errors → exit 1 line 314-319), do_report (line 500, errors → warnings printed, exit 0). Probed all three manually with malformed manifests |
| 9 | Real 64-row manifest parses to ZERO new errors | PASS | `verify` on real tree exits 0; `--report` shows 64 rows, 0 warnings; parse_manifest on real VENDOR.md returns 64 rows + empty errors |
| 10 | `_safe_repo_path` rejects absolute + `..`-escapes | PASS (after fix) | check_boundary.py:166-188; probed traversal + absolute paths. **FIX APPLIED**: original admitted `.`/empty paths (resolves to REPO itself → `IsADirectoryError` crash). Now rejects both loud at parser boundary |
| 11 | `Path.is_relative_to` (or fallback) used | PASS | Project is Python 3.13 (confirmed `uv run python --version` → 3.13.13); `is_relative_to` would work but implementer used the explicit `parents` membership check (equivalent, more portable). Defense-in-depth acceptable |
| 12 | `ManifestError` defined | PASS | check_boundary.py:56-61 |
| 13 | All manifest-path dereferences go through `_safe_repo_path` | PASS | Grep audit: every `REPO / r.path` and `REPO / rel` read in verify (lines 411, 439) and do_init (lines 331, 345, 351) routes through `_safe_repo_path`. Only literal-string `REPO / "agents"`, `REPO / "skills"` (disk discovery) bypass — those are not manifest-sourced. **No unsanitized REPO/rel reads remain** |
| 14 | All current real rows (relative, in-tree) still PASS | PASS | Real verify exits 0 on the 64-row manifest |

**Required tests (spec §5):**

| Test | Present | Passes | Notes |
|------|---------|--------|-------|
| `test_malformed_row_fails` (3+5 cell) | YES | YES | Non-vacuous: probed directly, "expected 4 cells" fires |
| `test_duplicate_path_fails` | YES | YES | Re-adds `agents/critic.md`; "duplicate path" fires |
| `test_bad_hash_fails` | YES | YES | 63-char hash; "64-hex" message fires |
| `test_native_with_hash_fails` | YES | YES | NATIVE row with real hash; "must have" message fires |
| `test_path_traversal_rejected` | YES | YES | `../../etc/passwd`; verify exits ≠ 0 |
| `test_absolute_path_rejected` | YES | YES | `/etc/passwd`; "absolute" message fires |
| `test_well_formed_manifest_has_zero_errors` | YES | YES | Clean fixture → `errors == []` |
| `test_clean_corpus_passes` | YES | YES | Self-consistent fixture → verify exit 0 |

**Tests added during this gate (regression for found defects):**

| Test | Reason |
|------|--------|
| `test_dot_or_empty_path_rejected` | Regression for the `.`/empty-path crash I found (Finding F-1 + F-2) |
| `test_report_exits_0_on_malformed` | Closes a missing spec §5 row (`test_report_exits_0_on_malformed`) — the do_report exit-0-on-malformed contract had no automated test |

## Summary
- Checks passed: 14 / 14 (after fixes)
- Checks failed: 0 (2 were found and fixed during this gate)
- Required tests passing: 8 / 8
- Total tests passing: 10 / 10 (8 required + 2 new)
- Critical issues found: 2 (both FIXED)
- Issues fixed in-place: 2

---

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| F-1 | IMPORTANT | check_boundary.py `_safe_repo_path` (lines 177-179 original) | A manifest row `| . | ADOPTED-CLEAN | <hash> | <hash> |` resolved `.` to REPO itself, passed the containment check (the `resolved == REPO.resolve()` first branch admitted REPO), then crashed with unhandled `IsADirectoryError` at `read_text(REPO_dir)` in Rule A. Violates CH-4 "fail loud, not crash" principle. | Reject `.` and empty paths at the `_safe_repo_path` boundary with a clear ManifestError; tighten the containment check so `resolved == REPO` is a reject, not an admit | FIXED |
| F-2 | IMPORTANT | check_boundary.py `parse_manifest` separator detection (line 213 original) | The header/separator detection `set(path) <= set("-: ")` admitted the empty string silently — `set()` is a subset of every set, so `|  | ADOPTED-CLEAN | <hash> | <hash> |` (4 cells, empty path) was silently swallowed as if it were a separator row. Violates CH-6 "fail loud, not silent drop." (Related to F-1: same class of degenerate-path bug; the parser's silent skip masked `_safe_repo_path`'s never being called for empty paths.) | Replace the permissive `set(path) <= set("-: ")` with a precise check: header is the exact string `path`, separator is one-or-more dashes only. Anything else (empty, single space, `:`-only) proceeds to validation and fails loud | FIXED |

### Non-issues investigated and dismissed

- **Vacuous-test check:** Probed every test assertion directly — none are vacuous. `test_malformed_row_fails` actually fires "expected 4 cells"; `test_bad_hash_fails` actually fires "64-hex"; etc.
- **Silent error-swallowing in do_init:** Verified do_init returns exit 1 on malformed manifest when reached (line 314-319). Note: do_init checks `--upstream` validity BEFORE manifest parsing, so a missing upstream short-circuits at exit 2 before the manifest is parsed — this is correct ordering (manifest parse needs a valid upstream context), not a defect.
- **Adopted-integrity weakening:** No logic change to Rules A/B/C semantics; only the parser boundary and path-safety helper were tightened. Adopted-file integrity is strictly strengthened (more malformed inputs rejected), never weakened.
- **Missed-hardening audit (REPO / r.path):** Grep audit confirmed every manifest-sourced path read goes through `_safe_repo_path`. Only literal-string subtree roots (`REPO / "agents"`, `REPO / "skills"`) bypass — those are not attacker-controlled.

---

## Actions Taken

- **FIX F-1:** Rewrote `_safe_repo_path` (check_boundary.py:166-188) to (a) reject empty/dot paths explicitly with a clear ManifestError, (b) make the containment check strict (resolved must be strictly under REPO, not equal to it). Added a docstring paragraph documenting the REPO-itself reject rationale.
- **FIX F-2:** Replaced the permissive separator detection in `parse_manifest` (check_boundary.py:212-222) with a precise check: `is_header = path.lower() == "path"` and `is_separator = len(path) >= 1 and set(path) <= {"-"}`. Added a comment explaining why the previous `set(path) <= set("-: ")` was too permissive (empty-set subset bug).
- **TEST ADDED:** `test_dot_or_empty_path_rejected` in `PathSafetyTests` — regression for F-1 + F-2. Asserts both `.` and `` empty paths produce errors AND verify fails (does not crash).
- **TEST ADDED:** `test_report_exits_0_on_malformed` in new `ReportContractTests` class — closes the missing spec §5 row. Asserts `do_report()` returns 0 on a malformed manifest.

### Verification of fixes

- Test suite: 10/10 pass (`uv run python laf-adaptation/scripts/test_check_boundary.py`)
- Verify gate on real tree: exit 0 (`uv run python laf-adaptation/scripts/check_boundary.py`)
- Report gate on real tree: exit 0 (`uv run python laf-adaptation/scripts/check_boundary.py --report`)
- File-scope invariant: `git status --short laf-adaptation/` shows only `M scripts/check_boundary.py` + `?? scripts/test_check_boundary.py`. No adopted body or carried-verbatim payload touched.

---

## Recommendations

- **Green light to proceed to Phase 3.** Both found defects are fixed and locked with regression tests.
- Future-phase note (out of scope here): the spec's `test_report_exits_0_on_malformed` row is now covered; the remaining spec §5 rows (`test_adopted_body_edit_plus_laf_hash_rewrite_fails`, `test_adopted_resource_row_deleted_fails`, `test_untracked_adopted_resource_fails`, `test_patched_class_off_writer_fails`, `test_upstream_wrong_sha_fails`, `test_prefix_rewrite_positive`) belong to CH-1/CH-2/CH-3/CH-5/CH-7 and are not in Phase-2 scope.

---

## Confidence

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 (spec, check_boundary.py, test_check_boundary.py) | Grep: 3 (REPO /, parse_manifest/read_text, r.path/rel) | Bash: 11 (test suite x3, verify gate x3, report gate x2, git status x2, python version, plus 3 adversarial probes via `uv run python -c`)

Every checklist item verified with cited tool output (file:line for static checks; command + result for behavioral checks).

## QA Complete
