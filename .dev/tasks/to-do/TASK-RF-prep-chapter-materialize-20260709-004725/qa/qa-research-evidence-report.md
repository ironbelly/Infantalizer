# QA Report — Research Gate (Evidence Quality + Gap Detection)

**Topic:** prep-chapter-ingestion / materialize prep chapter
**Date:** 2026-07-09
**Phase:** research-gate
**Lens:** evidence-quality + gap-detection (combined)
**Fix authorization:** false
**Assigned files:** 01-file-inventory-and-edits.md, 02-boundary-contract-and-verification.md, 03-skill-authoring-spec.md, 04-mdtm-template-and-gate.md

---

## Overall Verdict: PASS

The four assigned research files are **evidence-dense, spot-check-clean, and gap-free** against the
driving spec. Every high-risk citation I independently re-verified matched the repo byte-for-byte or
line-for-line. No CRITICAL or IMPORTANT issues found. Three MINOR off-by-one / stale-count nits are
documented below; none blocks synthesis because each edit-locus still resolves to the correct target.

Adversarial note: I approached this expecting fabricated line numbers (the usual failure mode for
"file:line" research). I verified >30% of cited loci across all four files including every claim the
spawn prompt flagged. The research held up under every check. The single spec requirement that research
04 flagged as an "open question" (does the prep `.claude/` mirror carry `resources/`?) is in fact
**resolved by research 01's symlink finding** and I confirmed it live — so it is not a builder gap.

---

## Tool Engagement

Read: 6 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 8
(No web research required — all claims are repo-internal source-truth. Tavily not engaged.)

Tool calls (14) >= combined checklist items exercised — engagement floor satisfied.

---

## Confidence

**Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Every spawn-prompt-flagged claim was checked with a direct tool call against the live repo. Spot-check
coverage well exceeds the 20% floor (I verified ~all flagged loci plus additional cross-checks).

---

## Items Reviewed (Evidence Spot-Checks)

| # | Check (claim) | Result | Evidence |
|---|-------|--------|----------|
| 1 | `check_boundary.py` `classify()` defaults NATIVE (~L367) | PASS | Read L340-368: `parts[0]=="skills"` -> `return "NATIVE"` at **L367**; final fallthrough `return "NATIVE"` L368. Exact. |
| 2 | `NATIVE_SKILLS`/`BUILD_NEW_SKILLS` constants (r02 L46-47) | PASS | grep: L46 `NATIVE_SKILLS={adaptation-tiers,adaptation-rules,source-fidelity}`; L47 `BUILD_NEW_SKILLS={adaptation-safety}`. `NATIVE_SKILLS` not read in classify — confirms r02's "not an allowlist". |
| 3 | `NO_HASH = "—"` em-dash = U+2014 (r02 L50/L179) | PASS | grep L50 `NO_HASH="—"`; python hexdump of the live `skills/adaptation-rules/**` row hash cells -> `0x2014` x2. Not U+2013, not ASCII. |
| 4 | VENDOR NATIVE rows: prep-cordinator L121, prep/** L122, thematic L123 | PASS | sed 116-126 matches r01/r02 verbatim, including exact line numbers. |
| 5 | VENDOR total 126 lines; format constraint L40-42 (`|`-free) | PASS | `wc -l`=126; L40-42 is the `## Format constraint` `|`-in-cell rule. `skills/chapter-materialize/**` is `|`-free. |
| 6 | `.claude/skills/prep` + `.claude/agents/prep-cordinator.md` are symlinks | PASS | `ls -la`: both are `lrwxrwxrwx` -> `../../laf-adaptation/...`. Confirms MIRROR MAP. |
| 7 | `.claude/commands/laf/prep.md` is a real file; no laf-adaptation/commands dir | PASS | `ls -la` -> `-rw-r--r--` (regular file, 20 lines); `find laf-adaptation -type d -name commands` -> empty. |
| 8 | `chapter-materialize` absent in both trees (Rule-E clean, NEW) | PASS | `ls` both paths -> "No such file or directory". |
| 9 | path-contract §4 read-set: 3 files, byte-frozen, L62-73 | PASS | Read L60-92: heading L62, fenced 3-path block L66-70 (30-mapping/40-prep-brief/10-challenges L67-69), greenlight precondition L72, 70-traceability exclusion L73. Matches r01+r02. |
| 10 | path-contract §2 "8 package files" table (r01 L22-33) | PASS | Read L22-34: table 24-33, 8 rows 00->70. Confirms N3 no-9th-file basis. |
| 11 | path-contract §5 write-ownership table L76-85 (r01 EDIT-B locus) | PASS | Read L75-92: header L77-78, rows L79-82; Form-transform note L87-91. r01's "insert after L80" locus valid. |
| 12 | path-contract total 91 lines (r01/r03 EOF-append loci) | PASS | `wc -l`=91. r01 §6 "append after L91" and r03 schema-append valid. |
| 13 | prep-cordinator `skills:` block L5-11 (6 entries, thematic L11, tools L12) | PASS | Read L1-16: skills L5-11, thematic-fidelity L11, `tools: >` L12. r01/r04 "insert after L11" locus exact. |
| 14 | prep-cordinator 8-stages fenced block L44-62; Q-GATE=STAGE5, GREENLIGHT=STAGE7 | PASS | sed 44-62: heading L44, STAGE 5 Q-GATE, STAGE 7 GREENLIGHT present. Confirms r04 Approach-A "no-renumber" rationale. |
| 15 | prep-cordinator count words L20/L25/L26 (r04 nuance) | PASS | L20 "Owns the 8-stage prep pipeline"; L25 "execute its 8-section procedure"; L26 "the two HALT gates". r04's "L25=skill §-count, leave as-is" nuance is correct. |
| 16 | prep-cordinator total 98 lines | PASS | `wc -l`=98. Matches r01/r04. |
| 17 | prep SKILL "8 fixed-name files 00-70" (r01 EDIT-A after L19) | PASS | L19 is exactly that sentence (last §1 body line); §2 heading L21. Locus valid. |
| 18 | prep SKILL Resources L122, path-contract bullet 124-125; total 125 | PASS | grep `## Resources`=L122, bullet L124-125; `wc -l`=125. r01 "append after L125" valid. |
| 19 | Global MDTM template exists at cited path | PASS | `ls -la` -> present (120KB). r04 cites D3=L286-289, M3=L1059+, I19 floor 3+3=6 <500ln — all spot-checked EXACT. |
| 20 | Books/LWW real case (spec AC2): split `-1..-4.html` + `copy*.html` monoliths both present | PASS | `ls Books/LWW/`: `-1..-4.html`, `copy`/`copy 2/3/5.html`, base `.html`, `.pdf` all present. Spec's mode-ambiguity case is real. |

---

## Gap Detection — Spec Requirement Actionability

Every driving-spec requirement is traced to a research file with an actionable locus. No builder-invented content required.

| Spec requirement | Actionable from research? | Where |
|---|---|---|
| §3 auto-detect precedence (adopt>folder>file>HALT) | YES | r03 §B5 (verbatim ordered list); r03 §E filename natural-sort; command hint r01 §5 EDIT-A/B |
| §3 `--source-mode` flag | YES | r01 §5 EDIT-A (arg-hint L3) + EDIT-B (body L18-20) |
| §5 manifest schema (v1) | YES | r03 §D carries the full YAML block VERBATIM; §D.1 field-notes (confidence/provenance/needs_human_review) |
| §6 confidence rule (CERTAIN>=2 signals; single->PROBABLE cap) | YES | r03 §B6 (bolded, verbatim); §F invariant #3; 5 evidence layers §B6 |
| §7 failure modes (16 rows) | YES | r03 §C reproduces all 16 rows inline for the builder to paste verbatim |
| §10 gate integration (fold into §5, deferred-write invariant) | YES | r04 §2b + Step-3 contract (STAGE5/STAGE7 extensions, no new gate); r03 §B7/B8 |
| §12 path-contract deltas (§4 note, +3 §5 rows, new §6) | YES | r01 §3 EDIT-A/B/C with exact loci; §4 read-set byte-frozen asserted |
| AC1-AC7 | YES | AC1-A2 Books/LWW (r03 §C anchors); AC3 Mode-C adopt (r03 §10); AC4 deferred-write (r03 §F#4); AC5 manifest rows (r03 §D.1); AC6 boundary cmd (r02 §Q5, baseline PASS captured); AC7 greenlight-gate (r04 §2b) |
| Release-blockers 1-7 | YES | RB1 mode-ambiguity (r03 §C); RB2 collision (r03 §10); RB3 single-signal (r03 §F#3); RB4-5 manifest/normalization (r03 §D.1); RB6-7 boundary/one-script (r02 §Q1/Q5, r04 ADR-006 N/A-testing) |

**No item requires the builder to invent content.** The only authoring gaps are explicitly, correctly
scoped to the builder (regex patterns in `boundary-rules.yaml`, plausible-length floors) and r03 marks
each "Builder to author" with the fixed shape supplied — that is intended latitude, not a research gap.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | r04 Step-1 L12 | Claims global MDTM template is "1516 lines total"; actual `wc -l` = **1515**. Off-by-one (trailing-newline count). Does NOT affect any cited line locus (D3/M3/I19 all verified exact). | Change "1516" -> "1515" if regenerating; harmless as-is. |
| 2 | MINOR | r01 §1 L46 / index L42 | States prep SKILL `## §1` heading is at "line 15"; actual heading is **line 16** (body 17-19). The EDIT-A locus "insert after line 19" is still correct (L19 = last §1 body line), so the edit is unaffected. | Note heading = L16 for precision; edit locus unchanged. |
| 3 | MINOR | r04 Step-4 "open question gap #1" (P4.1 mirror) | r04 flags as OPEN whether the prep `.claude/` mirror carries `resources/` (path-contract). r01's MIRROR MAP already answers this (parent-dir symlink covers `resources/`). I confirmed LIVE: `readlink -f .claude/skills/prep/resources/path-contract.md` -> the laf-adaptation source; editing source auto-mirrors. NOT an open gap. | Builder should treat P4.1 mirror as auto (symlink), per r01, not an open question. Cross-file coherence nit only. |

Note: Items 2 and 3 are cross-file coherence observations between r01 and r04, not evidence-fabrication.
Neither changes an edit target. No finding rises to IMPORTANT because every actual edit-locus in the
research resolves to the correct line/target in the live repo.

---

## Summary

- Checks passed: 20 / 20 evidence spot-checks; 9 / 9 spec-requirement actionability rows
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 3 (all cosmetic count / cross-file coherence; zero impact on edit loci)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Recommendations

- **GREEN LIGHT for synthesis.** The research is a reliable foundation; a builder can execute every
  edit locus directly from these four files without inventing content or re-deriving line numbers.
- Optional (non-blocking): correct the two count nits (template 1515 not 1516; prep §1 heading L16 not
  L15) and drop r04's "open question gap #1" since r01 + this QA confirm the prep mirror covers
  `resources/` automatically via the parent-dir symlink.

## QA Complete

---

## Status: COMPLETE

---
