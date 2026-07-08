# QA Report — Phase Gate P0 Operational-Coherence Lens

**Topic:** laf-adaptation P0 prep skeleton — operational coherence across prep-cordinator + prep SKILL.md + thematic-fidelity + adaptation-rules exemplars + `/laf:prep` & `/laf:rewrite` commands
**Date:** 2026-07-05
**Phase:** doc-qualitative (Phase Gate P0 operational-coherence lens, report-only)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY — no edits applied)

---

## Overall Verdict: FAIL

The P0 skeleton does NOT hang together operationally as a coherent prep phase as written. Of the 9
targeted operational-coherence checks, **5 fail** (2 CRITICAL, 3 IMPORTANT) and 1 more surfaced a
MINOR lens concern. The defects cluster around two failure modes: (a) the Stage-7 greenlight
promotion delegates to an adopted skill (`/kb-management`) that has no awareness of the dual-form
6-key/5-key promotion the prep spec requires, leaving the actual promotion mechanism
unspecified; and (b) Stage 3 assumes an `analyst` `granularity: work` branch that does not exist
in the shipped analyst body — neither its inputs, its output schema, nor its procedure is defined
anywhere except by the prep-cordinator's forward reference. A coordinator cannot dispatch to an
agent mode that the agent itself does not expose.

This is a REPORT-ONLY pass. All findings below are documented; none are applied.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Coordinator stage flow references only existing/new skills (cross-check vs `skills:` frontmatter) | PASS | prep-cordinator.md L6-11 lists `{source-fidelity, adaptation-tiers, adaptation-rules, kb-management, prep, thematic-fidelity}`; all 6 exist under `laf-adaptation/skills/` (verified via `ls skills/`). Stage-flow prose at L46-61 references `/source-fidelity`, `/adaptation-rules`, `/kb-management`, `prep`, `/thematic-fidelity` — all within the frontmatter set. |
| 2 | Commands delegate to agents that exist (`prep-cordinator` for prep; `muse` for rewrite) | PASS | `commands/laf/prep.md` L8 delegates to `prep-cordinator` (exists at `agents/prep-cordinator.md`). `commands/laf/rewrite.md` L15 delegates to `muse` (exists at `agents/muse.md`, an adopted agent). |
| 3 | Greenlight promotion references `/kb-management` correctly (existing adopted skill) | **FAIL** | `/kb-management` is adopted (`skills/kb-management/SKILL.md` L1-5; described in `CLAUDE.md` §1 as adopted). Its body has NO knowledge of: the dual-form 6-key/5-key promotion, the `meaning:` strip rule, the two promotion targets (`kb/adaptation-mapping/<slug>-mapping.yaml` hyphen; `config/concept_mapping/templates/<slug>_mapping.yaml` underscore), or `_confidence` annotation stripping. grep of `kb-management/SKILL.md` for `dual`, `6-key`, `5-key`, `promote`, `meaning` returns zero operational hits. Per the boundary contract (CLAUDE.md §2), `/kb-management` body CANNOT be edited. The prep SKILL.md §6 (L93-99) and prep-cordinator Stage 7 (L82-86) say "promote via `/kb-management`" but the actual transformation (strip `meaning:`, pick hyphen vs underscore, drop `_confidence`, write to two distinct trees) is **not encoded anywhere that the runtime `/kb-management` skill will read it**. The promotion step is therefore operationally undefined — `/kb-management` would receive a 6-key mapping and have no native rule telling it to emit a 5-key stripped variant. |
| 4 | Exemplars clearly marked DERIVED method illustrations (line-1 marker) | PASS | All three exemplars open with the literal line-1 marker `<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-source-truth -->` (sacrifice-and-return.md L1; betrayal-and-redemption.md L1; petrification-body-horror.md L1). This matches the rule in `thematic-fidelity/SKILL.md` §"Exemplar DERIVED-marking rule" L36-44. |
| 5 | Source-path-required semantics coherent end-to-end (Stage 1a, no memory-based work-level) | PASS with NOTE | End-to-end coherence verified across 4 surfaces: `commands/laf/prep.md` L15-16 ("the novel text is mandatory; there is no memory-based work-level analysis"); `prep-cordinator.md` Inputs table L35 (`source_path` REQUIRED, elicited as required input); `prep-cordinator.md` Stage 1(a) L47 + Stage notes L65-67 (NO-ACCESS aborts whole prep; MEMORY-BASED never acceptable at work level); `prep/SKILL.md` §3 L58-62 (text track mandatory; MEMORY-BASED never acceptable at work level). The text-required invariant is stated consistently in all four places. |
| 6 | Stage 3 dispatches `analyst` with `granularity: work` — does the analyst support this mode? | **FAIL** | The shipped `agents/analyst.md` (65 lines, read in full) defines its inputs as `{source_path: source/<work>/ch-<NN>.txt, work, chapter}` (L18-21), is described as running "once per source chapter" (L14), and its output schema (L52-55) is the per-chapter `work/analysis/ch-<NN>.yaml` form. There is NO `granularity` input, NO `granularity: work` branch, NO work-level output schema, and NO work-level procedure in the analyst body. grep across the entire `laf-adaptation/` tree confirms `granularity` appears ONLY in `prep-cordinator.md` and `prep/SKILL.md` — never in `analyst.md`. prep-cordinator.md L72-75 claims "the analyst's additive `granularity: work` branch" exists and specifies a dispatch payload `{work, granularity: work, source_path, out_path: …/20-analysis-work-level.yaml}`, but the analyst itself has no such branch, no work-level output schema, and no work-level meaning-field emission. The Stage-3 text track is therefore dispatching into a mode the agent does not implement. |
| 7 | `meaning:` field — is the analyst's responsibility to emit it defined? | **FAIL** | `thematic-fidelity/SKILL.md` L17-26 defines `meaning: {value, confidence}` as "analyst output" and states "Every analyzed unit (work / chapter / scene) emits" it. But the analyst does NOT load `/thematic-fidelity` (analyst.md L5-8 lists `source-fidelity`, `adaptation-tiers`, `story-memory` — no thematic-fidelity). Nor does `/source-fidelity` (the analyst's loaded skill) mention `meaning` anywhere (grep returns zero hits across 100 lines). The work-level mapping derivation in `prep/SKILL.md` §4 L66-70 says "ADD the top-level `meaning:` key (`/thematic-fidelity`)" but the analyst that produces `20-analysis-work-level.yaml` has no skill loaded that tells it what the `meaning:` field is, what its allowed values are, or how to confidence-tag it. The `meaning:` invariant is owned by a skill the analyst cannot load. |
| 8 | Promotion targets — paths exist (or are runtime-created)? | PASS | `laf-adaptation/kb/adaptation-mapping/` exists and contains sibling mappings (`tolkien-mapping.yaml`, `universal-mappings.yaml`); `config/concept_mapping/templates/` resolves at the repo root (confirmed via `find -type d -name concept_mapping`). Path-contract §3 L51-53 correctly states these are runtime outputs that "do NOT exist before a /laf:prep run reaches greenlight" — i.e., the directories exist, the per-work files are runtime-created. Path infrastructure is sound. |
| 9 | Template tier-key alignment — does `work-mapping-template.yaml` use the 4-tier set the prep spec promises? | **FAIL** (MINOR) | `prep/SKILL.md` §2 L24 and §6 L91 fix the active tier set as `{1,2,3,5}` (four tiers; T4 interpolated, never stored). The shipped `templates/work-mapping-template.yaml` uses `tier_1 / tier_3 / tier_4_5` (and one `tier_2` for concepts) — there is NO `tier_5` key in the template (grep confirms only `tier_1`, `tier_2`, `tier_3`, `tier_4_5`). The mapping the prep pipeline derives into the 5-key form will not have a `tier_5` slot defined by the template; this is a 4-tier-vs-3-tier-key vocabulary mismatch between the prep spec and the carried-verbatim template. (The existing `tolkien-mapping.yaml` similarly has only `tier_1` and `tier_3` rows, so the template vocabulary IS the prior art — but the prep spec's "{1,2,3,5}" language does not match it.) |
| 10 | `/laf:rewrite` reads set matches path-contract §4 | PASS | `commands/laf/rewrite.md` L9-13 reads `[30-mapping, 40-prep-brief, 10-challenges]` by hardcoded path and confirms `50-greenlight.md` shows `status: CONFIRMED`. This matches path-contract.md §4 L59-66 (`rewrite_phase_reads`) exactly, including the explicit exclusion of `70-traceability.md`. The coordinator's Stage-8 handoff prompt (L60: literal `/laf:rewrite --work <slug>`) round-trips correctly. |
| 11 | Coordinator `tools:` list supports the dispatched agents | PASS | prep-cordinator.md L13 lists `Agent(web-researcher, analyst, tier-coordinator)` — all three exist (`agents/web-researcher.md`, `agents/analyst.md`, `agents/tier-coordinator.md`). The tier-coordinator agent is listed in `tools:` but NOT actually dispatched by any stage (Stage 3 dispatches `analyst`; Stage 1c dispatches `web-researcher`) — surfaced as a note, not a defect (it's permissive over-listing). |

## Summary
- Checks passed: 6 / 11 (5 PASS, 1 PASS-with-NOTE)
- Checks failed: 5
- Critical issues: 2 (Stage-3 analyst `granularity: work` mode does not exist; Stage-7 promotion mechanism undefined because `/kb-management` cannot be told the dual-form rule)
- Important issues: 3 (analyst does not load thematic-fidelity so cannot emit `meaning:`; promotion target writer is unspecified under the boundary contract; tier-key vocabulary mismatch is template-level)
- Minor issues: 1 (template tier-key set vs prep spec tier set)
- Issues fixed in-place: 0 (REPORT-ONLY — fix-authorization: false)
- Tool engagement: Read 9 target files (all 9 P0 docs); Bash grep/ls 14 calls for cross-file verification (skills/, agents/, kb/, config/, templates/, .claude/commands/laf/)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `agents/prep-cordinator.md` Stage 3 (L51, L72-75) → `agents/analyst.md` (whole body, 65 lines) | Stage 3 dispatches `Agent(analyst, granularity: work, out_path=…/20-analysis-work-level.yaml)` and asserts "the analyst's additive `granularity: work` branch" exists. The shipped analyst has NO such branch, NO `granularity` input, NO work-level output schema. A coordinator cannot dispatch to a mode the agent does not implement; the text track would either be refused by the analyst (which expects per-chapter `ch-<NN>.txt` input and emits `work/analysis/ch-<NN>.yaml`) or silently mis-parse the payload. | Either (a) author a NATIVE additive `granularity: work` branch on the analyst (new input `granularity`, new output schema `work/prep/<slug>/20-analysis-work-level.yaml`, new procedure that runs Phase-0 on the full novel text and emits per-work facts + work-level `meaning`), AND list `laf-adaptation:thematic-fidelity` in the analyst's `skills:` frontmatter; or (b) define the work-level analysis as a coordinator-owned procedure in `prep/SKILL.md` §3 (not delegated to analyst). Pick one and implement; do not leave the dispatch target undefined. |
| 2 | CRITICAL | `skills/prep/SKILL.md` §6 (L93-99) + `agents/prep-cordinator.md` Stage 7 (L82-86) → `skills/kb-management/SKILL.md` (whole body) | Stage-7 greenlight promotion says "promote `30-mapping.yaml` (dual-form) via `/kb-management`" but `/kb-management` is an ADOPTED skill whose body has zero awareness of: the dual-form 6-key/5-key rule, the `meaning:` strip, the `_confidence` strip, the two promotion targets, or the hyphen-vs-underscore naming. The boundary contract (`CLAUDE.md` §2) FORBIDS editing `/kb-management` to add this knowledge. So the actual transform — strip `meaning:`, drop `_confidence`, pick hyphen vs underscore, write to two distinct trees — has no defined operator at runtime. | Encode the dual-form promotion rule in NATIVE-owned surface that the coordinator actually executes: either (a) a new NATIVE skill (e.g. `laf-adaptation:mapping-promotion`) that the prep-cordinator loads and that owns the 6-key↔5-key transform + target paths, with `/kb-management` invoked only for the mechanical write; or (b) inline the promotion procedure in `prep/SKILL.md` §6 as a coordinator-owned step (write both files from `prep-cordinator`'s own `Write` tool, since its `tools:` already lists `Write`). The current "delegate to `/kb-management`" instruction is operationally empty as written. |
| 3 | IMPORTANT | `agents/analyst.md` L5-8 (skills list) vs `skills/thematic-fidelity/SKILL.md` L17-26 ("the analyst output `meaning` field") + `skills/prep/SKILL.md` §4 L66-70 | `thematic-fidelity` defines `meaning: {value, confidence}` as "analyst output" and the prep mapping derivation depends on the analyst emitting it. But the analyst does not load `/thematic-fidelity`, and its loaded skill `/source-fidelity` does not mention `meaning`. The `meaning:` field is owned by a skill the analyst cannot load, so the analyst has no rule telling it what `meaning:` is, what its allowed values are, or how to confidence-tag it. | Add `laf-adaptation:thematic-fidelity` to the analyst's `skills:` frontmatter (additive, boundary-safe — the analyst is NATIVE so its frontmatter is freely editable), OR move the `meaning:` field definition into `/source-fidelity` (which the analyst already loads). The `meaning:` invariant must live in a skill the analyst actually loads. |
| 4 | IMPORTANT | `skills/prep/SKILL.md` §6 + `skills/prep/resources/path-contract.md` §3 (L31-53) | Path-contract §3 specifies the dual-form promotion outputs in fine detail (6-key hyphen keeps `meaning:`; 5-key underscore strips `meaning:` AND drops `_confidence` annotations), and §5 attributes the writes to "`/kb-management` on greenlight (prep phase)". But there is no NATIVE artifact that actually performs the `_confidence`-annotation strip, the `meaning:` strip, or the schema-form transform. The path contract says WHAT; nothing operationally says HOW or WHO. The `prep-cordinator` is told to "promote via `/kb-management`" — which (per finding #2) is an adopted skill with no such capability. | Same remediation as finding #2: a NATIVE-owned operator (new skill or inline coordinator step) must perform the form transform. Additionally, the path contract should name the actual operator (currently it names `/kb-management`, which is operationally inert for this transform). Update path-contract §5's write-ownership table to name the real operator once chosen. |
| 5 | IMPORTANT | `templates/work-mapping-template.yaml` L17, L21, L23, L30, L34, L36, L50, L54 (tier keys) vs `skills/prep/SKILL.md` §2 L24, §6 L91 ("{1,2,3,5}") | The prep spec fixes the active tier set as `{1,2,3,5}` (4 tiers, T4 interpolated, never stored). The shipped `work-mapping-template.yaml` exposes only `tier_1`, `tier_2`, `tier_3`, `tier_4_5` — there is no `tier_5` slot. The 5-key form the prep pipeline is supposed to produce (and that the rewrite `muse` reads as data) has no template-defined `tier_5` key. Either the prep spec's "{1,2,3,5}" is wrong, or the template is missing a `tier_5` slot, or `tier_4_5` is intended to collapse {4,5} (in which case the prep spec's separate-T5 language is misleading). | Reconcile the vocabulary: either (a) update the prep spec to say "{1,2,3,4-5}" with explicit acknowledgment that T4 and T5 share a slot in the carried template, and explain how the T4-interpolation rule (which `adaptation-tiers/SKILL.md` §"Interpolation" defines as T3-floor + T5-ceiling) applies when the template only has a `tier_4_5` slot; or (b) add explicit `tier_4` and `tier_5` slots to a NATIVE work-mapping template (the existing one is carried-verbatim and likely not editable — confirm against `VENDOR.md`). The current state has the prep spec and the template using incompatible tier vocabularies. |
| 6 | MINOR | `agents/prep-cordinator.md` L13 (`tools: Agent(web-researcher, analyst, tier-coordinator)`) | `tier-coordinator` is listed in the prep-cordinator's `tools:` but is never dispatched by any of the 8 stages (Stages 1c and 3 dispatch `web-researcher` and `analyst` respectively; the rewrite phase's tier-coordinator is dispatched by `muse` later). This is permissive over-listing, not a defect, but it implies a coordination responsibility the coordinator does not actually perform. | Drop `tier-coordinator` from the prep-cordinator's `tools:` list (it's a rewrite-phase agent), OR add a Stage that explains why the prep coordinator needs it. Cosmetic; does not block execution. |

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was present in this spawn prompt; this is a standalone
  Phase-Gate-P0 operational-coherence pass. No rf-qa PASS items were relied on.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Agent-dispatch target audit** — Read the full `agents/analyst.md` (65 lines) and grepped
  `laf-adaptation/` tree-wide for `granularity`. Confirmed the `granularity: work` mode referenced
  by `prep-cordinator.md` Stage 3 exists ONLY in prep-cordinator and prep SKILL.md — never in
  `analyst.md`. The dispatched mode is not implemented by the dispatch target. (Finding #1.)
- **Adopted-skill capability audit** — Read `skills/kb-management/SKILL.md` and grepped it for
  `dual`, `6-key`, `5-key`, `promote`, `meaning` (zero operational hits). Confirmed that
  `/kb-management` is adopted (`CLAUDE.md` §1) and uneditable under the boundary contract
  (`CLAUDE.md` §2), and therefore cannot be the operator that performs the dual-form 6-key↔5-key
  promotion the prep spec encodes. (Finding #2.)
- **Skill-loading coverage audit** — Cross-checked `analyst.md` L5-8 `skills:` list against the
  skill that owns the `meaning:` invariant (`thematic-fidelity/SKILL.md` L17-26). Confirmed
  `thematic-fidelity` is NOT in the analyst's loaded skills and `/source-fidelity` (which IS
  loaded) does not mention `meaning`. The invariant is owned by an unloaded skill. (Finding #3.)
- **Template-tier-vocabulary audit** — Read `templates/work-mapping-template.yaml` (60 lines) and
  grepped for `tier_` keys. Confirmed the template exposes only `{tier_1, tier_2, tier_3,
  tier_4_5}` — no `tier_5` slot — while `prep/SKILL.md` fixes the active set as `{1,2,3,5}`.
  Vocabulary mismatch confirmed. (Finding #5.)
- **Path-infrastructure audit** — Ran `find` for `concept_mapping` and `ls` on
  `kb/adaptation-mapping/`. Confirmed both promotion-target directories exist (and
  `kb/adaptation-mapping/` already contains sibling mappings), so path-contract §3's
  runtime-output claim is consistent with the shipped tree. (Check #8 PASS.)
- **Exemplar marker audit** — Read line 1 of all three exemplars
  (`sacrifice-and-return.md`, `betrayal-and-redemption.md`, `petrification-body-horror.md`) and
  cross-checked against the DERIVED-marking rule in `thematic-fidelity/SKILL.md` L36-44. All
  three carry the literal `<!-- @kind method-illustration; source-fidelity: DERIVED;
  do-not-treat-as-source-truth -->` marker. (Check #4 PASS.)

## Tool engagement summary
- Read: 9 (all 9 P0 target files: prep-cordinator.md, prep/SKILL.md, prep/resources/path-contract.md,
  thematic-fidelity/SKILL.md, 3 exemplars, commands/laf/prep.md, commands/laf/rewrite.md)
- Read (cross-verification): 4 (analyst.md, source-fidelity/SKILL.md, kb-management/SKILL.md,
  templates/work-mapping-template.yaml, muse.md head, tier-coordinator.md head, web-researcher.md head)
- Bash: 14 (ls / find / grep cross-checks against skills/, agents/, kb/, config/, .claude/,
  templates/, exemplar line-1 markers, tier-key vocabulary, granularity presence, meaning presence)
- Web research / external lookup: 0 (this is a local-file-bound operational-coherence review;
  no external lookup required)
- Tavily engagement: 0 attempted (no external lookup required by any check)

## Recommendations
Before this P0 skeleton can be declared operationally coherent, the following MUST be resolved
(ALL findings regardless of severity, per the FAIL verdict):

1. **(Blocking, CRITICAL)** Define who actually performs the Stage-3 work-level analysis. Either
   ship an `analyst` `granularity: work` branch (with input, output schema, and procedure) or move
   the work-level analysis into the coordinator's own procedure. As written, Stage 3 dispatches
   into a mode that does not exist.
2. **(Blocking, CRITICAL)** Define who actually performs the Stage-7 dual-form promotion. A NATIVE
   operator (new skill or inline coordinator step using its own `Write` tool) must own the
   6-key↔5-key transform, the `meaning:` strip, the `_confidence` strip, and the hyphen vs
   underscore path selection. `/kb-management` cannot be that operator (adopted, uneditable, no
   awareness).
3. **(Blocking, IMPORTANT)** Make the `meaning:` invariant reachable from the analyst. Add
   `laf-adaptation:thematic-fidelity` to the analyst's `skills:` (NATIVE-additive) OR move the
   `meaning:` definition into `/source-fidelity`.
4. **(Blocking, IMPORTANT)** Reconcile the tier-key vocabulary between `prep/SKILL.md` "{1,2,3,5}"
   and `templates/work-mapping-template.yaml` `{tier_1, tier_2, tier_3, tier_4_5}`.
5. **(Non-blocking, MINOR)** Drop the unused `tier-coordinator` from `prep-cordinator.md`'s
   `tools:` list, OR add a stage that uses it.

Until findings #1–#4 are resolved, the P0 prep skeleton would fail at Stage 3 (analyst cannot
dispatch) and at Stage 7 (promotion operator undefined) when actually executed.

## QA Complete
