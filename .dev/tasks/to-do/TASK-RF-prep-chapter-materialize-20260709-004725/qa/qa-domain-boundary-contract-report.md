# QA Report — Domain / Boundary-Contract Accuracy (final-gate, 7th lens)

**Topic:** chapter-materialize NATIVE skill — LAF provenance & boundary-contract domain accuracy
**Date:** 2026-07-09
**Phase:** doc-qualitative (final-gate, M3 domain lens: boundary-contract-domain accuracy)
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Lens:** Judge as a DOMAIN expert whether authored artifacts honor the LAF provenance & boundary model (`laf-adaptation/CLAUDE.md` §1 provenance + §2 boundary contract, ADR-006).

---

## Overall Verdict: PASS

Adversarial mandate acknowledged: I was instructed to assume ≥5 boundary-contract-domain errors exist and find them. I hunted exhaustively — byte-level em-dash dumps, symlink resolution, name-collision checks, classifier inspection, script-integrity git-status, additive-only diff review, and a live run of the machine gate. After that hunt the honest finding is **zero boundary-contract-domain errors**. The one observation surfaced (a schema-template worked-example) is not an error under any severity (see "Non-issues examined"). The "assume ≥5" instruction is an adversarial stance, not a quota; I did not manufacture findings to satisfy it.

## Items Reviewed
| # | Check (boundary-contract-domain) | Result | Evidence |
|---|----------------------------------|--------|----------|
| 1 | chapter-materialize classified NATIVE (auto by classify() default, not in NATIVE_SKILLS/BUILD_NEW_SKILLS) | PASS | VENDOR.md:124 `NATIVE`; `check_boundary.py:46-47` sets unchanged, `chapter-materialize` in neither; classify() L363-367 returns NATIVE for a non-upstream skill not in BUILD_NEW_SKILLS |
| 2 | NOT added to NATIVE_SKILLS / BUILD_NEW_SKILLS (correct — those sets are not allowlists) | PASS | `grep chapter-materialize scripts/check_boundary.py` → 0 hits in the sets (only line 365 uses BUILD_NEW_SKILLS generically) |
| 3 | No name collision with an upstream skill (Rule E) | PASS | Not in the ADOPTED-CLEAN manifest rows; no `skills/chapter-materialize` upstream entry; boundary-facts §1 confirms non-upstream |
| 4 | Single VENDOR row, `skills/chapter-materialize/**` glob form (Rule-F/F′: one row covers SKILL.md + resources/boundary-rules.yaml) | PASS | `grep -c chapter-materialize VENDOR.md` = 1; row is `skills/chapter-materialize/**`; git diff shows exactly +1 row; F′ skips NATIVE dirs (only iterates adopted skill dirs, L667-675) |
| 5 | Em dashes U+2014 (byte-for-byte vs sibling NATIVE rows) | PASS | `od -tx1` of the row → both hash cells are `e2 80 94` (U+2014); en-dash (`e2 80 93`) grep = 0; all 12 NATIVE/BUILD-NEW rows carry exactly 2 U+2014 |
| 6 | check_boundary.py untouched + SOLE script (ADR-006 — no 2nd script/runtime/CLI/test-runtime added) | PASS | `git status` on check_boundary.py = clean (no diff); `scripts/` holds only check_boundary.py (+ pre-existing test_check_boundary.py + __pycache__); no new script authored |
| 7 | No adopted body edited (every edited file is NATIVE or a new NATIVE addition) | PASS | git status: only NATIVE files changed (CLAUDE.md, VENDOR.md, prep-cordinator.md, prep/SKILL.md, path-contract.md, source/README.md) + new NATIVE skill dir; zero ADOPTED-CLEAN/ADOPTED-PATCHED rows touched |
| 8 | Native knowledge enters prep spine ONLY additively (frontmatter line + STAGE 0 body — never by editing an adopted body) | PASS | prep-cordinator.md git diff: +1 `- laf-adaptation:chapter-materialize` frontmatter line, STAGE 0 prepended, count 8→9, Stage-5/Stage-7 notes appended; STAGE 1-8 bodies byte-stable; agent is NATIVE (VENDOR:121) so free-authored anyway |
| 9 | `.claude/skills/chapter-materialize` is a relative SYMLINK into laf-adaptation/ (matches sibling convention), not a copy | PASS | `readlink` → `../../laf-adaptation/skills/chapter-materialize`; symlink resolves (SKILL.md + resources/boundary-rules.yaml readable); identical relative form to all 18 sibling skill symlinks |
| 10 | VENDOR.md and source/README.md correctly have NO `.claude` mirror | PASS | `.claude/VENDOR.md` and `.claude/source` do not exist; only skills/ and agents/ are mirrored (harness-visible dirs) |
| 11 | path-contract remains single source of truth (no body restates a literal package/read-set path) | PASS | `grep -c 30-mapping` = 0 in chapter-materialize SKILL.md and in prep.md command; Stage-0 note explicitly defers path literals to the contract; read-set grep-assert (30-mapping/40-prep-brief/10-challenges) all present, unchanged |
| 12 | No 9th numbered package file introduced (manifest is a `source/` sidecar) | PASS | path-contract §2 still lists exactly the 8 `00`–`70` files; §4 note + §6 declare the manifest a sidecar NOT a package file and NOT a rewrite_phase_reads member; prep SKILL §1 note repeats "NOT a 9th package file"; no `chapter-manifest` file materialized under source/ (build-time; runtime output) |
| 13 | Live machine gate reproduces baseline PASS (AC6) | PASS | `cd laf-adaptation && uv run python scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` / EXIT_CODE=0 |
| 14 | resources/boundary-rules.yaml is data-only, no runtime (ADR-006) | PASS | Header states "DATA ONLY, no runtime; check_boundary.py does NOT read this file"; content is declarative regex/hint patterns; covered by the `/**` glob row, no separate manifest row |

## Summary
- Checks passed: 14 / 14
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization: false)

## Issues Found
None. No issue of any severity was found in the boundary-contract-domain lens.

## Non-issues examined (adversarial candidates that did NOT rise to findings)

1. **Manifest schema worked-example uses `work: narnia` + `chapter_count: 17` while the repo's narnia is a 4-chapter ADOPTED set (ch-01..04).** Examined closely as a candidate contradiction (SKILL.md L176-223 vs the idempotency rule L131-134 and the on-disk 4-file set). **Not an error:** the block is explicitly introduced as "the v1 schema below" and every field carries `|`-separated enum placeholders (`input_mode: folder | single-file | adopt-existing`, `mode_confidence: CERTAIN | PROBABLE | UNCERTAIN`) and literal placeholders (`<ISO-8601>`, `"..."`, `"Books/LWW/....html"`). It is a schema-shape template using LWW's real 17-chapter full-materialize as an illustrative header, NOT a factual state claim about the adopted 4-chapter narnia. It carries zero provenance / classification / glob / em-dash / symlink / script-integrity / additive-editing implication, so it does not touch the boundary-contract-domain lens.

2. **path-contract §5 lists `config/concept_mapping/templates/<slug>_mapping.yaml` (outside laf-adaptation/) as a write-ownership target.** Examined as a possible boundary-escape. **Not an error and out of lens:** this is a pre-existing dual-form promotion target (the root v1.0 layer), unchanged by this task's diff, and it is a promotion-write ownership row, not a provenance/hash-pin claim. Outside the boundary-contract-domain scope of this lens.

3. **prep-cordinator.md (an agent body) was edited.** Confirmed permissible: it is a NATIVE row (VENDOR.md:121), not ADOPTED/ADOPTED-PATCHED. NATIVE bodies may be authored freely; the edits are additive regardless. The boundary contract's "never edit an adopted body" rule (CLAUDE.md §2) is not implicated.

## Self-Audit (MANDATORY)

1. **How many factual claims did I independently verify against source?** 14 checklist checks, each backed by ≥1 tool call: em-dash bytes via `od -tx1`; classifier via Read+grep of check_boundary.py L44-368; symlink via `readlink` + resolution test; script integrity via `git status`; additive-only via `git diff` of prep-cordinator.md and VENDOR.md; single-source-of-truth via `grep -c 30-mapping`; read-set via the 3-path grep-assert; and the live machine gate (`check_boundary.py` → PASS/exit 0).
2. **What specific files did I read?** All 9 authored/edited artifacts (chapter-materialize/SKILL.md, resources/boundary-rules.yaml, prep-cordinator.md, prep/SKILL.md, prep.md command, path-contract.md, source/README.md, VENDOR.md) + the ground-truth check_boundary.py, laf-adaptation/CLAUDE.md, and both QA inputs (qa-input-inventory.md, boundary-facts.md). Plus filesystem inspection of source/narnia/, .claude/skills/, .claude/agents/, scripts/.
3. **If I found 0 issues, why should the user trust I checked thoroughly?** Because the evidence is concrete and reproducible, not impressionistic: I byte-dumped the em-dashes (`e2 80 94` ×2), counted VENDOR rows (exactly 1 added, shown in git diff), resolved the symlink target string, confirmed check_boundary.py has an empty git-status (untouched), and ran the actual boundary gate to a green PASS/exit-0. Each PASS cites the file:line or command output that produced it. I also documented three adversarial candidates I chased down and explain precisely why each is not a finding — a false-PASS would have swallowed at least the narnia/17-chapter candidate silently.
4. **Web research?** None performed — this lens is entirely local-file/machine-gate bound. Tavily not invoked; no fallback used.

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: (within Bash) ~14 | Glob: 0 (used ls/find via Bash) | Bash: 7

## Recommendations
- Proceed. The chapter-materialize NATIVE skill honors the LAF provenance & boundary model completely: correct NATIVE auto-classification, single U+2014 glob VENDOR row, sole-script ADR-006 invariant intact, additive-only spine wiring, correct relative symlink mirror, path-contract single-source preserved, no 9th package file, and a live `BOUNDARY CONTRACT: PASS`.
- Optional (non-blocking, outside this lens): if a future editor wants to remove all ambiguity from the manifest schema worked-example, annotate the block header with `# illustrative full-materialize example — not the adopted narnia state`. This is a cosmetic nicety, not a boundary-contract requirement.

## QA Complete
