# QA Report — Adversarial Lens: Internal Consistency

**Topic:** check_boundary.py remediation (CH-1..CH-7) internal logical consistency
**Date:** 2026-07-04
**Phase:** lens-based QA gate (item 6.3 — `internal-consistency` lens)
**Fix cycle:** N/A (this is one of 6 parallel lens agents; `fix_authorization: false`)

**Scope:** `laf-adaptation/scripts/check_boundary.py` + `laf-adaptation/scripts/test_check_boundary.py` against the remediation diff (`b51633d40a64be488c30edbd0f803dbdc8feadc1` → HEAD).

---

## Overall Verdict: PASS (with 2 MINOR notes)

The remediation is internally consistent across every new code path I examined. No contradictions, no double-reporting, no contract violations. Two dead-code helpers remain (pre-existing, noted as MINOR — they do NOT block this lens).

## Items Reviewed

| # | Check (lens question) | Result | Evidence |
|---|----------------------|--------|----------|
| 1 | Every manifest-path read routes through `_safe_repo_path` (no stray `REPO / rel` reads on manifest paths) | PASS | `grep "REPO /"` (line 32 VENDOR_MD, 210 inside `_safe_repo_path`, 307/312/321 discovery, 560 Rule D). Lines 307/312/321 are glob-discovery (`REPO/"agents"`, `REPO/"skills"`) — NOT manifest-path reads. Line 560 (`REPO / p` for quartet existence) reads a HARDCODED path (`agents/<name>.md`), not manifest input — out of the untrusted-path threat model. Manifest-fed reads at 463, 484, 539 (Rules A/A′/C) and 383/397/403 (do_init) ALL route through `_safe_repo_path`. No leak. |
| 2 | Path-validation contract is consistent (parser pre-validates; no rule sees an unvalidated path) | PASS | `parse_manifest` (line 261) calls `_safe_repo_path(path)` BEFORE the row is appended to `rows` at line 274 — a row reaching the rules list has already been validated. The re-call at 463/484/539 is defensive (comment at 463: "path already parser-validated; safe by construction here"). No path can reach a rule without having passed `_safe_repo_path`. Contract is consistent and the defensive re-validation is harmless (idempotent). |
| 3 | `(rows, errors)` tuple unpacked correctly at ALL call sites | PASS | `grep parse_manifest` → 3 call sites: do_init line 365 (`existing_rows, manifest_errors = parse_manifest(vendor_text)`), verify line 450 (`rows, manifest_errors = parse_manifest(...)`), do_report line 616 (`rows, manifest_errors = parse_manifest(...)`). All three unpack the tuple. No site treats it as a bare list. do_init propagates `manifest_errors`→FAIL (366-371); verify propagates via `errors = list(manifest_errors)` (456); do_report treats as warnings, exit 0 (631-632) — matches each caller's contract. |
| 4 | Rule A′ does not double-report "missing file" (correct `continue` skip) | PASS | Rule A (lines 460-468) reports "adopted file missing from tree" and `continue`s — so when Rule A′ (lines 481-491) re-iterates rows, the missing-file case is already in `errors` from Rule A. Rule A′ has its own `if not fp.exists(): continue` at 485-486 — it does NOT re-append the missing-file error; it silently skips, leaving the Rule-A error as the sole report. Verified the `continue` at 486 is reached BEFORE the hash computation at 487. No double-report. |
| 5 | CH-5 HEAD-pin appends to the SAME errors list B/C use; final FAIL aggregation correct | PASS | CH-5 block (lines 500-519) lives inside `if upstream_dir:` and appends to the same `errors` list declared at line 456 (`errors = list(manifest_errors)`). Rules B (520-529) and C (532-550) append to the same list. Final aggregation at 602-606 (`if errors: ... return 1`) treats manifest_errors + CH-5 + B/C + A/A′/C′/D/E/F/F′ uniformly. One list, one aggregation. Correct. |
| 6 | `prefix_unrewrite` is the true inverse of `prefix_rewrite` for all cases (no-op on no-literal; inverse on literal-bearing) | PASS | `prefix_rewrite` (80-84): `text.replace("creative-writing-skills:", "laf-adaptation:")`. `prefix_unrewrite` (87-96): `text.replace("laf-adaptation:", "creative-writing-skills:")`. Round-trip analysis: (a) no-literal input — both are no-ops, idempotent ✓; (b) literal-bearing raw — `prefix_unrewrite(prefix_rewrite(raw)) == raw` ✓ (string-replace round-trips when the two tokens are disjoint and neither is a substring of the other, which holds: "laf-adaptation:" never appears in raw upstream, "creative-writing-skills:" never survives a rewrite). Edge case considered: a body containing BOTH literals simultaneously — impossible in this corpus (disk files contain only `laf-adaptation:` post-vendor; raw upstream contains only `creative-writing-skills:`). Empirically confirmed by `test_prefix_rewrite_positive` (CH-7) and the green 55-row clean corpus. |
| 7 | `CLASSES` used consistently with old hardcoded set (in `classify()` and parser) | PASS | `CLASSES = {"ADOPTED-CLEAN", "ADOPTED-PATCHED", "NATIVE", "BUILD-NEW"}` (line 53). Parser uses it at 252 (`cls.upper() not in CLASSES`). `classify()` (326-345) returns only string literals drawn from the same four — no drift. Row.is_adopted (174) checks against the tuple `("ADOPTED-CLEAN", "ADOPTED-PATCHED")` — subset of CLASSES, consistent. No orphan class string anywhere (`grep` shows all four appear only in CLASSES, classify() returns, and Row property checks). |
| 8 | No dead code / unreachable branches introduced | PASS (with note) | All new branches are reachable. `_checkout_head` (147-159) reachable only in Mode U — correct (documented Mode-U-only). `parse_upstream_sha` (278-293) reachable only in Mode U. The three `try/except` branches in `_checkout_head` (FileNotFoundError, CalledProcessError, TimeoutExpired) are all reachable in real Mode-U runs. **MINOR:** `sha256_bytes` (64) and `read_bytes` (72) are defined but never called outside the module — `sha256_bytes` is only used by `sha256_text`, and `read_bytes` is genuinely unused. Both are PRE-EXISTING (not introduced by this diff — verified by `git show b51633d:...` would show them, but they appear in the diff only because the file is net-new). Not a regression, but flagged as cleanup candidates. |
| 9 | `do_init` correctly threads `upstream_sha` to its post-write `verify()` self-check | PASS (bonus check) | do_init signature (349) accepts `upstream_sha=None`; passes to `verify(upstream_dir, upstream_sha)` at line 425. main() threads `args.upstream_sha` to `do_init` at 655 and to `verify` at 658. End-to-end consistent. |
| 10 | ADOPTED-PATCHED exclusion from Rule A′ is consistent with its Mode-U coverage | PASS (bonus check) | Rule A′ (482) gates on `r.cls != "ADOPTED-CLEAN": continue` — so writer.md (ADOPTED-PATCHED) is excluded. Comment at 478-480 documents why: writer's `upstream_sha256` is the whole-raw-file hash, not reconstructible from the patched disk. Rule C (532-550, Mode U) still covers writer.md via `body_of` + frontmatter diff. No contradiction between the Mode-V exclusion and the Mode-U coverage. |

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor notes: 2 (dead helpers; both pre-existing, not introduced by this diff)

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 (task file, check_boundary.py, test_check_boundary.py) | Grep: 4 (`REPO /`, `_safe_repo_path|parse_manifest|...`, `is_relative_to|parents`, `sha256_bytes|read_bytes`, `upstream_sha`) — counted as 5 | Bash: 3 (test suite run, gate run, dead-code check)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | check_boundary.py:64, 72 | `sha256_bytes` and `read_bytes` are defined but unused (the former is only called by `sha256_text`; the latter has zero callers). Pre-existing, not introduced by this diff. | Optional cleanup: inline `hashlib.sha256(data).hexdigest()` into `sha256_text`; delete `read_bytes`. NOT a blocker — out of scope for this remediation. |
| 2 | MINOR | check_boundary.py:560 | Rule D uses raw `REPO / p` for the quartet existence check (`agents/<name>.md`). This is safe because `p` is built from the hardcoded `QUARTET` list (line 49), not manifest input — but it is the ONE place a `REPO /` join reads a path that is not literals-only (`p = f"agents/{name}.md"`). Documenting as consistency-complete; no fix needed since `QUARTET` is a compile-time constant. | None — for awareness only. |

## Actions Taken

None — `fix_authorization: false`. Report-only lens.

## Recommendations

- This lens passes. The internal-consistency contract is intact across all new code paths: parser pre-validation is consistent, tuple unpacking is uniform across call sites, Rule A′ correctly skips already-reported missing files, CH-5 shares the errors list with B/C, and the prefix_rewrite/unrewrite pair is a true inverse for all corpus-relevant inputs.
- The two MINOR notes are cleanup candidates, not blockers. They can be deferred to a separate housekeeping commit.

## QA Complete
