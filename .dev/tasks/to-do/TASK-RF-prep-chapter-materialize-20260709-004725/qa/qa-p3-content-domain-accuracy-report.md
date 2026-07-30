# QA Report — Phase-3 Content (domain-accuracy lens)

**Topic:** /laf:prep Stage-0 chapter-materialize wiring
**Date:** 2026-07-09
**Phase:** doc-qualitative (adapted — phase-gate content, LENS: domain-accuracy)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Adversarial stance:** assumed ≥5 errors; grounded every wiring claim against LAF reality.

---

## Overall Verdict: FAIL

Two cross-reference/consistency defects introduced by the wiring edit. Both are in-scope
(they live in the three EDITED files) and both are verifiable against current LAF source.
The substantive mechanism claims (checks 1–6 of the spawn brief) are otherwise accurate.

---

## Items Reviewed

| # | Check (from spawn brief) | Result | Evidence |
|---|--------------------------|--------|----------|
| 1a | prep §5 question gate exists | PASS | `skills/prep/SKILL.md:83` `## §5 Question-gate coverage rule` |
| 1b | §6 greenlight exists | PASS | `skills/prep/SKILL.md:94` `## §6 Greenlight` |
| 1c | /source-fidelity Phase-0 + source-access declaration exist | PASS | `skills/source-fidelity/SKILL.md:21` `## Phase 0 — Source Declaration`; source-access declaration is that phase's content |
| 1d | 70-traceability [skip]→DEFAULTED exists | PASS | `skills/prep/SKILL.md:91` `[skip]` → DEFAULTED in `70-traceability.md`; path-contract §2 row 33 |
| 1e | path-contract §3 exists (promotion targets) | PASS | `path-contract.md:35` `## 3. Promotion targets` |
| 1f | path-contract §5 exists (write-ownership) | PASS (see #A) | `path-contract.md:75` `## 5. Write-ownership` — exists but does NOT list chapter/manifest paths |
| 1g | **path-contract §6 exists** | **FAIL** | path-contract has only §1–§5; **there is no §6** (headers: 1,2,3,4,5). Agent references a non-existent section. See Finding #A |
| 1h | No invented Stage-0 mechanism | PASS | `ambiguous_splits`, `needs_human_review`, `review.status PENDING/CONFIRMED`, `.raw/` all defined in `skills/chapter-materialize/SKILL.md` (grep hits: 5/7/4) |
| 2 | "no new gate or HALT machinery" is TRUE; reuses §5/§6 (matches spec §10) | PASS | agent 99–101 + SKILL 26 match spec §10 (`merged-requirements.md:223-232`); greenlight gains one checklist line only (agent 110–114 = spec §10). No runtime/script added — git diff shows only 3 `.md` edits (ADR-006 honored) |
| 3 | Frontmatter dialect valid; skills line is `laf-adaptation:<skill>`; no Mars keys | PASS | frontmatter keys = name/description/model/skills/tools; `- laf-adaptation:chapter-materialize` correct form; Mars-key grep = NONE; `model: opus` ∈ valid set |
| 4 | chapter-materialize dispatched inline as a skill, NOT an Agent type; tools line unchanged | PASS | `tools:` line still `Agent(web-researcher, analyst, tier-coordinator)` — unchanged; chapter-materialize added ONLY to `skills:` frontmatter. Consistent with how the coordinator's other skills load |
| 5 | Command delegates whole run to prep-cordinator (opus); no pipeline duplication | PASS (see #B) | `prep.md:8` "Delegate the entire run to the `prep-cordinator` agent (opus)"; `prep.md:11-13` "Do not restate the pipeline here". BUT stale "8-stage" claim — Finding #B |
| 6 | No claim contradicts CLAUDE.md / path-contract / spec non-goals (no new command; --source-mode is a flag) | PASS | `--source-mode` added as a flag on `/laf:prep` (argument-hint + body); no new command. Matches spec N2 (`merged-requirements.md:43`) and §3/§5. No `/laf:ingest` |

---

## Summary

- Checks passed: 11 / 13
- Checks failed: 2 (Finding #A dangling path-contract §5/§6 reference; Finding #B stale "8-stage" in command)
- CRITICAL: 0
- IMPORTANT: 2
- MINOR: 0
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 8 (via Bash) | Glob: 0 | Bash: 8

Every checklist item was verified against actual source (three edited files + path-contract,
source-fidelity, chapter-materialize skills, and the driving spec `merged-requirements.md`).
No item is Unverifiable or Unchecked.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| A | IMPORTANT | `laf-adaptation/agents/prep-cordinator.md:82` | Dangling / inaccurate cross-reference. The Stage-0 note states "Chapter paths and the manifest path are owned by **path-contract §5/§6**; never restate them here." But `path-contract.md` has only §1–§5 — **§6 does not exist**, and current §5 (Write-ownership) does **not** list `source/<slug>/ch-<NN>.txt`, `chapter-manifest.yaml`, or `.raw/*`. The spec (§11/§12) *planned* to add these §5 rows and a new §6 to path-contract, but path-contract.md was NOT edited in this task (git diff touches only the 3 wiring files). The agent therefore defers path-ownership authority to a section that does not exist and to a §5 table that lacks the rows — an ownership gap for the very paths Stage 0 writes. (AX-1 drift / AX-2 contradiction against current path-contract.) | Either (a) update `path-contract.md` §5 to add the three `source/<slug>/…` write-ownership rows and add the new §6 "Source-side chapter manifest" subsection (per spec §12), then keep the agent's `§5/§6` pointer; OR (b) if path-contract is out of this task's edit set, change the agent line to reference only the `chapter-materialize` SKILL's Manifest-output-contract as the path authority and drop the false `path-contract §5/§6` citation. Do not leave a pointer to a non-existent section. |
| B | IMPORTANT | `.claude/commands/laf/prep.md:11` | Stale stage count. The command body still says the coordinator "owns the **8-stage** procedure," but the same task re-labeled the agent as a **9-stage** pipeline (`prep-cordinator.md:21` "9-stage prep pipeline (STAGE 0 + the 8 below)", `:46` "## The 9 stages"). The command file WAS edited in this task (argument-hint + a body paragraph added) yet the "8-stage" claim in its own body was not updated — an incomplete edit leaving the command contradicting the agent it delegates to. A reader of the command is told 8 stages; the agent says 9. (AX-2 contradiction — two edited artifacts disagree on the same subject; IMPORTANT per Critical Rule #6.) | Update `prep.md:11` to "owns the 9-stage procedure (STAGE 0 materialize + the 8 prep stages)" — or phrase it as "the STAGE-0-prepended prep pipeline" — so the command's stage count matches the agent's post-edit self-description. |

### Note on stage-numbering vs the spec (NOT a finding)

The driving spec `merged-requirements.md:86-95` presents a **7-stage** conceptual grouping
(STAGE 0–6, collapsing the SKILL's §-sections). The agent instead prepends STAGE 0 onto its
own pre-existing 8-stage numbering → **9 stages** (STAGE 0 + STAGE 1–8). These are two
different numbering schemes, not a contradiction the wiring introduced: the agent's STAGE 1–8
numbering pre-dates this task (the pre-edit body already said "8-stage pipeline" / "STAGE 8
HANDOFF"). The agent's numbering is internally consistent and correctly labels STAGE 0 as the
prepend. No action required — flagged only so the reader knows the spec/agent numbering
divergence was examined and is benign. (The command inconsistency in Finding #B is a genuine
defect because it disagrees with the *agent's own* chosen scheme.)

## Out-of-scope observations (documented, NOT counted against verdict; not fixed)

- `[OUT-OF-SCOPE]` **VENDOR.md missing Rule-F row for `chapter-materialize/SKILL.md`.**
  Spec §11 requires "+1 NATIVE row for `chapter-materialize/SKILL.md` (Rule F)". `grep
  chapter-materialize VENDOR.md` returns nothing. This would fail `check_boundary.py` Rule F
  (every `skills/**/SKILL.md` must be manifested). This concerns `VENDOR.md` and the
  `chapter-materialize` skill file — neither is in the assigned EDITED FILES set (wiring only),
  so it is not this review's to fix. Flagged for the orchestrator: it is a real release-blocker
  (spec AC6) that a separate structural/boundary QA pass must own.

## Actions Taken

None. `fix_authorization: false` — report-only. Both findings documented with exact location
and required fix above.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was present in the spawn prompt; this review ran
  in standalone mode. No structural PASS items were relied upon — every claim was independently
  verified with own tool engagement.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verified path-contract has only §1–§5 (`grep -E '^## [0-9]'` → headers 1,2,3,4,5) and that
  §5 write-ownership does NOT list chapter/manifest paths — exposing the agent's `§5/§6`
  reference as dangling (Finding #A). Tool evidence: Bash grep on `path-contract.md` +
  Read of §5 table lines 75–91.
- Verified stage-count divergence by grepping `8-stage|9-stage` across all three edited files,
  surfacing the command's stale "8-stage" against the agent's "9 stages" (Finding #B). Tool
  evidence: Bash grep hits on `prep.md:11`, `prep-cordinator.md:21/26/27/46`.
- Confirmed the `tools:` Agent list is byte-unchanged and chapter-materialize entered only via
  `skills:` frontmatter (check 4) — Read of frontmatter lines 1–16 + Bash `grep Agent(`.

**Self-Audit questions:**
1. Factual claims independently verified against source: 13/13 checklist items, each mapped to a
   specific Read or grep.
2. Files read to verify claims: `prep-cordinator.md`, `prep/SKILL.md`, `.claude/commands/laf/prep.md`,
   `path-contract.md`, `source-fidelity/SKILL.md`, `chapter-materialize/SKILL.md`, `laf-adaptation/CLAUDE.md`,
   and the driving spec `merged-requirements.md`; git diff of the 3 edited files.
3. Why trust the finding count: two defects are shown with exact file:line and reproduced via grep
   output in this report (path-contract has no §6; command says 8-stage while agent says 9). The
   adversarial pass did not stop at the first defect — it verified all 6 brief checks and the
   frontmatter dialect before concluding.
4. Web research performed: none required (all verification was local-file-bound). Tavily not invoked.

## Recommendations

- Resolve Finding #A: fix the agent's `path-contract §5/§6` citation (either edit path-contract to
  add the §5 rows + §6 subsection per spec §12, or repoint the agent to the chapter-materialize
  manifest contract as path authority). A dangling authority pointer for the paths Stage 0 writes
  is not acceptable.
- Resolve Finding #B: update the command's "8-stage" to match the agent's 9-stage self-description.
- Orchestrator: route the out-of-scope VENDOR.md Rule-F gap (chapter-materialize SKILL.md not
  manifested) to the structural/boundary QA owner — it is a spec-AC6 release-blocker.

## QA Complete
