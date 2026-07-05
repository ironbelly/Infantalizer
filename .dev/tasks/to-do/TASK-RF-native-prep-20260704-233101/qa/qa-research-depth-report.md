# QA Report — research-depth lens

**Phase:** research-depth
**Track goal:** implement the LAF adaptation-prep phase from docs/native-prep/design/DESIGN.md
**Fix authorization:** false
**Date:** 2026-07-04

---

## Assigned Files
- 01-file-inventory.md
- 02-patterns-conventions.md
- 03-boundary-integration.md
- 04-template-and-examples.md
- 05-design-pack-crossvalidation.md
- 06-verification-and-proof-flow.md

## Lens Focus
Is the research DEEP enough to produce a high-quality, granular task file WITHOUT re-reading source?

---

## Tool engagement
- Read: 9 (DESIGN.md; all 6 research files; analyst.md; check_boundary.py slice; prep-agent-schemas.md slice)
- Bash/Grep: 3 (BUILD_NEW sets + VENDOR rows; tier-coordinator anchors; P3/template/absent-dir probes)
- Independent source verifications performed: 24+ discrete claims re-checked against live code (not relied on from research text)

## Depth checklist verdicts (6 lens questions)

### Q1 — Does the research explain HOW the boundary check behaves (classify / --init / Mode-V rule flow), not just WHAT the files are? → **PASS (deep)**
Research 03 is a behavioral trace, not a file listing. It walks `classify()` control flow branch-by-branch (03 Q1), the `do_init` row-shape else-branch, the `--init` hard-require-`--upstream` early return, and a per-rule Mode-V table (A/A′/C′/B/C/D/E/F/F′) stating which rules run and their exact effect on the 3 new rows.
**Independently verified against source:** `classify()` at check_boundary.py:326-345 matches the trace exactly (agents branch 336-339, skills branch 340-344, NATIVE fallthrough 345). `BUILD_NEW_AGENTS={chronicler.md,tier-coordinator.md}` (line 45) and `BUILD_NEW_SKILLS={adaptation-safety}` (line 47) confirmed verbatim — so `prep-cordinator.md`/`prep`/`thematic-fidelity` → NATIVE is proven, not asserted. `do_init` else-branch glob row `rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))` at 405-407 confirmed. `--init requires --upstream` early return at 350-354 confirmed. This is genuinely deep — a builder can write the boundary gate item and predict its exact PASS output without re-reading the script.

### Q2 — Are the analyst.md / tier-coordinator.md edits specified with enough behavioral detail (what to SAY and WHERE) to write a self-contained edit item? → **PASS (deep)**
Research 01 §Category-2 gives per-change anchor headings + exact insertion line spans (E1a after line 21; E1b at line 51 schema; E1c after Phase-0 block line 39; E2a after Check-C block line 93; E2b after line 148; E2c lines 153-155). **The verbatim edit *content* lives in the design pack** (`prep-agent-schemas.md §3-4`), which I independently opened: lines 117-121 carry the exact `granularity`/`out_path` bullets; 130-143 the exact `meaning:`/`compound_scene`/`compound_scenes` YAML diff; 155-160 the exact "Meaning & compound-scene passes" paragraph; 178-194 the Check-D markdown + `preserves_meaning()` pseudocode; 204 the `- D meaning-preserved:` report line. **All anchors verified live:** analyst.md line 18/33/51 and tier-coordinator.md line 59/70/82/145-148/150/153-155 match byte-for-byte. A builder CAN write self-contained B2 edit items — the "what to say" is copy-followable from the design pack and the "where" is a verified anchor. The research correctly points the builder at the design pack for the diff body rather than re-transcribing it (appropriate; the design pack IS the buildable source of truth per DESIGN.md §8).

### Q3 — Are the MDTM QA-encoding rules (M3/M4/I19/I20/I21) captured with enough specificity to encode compliant PER_PHASE gates? → **PASS (deep)**
Research 04 §8 quotes M3 (8-step sequence, per-report-path), M4 (6-step fidelity, runs-after-M3), I19 (size-scaled 6/8/10/12 floors + named lenses + adversarial framing N), I20 (5-step serialized fix protocol, parallel-fix PROHIBITED), I21 (fidelity-gate mandatory triggers), I22 (lite/standard/full intensity maps), plus I15/I16 (gate floors + fix-cycle caps). §9 shows the prior example task's *actual* per-agent gate expansion (PGn.1 L6-aggregate → PGn.2 structural parallel → PGn.3 content parallel → PGn.4 consolidate+one-fix → PGn.5 verify) and its `check_boundary.py` L3 fix-loop gate items (max-3-cycles→HALT). This is enough to encode compliant PER_PHASE gates verbatim.

### Q4 — Is the design→code fidelity check thorough (real verdicts with evidence, not a rubber stamp)? → **PASS (deep)**
Research 05 is a claim-by-claim cross-validation table (sections A–I) with a `file:line` for every verdict. It is NOT a rubber stamp: it carries one honest **[UNVERIFIED]** (Rule E upstream-collision arm — uncheckable without a `--upstream` CWS checkout, correctly labeled non-blocking for Mode V) among the [CODE-VERIFIED] rows. I spot-re-verified the load-bearing rows independently: VENDOR rows 60/64/65/111/113/117 match verbatim; classify()/do_init line refs match; analyst.md + tier-coordinator.md anchor lines match. A rubber stamp would have marked Rule E verified too — the presence of a scoped [UNVERIFIED] with the correct non-blocking rationale is the signature of a genuine adversarial pass.

### Q5 — Could a builder create one granular item per file (9 new + 2 edits + VENDOR + doc) + per-phase verification items from this research alone? → **PASS (deep)**
Research 01 enumerates all 9 NEW files (N1-N9) with absence-confirmed status + provenance + VENDOR-row consequence, both EDIT targets (E1/E2) with anchors, and the 3 UNCHANGED must-not-touch files (U1-U3) with hash-pin proof. Research 02 gives per-file-type authoring dialect (agent 5-key frontmatter, skill 2-key, command frontmatter, the byte-exact DERIVED exemplar line-1 marker, mapping underscore/hyphen split). VENDOR delta (3 hand-added rows) and the doc pointer (R14) are both specified. **Independently confirmed absent:** `.claude/commands/laf/` (dir missing), `skills/adaptation-rules/resources/exemplars/` (only agency/character/thematic.md present), no narnia. A builder has one-item-per-file granularity source material for every artifact.

### Q6 — Is the P3 proof path concrete (which source, which commands, expected outputs)? → **PASS (deep), with a surfaced design↔shipped mismatch**
Research 06 actually **executed** every gate command and pasted verbatim exit-0 output: Mode-V boundary (`BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.`), `--report` (NATIVE=5/TOTAL=64 delta baseline), `git diff --stat` empty-pass for writer/muse, and the pyyaml 5-key check returning the exact key list. It surfaces two adversarial findings a shallow pass would miss: (1) the boundary final line has a suffix so gates must assert on the **prefix** `BOUNDARY CONTRACT: PASS`, not the full string; (2) **P3 as written names Narnia but the repo ships NO Narnia source and NO narnia mapping** — P3 is runnable today only on the Tolkien synthetic fixture. **I independently confirmed:** `find laf-adaptation -iname '*narnia*'` returns nothing; `source/` holds only `tolkien/ch-01.txt`; `kb/adaptation-mapping/` holds only `tolkien-mapping.yaml`. The Narnia/Tolkien mismatch is REAL and correctly flagged for the task author to resolve. This is exactly the kind of concrete, run-it-and-see depth the lens demands.

## Minor discrepancies (non-blocking, do not affect any checklist item)
- Research 04 states the MDTM template is "1516 lines"; actual `wc -l` = 1515. Off-by-one (likely trailing-newline counting); no rule ID or line-cited quote is affected.
- Research 06's P3 note is a design↔code mismatch (Narnia vs Tolkien) that is correctly *surfaced for the task author*, not a research defect — the research's job was to flag it, which it did.

## Self-Audit
1. **Claims independently verified against source (not relied on from research text):** 24+. Notably: `classify()` full branch flow (check_boundary.py:326-345), `BUILD_NEW_AGENTS`/`BUILD_NEW_SKILLS`/`NATIVE_*` sets (lines 44-47), `do_init` glob-row else-branch (405-407), `--init` upstream early-return (350-354), VENDOR rows 60/64/65/111/113/117, analyst.md anchors (18/33/51 + full body), tier-coordinator anchors (59/70/82/145-150/153-155), prep-agent-schemas.md §3-4 verbatim diff content (117-121/130-143/155-160/178-194/204), Narnia absence, source fixture, kb/root mapping inventory, template existence, absent command+exemplar dirs.
2. **Files I read to verify claims:** docs/native-prep/design/DESIGN.md; the 6 research files; laf-adaptation/agents/analyst.md; laf-adaptation/agents/tier-coordinator.md (via sed); laf-adaptation/scripts/check_boundary.py (326-410 + sets); laf-adaptation/VENDOR.md (rows); docs/native-prep/design/prep-agent-schemas.md (104-218); laf-adaptation/CLAUDE.md (context). Plus filesystem probes of source/, kb/, config/templates/, .claude/commands/, exemplars/, and the MDTM template.
3. **Why trust this review found real depth:** I did not accept the research's self-reported [CODE-VERIFIED] tags. I re-opened check_boundary.py and confirmed the line numbers and set contents the boundary trace depends on; I re-opened the design pack and confirmed the verbatim edit diffs a "self-contained edit item" would copy; and I re-ran the P3 filesystem probes that surface the Narnia mismatch. Every depth verdict above cites an independent check, not a restatement of the research.
4. **Web research:** none required — this is a fully local-file-bound depth review. Tavily not engaged; no fallback occurred.

## Confidence
Verified: 6/6 depth-lens questions | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
(Every depth verdict is backed by an independent source re-check, enumerated in Self-Audit #1.)

## Advisory notes (MINOR — do not block the depth gate; forward to task author)
| # | Severity | Location | Note | Suggested handling |
|---|----------|----------|------|--------------------|
| A1 | MINOR | research 04 §1 | Template stated as "1516 lines"; actual = 1515. Off-by-one; no cited rule/quote affected. | Optional: correct to 1515. Non-load-bearing. |
| A2 | MINOR (design↔code, not a research defect) | research 06 P3 section | P3 gate in DESIGN.md §7 names Narnia, but repo ships NO Narnia source and NO narnia kb-mapping (independently confirmed: `find … -iname '*narnia*'` empty). Research CORRECTLY surfaced this. | Task author must resolve in the P3 gate item: substitute the Tolkien synthetic fixture, OR add a "provision Narnia source+mapping" P3 pre-step. |
| A3 | INFO | research 06 | Boundary final line carries a suffix (`… — all rules (A-F) satisfied.`). Research correctly instructs gates to assert on the **prefix** `BOUNDARY CONTRACT: PASS`. | Encode prefix-match in the boundary gate item, not full-string equality. |

Both A1 and A2 are non-blocking for the **research-depth lens**: the research is deep enough to build a high-quality granular task file without re-reading source. A2 is a design-vs-shipped mismatch that the research's depth is precisely what caught — it is a WIN for research quality, and its resolution belongs to the task author when authoring the P3 gate item, not to the research.

---

VERDICT: PASS

The research across all six assigned files is DEEP — behavioral (not just inventorial) on the boundary check, edit-anchored down to verified line spans with verbatim design-pack diff content, MDTM-QA-rule-complete, genuinely adversarial on design↔code fidelity (honest [UNVERIFIED] scoping, no rubber stamp), one-item-per-file enumerable, and concrete-and-executed on the P3 proof path (commands actually run, verbatim outputs pasted, the Narnia/Tolkien mismatch surfaced). A builder can produce a high-quality, granular Template-02 task file — one checklist item per file (9 new + 2 edits + VENDOR delta + doc pointer) plus compliant per-phase M3/M4 verification items — from this research alone, without re-reading source. Only non-blocking MINOR advisories (A1 line-count off-by-one; A2 Narnia P3 mismatch for the author to resolve).

## Findings (incremental)
