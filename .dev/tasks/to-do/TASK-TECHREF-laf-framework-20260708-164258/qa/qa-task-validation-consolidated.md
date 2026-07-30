# Consolidated Task-File Validation Findings — TASK-TECHREF-laf-framework

Sources: A.10 b2-self-containment (FAIL, fixable), A.10 phase-structure (timed out — checks independently verified by orchestrator via bash: 7 phases, correct P1→P7 ordering, `reflect_post_mode: skill` with no `start_commit`/`executor_model_class`, anti-orphaning completion items in Phase 7, 53 items), A.10.25 task-research-alignment (PASS + 1 IMPORTANT).

## Fixes to apply (single serialized fix pass)

### IMPORTANT
1. **Step 3.5 (gap-fill FAIL branch) — inline the prompt.** The conditional gap-fill research agent prompt is given by reference ("the same Codebase Research Agent Prompt structure used in Phase 2"). A cold-resuming executor must scroll back to Steps 2.1–2.6. FIX: embed the full Codebase Research Agent Prompt inline in Step 3.5 (the `# Research:` header block + Incremental File Writing Protocol + Documentation Staleness Protocol + evidence discipline), exactly as Steps 2.1–2.6 do, parameterized for "fill the specific gap identified by the Phase 3 gate."

2. **Steps 4.1, 5.1, 5.2, 5.3, 5.4, 5.5 — fix blocker-log routing.** These Phase 4/Phase 5 items route their on-blocker findings log to "### Phase 2 - Deep Investigation Findings". FIX: route each to its own phase's findings subsection — Step 4.1 → "### Phase 4 - Web Research Findings"; Steps 5.1–5.5 → "### Phase 5 - Synthesis Findings". If those subsections do not exist in the Task Log, add them.

3. **Overflow-flag mis-phased (alignment Finding B) — move to Phase 6.** research-notes AMBIGUITY #1 requires **Phase 6** to flag a ~1200-line Standard-tier overflow and recommend either Heavyweight-upgrade or splitting the boundary-contract subsystem into its own reference. Currently the only overflow flag is Phase 7 Step 7.2 (final summary), past the Gate-3 fix cycles where it would be actionable. FIX: add an explicit overflow-check to Phase 6 (in the assembler item 6.1 or the lens-QA completeness check 6.2/6.3) — "if the assembled doc exceeds ~1200 lines, record an overflow finding recommending Heavyweight-upgrade or a boundary-contract split, do NOT silently truncate." Keep the Phase 7 summary mention.

### MINOR
4. **Steps 7.2, 7.3, 7.5 — blocker-log routing** to "### Phase 1 - Preparation Findings" (misplaced). FIX: route to "### Phase 7 - Completion Findings" (add the subsection if absent). Low priority.
5. **Step 2.6** uses `docs/guides/*` glob — optionally name the two specific RN guides (`docs/guides/CHOOSING_A_TIER.md`, `docs/guides/lion-witch-wardrobe/ADAPTATION_GUIDE.md`). Coverage already preserved; cosmetic.
6. **web-01-skipped.md** filename is an authorized execution artifact, grounded — no fix.

## Not fixed (verified correct, no action)
- 53 items ↔ 53 checkboxes 1:1, no batch items.
- 40/41 agent prompts fully inlined.
- All 5 B2 components present in every item.
- Absolute paths throughout; template exists at /config/.claude/templates/documents/technical_reference_template.md.
- Count-drift discipline correct (stale 15/16 only ever a Tech-Debt §14 target; actions use verified 16/18).
- N/A §6/§7 + §11-minimal correctly propagated.
- Staleness item quarantined as [CODE-CONTRADICTED] Tech-Debt, not a defect, not a C8 item.
- Cycle-control "repeat Steps X–Y" acceptable (referenced items self-contained).
