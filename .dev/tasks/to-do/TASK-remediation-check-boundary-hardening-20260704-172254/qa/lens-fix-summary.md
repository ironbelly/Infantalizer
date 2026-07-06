# Lens-Fix Summary — check_boundary hardening (Phase-6 lens-based QA gate)

**Date:** 2026-07-04
**Scope:** 3 consolidated findings from the Phase-6 lens-based QA gate (security-boundary lens).
**Files in scope:** `laf-adaptation/scripts/check_boundary.py`, `laf-adaptation/scripts/test_check_boundary.py`, `laf-adaptation/VENDOR.md`, `laf-adaptation/CLAUDE.md`, `.github/workflows/boundary.yml`.
**File-scope invariant:** `git status --short laf-adaptation/{agents,skills,kb,agents,templates}` is EMPTY — no adopted body or carried-verbatim payload was touched.

---

## What changed and why

### F1 (CRITICAL) — CH-5 broke the documented `--init` re-vendor flow
**Root cause:** `do_init()` wrote manifest rows via `_write_manifest_rows()` but never updated the `VENDOR.md` `upstream_sha:` header. The post-write `verify()` then ran CH-5's HEAD-pin, comparing the NEW checkout HEAD (the sha being vendored) against the STALE OLD pinned sha still in the header → a legitimate re-vendor spuriously exited 1.

**Fix:**
1. Added `_write_upstream_sha_header(sha)` helper in `check_boundary.py` — idempotently rewrites the first `upstream_sha:` line in `VENDOR.md`, preserving every other line byte-for-byte.
2. In `do_init()`, AFTER `_write_manifest_rows()` and BEFORE the post-write `verify()`, compute `new_pin = _checkout_head(upstream_dir) or upstream_sha` (HEAD precedence, then `--upstream-sha` flag fallback) and write it into the header. If neither source yields a pin, leave the header as-is and let CH-5 fail loud below (the normal git-checkout re-vendor path now succeeds).

**Regression test added:** `test_init_revendor_updates_upstream_sha_header` — builds a fixture upstream git checkout, stamps a STALE header pin, runs `do_init`, asserts (a) exit 0 and (b) the header was rewritten to the checkout HEAD.

### F2 (CRITICAL) — CH-1 two-field forgery untested + docs over-claimed
**Problem A (test gap):** spec §4.1 acceptance bullet 2 required the "mutate body + rewrite BOTH hashes to be self-consistent" attack to be tested. It was not.

**Fix (test):** Added `test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v` to `TrustRootTests`. Mutates an ADOPTED-CLEAN body, forges `upstream_sha256 = sha256(prefix_unrewrite(mutated))` and `laf_sha256 = sha256(mutated)`, asserts `verify() == 0`. The test name (with `PASSES_mode_v` suffix), the docstring, and an inline comment block explicitly name this as a **documented-residual**, not a desired property, and call out the backstops (Mode U + branch protection + mandatory human review of any `upstream_sha256` diff). Asserting `== 0` is CORRECT here — it locks the residual into the suite so a future change cannot accidentally under-claim closure.

**Problem B (doc over-claim):** the docs called Mode V "a malicious-drift gate" without the two-field caveat.

**Fix (docs):** Demoted to honest "single-field `laf_sha256`-forgery gate" language in all three sites:
- `VENDOR.md` — new "What Mode V catches — and what it does NOT (documented honestly, no over-claim)" subsection under Hash semantics, naming the two-field bypass + the three backstops (Mode U / branch protection / human review of `upstream_sha256` diffs).
- `CLAUDE.md` §2 A′ bullet — rewritten to state "single-field `laf_sha256`-forgery gate" + the two-field caveat + pointer to `VENDOR.md` Hash semantics.
- `.github/workflows/boundary.yml` header comment — same demotion.

The docs neither over-claim (single-field forgery IS caught) nor under-claim (two-field forgery is NOT caught by Mode V; the backstops are named).

### F3 (MINOR) — CH-5 tarball/no-git fallback unused
**Root cause:** spec §4.5 wanted `--upstream-sha` to enable Mode U when git is unavailable (tarball checkout). When `_checkout_head` returned `None`, the code always failed even when `--upstream-sha` was passed.

**Fix:** In `verify()`'s CH-5 HEAD-pin block, the HEAD-unreadable error now fires only when `head is None AND upstream_sha is None` (no explicit operator assertion). With an explicit `--upstream-sha`, the HEAD check is skipped (operator has asserted the pin explicitly) and Rules B/C still run against the supplied tree. Security stance preserved: the pin is an operator assertion, never an inference from an unverifiable tree.

**Tests added:**
- `test_mode_u_tarball_with_explicit_sha_skips_head_check` — non-git tmp dir + `--upstream-sha` → no "could not read HEAD" error.
- `test_init_revendor_with_explicit_sha_flag` — `--init` on a tarball checkout with explicit `--upstream-sha` rewrites the header to the explicit pin and exits 0 (F1 + F3 composition).

---

## Boundary-contract posture (each fix STRENGTHENS, never weakens)

| Fix | Direction | Justification |
|----|-----------|---------------|
| F1 | Strengthens | The documented re-vendor flow now actually works; the CH-5 HEAD-pin still fires on a real HEAD mismatch. No check was removed or relaxed. |
| F2 | Strengthens | A previously-undocumented residual (two-field forgery) is now explicitly named in the docs and locked into the test suite. No claim was weakened — the single-field guarantee is restated, the two-field gap is honestly added. |
| F3 | Strengthens (usability, security-neutral) | The explicit `--upstream-sha` flag is now an operator assertion that satisfies the pin requirement; Rules B/C still run against the supplied tree. The fail-loud path is preserved when there is no explicit pin AND no readable HEAD. |

---

## Final green evidence

```
=== TEST SUITE ===
Ran 25 tests in 0.078s
OK

=== VERIFY (Mode V on real clean corpus) ===
BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.
EXIT=0

=== REPORT ===
REPORT_EXIT=0

=== FILE-SCOPE INVARIANT (agents/skills/kb/templates) ===
(empty — no adopted body or carried-verbatim payload touched)

=== Docs over-claim audit ===
grep "malicious-drift" laf-adaptation/ .github/ → 0 hits (over-claim removed)
grep "single-field\|two-field" → 5 hits across VENDOR.md, CLAUDE.md, boundary.yml
  (honest single-field claim + two-field caveat in all three sites)
```

**Test count:** 25 (21 baseline + 4 new).
**Gate exit codes:** verify=0, --report=0.
**Baseline → final:** 21 → 25 tests, both green; verify exit 0 preserved throughout (no false positives on the real clean corpus).
