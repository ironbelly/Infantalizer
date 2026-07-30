# QA Report — Source-Fidelity Verification

**Doc:** `docs/laf/LAF-ADAPTATION-FRAMEWORK-TECHNICAL-REFERENCE.md`
**Source of truth:** `laf-adaptation/` @ `feature/laf-0.1-artifacts-and-docs`
**Date:** 2026-07-08
**Phase:** source-fidelity
**Fix authorization:** false (report-only)

---

## Overall Verdict: FAIL

FAIL is driven by fidelity discrepancies, not by any collapse of the doc's core.
The doc's structural spine (6 subsystems, both pipelines, tier axis, boundary
contract, 11-step workflow, prep 8-stage) is overwhelmingly accurate and
code-traced. However the adversarial pass found **6 real divergences** — one of
which recurs in ~5 places (the "69-row" count) and two of which are internal
self-contradictions inside the §5.1 subsystem itself. Per zero-tolerance
standard, any inaccurate quantitative claim or internal contradiction = FAIL.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Semantic coverage (6 subsystems / 2 pipelines / tier axis / boundary) | PASS | §5.1–5.6 each trace to real dirs: `agents/`, `skills/prep/`, `kb/tiers/`, `skills/adaptation-*`, `kb/`, `scripts/check_boundary.py`+`VENDOR.md`. All present in tree. |
| 2 | §5.1 agent I/O — models | PASS | Verified all 11: analyst=opus, muse=opus, writer=opus, critic=sonnet, editor=sonnet, continuity-checker=inherit, safety-verifier=sonnet, reader-sim=opus, tier-coordinator=opus, chronicler=sonnet, prep-cordinator=opus. Exact match to spawn-prompt spec. |
| 3 | §5.1 agent I/O — write/read-only classification | **FAIL** | Table rows correct, but §5.1 *Conventions* prose is wrong twice (see Issues #2, #3). |
| 4 | read-only trio (critic/reader-sim/continuity-checker) tools | PASS | critic=Read/Glob/Grep; reader-sim=Read/Glob/Grep; continuity-checker=Read/Glob/Grep/Bash (no Write) — matches table's "read-only (+Bash)". |
| 5 | writer/chronicler/tier-coordinator/safety-verifier/analyst/muse can Write | PASS | writer=Read/Write/Edit/Bash/Glob/Grep; chronicler=Read/Write/Glob/Grep; tier-coordinator=Read/Write/Glob/Grep/Bash; safety-verifier=Read/Write/Glob/Grep; analyst=Read/Write/Glob/Grep; muse has Write/Edit. All confirmed. |
| 6 | §5.6 boundary rules A/A′/B/C/C′/D/E/F/F′ | PASS | All 9 rule blocks present in `check_boundary.py`: A@521, A′@532, B@561, C@601, C′@555, D@631, E@638, F@656, F′@661. |
| 7 | Modes V/U + hash semantics (LF-normalized, two-field forgery) | PASS | `VENDOR.md:7` prefix_rewrite; VENDOR notes confirm Mode V ≠ two-field forgery; script Mode U HEAD-pin @563-588. LF-normalized text hashing per script docstrings. |
| 8 | ADOPTED-PATCHED = writer.md only (Rule C′) | PASS | `VENDOR.md:48` "ADOPTED-PATCHED is reserved for agents/writer.md only (CH-3)"; `VENDOR.md:70` writer.md=ADOPTED-PATCHED; `check_boundary.py:555` C′ block. writer's `skills:` carries the additive NATIVE `adaptation-rules` line. |
| 9 | §5.3 tier axis (ages / agency-ext / safety) | PASS | tier_1 age[3,5], tier_2[6,8], tier_3[9,11], tier_5[15,17]. agency_externalization present per profile; T1-2 mandatory, T3 permits internal flaws, T5 forbidden. |
| 10 | No tier_4.yaml exists | PASS | `ls kb/tiers/` = tier_1,2,3,5.yaml only. T4 interpolated per doc §5.3. |
| 11 | Count: 16 agents | PASS | `ls agents/` = 16 files. |
| 12 | Count: 18 skills | PASS | `ls -d skills/*/` = 18 dirs. |
| 13 | Count: check_boundary.py = 737 lines | PASS | `wc -l` = 737. |
| 14 | Count: VENDOR 69 rows | **FAIL** | Actual per-file data rows = 67 (lines 60–126). "69" counts header (58) + separator (59). See Issue #1. |
| 15 | Count: upstream SHA 3338495f… | PASS | `VENDOR.md:7` `upstream_sha: 3338495f0fabf778720effdda9386ab56d4ebf6e`. |
| 16 | Phantom detection (all doc paths exist) | PASS | Every cited path resolves: commands at `.claude/commands/laf/{prep,rewrite}.md`, all agents/skills/tiers, `path-contract.md`, `.githooks/pre-commit` region. No fabricated path/rule/mode found. |
| 17 | §14 staleness item (CLAUDE.md 15/16 vs 16/18) TRUE | PASS | `CLAUDE.md:31` "15 agent files"; `CLAUDE.md:33` "16 skill dirs"; also :178/:179. Tree=16/18. Doc's §14 debt entry is **accurate**. |
| 18 | Pipeline order — 11-step rewrite | PASS | `tier-coordinator.md:15-18` defines exact order: analyst→muse→writer→critic→editor→writer→continuity-checker→safety-verifier→reader-sim→tier-coordinator→chronicler. Matches doc §4.2/§5.1. |
| 19 | Pipeline order — 8-stage prep | PASS (minor) | `skills/prep/SKILL.md` §1–§8 + `prep.md` command confirm 8-stage procedure, two HALT gates, dual-form transform. Stages map to skill sections. See Note A. |
| 20 | Checks A/B/C/D (tier-coordinator) | PASS | `tier-coordinator.md`: Check A@59, B@70, C@82, D@95; Meaning-DIFF rides the reconcile gate @178. Matches §5.4. |

---

## Summary

- Checks passed: 18 / 20
- Checks failed: 2 (items 3, 14)
- Critical issues: 0
- Important issues: 3 (one recurring count; two §5.1 internal contradictions)
- Minor issues: 3
- Issues fixed in-place: 0 (report-only, `fix_authorization: false`)

---

## Issues Found

| # | Severity | Location | Doc Claim | Actual Code | Required Fix |
|---|----------|----------|-----------|-------------|--------------|
| 1 | IMPORTANT | §1 L86 ("69-row vendor manifest"), §2.1 diagram L120 ("VENDOR.md manifest (69 rows)"), §5.6 L370 ("`VENDOR.md` (69-row manifest)"), §8.3-region / §9.1 L439 ("69 per-file `laf_sha256`/`upstream_sha256` rows") | VENDOR manifest = **69 rows** / **69 per-file sha256 rows** | `VENDOR.md`: table is lines 58–126. Line 58 = header `\| path \| class \| …`, line 59 = separator `\|---\|`, lines **60–126 = 67 data rows** (10 ADOPTED-CLEAN agents + writer PATCHED + adopted skills globs + NATIVE + BUILD-NEW). Total `\|`-prefixed lines = 69, but **per-file data rows = 67**. | Change "69" → "67" everywhere the claim is *per-file rows*, OR reword to "a 69-line manifest table (67 file rows + header/separator)". The phrase "69 **per-file** sha256 rows" (§9.1 L439) is strictly false. |
| 2 | IMPORTANT | §5.1 Conventions L292 | "Read-only reviewers (`critic`, `reader-sim`, `continuity-checker`) return findings inline" | `editor.md` tools = `Read, Glob, Grep` — **editor is also a read-only reviewer** and is omitted from this list. The doc's own §5.1 table (L284) marks editor "**read-only**". | Add `editor` to the read-only-reviewer list, or reword to "the read-only reviewers (critic, editor, reader-sim, continuity-checker)". Internal contradiction with the table above it. |
| 3 | IMPORTANT | §5.1 Conventions L292 (final sentence) | "Only `writer`/`chronicler`/`tier-coordinator`/`safety-verifier` can write." | This **omits `muse` (Write/Edit) and `analyst` (Write)** — both are Write-capable per the §5.1 I/O table directly above (muse "Write/Edit", analyst "Write (analysis)"). | Reword to include muse + analyst, or scope the sentence to "among the reviewers/promoters." As written it contradicts the table 6 lines above. |
| 4 | MINOR | §5.1 table L281 & §12/§13 | writer = "(ADOPTED-PATCHED, +1 skills line)" | writer's `skills:` block has **7 entries but a duplicate** — `laf-adaptation:creative-writing-craft` appears **twice** (agents/writer.md lines ~7 and ~8), plus the additive NATIVE `adaptation-rules`. The "+1 skills line" (the native `adaptation-rules` graft) is correct; the duplicate craft line is a source-side wart, not a doc error, but the doc's clean "+1" framing hides that the patched frontmatter carries a redundant line. | No doc change strictly required (the "+1 additive NATIVE line" claim is true). Flagging the **source** duplicate for upstream cleanup; optionally note it. |
| 5 | MINOR | §3 tree comment L167 / §1 L84 | "16 agents (rewrite workflow + prep-cordinator + supporting adopted)" | Accurate (16), but the tree includes `brainstormer`, `character-sim`, `outliner`, `style-creator`, `web-researcher` — 5 *adopted* agents not surfaced in the §5.1 table (which only lists the 10 rewrite-workflow agents + prep-cordinator elsewhere). Doc discloses this as "+ supporting adopted", so not a fabrication, but a reader cannot reconcile "16" from §5.1 alone. | Optional: add a one-line note enumerating the 5 supporting adopted agents so the count of 16 is reconcilable from the doc. |
| 6 | MINOR | §5.3 L328 tier-4 row | Tier 4 "Ages 12–14" | No `tier_4.yaml` exists (correct per doc), so ages 12–14 are asserted for an interpolated band with no on-disk source. tier_3=[9,11], tier_5=[15,17] leave 12–14 as the gap — **consistent** and defensible, but unverifiable against a file. | None required; the doc already flags T4 as interpolated. Noting the 12–14 figure has no YAML backing (by design). |

---

## Notes

- **Note A (prep 8-stage):** `prep.md` command and `skills/prep/SKILL.md` confirm the 8-stage procedure, but the SKILL uses §-section numbering (§1–§8) rather than literal "Stage 1..8" labels. The doc's §4.1 stage enumeration is faithful to the section content and the two HALT gates (question gate, greenlight). No fidelity error.
- **Note B (muse skills, out of scope):** `agents/muse.md` references `laf-adaptation:story-planning` and `laf-adaptation:project-setup` skills that have **no matching skill dir** in `skills/`. This is a *source-side* dangling reference, NOT a doc-fidelity error (the tech-ref does not enumerate muse's skill list). Flagged for the source-code owner, tagged `[OUT-OF-SCOPE]` for this doc-QA pass.
- **Confirmed accurate & non-trivial:** the §14 staleness call-out is genuinely correct (CLAUDE.md is stale at 15/16; tree is 16/18) — the doc correctly self-identifies as authoritative over CLAUDE.md, which is exactly the behavior a tech-ref should exhibit.

---

## Confidence Gate

- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 | Glob: 0 | Bash: 12 (each targeting a specific claim: agent frontmatters, VENDOR row count, script line count, tier YAMLs, boundary rules, CLAUDE.md counts, command bodies, workflow order)
- No web research required (all claims intrinsically local).
- Tool-call count (13) ≥ checklist items driving verdict; not padded — each Bash call mapped to a specific claim class.

---

## Recommendations (before doc can PASS)

1. Fix the "69" → "67" per-file-row count everywhere it is stated as *per-file rows* (Issue #1). This is the highest-priority correction — it appears in 4–5 locations.
2. Repair the two §5.1 *Conventions* self-contradictions (Issues #2, #3): add `editor` to the read-only reviewers, and add `muse`+`analyst` to the writers list — both contradict the §5.1 I/O table on the same page.
3. Optionally address the MINOR items (#4 source duplicate skill line, #5 reconcilable 16-count, #6 T4 age provenance note).
4. Source-side (out of scope for this doc): dedupe `creative-writing-craft` in `writer.md`; resolve muse's dangling `story-planning`/`project-setup` skill references.

## VERDICT: FAIL

Severity-rated: 3 IMPORTANT (1 recurring count error, 2 internal contradictions) + 3 MINOR. Zero CRITICAL/fabrication. The doc is ~90% faithful and structurally sound; it fails the zero-tolerance gate on the "69 per-file rows" quantitative error and the two §5.1 convention contradictions.

## QA Complete
