---
id: "TASK-RF-pr1-boundary-remediation-20260706-013133"
title: "Remediate PR #1 boundary-contract findings (H1 + M1/M2/M3)"
description: "Apply the four reviewed-and-approved fixes from .dev/troubleshoot/pr1-remediation-20260706000535/REPORT.md to the laf-adaptation boundary contract: parse-time glob restriction (H1), CI+pre-commit test runs (M1), docs-align for text-normalized hashing (M2 Option B), writer.md Mode-V comment (M3)."
status: "🟢 Done"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-07-06"
updated_date: "2026-07-06"
start_date: "2026-07-06"
completion_date: "2026-07-06"
assigned_to: "orchestrator"
estimation: "~1.5 hours"
task_type: static
start_commit: "b51633d40a64be488c30edbd0f803dbdc8feadc1"
executor_model_class: "sonnet"
reflect_pre:
  verdict: skipped
  skip_reason: no-spec
  coverage_pct: null
  depth: n/a
  tcs: 14
  run_id: n/a
  report: null
  reviewed_at: "2026-07-06T01:33:00Z"
related_docs:
- path: ".dev/troubleshoot/pr1-remediation-20260706000535/REPORT.md"
  description: "Diagnosis report with per-finding evidence and the four approved fix proposals"
- path: ".dev/troubleshoot/pr1-remediation-20260706000535/fix-proposals/fix-1.md"
  description: "H1: manifest_covers class-aware + glob restriction + regression test (verbatim code)"
- path: ".dev/troubleshoot/pr1-remediation-20260706000535/fix-proposals/fix-2.md"
  description: "M1: run test_check_boundary.py in CI (+ pre-commit)"
- path: ".dev/troubleshoot/pr1-remediation-20260706000535/fix-proposals/fix-3.md"
  description: "M2 Option B: docs-align to text-normalized hashing + CRLF normalization test (NO code/hash change)"
- path: ".dev/troubleshoot/pr1-remediation-20260706000535/fix-proposals/fix-4.md"
  description: "M3: writer.md Mode-V residual comment pointer at the else block"
- path: ".dev/reviews/pr-1-20260705134814/REVIEW.md"
  description: "The original auggie-review that surfaced these findings"
tags:
- boundary-contract
- security-hardening
- remediation
- pr-1
reflect_post:
  verdict: degraded
  status: success
  run_id: ae1184b0e0ae
  tier_reached: 1
  report: /config/workspace/Infantalizer/.dev/tasks/to-do/TASK-RF-pr1-boundary-remediation-20260706-013133/reflect/post/ae1184b0e0ae/t2-swarm/reflect-review-01-qwen3.6-plus.final.md
  contract: /config/workspace/Infantalizer/.dev/tasks/to-do/TASK-RF-pr1-boundary-remediation-20260706-013133/reflect/post/ae1184b0e0ae/return-contract.yaml
  reason: degraded-tier1
  deviations:
    authorized: 0
    necessary: 0
    drift: 0
    regression: 0
  head: ae1184b0e0aebfa29a1f1452f3d47c6a4c35d180
  reviewed_at: '2026-07-06T02:51:29.924575+00:00'
---

# Remediate PR #1 Boundary-Contract Findings (H1 + M1/M2/M3)

## Task Overview

This task applies the four fixes reviewed and approved in the `/sc:troubleshoot` diagnosis at `.dev/troubleshoot/pr1-remediation-20260706000535/REPORT.md`. Three (H1, M1, M3) are deterministic low-risk changes; M2 is **Option B** (docs-align only — no `--init`, no manifest rehash), chosen by the user this turn. The fixes harden the `laf-adaptation` boundary-contract enforcer (`check_boundary.py`), wire its regression suite into CI and the pre-commit hook, align the contract's prose with its text-normalized hashing reality, and document an existing Mode-V residual in the code path that skips it.

All evidence (verbatim code, `file:line`, empirical CRLF test output) lives in the four `fix-proposals/fix-*.md` files — read them before editing; do not re-derive.

## Key Objectives

- **H1 (HIGH)**: Add a parse-time gate rejecting non-`skills/<name>/**` globs and ADOPTED-class globs; make `manifest_covers` class-aware; add `GlobSafetyTests` (3 tests).
- **M1 (MEDIUM)**: Add `uv run python scripts/test_check_boundary.py` as a CI step in `boundary.yml` and as a run in `.githooks/pre-commit`.
- **M2 (MEDIUM, Option B)**: Soften "byte-identical"/"byte-faithful" → "text-normalized (LF) integrity" in `CLAUDE.md`, `VENDOR.md`, `NOTICE`; add `CRLFNormalizationTests` pinning the normalization as intended.
- **M3 (LOW)**: Add a 4-line comment at the Mode-V `else` block naming the writer.md residual + OQ-4.

## Prerequisites & Dependencies

- All fixes are independent; phases may be executed in any order, but the verification phase (Phase 5) MUST run last.
- Pure standard library only (ADR-006). No new runtime deps.
- **Do NOT edit any adopted agent body or adopted SKILL.md body** (boundary contract). The changed `.py`/`.yml`/`.md` files are NATIVE — allowed.
- **Do NOT run `--init` or recompute manifest hashes** (M2 is Option B, docs-only).
- Match existing code style: 4-space indent, FAIL-LOUD comment style (`check_boundary.py:225-247`), `sys.stderr` error reporting.

## Execution Context

- **References:** GOAL = apply H1/M1/M2/M3 fixes from `.dev/troubleshoot/pr1-remediation-20260706000535/REPORT.md`; WHY = harden the boundary-contract keystone against silent hash-protection loss (H1) and close CI/doc gaps (M1/M2/M3); related-docs R-001..R-006 above.
- **Source areas:** `check_boundary.py` parser + `manifest_covers` + hashing helpers; `test_check_boundary.py` test base class; `.github/workflows/boundary.yml`; `.githooks/pre-commit`; NATIVE docs (`CLAUDE.md`, `VENDOR.md`, `NOTICE`).
- **Key constraints:** (1) FAIL-LOUD parser pattern — never silently drop a row; (2) no `--init`/hash recompute; (3) still exactly one runtime script (`test_check_boundary.py` is test-time, not runtime — ADR-006).

---

## Phase 1: H1 — Parse-time glob restriction + class-aware manifest_covers + tests

- [x] **1.1 — Add parse-time glob gate in `parse_manifest`**
  - **Context**: `laf-adaptation/scripts/check_boundary.py:221-275`. The parser validates class-specific hashes at lines 266-273 but imposes NO restriction on glob rows (`path.endswith("/**")`). The shipped `--init` only emits `/**` for NATIVE/BUILD-NEW skills (line 407), but a hand-edited `agents/**` row is accepted, which lets an adopted file lose hash protection silently (Rule A only hash-checks `is_adopted` rows; Rule D covers only the quartet). Follow the FAIL-LOUD style at lines 225-247.
  - **Action**: In `parse_manifest`, immediately AFTER the class hash-validation block (after line 274, before `rows.append`), add:
    ```python
            # Glob-shape gate (H1): glob rows are reserved for NATIVE/BUILD-NEW skill
            # roots of the exact form 'skills/<name>/**'. A hand-edited 'agents/**'
            # or adopted-path glob would let an adopted file be "manifest-covered"
            # by a non-hash row, silently dropping its hash protection (Rule A only
            # hash-checks is_adopted rows; Rule D protects only the quartet).
            if path.endswith("/**"):
                if cls.upper() in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
                    errors.append(f"manifest line {lineno}: glob row {path!r} cannot be "
                                  f"ADOPTED (adopted files need exact hash rows)")
                    continue
                if not path.startswith("skills/"):
                    errors.append(f"manifest line {lineno}: glob row {path!r} must be under "
                                  f"skills/ (only 'skills/<name>/**' is allowed)")
                    continue
    ```
  - **Output**: `parse_manifest` now rejects `agents/**`, root-level `**`, and any ADOPTED-class glob with a loud error.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` still exits 0 on the live tree (no glob rows exist for adopted paths today); a hand-injected `agents/**` row in a tmp fixture fails loud.
  - **Completion gate**: Gate present; live verify still PASS.

- [x] **1.2 — Make `manifest_covers` class-aware (belt-and-suspenders)**
  - **Context**: `laf-adaptation/scripts/check_boundary.py:296-302`. The predicate matches any `/**` row regardless of class. Item 1.1 is the real gate (parse-time), but `manifest_covers` should be self-defending so a future caller can't reintroduce the gap.
  - **Action**: Edit `manifest_covers` to add `and not r.is_adopted` to the glob branch:
    ```python
    def manifest_covers(rows, rel: str) -> bool:
        for r in rows:
            if r.path == rel:
                return True
            if r.is_glob and rel.startswith(r.path[:-2]) and not r.is_adopted:
                # 'skills/x/**' covers 'skills/x/...' — adopted files require exact hash rows
                return True
        return False
    ```
  - **Output**: `manifest_covers` only honors glob coverage from non-adopted rows.
  - **Verification**: Read the function back; confirm the new clause. Existing tests still pass.
  - **Completion gate**: Clause present; no test regression.

- [x] **1.3 — Add `GlobSafetyTests` class to `test_check_boundary.py`**
  - **Context**: `laf-adaptation/scripts/test_check_boundary.py`. `BoundaryTestBase` at lines 56-94 patches `check_boundary.REPO`/`VENDOR_MD` to a tmp dir and writes a VENDOR.md fixture (the `_write_vendor` helper at ~line 81-90). New tests follow the same pattern as `ParserHardeningTests` (line 154) / `WriterOnlyPatchTests` (line 379), which inject raw manifest lines and assert `verify() != 0`.
  - **Action**: Add a new `class GlobSafetyTests(BoundaryTestBase)` with three tests:
    1. `test_agents_glob_rejected` — inject a manifest row `| agents/** | NATIVE | — | — |`, assert `check_boundary.verify() != 0` and the error mentions glob/skills/under.
    2. `test_adopted_glob_rejected` — inject `| agents/writer.md/** | ADOPTED-CLEAN | <64hex> | <64hex> |` (use real 64-hex strings), assert fail.
    3. `test_broad_glob_does_not_cover_adopted` — build a fixture where an adopted agent exists on disk but the manifest only has a (rejected) `agents/**` row; assert `verify()` reports the agent as not-manifested or the glob error (whichever fires first), NOT a silent PASS.
    Each test: `self._write_vendor(...)` to seed a baseline passing manifest, then append the bad row via the same append pattern used at lines 217/230/245, then call `check_boundary.verify()` and assert non-zero.
  - **Output**: 3 new tests in a `GlobSafetyTests` class.
  - **Verification**: `uv run python laf-adaptation/scripts/test_check_boundary.py -v 2>&1 | grep -E 'GlobSafety|test_agents_glob|test_adopted_glob|test_broad_glob'` → all 3 run and pass; total test count rises from 25 to 28.
  - **Completion gate**: 3 tests present, all pass.

---

## Phase 2: M1 — Run test_check_boundary.py in CI and pre-commit

- [x] **2.1 — Add test step to `.github/workflows/boundary.yml`**
  - **Context**: `.github/workflows/boundary.yml:49-54`. The workflow has a "Set up uv" step and a "Boundary contract (verify)" step with `working-directory: laf-adaptation`. The 25-test regression suite (`test_check_boundary.py`, confirmed passing) runs nowhere in CI. Adding the step does NOT violate ADR-006 (the "one script" rule concerns runtime; this is test-time for the boundary tool itself).
  - **Action**: After the existing "Boundary contract (verify)" step, add:
    ```yaml
          - name: Boundary checker regression tests
            working-directory: laf-adaptation
            run: uv run python scripts/test_check_boundary.py
    ```
  - **Output**: `boundary.yml` now runs the regression suite after the verify step.
  - **Verification**: Read `boundary.yml`; confirm the new step exists with `working-directory: laf-adaptation`. Optionally validate YAML: `python -c "import yaml; yaml.safe_load(open('.github/workflows/boundary.yml'))"`.
  - **Completion gate**: Step present, YAML valid.

- [x] **2.2 — Add test run to `laf-adaptation/.githooks/pre-commit`**
  - **Context**: `laf-adaptation/.githooks/pre-commit:26-29`. The hook runs `uv run python scripts/check_boundary.py` and sets `fail=1` on non-zero. The test suite should also run locally for fast fail (user chose CI + pre-commit this turn).
  - **Action**: After the existing verify block (after line 29, before the `if [ "$fail" ...` check at line 31), add:
    ```bash
    echo "pre-commit: boundary checker regression tests..."
    if ! uv run python scripts/test_check_boundary.py; then
      fail=1
    fi
    ```
  - **Output**: The pre-commit hook now runs the regression suite after the verify, incrementing `fail` on failure.
  - **Verification**: Read the hook back; confirm the new block is inside the `laf-adaptation` cwd context (the hook already `cd`s there at lines 19-24) and sets `fail=1`.
  - **Completion gate**: Block present, hooks into the existing `fail` accumulation.

---

## Phase 3: M2 (Option B) — Docs-align for text-normalized hashing + CRLF normalization test

- [x] **3.1 — Add `CRLFNormalizationTests` to `test_check_boundary.py`**
  - **Context**: Empirically confirmed this turn (`/tmp/crlf_test.py`): `Path.read_text` (text mode, `newline=None`) normalizes CRLF→LF, so `sha256_text` produces identical hashes for CRLF and LF content (`3ff7e685...` both), while `sha256_bytes` distinguishes them. M2 is **Option B** — keep the text pipeline, document the normalization as INTENDED (not accidental), so a future reader doesn't "fix" it.
  - **Action**: Add a `class CRLFNormalizationTests(BoundaryTestBase)` (or `unittest.TestCase` — does not need the VENDOR fixture, just a tmp file) with one test `test_crlf_and_lf_hash_identically_under_text_pipeline`:
    ```python
    class CRLFNormalizationTests(unittest.TestCase):
        """M2 (Option B): the boundary contract is TEXT-NORMALIZED (LF), not byte-accurate.
        Path.read_text (newline=None) normalizes CRLF->LF before hashing, so CRLF and LF
        versions of the same content produce identical laf_sha256. This is INTENDED —
        the contract hashes the LF-normalized form. This test PINS that behavior so a
        future change to byte-level hashing (Option A) is a deliberate, manifest-wide
        rehash, not an accident. See VENDOR.md 'Hash semantics'."""
        def test_crlf_and_lf_hash_identically_under_text_pipeline(self):
            tmp = Path(tempfile.mkdtemp(prefix="crlf_test_"))
            content = b"---\nname: x\n---\nbody line 1\nbody line 2\n"
            (tmp / "lf.md").write_bytes(content)
            (tmp / "crlf.md").write_bytes(content.replace(b"\n", b"\r\n"))
            self.assertEqual(
                check_boundary.sha256_text(check_boundary.read_text(tmp / "lf.md")),
                check_boundary.sha256_text(check_boundary.read_text(tmp / "crlf.md")),
                "text pipeline must LF-normalize (M2 Option B contract)")
    ```
  - **Output**: 1 new test pinning the normalization.
  - **Verification**: `uv run python laf-adaptation/scripts/test_check_boundary.py -v 2>&1 | grep -E 'CRLF|test_crlf'` → runs and passes; total now 29 (25 + 3 GlobSafety + 1 CRLF).
  - **Completion gate**: Test present, passes.

- [x] **3.2 — Soften "byte-identical"/"byte-faithful" claims in NATIVE docs**
  - **Context**: M2 Option B = make the contract's prose honest about its text-normalized reality. Affects NATIVE docs only: `laf-adaptation/CLAUDE.md`, `laf-adaptation/VENDOR.md` (especially the "Hash semantics" section), `laf-adaptation/NOTICE`. **Do NOT** edit any adopted agent body or adopted SKILL.md. **Do NOT** change `VENDOR.md`'s manifest table hashes or its `upstream_sha`/row data — only the descriptive prose around them.
  - **Action**: Find each occurrence of "byte-identical" / "byte-faithful" / "byte-accurate" / "byte-equality" in those three files. For each, reword to convey "text-normalized (LF) integrity" — e.g. "byte-identical vendoring" → "text-normalized (LF) vendoring"; "byte-faithful copies" → "text-normalized (LF) faithful copies". In `VENDOR.md`'s "Hash semantics" section, add one sentence: "Hashes are computed over the LF-normalized text form (`Path.read_text`), so CRLF and LF versions of the same content hash identically; the contract is text-normalized, not byte-accurate." Leave any occurrence inside a historical/CHANGELOG quote or inside an ADR citation untouched (note it in the task log).
  - **Output**: Three doc files updated; no hash/manifest data changed.
  - **Verification**: `grep -nE 'byte-identical|byte-faithful|byte-accurate|byte-equality' laf-adaptation/CLAUDE.md laf-adaptation/VENDOR.md laf-adaptation/NOTICE` → remaining matches are only in historical/CHANGELOG/citation context (note each in the task log); `uv run python laf-adaptation/scripts/check_boundary.py` still exits 0 (no manifest change).
  - **Completion gate**: Prose softened; verify still PASS; no manifest row touched.

---

## Phase 4: M3 — Document the writer.md Mode-V residual in code

- [x] **4.1 — Add writer.md / OQ-4 comment at the Mode-V `else` block**
  - **Context**: `laf-adaptation/scripts/check_boundary.py:598-601`. The `else:` block prints a NOTE when running without `--upstream` (Mode V skips Rules B/C). The writer.md Mode-V residual is documented at line 517, in the workflow header (`boundary.yml:27-33`), in `CLAUDE.md`, and in two regression tests — but the code path that actually skips it (the `else` block) does not name writer.md or OQ-4. Comment-only change; zero behavior change.
  - **Action**: At the `else:` block (line 598), insert a comment BEFORE the `print(...)`:
    ```python
        else:
            # Mode V (no --upstream): Rules B/C skipped. ADOPTED-PATCHED writer.md's
            # additive-body guarantee is a documented residual here — its absolute
            # proof is Mode-U Rule C (OQ-4: Mode U in CI is deferred). Backstopped by
            # branch protection + mandatory human review of any upstream_sha256 diff.
            # See check_boundary.py:517, .github/workflows/boundary.yml:27-33, VENDOR.md.
            print("NOTE: verify running without --upstream — Rules B and C (upstream-diff "
    ```
  - **Output**: The Mode-V skip block is self-documenting.
  - **Verification**: Read lines ~596-605 back; confirm the comment is present and the `print(...)` call is unchanged. `uv run python laf-adaptation/scripts/check_boundary.py` still exits 0 (comment-only).
  - **Completion gate**: Comment present; behavior unchanged.

---

## Phase 5: Verification (acceptance gates)

- [x] **5.1 — Run the full regression suite**
  - **Context**: All four fixes are applied. The suite must pass with the new tests added.
  - **Action**: `cd laf-adaptation && uv run python scripts/test_check_boundary.py`
  - **Output**: Suite output.
  - **Verification**: `Ran 29 tests` (25 original + 3 GlobSafety + 1 CRLF) and `OK`. If any test fails, fix the implementation (not the test, unless the test itself is wrong — note in task log).
  - **Completion gate**: `OK` with 29 tests.

- [x] **5.2 — Run the boundary verify on the live tree**
  - **Context**: The H1 parse-time gate and class-aware `manifest_covers` must not break the live manifest (which has no offending glob rows). The M2 doc edits must not touch manifest data.
  - **Action**: `uv run python laf-adaptation/scripts/check_boundary.py`
  - **Output**: Verify output.
  - **Verification**: Exits 0, prints `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.`
  - **Completion gate**: Exit 0, PASS.

- [x] **5.3 — Confirm no stray "byte-*" claims remain (except documented exceptions)**
  - **Context**: M2 Option B prose change verification.
  - **Action**: `grep -nE 'byte-identical|byte-faithful|byte-accurate|byte-equality' laf-adaptation/CLAUDE.md laf-adaptation/VENDOR.md laf-adaptation/NOTICE`
  - **Output**: List of remaining matches.
  - **Verification**: Every remaining match is in a historical/CHANGELOG/ADR-citation context noted in the task log — no live prose claim of byte-level integrity.
  - **Completion gate**: Clean grep or only-exception matches logged.

- [x] **5.4 — Confirm CI + pre-commit wiring**
  - **Context**: M1 verification.
  - **Action**: `grep -n 'test_check_boundary' .github/workflows/boundary.yml laf-adaptation/.githooks/pre-commit`
  - **Output**: Match list.
  - **Verification**: Both files reference `test_check_boundary.py`.
  - **Completion gate**: Both wired.

---

## Phase 6: Finalize (POST reflect gate + status)

- [x] **6.1 — Independent post-execution reflection gate (wrapper shell-out)**
  - **Context**: All implementation/verification items above are complete. The inline rf-qa/verify steps ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per the reflect-wrapper contract, the canonical POST gate is a flat `superclaude reflect run` Bash shell-out: the wrapper internally runs reflect's POST audit as a disjoint `claude --print` subprocess (executor-disjoint context that prevents self-rubber-stamping) and, with `--fix`, runs a bounded audit→apply→re-verify loop before writing `reflect_post:` back to this file's frontmatter itself.
  - **Action**: Ensure new task artifacts are staged so the working-tree diff is complete (`git add -A` — the wrapper's audit omits never-`git add`-ed files). Then emit the recursion-breaker-guarded wrapper shell-out as a single Bash command: first the skip guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`, then `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`. `{TASK_FILE}` is the absolute tasklist path. NO `--base` (wrapper resolves from frontmatter `start_commit`). `--depth deep` fixed; `--fix` runs the bounded auto-fix loop; `--promote` lets the task adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS. Consume the EXIT CODE: only `0` completes the gate; `10`/`11`/`2` FAIL → surface the wrapper report and HALT before Update-status-to-Done.
  - **Output**: The wrapper returns and writes `reflect_post: {verdict, run_id, report}` back to this file's frontmatter itself. If it surfaces unresolved deviations (exit 10/11/2), apply remediations or append them to `### Open Questions` (never delete existing items).
  - **Verification**: Wrapper exited `0`; frontmatter `reflect_post` holds a non-empty `{verdict, run_id, report}`; any flagged deviations remediated or logged.
  - **Completion gate**: Wrapper exited 0 (clean or auto-fixed-and-verified, and promoted). THEN 6.2 proceeds.

- [x] **6.2 — Update task status to Done**
  - **Context**: All phases complete and POST reflect gate passed.
  - **Action**: Update frontmatter: `status` → `🟢 Done`, set `completion_date`.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows `🟢 Done`.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log
(entries added during execution)
- [2026-07-06] All four implementation phases executed and were individually QA-gated by rf-qa (`qa-phase-1..4-report.md`). Phase 5 acceptance gates pass on the live tree: `Ran 30 tests ... OK`, boundary verify exit 0 / PASS, doc grep has only the honest `text-normalized, not byte-accurate` descriptor, and both CI + pre-commit reference `test_check_boundary.py`.
- [2026-07-06] **Phase 6.1 reflect gate — DEGRADED (exit 11), resolved by user direction.** The wrapper self-blocked once on `phase-incomplete` because item 6.1's `- [ ]` line preceded the in-body boundary token; after marking item 6.1 as triggered, the wrapper launched and wrote `reflect_post`. Machine-contract reconciliation: `reflect_post.verdict: degraded`, `reason: degraded-tier1`, `tier_reached: 1`, `merge_method: single-reviewer-fallback`, `t2_model_class_diversity: insufficient`, and `deviation_count_by_class: {authorized: 0, necessary: 0, drift: 0, regression: 0}`. The degraded verdict fails the strict POST gate (not a clean Tier-2 pass), but it reflects insufficient heterogeneous Tier-2 fan-out rather than code drift/regression. The one reviewer report was `CONDITIONAL PASS` and listed task-artifact prose staleness (e.g. stale 29-test literal and pre-QA line/code snippets), not code defects. Per user selection after surfacing the degraded contract, the task is marked Done with this degradation documented. Report: `reflect/post/ae1184b0e0ae/t2-swarm/reflect-review-01-qwen3.6-plus.final.md`; contract: `reflect/post/ae1184b0e0ae/return-contract.yaml`.

### Phase Findings
- **Phase 1 (H1) — PASS after 1 in-place QA fix.** rf-qa phase-gate (qa-phase-1-report.md) found a CRITICAL gap in item 1.1's gate: my prefix-only `path.startswith("skills/")` check admitted `skills/**` (no `<name>` segment), which `manifest_covers` would honor to cover EVERY skill dir including adopted ones — re-opening the exact H1 silent-coverage hole. Fixed in-place by tightening to `glob_prefix.startswith("skills/") and glob_prefix.count("/") == 1` (admits `skills/native1/**`, rejects `skills/**` and `skills/a/b/**`), plus a 4th regression test `test_bare_skills_glob_rejected`. Re-verified by executor: live verify exit 0; `Ran 29 tests ... OK`. The fix is a genuine hardening beyond the original spec — the item's "must be under skills/" gate was underspecified and the QA adversarial probe caught it.
- **Phase 2 (M1) — PASS, 0 findings.** rf-qa phase-gate (qa-phase-2-report.md) confirmed the CI step and pre-commit block are correctly placed/ordered, YAML valid, `bash -n` clean, exact command exits 0 from the laf-adaptation cwd, no adopted body touched. **Count reconciliation note for 5.1:** the current 29 tests = 25 original + 4 GlobSafety (Phase 1 QA added the 4th). Item 3.1's CRLFNormalizationTests will bring the total to **30**, not the 29 the task file's item 5.1 spec literal predicted (it predated the QA-added test). 5.1's true gate is `OK` with the full new count.
- **Phase 3 (M2 Option B) — PASS after 1 in-place QA fix.** rf-qa phase-gate (qa-phase-3-report.md) verified all three Option-B CRITICAL constraints: NO `--init` run, NO manifest row/hash/upstream_sha changed (VENDOR.md diff is purely a +5-line prose bullet; the 64-row table and `upstream_sha:` header byte-identical), NO adopted body touched. The one MINOR fix: CRLFNormalizationTests leaked a `/tmp/crlf_test_*` dir (it extends `unittest.TestCase` directly, no `tearDown`), fixed by adding `self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)`. Suite `Ran 30 tests ... OK`, live verify exit 0. Only remaining `byte-*` match is the honest descriptor "text-normalized, not byte-accurate" in the new VENDOR.md bullet.
- **Phase 4 (M3) — PASS after 1 in-place QA fix.** rf-qa phase-gate (qa-phase-4-report.md) confirmed comment-only change, `print(...)` NOTE string byte-identical, zero behavior change (verify exit 0, 30 tests OK), no adopted body touched. The one IMPORTANT fix: the comment's self-citation `check_boundary.py:517` was a stale line number (item 4.1's spec baked in a pre-execution snapshot; Phases 1-3 shifted lines). Fixed to `check_boundary.py:540-542 (Rule A′ writer.md exclusion)` — verified those lines hold the named content. The other cross-refs (`boundary.yml:27-33` OQ-4, VENDOR.md writer.md residual) were accurate as-is.

### Follow-Up Items
- After merge, consider reopening M2 Option A (byte-accurate hashing + manifest-wide `--init` rehash) if/when upstream ships mixed line endings. Tracked as the inverse of this task's Option B decision.
- The H1 fix is additive hardening; if a future feature legitimately needs an `agents/**` glob, the parse-time gate must be revisited (currently no such need exists).
- Optional: re-run `superclaude reflect run ... --depth deep --fix --promote` later in an environment that can assemble heterogeneous Tier-2 reviewer/model-class diversity. This run degraded to single-reviewer Tier 1 (`degraded-tier1`) but found zero drift/regression and the user authorized marking Done with the degradation documented.

### Open Questions
- Reflect POST gate did not achieve a clean Tier-2 PASS in this environment (`reflect_post.verdict: degraded`, reason `degraded-tier1`, one-reviewer fallback). User explicitly chose "Mark Done, document degradation" after the machine contract and single-reviewer findings were surfaced. No code defects remain open; the only reflect-reviewer findings were task-artifact prose staleness caused by QA-improved implementation details.
