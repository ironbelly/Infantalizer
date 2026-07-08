# T2 Reviewer Card #1 — ANALYZER lens (opus / claude-opus-4-8[1m])

**Persisted by orchestrator** — reflect-reviewer agent is read-only (no Write tool); card content returned by reviewer agent aa275ed2358e439a2.

## Verdict
- status: partial
- coverage_pct_union: 0.96
- unmapped_requirements: []
- regression_present: true
- unauthorized_deviation_present: true
- calibrated_confidence: 0.86

## Findings

### Finding A1 — Phase-3 hard gate can be satisfied with a non-Tolkien stand-in
- spec_anchor: DESIGN.md:296
- tasklist_anchor: TASK...md:421 (Step 5.1)
- classification: REGRESSION
- evidence:
  - Spec DESIGN.md:296 — "Run the full 11-step workflow on one Tolkien chapter at Tier 1; then same chapter at Tiers 1/3/5 through tier-coordinator."
  - Spec DESIGN.md:282 — "Phase 3 hard gate: full 11-step run on a real Tolkien chapter across 3 tiers before 0.1 ships"
  - Tasklist line 421 — "OR (PATH B — committable fallback) place a short PUBLIC-DOMAIN narrative excerpt ... purely to prove the pipeline mechanics"
  - Tasklist line 424 — "If the proof work is not Tolkien, copy the template and fill in the [Bracketed] placeholders for the chosen work instead."
- rationale: DESIGN.md makes the Tolkien chapter run a hard acceptance gate and a residual-risk mitigation against "Hybrid → everything half-done." The tasklist permits a public-domain stand-in to satisfy the same Phase-3 proof path. The copyright concern is real, but the spec does not require committing Tolkien prose; it requires running the proof on one Tolkien chapter. The tasklist already supports operator-supplied external input, so the fallback is not forced. If executed literally with PATH B, the task can mark the Phase-3 hard gate complete without satisfying the spec's "real Tolkien chapter" condition.
- severity: HIGH

### Finding A2 — `check_boundary.py --init` is instructed to apply the writer graft, contradicting the validation-only boundary contract
- spec_anchor: boundary-contract.md:17
- tasklist_anchor: TASK...md:182 (Step 2.2)
- classification: REGRESSION
- evidence:
  - Spec boundary-contract.md:17-19 — "This is the only script LAF 0.1 ships ... It is a validation tool, not a runtime — it reads files and computes hashes; it never transforms the framework."
  - Spec boundary-contract.md:96-103 — "check_boundary.py --init # first vendor: compute laf_sha256 for adopted files, write manifest rows" and "--init ... requires a local checkout ... to record upstream_sha256 and prove the prefix rewrite is the only transformation."
  - Tasklist line 182 — "the --init mode ... computes both upstream_sha256 and laf_sha256 for adopted files, writes/updates the manifest rows, applies the writer additive graft before hashing its laf_sha256"
- rationale: The spec's boundary contract is load-bearing: check_boundary.py is a read-only validation tool that computes hashes and proves allowed transformations, not the component that performs those transformations. The tasklist's instruction for --init to "apply" the writer additive graft before hashing is structurally wrong. The writer graft should already be present from the vendoring step and then verified/hashed; if the script mutates the tree or computes a synthetic post-graft hash, it weakens the proof that the actual file on disk matches the allowed ADOPTED-PATCHED state.
- severity: HIGH

## Coverage gaps
None found. The tasklist broadly maps the DESIGN.md §7 phase gates, DESIGN.md §5 constraints, G1/G2/G3 invariants, and companion-spec artifact requirements. The defects above are not unmapped requirements; they are mapped requirements whose tasklist realization would violate a spec gate or load-bearing invariant.

## Notes
- The tasklist correctly resolves several known spec tensions:
  - DESIGN.md §7 "6 adopted review/orch agents" vs §1.1's 11 adopted agents: tasklist builds to the fuller 11-agent inventory.
  - DESIGN.md §5 listing analyst under active_tier vs DESIGN.md §3.2 / agent-schemas.md §2.1 tier-invariant analyst: tasklist makes analyst tier-invariant.
  - kb-formats.md §3.2 prose "Four top-level keys" vs the enumerated 5 keys: tasklist builds to 5 keys.
- No structurally unmapped constraint among the six DESIGN.md §5 constraints; each has a mechanized tasklist item, though Finding A2 affects the correctness of constraint #6's implementation.
