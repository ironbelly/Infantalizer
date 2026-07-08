# Phase 0 (Vendor) — Consolidated Output Summary (Step PG0.1)

**Compiled:** 2026-07-03 | **Aggregates:** `discovery/upstream-cws-inventory.md`,
`test-results/boundary-init-summary.md`, `test-results/boundary-verify-phase0-summary.md`

## Executive summary

Phase 0 vendored the adopted CWS subset patch-clean and stood up the boundary contract. **11 adopted
agents + 12 adopted skills = 23 top-level adopted units (56 files recursively)** were vendored from the
pinned upstream checkout (`https://github.com/haowjy/creative-writing-skills` @
`3338495f0fabf778720effdda9386ab56d4ebf6e`) via `cw/` (Claude-lowered dialect), applying only the
deterministic prefix rewrite `creative-writing-skills:` → `laf-adaptation:` (plus one additive skill
line on `writer.md`). `check_boundary.py --init` wrote 56 manifest rows; both `--init` post-write verify
and standalone verify (with and without `--upstream`) exit 0 — **all rules A–F green.**

## Vendored artifacts

| Path (group) | Provenance Class | Vendored-From |
|--------------|------------------|---------------|
| `agents/{muse,critic,editor,reader-sim,continuity-checker,brainstormer,outliner,character-sim,style-creator,web-researcher}.md` (10) | ADOPTED-CLEAN | `cw/agents/<name>.md` @ pinned SHA |
| `agents/writer.md` | ADOPTED-PATCHED | `cw/agents/writer.md` + 1 additive `- laf-adaptation:adaptation-rules` |
| `skills/{writing-principles,creative-writing-craft,creative-writing-modes,story-review,story-memory,kb-management,shared-dao,llm-writing,writing-staffing,intent-modeling,grill-with-docs,creative-research}/` (12 dirs, 45 files) | ADOPTED-CLEAN | `cw/skills/<name>/**` @ pinned SHA |
| `VENDOR.md` | NATIVE (manifest) | authored (Step 2.12) + rows by `--init` |
| `NOTICE` | NATIVE | authored (Apache-2.0 attribution) |
| `LICENSE-CWS` | vendored verbatim | `cw/../LICENSE` (byte-identical, sha `c71d239d…`) |
| `CLAUDE.md` | NATIVE | authored (thin-entry pattern, conventions inline) |
| `scripts/check_boundary.py` | NATIVE (the only script) | authored (boundary-contract.md §3) |
| `.githooks/pre-commit` | NATIVE | authored (opt-in enforcement wrapper) |
| `.github/workflows/boundary.yml` (repo root) | NATIVE | authored (CI gate) |
| `kb/{canon,characters,world,timeline,styles,issues}/` + `kb/vocab.md` | ADOPTED scaffold | empty scaffold (runtime-populated) |
| `work/{drafts,critique-reports}/` | ADOPTED scaffold | empty scaffold (runtime-populated) |

## Gate results

| Gate | Command | Exit | Verdict |
|------|---------|------|---------|
| `--init` (populate manifest) | `check_boundary.py --init --upstream <ck>` | 0 | 56 rows written; post-write verify PASS |
| verify (CI mode) | `check_boundary.py` | 0 | A/D/E/F PASS; B/C skipped w/ note |
| verify (full) | `check_boundary.py --upstream <ck>` | 0 | A–F all PASS |

Disk↔manifest reconcile: 11 agents + 45 skill-tree files = **56** on disk = **56** manifest data rows.

## Blockers encountered

None. No fix cycles were needed. A pre-existing pinned upstream checkout at
`.dev/releases/current/0.1/creative-writing-skills` was used directly as the `--upstream` source
(recorded in the discovery inventory), avoiding a network clone.

## Overall Phase-0 verdict

**READY FOR PHASE 1** — the boundary gate is green on the complete adopted subset; the manifest is
populated and reconciles to the on-disk tree.
