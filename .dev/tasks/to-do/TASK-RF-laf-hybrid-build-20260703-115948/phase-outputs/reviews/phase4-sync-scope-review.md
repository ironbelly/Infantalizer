# Phase-4 Sync-Scope Review (Step 6.2)

**Reviewed:** `laf-adaptation/UPSTREAM-SYNC.md` against `boundary-contract.md §5` | 2026-07-04

## Overall verdict: PASS

The documented sync flow touches ONLY ADOPTED-CLEAN (step 2) and ADOPTED-PATCHED (step 3) files; step 4
explicitly excludes NATIVE/BUILD-NEW; no step could touch a native/build-new file.

## Per-step provenance scope

| Step | Action | Provenance class touched |
|------|--------|--------------------------|
| 1 | Fetch upstream; pick new target SHA | none (upstream only, outside the tree) |
| 2 | 3-way reconcile per ADOPTED-CLEAN file (base==ours ⇒ fast-forward theirs) | **ADOPTED-CLEAN only** |
| 3 | Re-apply the single additive skill line on writer.md's body | **ADOPTED-PATCHED only** (writer.md) |
| 4 | **NEVER touch NATIVE / BUILD-NEW files** | **explicitly excludes NATIVE + BUILD-NEW** |
| 5 | `check_boundary.py --init --upstream <new>`; update upstream_sha + vendored_on | recomputes hashes for adopted rows; NATIVE/BUILD-NEW rows stay `—` (not written as content, only manifest metadata) |
| 6 | Re-run the Phase-3 hard gate | read-only verification (runs the workflow; does not sync-edit any file) |

**Conclusion:** the only files the sync flow *edits* are the ADOPTED subset (step 2 fast-forward + step 3
writer re-graft). The adaptation spine (`analyst`, `safety-verifier`, `adaptation-tiers`,
`adaptation-rules`, `source-fidelity`) and the greenfield components (`chronicler`, `tier-coordinator`,
`adaptation-safety`) — all NATIVE/BUILD-NEW — are never read, diffed, or written by the sync. This is
step 4 stated as an explicit invariant and reinforced by steps 2/3 scoping to adopted files only.

## Phase-3 hard-gate re-run requirement (confirmed present)

`UPSTREAM-SYNC.md` step 6 requires re-running the Phase-3 hard gate and confirming **all 5 gate
conditions** re-pass (v2.0 tags · safety PASS · per-tier canon · quartet ran · check_boundary green)
before a synced version ships. This is documented verbatim and matches `boundary-contract.md §5` step 6.

## Verdict
**PASS** — the sync flow is provably scoped to the adopted subset; NATIVE/BUILD-NEW are never touched; the
`--init` re-pin command and the Phase-3 hard-gate re-run requirement are both specified.
