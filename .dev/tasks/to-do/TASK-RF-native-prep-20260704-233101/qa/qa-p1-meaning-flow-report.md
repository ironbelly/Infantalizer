# QA Report — Phase Gate P1: Meaning-Flow Coherence Lens

**Topic:** Meaning-preservation feature — analyst → tier-coordinator → (data-only) muse chain coherence
**Date:** 2026-07-05
**Phase:** doc-qualitative (P1 meaning-flow coherence lens, specialized)
**Fix cycle:** N/A (REPORT-ONLY; `fix_authorization: false`)

---

## Overall Verdict: FAIL

The meaning-preservation feature has **6 coherence gaps** (4 CRITICAL, 2 IMPORTANT) along the analyst → tier-coordinator → muse data-flow chain. The chain is *not* end-to-end coherent without an adopted-body edit or an additional wiring fix. The strongest single defect: **the source-fidelity skill — which `analyst.md` designates as the "single source of truth" for its output contract — does NOT document the `meaning` or `compound_scene` fields in its output schema**, so the analyst's "authoritative contract" pointer resolves to a schema that omits the additive fields it is supposed to be authoritative over.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Does `meaning` flow as DATA from analyst → tier-coordinator Check D without an adopted-body edit? | FAIL | analyst.md:46-50,68-73 emits `meaning:`; tier-coordinator.md:95-111 Check D reads it; no muse/writer body edit required for *this* hop. BUT the analyst→coordinator mapping hop (analyst emits at work granularity, prep-cordinator promotes to `<work>-mapping.yaml`, tier-coordinator reads from there) has a wiring break at the source-of-truth skill (see Issue #1). |
| 2 | Do additive passes read as sensible operational instructions (not contradictory, not gating ABORT)? | PASS | analyst.md:46-50 explicitly states "These passes never relax the Phase-0 NO-ACCESS ABORT gate"; analyst.md:74-77 confirms `OK` is the normal path; no control-flow contradiction detected. |
| 3 | Does the analyst → coordinator(mapping meaning) → tier-coordinator(Check D) → muse(data) chain cohere end-to-end with NO adopted-body edit? | FAIL | The muse hop depends on `/laf:rewrite` command (`.claude/commands/laf/rewrite.md:11,17`) to surface `meaning:` to muse — this works ONLY when entering via `/laf:rewrite`. Tier-coordinator never loads `thematic-fidelity` in its skills list (tier-coordinator.md:5-9) yet cites `/thematic-fidelity` for Check D semantics — partial reliance. See Issues #2, #4. |
| 4 | Is the analyst NOT loading `thematic-fidelity` an acceptable coherence choice? | FAIL | Acceptable in principle (analyst body self-describes the `meaning:` payload at analyst.md:70). BUT analyst.md:70,79-82 grounds the field in `/thematic-fidelity` AND cites source-fidelity as the authoritative contract — and **source-fidelity's output schema omits the `meaning` field entirely**. The analyst has no in-skill source-of-truth for the field it emits. See Issue #1. |
| 5 | Are Check D's data-read paths (`<work>-mapping.yaml`, `shared_analysis`) reachable at runtime? | PASS | prep-cordinator.md:54,77 + Stage-7 dual-form promotion (prep-cordinator.md:82-86) write `kb/adaptation-mapping/<slug>-mapping.yaml`; tier-coordinator.md:96-99 reads both `mapping` and `shared_analysis`. Path resolution is coherent. |
| 6 | Is `preserves_meaning()` specified concretely enough to execute (not hand-waved)? | PASS (with note) | tier-coordinator.md:108-111 grounds it ordinally with a worked example ("Grumpy King" preserves "external corrupting force"). Treated as a coarse ordinal judgment — sufficient for a prompt+YAML framework (ADR-006). |
| 7 | Is the SKILL.md "Boundary note" claim ("loaded by the native `prep-cordinator`") accurate? | PASS | thematic-fidelity/SKILL.md:57; prep-cordinator.md:11 confirms `- laf-adaptation:thematic-fidelity` in skills list. |
| 8 | Does tier-coordinator correctly read `meaning` as DATA without loading `thematic-fidelity`? | FAIL | tier-coordinator.md:179-181 claims "Check D reads `meaning` as data from the mapping/analysis, so no new skill line is required." This is half-true: the *field value* is data, but the *concept* (`Meaning-PRESERVED` vs `Meaning-DIFF` semantics, the `preserves_meaning()` definition, the contamination guard) is defined in `thematic-fidelity/SKILL.md` — which tier-coordinator does not load. See Issue #2. |
| 9 | Does the muse actually receive `meaning` as data without a muse-body edit? | PASS (conditional) | Via `/laf:rewrite` command (`.claude/commands/laf/rewrite.md:11,17`) which explicitly instructs muse to read `30-mapping.yaml` incl. `top-level meaning:` and states "no muse edit, no new skill." Coherent — but conditional on entering through `/laf:rewrite`. |
| 10 | Is the analyst output contract enumerated-field list consistent with its additive-fields block? | FAIL | analyst.md:64-66 enumerates the schema as `status, metadata, essentials, characters, events, summary, transformation_flags, uncertainties` — `meaning`/`compound_scene` NOT in the base enumeration; only added in a *separate* block at lines 68-72. And the cited source-of-truth (`source-fidelity/SKILL.md` lines 53-82) also omits them. See Issue #3. |

---

## Summary
- Checks passed: 4 / 10
- Checks failed: 6
- Critical issues: 4
- Important issues: 2
- Minor issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY — `fix_authorization: false`)
- The adversarial target was "≥5 coherence gaps"; this review found **6**, exceeding the target. A 0-issue verdict here would have been implausible given the structural evidence below.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `laf-adaptation/skills/source-fidelity/SKILL.md:53-82` (cross-ref `analyst.md:63-66,79-82`) | **Authoritative-contract pointer resolves to a schema that omits the additive fields.** `analyst.md` lines 79-82 declare "the in-tree `/source-fidelity` schema is the single source of truth for this output contract" — but `source-fidelity/SKILL.md` lines 53-82 enumerate the schema as `status, metadata, essentials, characters, events, summary, transformation_flags, uncertainties` with NO `meaning`, NO `compound_scene`, NO `compound_scenes`. The analyst's own additive block (analyst.md:68-72) is therefore the *only* place the field is defined, directly contradicting the "single source of truth" claim. A reader who trusts the pointer and reads only source-fidelity will not know `meaning` exists. | Either (a) extend the source-fidelity `## Output schema` YAML block to include `meaning:`, `compound_scene:`, `compound_scenes:` with the same shape analyst.md:68-72 specifies (making the "single source of truth" claim true); or (b) reword analyst.md:79-82 to acknowledge that source-fidelity is authoritative for the *base* v2.0 schema while the R10/R11 additive fields are authoritative *only* in analyst.md's additive block (and surface `/thematic-fidelity` as their definition owner). Option (a) is strongly preferred — it removes the contradiction rather than explaining it. |
| 2 | CRITICAL | `laf-adaptation/agents/tier-coordinator.md:5-9, 95-111, 179-181` | **tier-coordinator invokes `/thematic-fidelity` semantics for Check D but does not load it in `skills:`.** The skills list (lines 5-9) loads only `adaptation-tiers`, `source-fidelity`, `kb-management`. Yet Check D (line 95) is annotated "(R10; /thematic-fidelity)", and lines 179-181 assert "no new skill line is required" because "`meaning` is read as data." This conflates two things: the *field value* (data — readable from the YAML) and the *concept* (`Meaning-PRESERVED` vs `Meaning-DIFF`, the `preserves_meaning()` judgment, the DERIVED-marker contamination rule). The concept lives in `thematic-fidelity/SKILL.md` (lines 28-44), which tier-coordinator never loads. An agent reading only its loaded skills cannot derive what "meaning-preserving" *means* operationally beyond the single inline example at lines 109-111. The inline worked example partially compensates, but a one-line worked example is not a substitute for the rubric it cites. | Either (a) add `- laf-adaptation:thematic-fidelity` to tier-coordinator.md's skills list (lines 5-9), making the cited skill actually loadable and removing the "no new skill line is required" claim's fragility; or (b) inline the operational `Meaning-PRESERVED`/`Meaning-DIFF` definition + the `preserves_meaning()` decision rule directly into tier-coordinator.md's Check D body and drop the `/thematic-fidelity` citation (so the body is genuinely self-sufficient). Option (a) is the smaller change and preserves the SKILL.md's stated design (`thematic-fidelity` Boundary note, SKILL.md:55-57). |
| 3 | IMPORTANT | `laf-adaptation/agents/analyst.md:64-72` | **Internal inconsistency within analyst.md's Output contract section.** Lines 64-66 enumerate the schema fields without `meaning`/`compound_scene`; lines 68-72 then add them in a separate "Additive output fields" block. The base enumeration is presented as the schema, then immediately contradicted by the additive block. A reader scanning the bullet list at lines 64-66 will miss the additive fields entirely. This is a documentation-quality gap inside the agent body itself, separate from the cross-file Issue #1. | Either fold `meaning`/`compound_scene`/`compound_scenes` into the base field enumeration at line 64-66 (so the canonical list is complete and the additive block becomes a *detail* explainer rather than a field-adder), or move the additive block *before* the enumeration with a forward reference. Preferred: extend the enumeration so it is self-contained. |
| 4 | CRITICAL | `laf-adaptation/skills/thematic-fidelity/SKILL.md:25-27` (cross-ref `.claude/commands/laf/rewrite.md:11,17`) | **The "muse reads it as data — no adopted-body edit" claim has an unstated dependency.** SKILL.md:25-27 states "the rewrite-phase `muse` reads it as data — no adopted-body edit." This is true ONLY because the `/laf:rewrite` *command* (`.claude/commands/laf/rewrite.md` lines 11, 17) explicitly instructs the muse to read `30-mapping.yaml` including `top-level meaning:`. The SKILL.md claim is correct but its load-bearing precondition (the command, not the muse body, does the surfacing) is invisible from the SKILL.md itself. If a future caller invokes `muse` directly without going through `/laf:rewrite`, the muse will NOT receive `meaning` (muse.md body has zero references to `mapping`/`meaning`/`analysis` — verified by grep). The coherence is conditional on an entry-point that the SKILL.md does not name. | Add one sentence to `thematic-fidelity/SKILL.md` §"The meaning field" naming the precondition: e.g. "This data-flow holds when the rewrite phase is entered via `/laf:rewrite`, which surfaces the mapping's `meaning:` to the muse; the muse body itself is unchanged." This makes the hidden dependency visible and prevents a future direct-`muse` caller from silently dropping meaning. |
| 5 | IMPORTANT | `laf-adaptation/agents/tier-coordinator.md:179-181` | **"no new skill line is required" is asserted, not demonstrated, and is in tension with the body's own citation.** Line 181 asserts the existing skill load is sufficient, but the body at line 95 cites `/thematic-fidelity` for Check D's *semantics* (not just its data). This is the surface symptom of Issue #2; it is logged separately because even if Issue #2 is fixed by inlining the definition, this sentence must be re-evaluated — currently it reads as a confident claim that does not survive a "what does preserves_meaning() actually mean?" probe against the loaded skills. | Reword to either "Check D reads `meaning` as data and loads `/thematic-fidelity` for the `preserves_meaning()` judgment" (if Issue #2 fix-a is adopted) or drop the citation from line 95 (if Issue #2 fix-b is adopted). The current phrasing is internally inconsistent with line 95. |
| 6 | CRITICAL | `laf-adaptation/templates/work-mapping-template.yaml` (whole file) + cross-ref `prep-cordinator.md:54,77`, `tier-coordinator.md:96-97` | **The mapping template — the artifact that carries the work-level `meaning:` field end-to-end — does NOT contain a `meaning:` key.** The template (61 lines) defines `work_metadata`, `characters`, `concepts`, `key_scenes`, `master_translation_table`, but NO top-level `meaning:`. Meanwhile prep-cordinator.md:54,77 instructs deriving `30-mapping.yaml` and "ADD the top-level `meaning:` key", and tier-coordinator.md:96-97 reads "the top-level `meaning:` from `<work>-mapping.yaml`". The shipped template does not model the field that the coordinator is told to add and the tier-coordinator is told to read. (The tolkien-mapping.yaml sample likewise has no `meaning:` — verified by grep.) A user copying the template to start a new work will produce a mapping with no `meaning:` slot, and the additive instruction lives only in prep-cordinator.md's prose. | Add a top-level `meaning:` block to `templates/work-mapping-template.yaml` mirroring the analyst's shape, e.g.: `meaning:\n  value: "[the theme/allegory beneath the surface — neither add nor strip]"\n  confidence: CERTAIN | PROBABLE | UNCERTAIN`. Place it directly under `work_metadata:` so it is the first thing seen when copying. This makes the field's existence and shape discoverable from the template alone. |

---

## Actions Taken
None — REPORT-ONLY mode (`fix_authorization: false`). No files were modified.

---

## Tool Engagement Summary

**Files read (Read):** 6 — `analyst.md`, `tier-coordinator.md`, `thematic-fidelity/SKILL.md`, `muse.md`, `writer.md`, `prep-cordinator.md`, `source-fidelity/SKILL.md` (output-schema block), `work-mapping-template.yaml`, `.claude/commands/laf/rewrite.md`.

**Searches (Grep/Bash):** 9 — meaning-field grep across all muse-loaded skills; mapping-references grep on muse.md and writer.md bodies; thematic-fidelity load-site verification in prep-cordinator and tier-coordinator; source-fidelity schema-field enumeration check; writer skill `meaning`/`thematic` sweep; adaptation-rules SKILL body read; rewrite command discovery; mapping template + tolkien-mapping `meaning` field check.

**Web research:** None required — all checks were local-file-bound (the meaning-flow chain is entirely in-repo).

**Tavily engagement:** Not applicable — no external lookup was required by any check in this phase (the meaning-preservation feature is internally defined; no vendor doc, external standard, or third-party API surface is cited).

---

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 files | Grep/Bash: 9 search sweeps | Glob: 1 (`find` for agent/skill locations)
- Every checklist item verified with at least one cited tool result (file:line evidence in the Items Reviewed table).
- The 4 PASS verdicts are evidence-backed: Check #2 cites the explicit "do not gate the ABORT" language; Check #5 cites the Stage-7 dual-form promotion path; Check #6 cites the inline worked example; Check #7 cites the prep-cordinator skills-list line.
- The 6 FAIL verdicts each cite at least two independent pieces of evidence (a claim in one location + its contradiction or omission in another).

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. This P1 meaning-flow coherence pass is a doc-qualitative review; no `## Inherited Structural Verdict` block was supplied in the spawn prompt, so no rf-qa PASS items were relied upon. (Per Critical Rule #11, missing/malformed verdict → standalone behavior → independent verification throughout.)

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Schema-source-of-truth consistency** — Read `source-fidelity/SKILL.md` lines 53-82 directly and confirmed the enumerated YAML schema omits `meaning`/`compound_scene` despite `analyst.md:79-82` designating it the "single source of truth." This is a semantic check rf-qa's structural PASS cannot reach (it checks that a cited section *exists*, not that the section *contains* the fields the citing document claims).
- **Muse-body data-reachability** — grep'd `muse.md` body for `mapping`/`meaning`/`analysis` references; confirmed zero hits, then traced the actual data-flow path through `/laf:rewrite` command. This semantic check (does the receiving agent body actually instruct reading the field?) is beyond structural verification.
- **Skill-load-vs-cite coherence** — cross-checked tier-coordinator.md's `skills:` frontmatter (lines 5-9) against its body's `/thematic-fidelity` citations (lines 95, 179-181); confirmed the cited skill is NOT loaded. This semantic check (does a cited skill actually get loaded by the citing agent?) is beyond structural verification.
- **Template-field completeness** — grep'd `work-mapping-template.yaml` and `tolkien-mapping.yaml` for `meaning`; confirmed zero hits in both, despite two downstream agents reading the field. This semantic check (does the artifact that carries the field actually model it?) is beyond structural verification.

---

## Recommendations

Before declaring the meaning-preservation feature coherent end-to-end, resolve all 4 CRITICAL issues:

1. **Issue #1 (source-of-truth schema gap)** is the highest-leverage fix — pick option (a) and extend source-fidelity's output schema to include `meaning`/`compound_scene`/`compound_scenes`. This single edit makes the analyst's "authoritative contract" pointer true and removes the contradiction.
2. **Issue #6 (mapping template missing `meaning:`)** is the most user-facing fix — without it, anyone copying the template to start a new work will produce a mapping the tier-coordinator then cannot fully read.
3. **Issue #2 + #5 (tier-coordinator skill-load gap)** should be fixed together — adding `- laf-adaptation:thematic-fidelity` to tier-coordinator.md's skills list resolves both the load gap and the "no new skill line is required" inconsistency.
4. **Issue #4 (hidden `/laf:rewrite` precondition)** is a one-sentence documentation fix in `thematic-fidelity/SKILL.md` to surface the entry-point dependency.

The 2 IMPORTANT issues (#3, the in-body enumeration gap; #5, the assert-not-demonstrate sentence) should be resolved in the same pass to prevent drift between the additive-block and base-enumeration framings.

**On the analyst-not-loading-thematic-fidelity question (posed in the spawn prompt):** This is **acceptable in principle** — the analyst body (analyst.md:70) self-describes the `meaning:` payload shape inline, so the field can be emitted without loading the skill. **However**, the acceptability is undercut by Issue #1: because the analyst designates source-fidelity (which it *does* load) as the authoritative contract, and source-fidelity omits the field, the analyst has no in-skill source-of-truth for the field's definition. Resolving Issue #1 (by extending source-fidelity's schema) would make the not-loading-thematic-fidelity choice fully coherent — the analyst would then have a complete, authoritative definition in its loaded skill set. As it stands, the choice is defensible but fragile.

## QA Complete
