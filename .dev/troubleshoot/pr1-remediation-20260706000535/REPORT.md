# Troubleshoot Report — PR #1 High/Medium Remediation

**Target**: Remediate H1 + M1/M2/M3 from `.dev/reviews/pr-1-20260705134814/REVIEW.md`
**Tier reached**: 1 (re-grounding of an already-grounded auggie-review; single-domain, high-confidence)
**Confidence**: 0.93
**Fix authorized**: yes (`--fix`)
**Source**: `/sc:troubleshoot "Review and remediate the high and medium issues. --fix"`

---

## Summary

All four findings re-verified against the live tree. Three (H1, M1, M3) have deterministic, low-risk fixes ready to apply. **M2 (text-normalized hashing) is a genuine contract decision requiring your input** — empirically confirmed that CRLF and LF files hash identically under the current `sha256_text` pipeline, but the fix is a breaking manifest-wide rehash (Option A) versus a docs-alignment (Option B). I recommend Option B for 0.1 and will not apply either without your call.

The fixes are independent and can be applied atomically or in any order. H1 is the only one with new test coverage.

## Diagnosis (per finding)

### H1 — `manifest_covers` class-agnostic globs (HIGH → fix ready)
Re-verified: `manifest_covers` (`check_boundary.py:296`) matches any `/**` row regardless of class. Rule A hash-checks only `is_adopted` rows (line 500); Rule D covers only the quartet (line 604). The parser emits `/**` only for NATIVE/BUILD-NEW skills (line 407) but **imposes no parse-time restriction** — a hand-edited `agents/**` row would be accepted. Confirmed no regression test exists for this. **Fix**: parse-time glob restriction (skills-only + NATIVE/BUILD-NEW only) + class-aware `manifest_covers` + 3 regression tests.

### M1 — CI doesn't run test suite (MEDIUM → fix ready)
Re-verified: `boundary.yml:49-54` has only the verify step. `test_check_boundary.py` (25 tests) runs nowhere in CI/hooks. **Fix**: add one workflow step. Does not violate ADR-006 (the "one script" rule is about runtime; this is test-time for the boundary tool itself).

### M2 — Text-normalized hashing (MEDIUM → CONTRACT DECISION)
**Empirically confirmed** (ran `/tmp/crlf_test.py`): `read_text` normalizes CRLF→LF, so `sha256_text` produces identical hashes for CRLF and LF content (`3ff7e685...` both), while `sha256_bytes` distinguishes them. The contract claims "byte-identical" but is text-normalized. Two resolutions, both legitimate:
- **Option A** — byte-accurate: rewrite 8 hash sites + byte-level prefix rewrite + recompute all 64 manifest hashes via `--init`. Breaking, higher fidelity.
- **Option B (recommended)** — align docs to "text-normalized (LF) integrity," add a test pinning the normalization as intended. Docs-only, zero functional risk.

### M3 — writer.md Mode-V residual comment (MEDIUM/LOW → fix ready)
Re-verified: the residual is documented at `check_boundary.py:517`, `boundary.yml:27-33`, `CLAUDE.md`, `VENDOR.md`, and in two named regression tests. **Fix**: comment-only — add a writer.md/OQ-4 pointer at the `else` block (line 598). Zero behavior change.

## Evidence (all re-grounded this turn)

| Claim | File:line | Verified |
|---|---|---|
| manifest_covers class-agnostic | `check_boundary.py:296-302` | Read |
| is_glob = endswith("/**") | `check_boundary.py:177-178` | Read |
| parser only emits /** for NATIVE/BUILD-NEW (no gate) | `check_boundary.py:407`, `266-274` | Read |
| Rule A iterates is_adopted only | `check_boundary.py:499-507` | Read |
| Rule D = quartet only | `check_boundary.py:603-608` | Read |
| CI has no test step | `.github/workflows/boundary.yml:49-54` | Read |
| CRLF==LF under sha256_text | `/tmp/crlf_test.py` output | Ran |
| 8 sha256_text call sites | `check_boundary.py:382,383,396,397,403,506,526,573` | Grep |
| writer.md residual documented | `check_boundary.py:517`, `boundary.yml:27-33` | Read |
| 25 tests pass | `uv run python scripts/test_check_boundary.py` → OK | Ran |

## Proposed Fix

Four fix proposals written to `fix-proposals/`:
1. `fix-1.md` — H1: parse-time glob restriction + class-aware `manifest_covers` + 3 tests
2. `fix-2.md` — M1: add `test_check_boundary.py` step to `boundary.yml` (+ optional pre-commit)
3. `fix-3.md` — M2: **OPTION A vs OPTION B decision** (byte-accurate vs docs-align) — needs you
4. `fix-4.md` — M3: comment-only writer.md/OQ-4 pointer at line 598

## Risk + Rollback
- H1: additive hardening; live manifest has no `agents/**` rows, so `verify()` stays green. Rollback = revert the parse-time block + test class.
- M1: zero-risk (test already passes). Rollback = delete the workflow step.
- M2-A: rehash must use the correct upstream SHA; rollback = revert + restore old manifest hashes.
- M2-B: docs-only, no rollback risk.
- M3: comment-only, no rollback risk.

## Decision required before I build the task file

**M2 — which option?** (A: byte-accurate breaking rehash · B: docs-align, recommended)

If you pick B (or "skip M2 for now"), I'll build the task file covering H1 + M1 + M3 (+ M2-B if chosen) and hand you the `/task` command. If you pick A, the task also includes the `--init` rehash against the pinned upstream SHA — note that requires the upstream checkout available locally.

## Next Steps
- Confirm M2 option (A / B / skip).
- I build the MDTM task file via `task-builder`, run `/sc:reflect --type task --analyze`, and surface the `/task <path>` command for you to execute (I will not auto-execute).
- After you run `/task`, you run `/sc:reflect --type task --validate` as the pre-commit gate.

<!-- SC:TROUBLESHOOT:SUMMARY
status: success
tier_reached: 1
confidence: 0.93
escalation_reason: none
hypothesis_count: 4
adversarial_invoked: false
fix_authorized: true
duration_sec: ~300
caller: none
context_path: none
return_contract_path: none
-->
