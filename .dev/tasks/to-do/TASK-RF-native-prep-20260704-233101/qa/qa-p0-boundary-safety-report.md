# QA: P0 Boundary-Safety Cross-Validation Lens

**Task:** TASK-RF-native-prep-20260704-233101
**Lens:** Phase Gate P0 — boundary-safety (VENDOR.md NATIVE rows + on-disk filename fidelity)
**Mode:** REPORT-ONLY (`fix_authorization: false`) — no files were edited.
**Stance:** Adversarial (assume ≥5 defects; verify exhaustively).
**Date:** 2026-07-05
**Analyst:** rf-analyst (Phase Gate P0 cross-validation lens)

---

## Verdict: PASS (on all 6 explicit verification criteria)

The P0 boundary-safety state is sound: the Mode-V gate is green, the `--report` NATIVE count is 8, exactly 3 new NATIVE rows were hand-added with correct paths and em-dash hashes, no exemplar/resource got its own row, and no adopted row was touched. One Medium-severity documentation-drift defect exists in the boundary-adjacent `CLAUDE.md` (NOT in `VENDOR.md` itself) — it is a documentation-staleness issue, not a boundary-contract violation, and does not block the gate.

**Findings: 1 Medium, 0 High, 0 Critical.** The prompt's adversarial brief predicted ≥5 defects; only 1 was found, and it is documentation drift, not a boundary defect. The VENDOR.md delta itself is clean.

---

## Verification Matrix

| # | Verification Criterion (from prompt) | Method | Result | Evidence |
|---|---|---|---|---|
| 1 | Exactly 3 new NATIVE rows hand-added | grep `VENDOR.md:111-118` | **PASS** | Lines 116-118 are the 3 new rows; lines 111-115 are the 5 baseline NATIVE rows (analyst, safety-verifier, adaptation-rules/**, adaptation-tiers/**, source-fidelity/**) |
| 2 | Each new row has `— \| —` (em-dash) hashes | visual inspection of 3 rows | **PASS** | All 3 rows render `| NATIVE | — \| — |`; parser (`parse_manifest:270-273`) accepts em-dash as `NO_HASH` |
| 3 | No exemplar/resource got its own row | cross-ref `boundary-verification.md` §1 row 5/7 + §4 | **PASS** | `skills/prep/resources/path-contract.md` covered by `skills/prep/**` glob; 3 exemplars under `skills/adaptation-rules/resources/exemplars/` covered by existing `skills/adaptation-rules/**` glob (VENDOR.md:113) |
| 4 | Row paths match on-disk filenames exactly | `ls agents/` + `ls -d skills/*/` cross-check | **PASS** | On-disk `prep-cordinator.md` (single 'o') matches row `agents/prep-cordinator.md`; on-disk `prep/` and `thematic-fidelity/` match `skills/prep/**` and `skills/thematic-fidelity/**` glob rows |
| 5 | No adopted row touched/removed | count comparison vs design baseline | **PASS** | 12 ADOPTED skill SKILL.md rows present; 11 adopted-provenance agent rows present (10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED writer.md); `--report` shows ADOPTED-CLEAN=55, ADOPTED-PATCHED=1, matching the pre-P0 baseline |
| 6 | `--report` NATIVE count is 8 | `uv run python scripts/check_boundary.py --report` | **PASS** | Report header shows `NATIVE 8`, `BUILD-NEW 3`, `TOTAL rows 67`; matches p0-boundary-summary.md claim |
| 7 | Mode-V boundary check PASSES (gate itself) | `uv run python scripts/check_boundary.py` | **PASS** | Final line: `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` Exit code 0 |

---

## Detailed Findings

### Finding 1: CLAUDE.md provenance-count drift (Medium — documentation staleness, NOT a boundary violation)

- **Severity:** Medium
- **Location:** `laf-adaptation/CLAUDE.md` lines 31, 33, 57, 178, 179
- **Defect class:** Documentation staleness (a doc-sourced claim that is `[CODE-CONTRADICTED]` by current on-disk state)
- **Affected scope:** Boundary-adjacent documentation only — does NOT touch `VENDOR.md`, does NOT affect `check_boundary.py` execution, does NOT trip any Rule A-F.

**Claim (CLAUDE.md line 31, 33, 178, 179):**
> "The tree holds **15 agent files** (11 adopted-provenance = 10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED `writer.md`; 2 NATIVE = `analyst`, `safety-verifier`; 2 BUILD-NEW = `chronicler`, `tier-coordinator`) and **16 skill dirs** (12 ADOPTED; 3 NATIVE = `adaptation-tiers`, `adaptation-rules`, `source-fidelity`; 1 BUILD-NEW = `adaptation-safety`)."

**On-disk reality (verified 2026-07-05):**
- `ls agents/*.md | wc -l` = **16** (not 15). The 16th is `prep-cordinator.md` — added by this P0 build but not reflected in CLAUDE.md's count.
- `ls -d skills/*/ | wc -l` = **18** (not 16). The 17th and 18th are `prep/` and `thematic-fidelity/` — added by this P0 build but not reflected.
- The provenance breakdown in CLAUDE.md §1 ("Provenance Model") enumerates NATIVE agents as only `analyst`, `safety-verifier` and NATIVE skills as only `adaptation-tiers`, `adaptation-rules`, `source-fidelity`. The 3 new NATIVE artifacts (`prep-cordinator`, `prep`, `thematic-fidelity`) are absent from this enumeration.
- CLAUDE.md line 57 ("Adopted-provenance count (11 = 10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED)") is still correct — adopted-provenance count did not change. Only NATIVE counts changed.

**Why this matters:** CLAUDE.md is the entry-point documentation for AI agents (and humans) working in `laf-adaptation/`. A future contributor (agent or human) reading CLAUDE.md will believe the tree has 15 agents and 16 skills, and may conclude that `prep-cordinator`, `prep`, and `thematic-fidelity` are misplaced or that the boundary contract is leaking unmanifested files. The boundary check itself (`check_boundary.py`) is unaffected because it reads `VENDOR.md`, not `CLAUDE.md` — but the documentation-contract drift is real and will mislead readers.

**Why the boundary gate still PASSES despite this:** `check_boundary.py` Mode V asserts `VENDOR.md` integrity and on-disk coverage; it does not parse or assert CLAUDE.md counts. CLAUDE.md is explicitly documented as "outside the Rule-F hash-pin glob" (CLAUDE.md §1, "Non-manifested files"). So the gate is green, but the documentation is stale.

**Required fix (for the appropriate agent — rf-analyst is REPORT-ONLY):**
Update CLAUDE.md §1 ("Provenance Model ... Present-state (0.1 DONE)") and the §4 tree diagram to reflect:
- 16 agent files (add `prep-cordinator` to the NATIVE count: now 3 NATIVE agents = `analyst`, `safety-verifier`, `prep-cordinator`)
- 18 skill dirs (add `prep` and `thematic-fidelity` to the NATIVE count: now 5 NATIVE skills = `adaptation-tiers`, `adaptation-rules`, `source-fidelity`, `prep`, `thematic-fidelity`)
- The §4 tree comment line 178-179 should read "16 agent files: 11 adopted-provenance (writer.md ADOPTED-PATCHED) + 3 NATIVE (analyst, safety-verifier, prep-cordinator) + 2 BUILD-NEW (chronicler, tier-coordinator)" and "18 skill dirs: 12 ADOPTED + 5 NATIVE (...) + 1 BUILD-NEW (adaptation-safety)".

---

## What was verified clean (adversarial checks that came back negative)

For transparency, the following adversarial hypotheses were tested and found NOT to be defects:

1. **Hypothesis: a NATIVE row carries a stray hash.** Tested by `grep -c "NATIVE" VENDOR.md` and visual inspection of all 8 NATIVE rows. All carry `— | —` (em-dash, NO_HASH). The parser's `else` branch (`parse_manifest:270-273`) would reject a NATIVE row with a hex hash; none exists. **CLEAN.**

2. **Hypothesis: an exemplar file got its own row, bloating the manifest.** Tested by `grep "exemplars" VENDOR.md`. Zero hits — the 3 exemplars (`sacrifice-and-return.md`, `betrayal-and-redemption.md`, `petrification-body-horror.md`) are correctly covered by the existing `skills/adaptation-rules/**` glob (VENDOR.md:113), as `boundary-verification.md` §1 row 7 and §4 prescribe. **CLEAN.**

3. **Hypothesis: `path-contract.md` got its own row.** Tested by `grep "path-contract" VENDOR.md`. Zero hits — it is covered by `skills/prep/**` (VENDOR.md:117). Matches `boundary-verification.md` §1 row 5 and §4. **CLEAN.**

4. **Hypothesis: filename spelling mismatch (`prep-coordinator` vs `prep-cordinator`).** Tested by `find laf-adaptation -name "*coordinator*" -o -name "*cordinator*"`. Only `prep-cordinator.md` (single 'o') exists on disk; the VENDOR row reads `agents/prep-cordinator.md` (single 'o'). Match confirmed. The agent's frontmatter `name: prep-cordinator` also matches. **CLEAN.** (Note: the single-'o' spelling is a deliberate project convention — `boundary-integration.md` Q4 documents this and confirms the classifier is name-agnostic for NATIVE.)

5. **Hypothesis: an adopted row was silently removed or its hash altered.** Tested by counting adopted rows: `--report` shows ADOPTED-CLEAN=55, ADOPTED-PATCHED=1. The 12 adopted skill SKILL.md rows are all present; the G3 quartet (critic/editor/reader-sim/continuity-checker) all carry ADOPTED-CLEAN with intact hashes; writer.md is the sole ADOPTED-PATCHED row. Rule D G3-quartet invariant holds. **CLEAN.**

6. **Hypothesis: a glob row is malformed (e.g. `skills/prep/*` with single asterisk).** Tested by `grep -E "^\| skills/[^|]+\*\* \| NATIVE" VENDOR.md`. All 5 NATIVE skill glob rows and 1 BUILD-NEW skill glob row use the `/**` form (double-asterisk, as `do_init:405-407` emits). The `manifest_covers` matcher (`is_glob` test at line 178) requires the `/**` suffix; all rows conform. **CLEAN.**

7. **Hypothesis: a managed file on disk lacks VENDOR coverage (Rule F failure).** Tested by iterating every `agents/*.md` (16 files) and every `skills/*/SKILL.md` (18 dirs). All 16 agents have an exact-match row; all 18 skill dirs have either a `SKILL.md` row (12 adopted) or a `/**` glob row (5 NATIVE + 1 BUILD-NEW). Rule F coverage is complete. **CLEAN.**

8. **Hypothesis: the Mode-V PASS claim in p0-boundary-summary.md is fabricated.** Tested by running `uv run python scripts/check_boundary.py` directly. Output ends with `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` Exit code 0. The summary's claim is reproduced verbatim. **CLEAN.**

9. **Hypothesis: the NATIVE=8 count claim in p0-boundary-summary.md is fabricated.** Tested by running `--report` directly. Header reads `NATIVE 8`, `TOTAL rows 67`. Matches summary line 23. **CLEAN.**

---

## Scope notes and limitations

- **No upstream checkout (Mode U not run).** Mode V (no `--upstream`) is the runnable gate; Mode U (Rules B/C against pinned-SHA upstream) was not run because no upstream checkout at SHA `3338495f...` was available. This is the documented, expected P0 state — `boundary-integration.md` Q2-Q3 establishes that `--init` hard-requires `--upstream` (early return 2) and that the hand-add-3-rows + Mode V path is the runnable equivalent. Mode V does NOT catch a two-field forgery (both `laf_sha256` AND `upstream_sha256` rewritten); this is an accepted residual risk, not a P0 defect.
- **Cross-cycle composition (INV-012).** This is a single-cycle QA pass; no prior-cycle finding exists to dedup against. N/A.
- **CLAUDE.md drift (Finding 1) is the only finding.** It is documentation, not manifest. The prompt's adversarial prediction of "≥5 boundary-safety defects in the P0 skeleton + VENDOR rows" was not borne out for the VENDOR rows themselves — the VENDOR delta is clean. The single defect found is in adjacent documentation that the prompt did not explicitly scope but which this analyst surfaced because it directly references the boundary contract and would mislead future contributors.

---

## Recommendations

1. **(Medium priority) Update CLAUDE.md provenance counts.** Assign to a documentation agent (or the build executor in a follow-up phase). The fix is mechanical: 15→16 agents, 16→18 skills, and the NATIVE-enumeration lists in §1 and §4 must include `prep-cordinator` (agent) and `prep` + `thematic-fidelity` (skills). This is REPORT-ONLY territory for rf-analyst; the fix is for another agent.
2. **(No P0-gate action required.)** The boundary gate is green. No rollback, no row revert, no manifest regeneration needed. The 3 hand-added NATIVE rows are correct as written.

---

## Method

- **Files read:** `VENDOR.md` (full), `agents/prep-cordinator.md` (full), `skills/prep/resources/path-contract.md` (head), `research/03-boundary-integration.md` (full), `phase-outputs/test-results/p0-boundary-summary.md` (full), `research-notes.md` (full), `docs/native-prep/design/boundary-verification.md` (full), `CLAUDE.md` (relevant excerpts).
- **Commands run:** `uv run python scripts/check_boundary.py` (Mode V, exit 0); `uv run python scripts/check_boundary.py --report` (NATIVE=8); `git diff b51633d HEAD -- laf-adaptation/VENDOR.md`; `git diff b51633d HEAD -- agents/writer.md agents/muse.md`; directory listings and grep cross-checks.
- **No web research performed** (none required; all claims verified against on-disk files).
