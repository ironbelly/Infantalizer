# Adversarial Merge — Wave 4 (sc-adversarial-protocol Mode A --compare)

**Cards merged:** card-1-analyzer.md, card-2-qa.md, card-3-refactorer.md
**Merge method:** adversarial (3-way debate + scoring); judge frame = executor-disjoint (orchestrator, no executor exists in PRE mode)
**Pre-merge calibration:** per-card blind calibration applied (calibrator class = sonnet for card-1/3, haiku for card-2 — disjoint rotation per §11.3)

## Per-card calibrated scores (Wave 3C blind re-grade)

| Card | Self-conf | Calibrated | Delta | Calibrator class |
|------|-----------|------------|-------|------------------|
| card-1 (analyzer/opus) | 0.86 | 0.84 | -0.02 | sonnet |
| card-2 (qa/sonnet) | 0.86 | 0.85 | -0.01 | haiku |
| card-3 (refactorer/haiku) | 0.82 | 0.83 | +0.01 | sonnet |

Calibration deltas are small (≤0.02) — the reviewers were not anchored to over-confident self-reports. calibrator_diversity: full (calibrators disjoint from each card's reviewer class).

## Regression-candidate debate (the load-bearing stage)

Three REGRESSION candidates were raised (A1, A2, Q1). Per §5.3 rule 3, regression candidacy MUST be debated by ≥2 reviewers. The debate below adjudicates each against the verbatim spec (re-read in Wave 5 evidence-validator style: boundary-contract.md:1-110, DESIGN.md:279-298).

### REGRESSION candidate A1 — Phase-3 hard gate satisfiable with non-Tolkien stand-in
- **Raised by:** card-1 (analyzer) — REGRESSION, HIGH
- **Concurrence:** card-2 (qa) did NOT raise A1 explicitly but its Q1 references the same Phase-3 gate.
- **Dissent:** card-3 (refactorer) did not flag A1; it classified the proof-chapter provisioning as out-of-scope process.
- **Spec re-read:** DESIGN.md:282 ("full 11-step run on a real Tolkien chapter across 3 tiers") + DESIGN.md:296 ("one Tolkien chapter at Tier 1; then same chapter at Tiers 1/3/5") + tasklist Step 5.1 PATH B (public-domain stand-in) + tasklist Open Questions line 590 ("real Tolkien is NOT public domain... Step 5.1 supports an execution-time external input (PREFERRED) OR a public-domain stand-in").
- **Debate:**
  - *For REGRESSION:* The spec's §7 Phase 3 gate and §6 residual-risk mitigation both say "Tolkien chapter." PATH B permits a non-Tolkien stand-in. If an executor picks PATH B, the letter of the spec gate is not met.
  - *Against REGRESSION:* The spec never requires COMMITTING Tolkien prose — it requires running the proof on one Tolkien chapter. PATH A (PREFERRED) IS the Tolkien-chapter path (operator supplies prose under their access rights, not committed). PATH B is a committable MECHANICS-PROOF fallback explicitly for the case where the operator cannot supply Tolkien prose. The tasklist documents this as an Open Question (line 590), transparently. The pipeline mechanics (the actual integration-test target) are proven either way; only the domain-specific transformation richness differs. More importantly, committing copyrighted Tolkien prose would itself violate a higher-order constraint (legal/copyright) not in the spec but binding on the operator.
  - *Adjudication:* This is a **NECESSARY DEVIATION, not a REGRESSION.** The tasklist resolves a genuine spec-vs-legal-constraint tension (Tolkien still under copyright in most jurisdictions per Open Question line 590) by offering two paths, PREFERRED being the spec-faithful one. The fallback is documented inline with rationale and surfaced as an Open Question — the §10.2 Necessary-deviation signature. The REGRESSION classification is **DOWNGRADED to NECESSARY DEVIATION** by the merge judge. However, the tasklist SHOULD tighten Step 5.1 to require PATH A as the gate-faithful default and record PATH B explicitly as a mechanics-only proof that does NOT satisfy the §6 "real Tolkien" mitigation (only the §7 mechanical gate). This is a **recommendation**, not a blocking defect.

### REGRESSION candidate A2 — `--init` instructed to "apply the writer additive graft"
- **Raised by:** card-1 (analyzer) — REGRESSION, HIGH
- **Concurrence:** card-2 (qa) did not raise A2; card-3 did not raise A2.
- **Spec re-read:** boundary-contract.md:17-19 ("It is a validation tool... it reads files and computes hashes; it never transforms the framework") vs boundary-contract.md:85-86 ("laf_sha256 — hash of the file as it lives in laf-adaptation/ (after prefix rewrite, and for writer.md, after the additive graft)") vs tasklist Step 2.2 line 182 ("--init mode ... applies the writer additive graft before hashing its laf_sha256").
- **Debate:**
  - *For REGRESSION:* The script "never transforms the framework" (boundary-contract.md:18). If --init APPLIES the graft, it transforms writer.md, violating the validation-tool contract.
  - *Against REGRESSION:* boundary-contract.md:85-86 explicitly states the laf_sha256 for writer.md is computed "after the additive graft." This means the graft must be present at hash time. There are two readings: (i) the graft is applied at vendoring time (Step 2.3 writer item — "create the vendored file writer.md whose skills: list is the upstream list ... PLUS exactly one appended line") and --init merely hashes the already-grafted file; OR (ii) --init applies the graft. Reading (i) is consistent with both spec lines: vendoring does the transform (Step 2.3), --init hashes the result. Reading (ii) — which the tasklist Step 2.2 line 182 literally says — would double-apply if Step 2.3 also grafts. The tasklist is INTERNALLY INCONSISTENT on which step applies the graft: Step 2.3 says vendoring applies it, Step 2.2 says --init applies it.
  - *Adjudication:* The reviewer's REGRESSION is **UPHELD as a real defect, but DOWNGRADED from REGRESSION to DRIFT.** Reasoning: the spec is unambiguous that the script "never transforms the framework" (boundary-contract.md:18) — so reading (ii) in Step 2.2 line 182 is spec-wrong. BUT the practical impact is bounded: Step 2.3 (vendoring) correctly applies the graft, so if the executor follows Step 2.3 first, --init hashing an already-grafted file produces the correct laf_sha256 (the Step 2.2 "applies ... before hashing" wording would only cause a double-graft bug if read literally and the script actually re-applied). The defect is a **wording/ambiguity drift in Step 2.2** that could mislead an implementer into having --init perform the graft (violating the validation-tool contract) OR double-graft. This is a **blocking DRIFT finding** requiring remediation: Step 2.2 should say "--init hashes the writer.md that Step 2.3 already grafted; it does NOT apply the graft itself" to match boundary-contract.md:17-19. Not a REGRESSION because it does not silently pass a spec gate at runtime — it is a build-time wording defect that, if mis-implemented, would surface as a Rule A/C failure (caught by the very gate it might break).

### REGRESSION candidate Q1 — PC.6 `--fix --promote` mutates after final QA with no re-verification
- **Raised by:** card-2 (qa) — REGRESSION
- **Concurrence:** card-1 (analyzer) did not raise Q1; card-3 (refactorer) did not raise Q1.
- **Spec re-read:** DESIGN.md:296 (5 hard-gate conditions) + DESIGN.md:308 ("Phase 3 hard gate is the definition of '0.1 done'") + tasklist Step PC.6 line 524 (`superclaude reflect run --depth deep --fix --promote`) + tasklist Step PC.6 line 528 ("only after ... POST reflect gate ... has PASSED ... AND final assembled-output QA gate ... has PASSED, AND Phase-3 hard gate is GREEN").
- **Debate:**
  - *For REGRESSION:* `--fix` auto-mutates artifacts; `--promote` mutates the work-unit location. If reflect auto-fixes a file (e.g., re-ports a YAML) after PC.1-PC.5 passed, the post-fix tree is NOT re-verified by PC.1-PC.5 nor by the Phase-3 hard-gate condition files. The tasklist treats exit 0 as proceed-to-Done even when "deviations auto-fixed and promoted" occurred.
  - *Against REGRESSION:* (a) The POST reflect gate runs `superclaude reflect run` which is itself a deep audit with its own evidence-validator — it does not blindly mutate; `--fix` only auto-fixes AUTO-FIXABLE registers (Drift/Necessary) per the reflect protocol, and any HUMAN-REQUIRED register (Regression, needs_human_decision) blocks. So `--fix` cannot silently pass a Regression. (b) `--promote` only fires when the strict 9-condition gate passes (including citations_dropped==0, no drift, no regression, needs_human_decision==false) — so promotion implies the gate already re-verified. (c) The tasklist's Step PC.6 line 524 contract says "exit 10/11/2 are FAILs that HALT" — only exit 0 proceeds, and exit 0 means the reflect audit itself confirmed no regressions. So the mutation (if any) is gated by a fresh audit.
  - *Adjudication:* The reviewer's concern is **PARTIALLY UPHELD but DOWNGRADED from REGRESSION to a NECESSARY-DEVIATION-WITH-RISK.** Reasoning: the `--fix`/`--promote` flags are NOT unguarded — they run inside a deep reflect audit whose exit code is the gate. However, the reviewer raises a legitimate ordering concern: if `--fix` mutates a file mid-audit, the reflect's OWN evidence-validator re-reads cited files at Wave 7 step 7.2 (per the reflect protocol's `citation_revalidation_at_promotion`), so reflect internally re-verifies. BUT the tasklist's Phase-3 hard-gate condition files (gate-cond1..5) and the PC.1-PC.5 QA reports were computed on the PRE-fix tree and are NOT recomputed. This is a real gap IF --fix mutates an artifact those gates depend on. The cleanest fix (and the merge judge's recommendation): Step PC.6 should use `--no-promote` (audit-only) for the 0.1 release, OR if `--fix`/`--promote` is retained, add a PC.7 step that re-runs the 5 Phase-3 hard-gate conditions + check_boundary.py on the post-reflect tree before marking Done. This is a **blocking finding requiring remediation** but classified as NECESSARY DEVIATION (the reflect gate itself is a documented process addition; the auto-mutation posture is a tunable parameter within it), not REGRESSION (it does not silently pass a spec gate — reflect exit 0 is a real audit verdict).

## Other findings (no regression candidacy; merge by severity)

- **Q2 (DRIFT, working-directory cwd)**: card-2 raised; the verifier commands `uv run python laf-adaptation/scripts/check_boundary.py` from repo root while boundary-contract.md:109-150 uses relative paths/globs assuming cwd=laf-adaptation/. **UPHELD as DRIFT.** The tasklist partially acknowledges this (line 592 hook/CI note) but does not require either `cd laf-adaptation` OR script-internal path rooting from `__file__` in Step 2.2. Blocking — must be resolved in Step 2.2 (script roots paths from its own location) or all verifier commands must `cd` first.
- **R2 (DRIFT, "Assume at least 5/10 errors" framing)**: card-3 raised; LOW severity. **UPHELD as LOW DRIFT.** Not blocking; recommendation to soften the fixed-count adversarial framing.
- **R1, R3, R4, R5 (NECESSARY)**: card-3 raised; all document process additions with rationale. **UPHELD as NECESSARY DEVIATION.** Non-blocking.
- **F2, F3, F4, F5, F6 (T1 findings)**: spec-internal tensions resolved correctly by tasklist. **Non-defects.** Confirmed.

## Merged verdict

- **status: partial** — 2 blocking DRIFT findings (A2 wording, Q2 cwd) + 1 blocking NECESSARY-DEVIATION-WITH-RISK finding (Q1 auto-mutation posture) require remediation before the tasklist is execution-ready. The tasklist is NOT marked `failed` because: (a) coverage is complete (1.00 union); (b) no finding is a true REGRESSION that would silently pass a spec gate at runtime — all three blocking findings are build-time wording/posture defects that, if mis-implemented, would surface as visible gate failures (caught by check_boundary.py or the reflect audit itself), not silent spec violations.
- **coverage_pct_union: 0.97** (down from T1's 1.00 — the merge identified that the "POST reflect gate re-verification" requirement and the "cwd-rooted verifier" requirement are spec-implied requirements the tasklist under-specifies, matching card-2's unmapped_requirements list)
- **regression_present: false** (no upheld REGRESSION; A1 downgraded to NECESSARY, A2 downgraded to DRIFT, Q1 downgraded to NECESSARY-WITH-RISK)
- **unauthorized_deviation_present: true** (R2 — the fixed-count adversarial framing — is LOW DRIFT, but it IS unauthorized; plus the blocking A2/Q2 wording drifts)
- **convergence_score: 0.71** — reviewers converged on coverage completeness (all 3 agree ≥0.96) and on the absence of true regressions, but diverged on the regression candidates (card-1 found 2, card-2 found 1 overlapping, card-3 found 0). Cross-class disagreement on A1/A2/Q1 is the non-convergence. Score ≥0.60 (PARTIAL per §8 convergence routing), <0.75.

## Blocking remediation list (for Wave 6 / report)

1. **A2 (DRIFT, blocking):** Step 2.2 line 182 — clarify that `--init` hashes the writer.md that Step 2.3 already grafted; it does NOT apply the graft itself. Aligns with boundary-contract.md:17-19 ("never transforms the framework") and :85-86 (laf_sha256 "after the additive graft" = the file Step 2.3 produced).
2. **Q1 (NECESSARY-WITH-RISK, blocking):** Step PC.6 — either change `--fix --promote` to `--no-promote` (audit-only, recommended for 0.1), OR add a Step PC.7 that re-runs the 5 Phase-3 hard-gate condition files + check_boundary.py on the post-reflect tree before the status flips to Done.
3. **Q2 (DRIFT, blocking):** Step 2.2 + all verifier commands — require either (a) the script roots all paths from `Path(__file__).parents[1]` so cwd is irrelevant, OR (b) every verifier command is `cd laf-adaptation && uv run python scripts/check_boundary.py`. Currently ambiguous; boundary-contract.md:109-150 assumes cwd=laf-adaptation/.
4. **A1 (recommendation, non-blocking):** Step 5.1 — tighten to make PATH A (Tolkien) the gate-faithful default and explicitly mark PATH B as a mechanics-only proof that does NOT satisfy the §6 "real Tolkien" residual-risk mitigation.

## Non-blocking recommendations

5. **R2:** Soften the fixed-count "Assume at least 5/10 errors" adversarial framing to "Find any errors present" — avoids biasing reviewers toward false positives.
6. **F2 (T1, surface to spec author):** DESIGN.md §5 #1 wording lists "analyst" in the active_tier recipient set, contradicting §3.2 + agent-schemas §2.1 (analyst is tier-invariant). The tasklist resolves this correctly; the spec wording is imprecise. Out-of-scope for the tasklist; flag for spec author.

## merge_method: adversarial
## adversarial_unavailable: false
## fallback_path: null
