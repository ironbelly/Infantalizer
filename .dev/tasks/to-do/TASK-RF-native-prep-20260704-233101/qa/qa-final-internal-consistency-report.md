# QA Report — Phase 6 FINAL Internal-Consistency Lens

**Topic:** Native prep adaptation — final consolidated gate, internal-consistency lens
**Date:** 2026-07-05
**Phase:** report-validation (final / internal-consistency)
**Fix cycle:** N/A (REPORT-ONLY, `fix_authorization: false`)

---

## Overall Verdict: FAIL

(7 internal-consistency defects found; adversarial-stance target was ≥5. Verdict is FAIL because 4 of
the 7 are CRITICAL — they break the boundary-contract invariant or leave a delegated agent unreachable
at the load step.)

## Verification Targets
Cross-references verified:
1. prep-cordinator `skills:` names match skills that exist — **PASS** (all 6 skill dirs confirmed on disk)
2. commands delegate to agents that exist — **PASS** (prep.md → prep-cordinator; rewrite.md → muse)
3. analyst `meaning:` field name vs tier-coordinator Check D consumer — **PASS** (token `meaning:` consistent)
4. VENDOR rows match on-disk paths (3 new NATIVE rows) — **PASS** (all 3 rows map to extant files)

(Layer-2 cross-cutting checks below then surfaced the 7 defects.)

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | prep-cordinator `skills:` → on-disk skill dirs | PASS | Bash `ls skills/`: all 6 of {source-fidelity, adaptation-tiers, adaptation-rules, kb-management, prep, thematic-fidelity} present with SKILL.md |
| 2 | prep.md command → prep-cordinator agent exists | PASS | `ls agents/prep-cordinator.md` OK; prep.md L8 names `prep-cordinator` |
| 3 | rewrite.md command → muse agent exists | PASS | `ls agents/muse.md` OK; rewrite.md L15 hands to `muse` |
| 4 | analyst `meaning:` field name vs Check D consumer | PASS | tier-coordinator.md L97 reads top-level `meaning:`; analyst.md L74 emits `meaning:` — same token |
| 5 | VENDOR row 116 `agents/prep-cordinator.md` on disk | PASS | file exists, NATIVE class matches |
| 6 | VENDOR row 117 `skills/prep/**` on disk | PASS | SKILL.md + resources/path-contract.md both present |
| 7 | VENDOR row 118 `skills/thematic-fidelity/**` on disk | PASS | SKILL.md present |
| 8 | Inventory line counts accurate | PASS | all 9 cited line counts (analyst 92, tier-coordinator 199, prep-cordinator 94, prep/SKILL 124, path-contract 84, thematic-fidelity 57, prep.md 16, rewrite.md 21, VENDOR 121) verified by `wc -l` |
| 9 | `Meaning-PRESERVED` / `Meaning-DIFF` token consistency | PASS | identical token pair in tier-coordinator.md (L106) and thematic-fidelity/SKILL.md (L31, L49) and all 3 exemplars |
| 10 | 3 exemplars carry DERIVED marker | PASS | all 3 files open with `<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->` per thematic-fidelity/SKILL.md L39-41 rule |
| 11 | analyst.md loads `laf-adaptation:thematic-fidelity`? | **FAIL — CRITICAL** | analyst.md L5-9 `skills:` lists only source-fidelity, adaptation-tiers, story-memory — but body L47/L74 invokes `/thematic-fidelity` and emits the `meaning:` field it defines. See Issue #1. |
| 12 | analyst boundary-contract claim consistency | **FAIL — IMPORTANT** | analyst.md L86-92 asserts meaning/compound_scene/compound_scenes are "NOT in `/source-fidelity`" because source-fidelity is ADOPTED-CLEAN — but VENDOR.md L115 + CLAUDE.md both classify `source-fidelity` as **NATIVE**, not ADOPTED-CLEAN. The justification for the additive block is internally contradictory. See Issue #2. |
| 13 | prep-cordinator `tools: Agent(...)` includes tier-coordinator | **FAIL — CRITICAL** | prep-cordinator.md L13 declares `Agent(web-researcher, analyst, tier-coordinator)` in `tools:`, but Stages 1–8 (L46-61) only ever dispatch `Agent(web-researcher)` (Stage 1c) and `Agent(analyst, …)` (Stage 3). `tier-coordinator` is NEVER dispatched anywhere in the prep body — it is a *rewrite-phase* agent (own body L20 "workflow step 10"; chronicler L20 "AFTER tier-coordinator"). Listing it as a prep tool is misleading and contradicts the prep/rewrite phase split in path-contract §5. See Issue #3. |
| 14 | `/thematic-fidelity` loaded only by prep-cordinator | **FAIL — IMPORTANT** | thematic-fidelity/SKILL.md L57 ("It is loaded by the (native) `prep-cordinator`") claims single load-source — verified true. BUT analyst.md L47/L74 and prep/SKILL.md §2.1 L49 / §4 L68 *invoke* `/thematic-fidelity` as if it were loadable from analyst's or prep's context. Since analyst does not load it (Issue #1) and prep does load it, only the prep path is valid; the analyst invocations are dangling. See Issue #4. |
| 15 | source-fidelity provenance classification | **FAIL — IMPORTANT** | CLAUDE.md "Present-state" para and §1 table classify `source-fidelity` as **NATIVE**; VENDOR.md L115 classifies `skills/source-fidelity/**` as **NATIVE**. analyst.md L66 + L83-92 repeatedly justify the additive meaning block on the grounds that `/source-fidelity` is "ADOPTED-CLEAN" and "cannot be extended per the boundary contract, constraint #6". The justification is wrong: a NATIVE skill *can* be edited directly, so the additive block's stated rationale is unfounded. See Issue #2 (root) / #5 (analyst prose). |
| 16 | Check D `/thematic-fidelity` load claim in tier-coordinator | **FAIL — MINOR** | tier-coordinator.md L178-181 says "no new skill line is required" because "Check D reads `meaning` as **data**". Consistent with its `skills:` (loads adaptation-tiers, source-fidelity, kb-management — NOT thematic-fidelity). The skill-name `/thematic-fidelity` only appears in a section heading (L95). Functionally OK, but the Check D heading cites `/thematic-fidelity` as if loaded — cosmetic inconsistency with the load list. See Issue #6. |
| 17 | `cordinator` vs `coordinator` spelling drift | **FAIL — MINOR** | agent file, command, and 5 internal references use the misspelling `prep-cordinator` (missing 'i'); the standard spelling `coordinator` is used everywhere else (`tier-coordinator`, UPSTREAM-SYNC, NOTICE, CLAUDE.md prose). Intentional-but-undocumented or drift — either way a cross-file inconsistency a downstream consumer will trip on. See Issue #7. |

## Summary
- Checks passed: 10 / 17
- Checks failed: 7
- Critical issues: 4 (#1, #2-root, #3, #5 — boundary-contract violations / unreachable-load / phase-split contradictions)
- Important issues: 2 (#4 dangling `/thematic-fidelity` invocation, #12-15 analyst provenance misclass)
- Minor issues: 2 (#6 cosmetic heading citation, #7 spelling drift)
- Issues fixed in-place: 0 (REPORT-ONLY — `fix_authorization: false`)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `laf-adaptation/agents/analyst.md` L5-9 (`skills:` frontmatter) vs L46-50, L74 (body) | analyst.md invokes `/thematic-fidelity` and emits the `meaning:` field that thematic-fidelity defines, but does NOT load `laf-adaptation:thematic-fidelity` in its `skills:` list. At runtime the analyst cannot resolve the `/thematic-fidelity` citation; the meaning field is emitted without its defining skill loaded. | Add `- laf-adaptation:thematic-fidelity` to analyst.md `skills:` (after the existing 3 entries). This is the additive-skill pattern the boundary contract intends. |
| 2 | CRITICAL | `laf-adaptation/agents/analyst.md` L66, L83-92 (justification prose) | The additive `meaning`/`compound_scene`/`compound_scenes` block is justified on the grounds that `/source-fidelity` is "ADOPTED-CLEAN" and therefore "cannot be extended per the boundary contract, constraint #6". But VENDOR.md L115 classifies `skills/source-fidelity/**` as **NATIVE**, and CLAUDE.md §1 table + "Present-state" para also classify `source-fidelity` as NATIVE. NATIVE skills *can* be edited directly — the stated rationale for keeping these fields in the agent body (rather than in the skill) is unfounded. Either the rationale is wrong, or the VENDOR/CLAUDE.md classification is wrong; both cannot be true. | Reconcile the provenance of `source-fidelity`. If NATIVE: edit source-fidelity/SKILL.md to define these fields directly and remove the additive block's "ADOPTED-CLEAN" justification. If actually ADOPTED-CLEAN: fix VENDOR.md L115 and CLAUDE.md to say so and pin its hashes. One side must change. |
| 3 | CRITICAL | `laf-adaptation/agents/prep-cordinator.md` L13 (`tools:`) vs L46-61 (8-stage body) | `tools:` declares `Agent(web-researcher, analyst, tier-coordinator)`, but tier-coordinator is never dispatched in any of Stages 1–8 (only web-researcher @ 1c and analyst @ Stage 3 are). `tier-coordinator` is a rewrite-phase agent (own body L20 "step 10"; path-contract §5 assigns it to the rewrite phase). Listing it as a prep tool is misleading and contradicts the prep/rewrite phase split. | Remove `tier-coordinator` from prep-cordinator.md `tools:` Agent(...) tuple, leaving `Agent(web-researcher, analyst)`. |
| 4 | IMPORTANT | `laf-adaptation/agents/analyst.md` L47, L74 | Body invokes `/thematic-fidelity` as if loadable, but (per Issue #1) it is not in the analyst's skill set. Combined with #1: dangling citation. | Resolved transitively by fixing #1. After fix, re-verify the citation resolves. |
| 5 | CRITICAL | `laf-adaptation/agents/analyst.md` L66, L83-92 ↔ `VENDOR.md` L115 ↔ `CLAUDE.md` §1 + "Present-state" | Root form of Issue #2: the source-fidelity provenance classification is asserted 3 different ways in 3 files (NATIVE in VENDOR/CLAUDE.md, ADOPTED-CLEAN-justification in analyst.md). The boundary-contract reasoning depends on which is true; right now the tree contradicts itself. | Same fix as #2: pick one classification, propagate to all 3 files. |
| 6 | MINOR | `laf-adaptation/agents/tier-coordinator.md` L95 (Check D heading) vs L5-9 (skills:) | Check D heading reads `### Check D — Meaning preservation (R10; /thematic-fidelity)` as if `/thematic-fidelity` were loaded; the skill is NOT in tier-coordinator's `skills:` (it loads adaptation-tiers, source-fidelity, kb-management only). L178-181 explicitly says no new skill line is required (reads `meaning` as data). Cosmetic — functionally consistent, but the heading cites an unloaded skill path. | Either drop `/thematic-fidelity` from the heading (keep "R10"), or add a one-line note clarifying the citation is conceptual not a load. |
| 7 | MINOR | `laf-adaptation/agents/prep-cordinator.md` (filename + L11, L19, L72, L73, L87, L93); `.claude/commands/laf/prep.md` L8, L11, L15 | Misspelling `prep-cordinator` (missing 'i') used as the canonical agent name across 2 files, while `coordinator` (correct) is used everywhere else (tier-coordinator, UPSTREAM-SYNC, NOTICE, CLAUDE.md prose). Either intentional-but-undocumented or silent drift; either way a cross-file inconsistency. | Rename to `prep-coordinator` everywhere (filename, frontmatter `name:`, command delegations) OR add a one-line provenance note documenting the misspelling as intentional. Renaming is strongly preferred for downstream-tool compatibility. |

## Confidence Gate Protocol

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 9 | Grep: 1 (multi-pattern, batched) | Glob: 0 | Bash: 4 (all multi-check batched enumerations)

- Web research not performed this phase: all verification targets are local-file cross-references; no external/standards-bound claim needed Tavily-first lookup. `tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0`.
- Every checklist item is VERIFIED with cited tool evidence (specific file paths + line numbers in the table above). No item was marked VERIFIED based on another report's claim.
- Tool engagement minimum met: 14 evidence-bearing tool calls across 17 checks (Read calls cover multiple checks each; Bash calls cover multiple enumeration checks each). All calls map to specific verification targets — no padding.

## Recommendations
Before this build can PASS an internal-consistency gate, ALL 7 issues must be resolved (zero-tolerance; no severity exempt):

1. **Issue #1 / #4 (CRITICAL):** add `laf-adaptation:thematic-fidelity` to analyst.md `skills:`.
2. **Issue #2 / #5 (CRITICAL):** reconcile `source-fidelity` provenance — pick NATIVE (per VENDOR.md/CLAUDE.md) or ADOPTED-CLEAN (per analyst.md justification) and propagate the choice across all 3 files. This is the load-bearing decision; everything else follows.
3. **Issue #3 (CRITICAL):** remove `tier-coordinator` from prep-cordinator.md `tools:` Agent(...) tuple.
4. **Issue #6 (MINOR):** clarify Check D heading citation.
5. **Issue #7 (MINOR):** standardize on `prep-coordinator` (preferred) or document the misspelling.

Issue #2/#5 is the hardest because it forces a design decision (where do `meaning` and `compound_scene` canonically live — in source-fidelity/SKILL.md or in analyst.md's additive block?). The current tree asserts both answers simultaneously, which is the defect.

## QA Complete
