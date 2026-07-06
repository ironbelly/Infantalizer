# T2 Reviewer Card #2 — QA lens (sonnet / gpt-5.5)

**Persisted by orchestrator** — reflect-reviewer agent is read-only; card content returned by reviewer agent a15efdc36f5e9d96d.

## Verdict
- status: partial
- coverage_pct_union: 0.96
- unmapped_requirements:
  - "POST reflect gate must not mutate/promote release artifacts after final assembled-output QA without a subsequent verification gate"
  - "Boundary verifier commands must execute from the directory assumed by check_boundary.py/boundary-contract.md, or the script must be explicitly required to root paths from __file__"
- regression_present: true
- unauthorized_deviation_present: true
- calibrated_confidence: 0.86

## Findings

### Finding Q1 — PC.6 auto-fix/auto-promote can mutate after final QA with no re-verification
- spec_anchor: DESIGN.md:296
- tasklist_anchor: TASK...md:523-528 (Step PC.6)
- classification: REGRESSION
- evidence:
  - Spec hard-gate definition: DESIGN.md:296 — "Run the full 11-step workflow on one Tolkien chapter at Tier 1; then same chapter at Tiers 1/3/5 through tier-coordinator. | v2.0 tags present · safety PASS · per-tier canon written · all four quartet agents ran · check_boundary.py green"
  - Spec done definition: DESIGN.md:307-308 — "Implementation should proceed phase-by-phase (0→4) and treat the companion specs as the buildable source of truth. The Phase 3 hard gate is the definition of '0.1 done.'"
  - Tasklist final QA gate passes before PC.6: TASK...md:518-521 — "IF both PASS, the final assembled-output gate PASSES — the tree is release-ready."
  - Tasklist PC.6 command: TASK...md:524 — `superclaude reflect run "...TASK...md" --depth deep --fix --promote`
  - Tasklist PC.6 proceeds after auto-fix/promote: TASK...md:524 — "IF exit code 0 (reflect PASSED — coverage adequate, no deviations, or deviations auto-fixed and promoted), proceed to mark this item complete"
  - Status update follows directly after PC.6: TASK...md:528 — "only after the POST reflect gate (Step PC.6) has PASSED … AND the final assembled-output QA gate … has PASSED, AND the Phase-3 hard gate is GREEN."
- rationale: This is a load-bearing gate-discipline regression. The tasklist places an auto-mutating --fix --promote reflect run after final assembled-output QA and after the Phase-3 hard gate has already been evaluated. If reflect auto-fixes artifacts and promotes them, the tasklist does not require rerunning PC.1-PC.5, Step 6.3, or the Phase-3 hard-gate condition files on the mutated tree before marking Done. In PRE-mode terms, this is a tasklist gate that can silently pass a spec violation: exit 0 is treated as acceptable even when "deviations auto-fixed and promoted" occurred, but those mutations are not subsequently re-verified against the design's five hard-gate conditions.
- QA posture recommendation: PC.6 should use a non-mutating posture, e.g. --no-promote / no --fix, or require a mandatory post-reflect re-run of boundary, final QA, and any affected hard-gate conditions if auto-fix is retained.

### Finding Q2 — Boundary verifier commands are inconsistent with the nested laf-adaptation/ working-directory contract
- spec_anchor: boundary-contract.md:171-181
- tasklist_anchor: Steps 2.13, 2.14, 3.19, 4.8, 5.10, 6.3, PC items / TASK...md:241-245,330-331,388-389,447-448,488-489,493-495
- classification: DRIFT
- evidence:
  - Boundary-contract enforcement commands are relative to the framework tree: boundary-contract.md:175-181 — "Pre-commit hook … python3 scripts/check_boundary.py"; "CI … python3 scripts/check_boundary.py"; "Per project rules, LAF uses UV: the pre-commit and CI invocations are uv run python scripts/check_boundary.py."
  - Verify algorithm uses relative paths/globs: boundary-contract.md:109-150 — "load VENDOR.md manifest", sha256(row.path), read(row.path), glob("agents/*.md") + glob("skills/**/SKILL.md")
  - Tasklist places the script under nested tree: TASK...md:181-182 — author at laf-adaptation/scripts/check_boundary.py
  - Tasklist repeatedly invokes from repo root with nested script path: TASK...md:241-245 — `uv run python laf-adaptation/scripts/check_boundary.py --init --upstream <checkout-dir>` and `uv run python laf-adaptation/scripts/check_boundary.py`
  - Tasklist acknowledges cwd sensitivity for hook/CI only: TASK...md:592 — "repo root is /config/workspace/Infantalizer, so the wrappers must account for the nested path"
- rationale: The companion spec's algorithm and enforcement command assume the cwd is laf-adaptation/: VENDOR.md, agents/*.md, and skills/**/SKILL.md are relative to that tree. The tasklist's repeated verifier commands use `uv run python laf-adaptation/scripts/check_boundary.py` from the repo root without requiring either cd laf-adaptation or a script implementation that roots all paths from Path(__file__).parents[1]. This is a verifiability/gate-discipline drift: the gate may fail for cwd reasons rather than validating the boundary contract, or an implementer may "fix" the script ad hoc. Classified as DRIFT rather than REGRESSION because it is more likely to block execution than silently pass a spec violation, but it directly undermines verifier correctness.

## Coverage gaps
The major spec-defined Phase-3 hard-gate conditions are explicitly covered:
- v2.0 tags: Step 5.6 (TASK...md:435-436)
- safety PASS: Step 5.7 (TASK...md:438-439)
- per-tier canon: Step 5.8 (TASK...md:441-442)
- quartet ran: Step 5.9 (TASK...md:444-445)
- boundary green: Step 5.10 (TASK...md:447-448)
- all-five aggregation/HALT: Step 5.11 (TASK...md:450-451)

The Phase-0 gate is verified rather than assumed: --init (TASK...md:241-242); default verify + zero-edit assertion (TASK...md:244-245).

The six DESIGN.md §5 constraint-enforcement claims are covered by a mix of runnable checks, artifact inspections, and QA agents. The strongest runnable enforcement is for boundary/quartet/writer via check_boundary.py; several others are verified through generated artifacts and lens reviews rather than a single deterministic script (reasonable for a prompt/YAML framework but increases review cost).

## Notes
- Proportionality debate: The QA ceremony is heavy for a 0.1 release (PG0-PG3 + PC.1-PC.5 ≈ 30+ QA agent spawns). However, the tasklist explicitly declares "QA intensity = full (PER_PHASE)" (TASK...md:132), and the release has unusual high-risk properties: vendored boundary contract, source-fidelity protocol, safety gate, live Phase-3 proof. The volume itself is NOT classified as drift. Cost is high but intentionally selected and bounded by max-three fix cycles.
- Retry discipline is mostly consistent: PG0 (:270), PG1 (:361), PG2 (:414), PG3 (:476), PC.5 (:521) — all max-three-cycles-then-HALT.
