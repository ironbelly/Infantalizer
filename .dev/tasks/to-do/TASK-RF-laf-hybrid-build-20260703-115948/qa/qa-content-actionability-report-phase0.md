# QA Report — ACTIONABILITY lens (Phase-0 LAF framework docs)

**Topic:** LAF Phase-0 — CLAUDE.md + VENDOR.md actionability
**Date:** 2026-07-03
**Phase:** doc-qualitative (ACTIONABILITY lens)
**Fix cycle:** N/A (fix_authorization: FALSE — REPORT ONLY)
**Scope:** `/config/workspace/Infantalizer/laf-adaptation/CLAUDE.md`, `/config/workspace/Infantalizer/laf-adaptation/VENDOR.md`

---

## Overall Verdict: FAIL

7 findings (2 CRITICAL, 3 IMPORTANT, 2 MINOR). The enforcement command is concrete and
runnable, but the upstream-sync pointer targets a file that does not exist, the only command
that arms enforcement is absent from the guidance doc, and the Provenance Model leaves several
real on-disk file classes unclassifiable.

---

## Items Reviewed (ACTIONABILITY checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every instruction specific enough to execute without interpretation | FAIL | STOP/add-a-skill rule (L27) is crisp & actionable; but §2 tells a contributor the hook is "opt-in" without the concrete enable command, and the tree lists paths that don't exist. |
| 2 | Enforcement + upstream-sync pointers name EXACT commands | FAIL | Enforcement command `uv run python scripts/check_boundary.py` is exact and VERIFIED to run (PASS). Upstream-sync pointer → `UPSTREAM-SYNC.md` which does NOT exist → names zero commands. Enable command `git config core.hooksPath ...` exists only inside the hook file, never in CLAUDE.md. |
| 3 | Provenance Model classifies ANY new file unambiguously (3 hypotheticals) | FAIL | Agent/skill files classify cleanly. But `scripts/`, `kb/*.yaml`, `templates/`, `source/`, root docs have no manifest row and the §1 table's editing-rule column gives no rule for them. 2 of 3 hypotheticals are unclassifiable. |

---

## Summary
- Checks passed: 0 / 3
- Checks failed: 3
- Critical issues: 2
- Issues fixed in-place: 0 (report-only)

## What I Verified (tool evidence)
- **Read** both in-scope files in full (CLAUDE.md 109 lines, VENDOR.md 74 lines).
- **Read** `scripts/check_boundary.py` (459 lines) — confirmed Rule F iterates `disk_agents()` (`agents/*.md`) + `disk_skill_skillmds()` (`skills/**/SKILL.md`) only, so CLAUDE.md L10's Rule-F glob claim is ACCURATE.
- **Ran** `uv run python scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS`. Enforcement command is real and works (Rules A/D/E/F run without `--upstream`).
- **Verified** git root = `/config/workspace/Infantalizer` (repo root); `laf-adaptation/` is a subdir; CI lives at repo-root `.github/workflows/boundary.yml` (VERIFIED present) — NOT under `laf-adaptation/`.
- **Verified** `agents/writer.md` frontmatter: single additive `- laf-adaptation:adaptation-rules` line + preserved duplicate `creative-writing-craft` line — CLAUDE.md L41-44 ADOPTED-PATCHED claim ACCURATE.
- **Verified filesystem** for every path the docs name (see findings): `UPSTREAM-SYNC.md`, `templates/`, `source/`, `LICENSE`, and all 4 NATIVE + 4 BUILD-NEW agents/skills are ABSENT; the 11 ADOPTED agents + 12 ADOPTED skill dirs are PRESENT and manifested.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | CLAUDE.md:39 and CLAUDE.md:96 (and L108) | The upstream-sync pointer links to `[`UPSTREAM-SYNC.md`](UPSTREAM-SYNC.md)` (twice) and the tree calls it "the 6-step upstream-sync procedure (Phase 4)", but **the file does not exist** anywhere in the repo. The entire upstream-sync side of Check 2 gestures at a procedure that names zero commands. A contributor following the boundary-contract rationale ("a 3-way merge against upstream stays a clean fast-forward … see UPSTREAM-SYNC.md") hits a dead link and cannot execute the sync. | Either (a) author `laf-adaptation/UPSTREAM-SYNC.md` with the concrete 6-step procedure incl. exact commands (`git checkout <upstream_sha>`, the prefix-rewrite step, `uv run python scripts/check_boundary.py --init --upstream <dir>`, `uv run python scripts/check_boundary.py`), or (b) if Phase-0 defers it, replace both links with a non-link "(authored in Phase 4 — not yet present)" marker so no dead pointer ships. |
| 2 | CRITICAL | CLAUDE.md §2 (L45-49) | Enforcement is called "opt-in" but the **concrete command that arms it is never given in CLAUDE.md**. `git config core.hooksPath laf-adaptation/.githooks` exists ONLY as a comment inside `.githooks/pre-commit` (L6-7). A contributor reading the guidance doc is told to opt in with no instruction how. This is a "gestures at an action without the concrete command" failure — exactly what Check 2 targets. | In §2 after the pre-commit sentence, add the exact enable line: `Enable once per clone: `git config core.hooksPath laf-adaptation/.githooks`` (and the bypass `git commit --no-verify`). Do not rely on the reader opening the hook file to discover it. |
| 3 | IMPORTANT | CLAUDE.md §1 heading (L18) + editing-rule column (L20-25) vs on-disk `scripts/`, `kb/`, `templates/`, root docs | The §1 heading asserts "**every file** is ADOPTED, NATIVE, or BUILD-NEW", but the classification table only supplies an *editing rule* for agents and skills. Real on-disk files with no class + no manifest row + no editing rule: `scripts/check_boundary.py`, `kb/vocab.md`, `kb/tiers/*.yaml` (planned), `NOTICE`, `LICENSE-CWS`, and (per the tree) `templates/`, `source/`. `check_boundary.py`'s Rule F only manifests `agents/*.md` + `skills/**/SKILL.md`, so these are silently unmanaged — the model's "every file" promise is not backed by an actionable rule. | Add an explicit row (or a "Non-manifested files" note) covering the residual classes: e.g. `scripts/` = NATIVE tooling (not hash-pinned, single-script rule per ADR-006); `kb/` runtime + `kb/tiers`/`kb/adaptation-mapping` = NATIVE carried-verbatim YAML; `source/` = BUILD-NEW; root docs (`NOTICE`, `LICENSE-CWS`, `CLAUDE.md`, `VENDOR.md`) = ADOPTED-attribution / NATIVE. State that these are intentionally outside the Rule-F glob. |
| 4 | IMPORTANT | CLAUDE.md §1 table L24 (`analyst.md`, `safety-verifier.md`), L25 (`chronicler.md`, `tier-coordinator.md`); skills L24-25; L97-98 counts | The Provenance Model and the "Where things live" counts present NATIVE/BUILD-NEW exemplars as present ("15 agent files", "16 skill dirs"), but **all 4 native/build-new agents and all 4 native/build-new skills are absent** (only 11 agents / 12 skill dirs on disk). For a Phase-0 scaffold this is expected, but a contributor told "author NATIVE like `agents/analyst.md`" cannot open that file as a pattern, and the stated totals don't match reality — an interpretation gap. | Mark the not-yet-authored NATIVE/BUILD-NEW rows and the L97-98 counts as forward-looking (e.g. "target: 15 agents — 11 ADOPTED present; 2 NATIVE + 2 BUILD-NEW authored in later phases"), so the doc's present-tense claims match the Phase-0 tree. |
| 5 | IMPORTANT | CLAUDE.md:49 and tree L108 vs actual CI path | §2 says CI `.github/workflows/boundary.yml` "runs it", and the tree implies the workflow is inside the laf-adaptation tree. The file actually lives at **repo-root** `/config/workspace/Infantalizer/.github/workflows/boundary.yml` (VERIFIED), because `laf-adaptation/` is a git subdir, not the git root. A contributor looking for `laf-adaptation/.github/workflows/boundary.yml` (as the tree suggests) will not find it. | State the CI path is at the **git repo root** `.github/workflows/boundary.yml` (with `working-directory: laf-adaptation`), not inside the laf-adaptation tree. The tree diagram should either omit it or annotate "(at repo root, not under laf-adaptation/)". |
| 6 | MINOR | CLAUDE.md:96 references "Phase 4"; VENDOR.md has no cross-ref to the sync procedure | "the 6-step upstream-sync procedure (Phase 4)" names a phase but no command surface, and VENDOR.md — the pinned manifest the sync consumes — never points back at the sync procedure or the `--init --upstream` refresh command. The re-vendor path (`--init --upstream <dir>`) is documented only in `check_boundary.py`'s docstring, not in either in-scope doc. | Add to VENDOR.md a one-line "To re-vendor at a new upstream_sha: `uv run python scripts/check_boundary.py --init --upstream <checkout>` then commit the manifest diff" pointer, so the manifest and its refresh command live together. |
| 7 | MINOR | CLAUDE.md tree L104, L106 (`source/`, `templates/`) | The "Where things live" tree lists `source/` (BUILD-NEW) and `templates/` (NATIVE, "carried verbatim") as if present, but neither directory exists on disk yet. A reader treating the tree as ground truth will look for directories that aren't there. | Annotate not-yet-created dirs (e.g. "created when first work is adapted") or use a legend distinguishing present vs planned entries. |

---

## Check 3 detail — 3 hypothetical-file classification trials

Per the ACTIONABILITY check, I tried to classify 3 hypothetical new files using ONLY CLAUDE.md §1
+ VENDOR.md + `check_boundary.py`'s `classify()`:

1. **`agents/plot-doctor.md`** (new LAF-authored agent, no upstream twin) → **RESOLVES.** §1 NATIVE
   rule + `classify()` L211-213 (non-upstream agent not in `BUILD_NEW_AGENTS` → NATIVE) both give
   NATIVE unambiguously. Rule E (no upstream name collision) is checkable. PASS.

2. **`kb/tiers/tier_2.yaml`** (new tier profile YAML) → **UNCLASSIFIABLE by the §1 table.** The
   editing-rule table only describes agents & skills; `classify()` returns a default "NATIVE" for
   any non-agent/non-skill path (L219), but there is **no manifest row, no hash pin, and the §1
   "every file is ADOPTED/NATIVE/BUILD-NEW" heading is not backed by a rule the contributor can
   apply** — L70 conventions call these "carried-verbatim NATIVE", but a first-time contributor
   reading §1 alone cannot derive that. Ambiguous → FAIL (Finding #3).

3. **`scripts/refresh_hashes.py`** (a hypothetical second script) → **DIRECTLY CONTRADICTORY.** L13-14
   says "there is exactly ONE script … Do not add other scripts", so the file is forbidden — yet §1
   provides no class for `scripts/` at all, and `classify()` would silently label it NATIVE. The
   provenance model and the one-script rule disagree about whether a `scripts/` file is even
   representable. A contributor cannot cleanly classify it. FAIL (feeds Finding #3).

Result: 1/3 clean, 2/3 unclassifiable/ambiguous → Check 3 FAILS.

---

## Self-Audit

**(a) Reliance list — rf-qa (structural) PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was provided in the spawn prompt; this review ran standalone
  (no reliance on a prior structural pass). All structural facts below were independently verified.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Enforcement command executability — verified by **Bash** `uv run python scripts/check_boundary.py` → exit 0, `BOUNDARY CONTRACT: PASS`.
- Rule-F glob-coverage claim (CLAUDE.md L10) — verified by **Read** of `check_boundary.py:401` (`disk_agents() + disk_skill_skillmds()`) + `:182`/`:196` glob defs.
- Dead-pointer detection (`UPSTREAM-SYNC.md`) — verified by **Bash** `find … -iname '*upstream*sync*'` → no results, and `ls UPSTREAM-SYNC.md` → No such file.
- CI path topology — verified by **Bash** `git rev-parse --show-toplevel` (repo root) + `ls .github/workflows/boundary.yml` present at repo root, absent under laf-adaptation/.
- Provenance exemplar existence — verified by **Bash** per-file `test -f` loop: all 4 NATIVE + 4 BUILD-NEW agents/skills MISSING; 11 ADOPTED agents present.

## Confidence
- Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 5 | Grep: 0 (grep folded into Bash) | Glob: 0 | Bash: 6

## Recommendations
- Resolve #1 and #2 (CRITICAL) before this doc set ships as guidance — both leave a contributor
  unable to execute a named action (upstream sync; arming enforcement).
- Resolve #3-#5 (IMPORTANT) to make the Provenance Model's "every file" promise real and to stop the
  tree/counts from asserting present-tense facts that don't match the Phase-0 tree.

## QA Complete
