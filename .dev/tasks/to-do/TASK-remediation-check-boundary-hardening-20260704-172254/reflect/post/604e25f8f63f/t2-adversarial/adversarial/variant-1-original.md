# Tier-2 Independent Audit Report
**Target:** `TASK-remediation-check-boundary-hardening-20260704-172254.md`  
**Base Ref:** `b51633d40a64be488c30edbd0f803dbdc8feadc1`  
**Audit Scope:** Regressions, spec drift, missing verification, unresolved decisions, adversarial exposure surface.

---

## 🔍 Executive Summary
The remediation successfully closes the primary trust-root gap (H1) and extends coverage (H2), with robust parser hardening (CH-6) and path safety (CH-4). The mid-execution empirical correction to OQ-1 (`prefix_unrewrite` inverse formula) prevents a catastrophic false-positive regression. However, **three high-confidence gaps** remain in cryptographic edge-case verification, manifest parsing fragility, and deferred CI hardening. The task correctly documents residual risks but lacks explicit test coverage for platform-dependent hashing and symlink traversal. Downstream adversarial scoring should treat `check_boundary.py` and `VENDOR.md` as high-scrutiny targets due to accepted two-field forgery tolerance and brittle path extraction logic.

---

## 📋 Concrete Findings

### 🔴 HIGH: Missing Verification / Cryptographic Edge Cases
| ID | Category | Evidence (Target Ref) | Finding |
|----|----------|----------------------|---------|
| **F-H1** | `[MISSING_VERIFICATION]` | `Resolutions → OQ-1`, `Phase 3 → 3.1 Action` | `prefix_unrewrite` is implemented as a naive string substitution (`laf-adaptation:` → `creative-writing-skills:`). No test verifies collision resistance or round-trip integrity when the upstream blob *already contains* the target string. If an upstream file legitimately contains `creative-writing-skills:`, the inverse transform will corrupt the hash, causing false negatives or silent bypasses. |
| **F-H2** | `[MISSING_VERIFICATION]` | `Phase 2 → 2.1 Action`, `Phase 4 → 4.1 Action` | `sha256_text()` and `sha256()` are used interchangeably for hash computation. No verification confirms whether `read_text()` vs `read_bytes()` is used, nor whether line-ending normalization (`\r\n` ↔ `\n`) is stripped before hashing. Cross-platform execution (Windows CI runners vs Linux dev) could produce divergent hashes, breaking the `GATE-GREEN INVARIANT`. |
| **F-H3** | `[REGRESSION RISK]` | `Phase 3 → 3.3 Action` | Rule F′ uses `r.path.split("/")[1]` to extract skill directories. This assumes a flat `skills/<dir>/...` structure. Nested skill paths (e.g., `skills/deep/nested/skill.md`) will extract `deep` instead of the intended skill root, causing false negatives in resource coverage checks. |

### 🟡 MEDIUM: Spec Drift / Unresolved Decisions
| ID | Category | Evidence (Target Ref) | Finding |
|----|----------|----------------------|---------|
| **F-M1** | `[DRIFT]` | `Phase 2 → 2.1 Action`, `VENDOR.md` notes | Parser enforces `len(cells) != 4` and explicitly rejects `|` in cells without escaping. While documented, this creates a hard failure mode for legitimate paths containing `|`. The spec (§4.6) permits this, but the implementation drifts from robust manifest parsing standards. No fallback or warning tier exists. |
| **F-M2** | `[UNRESOLVED]` | `Follow-Up Items → F1`, `Phase 5 → 5.2` | Mode U in CI is deferred. The target correctly labels this as a residual risk, but the `GATE-GREEN INVARIANT` now explicitly tolerates a coordinated two-field forgery (body + both hashes). This is documented, but the CI workflow lacks a `SECURITY: PARTIAL` badge or explicit risk-acceptance tag, which may mislead downstream reviewers. |
| **F-M3** | `[MISSING_VERIFICATION]` | `Phase 2 → 2.2 Action`, `_safe_repo_path` | `_safe_repo_path` uses `Path.resolve()` + `is_relative_to()`. Symlink traversal is not explicitly tested. If a manifest row points to a symlink inside `REPO` that resolves outside, `resolve()` follows it, but `is_relative_to()` checks the resolved path. This is likely safe, but no test (`test_symlink_escape_rejected`) exists to prove it. |

### 🟢 LOW: Process / Documentation
| ID | Category | Evidence (Target Ref) | Finding |
|----|----------|----------------------|---------|
| **F-L1** | `[INFO]` | `Phase 6 → 6.3`, `qa/lens-fix-summary.md` | Lens QA correctly caught `do_init` header-write ordering (F1) and over-claiming (F2). The fix cycle was bounded and verified. No further action required. |
| **F-L2** | `[INFO]` | `Task Log → Resolutions → OQ-2` | Python 3.13 confirmed. `Path.is_relative_to` is safe. Fallback branch correctly omitted per resolution. |

---

## ✅ Pass/Fail Signals

| Check | Signal | Evidence |
|-------|--------|----------|
| Gate-Green Invariant (Mode V) | ✅ PASS | `Phase 6 → 6.1`: Real-tree verify exits 0 on 64-row corpus. |
| `--report` Contract | ✅ PASS | `Phase 6 → 6.1`: Exits 0 with warnings on malformed rows. |
| Pure-Stdlib (ADR-006) | ✅ PASS | `Phase 6 → 6.2`: Only `argparse, hashlib, subprocess, sys, pathlib` used. |
| File-Scope Invariant | ✅ PASS | `Phase 6 → 6.1`: `git status` confirms only 5 target files modified. |
| OQ-1–OQ-4 Resolution | ✅ PASS | All resolved, logged, and empirically validated (OQ-1 corrected mid-flight). |
| Test Suite Coverage | ⚠️ PARTIAL | 25/25 pass, but missing: `prefix_unrewrite` collision, symlink escape, cross-platform line-ending hash consistency, nested-skill path extraction. |
| CI Security Posture | ⚠️ PARTIAL | Mode V closes single-field forgery; two-field forgery explicitly accepted. Mode U deferred. Documented but not mitigated. |

---

## 🎯 Suspect-Source Files for Adversarial Scoring
The following files should receive elevated scrutiny in downstream adversarial scoring due to accepted residual risks, brittle parsing logic, or cryptographic edge-case exposure:

| File | Reason for Elevated Scrutiny | Attack Surface |
|------|-----------------------------|----------------|
| `laf-adaptation/scripts/check_boundary.py` | Contains `prefix_unrewrite` (naive inverse), `split("/")[1]` path extraction, and `sha256_text()` without explicit byte/line-ending guarantees. | Hash collision via string substitution, nested-skill bypass, platform-dependent hash drift. |
| `laf-adaptation/VENDOR.md` | Manifest parser rejects `|` without escaping; two-field forgery tolerated in Mode V. Header `upstream_sha:` is mutable by `do_init`. | Malformed row injection, coordinated body+hash rewrite, header tampering during `--init`. |
| `.github/workflows/boundary.yml` | Runs Mode V only; lacks `permissions:` block (L2 deferred); no explicit `SECURITY: PARTIAL` risk tag. | CI environment escalation, silent acceptance of two-field forgery, missing least-privilege enforcement. |

---

## 🛠 Recommendations for Downstream Execution
1. **Add `prefix_unrewrite` collision test:** Construct a synthetic upstream blob containing `creative-writing-skills:` and verify `prefix_unrewrite` does not corrupt the hash or produce false matches.
2. **Enforce byte-level hashing:** Replace `read_text()` with `read_bytes()` in `sha256_text()` and explicitly strip `\r` before hashing to guarantee cross-platform determinism.
3. **Fix brittle skill-dir extraction:** Replace `r.path.split("/")[1]` with `Path(r.path).parts[1]` or a regex anchored to `^skills/([^/]+)/` to safely handle arbitrary nesting.
4. **Add symlink traversal test:** Verify `_safe_repo_path` rejects symlinks resolving outside `REPO`.
5. **Tag CI workflow risk:** Add a `# SECURITY: PARTIAL (Mode V only; two-field forgery accepted)` comment to `boundary.yml` to prevent downstream misinterpretation of the gate's guarantees.

**Audit Verdict:** `CONDITIONAL PASS`  
The remediation meets the stated DoD and correctly documents residual risks. However, the missing cryptographic edge-case verification and brittle path extraction logic warrant targeted regression testing before merging. Suspect-source files flagged above should be prioritized in adversarial scoring pipelines.