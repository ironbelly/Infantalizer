# Phase Gate 0 — Fix-Applied Summary (Step PG0.5)

**Applied:** 2026-07-03
**Fix agent:** rf-qa (single authorized serialized fix agent, fix_authorization: TRUE)
**Scope:** NATIVE docs only — `laf-adaptation/CLAUDE.md` and `laf-adaptation/VENDOR.md`. No adopted file touched. No upstream-verbatim content normalized.

---

## Findings applied (F1–F7)

| # | Severity | File edited | What changed |
|---|----------|-------------|--------------|
| F1 | CRITICAL | CLAUDE.md | Annotated **both** `UPSTREAM-SYNC.md` references — §2 inline link now reads "(authored in Phase 4; present in the completed tree)", and the §4 tree comment now reads "authored in Phase 4; present in the completed tree, not at Phase 0". Removes the Phase-0 dead-pointer confusion. |
| F2 | CRITICAL | CLAUDE.md §2 | Added the exact enable command `git config core.hooksPath laf-adaptation/.githooks` (run once from repo root) and the bypass `git commit --no-verify` as a new "Enabling the opt-in hook" bullet under the Enforcement block. |
| F3 | IMPORTANT | CLAUDE.md §1 | Added a "Non-manifested files (outside the Rule-F hash-pin glob)" note classing `scripts/` (NATIVE tooling), `kb/tiers` + `kb/adaptation-mapping` (NATIVE carried-verbatim YAML), `kb/adaptations/<work>/tier-<N>/` (NATIVE graft G1), `kb/` adopted layers (ADOPTED scaffold), `templates/` (NATIVE), `source/` (BUILD-NEW), `NOTICE`/`LICENSE-CWS` (attribution), and the NATIVE docs — explicitly stating they are intentionally outside the Rule-F hash-pin glob. |
| F4 | IMPORTANT | CLAUDE.md §1 + §4 | Annotated counts as **target totals** with the Phase-0 present split. Added a "Phase-0 present-state" note to §1 (11 ADOPTED agents + 12 ADOPTED skills present now; +2 NATIVE +2 BUILD-NEW agents and +3 NATIVE +1 BUILD-NEW skills authored in Phases 1–2). Rewrote the §4 `agents/` and `skills/` tree comments to the same "TARGET … present now … authored in Phases 1–2" form. |
| F5 | IMPORTANT | CLAUDE.md §2 | Removed the misleading inline `.github/workflows/boundary.yml` from the Enforcement line and added a dedicated "CI location" bullet clarifying the workflow lives at the **git repo root** `.github/workflows/boundary.yml` (NOT under `laf-adaptation/`), with `working-directory: laf-adaptation`. |
| F6 | MINOR | VENDOR.md | Added the re-vendor pointer as an HTML **comment** in the header area, placed after the Invariants block and **before** `## Manifest` (never inside the manifest table): to re-vendor at a new upstream_sha, run `uv run python scripts/check_boundary.py --init --upstream <checkout>` then commit the manifest diff (see UPSTREAM-SYNC.md). Manifest table rows and hashes untouched. |
| F7 | MINOR | CLAUDE.md §4 | Annotated the not-yet-created tree dirs: `source/` — "created when the first work is adapted (later phase; not present at Phase 0)"; `templates/` — "authored in Phase 1 (not present at Phase 0)". |

---

## Hard-constraint compliance

- **Adopted files:** untouched. Only `CLAUDE.md` and `VENDOR.md` (both NATIVE, both outside the Rule-F glob) were edited.
- **Upstream-verbatim content:** not normalized. The recorded "Non-actionable observations" (dormant sibling-skill refs, `model: inherit`, cosmetic `prefix_rewrite` glyphs, un-vendored plugin.json) were NOT changed.
- **VENDOR.md manifest table:** rows and hashes are byte-unchanged. The F6 pointer was added as a comment in the header/Invariants area only.

---

## Post-fix boundary gate

Command (from `/config/workspace/Infantalizer`):
`uv run python laf-adaptation/scripts/check_boundary.py`

Output:
```
NOTE: verify running without --upstream — Rules B and C (upstream-diff checks) skipped; Rule A hash-match covers adopted-file integrity against the recorded manifest, plus Rules D/E/F.
BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.
```

**Exit code: 0** (boundary gate stays GREEN — VENDOR.md edits did not disturb the manifest table).

---

## Result

- Fixes applied: **7 / 7** (F1–F7)
- Post-fix `check_boundary.py` exit code: **0**
