---
name: laf-boundary-contract
description: Hard boundary-contract invariants any LAF prep/rewrite task build must preserve; verified live 2026-07-09
metadata:
  type: project
---

The LAF adaptation subsystem (`laf-adaptation/`) has a boundary contract enforced by `scripts/check_boundary.py`. Any task that edits the prep/rewrite spine MUST preserve these invariants or the build is malformed.

**Why:** ADR-006 mandates `check_boundary.py` be the SOLE script and a validator only; the contract protects the vendored CWS (upstream) surface from LAF-native drift. Breaking it silently regresses the adopted/native separation.

**How to apply:** when building a LAF task, encode VALIDATION items (not tests) for:
- `cd laf-adaptation && uv run python scripts/check_boundary.py` must exit 0 with `BOUNDARY CONTRACT: PASS` (Mode V, no --upstream). Baseline PASSes.
- The 8-file `00`-`70` package table (path-contract.md §2) stays byte-unchanged; source-side sidecars (e.g. `chapter-manifest.yaml`) are NOT a 9th numbered file.
- The frozen 3-file `rewrite_phase_reads` (path-contract §4: `work/prep/<slug>/30-mapping.yaml`, `40-prep-brief.md`, `10-challenges.yaml`) stays byte-unchanged.
- `check_boundary.py` itself stays byte-unchanged; a NEW native skill auto-classifies NATIVE via `classify()` default (line ~367) — do NOT add it to `NATIVE_SKILLS`/`BUILD_NEW_SKILLS`.
- No ADOPTED body edited. NATIVE files carry `laf_sha256 = —` (body edits are hash-free).
- VENDOR.md: a new NATIVE skill needs EXACTLY ONE glob row `| skills/<name>/** | NATIVE | — | — |` with U+2014 em dashes (bytes e2 80 94) in both hash cells; the `/**` covers SKILL.md AND resources/** in one Rule-F/F′ row (no per-file rows for NATIVE dirs).

See [[laf-claude-mirror-symlink]] for the mirror mechanics.
