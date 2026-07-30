# Proposal C — Minimal-Loop Manifest Enumerator (refactorer lens)

> Archived verbatim from the refactorer-lens agent (haiku). Variant C of 3.

## 1. Thesis
The smallest change satisfying S1–S7: **zero change to the frozen 3-file `rewrite_phase_reads`**; `chapter-manifest.yaml` is consumed as the **source-side chapter enumerator** — a structurally separate read surface from the prep-package read-set. Add **one NATIVE skill** (`chapter-iterate`) on `muse` via one additive `skills:` line; the entire 11-step workflow is reused unchanged. No new agent, script, or state file.

## 2. RQ1 (the crux) — read-set STAYS frozen at 3; manifest is a separate read surface
**Choice: `rewrite_phase_reads` byte-unchanged.** The manifest is read, but **not as a 4th prep-package member** — as part of **source-side chapter enumeration**, the same surface that already reads each `source/<slug>/ch-<NN>.txt` (the analyst does this today at step 1, unchallenged, not counted against the read-set).

- S1's intent (chapter *set* from the manifest, not eyeballing a directory) is honored: manifest is the authoritative enumerator.
- S5 (drift) genuinely requires reading the manifest — so the manifest **must** be read. The refactorer's move is "read it in the right category," not "don't read it."
- The frozen `rewrite_phase_reads` is defined in path-contract §4 as a list of **prep-package files** under `work/prep/<slug>/`. The manifest lives at `source/<slug>/chapter-manifest.yaml` — a **source-side sidecar**, not a prep-package member. Conflating "rewrite reads the manifest" with "rewrite_phase_reads gains an entry" is a category error.

**Minimal path-contract §4 change is a NOTE, not a list edit** restating prep §12's intent (source-side enumeration ≠ prep-package read-set).

## 3. RQ2 — REUSE step-1 analyst inline; cut the pre-rewrite stage
Analyst already `granularity=chapter`, already per-chapter, already at step 1. A pre-stage either re-runs step 1 (waste) or forces "skip step 1 if pre-staged" (new control flow) — both add moving parts for zero output delta.

## 4. RQ3 — REUSE filesystem done-markers (E3); no new state file
DONE iff accept-triple exists for every tier in the active set. In-flight = partial; not-started = nothing. `chapter-iterate` Globs once at loop entry. Flags: `--chapter N` (load-bearing single re-run) + `--chapters <range>` (zero-cost sugar); default = all manifest chapters on disk.

## 5. RQ4 — minimal honest drift response per class
- **Hash mismatch** → HALT that chapter; "re-run /laf:prep or edit the manifest hash." No auto-re-verify/re-prep (that's prep's job; pulling it in = scope creep + second writer into `source/`, violating C3).
- **`review.status:PENDING`** → HALT; folds into the greenlight gate (both are "is prep finished" checks).
- **Partial set** → iterate the intersection (manifest ∩ files-on-disk); surface missing as non-blocking note. Hard-failing would block the only real test case (4-of-17).
- **Manifest absent** → degrade to convention-discovery (`Glob ch-*.txt`, natural-sort); surface "no manifest — convention-discovery mode."

## 6. RQ5 — minimal flags
```
/laf:rewrite --work <slug> [--chapter N | --chapters <range>]
```
No `--source`/`--manifest` overrides (drift footgun + scope creep; manifest always convention-discovered at `source/<slug>/chapter-manifest.yaml`). Manifest guard folds into the greenlight gate.

## 7. RQ6 — tier fan-out stays inner loop (E2); preserve as-is
Chapter outer loop (now manifest-driven, was informal); tier inner loop at step 10; safety per (chapter,tier) at step 8; chronicler per tier at step 11 only on RECONCILED. Zero structural change to the 11-step workflow.

## Reuse inventory / BOM
REUSED UNCHANGED: analyst (step1), muse body (+1 skills line only), steps 2-9 quartet+writer, safety-verifier, tier-coordinator, chronicler accept-triple, greenlight gate, frozen 3-file read-set, filesystem done-markers, check_boundary.py.
ADDED: `chapter-iterate` skill (NATIVE); +1 `skills:` line on muse; ~10 lines in rewrite.md; §4 NOTE in path-contract (not a list edit); +1 NATIVE row in VENDOR.md. Zero adopted-body edits; Mode V green.

## Risks (honest under-delivery)
1. Convention-fallback can mask a missing manifest (drift detection unavailable without manifest) — honest trade for running on the real 4-of-17 partial set now.
2. SHA-256 halt is coarse (trailing-newline change halts) — coarse-but-safe.
3. No `--source`/`--manifest` override (operator can't point elsewhere).
4. Resume granularity is per-(chapter,tier), not per-step.
5. `--chapters` range parsing is model-executed, not runtime-validated (ADR-006).
6. Manifest-read not hash-pinned to prep (source-side); caught by per-chapter `output_sha256` drift on consequence.

## What it rejected
The heaviest alternative — 4th read-set entry + pre-rewrite analysis stage + progress-tracker state file — each rejected on refactorer grounds: 4th entry conflates prep-package read-set with source-enumeration surface (a §4 NOTE resolves it without an edit, and creates a hash-pinning scope-creep expectation); pre-stage duplicates step 1; progress file is a second source of truth that drifts from the filesystem. Smallest defensible thing satisfying S1–S7.
