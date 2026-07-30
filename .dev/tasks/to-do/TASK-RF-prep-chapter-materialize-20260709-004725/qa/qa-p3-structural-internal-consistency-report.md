# QA Report — Phase 3 Structural / Internal-Consistency Gate

**Topic:** prep ↔ chapter-materialize wiring (STAGE 0 materialization)
**Date:** 2026-07-09
**Phase:** phase-gate (Phase 3) — internal-consistency lens
**Fix cycle:** N/A (fix_authorization: false)
**Repo root:** /config/workspace/Infantalizer

Files verified (edited): `laf-adaptation/agents/prep-cordinator.md`, `laf-adaptation/skills/prep/SKILL.md`, `.claude/commands/laf/prep.md`
Cross-checked against: `laf-adaptation/skills/chapter-materialize/SKILL.md`, `laf-adaptation/skills/prep/resources/path-contract.md`

---

## Overall Verdict: FAIL

Two zero-tolerance internal-consistency defects (one IMPORTANT drift, one broken cross-reference that is simultaneously a boundary-contract self-contradiction), plus two MINOR drifts. Any consistency defect fails a structural gate.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Skill name exactly `laf-adaptation:chapter-materialize` / `chapter-materialize` everywhere; matches skill dir + frontmatter `name` | PASS | `grep` found the name in prep-cordinator (frontmatter L12 fully-qualified; body L50, L73 bare), prep/SKILL.md (L22, L133 fully-qualified), command (L25 bare). chapter-materialize frontmatter `name: chapter-materialize` (L2). Dir is `skills/chapter-materialize/`. No typo, no wrong prefix. |
| 2 | STAGE 0 behavior in prep-cordinator matches chapter-materialize stages 0.1–0.5 (source-access ABORT-first, detect mode, plan-no-writes, commit CERTAIN, defer PROBABLE/UNCERTAIN, manifest PENDING→CONFIRMED) | PASS | prep-cordinator L49–53 + L73–82 map 1:1 to CM 0.1 (source-access ABORT-first, L30–33), 0.2 (detect mode, L42–61), 0.3 (plan/no-writes, L63–89), 0.4 (commit CERTAIN + `.raw/` + manifest PENDING, L91–101), 0.5 (defer to §5 gate, L103–109). No contradiction. |
| 3 | "manifest is a source/ sidecar, NOT a 9th package file, NOT in rewrite_phase_reads" stated consistently in prep-cordinator, prep/SKILL.md §1, chapter-materialize | **FAIL** | prep/SKILL.md L24–25 states it ("`source/` **sidecar** — NOT a 9th package file and NOT a `rewrite_phase_reads` member"); chapter-materialize L170–172 states it ("`source/` sidecar — NOT a numbered package file, NOT a `rewrite_phase_reads` member"). **prep-cordinator states it NOWHERE** — `grep -i "sidecar\|9th\|rewrite_phase_reads\|numbered package"` on prep-cordinator returns zero hits. The task requires the claim in all three; it is absent from one. See Issue #1. |
| 4 | prep-cordinator STAGE 5 "also receives ambiguous_splits" + STAGE 7 greenlight ratification align with chapter-materialize Stage 0.5 gate-routing | PASS | prep-cordinator STAGE 5 note L97–101 (folds `ambiguous_splits` + `needs_human_review` into the same §5 block, "no new gate or HALT machinery"); STAGE 7 note L110–114 (greenlight cannot reach CONFIRMED while any unresolved; on CONFIRM commit deferred writes + flip manifest PENDING→CONFIRMED). Matches CM Stage 0.5 L105–109 verbatim in intent. |
| 5 | No literal package/read-set path restated in prep-cordinator or command; boundary "never restate a path" rule holds | **FAIL** | prep-cordinator L82 asserts "Chapter paths and the manifest path are owned by path-contract §5/§6; never restate them here" — but (a) path-contract has NO §6 (sections stop at §5), and (b) §5 is "Write-ownership" and does NOT define `source/<slug>/ch-<NN>.txt` or the manifest path at all. Meanwhile prep-cordinator DOES restate literal source paths at L52, L77 (`source/<slug>/ch-<NN>.txt`, `source/<slug>/.raw/`, `chapter-manifest.yaml`) while claiming "never restate them here." Broken pointer + self-contradiction. See Issue #2. |
| 6 | Command Mode A/B/C mapping matches mode-detect precedence in chapter-materialize + prep-cordinator | PASS (with MINOR enum drift, see Issue #3) | Command L22–23: Mode A=folder/directory, Mode B=single file/monolith, Mode C=adopt already-split. CM precedence L46–54: adopt(C)/folder(A)/file(B). Semantics of A/B/C are consistent across all three; `--source-mode` override honored in both (command L26, CM L58). Letter→mode mapping is sound. |

## Summary
- Checks passed: 4 / 6
- Checks failed: 2 (checks 3 and 5)
- Critical issues: 0
- IMPORTANT issues: 2
- MINOR issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `prep-cordinator.md` (missing) vs `prep/SKILL.md` L24–25 + `chapter-materialize/SKILL.md` L170–172 | The manifest "source/ sidecar — NOT a 9th/numbered package file, NOT a `rewrite_phase_reads` member" invariant is stated in prep/SKILL.md and chapter-materialize but is entirely absent from prep-cordinator. Check 3 explicitly requires the claim in all three wired surfaces. The coordinator is the agent that actually writes the manifest (L77), so its silence on the sidecar status is the most consequential omission. | Add one sentence to the prep-cordinator Stage 0 note (near L82) stating the manifest is a `source/` sidecar — not a 9th package file and not a `rewrite_phase_reads` member — or explicitly defer to prep/SKILL.md §1 for that invariant. |
| 2 | IMPORTANT | `prep-cordinator.md` L82 (pointer) + L52, L77 (restated paths) vs `path-contract.md` (§5 = Write-ownership; no §6) | Two-part defect. (a) Broken cross-reference: L82 says chapter/manifest paths "are owned by path-contract §5/§6" but path-contract has no §6, and §5 (Write-ownership) does not DEFINE the `source/<slug>/ch-<NN>.txt` or `chapter-manifest.yaml` paths — those literal paths are defined only in chapter-materialize, NOT in path-contract. (b) Self-contradiction against the boundary "never restate a path" rule: L82 says "never restate them here," yet L52 and L77 of the same file DO restate `source/<slug>/ch-<NN>.txt`, `source/<slug>/.raw/`, and `chapter-manifest.yaml`. | Correct the §-reference (the source/manifest paths are actually owned by chapter-materialize's Manifest output contract + Stage 0.4, not path-contract §5/§6 which does not define them). Either add a canonical source-path section to path-contract and point at it, or point at chapter-materialize. And reconcile the "never restate" claim with the literal paths appearing at L52/L77 (either remove the literals or soften the "never restate" assertion for the source/ tree). |
| 3 | MINOR | `.claude/commands/laf/prep.md` L3, L26 (`auto\|folder\|file\|adopt`) vs `chapter-materialize/SKILL.md` L181 manifest schema (`folder \| single-file \| adopt-existing`) | Two distinct token vocabularies for the same three modes with no stated mapping: operator-facing override tokens `file`/`adopt` vs persisted `input_mode` values `single-file`/`adopt-existing`. `folder` matches; the other two silently diverge. A reader cannot mechanically map `--source-mode file` to `input_mode: single-file`. | Add a one-line mapping note (e.g., in chapter-materialize near the schema or in the command) tying `file`↔`single-file` and `adopt`↔`adopt-existing`, or unify the tokens. |
| 4 | MINOR | `prep-cordinator.md` L78, L112 (`ambiguous_split`, singular) vs `chapter-materialize/SKILL.md` L100, L105, L219 (`ambiguous_splits[]`, the array) | prep-cordinator refers to "an `ambiguous_split`" (singular) for a single array entry. This is grammatically defensible (one element of the `ambiguous_splits[]` array) and prep-cordinator L53 + L100 also use the correct plural `ambiguous_splits`. Flagged for completeness only; not a true contradiction. | Optional: use `ambiguous_splits[]` entry phrasing for exactness, or leave as-is. |

## Cross-file coverage note

Checks 3, 5, and 6 are inherently cross-file. I verified them across the full set of five files named in scope (no partitioning — single instance), so cross-file coverage is complete for this gate.

## Recommendations
- Resolve Issue #1 (add the sidecar invariant to prep-cordinator) and Issue #2 (fix the broken §5/§6 pointer AND the "never restate" self-contradiction) before this wiring is considered internally consistent. Both are IMPORTANT and a structural gate is zero-tolerance.
- Issues #3 and #4 are MINOR but should be closed in the same pass — the enum-token divergence (#3) is the kind of silent drift that produces wrong manifest values at materialization time.

## Confidence Gate

Checklist categorization (6 items):
- [x] Check 1 (skill name) — VERIFIED via grep across all 5 files + frontmatter/dir inspection.
- [x] Check 2 (STAGE 0 behavior match) — VERIFIED by reading prep-cordinator L49–82 against CM Stages 0.1–0.5.
- [x] Check 3 (sidecar claim in all three) — VERIFIED (grep confirms absence from prep-cordinator; present in other two).
- [x] Check 4 (gate-routing alignment) — VERIFIED by reading CM Stage 0.5 against prep-cordinator STAGE 5/7 notes.
- [x] Check 5 (no restated path / broken pointer) — VERIFIED by reading path-contract section headers (§1–§5, no §6) + §5 body + prep-cordinator L52/L77/L82.
- [x] Check 6 (Mode A/B/C mapping) — VERIFIED by reading CM precedence L42–61 + command L22–26.

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 7 | Glob: 0 | Bash: 1 (mkdir)
  (No web research performed — all claims are intrinsic to local files; Tavily not required.)
- Unchecked items: none.
- Unverifiable items: none.

Tool-engagement check: 6 Read + 7 Grep = 13 verification tool calls ≥ 6 checklist items. Not padded — each Grep/Read targeted a specific check (skill-name grep → check 1; stage-count grep → checks 2/3; sidecar grep → check 3; input_mode grep → checks 2/6; ambiguous_split grep → check 4; path-contract section grep + Read → check 5).

## QA Complete
