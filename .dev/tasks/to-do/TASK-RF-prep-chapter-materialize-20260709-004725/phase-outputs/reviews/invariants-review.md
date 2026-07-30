# Phase 5 — Hard Invariants Review

**Date:** 2026-07-09 · Repo root: `/config/workspace/Infantalizer`

## Hard invariants (1–6)

| # | Invariant | Result | Evidence |
|---|-----------|--------|----------|
| 1 | `rewrite_phase_reads` byte-unchanged | **PASS** | grep-assert: all 3 paths present (`work/prep/<slug>/30-mapping.yaml`, `40-prep-brief.md`, `10-challenges.yaml`). `git diff` on path-contract.md shows NO added/removed line touching any of the 3 read-set path tokens (fenced §4 block intact; the added §4 note is outside the fence). |
| 2 | No 9th numbered package file | **PASS** | `git diff` shows no change to any `00`–`70` package-table row in §2; the manifest is added only as a `source/` sidecar (§6) + write-ownership rows (§5). |
| 3 | No second script; `check_boundary.py` byte-unchanged | **PASS** | `git diff --stat laf-adaptation/scripts/check_boundary.py` empty; `git status --porcelain laf-adaptation/scripts/` shows no new `.py` file. |
| 4 | `.claude/` mirror parity (readlink, not diff -r) | **PASS** | `readlink .claude/skills/chapter-materialize` → `../../laf-adaptation/skills/chapter-materialize` (correct relative symlink matching siblings). `.claude/commands/laf/prep.md` (canonical file) carries the `--source-mode` edit. |
| 5 | No adopted body touched | **PASS** | This task's footprint = 6 NATIVE edits (CLAUDE.md, VENDOR.md, agents/prep-cordinator.md, skills/prep/SKILL.md, skills/prep/resources/path-contract.md, source/README.md) + 1 NEW NATIVE skill dir (skills/chapter-materialize/). No ADOPTED file (writer.md / the ADOPTED-CLEAN quartet / any vendored body) changed. (Other dirty `work/`, `kb/`, `source/narnia/` files pre-date this task per the session-start git snapshot — unrelated.) |
| 6 | `check_boundary.py` exits 0 `PASS` (AC6) | **PASS** | `cd laf-adaptation && uv run python scripts/check_boundary.py` → exit 0, `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` (see `../test-results/check-boundary-summary.md`). |

## AC1–AC7 walkthrough (spec §13)

| AC | Requirement | Satisfied by | Verdict |
|----|-------------|--------------|---------|
| AC1 | Mode A (dir) and Mode B (monolith) each yield identical canonical `ch-<NN>.txt` + manifest, no manual pre-split | `chapter-materialize/SKILL.md` Stage 0.2 (mode detect) + 0.3 (five evidence layers) + 0.4 (commit) produce the same canonical set from either input; `## Format normalization & fidelity` identical | PASS |
| AC2 | `--source Books/LWW/` (split + monolith both present) does NOT auto-pick — raises a mode question | SKILL.md Stage 0.2 precedence rule #4: ambiguity → `mode_confidence: UNCERTAIN` → HALT-ask (split+monolith example carried verbatim); blocks any `source/` write until resolved | PASS |
| AC3 | Re-run vs `source/narnia/`, `source/tolkien/` adopts with zero byte rewrites (Mode C) | SKILL.md `## Idempotency, collisions, backward-compat`: Mode C adopt writes `provenance.class: ADOPTED`, re-run reads manifest first + no-ops on hash match; existing narnia ch-01..04 / tolkien ch-01 untouched | PASS |
| AC4 | No `ch-NN.txt` for a non-CERTAIN boundary before greenlight; single-signal never CERTAIN | SKILL.md Stage 0.4 bolded deferred-write invariant + Stage 0.3 bolded confidence rule ("CERTAIN requires ≥2 independent agreeing signals"; single-signal capped PROBABLE) | PASS |
| AC5 | Every manifest chapter row carries confidence + provenance + `needs_human_review`; every markup discard is a `normalization_event` with fidelity-risk | manifest v1 schema (SKILL.md `## Manifest output contract`) has per-chapter `title/split/order_confidence`, `provenance`, `needs_human_review`; `## Format normalization & fidelity` requires a `normalization_event` w/ `source_fidelity_risk` per discard | PASS |
| AC6 | `check_boundary.py` exits 0; read-set byte-unchanged; no 9th file; no second script | Invariants 1–3, 6 above all PASS | PASS |
| AC7 | Greenlight cannot reach CONFIRMED while any `ambiguous_split` / `needs_human_review` / high-risk loss unresolved | prep-cordinator STAGE 7 note (greenlight checklist +1 line; deferred commit on confirm; `review.status: PENDING→CONFIRMED` only after all resolved) + SKILL.md Stage 0.5 | PASS |

## Overall: **ALL PASS** (6/6 invariants + AC1–AC7). Proceed.
