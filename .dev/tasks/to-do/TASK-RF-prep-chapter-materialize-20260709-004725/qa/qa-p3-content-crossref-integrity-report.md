# QA Report — Phase-3 Content Cross-Reference Chain Integrity

**Topic:** LAF native-prep Phase 3 (Stage-0 / chapter-materialize wiring)
**Date:** 2026-07-09
**Phase:** doc-qualitative (LENS: cross-reference-chain-integrity)
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Adversarial stance:** Assumed ≥5 errors; traced every Phase-3 cross-reference to resolution.

---

## Overall Verdict: FAIL

Two genuine cross-reference defects found (one CRITICAL-adjacent semantic mis-resolution, one
IMPORTANT stale stage-count contradiction between two edited files), plus confirmation of the
expected within-build forward-ref. Under NO-LENIENCY rules, any unresolved defect = FAIL.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `laf-adaptation:chapter-materialize` skill dir + SKILL.md + frontmatter `name:` + `.claude` symlink | PASS | Dir `laf-adaptation/skills/chapter-materialize/` exists; `SKILL.md` (14104 B) exists; frontmatter line 2 `name: chapter-materialize` matches dir; symlink `.claude/skills/chapter-materialize -> ../../laf-adaptation/skills/chapter-materialize` resolves (readlink -f confirms). Frontmatter ref `- laf-adaptation:chapter-materialize` (prep-cordinator.md:12) is fully-qualified and valid. |
| 2 | path-contract §5/§6 references | FAIL | See Finding #1. §5 exists but = "Write-ownership" (path-contract.md:75), NOT chapter/manifest path ownership. §6 does not exist (acceptable Phase-4 forward-ref per brief). But path-contract contains ZERO mention of `ch-<NN>.txt` / `chapter-manifest.yaml` / `source/<slug>/` — the "owned by" claim is false today. |
| 3 | prep SKILL §1 / §3 / §5 / §6 sections exist | PASS | prep/SKILL.md: §1 Path contract (:15), §3 Two-track analysis (:61), §5 Question-gate (:83), §6 Greenlight (:94). All four exist and contain the referenced content. |
| 4 | `chapter-manifest.yaml` / `source/<slug>/ch-<NN>.txt` / `.raw/` naming consistency | PASS | Naming identical across all 3 edited files + chapter-materialize SKILL.md: `source/<slug>/ch-<NN>.txt`, `chapter-manifest.yaml`, `source/<slug>/.raw/`. Deferred-write variant `ch-NN.txt` used consistently for the un-templated form. No drift. |
| 5 | command → `SKILL.md §1 Stage-0 note` resolves | PASS | prep.md:25 cites "SKILL.md §1 Stage-0 note"; the Stage-0 note is a blockquote inside §1 (prep/SKILL.md:21–26). Resolves correctly. |
| 6 | Orphaned / dangling "see X" references | FAIL | See Finding #2 (stage-count contradiction — command says "8-stage", coordinator now "9-stage"). Other refs clean: `prep-agent-schemas.md §5.1` resolves (docs/native-prep/design/prep-agent-schemas.md:221, correct target); `rewrite.md` exists; `.claude/skills/prep` + `.claude/agents/prep-cordinator.md` symlinks resolve; `ambiguous_splits` defined in chapter-materialize and consumed in prep-cordinator (no orphan). |

## Summary
- Checks passed: 4 / 6
- Checks failed: 2
- Critical issues: 1
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence
Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 5 | Grep: (within Bash) | Glob: 0 | Bash: 6
Every trace target was resolved against the actual filesystem (ls/readlink/grep/git diff), not
asserted from memory. Tool calls ≥ checklist items.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | prep-cordinator.md:82 | "Chapter paths and the manifest path are owned by **path-contract §5/§6**." Today path-contract §5 = **Write-ownership** (a who-writes-what table), and it does NOT define or "own" chapter/manifest path *naming*. path-contract.md contains **zero** occurrences of `ch-<NN>.txt`, `chapter-manifest.yaml`, or `source/<slug>/` anywhere in §1–§5. The paths are actually defined in `chapter-materialize/SKILL.md`, not the path-contract. So the "owned by §5" half of the reference points at a section that exists but does not contain the referenced content (violates cross-ref-content rule: the target must actually hold what is cited). The §6 half is a legitimate Phase-4 forward-ref (§6 will be added then) — flagged as a **within-build forward-ref, NOT a broken link**, per brief item 2. But the combined "§5/§6" citation is currently mis-resolving on its §5 leg. | Either (a) defer the WHOLE citation to §6 only (`path-contract §6`) since chapter/manifest path ownership is the Phase-4 addition, not §5's write-ownership concern; OR (b) if §5 is intended to be restructured in Phase 4 to include path-naming, add an explicit "(added in Phase 4)" within-build forward-ref marker to the §5/§6 citation so a reader in Phase 3 does not resolve §5 to the current Write-ownership table and find no chapter-path definition. As written, a reader following the pointer today lands on Write-ownership and finds no chapter/manifest path spec. |
| 2 | IMPORTANT | .claude/commands/laf/prep.md:11 | Stage-count contradiction between two Phase-3-edited files. The command says: "The `prep-cordinator` owns the **8-stage** procedure." Phase 3 changed prep-cordinator.md from 8→9 stages (git diff confirms: "Owns the **9-stage** prep pipeline (STAGE 0 + the 8 below)", ## The 9 stages). The command was edited in the same Phase 3 (git diff shows the `--source-mode` + Stage-0 additions) but its "8-stage" claim was left stale. A reader of the command is told 8 stages; the coordinator it delegates to runs 9. Contradiction across edited files = never MINOR (Critical Rule #6). | In prep.md:11 change "owns the 8-stage procedure" → "owns the 9-stage procedure (Stage 0 + the 8 below)" (or "8-stage §1–§8 procedure plus the prepended Stage 0"), matching the coordinator's own framing at prep-cordinator.md:21,26–27. |

### Note on brief item 2 (§6 forward-ref) — resolved as acceptable
path-contract §6 does not exist today; §5 = Write-ownership is the last section. Per the brief, the
§6 leg is an expected Phase-4 forward reference and is **not** counted as a broken link. It is
recorded here as a within-build forward-ref. The FAIL on Finding #1 is specifically about the **§5
leg mis-resolving** (§5 exists but holds write-ownership, not path ownership) plus the absence of
any chapter/manifest path definition in the path-contract that the "owned by path-contract" phrasing
promises.

## Actions Taken
None — fix_authorization: false. All findings documented for the orchestrator to route to a fixer.

## Recommendations
1. Resolve Finding #1: retarget the prep-cordinator.md:82 citation to `path-contract §6` alone (the
   Phase-4 section that will define chapter/manifest paths), OR add an explicit "(§6 added in
   Phase 4; chapter/manifest paths not in §5 today)" within-build forward-ref marker so the §5 leg
   does not mislead a Phase-3 reader.
2. Resolve Finding #2: update prep.md:11 "8-stage" → "9-stage" to match the coordinator.
3. After fixes, re-run this cross-reference trace (single fix cycle expected — both are one-line edits).

## Self-Audit (mandatory)
1. **Factual claims verified against source:** 6/6 trace items, each resolved against the actual
   filesystem — skill dir/SKILL.md existence (ls), frontmatter `name:` (Read line 2), symlink
   resolution (readlink -f), path-contract section inventory (grep `^## `), naming consistency
   (grep across 4 files), Stage-0-note location (sed on §1), stage-count (git diff of both files),
   schemas §5.1 target (grep), rewrite.md + prep/agent symlink existence (ls/readlink).
2. **Files read:** prep-cordinator.md, prep/SKILL.md, .claude/commands/laf/prep.md,
   chapter-materialize/SKILL.md, path-contract.md (all fully); plus filesystem/git checks on
   symlinks, prep-agent-schemas.md, rewrite.md.
3. **Why trust this (2 issues found, not 0):** the review is adversarial and evidence-backed — the
   §5-leg mis-resolution was caught by grepping path-contract for `ch-<NN>`/`chapter-manifest`/
   `source/` and finding ZERO hits, proving the "owned by §5" claim has no target content; the
   stage-count contradiction was caught by diffing both edited files and observing the coordinator
   went 8→9 while the command's "8-stage" line was untouched. Neither is a judgment call — both are
   filesystem/diff facts.
4. **Web research:** none performed (all checks are local-file-bound); Tavily-first policy not
   triggered.

## QA Complete
