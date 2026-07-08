# QA Report — lens-security-boundary-correctness (task-qualitative lens)

**Topic:** Security-boundary correctness of `laf-adaptation/scripts/check_boundary.py` (PR-1 remediation CH-1..CH-8)
**Date:** 2026-07-04
**Phase:** task-qualitative (single-lens security review, fix-cycle N/A)
**Fix cycle:** N/A
**Lens:** security-boundary-correctness (the most important lens — adversarial attacker mindset)
**fix_authorization:** false (REPORT ONLY)

---

## Overall Verdict: FAIL

The remediation closes the **single-field** `laf_sha256` forgery attack at zero CI cost (CH-1, the
H1 floor) and the path/parser hardening (CH-4, CH-6) is sound against the standard traversal and
malformed-row vectors. **However, two material defects remain**, both concentrated in the CH-1
trust-root re-anchoring:

1. **CRITICAL — undetected attack, missing acceptance test.** The both-hashes-forged-self-consistent
   attack (mutate body + rewrite BOTH `laf_sha256` AND `upstream_sha256` to be self-consistent)
   **PASSES Mode V green**. The spec §4.1 acceptance bullet 2 *explicitly* required this case to be
   tested and to FAIL or be loudly detectable; the implemented test
   `test_upstream_sha256_rewrite_of_clean_body_fails` does NOT cover it (it only rewrites one hash
   on an UNMODIFIED body). I empirically reproduced the bypass.
2. **IMPORTANT — over-claiming docs.** `VENDOR.md`, `CLAUDE.md` §2, and `boundary.yml` frame
   `upstream_sha256` as a "loud, review-visible" change because it is "documented as
   upstream-derived", and call Mode V "a malicious-drift gate". The qualifier "single-field"
   exists but is doing all the work; the docs do not state plainly that **two-field forgery defeats
   Mode V and requires Mode U / branch protection / human review**. The spec §4.8 REQUIRED doc
   alignment "no over-claiming"; the docs over-claim by omission.

The remaining lenses (CH-2/3/4/5/6/7) are sound against their threat models. The two findings above
are scoped to CH-1's residual gap and its documentation, which the spec itself flagged as the
crux ("This is the crux of H1").

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| CH-1a | Single-field `laf_sha256` forgery is rejected (mutate body + rewrite only `laf_sha256`) | none | PASS | `test_adopted_body_edit_plus_laf_hash_rewrite_fails` (test_check_boundary.py:299-311); also re-derived by hand: `sha(prefix_unrewrite(edited_body)) != pinned upstream_sha256` → Rule A′ fires |
| CH-1b | **Both-fields forgery is rejected (mutate body + rewrite BOTH hashes self-consistent)** | **AX-3** | **FAIL** | Empirically reproduced: a fixture with quartet-only rows passes baseline (`verify()==0`); after attacker mutates `critic.md` body AND rewrites both `laf_sha256` and `upstream_sha256` to `sha(prefix_unrewrite(mutated_body))`, `verify()` STILL returns 0. Mode V cannot detect — `upstream_sha256` is PR-editable and there is no independent trust root in Mode V. Spec §4.1 acceptance bullet 2 mandated this case be tested AND fail-or-be-loudly-detectable. |
| CH-1c | The acceptance test for spec §4.1 bullet 2 (both-hashes self-consistent) exists | **AX-3** | **FAIL** | `grep -n "self-consistent\|both.hash" test_check_boundary.py` returns only the `build_clean_fixture` docstring match (line 114) — NOT a test of the attack. `test_upstream_sha256_rewrite_of_clean_body_fails` (line 313) rewrites ONE hash on an UNMODIFIED body — wrong attack. The spec-required test is absent. |
| CH-1d | `prefix_unrewrite` is a sound inverse for all 55 ADOPTED-CLEAN rows in the real corpus | none | PASS | `grep -rln` for files containing BOTH `laf-adaptation:` AND `creative-writing-skills:` literals returned 0. Every adopted file is purely prefix-rewritten (or has neither literal), so the inverse is well-defined and idempotent. writer.md contains `laf-adaptation:` but NOT `creative-writing-skills:` and is correctly excluded from Rule A′ (whole-file raw hash not reconstructible from patched disk). |
| CH-1e | Docs honestly state the residual two-field forgery gap | **AX-4** | **FAIL** | `VENDOR.md:13-16`, `CLAUDE.md:104-106`, `boundary.yml:9-14` all describe Mode V as "a malicious-drift gate" and frame `upstream_sha256` rewrite as "loud, review-visible". The "single-field" qualifier is present but the docs never state plainly that **mutating the body AND rewriting both hashes to be self-consistent defeats Mode V**, nor that this is why Mode U / branch protection / human review are non-negotiable backstops. The spec §4.8 REQUIRED "no absolute-guarantee language the gate doesn't actually deliver" — calling Mode V "a malicious-drift gate" without naming the two-field bypass is over-claiming by omission. |
| CH-2 | Adopted skills' `resources/**` deletion and untracked-file injection both fail | none | PASS | `test_adopted_resource_row_deleted_fails`, `test_untracked_adopted_resource_fails` (test_check_boundary.py:368-389). Rule F′ (`verify` lines 592-600) computes `adopted_skill_dirs` from adopted rows and asserts every file in those dirs is `manifest_covers`-ed. |
| CH-3 | ADOPTED-PATCHED off-writer fails in BOTH modes | none | PASS | `test_patched_class_off_writer_fails_mode_v` and `_mode_u` (lines 333-362). Rule C′ placed OUTSIDE `if upstream_dir:` block (line 495) — verified by reading check_boundary.py:493-497. |
| CH-4a | `..`-escape and absolute-path traversal rejected | none | PASS | `_safe_repo_path` (lines 193-217) uses `(REPO / rel).resolve()` + `is_relative_to(REPO)` containment; `test_path_traversal_rejected`, `test_absolute_path_rejected`. Verified empirically that `..`, `/etc/passwd`, `.` and empty paths all rejected. |
| CH-4b | Symlink-based bypass rejected | none | PASS | Empirically tested: `os.symlink('/etc/passwd', tmp/'evil.md')` then `_safe_repo_path('evil.md')` → REJECTED (resolved real path is `/etc/passwd`, outside REPO). `REPO.resolve()` is called both at module load and inside `_safe_repo_path`, so a symlinked work-tree cannot smuggle a path back inside. |
| CH-4c | Encoding/normalization tricks (`..%2f`, `....//`, backslash) rejected | none | PASS | Probed empirically: `..%2f..%2fetc%2fpasswd`, `..%5c..%5cetc%5cpasswd`, `....//....//etc/passwd` all resolve to literal filenames inside REPO (no shell/HTTP decoder), so they are inert — they name nonexistent files and would surface as Rule A "adopted file missing" errors, not as escapes. |
| CH-4d | Subtree-escape within REPO (`skills/x/../../outside.md`) | none | PASS (with note) | `_safe_repo_path('skills/x/../../outside.md')` resolves to `<REPO>/outside.md` and PASSES the containment check (it is inside REPO). This is acceptable: the manifest is explicit about path → the file would be Rule-A-checked at `<REPO>/outside.md`, and `outside.md` is not in the declared manifest as a covered location for `skills/`, so Rule F′/E semantics still apply. Not a bypass — manifest is the source of truth for path. |
| CH-5 | Mode U asserts checkout HEAD == pinned `upstream_sha` | none | PASS | `_checkout_head` + `parse_upstream_sha` + `--upstream-sha` flag (lines 147-159, 278-293, 646-648). `test_upstream_wrong_sha_fails`, `test_upstream_matching_sha_passes_head_check` — the latter asserts `"HEAD"` absent from full stderr, not just preamble. Pin precedence `--upstream-sha` flag > VENDOR.md header; missing pin → FAIL LOUD. |
| CH-6a | Malformed rows (≠4 cells) fail loud | none | PASS | `parse_manifest` lines 236-238; `test_malformed_row_fails`. Verified by inspection that any `|` inside any cell yields >4 cells (a 4-cell result with embedded `|` is structurally impossible). |
| CH-6b | Duplicate paths fail loud | none | PASS | `seen_paths` dict (lines 230, 255-258); `test_duplicate_path_fails`. |
| CH-6c | Bad hash format (63-char, non-hex, NATIVE-with-hash) fails loud | none | PASS | `_is_hex64` (line 188); `test_bad_hash_fails`, `test_native_with_hash_fails`. |
| CH-6d | Header/separator detection is precise (no silent data-row drops) | none | PASS | Empirically: empty-path and `.`-path rows are now rejected (was the rf-qa F-2 finding, fixed). Header match is `path.lower() == "path"` (exact, case-insensitive); separator match is `set(path) <= {"-"}` (non-empty dashes-only) — neither admits a data row. |
| CH-7 | Rule B prefix-rewrite positive path exercised | none | PASS | `test_prefix_rewrite_positive` (lines 400-422) constructs a synthetic `creative-writing-skills:`-bearing blob, asserts `sha256(prefix_rewrite(raw))` satisfies Rule B, AND asserts skipping the rewrite fails. Real-corpus rows have no literal (grep returned 0) — without this test the rewrite machinery would be unexercised. |
| CH-8 | CI workflow + docs aligned with actual gate behavior, no over-claiming | **AX-2** | **FAIL** | See CH-1e — the docs call Mode V "a malicious-drift gate" without naming the two-field forgery bypass. CH-8 is the cross-cutting "doc-alignment" change and it under-claims the gap. Spec §4.8 REQUIRED doc accuracy. |
| WEAKEN-1 | Did CH-6's `(rows, errors)` restructure let a previously-caught violation through? | none | PASS | `verify` line 456: `errors = list(manifest_errors)` — every parser error becomes a verify FAIL. `do_init` lines 365-371: manifest errors → exit 1. `do_report` lines 616-632: errors → warnings, exit 0 (preserves L1 contract). No previously-caught violation is silently dropped; if anything the new parser is strictly stricter (duplicate-path, bad-hash, native-with-hash, dot/empty path are NEW rejections). |
| WEAKEN-2 | Did CH-1's Rule A′ introduction create any false-positive risk on the clean corpus? | none | PASS | `verify()` on real tree → exit 0 (Bash confirmed: `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied`). The inverse formula was empirically corrected during Phase 3 (the spec §4.1 first-recorded formula was wrong — would have false-positived every row; the corrected `prefix_unrewrite` formula is sound). |

## Summary
- Checks run: 22 (lens-specific, mapped to the task's CH-* items + WEAKEN cross-checks)
- Checks passed: 17
- Checks failed: 5 (CH-1b, CH-1c, CH-1e, CH-8, derived from 2 root causes: missing test + over-claiming docs)
- Critical issues: 1 (CH-1b/CH-1c — undetected attack + missing spec-required test)
- Important issues: 1 (CH-1e/CH-8 — over-claiming docs)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `laf-adaptation/scripts/test_check_boundary.py` (missing test); `check_boundary.py:481-491` (Rule A′) | The both-hashes-forged-self-consistent attack is **undetected** by Mode V and **untested**. Spec §4.1 acceptance bullet 2 explicitly required: "A test that mutates an adopted body and updates BOTH hashes to be self-consistent but wrong-vs-upstream → behaviour per §6 Q1 resolution (the whole point is to make this FAIL or be loudly detectable)." I reproduced the attack against a clean fixture: mutating `critic.md` and rewriting BOTH `laf_sha256` and `upstream_sha256` to `sha256(prefix_unrewrite(mutated_body))` returns `verify()==0`. The existing `test_upstream_sha256_rewrite_of_clean_body_fails` only rewrites ONE hash on an UNMODIFIED body — it does not exercise this attack. | (a) Add `test_adopted_body_edit_plus_both_hashes_forged_passes_mode_v__documented_gap` — a test that demonstrates the attack SUCCEEDS in Mode V (asserts `verify()==0`) and includes a comment block stating explicitly that this is the documented residual gap closed only by Mode U + branch protection + human review. (b) Optionally, if Mode U is in scope, add the same attack under Mode U and assert it FAILS via Rule B (the upstream blob won't match). The spec language "FAIL or be loudly detectable" is satisfied by either an explicit detection (Mode U) or an honest documented-and-tested gap (Mode V) — but the test MUST exist. |
| 2 | IMPORTANT | `laf-adaptation/VENDOR.md:13-16`; `laf-adaptation/CLAUDE.md:103-107`; `.github/workflows/boundary.yml:8-14` | The docs frame Mode V as "a malicious-drift gate against single-field `laf_sha256` forgery" and call an `upstream_sha256` rewrite "loud, review-visible", but never state plainly that **mutating the body AND rewriting both hashes self-consistently defeats Mode V**. The "single-field" qualifier is the only signal — a reader skimming the prose will conclude Mode V is a malicious-drift gate, full stop. The spec §4.8 REQUIRED: "no absolute-guarantee language the gate doesn't actually deliver" and "explicitly state CI is an accidental-drift gate, not a malicious-drift gate, and rely on branch protection + human review for the latter" if option (c) is chosen. The remediation effectively shipped option (c) (Mode V floor, Mode U deferred per OQ-4) but retained "malicious-drift gate" framing without the explicit two-field-bypass caveat. | Add to VENDOR.md Hash-semantics, CLAUDE.md §2 Enforcement bullet A′, and boundary.yml comment a single explicit sentence: "Mode V detects single-field `laf_sha256` forgery only; an attacker who mutates an adopted body AND rewrites both `laf_sha256` and `upstream_sha256` to be self-consistent defeats Mode V. Detection requires Mode U (`--upstream`), branch protection (no direct pushes to main, mandatory PR review), or human review of `upstream_sha:` and `upstream_sha256` diffs." Demote "malicious-drift gate" to "single-field-forgery gate" in summary lines. |

## Actions Taken
None (fix_authorization: false). Both findings are documented above with specific remediation.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` block was present in the spawn prompt; this review ran in
standalone mode and performed its own structural re-checks where load-bearing for the security
claims. Reliance list is empty; all checks above were verified with direct tool engagement.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None (no Inherited Structural Verdict provided).

**(b) Independent semantic checks (≥1 required, INV-019):**
- CH-1b — verified by executing the attack in a tmp fixture: `verify()==0` after both-hashes forgery (Bash).
- CH-1c — verified by `grep -n "self-consistent\|both.hash" test_check_boundary.py` returning no attack test (Grep).
- CH-1d — verified by `grep -rln` for files containing BOTH prefix literals across `agents/` and `skills/` returning 0 (Grep).
- CH-4a/4b/4c/4d — verified by probing `_safe_repo_path` with 9 traversal variants and one symlink attack (Bash).
- CH-6a — verified by inspecting `parse_manifest` cell-split semantics and confirming a `|`-in-cell always yields >4 cells (Read + Bash).
- WEAKEN-1 — verified by reading all 3 `parse_manifest` call sites and confirming errors → FAIL in verify/do_init, warnings in do_report (Read).

## Confidence
- Verified: 22 / 22
- Unverifiable: 0
- Unchecked: 0
- Confidence: 100.0%

## Tool engagement
- Read: 5 (check_boundary.py, TASK file, remediation-spec.md, VENDOR.md, boundary.yml, test_check_boundary.py)
- Grep: 4 (corpus literal scan, both-literal intersection, doc-framing grep, test-coverage grep)
- Bash: 6 (gate green check, test run, both-hashes attack reproduction, path-traversal probes, symlink probe, parser corner cases)
- Web research: 0 (no external lookup required — all claims are local-file-bound)

## Recommendations
Before marking the task Done:
1. Add the missing acceptance test for spec §4.1 bullet 2 (Issue #1). Either demonstrate-and-document
   the Mode V gap, or land Mode U detection for it. The spec's "FAIL or be loudly detectable" is
   satisfied by either — but the test MUST exist; its absence is a direct DoD violation (spec §9
   point 2: "test suite exists + passes" cannot be true for a test that does not exist).
2. Tighten the three doc surfaces (Issue #2) so a skimming reviewer cannot conclude Mode V is a
   general malicious-drift gate. Branch protection + human review of `upstream_sha256` diffs must be
   named as non-negotiable backstops in the docs themselves, not just the spec.
3. (Out of scope for this gate but worth flagging for F1/follow-up) The absolute guarantee for the
   both-hashes attack requires Mode U in CI (Option B, deferred per OQ-4). The remediation ships the
   weaker floor; the docs must say so plainly.

## QA Complete
