# QA Report — Structural Internal-Consistency (Phase-0 Vendored Artifacts)

**Topic:** LAF `laf-adaptation/` Phase-0 vendored artifacts — internal consistency
**Date:** 2026-07-03
**Phase:** report-validation (structural internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY
**Lens:** INTERNAL-CONSISTENCY (adversarial stance)

Files in scope:
- `laf-adaptation/VENDOR.md`
- `laf-adaptation/NOTICE`
- `laf-adaptation/CLAUDE.md`
- `.dev/tasks/.../phase-outputs/discovery/upstream-cws-inventory.md`

---

## Overall Verdict: PASS

All 5 mandated checks passed under character-exact / set-equality verification. No internal
inconsistency found. The adversarial hypothesis ("at least 5 inconsistencies exist") is NOT
supported by the actual files. Zero fabricated findings were manufactured to satisfy the hypothesis
(Principle 9: report honestly; Principle 0: adversarial but evidence-based). One MINOR observational
note (M1) is recorded — it is not an inconsistency.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Adopted-file count: inventory (11 agents + 45 skill-tree = 56) == VENDOR manifest DATA rows | PASS | `grep -cE '^\| agents/'` = **11**; `grep -cE '^\| skills/'` = **45**; total = **56**. Inventory Summary table (lines 22-25) states 11 + 45 = 56. Exact match. Class breakdown among rows: 55 ADOPTED-CLEAN + 1 ADOPTED-PATCHED = 56. |
| 2 | Pinned `upstream_sha` char-exact across VENDOR.md / inventory / NOTICE | PASS | All three extract to `3338495f0fabf778720effdda9386ab56d4ebf6e` (40 hex). Shell string equality: VENDOR==NOTICE YES, VENDOR==INVENT YES. Only ONE 40-hex token exists in NOTICE and in the inventory's SHA fields — no stray/typo variant. VENDOR.md:4, NOTICE:14, inventory:8 & :16. |
| 3 | `vendored_on` valid ISO date (2026-07-03) and agrees with NOTICE | PASS | VENDOR.md:5 `vendored_on: 2026-07-03`; NOTICE:15 `Vendored on: 2026-07-03`. Grep of all `2026-NN-NN` dates across all 4 files = **4 occurrences, all `2026-07-03`**, zero divergent dates. Valid ISO-8601. |
| 4 | `prefix_rewrite` (`"creative-writing-skills:" -> "laf-adaptation:"`) consistent across VENDOR.md / NOTICE / CLAUDE.md | PASS | VENDOR.md:7 `"creative-writing-skills:" -> "laf-adaptation:"`; NOTICE:23 `"creative-writing-skills:"  ->  "laf-adaptation:"`; CLAUDE.md:22 `` `creative-writing-skills:` → `laf-adaptation:` ``. Same source token, same target token, same direction in all three. (Cosmetic-only differences: NOTICE double-spaces the arrow; CLAUDE.md uses the Unicode arrow `→` and backticks vs VENDOR's ASCII `->` and quotes. Semantically identical — see M1.) |
| 5 | Quartet {critic, editor, reader-sim, continuity-checker} each has a manifest row classed ADOPTED-CLEAN | PASS | All 4 present in VENDOR manifest as ADOPTED-CLEAN: continuity-checker (line 20), critic (line 21), editor (line 22), reader-sim (line 25). None missing, none mis-classed. Matches G3 invariant (VENDOR.md:10) and constraint #4 (CLAUDE.md:82). |

### Additional zero-trust cross-checks (beyond the 5 mandated — done to satisfy adversarial stance)

| Check | Result | Evidence |
|-------|--------|----------|
| Path SET-equality (not just count) between inventory target-path tables and VENDOR manifest | PASS | `comm` of sorted path sets: 0 paths in VENDOR-not-inventory, 0 real paths in inventory-not-VENDOR. (The one `comm` artifact `skills/X` is the literal example token in inventory prose line 52 `cw/skills/X → skills/X`, not a manifest row — false positive, discounted.) |
| Per-skill file-count table (inventory lines 106-118) vs VENDOR row counts | PASS | Recomputed all 12 skills from VENDOR: writing-principles 1+2=3, creative-writing-craft 1+9=10, creative-writing-modes 1+1=2, story-review 1+15=16, story-memory 1+6=7, six single-file skills 1+0=1 each. TOTAL 12 SKILL.md + 33 resources = 45. Byte-for-byte matches inventory's self-declared table AND its own target-path listing (10 craft rows, 16 story-review rows). |
| Class-summary reconciliation (inventory line 26: "10 agents + all 12 skills CLEAN, writer.md PATCHED") | PASS | VENDOR: agents ADOPTED-CLEAN=10, ADOPTED-PATCHED=1 (writer.md); all 45 skill rows ADOPTED-CLEAN (0 non-clean). Reconciles exactly. |
| ADOPTED-PATCHED writer.md carries two DISTINCT hashes (inventory line 34 claim) | PASS | upstream `373e605b…d769290` != laf `c1b3e12f…52e09534`. Distinct, as required by the +1 additive frontmatter line. |
| Hash-relationship logic: 45 skill rows IDENTICAL up==laf; 11 agent rows DISTINCT | PASS | Consistent with the model: resource bodies have no `creative-writing-skills:` token so the rewrite is a byte no-op (identical hashes); agents carry rewritten `skills:` frontmatter (distinct hashes). No contradiction. |

## Summary
- Checks passed: 5 / 5 mandated (+ 5 supplementary cross-checks all PASS)
- Checks failed: 0
- Critical issues: 0
- Inconsistencies found: **0**
- Observational notes (non-defect): 1 (M1)
- Issues fixed in-place: 0 (fix_authorization: FALSE)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| M1 | MINOR (observational, NOT an inconsistency) | VENDOR.md:7 vs NOTICE:23 vs CLAUDE.md:22 | The `prefix_rewrite` rule is rendered with cosmetically different punctuation in each file: VENDOR uses ASCII `->` + double-quotes; NOTICE uses ASCII `->` with double spaces around the arrow; CLAUDE.md uses the Unicode arrow `→` inside backticks. The **semantic content** (source token, target token, direction) is identical in all three, so this is NOT a declaration mismatch and does NOT fail Check 4. | None required for correctness. OPTIONAL: normalize the glyph/quoting for presentational uniformity if a house style demands it. Flagged only for completeness; would not block Phase-0. |

## Actions Taken
None. `fix_authorization: FALSE` — report only. No files were modified.

## Adversarial-Stance Statement
The spawn prompt asserted "at least 5 internal inconsistencies" exist (a count mismatch, a SHA typo,
a missing quartet row, a divergent prefix_rewrite). I actively hunted for each named class:
- **Count mismatch:** searched — counts reconcile at top-level (56), per-skill (45), and set-equality. NONE.
- **SHA typo:** compared char-by-char across 3 files; only one 40-hex token exists per file, all identical. NONE.
- **Missing quartet row:** all 4 present and ADOPTED-CLEAN. NONE.
- **Divergent prefix_rewrite:** semantically identical in all 3 files (only cosmetic glyph/quote differences). NONE.
- **Fifth (unspecified):** extended to per-skill arithmetic, class summaries, hash-relationship logic, dates, ADOPTED-PATCHED hashes. NONE.

The hypothesis is not supported by the evidence. I did not invent findings to meet a quota — a false
FAIL would corrupt the Phase-0 record just as a false PASS would (Principle 9).

## Confidence Gate

- Check 1 [x] VERIFIED — grep row counts + inventory table read
- Check 2 [x] VERIFIED — 40-hex token extraction + string equality across 3 files
- Check 3 [x] VERIFIED — date grep across 4 files (4× 2026-07-03, 0 divergent)
- Check 4 [x] VERIFIED — prefix_rewrite grep across 3 files, token/direction compared
- Check 5 [x] VERIFIED — quartet manifest rows grepped, all ADOPTED-CLEAN
- Supplementary (set-equality, per-skill, class summary, patched-hash, hash-logic) [x] all VERIFIED with tool output

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: (via Bash) | Glob: 0 | Bash: 7
(No web research performed — all claims verified against local source files; Tavily not required.)

Note on tool-engagement minimum: 4 Read + 7 Bash (each Bash bundles multiple targeted greps/awk each
mapping to a specific check) >> 5 mandated checks. Each tool call targeted a specific claim, not padding.

## Recommendations
- Phase-0 vendored artifacts are internally consistent. Green light for downstream phases on the
  internal-consistency dimension.
- OPTIONAL (M1): normalize prefix_rewrite glyph/quoting for presentational uniformity — cosmetic only, non-blocking.
- Out of scope for THIS lens (not checked here): whether the recorded `laf_sha256` values actually
  match the bytes of the on-disk vendored files, and whether the pinned upstream_sha resolves in the
  upstream repo. Those are content-fidelity / provenance checks for a different lens.

## QA Complete
