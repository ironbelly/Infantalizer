# Tier-2 Independent Audit Report
**Target:** `TASK-remediation-check-boundary-hardening-20260704-172254.md`
**Base Ref:** `b51633d40a64be488c30edbd0f803dbdc8feadc1`
**Audit Scope:** Regressions, spec drift, missing verification, unresolved decisions, adversarial risk surface.

---

## 🔍 Concrete Findings

### 1. Regression / Mid-Execution Pivot (H1 Trust-Root Formula)
- **Evidence:** `TASK-remediation-check-boundary-hardening-20260704-172254.md` → `Phase 3 Findings` / `OQ-1 Resolution`
- **Finding:** The initial CH-1 implementation formula (`sha256(prefix_rewrite(disk)) == upstream_sha256`) was empirically proven **incorrect** and would have caused a false-positive failure across all 55 `ADOPTED-CLEAN` rows. The pivot to `prefix_unrewrite` (`sha256(prefix_unrewrite(disk)) == r.upstream_sha256`) corrected the regression.
- **Risk:** The inverse transform (`laf-adaptation:` → `creative-writing-skills:`) is not formally specified in the target. If `prefix_unrewrite` encounters malformed or dual-prefix content, it may raise an unhandled exception during `verify()`, crashing the CI gate.
- **Status:** `⚠️ CONDITIONAL PASS` (Fix applied, but robustness of `prefix_unrewrite` on edge-case inputs is unverified).

### 2. Spec Drift / Design Constraint (`--report` Error Masking)
- **Evidence:** `TASK-remediation-check-boundary-hardening-20260704-172254.md` → `2.1 — CH-6` / `Action`
- **Finding:** `do_report` is explicitly designed to print parser errors as warnings but **still exit 0** to preserve the `--report` contract. This drifts from the "fail loud" security posture mandated for CH-6. While intentional, it creates a silent-failure vector if `--report` is invoked in automated pipelines expecting strict validation.
- **Risk:** CI or local tooling relying on `--report` for manifest hygiene will not halt on malformed/duplicate rows.
- **Status:** `🟡 ACCEPTED DRIFT` (Documented, but requires explicit pipeline guardrails).

### 3. Missing Verification (`resources/**` Glob Specificity)
- **Evidence:** `TASK-remediation-check-boundary-hardening-20260704-172254.md` → `3.3 — CH-2` / `Action`
- **Finding:** The target states `enumerate disk_skill_files(skdir)` and asserts manifest coverage, but does not specify the file extension filter or glob pattern. If `disk_skill_files` defaults to `*.md` only, non-markdown resources (e.g., `.yaml`, `.json`, `.txt`) in adopted skill `resources/` directories will bypass Rule F′ enforcement.
- **Risk:** Partial coverage gap for adopted skill resource trees.
- **Status:** `🔴 MISSING VERIFICATION` (Glob definition and extension coverage must be explicitly validated against the spec's `resources/**` requirement).

### 4. Unresolved Decision / Deferred Security Guarantee (Mode U)
- **Evidence:** `TASK-remediation-check-boundary-hardening-20260704-172254.md` → `OQ-4 Resolution` / `5.2 — CH-8 Option B`
- **Finding:** Mode U (upstream checkout + HEAD pin) is deferred per OQ-4. Consequently, `ADOPTED-PATCHED` (`agents/writer.md`) and any literal-bearing bodies retain only a conditional guarantee in Mode V. The target explicitly documents this as a residual risk, but the absolute upstream-anchored guarantee remains unimplemented.
- **Risk:** A malicious actor with PR access can still forge both `laf_sha256` and `upstream_sha256` for `writer.md` without triggering a Mode V failure.
- **Status:** `🟡 KNOWN RESIDUAL RISK` (Deferred to F1; requires explicit maintainer sign-off on risk acceptance).

### 5. Controlled Bypass Test Pattern
- **Evidence:** `TASK-remediation-check-boundary-hardening-20260704-172254.md` → `Phase-6 lens-based QA gate` / `F2`
- **Finding:** The test `test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v` is explicitly designed to assert that a two-field forgery **passes** Mode V. While correctly documented as a residual risk, embedding a passing test for a security bypass normalizes the gap and may confuse downstream auditors or automated scoring.
- **Risk:** Test suite signals "PASS" for a known bypass condition.
- **Status:** `🟡 DOCUMENTED BYPASS` (Acceptable if strictly isolated and named, but requires clear annotation in test output).

---

## 📊 Pass/Fail Signals

| Signal | Status | Evidence |
|--------|--------|----------|
| **Gate Green Invariant** | ✅ PASS | `check_boundary.py` exits 0 on clean corpus; `--report` exits 0 (per target logs) |
| **Pure-Stdlib Constraint** | ✅ PASS | Imports limited to `argparse, hashlib, subprocess, sys, pathlib` (ADR-006) |
| **File-Scope Invariant** | ✅ PASS | Only `check_boundary.py`, `test_check_boundary.py`, `boundary.yml`, `VENDOR.md`, `CLAUDE.md` modified |
| **Parser Hardening (CH-6)** | ✅ PASS | `(rows, errors)` signature propagated; 10/10 parser tests pass |
| **Path Safety (CH-4)** | ✅ PASS | `_safe_repo_path` + `ManifestError` rejects traversal/absolute paths |
| **Mode U HEAD Pin (CH-5)** | ✅ PASS | `--upstream-sha` + `_checkout_head` implemented; wrong-SHA fails |
| **Resources Coverage (CH-2)** | ⚠️ PARTIAL | Glob specificity unverified; non-`.md` files may bypass |
| **Trust-Root Re-Anchor (CH-1)** | ⚠️ CONDITIONAL | `prefix_unrewrite` inverse transform works empirically, but edge-case robustness untested |
| **Deferred Absolute Guarantee** | 🟡 DEFERRED | Mode U/Option B deferred; `writer.md` remains conditionally secured |

---

## 🎯 High-Confidence Suspect-Source Files (Adversarial Scoring)

The following files should receive **elevated scrutiny** in downstream adversarial scoring due to logic pivots, controlled bypasses, or deferred guarantees:

| File | Reason for Elevated Scrutiny |
|------|------------------------------|
| `laf-adaptation/scripts/check_boundary.py` | Core boundary logic; contains `prefix_unrewrite` inverse transform, `(rows, errors)` parser refactor, and `_safe_repo_path`. Mid-execution formula correction increases mutation risk. |
| `laf-adaptation/scripts/test_check_boundary.py` | Contains `test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v` (explicit bypass validation) and fixture monkeypatching of `REPO`/`VENDOR_MD`. High surface for test-environment drift. |
| `laf-adaptation/VENDOR.md` | Header `upstream_sha:` semantics changed; `|`-in-cell constraint added. Parser relies on exact header format; malformed header could trigger silent fallbacks. |
| `.github/workflows/boundary.yml` | CI gate configuration; `--report` exit-0 behavior may mask parser errors if workflow misuses flags. Deferred Mode U steps leave CI running in weaker Mode V. |

---

## 📝 Recommendations for Downstream Adversarial Scorer

1. **Stress-Test `prefix_unrewrite`:** Inject malformed, dual-prefix, or empty-prefix strings into adopted bodies. Verify `verify()` fails gracefully (exit 1 + clear error) rather than crashing.
2. **Validate `resources/**` Glob:** Confirm `disk_skill_files(skdir)` matches `**/*` (all extensions), not just `*.md`. If limited, flag as a coverage regression.
3. **Audit `--report` Exit Code:** Ensure CI pipelines do not rely on `--report` for security gating. If they do, the exit-0-on-error design is a critical misconfiguration.
4. **Monitor `writer.md` Hash Pairing:** Since Mode V accepts two-field forgery for `ADOPTED-PATCHED`, adversarial scoring should simulate PRs that mutate `writer.md` + rewrite both hashes. Verify that branch protection/human review (the stated backstop) is the only control.
5. **Verify Test Isolation:** Ensure `BoundaryTestBase`'s `setUp`/`tearDown` fully isolates `REPO`/`VENDOR_MD` monkeypatches. Leaky state could cause false positives/negatives in parallel test runs.

**Audit Verdict:** `🟡 CONDITIONAL PASS`  
The remediation successfully closes the single-field `laf_sha256` forgery vector and hardens the parser/path-safety layer. However, the deferred Mode U guarantee, unverified `resources/**` glob scope, and `prefix_unrewrite` edge-case robustness require explicit validation before promoting to production. All findings are documented and traceable to the target's execution log.