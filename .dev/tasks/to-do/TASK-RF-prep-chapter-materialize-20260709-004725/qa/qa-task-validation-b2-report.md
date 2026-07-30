# QA Report — Task Integrity Check (B2 Self-Containment Lens)

**Topic:** /laf:prep Stage 0 chapter materialization (chapter-materialize skill + NATIVE prep-spine edits)
**Date:** 2026-07-09
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false

---

## Scope

B2 self-containment lens only (per spawn directive). This is the targeted B2 sub-lens: does every checklist item carry context + action + output + verification + completion gate, with specific/correct file anchors, embedded agent prompts, measurable verification, one-file-per-item granularity, and correct load-bearing directives?

## Verification performed (ground truth reads)

| Source file | Verified |
|---|---|
| `laf-adaptation/VENDOR.md` L116-126 | NATIVE rows use `M-bM-^@M-^T` = **U+2014 EM DASH** in both hash cells; `skills/prep/**` glob form confirmed (item 4.3 row shape matches byte-for-byte) |
| `laf-adaptation/agents/prep-cordinator.md` (98 lines) | skills block L5-11 (thematic-fidelity L11, tools L12); `## The 8 stages` fenced block L44-63 (STAGE 1..8, Q-GATE=STAGE 5, GREENLIGHT=STAGE 7); Stage notes L64; L20 "8-stage prep pipeline", L25 "execute its 8-section procedure" |
| `laf-adaptation/skills/prep/SKILL.md` (125 lines) | §1 ends L19 ("8 fixed-name files"), blank L20, `## §2` L21; `## Resources` L122, EOF L125 |
| `laf-adaptation/skills/prep/resources/path-contract.md` (91 lines) | `## 4.` L62, read-set fence L66-70, `## 5.` **L75**, `work/prep/<slug>/*` write-row **L79** |
| `.claude/commands/laf/prep.md` (20 lines) | canonical file (not symlink); argument-hint L3; `--source` body L18-20 |
| `laf-adaptation/source/README.md` (23 lines) | layout bullets L4-7, `## Provisioning contract` L9 |
| `laf-adaptation/scripts/check_boundary.py` (737 lines) | `classify()` default `return "NATIVE"` at **L368** (also L362, L367); `NATIVE_SKILLS` L46, `BUILD_NEW_SKILLS` L47 |

## B2 Self-Containment Checklist (the 7 lens sub-checks)

| # | B2 check | Result | Evidence |
|---|----------|--------|----------|
| B2.1 | Every item has all B2 components (context + action + output + verification + completion gate) | PASS | Every `- [ ]` item read (25 items across Phases 1-7). Each restates its inputs (reads the discovery artifact/research by absolute path), states a concrete action, names an output path, has a verification clause, and ends with the "log blocker … then mark this item complete / Once done, mark this item as complete" completion gate. No title-only or bare-context items found. |
| B2.2 | No item references prior-item context without restating it | PASS | Items do not say "see above" for data. Each Phase 2-6 item re-reads the concrete discovery artifact it needs (`skill-authoring-blueprint.md`, `boundary-facts.md`, `edit-loci-and-numbering.md`) by absolute path rather than assuming prior in-context state. Handoff-file convention documented in Execution Context (L146-160). |
| B2.3 | Agent-spawning items have FULLY EMBEDDED prompts (not "see SKILL.md") | PASS | Steps 6.2, 6.3 (six lens agents), 6.5, 6.6, 6.7, 6.8, 6.10, 6.11 all carry the full lens-specific adversarial prompt inline in quotes. Step 7.3 (POST reflect runner) embeds the ENTIRE verbatim runner prompt (L332-340) including the exact `Skill(...)` invocation string and the COMPLETION CONTRACT. No agent item defers its prompt to an external file. |
| B2.4 | File paths are specific (exact file + line/content anchor), not "the relevant file" | **PARTIAL** | Every item names absolute file paths. Line anchors are given AND paired with content anchors. HOWEVER two path-contract line anchors in Item 4.1 are off-by-one against ground truth (see Issue #1). Content anchors are correct and recoverable, which prevents this from being CRITICAL. |
| B2.5 | Verification criteria measurable (not "verify it works") | PASS | Verifications are concrete: Step 5.1 = "exit 0 AND stdout contains `BOUNDARY CONTRACT: PASS`"; Step 5.2 = explicit grep-asserts + `git diff` predicates; Step 2.3 = "`readlink … resolves to ../../laf-adaptation/skills/chapter-materialize`"; Step 2.1 = "failure table has exactly 16 rows", "frontmatter uses ONLY name + description". No vacuous "verify it works". |
| B2.6 | No batch items — each authored/edited file has its OWN item | PASS | SKILL.md=2.1, boundary-rules.yaml=2.2, symlink=2.3, prep-cordinator=3.1, prep/SKILL.md=3.2, command=3.3, path-contract=4.1, source/README=4.2, VENDOR=4.3. Nine files → nine dedicated items, one file per item. No item edits two authored files. |
| B2.7 | Load-bearing correctness directives present and correct | **PARTIAL** | VENDOR item 4.3: U+2014 + single `/**` row — CORRECT & VERIFIED. Symlink item 2.3: uses `ln -s`/`readlink`, forbids `diff -r` — CORRECT. check_boundary "ZERO edits" forbidden across items 4.3/5.2/Key Constraints — CORRECT. prep-cordinator Approach A (prepend STAGE 0, keep 1..8) — CORRECT. path-contract §1/§2/§4 read-set byte-unchanged — directive CORRECT but see Issue #2 (self-contradiction risk in 4.1 wording). One granularity concern on Item 2.1 (see Issue #3). |

## Load-bearing correctness detail (per spawn directive)

- **VENDOR U+2014 + single `/**` row:** VERIFIED. Item 4.3 specifies `| skills/chapter-materialize/** | NATIVE | — | — |` with "U+2014 (EM DASH) for BOTH hash cells to match the existing NATIVE rows byte-for-byte" and "do NOT add a separate row for boundary-rules.yaml". Ground truth: existing NATIVE rows in VENDOR.md L118-124 use `M-bM-^@M-^T` (U+2014) and the `/**` glob form. Directive is correct.
- **Symlink `ln -s`/`readlink` (NOT copy/`diff -r`):** VERIFIED. Item 2.3 runs `ln -s ../../laf-adaptation/skills/chapter-materialize .claude/skills/chapter-materialize`, verifies via `readlink`, and explicitly states "do NOT use `diff -r` … use `readlink`". Correct.
- **Forbids editing check_boundary.py:** VERIFIED. Stated in Key Constraints (L134), Item 4.3, and Item 5.2. classify() default `return "NATIVE"` confirmed at L368 (task says "line 367" — see Issue #4, minor).
- **prep-cordinator Approach-A (prepend STAGE 0, keep 1..8):** VERIFIED. Item 3.1(b) inserts STAGE 0 as FIRST entry "keeping every STAGE 1..8 line byte-identical"; Q-gate stays STAGE 5, greenlight stays STAGE 7. Ground truth fenced block (L44-63) confirms current Q-GATE=STAGE 5, GREENLIGHT=STAGE 7. Correct.
- **path-contract §1/§2/§4 read-set byte-unchanged:** Directive present and correct in Item 4.1 and Item 5.2 grep-assert. Byte-unchanged spans named. See Issue #2 for the anchor-arithmetic wording risk.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | Item 4.1(b), task L236 | Task says insert the 3 §5 write-ownership rows "immediately after the existing `work/prep/<slug>/*` row (**L80**)". Ground truth: the `work/prep/<slug>/*` row is at **L79**; L80 is the `kb/adaptation-mapping/<slug>-mapping.yaml` row. Following the literal line number (L80) would misplace the new rows after the kb-mapping row instead of after the `work/prep/<slug>/*` row. The CONTENT anchor ("after the existing `work/prep/<slug>/*` row") is correct, so an executor keying on content recovers — but the paired line number is wrong. | Change "(L80)" → "(L79)" in Item 4.1(b), OR drop the line number and rely on the content anchor `work/prep/<slug>/*` row. |
| 2 | MINOR | Item 4.1(a), task L236 | Task says append the new §4 paragraph "AFTER the end of the §4 body (after L73, BEFORE `## 5.` at **L76**)". Ground truth: `## 5. Write-ownership` is at **L75**, not L76. "after L73" is correct; the `## 5.` line reference is off-by-one. Content anchor (`## 5.`) recovers it. | Change "at L76" → "at L75" in Item 4.1(a). |
| 3 | MINOR | Item 1.5, task L196 | Task says "classify() default NATIVE at **line 367**; do NOT touch NATIVE_SKILLS/BUILD_NEW_SKILLS". Ground truth: the terminal `return "NATIVE"` default is at **L368** (L367 is the `return "NATIVE"` inside the BUILD_NEW branch; L362 is the earlier NATIVE return). The directive intent (do-not-edit) is correct and load-bearing; only the cited line number is slightly off. Since check_boundary.py must stay byte-unchanged, this anchor is informational and never acted on — lowest impact. | Change "at line 367" → "at line 368" (or drop the specific line, since the file is not to be edited). |
| 4 | MINOR (granularity) | Item 2.1, task L204 | Item 2.1 (author SKILL.md) is ~1 very long paragraph enumerating 13 ordered sections with deep sub-requirements (confidence rule verbatim, deferred-write invariant verbatim, 16-row table, full manifest schema, normalization rules). It is self-contained and correctly forbids one-shotting ("Author incrementally … DO NOT attempt to complete the entire file in a single write burst"), so it does NOT violate the one-file-per-item rule (B2.6) — SKILL.md is one file. But it far exceeds the ~15-line atomicity guideline and cannot be executed "without scrolling". This is a granularity tension, not a B2-self-containment failure: all B2 components are present. Flagged for awareness; the incremental-authoring instruction is the correct mitigation for a single large document artifact. | No change required for B2 pass. If desired, note in the item that the 13 sections may be authored as 13 sequential Edit appends (already implied). |

## Confidence Gate

Every B2 sub-check was verified with tool evidence (7 ground-truth source reads + 4 targeted line-pin greps). No sub-check is UNCHECKED or UNVERIFIABLE.

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 8 (each Bash call pinned a specific anchor claim: VENDOR em-dash bytes, prep-cordinator anchors, the 8-stages fenced block, prep SKILL structure, path-contract spans, command file, check_boundary classify(), and the two off-by-one line pins)

Tool-engagement note: 10 verification calls ≥ 7 B2 sub-checks — engagement floor satisfied.

## Summary

- B2 sub-checks passed: 5/7 fully PASS (B2.1, B2.2, B2.3, B2.5, B2.6)
- B2 sub-checks PARTIAL: 2/7 (B2.4 anchor precision, B2.7 one granularity note)
- Issues found: 4 (all MINOR)
- CRITICAL: 0 | IMPORTANT: 0 | MINOR: 4
- Load-bearing correctness directives (VENDOR U+2014 + single `/**`, symlink `ln -s`/`readlink`, no check_boundary edit, Approach-A STAGE 0, path-contract read-set byte-unchanged): ALL correct.

## Verdict Rationale

The B2 self-containment lens is fundamentally about whether an executor can act on each item WITHOUT external context. On that dimension the task file is strong: every item embeds its inputs, action, output path, measurable verification, and completion gate; every agent-spawning item embeds its full prompt (including the verbatim POST-reflect runner prompt); every authored/edited file has its own dedicated item; and all five load-bearing correctness directives called out in the spawn brief are present and correct against ground truth.

The four issues found are all MINOR line-anchor imprecisions (three off-by-one line numbers, one granularity note). Critically, EVERY imprecise line anchor is PAIRED with a correct content anchor (`## 5.`, the `work/prep/<slug>/*` row, the classify() do-not-edit intent), and the file targeted by the worst two (path-contract) is additionally guarded by the Step 5.2 byte-unchanged grep-assert and `git diff` predicate — so a misplaced insert would be caught by validation. None of the four rises to the "reference prior context without restating" or "vague path / vacuous verification" failures that would fail the B2 lens.

Because zero CRITICAL/IMPORTANT B2 failures exist, all load-bearing directives are correct, and the anchor defects are content-anchor-recoverable and validation-guarded, the B2 self-containment gate is a conditional PASS with 4 MINOR fixes recommended (fixing the two path-contract line numbers is the highest-value cleanup as it removes an off-by-one that could misplace an insert if an executor keys on the number over the content anchor).

---

## VERDICT: PASS (with 4 MINOR issues — 3 off-by-one line anchors + 1 granularity note; all content-anchor-recoverable, none CRITICAL/IMPORTANT)

## QA Complete

