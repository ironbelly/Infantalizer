# QA Report — Phase 3 (CH-1 trust-root + CH-3 writer-only + CH-2 resources/**)

**Topic:** Harden `laf-adaptation/scripts/check_boundary.py` — verify-mode coverage (CH-1 H1 trust-root, CH-3 M1 writer-only patch, CH-2 H2 resources/**)
**Date:** 2026-07-04
**Phase:** synthesis-gate-style adversarial phase-gate QA on executed remediation code (Phase 3 of TASK-remediation-check-boundary-hardening-20260704-172254)
**Fix cycle:** N/A (first pass)

---

## Overall Verdict: PASS

Phase 3 lands the H1 trust-root fix (CH-1), the M1 writer-only patch constraint (CH-3), and the H2 `resources/**` coverage extension (CH-2). All three are independently verified correct against the real 64-row corpus, both required test surfaces, and four live attack simulations. The executor's empirically-corrected H1 formula (`sha256(prefix_unrewrite(disk)) == upstream_sha256`) is mathematically sound, holds exhaustively across all 55 ADOPTED-CLEAN rows (including all 10 literal-bearing agent rows where the inverse is non-trivially exercised), and the gate stays green on the clean tree. No issues found. No fixes applied.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | **H1 corrected math (CRITICAL)** — recompute `sha256(prefix_unrewrite(disk))` independently across ALL 55 ADOPTED-CLEAN rows; expect 0 mismatches vs VENDOR.md `upstream_sha256` | PASS | Scratch verifier `_qa_phase3_verify.py` (since removed) recomputed the hash for all 55 rows directly from disk via `hashlib.sha256` + the module's `prefix_unrewrite`: **55/55 equal, 0 mismatches**. Diverse sample spans `agents/brainstormer.md` (executor's claimed spot-check), `agents/editor.md` ("never modified" invariant), `agents/critic.md` (quartet), `skills/.../SKILL.md`, `skills/.../resources/*.md`, and `skills/.../resources/prose-critique/analyze.py` (a `.py` resource). |
| 2 | **Inverse is genuinely exercised on real data** — confirm the formula is non-trivial for at least some rows (else "pass" is vacuous) | PASS | Of 55 ADOPTED-CLEAN rows, **10 have `upstream_sha256 != laf_sha256`** (all 10 are `agents/*.md` that contain the rewritten `laf-adaptation:` literal). For these 10, `prefix_unrewrite` MUST recover the raw upstream — and it does (Check 1). The other 45 are no-literal files where the inverse is correctly a no-op (`disk == raw_upstream`, `laf == upstream`). So the formula is provably exercised on the literal-bearing class. |
| 3 | **Inverse-breaker hunt** — does any ADOPTED-CLEAN file contain a `laf-adaptation:` literal NOT originating from rewriting `creative-writing-skills:` (which would break the inverse)? | PASS | `grep -rln "laf-adaptation:" laf-adaptation/{agents,skills}/`: 15 agent files (incl. 11 adopted) carry the literal; **0 skill files** (incl. all `resources/**`) carry it. For all 11 adopted agent files the inverse recovers the manifest `upstream_sha256` exactly (Check 1) — proving every `laf-adaptation:` literal in the adopted corpus IS the result of the uniform `creative-writing-skills:` rewrite, not an authored-as-`laf-adaptation:` literal. No inverse-breaker exists in the corpus. |
| 4 | **Forward-inverse composition** — `prefix_unrewrite(prefix_rewrite(x)) == x` (algebraic sanity) | PASS | Direct check: `prefix_unrewrite(prefix_rewrite("test creative-writing-skills: foo")) == "test creative-writing-skills: foo"` → True. The functions are exact string inverses. Also confirmed `prefix_rewrite` is idempotent on already-rewritten disk (`prefix_rewrite(disk) == disk` for the literal-bearing `brainstormer.md`), which is why the spec's original WRONG formula (`sha256(prefix_rewrite(disk))`) collapses to `laf_sha256` — confirming the executor's diagnosis of why the spec formula would have false-positive-failed the entire corpus. |
| 5 | **CH-1 attack sim A — forged `upstream_sha256`** (rewrite field to `0*64` on a clean row) → must FAIL | PASS | Scratch verifier rewrote `agents/critic.md`'s `upstream_sha256` cell to `0*64` in the manifest, leaving disk untouched, then ran `verify()`: **rc=1**, error `agents/critic.md: body no longer matches pinned upstream_sha256 — raw-upstream hash mismatch (CH-1; laf_sha256 rewrite detected)`. Manifest restored after. |
| 6 | **CH-1 attack sim B — laf-only rewrite of edited body** (the actual H1 attack: mutate body AND rewrite only `laf_sha256` to match) → must FAIL | PASS | Scratch verifier appended `\nMALICIOUS APPENDIX\n` to `agents/editor.md`, rewrote only its `laf_sha256` cell to match the mutated body, ran `verify()`: **rc=1** (Rule A passes — the new hash matches the new body — but Rule A′ fails — the body no longer inverts to the pinned `upstream_sha256`). Files restored after. This is the precise attack H1 describes, and it is now caught. |
| 7 | **CH-2 attack sim — untracked file in adopted skill `resources/`** → must FAIL | PASS | Live test against the REAL tree: created `laf-adaptation/skills/story-review/resources/qa-sneaky-test.md` (empty), ran `check_boundary.py`: **rc=1**, error `skills/story-review/resources/qa-sneaky-test.md: adopted-skill file not in VENDOR.md manifest`. Removed the file; gate green again. This is the precise H2 attack and it is now caught on the real corpus, not just the fixture. |
| 8 | **Rule A′ (CH-1) placement** — runs unconditionally, BEFORE the `if upstream_dir:` block (so it executes in Mode V/CI) | PASS | `check_boundary.py:451–473` — Rule A′ block is at top level of `verify()`, lines 481+ hold the `if upstream_dir:` block. Confirmed by direct read of the source. |
| 9 | **Rule C′ (CH-3) placement** — runs unconditionally, BEFORE the `if upstream_dir:` block (so it executes in Mode V AND Mode U) | PASS | `check_boundary.py:474–478` — Rule C′ block is at top level of `verify()`, before `if upstream_dir:` at line 481. |
| 10 | **Rule C′ actually fires in Mode U** (the critical "outside the block" proof) | PASS | Mode-U replication: built a fixture upstream tree + an off-writer `ADOPTED-PATCHED` row, ran `verify(upstream_dir)`. The error `agents/critic.md: ADOPTED-PATCHED is reserved for agents/writer.md only` was emitted. If C′ were inside the `if upstream_dir:` block this would still fire, but the placement check (#9) structurally proves it's outside; this test confirms it executes correctly when an upstream tree IS present (i.e. C′ did not get moved inside a sub-block). |
| 11 | **Rule F′ (CH-2) placement** — runs unconditionally, AFTER the `if upstream_dir:` block (uses only disk + manifest) | PASS | `check_boundary.py:548–562` — Rule F′ block is at top level of `verify()`, after the `else:` clause at line 513 closes the upstream branch. Uses `disk_skill_dirs()` + `disk_skill_files()` + `manifest_covers()` — no upstream dependency. |
| 12 | **Rule F′ `adopted_skill_dirs` derivation correctness** | PASS | Line 554–557: `{r.path.split("/")[1] for r in rows if r.path.startswith("skills/") and r.is_adopted}`. For `skills/story-review/resources/prose-critique.md` → split = `["skills","story-review","resources","prose-critique.md"]` → `[1] = "story-review"`. Correct. The `is_adopted` property covers `ADOPTED-CLEAN` + `ADOPTED-PATCHED` (conservative; no PATCHED skill rows exist in corpus). Glob rows (`skills/native1/**`) are excluded by `is_adopted` (NATIVE/BUILD-NEW), so the derivation correctly targets only adopted skill dirs. |
| 13 | **ADOPTED-PATCHED (writer.md) structural exclusion from A′** — code-level, not just comment | PASS | Line 463: `if r.cls != "ADOPTED-CLEAN": continue`. Writer.md is `ADOPTED-PATCHED`, so it is skipped. Direct measurement: `sha256(prefix_unrewrite(writer_disk)) = 4de6bbe1…` ≠ manifest `upstream_sha256 = 373e605b…` (writer's additive frontmatter survives unrewrite), confirming writer **cannot** be A′-anchored and the skip is necessary, not a weakness. Writer's absolute guarantee remains Mode-U Rule C (unchanged). |
| 14 | **Test non-vacuity — fail-tests flip when their rule is removed** | PASS | Manually replicated each test scenario with the rule stubbed off: (a) A′-skip + body-edit-attack → rc flips 1→0 (A′ is sole catcher); (b) A′-skip + upstream-forge → rc flips 1→0 (A′ is sole catcher); (c) C′-skip + off-writer-PATCHED Mode V → flips 1→0; (d) C′-skip + off-writer-PATCHED Mode U → flips 1→0; (e) F′-skip + deleted-resource-row → flips 1→0; (f) F′-skip + untracked-resource → flips 1→0. All 6 fail-tests are non-vacuous. (Initial `unittest`-based vacuity probe produced 3 false alarms due to module re-import rebinding `cb.verify`; manual direct-call replication is the authoritative evidence and is recorded here.) |
| 15 | **Required test names exist + pass** | PASS | All 8 named tests present in `test_check_boundary.py` and pass when run individually by class-qualified name (`TrustRootTests.test_adopted_body_edit_plus_laf_hash_rewrite_fails`, `test_upstream_sha256_rewrite_of_clean_body_fails`, `test_clean_corpus_still_passes_under_Aprime`, `test_writer_is_not_reanchored_in_mode_v`; `WriterOnlyPatchTests.test_patched_class_off_writer_fails_mode_v`, `..._mode_u`; `ResourcesCoverageTests.test_adopted_resource_row_deleted_fails`, `test_untracked_adopted_resource_fails`). |
| 16 | **Real gate green (Mode V, clean tree)** — corrected formula must NOT false-positive | PASS | `uv run python laf-adaptation/scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` exit 0. |
| 17 | **`--report` green** (contract preserved) | PASS | `uv run python laf-adaptation/scripts/check_boundary.py --report` → exit 0. |
| 18 | **Full test suite green (18 tests)** | PASS | `uv run python laf-adaptation/scripts/test_check_boundary.py` → `Ran 18 tests in 0.027s / OK`. |
| 19 | **File-scope invariant** — only `check_boundary.py` modified + `test_check_boundary.py` added | PASS | `git status --short laf-adaptation/` → `M scripts/check_boundary.py` + `?? scripts/test_check_boundary.py`. No adopted body, no `kb/tiers/*.yaml`, no `templates/*`, no fenced-block skill resource touched. (The diff against `start_commit b51633d` shows the entire LAF 0.1 tree because that commit predates the LAF work; the working-tree status is the correct Phase-3 scope indicator.) |
| 20 | **No over-claiming comments** (CH-1's ADOPTED-PATCHED carve-out must be honestly described in code; full doc alignment is item 5.1, a LATER phase, so doc prose is NOT in scope here) | PASS | `grep -nE "absolute|always|every|never|complete|all adopted"` against the CH-1/CH-3/CH-2-relevant matches in `check_boundary.py` → no over-claiming language. The Rule A′ comment (lines 451–461) explicitly states ADOPTED-PATCHED is "intentionally excluded" and that "its absolute guarantee is Mode-U Rule C" — accurate, not over-claiming. |
| 21 | **No weakening of adopted-file integrity** — every change is strictly additive (a new rule that can only ever ADD errors, never suppress them) | PASS | A′ (lines 451–473) only appends to `errors`; never removes. C′ (lines 474–478) only appends. F′ (lines 548–562) only appends. No prior rule (A, B, C, D, E, F) was modified to be more permissive. `prefix_unrewrite` is a new helper that does not affect any existing code path. |

## Summary

- Checks passed: **21 / 21**
- Checks failed: **0**
- Critical issues: **0**
- Important issues: **0**
- Minor issues: **0**
- Issues fixed in-place: **0** (no fixes needed)

## Issues Found

None.

## Actions Taken

None. No fixes were required.

## Recommendations

- **Phase 3 is GREEN.** Proceed to Phase 4 (CH-5 Mode-U HEAD pin + CH-7 prefix-rewrite positive test).
- **Carry-forward note for item 5.1 (doc alignment, LATER phase):** when VENDOR.md header / CLAUDE.md §2 / boundary.yml comment are updated, they must state that Mode V now re-anchors all ADOPTED-CLEAN integrity to the pinned `upstream_sha256` (catches single-field `laf_sha256` forgery), AND that the absolute upstream-checkout guarantee for the single ADOPTED-PATCHED row (writer.md) and for any future literal-bearing body still requires Mode U (Option B, deferred per OQ-4). The code already encodes this honestly; the doc phase must match.
- **Carry-forward note for OQ-1 resolution text in TASK file:** the "Resolutions" entry already records the empirical correction. Recommend the resolution also explicitly note that 10/55 ADOPTED-CLEAN rows are literal-bearing (so the inverse is non-trivially exercised — guards against a future reader assuming "the inverse is always a no-op on this corpus").
- **No regression risk observed.** The corrected formula's soundness is now backed by: (a) algebraic proof (forward-inverse composition), (b) exhaustive empirical verification across all 55 rows, (c) two live attack simulations both caught, (d) the gate green on the real clean tree.

## Confidence

- **Confidence:** Verified: 21/21 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 (task file, spec, check_boundary.py, test_check_boundary.py, VENDOR.md) | Grep: 4 (literal hunt, placement, over-claim, ADOPTED-CLEAN refs) | Glob: 0 | Bash: 9 (gate run, report run, test run, scratch verifier, vacuity probe, mode-U probe, inverse probe, file-scope check, final consolidated check)

## QA Complete
