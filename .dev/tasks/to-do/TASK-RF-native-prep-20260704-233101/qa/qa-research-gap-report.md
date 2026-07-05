# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Native-prep — build MDTM task file implementing docs/native-prep/design/DESIGN.md across P0→P4
**Date:** 2026-07-04
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Adversarial Stance

Assume research missed areas needed to build a granular, executable task file. Verify each of the 7 gap-checklist items against the actual research files. 0 issues requires cited tool evidence.

## Files In Scope
- 01-file-inventory.md
- 02-patterns-conventions.md
- 03-boundary-integration.md
- 04-template-and-examples.md
- 05-design-pack-crossvalidation.md
- 06-verification-and-proof-flow.md

(Findings appended incrementally below.)

---

## Gap-Checklist Findings

### Gap-1 — Authoring convention for EVERY new file type — COVERED (no gap)

Every new file type has copy-followable authoring guidance:
- New agent (`prep-cordinator.md`): 02-patterns §1.1–1.4 (5-key set, `tools: >` folded form, block-list skills). Evidence-cited to `muse.md:22-26`, `analyst.md:9`.
- New skill `SKILL.md` (`prep`, `thematic-fidelity`): 02-patterns §2.1–2.4 (name+description-only frontmatter, `SKILL.md`+`resources/`, no `rules/`/`templates/`). Full section outlines exist in `prep-skill-specs.md §1-2` (verified by me this turn — both skills have complete 8-section / 6-section body outlines + frontmatter).
- Resource md (`path-contract.md`): covered by skill `resources/` convention; DESIGN routes it as import-by-reference (prep-skill-specs §1 R3).
- Exemplar md: 02-patterns §4 gives the verbatim line-1 DERIVED marker + full section shape (`package-schemas.md §7`, verified L257-269 this turn).
- Command md: 02-patterns §3.1–3.4 gives path→invocation mapping + verbatim frontmatter for both commands (`prep-agent-schemas.md §5`).

Verdict: PASS. No new file type lacks authoring guidance.

### Gap-2 — analyst.md / tier-coordinator.md diffs precise enough for self-contained edit items — COVERED (no gap)

01-file-inventory Category 2 gives, for BOTH files, exact anchor headings, verified current line numbers, insertion points, and the design-doc line range carrying the verbatim content to land (E1a/E1b/E1c, E2a/E2b/E2c). 05-crossval §E/§F independently CODE-VERIFIED every anchor line (analyst.md:18/33/51; tier-coordinator.md:59/70/82/145). An edit item can be authored self-contained from these.

Minor observation (not a gap): E1b's landing content (the literal `meaning:`/`compound_scene` YAML schema) is described as living in "/source-fidelity + package-schemas.md §3" rather than quoted verbatim in 01. The exact YAML block IS quoted in 02-patterns §5.2 (`package-schemas.md:160-166`) and prep-skill-specs §"The meaning field". Cross-file, the content is fully specified — so this is adequately covered, but the builder must pull the literal block from 02/prep-skill-specs, not 01. Rated INFORMATIONAL only.

Verdict: PASS.

### Gap-3 — VENDOR-row-update actionable WITHOUT upstream checkout — COVERED (no gap)

03-boundary Q2/Q3 is the strongest section. It proves `--init` HARD-REQUIRES `--upstream` (early return 2, `check_boundary.py:349-354`) AND that `--init` rewrites the WHOLE manifest (regenerating every adopted hash). It then specifies the exact no-upstream fallback: hand-add three rows in verbatim 4-cell format `| path | NATIVE | — | — |`, then run plain Mode-V verify. Q3 traces every rule (A/A′/C′/B/C/D/E/F/F′) to prove the hand-add path yields `BOUNDARY CONTRACT: PASS`, exit 0, and warns Rule F FAILS loud if files exist but rows are NOT hand-added. The parser gate (4-cell, em-dash both hash cells) is spelled out. This is fully buildable.

Verdict: PASS.

### Gap-4 — Dual-form promotion buildable for the /kb-management step; runtime-vs-build-time distinction clear — PARTIAL GAP

What IS covered:
- The two promotion targets, forms, and the strip/keep rule are fully specified: 02-patterns §5.2, 05-crossval §D, 03-boundary Q6, plus `package-schemas.md §4.1` (verified this turn — the two-row table: kb hyphen 6-key `meaning` kept; root underscore 5-key `meaning` STRIPPED, `_confidence` dropped).
- 03-boundary Q6 correctly proves BOTH promotion dirs are OUTSIDE the boundary check's `agents/`+`skills/` glob, so promotion neither helps nor hurts the green gate.

What is UNDER-COVERED (the gap the lens asks about):
- **The runtime-vs-build-time distinction is NOT explicitly stated anywhere in the research.** The lens question notes promotion is a RUNTIME behavior of the prep-cordinator (`/kb-management` writes both forms on greenlight at Stage 6/7 — confirmed by me this turn in prep-skill-specs §6 and package-schemas §4.1 "On greenlight, /kb-management writes two forms"), NOT a build-time file the task creates. A grep of all six research files for `runtime|build-time|LangGraph` returns only two hits, NEITHER about promotion (02-patterns:133 is about §-refs; 04:32 is about `task_type`). A task builder reading only the research could mistakenly author a P0–P2 build-time item that hand-writes `<slug>-mapping.yaml`/`<slug>_mapping.yaml` into the promotion dirs, instead of encoding it as a behavior the `/prep` SKILL.md §6 describes and the P3 run exercises. Nothing in the research draws this boundary for the builder.
- **No kb-6-key validation command exists.** 06-verification explicitly self-flags this: the kb-6-key check "was NOT run here (out of my scope column; R1/R5 own the kb-mapping schema)" (06:145). I confirmed this turn that the CURRENT `kb/adaptation-mapping/tolkien-mapping.yaml` is **5-key, no `meaning:` key** (`sorted(d)` → 5 keys; `grep '^meaning:'` → none). So the 6-key form is a P3-RUN OUTPUT state, not a shipped file — the P3 gate needs a validation command that asserts on the run-produced `work/prep/<slug>/30-mapping.yaml` (or the promoted kb file AFTER the run), and no such command string is provided in any research file. R1/R5 were named as owners but neither 01 nor 05 supplies it.

Impact on task buildability: The /kb-management promotion STEP can be described, but (a) the builder has no explicit signal to encode it as prep-skill runtime behavior vs a build-time file-write item, and (b) the P3 hard-gate's "kb 6-key" verification sub-condition has no runnable command — only the root-5-key command is runnable today.

Verdict: PARTIAL — IMPORTANT gap (see Issues Found #1 and #2).

### Gap-5 — P3 end-to-end proof buildable; Narnia-vs-Tolkien resolution actionable — PARTIAL GAP

What IS covered:
- 06-verification did the critical work: it PROVED, by running `ls -laR laf-adaptation/source/` and `find … -iname '*narnia*'`, that NO Narnia source and NO narnia_mapping exist, and that a readable Tolkien fixture (`source/tolkien/ch-01.txt`, PATH-B synthetic, 259 words) + committed `tolkien-mapping.yaml` DO exist. This makes P3-on-Tolkien runnable today.
- It surfaces two resolution OPTIONS: (a) substitute Tolkien for Narnia, or (b) add a "provision Narnia source+mapping" P3 pre-step.

What is UNDER-COVERED:
- **The research presents two options but does NOT RESOLVE which to use** — it defers ("so it is resolved when the task is authored", 06:128). Per the QA-gate rule, an unresolved decision that gates a HARD phase is a gap, not a documented resolution. The lens explicitly frames the expected resolution as "use Tolkien source"; the research stops short of committing to it. Additionally, DESIGN.md §7 P3 (verified this turn, L315) literally interleaves BOTH works in one gate line: it says run `/laf:prep "The Lion, the Witch and the Wardrobe"` but then `/laf:rewrite --work narnia` reads the package — so even the "substitute Tolkien" option must decide the `--work <slug>` value (`tolkien` vs the on-disk mapping slug) and the `/laf:prep` title argument. The research does not spell out the substituted invocation (exact title string + `--work` slug) that a P3 item would embed.

Impact: A P3 gate item cannot be authored fully self-contained without the builder making an un-researched decision. The evidence to decide is present; the decision + the exact substituted command string is not.

Verdict: PARTIAL — IMPORTANT gap (see Issues Found #3).

### Gap-6 — Missing verification command for any phase gate — ONE GAP

Per-gate command coverage (from 06-verification §"summary table" + DESIGN §7, verified this turn):
- P0 boundary: `check_boundary.py --init` — 06 marks "Unverified — R3 scope"; 03-boundary Q2/Q3 RESOLVES it (hand-add + Mode V). Covered across files.
- P1 Mode-V: `uv run python laf-adaptation/scripts/check_boundary.py` — RUN, PASS baseline. Covered.
- P1 unchanged-adopted proof: `git diff --stat -- writer.md muse.md` — RUN, empty=PASS. Covered.
- P3 root-5-key: `uv run --with pyyaml python -c "…tolkien_mapping.yaml…print(sorted(d))"` — RUN, PASS. Covered.
- **P3 kb-6-key: NO COMMAND (see Gap-4).** This is the one genuinely missing phase-gate verification command. The P3 gate's own text (DESIGN L315) requires "dual-form promotion (root 5-key, kb 6-key)" — the kb-6-key half has no runnable assertion anywhere in the research.
- P2 command-resolution: DESIGN P2 gate says "`/laf:prep` resolves and delegates". No runnable NON-interactive verification command is given for "the command file resolves" (e.g. asserting the file exists at `.claude/commands/laf/prep.md` with valid frontmatter + a `prep-cordinator` delegation reference). 02-patterns §3 gives the authoring shape but no gate-check command. This is a MINOR gap — a file-existence + grep assertion is trivially authorable, but the research leaves it unspecified.

Verdict: PARTIAL — the kb-6-key command is IMPORTANT (folded into Issue #2); the P2 resolution check is MINOR (Issue #4).

### Gap-7 — MDTM QA-encoding detail for the generated task file's own gates — COVERED (no gap)

04-template §8 is thorough: it enumerates I15/I16/I19/I20/I21/I22/M2/M3/M4 with exact agent-count floors, intensity levels, serialized-fix protocol, and fidelity-gate requirement. §9 shows the prior example task's per-agent M3 gate encoding (PGn.1–PGn.5), the check_boundary L3 fix-loop gate item (max 3 cycles→HALT), the per-condition L4 verdict + L6 aggregation, and the PC.1–PC.6 post-completion structure. The builder has a complete, evidence-cited QA-encoding recipe including the source-fidelity M4 gate.

One note (not a gap): the design pack is the source doc, so per I21 an M4 source-fidelity gate is mandatory — 04 §8 covers I21 and §9 shows the prior task applied M4 after Phase 1. Adequately covered.

Verdict: PASS.

---

## File-Inventory / Completeness Cross-Check (research-gate items 1 & 10)

| File | Status marker | Summary present | Note |
|---|---|---|---|
| 01-file-inventory.md | `Status: Complete` (×2) | yes (`## Summary`) | Complete. |
| 02-patterns-conventions.md | `Status: **Complete.**` | yes (`---` closing summary bullets) | Complete. |
| 03-boundary-integration.md | header says `Status: In progress` (L6) BUT ends `## Status: Complete` (L204) | yes (3-line summary) | **STALE HEADER** — the top-of-file "In progress" was never updated to "Complete" though the file is finished. MINOR hygiene defect, does not indicate lost content (all 6 Q-sections present + summary). Issue #5. |
| 04-template-and-examples.md | `Status: Complete` (×2) | yes (`## Summary`) | Complete. |
| 05-design-pack-crossvalidation.md | `Status: Complete` | yes (bottom-line + Contradictions section) | Complete. |
| 06-verification-and-proof-flow.md | `## Status: Complete` | yes (`## Summary of what was RUN`) | Complete. |

Incremental-writing check (item 10): all six files show iterative structure (numbered Q/section growth, mid-file caveats, "coordinate with R3" cross-notes) — no one-shot perfect-structure signature. No lost-data flag.

Doc-cross-validation (item 4): 05-crossval tags every design claim `[CODE-VERIFIED]`/`[UNVERIFIED]`; I spot-verified the current kb 5-key state, the analyst/tier-coordinator anchors (via 05's cited lines), and package-schemas §4.1 — all consistent. One `[UNVERIFIED]` (Rule E upstream collision) is correctly flagged non-blocking for Mode V.

---

## Confidence Gate

Per-item categorization (gap-checklist, 7 items):
- Gap-1 [x] VERIFIED — read 02-patterns §1-4 + prep-skill-specs §1-2 this turn.
- Gap-2 [x] VERIFIED — read 01 Category 2 + 05 §E/§F; anchors cross-checked.
- Gap-3 [x] VERIFIED — read 03 Q2/Q3 in full.
- Gap-4 [x] VERIFIED — grepped all 6 files for runtime/build-time; ran `sorted(d)` + `grep '^meaning:'` on current kb file (5-key confirmed); read package-schemas §4.1 + prep-skill-specs §6.
- Gap-5 [x] VERIFIED — read 06 P3 section + DESIGN §7 L315.
- Gap-6 [x] VERIFIED — read 06 summary table + DESIGN §7 gate column.
- Gap-7 [x] VERIFIED — read 04 §8-9.

TOTAL = 7 | VERIFIED = 7 | UNVERIFIABLE = 0 | UNCHECKED = 0
confidence = 7 / (7 - 0) * 100 = **100.0%** — eligible for a verdict (threshold met; this is a FAIL verdict on gap-content, not a coverage failure).

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 1 (multi-pattern) | Glob: 0 | Bash: 4 (ls, grep-sweep, sorted(d)/meaning, status-check)
(No web research performed — all claims are source-truth-local; Tavily not required.)
Tool-engagement minimum: 14 tool calls ≥ 7 checklist items. Satisfied.

---

## Overall Verdict: FAIL

Rationale: Under the research-gate rule (item 6), ALL gaps regardless of severity = FAIL, and the gate must be resolved before the task file is built. Three IMPORTANT gaps and two MINOR gaps were found that would degrade the granularity/executability of the P3 hard gate and the /kb-management step if the builder proceeded on the research as-is. The research is strong (4 of 7 gap areas fully covered, zero fabrication, zero design↔code contradiction), but the gaps are real and concrete.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gap-1 authoring conventions per new file type | PASS | 02-patterns §1-4 + prep-skill-specs §1-2 read this turn; every file type has copy-followable guidance |
| 2 | Gap-2 analyst/tier-coordinator diff precision | PASS | 01 Cat-2 anchors + 05 §E/§F CODE-VERIFIED lines |
| 3 | Gap-3 VENDOR-row update without upstream | PASS | 03 Q2/Q3 hand-add + Mode-V rule-by-rule proof |
| 4 | Gap-4 dual-form promotion + runtime/build-time clarity | FAIL | grep→no runtime/build-time promotion note; current kb file confirmed 5-key; no kb-6-key command |
| 5 | Gap-5 P3 proof + Narnia/Tolkien resolution | FAIL | 06 offers 2 options, defers decision; DESIGN L315 mixes both works; no substituted command string |
| 6 | Gap-6 phase-gate verification commands | FAIL | kb-6-key command absent (06:145 self-flags); P2 resolution check unspecified |
| 7 | Gap-7 MDTM QA-encoding for generated gates | PASS | 04 §8-9 full I15-M4 + prior-task per-agent gate encoding |
| 8 | File inventory / Status / Summary (research-gate item 1) | PASS (1 minor) | all 6 Complete + summarized; 03 stale "In progress" header |
| 9 | Incremental-writing compliance (item 10) | PASS | iterative structure across all 6; no one-shot signature |
| 10 | Doc cross-validation tags (item 4) | PASS | 05 tags every claim; spot-verified kb/anchors/§4.1 |

## Summary
- Gap areas passed: 4 / 7 (Gap-1, Gap-2, Gap-3, Gap-7)
- Gap areas with gaps: 3 / 7 (Gap-4, Gap-5, Gap-6 — partially overlapping root causes)
- Critical issues: 0
- Important issues: 3
- Minor issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Gap-4 / all files (missing) | Runtime-vs-build-time boundary for dual-form promotion is never stated. Builder could wrongly author a build-time file-write item for the promotion targets instead of encoding it as `/prep` SKILL.md §6 runtime behavior exercised by the P3 run. | Add a research note (owner R1 or R5) explicitly stating: promotion via `/kb-management` is RUNTIME prep-cordinator behavior on greenlight (prep-skill-specs §6; package-schemas §4.1), NOT a P0–P2 build-time file. The task's P0–P2 must NOT create `<slug>-mapping.yaml`/`<slug>_mapping.yaml`; those appear only as P3-run outputs. |
| 2 | IMPORTANT | Gap-4/Gap-6, 06:145 | No runnable kb-6-key validation command. Current `kb/adaptation-mapping/tolkien-mapping.yaml` is 5-key (verified); the 6-key form is a P3-run output, so the P3 "kb 6-key" gate half has no assertion. | Supply the command (owner R1/R5): after the P3 run, assert the run-produced mapping (e.g. `work/prep/<slug>/30-mapping.yaml` and/or the promoted kb file) has the 6 keys incl. top-level `meaning:` — `uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('<path>')); assert 'meaning' in d and len(d)==6, sorted(d); print('kb 6-key OK')"`. Pair it with the existing root-5-key command in the P3 gate. |
| 3 | IMPORTANT | Gap-5, 06:128 / DESIGN L315 | Narnia-vs-Tolkien P3 mismatch is surfaced but NOT resolved; DESIGN L315 mixes `/laf:prep "The Lion, the Witch and the Wardrobe"` with `/laf:rewrite --work narnia`. No committed substituted invocation. | Resolve to the shipped fixture: commit "use Tolkien" and record the exact P3 invocation strings — `/laf:prep "<Tolkien title>" --source laf-adaptation/source/tolkien/ch-01.txt` then `/laf:rewrite --work <on-disk tolkien slug>` — so the P3 item is self-contained. (Slug must match the on-disk mapping filename stem.) |
| 4 | MINOR | Gap-6, DESIGN P2 gate | P2 gate ("`/laf:prep` resolves and delegates") has no runnable non-interactive verification command. | Add a trivial gate command: assert `.claude/commands/laf/prep.md` (and `rewrite.md`) exist with valid frontmatter and grep the body for a `prep-cordinator` (resp. `muse` + the 3 hardcoded paths) delegation reference. |
| 5 | MINOR | 03-boundary-integration.md:6 | Stale top-of-file `Status: In progress` header while file ends `## Status: Complete`. No content loss, but violates the "each file Status: Complete" gate-hygiene expectation. | Update L6 header to `Status: Complete` for consistency. |

## Recommendations
- Resolve all five issues before greenlighting synthesis / task-file build. Issues #1–#3 are the load-bearing ones: they directly determine whether the P3 hard gate and the /kb-management step become granular, self-contained, executable task items or leave the builder guessing.
- Issues #1, #2, #3 are best handled by a short follow-up research note (R1/R5 for #1/#2; R6/R5 for #3) rather than a rewrite — the underlying evidence is already gathered; only the explicit resolution/command is missing.
- Issues #4, #5 are trivial and can be closed in the same pass.
- No fabrication, no design↔code contradiction, and strong coverage on Gaps 1/2/3/7 — the research base is sound; these are additive closures, not a redo.

## QA Complete

