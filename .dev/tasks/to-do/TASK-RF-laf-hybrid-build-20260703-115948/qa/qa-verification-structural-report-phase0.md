# QA Report — Fix Cycle (Phase Gate 0 Structural Verification)

**Topic:** LAF hybrid build — Phase Gate 0 PG0.4 fix verification
**Date:** 2026-07-03
**Phase:** fix-cycle
**Fix cycle:** verification pass (fix_authorization: FALSE — REPORT ONLY)

---

## Scope

Verify PG0.4 fixes (findings F1–F7) were actually applied to `laf-adaptation/CLAUDE.md` and
`laf-adaptation/VENDOR.md`, and that they introduced no new problems (no adopted file edited, no
Mars key introduced, VENDOR.md manifest table unchanged at 56 data rows, boundary gate exit 0).

## Overall Verdict: PASS

All 7 findings (F1–F7) are addressed in the text, the boundary gate exits 0, and no new
issue was introduced (no adopted file edited, no Mars key introduced, VENDOR.md manifest
table unchanged at 56 data rows).

---

## Per-finding verification

| # | Sev | File | Fix required | Addressed? | Evidence (verified in text) |
|---|-----|------|--------------|------------|------------------------------|
| F1 | CRITICAL | CLAUDE.md §2 ref + §4 tree | Annotate BOTH UPSTREAM-SYNC.md refs as authored later | **ADDRESSED** | §2 line 62: link now reads "(authored in Phase 4; present in the completed tree)". §4 tree line 124: comment reads "authored in Phase 4; present in the completed tree, not at Phase 0". Both references annotated. |
| F2 | CRITICAL | CLAUDE.md §2 | Add exact hook enable + bypass commands | **ADDRESSED** | §2 lines 73–74: new "Enabling the opt-in hook" bullet with `git config core.hooksPath laf-adaptation/.githooks` (run once, from repo root) and bypass `git commit --no-verify`. |
| F3 | IMPORTANT | CLAUDE.md §1 | Add "Non-manifested files" note classing residuals + state they are outside Rule-F glob | **ADDRESSED** | §1 lines 37–53: "Non-manifested files (outside the Rule-F hash-pin glob)" note classes scripts/ (NATIVE), kb/tiers + kb/adaptation-mapping (NATIVE verbatim YAML), kb/adaptations graft G1 (NATIVE), kb/ adopted layers (ADOPTED), templates/ (NATIVE), source/ (BUILD-NEW), NOTICE/LICENSE-CWS (attribution), NATIVE docs; closes with explicit "intentionally outside the Rule-F hash-pin glob". |
| F4 | IMPORTANT | CLAUDE.md §1 + §4 counts | Annotate 15/16 counts as target totals with present split | **ADDRESSED** | §1 lines 30–33: "Phase-0 present-state (counts are target totals)" note — 11 ADOPTED agents + 12 ADOPTED skills present now; +2 NATIVE +2 BUILD-NEW agents, +3 NATIVE +1 BUILD-NEW skills in Phases 1–2 (target 15/16). §4 tree lines 125–126: `agents/` and `skills/` comments rewritten to "TARGET … present now … authored in Phases 1–2". |
| F5 | IMPORTANT | CLAUDE.md §2 + §4 | Clarify CI workflow lives at git repo root, not under laf-adaptation/ | **ADDRESSED** | §2 lines 75–77: dedicated "CI location" bullet — workflow at git repo root `.github/workflows/boundary.yml` (NOT under laf-adaptation/, a subdir), with `working-directory: laf-adaptation`. Misleading inline path removed from the Enforcement line (line 72 no longer cites the CI path). |
| F6 | MINOR | VENDOR.md | Add re-vendor/refresh command pointer | **ADDRESSED** | VENDOR.md lines 14–17: HTML comment after Invariants block and BEFORE `## Manifest` (line 19) — `uv run python scripts/check_boundary.py --init --upstream <checkout>` then commit manifest diff (see UPSTREAM-SYNC.md). Placed outside the manifest table; table untouched. |
| F7 | MINOR | CLAUDE.md §4 tree | Annotate not-yet-created dirs (source/, templates/) | **ADDRESSED** | §4 tree line 132: `source/` — "created when the first work is adapted (later phase; not present at Phase 0)". Line 134: `templates/` — "authored in Phase 1 (not present at Phase 0)". |

**Addressed: 7 / 7.**

---

## No-new-issue verification

| Check | Result | Evidence |
|-------|--------|----------|
| Only CLAUDE.md + VENDOR.md changed; no adopted file edited | **PASS** | Boundary gate Rule A (adopted-file hash-match against VENDOR.md manifest) passed — every adopted `agents/*.md` and `skills/**/SKILL.md` body still matches its recorded `laf_sha256`. A body edit would flip Rule A to non-zero. `git status --porcelain laf-adaptation/agents laf-adaptation/skills` shows only `??` (whole tree untracked — nothing committed yet, so porcelain cannot show per-file drift; the hash-match gate is the authoritative integrity proof and it is GREEN). |
| No Mars key introduced | **PASS** | `grep -nE 'model-invocable\|model-policies\|effort:\|subagents:\|sandbox:\|type:'` over both edited docs returns only CLAUDE.md line 86 — the pre-existing prose rule *prohibiting* Mars keys ("**Never** introduce Mars keys — …"), not an introduced key. VENDOR.md: none. |
| VENDOR.md manifest table rows/hashes unchanged (56 data rows) | **PASS** | `grep -cE '^\| (agents\|skills)/'` = **56** data rows. Every row still begins with `agents/` or `skills/`; no spurious/renamed row. F6 pointer added as a comment BEFORE `## Manifest` (line 19), never inside the table (rows start line 23). Hashes byte-unchanged (Rule A pass confirms). |
| Boundary gate exit 0 | **PASS** | `uv run python laf-adaptation/scripts/check_boundary.py` → "BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied." **EXIT_CODE=0**. |

---

## Boundary gate output

```
NOTE: verify running without --upstream — Rules B and C (upstream-diff checks) skipped; Rule A hash-match covers adopted-file integrity against the recorded manifest, plus Rules D/E/F.
BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.
```
**Exit code: 0**

---

## Confidence

**Confidence:** "Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"

Checklist items (7 per-finding + 4 no-new-issue = 11), all VERIFIED with tool evidence:
- F1–F7: verified by Read of CLAUDE.md (lines 30–33, 37–53, 62, 73–77, 124–126, 132, 134) and VENDOR.md (lines 14–17).
- Boundary exit 0: verified by Bash (EXIT_CODE=0).
- Manifest 56 rows: verified by Bash grep -c.
- No Mars key: verified by Bash grep.
- No adopted-file edit: verified by boundary Rule A pass + git status --porcelain.

**Tool engagement:** "Read: 4 | Grep: 0 (via Bash) | Glob: 0 | Bash: 3"
(No web research performed — all claims are source-truth-local; Tavily not required.)

**Note on git porcelain:** `laf-adaptation/` is entirely untracked (`??`), so `git status --porcelain`
cannot show per-file modification of an adopted body. The authoritative "no adopted file changed"
proof is the boundary gate Rule A hash-match against the VENDOR.md manifest — which is GREEN — combined
with the 56-row/hash-unchanged manifest check. This is not a gap in verification; it is the correct
integrity mechanism for a not-yet-committed tree.

## QA Complete

