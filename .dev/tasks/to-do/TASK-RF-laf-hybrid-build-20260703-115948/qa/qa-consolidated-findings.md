# Phase Gate 0 — Consolidated QA Findings (Step PG0.4)

**Compiled:** 2026-07-03 | **Sources:** 7 lens reports (4 structural + 3 content)

## Lens verdict rollup

| Lens | Agent | Verdict | Blocking issues |
|------|-------|---------|-----------------|
| template-conformance | rf-qa | PASS | 0 (2 MINOR observations) |
| internal-consistency | rf-qa | PASS | 0 (1 non-defect note) |
| evidence-quality | rf-qa | PASS | 0 |
| boundary-contract-fidelity | rf-qa-qualitative | PASS | 0 (1 informational note) |
| **actionability** | rf-qa-qualitative | **FAIL** | **7 (2 CRITICAL, 3 IMPORTANT, 2 MINOR)** |
| source-fidelity | rf-qa-qualitative | PASS | 0 (2 out-of-scope observations) |
| domain-accuracy | rf-qa-qualitative | PASS | 0 |

**Boundary gate itself: GREEN** (all 7 lenses confirmed `check_boundary.py` exit 0; A–F hold). The FAIL is
purely documentation-actionability in the two NATIVE docs (CLAUDE.md, VENDOR.md) — no adopted file, no
boundary violation, no fidelity breach.

## Consolidated actionable findings (deduplicated)

Root cause of most: CLAUDE.md describes the **target** complete tree, but Phase 0 is a partial state
(native/build-new agents+skills, `templates/`, `source/`, and `UPSTREAM-SYNC.md` are authored in later
phases). Fix = make the present-vs-planned distinction explicit and add two genuinely-missing command
pointers. All fixes touch ONLY `laf-adaptation/CLAUDE.md` and `laf-adaptation/VENDOR.md` (NATIVE docs —
never an adopted body).

| # | Severity | File | Issue | Fix to apply |
|---|----------|------|-------|--------------|
| F1 | CRITICAL | CLAUDE.md (§2 ref + tree) | `[UPSTREAM-SYNC.md](UPSTREAM-SYNC.md)` is referenced but the file is not authored until Phase 4 — a dead link at Phase 0. | Annotate both references so the reader knows it is authored in the upstream-sync phase (e.g. "see UPSTREAM-SYNC.md (authored in Phase 4)"). It legitimately exists in the completed tree; the annotation removes the Phase-0 dead-pointer confusion. |
| F2 | CRITICAL | CLAUDE.md §2 | Hook is called "opt-in" but the enable command is only inside `.githooks/pre-commit`, never in CLAUDE.md. | Add the exact enable + bypass commands to §2: `git config core.hooksPath laf-adaptation/.githooks` and `git commit --no-verify`. |
| F3 | IMPORTANT | CLAUDE.md §1 | "every file is ADOPTED/NATIVE/BUILD-NEW" but no rule covers `scripts/`, `kb/` YAML, `templates/`, `source/`, root docs (all outside the Rule-F glob). | Add a "Non-manifested files" note classing the residuals (scripts/ = NATIVE tooling, single-script per ADR-006; kb/tiers + kb/adaptation-mapping = NATIVE carried-verbatim YAML; kb adopted layers = ADOPTED scaffold; source/ = BUILD-NEW; templates/ = NATIVE; NOTICE/LICENSE-CWS = attribution; CLAUDE.md/VENDOR.md/UPSTREAM-SYNC.md = NATIVE) and state they are intentionally outside the Rule-F hash-pin glob. |
| F4 | IMPORTANT | CLAUDE.md §1 table + §4 counts | "15 agents / 16 skills" and the NATIVE/BUILD-NEW exemplars are present-tense, but in Phase 0 only 11 agents / 12 skills exist. | Annotate counts as target totals with the present-state split (e.g. "15 agent files total — 11 ADOPTED present now; +2 NATIVE +2 BUILD-NEW authored in Phases 1–2"). |
| F5 | IMPORTANT | CLAUDE.md §2 + §4 tree | CI path implied under laf-adaptation/, but `.github/workflows/boundary.yml` lives at the **git repo root** (laf-adaptation/ is a subdir), with `working-directory: laf-adaptation`. | Clarify the CI workflow is at the repo-root `.github/workflows/` (not under laf-adaptation/), with `working-directory: laf-adaptation`. |
| F6 | MINOR | VENDOR.md | No pointer to the re-vendor/refresh command; the manifest and its refresh command live apart. | Add a one-line note to VENDOR.md: to re-vendor at a new upstream_sha, run `uv run python scripts/check_boundary.py --init --upstream <checkout>` then commit the manifest diff (see UPSTREAM-SYNC.md). |
| F7 | MINOR | CLAUDE.md §4 tree | `source/` and `templates/` listed as if present, but not created until later phases. | Annotate not-yet-created dirs in the tree (e.g. "source/ — created when the first work is adapted"; "templates/ — authored in Phase 1"). |

## Non-actionable observations (recorded, no fix needed)

- template-conformance MINOR: adopted skills reference sibling skills `story-planning`/`project-setup`
  that are dormant/not-adopted; `continuity-checker` uses `model: inherit`. Both are **upstream-verbatim
  content** — editing them would violate the boundary contract. NO FIX (carried faithfully by design).
- source-fidelity out-of-scope: upstream `.claude-plugin/plugin.json` not vendored (intentional — Mars/
  plugin packaging is cut per DESIGN §2); `adaptation-rules` skill absent in Phase 0 (forward reference,
  authored Phase 1). NO FIX.
- internal-consistency: `prefix_rewrite` cosmetic glyph/quote differences across docs — semantically
  identical. NO FIX.

## Fix scope for the PG0.4 fix agent

Apply F1–F7 to `laf-adaptation/CLAUDE.md` and `laf-adaptation/VENDOR.md` only. Do NOT edit any adopted
file. Do NOT normalize upstream-verbatim content. After fixes, re-run `check_boundary.py` to confirm the
boundary gate stays exit 0.
