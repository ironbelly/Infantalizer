# QA Report — Adversarial Lens: Template-Conformance

**Topic:** PR #1 remediation diff (check_boundary.py hardening, 2 HIGH + 5 MED)
**Date:** 2026-07-04
**Phase:** report-validation (lens-based review, lens = template-conformance)
**Fix cycle:** N/A (single lens pass, `fix_authorization: false`)

**Base commit:** `b51633d40a64be488c30edbd0f803dbdc8feadc1`
**Diff scope:** 5 files — `laf-adaptation/scripts/check_boundary.py`, `laf-adaptation/scripts/test_check_boundary.py`, `.github/workflows/boundary.yml`, `laf-adaptation/CLAUDE.md`, `laf-adaptation/VENDOR.md`
**Driving spec:** `.dev/reviews/pr-1-20260704125705/remediation-spec.md` (§4.1–§4.8 sketches, §5 test plan, §9 DoD)
**Task file:** `.dev/tasks/to-do/TASK-remediation-check-boundary-hardening-20260704-172254/TASK-remediation-…md`

---

## Overall Verdict: PASS

The remediation faithfully implements every spec §4.x sketch in INTENT. The single most-noticed deviation — CH-1's correction of `prefix_rewrite(disk)` to `prefix_unrewrite(disk)` — is a JUSTIFIED, NECESSARY deviation that the spec itself flagged as a §6 Q1 BLOCKER ("the single most important detail to resolve before coding"); the executor resolved it empirically and documented the correction in three places (Task Log → Resolutions OQ-1 CORRECTED, Phase 3 Findings, VENDOR.md hash-semantics section). It is not silent drift. All §5 test-plan rows are covered (14/14 + 7 extras, 21/21 pass). Task-file phase order matches spec §7; item-level ordering within phases is correct; OQ-1–OQ-4 all have recorded resolutions; Phase 5.2 (CH-8 Option B) is explicitly DEFERRED per OQ-4 with rationale.

One MINOR finding (CH-5 tarball fallback) does not weaken enforcement and does not block the gate.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | CH-1 vs spec §4.1 sketch — `prefix_unrewrite` correction | PASS | `check_boundary.py:87-96, 481-491`. Spec formula `sha256(prefix_rewrite(disk)) == upstream_sha256` was flagged ambiguous (§4.1 + §6 Q1 BLOCKER). Executor empirically verified on brainstormer.md that disk is ALREADY prefix-rewritten (`sha256(disk)=5c827eff=laf_sha256`, `upstream_sha256=aa736c5d`), so the spec's literal formula would have FALSE-POSITIVEd on the entire clean corpus. Corrected to `sha256(prefix_unrewrite(disk)) == upstream_sha256`. Recorded in OQ-1 CORRECTED, Phase 3 Findings, VENDOR.md header. Mathematically sound (disk == prefix_rewrite(raw) ⟹ prefix_unrewrite(disk) == raw). |
| 2 | CH-6 vs spec §4.6 sketch — `parse_manifest` returns `(rows, errors)` | PASS | `check_boundary.py:220, 275`. Signature matches: `def parse_manifest(text)` → `return rows, errors`. CLASSES set defined (line 53). Strict `len(cells) != 4` check (line 236-237). `_is_hex64` helper (line 188). Duplicate-path detection with first-line ref (line 255-258). Adopted rows require 64-hex hashes (line 266-269). NATIVE/BUILD-NEW require NO_HASH (line 270-273). |
| 3 | CH-6 — 3 call sites handle `(rows, errors)` tuple | PASS | `verify` line 450 (`rows, manifest_errors = parse_manifest(...)` → errors propagated to `errors = list(manifest_errors)` line 456 → FAIL exit). `do_init` line 365 (`existing_rows, manifest_errors` → returns 1 on errors, line 366-371). `do_report` line 616 (errors printed as warnings, still exits 0 — preserves `--report` contract). |
| 4 | CH-2 vs spec §4.2 sketch — Rule F′ resources/** | PASS | `check_boundary.py:592-600`. `adopted_skill_dirs` set comprehension matches spec verbatim. Iterates `disk_skill_dirs()` + `disk_skill_files()` + `manifest_covers()`. Error message `"adopted-skill file not in VENDOR.md manifest"` matches spec §4.2 sketch byte-for-byte. |
| 5 | CH-3 vs spec §4.3 sketch — writer-only ADOPTED-PATCHED | PASS | `check_boundary.py:495-497`. Predicate `r.cls == "ADOPTED-PATCHED" and r.path != "agents/writer.md"` matches spec verbatim. Error message `"ADOPTED-PATCHED is reserved for agents/writer.md only"` matches spec verbatim. Placement OUTSIDE `if upstream_dir:` block confirmed (block opens at line 500, after the C′ loop) — runs in BOTH modes per spec. |
| 6 | CH-4 vs spec §4.4 sketch — `_safe_repo_path` + `ManifestError` | PASS | `check_boundary.py:56, 193-217`. `ManifestError(ValueError)` class. `Path(rel).is_absolute()` rejection. `resolve()` + `repo_resolved not in resolved.parents` containment check (3.9+-equivalent, OQ-2 confirmed Python 3.13). Rejects absolute, `..`-escape, `.`/empty. Spec sketch placement was at consumption sites; executor placed it BOTH inside the parser (line 261) AND at consumption sites (lines 463, 484, 539) — defense in depth, strictly stronger than spec. |
| 7 | CH-5 vs spec §4.5 sketch — Mode U HEAD pin | PASS (with MINOR) | `_checkout_head` via `git rev-parse HEAD` (line 147-159). `parse_upstream_sha` header parser (line 278-293). `--upstream-sha` CLI flag (line 646). Pin precedence `upstream_sha or parse_upstream_sha(...)` matches spec (flag > VENDOR.md). HEAD-mismatch error message format matches spec §4.5 sketch. **MINOR deviation:** spec §4.5 specifies `--upstream-sha` as a FALLBACK when git is unavailable (tarball checkout) — "fall back to accepting an explicit `--upstream-sha`... if neither is available, fail loud." Executor's implementation (line 511-519) ALWAYS fails when `_checkout_head` returns None, even if `--upstream-sha` is passed. The deviation is strictly strengthening (never silently trusts the tree), and the error message even directs the user to pass `--upstream-sha` — but the tarball-use-case from spec §4.5 is not honored. See Issue #1. |
| 8 | CH-7 vs spec §4.7 sketch — prefix-rewrite positive test (Option M5-A) | PASS | `test_check_boundary.py:400-422`. Option M5-A (test fixture) chosen per OQ-3 — matches spec recommendation. `test_prefix_rewrite_positive` constructs synthetic `creative-writing-skills:`-bearing blob, asserts `sha256(prefix_rewrite(raw))` satisfies Rule B AND that skipping the rewrite FAILS. `check_boundary.py` source unchanged by this item (test-only) — matches M5-A contract. |
| 9 | CH-8 vs spec §4.8 — doc alignment | PASS | `boundary.yml:3-30` comment accurately enumerates post-remediation rules (A, A′, C′, D, E, F, F′ + parser/path-safety). Honest disclosure of Mode V limitations (lines 23-29): "Rules B/C and the absolute upstream-anchored guarantee do not run here... requires Mode U... deferred follow-up (OQ-4)". CLAUDE.md §2 Enforcement bullet matches. VENDOR.md hash-semantics + format-constraint sections added. No over-claiming of absolute guarantee. |
| 10 | Test plan §5 coverage — 14 required rows | PASS | All 14 spec §5 test rows present: `test_clean_corpus_passes` (147), `test_adopted_body_edit_plus_laf_hash_rewrite_fails` (299), `test_adopted_resource_row_deleted_fails` (368), `test_untracked_adopted_resource_fails` (384), `test_patched_class_off_writer_fails` (333 + 344 mode-U variant), `test_path_traversal_rejected` (212), `test_absolute_path_rejected` (225), `test_upstream_wrong_sha_fails` (453), `test_malformed_row_fails` (164), `test_duplicate_path_fails` (174), `test_bad_hash_fails` (184), `test_native_with_hash_fails` (194), `test_prefix_rewrite_positive` (407), `test_report_exits_0_on_malformed` (261). Plus 7 extras beyond spec (clean-corpus-Aprime, upstream_sha256-forge, writer-not-reanchored, mode-U matching-SHA, well-formed-zero-errors, dot/empty-path). **No MISSING test rows.** Suite verified independently: 21/21 PASS via `uv run python laf-adaptation/scripts/test_check_boundary.py`. |
| 11 | Task file structure — phase order | PASS | 6 phases in spec §7 order: Phase 1 (Baseline + Harness) → Phase 2 (CH-6 + CH-4) → Phase 3 (CH-1 + CH-3 + CH-2) → Phase 4 (CH-5 + CH-7) → Phase 5 (CH-8) → Phase 6 (Verify + QA + Reflect). Phase 2 honors "CH-6 first" because it changes `parse_manifest` signature. No phases skipped or reordered. |
| 12 | Task file structure — item-level ordering | PASS | Within Phase 2: CH-6 (2.1) lands BEFORE CH-4 (2.2) per spec §7. Within Phase 3: CH-1 (3.1) executed AFTER OQ-1 resolution despite being listed first — Task Log records OQ-1 was pre-resolved before any Phase 3 coding. Within Phase 4: CH-5 (4.1) before CH-7 (4.2). Within Phase 5: REQUIRED doc-only (5.1) before DEFERRED Option B (5.2). |
| 13 | Task file structure — items checked/no skips | PASS | 13 implementation items marked `[x]` (1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 3.3, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2). 3 QA-gate items marked `[ ]` (6.3, 6.4, 6.5) — expected, this IS the current QA pass (6.3) plus the subsequent reflect wrapper (6.4) and status-flip (6.5). No item silently skipped; 5.2 explicitly DEFERRED with rationale. |
| 14 | OQ-1 CORRECTION recorded, not silent | PASS | OQ-1 CORRECTED recorded in 3 places: (a) `## Resolutions (OQ-1 through OQ-4)` block — "CORRECTION after empirical verification... the spec §4.1 formula was acknowledged-ambiguous and the version first recorded here was WRONG"; (b) `### Phase Findings → Phase 3` — "CRITICAL CORRECTION during implementation... Had that formula shipped, the gate would have FALSE-POSITIVE-FAILED on the entire clean corpus"; (c) `laf-adaptation/VENDOR.md` Hash semantics section — "the checker applies the INVERSE prefix rewrite (`laf-adaptation:` → `creative-writing-skills:`) to the on-disk adopted body". The correction is the antithesis of silent drift. |
| 15 | Header/separator detection (spec §4.6 sketch refinement) | PASS (NECESSARY DEVIATION) | Spec sketch had `set(path) <= set("-: ")`. Executor refined to `is_separator = len(path) >= 1 and set(path) <= {"-"}` (line 613). This was a Phase-2 rf-qa fix (F-2): the spec's `set(path) <= set("-: ")` admits the empty string (set() ⊆ every set), silently swallowing empty-path rows. Code comment (line 604-611) explicitly documents the deviation and the regression it closes. Necessary strengthening, not drift. |

---

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (CH-5 tarball-fallback semantics)
- Issues fixed in-place: 0 (`fix_authorization: false` — report only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `check_boundary.py:511-519` (`verify`, Mode U HEAD-pin block) | Spec §4.5 specifies `--upstream-sha` as a FALLBACK when git is unavailable (e.g. tarball checkout): "fall back to accepting an explicit `--upstream-sha`... if neither is available, fail loud." The executor's implementation ALWAYS emits the "could not read HEAD... pass --upstream-sha" error when `_checkout_head` returns None, even when `--upstream-sha` is already passed. The tarball-use-case from spec §4.5 is therefore not honored — a user with a tarball checkout and `--upstream-sha` set still FAILS Mode U. The deviation is strictly strengthening (never silently trusts the tree) and the error message even directs the user to pass `--upstream-sha`, so the security model is intact; only the tarball usability path from the spec is missing. | Optional (does not block this gate): in the `head is None` branch, check whether `upstream_sha` was explicitly passed and, if so, treat the pin as asserted-by-flag and proceed to Rules B/C (skip the HEAD comparison) rather than failing. If left as-is, document the deviation in the spec's §6 Q-resolution log or VENDOR.md so future maintainers know the tarball path is intentionally unsupported. |

---

## Recommendations

- **This lens PASSES.** The remediation diff conforms to every spec §4.x sketch in intent. The CH-1 correction is the headline deviation and it is fully justified, empirically verified, and documented in three places — exactly the disposition the spec's §6 Q1 BLOCKER demanded.
- Issue #1 (CH-5 tarball fallback) is non-blocking. If the maintainer wants to honor the spec's tarball-use-case, the fix is a 3-line conditional; otherwise the deviation should be recorded in the OQ-4 resolution so it's not re-litigated. The CH-5 security contract (no silent trust) is preserved either way.
- The remaining 5 lenses (internal-consistency, evidence-quality, actionability, crossref-chain-integrity, security-boundary-correctness) should run in parallel as scheduled; this lens's PASS does not pre-empt them.

---

## Confidence

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 (spec, TASK file, full diff, check_boundary.py, test_check_boundary.py, boundary.yml) | Grep: 9 (CH-1 through CH-8 cross-checks + test plan coverage + error wordings + CH-3 placement) | Glob: 0 | Bash: 4 (git diff, run test suite 21/21, run gate exit 0, run --report exit 0, phase/item counting)

  No web research performed — all verification was source-truth (local files + spec + test execution). Tavily-first rule not triggered.

---

## QA Complete
