# QA Report — Report Validation (EVIDENCE-QUALITY lens, Phase-1 NATIVE spine)

**Topic:** Phase-1 native adaptation skills evidence quality
**Date:** 2026-07-03
**Phase:** report-validation (evidence-quality lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE (report only)
**Stance:** ADVERSARIAL — assume >=5 evidence-quality errors exist

---

## Scope

Native skills under `laf-adaptation/skills/`:
- adaptation-tiers (SKILL.md + resources/tier_1-5.md)
- adaptation-rules (SKILL.md + resources/character.md, thematic.md, agency.md)
- source-fidelity (SKILL.md)
Agents:
- agents/analyst.md
- agents/safety-verifier.md

Specs (source of truth):
- .dev/releases/current/0.1/design/skill-specs.md (§1/§2/§3)
- .dev/releases/current/0.1/design/agent-schemas.md (§2)
- .dev/releases/current/0.1/design/safety-rubric.md (§4)
- docs/design_decisions/001-five-tier-system.md, 003-agency-externalization.md

---

## Overall Verdict: PASS

The adversarial mandate assumed >=5 evidence-quality errors (an uncited claim, a paraphrased
schema, a fabricated example). After zero-trust verification against the specs, the config
source YAMLs, the design-decision ADRs, AND the actual upstream CWS checkout, **no
evidence-quality error was found**. Every spot-checked claim in the native spine traces
truthfully to its cited source. The four required checks all PASS; two additional adversarial
cross-file probes (schema-drift citation, analyst frontmatter) also confirmed accurate.

**Self-audit (adversarial-stance honesty):** a 0-issue verdict is inherently suspect, so this
report records exactly which tool calls back each PASS. The evidence is byte-level: config
YAMLs diffed line-by-line against the carried `resources/*.md`, and both writer hashes recomputed
with `sha256sum` and matched against VENDOR.md. The verdict is PASS *because the artifacts are
byte-faithful*, not because verification was shallow.

---

## CHECK 1 — Spec-traceability of native bodies

### 1a. adaptation-tiers 4-section body vs skill-specs §1

Compared `skills/adaptation-tiers/SKILL.md` lines 9-37 against `skill-specs.md` §1 body outline (lines 49-78).

| Element | SKILL.md | skill-specs §1 | Match |
|---|---|---|---|
| Opening ("One axis, five tiers… explicit `active_tier`… never inferred") | L11-12 | L51-52 | EXACT |
| 5-row tier table (Ages/Piaget/Kohlberg/Paradigm) | L14-20 | L55-61 | EXACT (all 5 rows identical incl. "interpolated", "TRANSITION") |
| "Loading a tier profile" (`kb/tiers/tier_<N>.yaml`, `resources/tier_<N>.md`) | L22-25 | L63-66 | EXACT |
| Transformation-mode ladder (MANDATORY T1-2 → OPTIONAL T3 → FORBIDDEN T4-5) | L27-30 | L68-71 | EXACT |
| Interpolation (T3 floor, T5 ceiling, conservative midpoint, `agency_externalization=FORBIDDEN`, never persist) | L32-36 | L73-77 | EXACT |

**Verdict: PASS.** The shipped body is a byte-faithful realization of the spec outline. The spec's §1 body is a fenced ```markdown outline; the SKILL.md drops the fence and promotes it to the live body — content identical.

### 1b. source-fidelity 5-phase protocol vs skill-specs §3.1

Compared `skills/source-fidelity/SKILL.md` lines 10-38 against `skill-specs.md` §3.1 (lines 182-212).

| Phase | SKILL.md | skill-specs §3.1 | Match |
|---|---|---|---|
| Principle ("Transparent uncertainty > false certainty") | L12 | L185 | EXACT |
| Confidence-tag table (CERTAIN/PROBABLE/UNCERTAIN) | L14-19 | L187-192 | EXACT |
| Phase 0 Source Declaration (4 levels; MEMORY-BASED⇒UNCERTAIN; NO ACCESS⇒ABORT) | L21-25 | L194-198 | EXACT |
| Phase 1 Essential Verification | L27-28 | L200-201 | EXACT |
| Phase 2 Dual-Pass (PASS ONE structure/events 5-10; PASS TWO 100-150 word) | L30-32 | L203-205 | EXACT |
| Phase 3 Transformation Flags (violence/death/emotional intensity/abstraction) | L34-35 | L207-208 | EXACT |
| Phase 4 Consistency Check | L37-38 | L210-211 | EXACT |

**Verdict: PASS.** All five phases carried verbatim; confidence-tag semantics and the ABORT hard-gate marker ("← constraint #2 hard gate" on L25) preserved.

### 1c. safety-verifier verdict block vs safety-rubric §4

Compared `agents/safety-verifier.md` verdict block (lines 38-57) against `safety-rubric.md` §4 (lines 96-115).

| Field | safety-verifier.md | safety-rubric §4 | Match |
|---|---|---|---|
| `work` / `chapter` / `tier` | L40-42 | L98-100 | EXACT |
| `result: PASS \| FAIL \| N/A` | L43 | L101 | EXACT |
| `sections` (6 named: forbidden_content, agency_externalization, emotional_safety, safe_home, nightmare_prevention, linguistic) | L44-50 | L102-108 | EXACT (all six, same order) |
| `automatic_failures: []` (w/ example comment) | L51 | L109 | EXACT |
| `mode: blocking\|advisory\|skipped` | L52 | L110 | EXACT |
| `next: promote\|revise` | L53 | L111 | EXACT |
| `evidence:` (2 example rows: forbidden_content/sword, agency_externalization/the king) | L54-56 | L112-114 | EXACT |
| Workflow branch logic (skipped→reader-sim, PASS→reader-sim, advisory→attach, FAIL→block+return step 3) | L61-68 | §4.1 L119-127 | EXACT |
| Tier gate (T1-2 blocking / T3 advisory / T4-5 N/A) | L24-28 | agent-schemas §2.2 L104-106 | EXACT |

**Verdict: PASS.** The verdict contract is carried field-for-field. Note the agent body correctly attributes it to `safety-rubric.md §4` (L36) and the tier gate to ground-truth "safety_check.md is T1-2 only" (L27) — both citations verified accurate.

**CHECK 1 overall: PASS** (no uncited or mis-traced spec claim found in the spot-checked bodies).

---

## CHECK 2 — source-fidelity §3.2 output schema documented verbatim in SKILL.md

Field-by-field comparison: `skills/source-fidelity/SKILL.md` §"Output schema" (L45-69) vs `skill-specs.md` §3.2 (L219-243).

| Field | SKILL.md line | skill-specs §3.2 line | Match |
|---|---|---|---|
| `status: OK \| ABORTED` (+ABORT comment) | L46 | L220 | EXACT |
| `metadata.work` | L48 | L222 | EXACT |
| `metadata.chapter` | L49 | L223 | EXACT |
| `metadata.source_access: FULL\|PARTIAL\|MEMORY-BASED\|NO-ACCESS` | L50 | L224 | EXACT |
| `metadata.confidence` (overall) | L51 | L225 | EXACT |
| `essentials.title {value,confidence:CERTAIN}` | L53 | L227 | EXACT |
| `essentials.chapter_title {…:PROBABLE}` | L54 | L228 | EXACT |
| `essentials.opening_sentence {…:CERTAIN}` | L55 | L229 | EXACT |
| `essentials.closing_sentence {…:CERTAIN}` | L56 | L230 | EXACT |
| `characters: - {name,role,confidence}` | L57-58 | L231-232 | EXACT |
| `events: - {seq,event,confidence}` | L59-60 | L233-234 | EXACT |
| `summary: {text,confidence:PROBABLE}` | L61 | L235 | EXACT |
| `transformation_flags.violence/death/emotional/abstract {instances,severity}` | L62-66 | L236-240 | EXACT |
| `uncertainties: - "…"` | L67-68 | L241-242 | EXACT |

All 8 top-level keys named in the check (status/metadata/essentials/characters/events/summary/transformation_flags/uncertainties) present, in the same order, with identical nested structure and identical inline confidence exemplars.

**CHECK 2 overall: PASS.** The schema is documented verbatim, not paraphrased. (The SKILL.md adds one honest editorial sentence at L42-43 — "The analyst and this skill agree on this exact contract" — which is a claim, not a schema change; it is corroborated by `analyst.md` L42-45 which enumerates the same key list. Not a fabrication.)

---

## CHECK 3 — No fabricated examples / invented behavior (tier commentary + agency)

### 3a. "Sauron was evil → Grumpy King" and the MANDATORY→OPTIONAL→FORBIDDEN ladder

- Ladder **MANDATORY (T1-2) → OPTIONAL (T3) → FORBIDDEN (T4-5)**: verified in `003-agency-externalization.md` L18-22 (mode table: 1-2 MANDATORY, 3 OPTIONAL, 4-5 FORBIDDEN). Reproduced in tier_1.md/tier_2.md/tier_3.md/tier_4.md/tier_5.md and agency.md — all consistent with the ADR. **Not invented.**
- **"Sauron was evil" → "Grumpy King, no sunshine"**: verified in `003` L51-52 examples table (`| "Sauron was evil" | "Grumpy King, no sunshine" |`). Cited in tier_1.md L23 and agency.md L48. **Not invented.**
- tier_1.md L12 claim "the original system was preschool-only (001 §Context)": verified `001` L8 ("The original framework was preschool-only"). **Accurate.**
- tier_4.md L12 claim `001` offers `"Tier 4 can be interpolated from 3+5"`: verified `001` L50 verbatim. **Accurate.**
- tier_2.md L24-25 "misses the critical Tier 2→3 transition" / "forces crude binary choices": verified `001` L26-27 verbatim. **Accurate.**
- tier_3.md "natural inflection point": verified `001` L35 ("Tier 3 is natural inflection point"). **Accurate.**

### 3b. agency.md YAML payload — "carried VERBATIM from thematic.yaml"

Compared `agency.md` L9-25 payload against the actual source `config/transformation_rules/thematic.yaml` L33-47 (read directly, not via the ADR):

| Line | agency.md | config thematic.yaml | Match |
|---|---|---|---|
| core_principle | "Badness is always a STATE or ACCIDENT, never innate." | idem (L34) | EXACT |
| tier_1 example 1 | Dark Lord, evil → Grumpy King, no sunshine | idem (L38) | EXACT |
| tier_1 example 2 | driven mad by despair → very sad, windows closed | idem (L39) | EXACT |
| tier_1 example 3 | consumed by greed → really wanted to play | idem (L40) | EXACT |
| tier_2 softening | permits_misunderstanding_as_cause | idem (L43) | EXACT |
| tier_3 / tier_4_5 modes | optional / forbidden | idem (L45,47) | EXACT |

**The agency.md payload is byte-verbatim from the config source.** The "carried VERBATIM" claim (L4-6) is truthful.

### 3c. thematic.md and character.md — "carried VERBATIM"

- `resources/thematic.md` L3-94: diffed line-by-line against `config/transformation_rules/thematic.yaml` L1-91 — **identical** (all six rule groups: violence/conflict/agency/death/villain/heroism; every key, value, and inline example preserved, no rename). The wrapper HTML comment (L1) is the only addition, as claimed.
- `resources/character.md` L3-81: diffed against `config/transformation_rules/character.yaml` L1-78 — **identical**, including the 3-step `heroism_translation.subroutine` (IDENTIFY→LOOKUP→TRANSLATE) and `special_handling` (gollum: "Silly Creature"; denethor: "Sad Leader"). **Not invented.**

### 3d. Cross-check of a subtle claim (adversarial)

agency.md L48 and tier_1.md L23 quote *"Sauron was evil" → "Grumpy King, no sunshine"* and attribute the worked example to **003**. The `003` examples table (L50-54) also lists two MORE examples ("Denethor went mad → Very sad, windows closed", "Gollum attacked → Silly creature, wanted to play"). The agency.md YAML payload uses the thematic.yaml phrasings ("driven mad by despair", "consumed by greed") — which come from the config, NOT from 003's table. This is CORRECT provenance: the YAML is tagged as carried from thematic.yaml (matches), and the prose Sauron example is tagged as from 003 (matches). No cross-contamination or invented example. **PASS.**

**CHECK 3 overall: PASS.** Every spot-checked example traces to either `config/transformation_rules/*.yaml` (byte-verbatim) or `docs/design_decisions/001|003` (accurate quotation). No fabricated example, no invented behavior found.

---

## CHECK 4 — Writer's preserved duplicate `creative-writing-craft` line is evidenced as intentional (not "fixed")

Ground-truth verification against the **actual upstream checkout** (not just the spec claim):

- Upstream source: `.dev/releases/current/0.1/creative-writing-skills/cw/agents/writer.md` L6-8 lists `creative-writing-modes`, then `creative-writing-craft` **twice** (the duplicate is genuinely upstream — grep count 3 across the three `creative-writing-*` lines).
- `sha256(upstream cw/agents/writer.md)` = `373e605b…d769290` — **matches** VENDOR.md `upstream_sha256` for `agents/writer.md` exactly.
- `sha256(laf-adaptation/agents/writer.md)` = `c1b3e12f…09534` — **matches** VENDOR.md `laf_sha256` exactly.
- The vendored `laf-adaptation/agents/writer.md` L6-12 preserves the duplicate `creative-writing-craft` (L7-8), applies the uniform prefix rewrite, and appends exactly ONE additive line `- laf-adaptation:adaptation-rules` (L12). Diff from upstream is frontmatter-only + additive, as the boundary contract requires.

Intentionality is evidenced in **three independent places**, all consistent:
1. `agent-schemas.md` §3 L133-134: "the upstream file already lists `creative-writing-craft` twice; that duplication is preserved verbatim, not 'fixed', to keep the file patch-clean."
2. `laf-adaptation/CLAUDE.md` §2 L66: "even upstream quirks (e.g. its duplicate `creative-writing-craft` skill line) are preserved verbatim, not 'fixed'."
3. `boundary-contract.md` §3.2 (referenced by agent-schemas §3 L177): `check_boundary.py` asserts the writer diff is frontmatter-only and additive — a body-normalization "fix" of the duplicate would fail Rule C.

**CHECK 4 overall: PASS.** The duplicate is a real upstream artifact, verified by hash against the vendored upstream tree, and its preservation is documented as deliberate in three places. It is correctly NOT "fixed".

---

## Additional adversarial cross-file probes (beyond the 4 required checks)

### P1 — adaptation-rules "schema drift" claim (§Key-tolerant lookup)
`adaptation-rules/SKILL.md` L27-34 claims T1-3 use `conflict_to_cooperation`/`death_euphemism`
while T5 uses `conflict_handling`/`death_handling`, cites `kb-formats.md §2.2`, and prescribes
`.get(a) or .get(b)` normalization.
- Citation verified: `kb-formats.md §2.2` (L91-102) states exactly this and shows the same
  two-line `.get()` pattern (L97-100).
- Claim verified against ground-truth data: `kb/tiers/tier_{1,2,3}.yaml` use
  `conflict_to_cooperation`+`death_euphemism`; `tier_5.yaml` uses `conflict_handling`+`death_handling`.
  The drift is REAL, not asserted. **PASS — accurate, well-cited, non-obvious.**

### P2 — analyst frontmatter `story-memory` line
Spec `agent-schemas.md §2.1` shows `creative-writing-skills:story-memory  # rewritten … at vendor time`
(pre-rewrite authored form). Shipped `analyst.md` L8 correctly shows the post-rewrite
`laf-adaptation:story-memory`. `analyst.md` is NATIVE (VENDOR.md L79: `NATIVE | — | —`), and the
`skills/story-memory` dir exists. Correct realization of spec intent. **PASS.**

## MINOR observation (not an error — recorded for completeness)
The spec §2.1 renders the analyst's story-memory skill entry with the vendor-time-rewrite comment,
which could be misread as the final shipped form. The shipped file resolves it correctly to
`laf-adaptation:story-memory`. No action needed; flagged only so a future reader does not "correct"
the shipped file back to the annotated spec form. **Severity: MINOR / informational.**

---

## Confidence Gate

### Checklist categorization
| # | Check | Status | Tool evidence |
|---|-------|--------|---------------|
| 1a | adaptation-tiers body vs skill-specs §1 | [x] VERIFIED | Read SKILL.md L9-37 + skill-specs L49-78; row-by-row table match |
| 1b | source-fidelity 5-phase vs §3.1 | [x] VERIFIED | Read SKILL.md L10-38 + skill-specs L182-212 |
| 1c | safety-verifier verdict vs safety-rubric §4 | [x] VERIFIED | Read safety-verifier.md L38-68 + safety-rubric L96-127 |
| 2 | source-fidelity §3.2 schema verbatim | [x] VERIFIED | 14-field diff SKILL.md L45-69 vs skill-specs L219-243 |
| 3a | Sauron example + ladder trace to 001/003 | [x] VERIFIED | Read 001 (L8,26,35,50), 003 (L18-22,51) |
| 3b | agency.md YAML verbatim from thematic.yaml | [x] VERIFIED | Read config/…/thematic.yaml L33-47 vs agency.md L9-25 |
| 3c | thematic.md + character.md verbatim | [x] VERIFIED | Read both config YAMLs vs both resources; line-identical |
| 3d | provenance cross-contamination probe | [x] VERIFIED | Compared 003 table vs thematic.yaml phrasings |
| 4 | writer duplicate intentional, not fixed | [x] VERIFIED | sha256sum upstream+laf writer vs VENDOR.md; grep dup count=3; 3 doc citations |
| P1 | schema-drift citation accuracy | [x] VERIFIED | grep kb-formats §2.2 + grep tier_{1,2,3,5}.yaml keys |
| P2 | analyst story-memory frontmatter | [x] VERIFIED | Read analyst.md L5-9; ls story-memory dir; grep VENDOR class |

- TOTAL = 11
- VERIFIED = 11
- UNVERIFIABLE = 0
- UNCHECKED = 0

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 18 | Grep: 6 | Glob: 0 | Bash: 8  (no web research required — all claims verified against local source-truth per Principle 6)

Threshold: confidence 100% >= 95% AND UNCHECKED == 0 → eligible for PASS. Tool calls (>=32) exceed
checklist item count (11); engagement is genuine, each call mapped to a specific check above.

## Summary
- Checks passed: 6 / 6 (4 required + 2 adversarial probes)
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor (informational): 1
- Issues fixed in-place: 0 (fix_authorization: FALSE — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR (info) | skill-specs.md §2.1 vs analyst.md | Spec renders analyst story-memory line with vendor-rewrite comment; shipped file correctly post-rewrite. No defect. | None — do NOT "correct" shipped file back to annotated spec form. |

## QA Complete
