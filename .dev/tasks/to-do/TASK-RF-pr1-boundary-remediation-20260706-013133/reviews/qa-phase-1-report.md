# QA Report — Phase 1 Gate (H1 glob restriction)

**Topic:** PR #1 boundary-remediation Phase 1 — parse-time glob gate + class-aware `manifest_covers` + `GlobSafetyTests`
**Date:** 2026-07-06
**Phase:** research-gate / fix-cycle (single-phase phase-gate QA on an executed MDTM task)
**Fix cycle:** 1

---

## Overall Verdict: PASS (after 1 in-place fix)

## Items Reviewed

| # | Check (Item / Criterion) | Result | Evidence |
|---|--------------------------|--------|----------|
| 1 | Item 1.1 — gate placement (after class hash-validation, before `rows.append`) | PASS | `check_boundary.py:274-289`; gate block sits between the ADOPTED/NATIVE hash-validation block (266-273) and `rows.append(Row(...))` at 288. |
| 2 | Item 1.1 — rejects `agents/**` (loud error, `continue` not silent drop) | PASS | Re-probe: `agents/** NATIVE` → REJECTED with `must be exactly 'skills/<name>/**'`. `continue` at line 287 prevents `rows.append`. |
| 3 | Item 1.1 — rejects root-level glob `/**` | PASS | `/**` rejected via `_safe_repo_path` absolute-path check ("manifest path is absolute"). Loud, not silent. |
| 4 | Item 1.1 — rejects any ADOPTED-class glob | PASS | `skills/foo/** ADOPTED-CLEAN` and `ADOPTED-PATCHED` both REJECTED with `cannot be ADOPTED`. |
| 5 | Item 1.1 — **rejects bare `skills/**` (covers adopted skills)** | **FAIL → FIXED** | Pre-fix: `skills/** NATIVE` was ACCEPTED (startswith `skills/`). Exploit confirmed end-to-end: delete adopted-skill exact rows + mutate adopted SKILL.md body + add `skills/**` → `verify()==0`, empty stderr. Post-fix: REJECTED; attack now `rc=1`. |
| 6 | Item 1.1 — accepts the legitimate shape `skills/<name>/**` | PASS | `skills/native1/** NATIVE` and `skills/safety/** BUILD-NEW` both ACCEPTED. No false positive on the shape `--init` emits. |
| 7 | Item 1.2 — `manifest_covers` has `and not r.is_adopted` on glob branch | PASS | `check_boundary.py:314`. Direct probe: adopted-glob Row on `agents/critic.md` → False; native-glob → True; adopted-skill-glob → False. |
| 8 | Item 1.3 — `GlobSafetyTests` class with 3 named tests | PASS | `test_check_boundary.py:681-765`. All three present: `test_agents_glob_rejected`, `test_adopted_glob_rejected`, `test_broad_glob_does_not_cover_adopted`. Plus a 4th added during fix-cycle (`test_bare_skills_glob_rejected`). |
| 9 | Item 1.3 — tests meaningfully assert non-zero (not trivially passing) | PASS | Each calls `verify()` and `assertNotEqual(..., 0)`; probes parse_manifest errors too. Confirmed they exercise the gate, not a tautology. |
| 10 | Item 1.1/1.3 — total test count rose 25 → 28 (now 29 post-fix) | PASS | `Ran 29 tests ... OK` (was 28 before the in-place fix added the regression test). |
| 11 | Item 1.1 — live verify still PASS (exit 0) | PASS | `uv run python laf-adaptation/scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS` exit 0 (both before and after the fix). |
| 12 | Boundary contract — no adopted agent/skill body edited | PASS | `git diff --name-only HEAD laf-adaptation/agents/ laf-adaptation/skills/` → empty. Only `scripts/check_boundary.py` and `scripts/test_check_boundary.py` (both NATIVE) changed in this phase. |
| 13 | Adversarial: no path by which an adopted file is silently covered by a glob | **FAIL → FIXED** | Same root cause as #5. Pre-fix the `skills/**` path bypassed hash protection silently; post-fix rejected. Re-ran the full end-to-end attack → now `rc=1`. |

## Summary
- Checks passed: 12 / 13 (13/13 after in-place fix)
- Checks failed: 1 (CRITICAL) — found and fixed
- Critical issues: 1 (FIXED)
- Issues fixed in-place: 1 (1 code fix + 1 regression test)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `check_boundary.py` glob-shape gate (was lines 279-287) | Prefix-only check `path.startswith("skills/")` admitted `skills/**` (no `<name>` segment). `skills/**` matches every skill dir via `manifest_covers`, so deleting an adopted skill's exact ADOPTED-CLEAN hash rows and replacing them with one `\| skills/** \| NATIVE \| — \| — \|` row silently drops the adopted skill's hash protection — the exact H1 silent-coverage attack item 1.1 exists to prevent. Verified end-to-end: mutated adopted SKILL.md body → `verify()==0`, empty stderr. Item 1.1 Output explicitly requires rejecting this class of shape ("only `skills/<name>/**` is allowed"); fix-1.md Part A spec requires "a single non-empty skill name segment." | Tighten gate to require `glob_prefix.startswith("skills/") and glob_prefix.count("/") == 1` (single-level name). Add regression test `test_bare_skills_glob_rejected`. |

## Actions Taken

- **Fixed** (Finding #1): replaced the prefix-only check in `parse_manifest` with a single-level-name check. New gate logic (`check_boundary.py:274-295`):
  ```python
  glob_prefix = path[:-3]  # strip the trailing '/**'
  if not glob_prefix.startswith("skills/") or glob_prefix.count("/") != 1:
      errors.append(... "must be exactly 'skills/<name>/**' ...")
      continue
  ```
  Comment block expanded to document WHY the prefix-only check is insufficient (bare `skills/**` covers adopted skills).
- **Added regression test** `test_bare_skills_glob_rejected` to `GlobSafetyTests` (`test_check_boundary.py:727-738`) pinning the rejection so this cannot regress.
- **Verified the fix** by three independent means:
  1. Full suite: `Ran 29 tests ... OK` (was 28 pre-fix; +1 from the new regression test).
  2. Live verify: `BOUNDARY CONTRACT: PASS` exit 0 (no false positive on the real manifest).
  3. End-to-end exploit re-run: the exact pre-fix attack (delete adopted-skill rows + add `skills/**` + mutate adopted body) now returns `rc=1` with a loud error naming the illegal glob.

## Confidence

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 9 (suite run, live verify, diff scope, 3 adversarial probe sets, post-fix re-probe, post-fix exploit re-run, post-fix suite re-run)
- Every checklist item verified with tool evidence; no item relies on agent self-report.

## Recommendations
- Green light to proceed to Phase 2 (M1 CI/pre-commit wiring). The H1 silent-coverage hole is now closed at both the parse gate and the `manifest_covers` predicate, with regression coverage pinning both.

## QA Complete
