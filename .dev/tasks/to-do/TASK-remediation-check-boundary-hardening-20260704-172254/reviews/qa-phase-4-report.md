# QA Report — Phase 4 Gate (CH-5 Mode-U HEAD pin + CH-7 prefix-rewrite positive test)

**Topic:** PR-1 remediation — Phase 4 (CH-5 + CH-7) verification
**Date:** 2026-07-04
**Phase:** synthesis-gate / phase-gate (code+test verification)
**Fix cycle:** 1
**Driving spec:** `.dev/reviews/pr-1-20260704125705/remediation-spec.md` §4.5, §4.7, §5
**Fix authorization:** true

---

## Overall Verdict: PASS (after 2 in-place fixes)

Two issues found and fixed: one IMPORTANT vacuous test-assertion (`test_upstream_matching_sha_passes_head_check` would false-pass on a CH-5 regression) and one MINOR latent pin-parsing defect (`parse_upstream_sha` treated the em-dash `NO_HASH` placeholder as a truthy pin). Both fixed; full suite + verify + report re-run green; file scope unchanged (only `check_boundary.py` modified + `test_check_boundary.py` new).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | CH-5 block placement BEFORE Rules B/C | PASS | `check_boundary.py:496` `if upstream_dir:` → CH-5 at 497–515 → Rule B at 516 → Rule C at 527. Verified by grep + Read of the block. |
| 2 | CH-5 block INSIDE `if upstream_dir:` (zero Mode-V cost) | PASS | Block at 497–515 is nested under `if upstream_dir:` at 496; the `else` at 547 prints the "Rules B and C skipped" note. Mode V never invokes `_checkout_head`. |
| 3 | `_checkout_head` returns None on failure (not silent trust) | PASS | `check_boundary.py:147–159`. `try/except (FileNotFoundError, CalledProcessError, TimeoutExpired)` → `return None`. Caller at 508–512 FAILS loud when `head is None`. Probed non-git dir → returns None. |
| 4 | `_checkout_head` subprocess injection safety | PASS | List-form `subprocess.run(["git","-C",...,  "rev-parse","HEAD"], ...)` — no `shell=True`, no string interpolation. `check=True` + `timeout=10`. Path resolved via `Path(upstream_dir).resolve()`. Injection not possible. |
| 5 | `_checkout_head` timeout / edge handling | PASS | `timeout=10` set; `TimeoutExpired` caught. Empty stdout → `return head or None`. |
| 6 | `verify(upstream_dir, upstream_sha)` signature | PASS | `check_boundary.py:442` `def verify(upstream_dir=None, upstream_sha=None) -> int:`. Backward-compatible defaults (Mode V callers unaffected). |
| 7 | `do_init(upstream_dir, upstream_sha)` signature + post-write verify() threading | PASS | `check_boundary.py:345` `def do_init(upstream_dir: str, upstream_sha=None)`. Line 421 `return verify(upstream_dir, upstream_sha)` — passes the pin through. No signature mismatch. |
| 8 | `--upstream-sha` argparse addition + main() threading | PASS | `check_boundary.py:642–644` argparse flag; line 651 `do_init(args.upstream, args.upstream_sha)`; line 654 `verify(args.upstream, args.upstream_sha)`. Both paths thread the flag. |
| 9 | `parse_upstream_sha` (Phase 2 helper used by CH-5) | PASS (after fix) | `check_boundary.py:278–294`. Reads `upstream_sha:` header line. FIXED: now treats em-dash `NO_HASH` as unset (returns None) — was previously truthy, would have masked the "no pin" branch. |
| 10 | CH-5 pin-source precedence (`--upstream-sha` > VENDOR.md) | PASS | `check_boundary.py:503` `pinned = upstream_sha or parse_upstream_sha(...)`. Explicit flag wins. |
| 11 | CH-5 three failure branches reachable & tested | PASS | Probe confirms wrong-sha → HEAD-mismatch branch; `test_patched_class_off_writer_fails_mode_u` exercises no-pin/no-HEAD branches (fixture upstream is not a git repo). |
| 12 | CH-7 `test_prefix_rewrite_positive` non-vacuous | PASS | Test asserts 4 meaningful sub-properties: (a) `raw != rewritten`, (b) `creative-writing-skills:` absent from rewritten, (c) `laf-adaptation:` present, (d) `sha256(raw) != laf_sha` (skip-rewrite fails Rule B). Probed all 4 → True. Not tautological. |
| 13 | CH-7 test-only (no `check_boundary.py` source change for M5-A) | PASS | Spec §4.7 Option M5-A (test fixture) chosen. `test_check_boundary.py:400–422` is the test; no `do_init` rewrite logic added. |
| 14 | `test_upstream_wrong_sha_fails` (spec §5 row) | PASS | `test_check_boundary.py:453–460`. Asserts rc != 0 + "HEAD" in stderr. Probe confirms HEAD-mismatch branch fires. |
| 15 | `test_prefix_rewrite_positive` (spec §5 row) | PASS | `test_check_boundary.py:407–422`. See check #12. |
| 16 | Full suite green | PASS | `uv run python laf-adaptation/scripts/test_check_boundary.py` → 21/21 tests OK, exit 0. |
| 17 | Verify mode (Mode V) on real tree | PASS | `uv run python laf-adaptation/scripts/check_boundary.py` → "BOUNDARY CONTRACT: PASS", exit 0. |
| 18 | `--report` mode contract | PASS | `uv run python laf-adaptation/scripts/check_boundary.py --report` → exit 0, 64 rows summarized. |
| 19 | File scope: only check_boundary.py modified + test_check_boundary.py new | PASS | `git status --short laf-adaptation/` shows exactly `M .../check_boundary.py` + `?? .../test_check_boundary.py`. No other files touched. |
| 20 | `test_upstream_matching_sha_passes_head_check` assertion soundness | PASS (after fix) | FIXED: was `assertNotIn("HEAD", err.split("BOUNDARY")[0])` — inspected only the always-empty preamble before the "BOUNDARY CONTRACT" banner, so a HEAD-mismatch regression landing in the violation list would false-pass. Now asserts `assertNotIn("HEAD", err)` over the full stderr. |

---

## Summary

- Checks passed: 20 / 20 (after fixes)
- Checks failed: 0
- Critical issues: 0
- Important issues: 1 (fixed) — vacuous test assertion
- Minor issues: 1 (fixed) — em-dash pin-parsing latent defect
- Issues fixed in-place: 2

## Confidence

- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 1 | Glob: 0 | Bash: 11 (suite/gate runs + targeted probes)
- No web/Tavily lookups required (all verification was local source-truth).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `test_check_boundary.py:474–475` (`test_upstream_matching_sha_passes_head_check`) | Vacuous assertion. `assertNotIn("HEAD", err.split("BOUNDARY")[0])` inspects only the text BEFORE the first "BOUNDARY CONTRACT" banner. In both pass AND fail cases that preamble is empty (`''`) because stderr begins with "BOUNDARY CONTRACT: FAIL/PASS". A CH-5 HEAD-mismatch regression would appear in the post-banner violation list and the test would FALSE-PASS — defeating the test's stated intent ("the CH-5 HEAD-mismatch error must NOT be among them"). | Replace with `assertNotIn("HEAD", err)` over the full stderr stream. Verified the matching case emits no "HEAD" token anywhere, so the stronger assertion still passes for the right reason. |
| 2 | MINOR | `check_boundary.py:278–289` (`parse_upstream_sha`) | Latent pin-parsing defect. The em-dash `NO_HASH` placeholder (`—`) used in test fixtures (and a possible "unset" sentinel) was returned as a truthy pin string. With `pinned = upstream_sha or parse_upstream_sha(...)`, a header `upstream_sha: —` would skip the "no pin" branch and produce a misleading HEAD-mismatch error instead of the clearer "no pinned upstream_sha" failure. Spec §4.5 requires "If neither yields a pin... fail loud (do not silently trust the tree)" — the em-dash was being silently trusted as a pin. | Treat `NO_HASH` (em-dash) as unset: `if val and val != NO_HASH: return val`. Now `parse_upstream_sha('upstream_sha: —')` returns None → "no pin" branch fires correctly. |

---

## Actions Taken

1. **Fixed Issue #1** in `laf-adaptation/scripts/test_check_boundary.py` `test_upstream_matching_sha_passes_head_check`: replaced the preamble-only assertion with a full-stream `assertNotIn("HEAD", err)` plus a descriptive failure message including the full stderr. **Verified** by capturing the matching-case stderr — contains no "HEAD" token anywhere, so the stronger assertion holds; and by simulating a HEAD-mismatch violation in the post-banner region — the old assertion would have missed it, the new one catches it.
2. **Fixed Issue #2** in `laf-adaptation/scripts/check_boundary.py` `parse_upstream_sha`: added `val != NO_HASH` guard. **Verified** by direct probe: `parse_upstream_sha('upstream_sha: —')` now returns `None` (was `'—'`); `parse_upstream_sha('upstream_sha: abc123')` still returns `'abc123'`; empty header still returns None.
3. **Re-ran full verification** after both fixes:
   - `uv run python laf-adaptation/scripts/test_check_boundary.py` → 21/21 PASS, exit 0.
   - `uv run python laf-adaptation/scripts/check_boundary.py` → BOUNDARY CONTRACT: PASS, exit 0.
   - `uv run python laf-adaptation/scripts/check_boundary.py --report` → exit 0, 64 rows.
4. **Confirmed file scope unchanged**: `git status --short laf-adaptation/` shows only `M check_boundary.py` + `?? test_check_boundary.py`.

---

## Recommendations

- **Phase 4 is green.** All CH-5 acceptance criteria (1–5) and the CH-7 (M5-A) acceptance criterion are satisfied. Safe to proceed to the next phase.
- **Optional follow-up (out-of-scope, not blocking):** the `test_patched_class_off_writer_fails_mode_u` test exercises the CH-5 "could not read HEAD" branch only incidentally (its fixture upstream is not a git repo). A dedicated `test_mode_u_no_pin_fails_loud` and `test_mode_u_non_git_checkout_fails_loud` would give the no-pin and no-HEAD branches direct positive coverage. Filing as a Phase-7 nicety, NOT a Phase-4 gate failure.

## QA Complete
