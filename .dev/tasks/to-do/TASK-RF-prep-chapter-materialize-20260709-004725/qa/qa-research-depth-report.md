# QA Report — Research Depth Review

**Phase:** research-depth
**Lens:** research-depth
**Date:** 2026-07-09
**Fix authorization:** false
**Adversarial stance:** Assume research is superficial until proven otherwise.

**Assigned research files:**
- 01-file-inventory-and-edits.md
- 02-boundary-contract-and-verification.md
- 03-skill-authoring-spec.md
- 04-mdtm-template-and-gate.md

**Driving spec:** .dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md

---

## Overall Verdict: PASS

The research is **deep enough** to produce a high-quality task file without re-reading source.
It goes well past "list files": it captures the boundary-contract MECHANICS (with exact
`check_boundary.py` line cites, verified below), the authoring house-style (with verbatim
frontmatter/section conventions from the two model skills), the FULL manifest schema (carried
verbatim from spec §5), all 16 failure modes, and — most importantly — it RESOLVES the
three-numbering-system trap rather than merely naming it. Edge cases (Books/LWW mode ambiguity,
Mode C zero-resplit adopt, deferred-write invariant, byte-unchanged read-set) are understood
behaviorally, not just enumerated.

I independently verified the highest-risk claims against source (see Confidence + Self-Audit).
The one genuinely load-bearing correctness claim — "adding the new NATIVE skill requires ZERO
edits to `check_boundary.py`" — is TRUE and I proved it from the classifier + verify code paths.
Minor line-anchor imprecisions exist in research 01 but the research flags its own uncertainty
where it occurs, and every locus is independently re-findable, so none rises above MINOR.

---

## Evaluation Against the Four Assigned Questions

### Q1 — Can a builder author SKILL.md + boundary-rules.yaml + manifest schema purely from research 03? → YES

Research 03 is the strongest of the four. It provides:
- **House-style captured behaviorally**, not asserted: frontmatter = `name`+`description` ONLY
  (verified against `source-fidelity/SKILL.md:1-8` and `adaptation-safety/SKILL.md:1-8` — both
  confirmed exactly two keys); procedure-phase numbering (`## Stage 0.1..0.5`) chosen with a
  reason (mirrors spec §4 sub-steps 1:1); tables as the "house workhorse"; the fenced-YAML
  output-contract-at-the-end close (confirmed both model skills end on a schema/verdict block);
  the provenance footnote idiom. This is genuine style-transfer, not a checklist.
- **The FULL manifest schema carried VERBATIM** (§D) from spec §5 lines 106-154, with a field-notes
  subsection (§D.1) cross-cutting §7-§10 that a builder needs to fill each field correctly
  (confidence enums reuse source-fidelity vocab; every chapter row MUST carry
  confidence+provenance+needs_human_review or it's a release-blocking defect; `provenance.class`
  enum; who sets `review.status: CONFIRMED`).
- **A complete section-by-section OUTLINE** (§B, 13 sections) each mapped to a spec § cite, with a
  coverage self-check at the end.
- **All 16 failure modes carried verbatim** (§C) with the instruction NOT to paraphrase (it's the
  release-gating contract).
- **A concrete boundary-rules.yaml skeleton** (§E) with the five evidence-layer keys fixed and the
  regex/pattern content explicitly marked "Builder to author" — honest about what's derivable vs.
  authoring judgment.
- **The non-runtime / ADR-006 invariant** stated as a load-bearing Principle sentence that "MUST
  appear," discharging spec §6/§11/§14-risk-7.

A builder handed research 03 could author all three artifacts without re-reading the spec or the
model skills. **PASS.**

### Q2 — Is the boundary-contract reasoning deep enough to avoid editing check_boundary.py / breaking Rule F? → YES

Research 02 is the deepest technical analysis and its central claims are **independently verified
against source this turn**:
- **"Zero edits to check_boundary.py"** — VERIFIED. `classify()` (check_boundary.py:349-368)
  defaults to NATIVE for any non-upstream skill not in `BUILD_NEW_SKILLS`; `BUILD_NEW_SKILLS =
  {"adaptation-safety"}` (line 47, confirmed); `chapter-materialize` is not in it → NATIVE.
- **"NATIVE_SKILLS is not an allowlist"** — VERIFIED. `NATIVE_SKILLS = {"adaptation-tiers",
  "adaptation-rules", "source-fidelity"}` (line 46) is never read in classify()/verify; existing
  NATIVE rows `skills/prep/**`, `skills/thematic-fidelity/**` (VENDOR rows 122-123, confirmed) are
  NATIVE yet not members. Correct and non-obvious.
- **Rule F satisfied by one `/**` glob row** — VERIFIED. `manifest_covers` (lines 318-325) glob
  branch, `disk_skill_skillmds()` globs `skills/**/SKILL.md`, glob-shape gate requires exactly
  `skills/<name>/**` (one `/` after strip). `skills/chapter-materialize/**` passes.
- **Rule F′ skips NATIVE dirs** — VERIFIED. F′ (lines 661-675) iterates only `adopted_skill_dirs`;
  the code comment literally says "NATIVE/BUILD-NEW skill dirs are already covered by their `/**`
  glob rows." So `resources/boundary-rules.yaml` needs NO separate row.
- **NO_HASH = em dash U+2014** — VERIFIED (`NO_HASH = "—"` line 50).
- **AC6 baseline PASSES today** — VERIFIED by running it: `cd laf-adaptation && uv run python
  scripts/check_boundary.py` → `BOUNDARY CONTRACT: PASS`, exit 0.

Critically, research 02 goes beyond the checker: it identifies TWO invariants the boundary check
**cannot** catch and the task must self-assert — (Q6) `rewrite_phase_reads` byte-stability (§4 is
NATIVE `resources/`, not hashed) and (Q7) the `.claude/` mirror-drift failure mode ("green
boundary check + runtime skill-not-found"). This is exactly the adversarial depth a shallow
review would miss. A builder following research 02 will NOT touch check_boundary.py and will NOT
break Rule F. **PASS.**

### Q3 — Does research 04 give a concrete phase breakdown AND resolve the prep-cordinator renumber trap? → YES

Research 04 does both:
- **Concrete, defensible 6-phase breakdown** (Step 4) with per-phase QA-gate placement (I15),
  parallelism analysis (P2.1∥P2.2, P3.1∥P3.2∥P3.3, P4.1∥P4.2∥P4.3, each set = distinct files, no
  data dep), a dependency table, and the MDTM template rules extracted in Step 1 (B2 6-element
  item pattern, D3 no-items-before-Phase-1, M3 lens-QA sequence, I19 agent-count floors, M4
  source-fidelity gate applicability). It correctly derives QA_GATE=FINAL_ONLY, TESTING=NONE
  (ADR-006 forbids a new script; I18 N/A — no source code), and M4-applies (output derived from
  the spec).
- **The renumber trap is RESOLVED, not just listed.** Step 2c/3 identify THREE distinct numbering
  systems: agent body STAGE 1..8 (Q-gate=5, greenlight=7) — VERIFIED against
  prep-cordinator.md:44-62 this turn; prep SKILL §1..§8; spec §4's STAGE 0..6 (conceptual remap of
  the SKILL §-sequence). Research 04 names the exact trap ("conflating the spec's STAGE 0..6 table
  with an instruction to renumber the agent's 8-stage block") and gives an **evidence-based
  RECOMMENDATION (Approach A: prepend a new STAGE 0, keep STAGE 1..8 byte-identical)** with four
  rationale points, the key one being that prepending zero-shifts every existing "Stage 5"/"Stage
  7" note reference — the load-bearing consistency risk. It then lists the exact consistency
  contract (which prose mentions become "9 stages" vs. which stay "8-section" because they refer to
  the SKILL §-count). This is the single most valuable output for avoiding a silent breakage.
  **PASS.**

### Q4 — Are the edge cases understood behaviorally, not just named? → YES

- **Mode ambiguity (Books/LWW)** — VERIFIED the real files exist: `Books/LWW/` contains
  `...-1..-4.html` (split) AND four `...copy*.html` (monolith duplicates) AND a PDF — the exact
  "split + monolith both present" case. Research 03 §B5 and research 01 encode it as
  `mode_confidence: UNCERTAIN` → HALT-ask, honoring the "must not guess" precedence
  (adopt>folder>file>ambiguity-HALT) and the `--source-mode` override. Behavioral, correct.
- **Mode C zero-resplit adopt** — Research 03 §10 understands it as a behavior: read
  titles/ordinals from existing files, write/refresh ONLY the manifest with `provenance.class:
  ADOPTED`, narnia/tolkien untouched, manifest-less set adopts with `split_confidence: CERTAIN`
  for existence but provenance gaps flagged. Not just named.
- **Deferred-write invariant** — Stated as a bolded standalone rule in research 03 §B7 ("No
  ch-NN.txt for a PROBABLE/UNCERTAIN boundary is committed before the human resolves it") and
  traced through the gate flow (0.4 commit CERTAIN immediately → 0.5 route deferred to §5 gate →
  greenlight commits + sets CONFIRMED). Research 04 Step 2b independently reconstructs the same
  invariant from spec §10. Behavioral.
- **Byte-unchanged read-set** — Research 02 Q6 carries the 3-file read-set verbatim (VERIFIED
  against path-contract.md:62-73), explains WHY it is not machine-enforced (NATIVE resources/, not
  hashed), and gives two concrete verification recipes (grep-assert the 3 exact paths / git-diff
  the §4 region). Research 01 marks §1/§2/§4 BYTE-UNCHANGED at the locus level. Deeply understood.

**PASS.**

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | check_boundary.py needs zero edits (classify defaults NATIVE) | PASS | Read check_boundary.py:44-52, 349-368; BUILD_NEW_SKILLS={"adaptation-safety"} confirmed |
| 2 | NATIVE_SKILLS not an allowlist | PASS | Line 46 set never read in classify/verify; prep/thematic-fidelity NATIVE but not members |
| 3 | Rule F satisfied by single /** glob; F′ skips NATIVE | PASS | manifest_covers 318-325; F 656-659; F′ 661-675 with confirming comment |
| 4 | Glob-shape gate accepts skills/chapter-materialize/** | PASS | Read 285-295; one-`/`-after-strip rule confirmed |
| 5 | NO_HASH em dash U+2014 | PASS | Line 50 `NO_HASH = "—"`; VENDOR rows 116-126 use same |
| 6 | AC6 baseline passes today | PASS | Ran check_boundary.py → PASS, exit 0 |
| 7 | VENDOR NATIVE-row format/placement | PASS | Read VENDOR.md:116-126; existing glob rows match proposed shape |
| 8 | Symlink mirror mechanics (research 01) | PASS | `.claude/skills/prep -> ../../laf-adaptation/skills/prep`; prep-cordinator.md symlink; prep.md real file; no laf commands dir |
| 9 | prep-cordinator STAGE 1..8, Q-gate=5, greenlight=7 | PASS | Read prep-cordinator.md:5-11,20,44-62 |
| 10 | Three-numbering-system trap resolved | PASS | Research 04 Step 2c/3 + Approach A rationale; verified all three numberings against source |
| 11 | Model-skill frontmatter = name+description only | PASS | source-fidelity + adaptation-safety SKILL.md:1-8 |
| 12 | Manifest schema carried verbatim & complete | PASS | Research 03 §D == spec §5 lines 106-154 |
| 13 | 16 failure modes carried verbatim | PASS | Research 03 §C == spec §7 table |
| 14 | Books/LWW mode-ambiguity edge case is real | PASS | ls Books/LWW: -1..-4.html + copy*.html + pdf all present |
| 15 | Read-set byte-unchanged understanding | PASS | path-contract.md:62-73 == research 02 Q6 verbatim; not machine-enforced correctly noted |
| 16 | Command arg-hint locus (research 01) | PASS | .claude/commands/laf/prep.md:3 matches cited hint |
| 17 | prep SKILL §1 "8 files 00-70" intact requirement | PASS | prep/SKILL.md:15-20 confirms; N3 no-9th-file honored |
| 18 | MDTM template rules + phase breakdown defensible | PASS | Research 04 Step 1 (B2/D3/M3/I19/M4) + Step 4 phase map with parallelism |

## Summary
- Checks passed: 18 / 18
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (line-anchor imprecision; self-flagged cross-file open-question)
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence
Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 6 (all 4 research files + spec + report readback) | Grep: 0 | Glob: 0 | Bash: 6
(check_boundary.py sections x2, boundary run, Books/LWW+VENDOR listing, symlink+structure,
model-skill+read-set+loci)

Bash calls each verified multiple items (e.g. one call confirmed Books/LWW + VENDOR rows +
skill-absence), so tool-call count is lower than 18 by design, not by sampling — every claim above
maps to a specific tool output; none is padding. Adversarial minimum met: I attempted to falsify the
central "zero edits to check_boundary.py" claim by reading the actual classifier and both verify
rules, and could not — it holds.

Tool-engagement summary (web): No external/web lookup was required — all verification was
local-file-bound (research files, spec, source code). Tavily was therefore not invoked; no fallback
occurred.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | research 01 §3 (path-contract §5 anchors) | §5 header cited as "line 76" and chapter-row line noted ambiguously ("actually the chronicler row is line 82"); research self-flags the uncertainty. Actual §5 header is `## 5. Write-ownership` and the table structure is as described. | No blocking fix. Builder inserts §5 rows by content-anchor ("after the work/prep/<slug>/* row"), which research 01 already specifies — robust to the off-by-a-few. |
| 2 | MINOR | research 04 P4.1 residual open-question | P4.1 leaves "mirror to .claude/ if the prep mirror carries resources/ (open question gap #1)" partly open. Research 01 §0 already resolves it: `.claude/skills/prep` is a DIRECTORY symlink (verified this turn), so editing the laf source auto-mirrors resources/. | No blocking fix. Builder applies research 01's dir-symlink conclusion to close research 04's residual open-question; worth noting explicitly in the task. |

## Actions Taken
None — fix_authorization: false. Both findings are MINOR and non-blocking; documented for the builder.

## Recommendations
- Proceed to task authoring. The research package is builder-ready.
- Builder should carry research 04's Approach-A consistency contract verbatim (the STAGE-0 prepend
  that zero-shifts STAGE 1..8) — this is the highest-risk edit and the research resolves it correctly.
- Builder should include the two task-owned asserts research 02 flags that the boundary check cannot
  catch: (a) grep-assert the 3 rewrite_phase_reads paths byte-unchanged; (b) verify the new skill dir
  is mirrored (or rely on the verified dir-symlink pattern) so there is no "green check + runtime
  skill-not-found."
- Builder should reconcile the one residual cross-file open-question (research 04 P4.1 resources/
  mirror) using research 01's dir-symlink finding.

## QA Complete
