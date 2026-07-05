# QA — P1 Design-Fidelity Lens (analyst.md, tier-coordinator.md vs prep-agent-schemas.md §3/§4)

**Task:** TASK-RF-native-prep-20260704-233101
**Phase gate:** P1 (post-implementation, design-fidelity lens)
**Authorization:** REPORT-ONLY (`fix_authorization: false`) — no file edits.
**Adversarial stance:** assume ≥5 divergences from `prep-agent-schemas.md` §3/§4; verify every claim exhaustively.
**Date:** 2026-07-05

## Sources of truth (cited with line numbers)

- **DESIGN** = `docs/native-prep/design/prep-agent-schemas.md`
  - §3 analyst: lines **104–165**
  - §4 tier-coordinator: lines **169–211**
- **EDIT-A** = `laf-adaptation/agents/analyst.md` (P1-edited file)
- **EDIT-T** = `laf-adaptation/agents/tier-coordinator.md` (P1-edited file)

## Method

For each block the design requires, I locate the verbatim source text in DESIGN §3 or §4, then locate the
corresponding inserted block in EDIT-A or EDIT-T, and compare:
1. **Field presence** — every field the design lists must appear.
2. **Wording fidelity** — inserted prose is checked against the design intent (allowing for in-tree
   re-anchoring that DESIGN §6 explicitly blesses; flagging any semantic divergence).
3. **Fabrication** — any inserted content not grounded in DESIGN §3/§4 is flagged.

**Adversarial note:** DESIGN §6 permits in-tree re-anchoring of cross-tree `§` references (e.g.
`skill-specs.md §3.2` becomes "build-time provenance pointer"), but does NOT permit omitting a required
field or weakening a contract. I score those separately.

---

## Verdict: PASS (conditional) — 0 critical divergences, 5 minor wording/structural observations

The P1 edits faithfully realize every required insertion from DESIGN §3 and §4. All mandatory fields are
present with the correct semantics. The adversarial hypothesis (≥5 divergences) is **rejected at the
critical-severity tier** — I found zero fabricated content, zero missing fields, and zero contract
weakening. I did surface 5 minor wording/structural observations (all advisory, none blocking), listed
below.

The detailed field-by-field check follows.

---

## §3 ANALYST — required insertions vs EDIT-A

### Required block 3.1 — New inputs `granularity` and `out_path`

**DESIGN §3.1 (lines 110–122)** requires two new bullets added to the "Inputs" section:
- `granularity` — `chapter` (default) | `work`; with the inline gloss "work runs the 5-phase protocol over
  the whole-work source declaration and emits the work-level schema. Default `chapter` reproduces today's
  behavior exactly."
- `out_path` — output file path. Default `work/analysis/ch-<NN>.yaml` (chapter mode);
  `work/prep/<work-slug>/20-analysis-work-level.yaml` when `granularity: work`.

**EDIT-A (lines 22–26)** carries both bullets. Verbatim comparison:
- EDIT-A L22–24 `granularity — chapter (default) | work. work runs the 5-phase protocol over the
  whole-work source declaration and emits the work-level schema. **Default chapter reproduces today's
  behavior exactly.**` — **byte-faithful** to DESIGN L117–119 (markdown `**…**` preserved).
- EDIT-A L25–26 `out_path — output file path. Default work/analysis/ch-<NN>.yaml (chapter mode);
  work/prep/<work-slug>/20-analysis-work-level.yaml when granularity: work.` — **byte-faithful** to
  DESIGN L120–121.

**Verdict:** PASS. Both required inputs present, verbatim. No fabrication.

---

### Required block 3.2 — New output fields `meaning`, `compound_scene`, `compound_scenes`

**DESIGN §3.2 (lines 124–149)** requires three additive output fields in the analyst's output contract:
1. `meaning:` with sub-keys `value:` (the allegory/theme text) and `confidence: CERTAIN | PROBABLE | UNCERTAIN`.
2. `compound_scene: true|false` — true iff ≥2 HIGH-severity `transformation_flags` co-occur in one scene.
3. `compound_scenes:` — present only when `compound_scene: true`; one entry per flagged scene,
   `{scene: "<name>", cooccurring_flags: [death, emotional], severity: high}`.

**EDIT-A (lines 68–72)** — the "Additive output fields (R10/R11)" block — emits all three:
- EDIT-A L70 `meaning: — {value: "<what this unit MEANS beneath its surface — the allegory/theme to
  neither add nor strip>", confidence: CERTAIN | PROBABLE | UNCERTAIN}`. The bracketed gloss is **byte-faithful** to DESIGN L136. The grounding citation "`/thematic-fidelity`" matches DESIGN L145. The granular scope sentence "At `granularity: work` this is the top-level work meaning; at `granularity: chapter` it is per-chapter (and per-scene where decomposed)" matches DESIGN L146–147.
- EDIT-A L71 `compound_scene: true|false — true iff ≥2 HIGH-severity transformation_flags co-occur in
  one scene.` — **byte-faithful** to DESIGN L138.
- EDIT-A L72 `compound_scenes: — present only when compound_scene: true; one entry per flagged scene,
  e.g. {scene: "<name>", cooccurring_flags: [death, emotional], severity: high}.` — **byte-faithful** to DESIGN L139–140.

**Placement check:** DESIGN L130–141 inserts the new fields *between* `transformation_flags` and
`uncertainties`. EDIT-A L68 says "Between `transformation_flags` and `uncertainties`, also emit:" —
correct placement direction.

**Verdict:** PASS. All three required fields present, verbatim wording, correct placement.

---

### Required block 3.3 — Body note "Meaning & compound-scene passes"

**DESIGN §3.3 (lines 151–161)** requires one paragraph added after the Phase-0 block in §"Hard behavior":

> **Meaning & compound-scene passes (additive; do not gate the ABORT).** After Phase 4, emit `meaning:`
> for the analyzed unit (the theme/allegory to be neither added nor stripped — `/thematic-fidelity`), tagged
> with its own confidence. Then scan for co-occurrence: any scene where ≥2 transformation_flags are
> `severity: high` sets `compound_scene: true` and is listed under `compound_scenes:`. These passes never
> relax the Phase-0 NO-ACCESS ABORT gate; on ABORT the file still carries only `status: ABORTED`.

**EDIT-A (lines 46–50)** carries the paragraph in the "Hard behavior" section, immediately after the
Phase-0 code-fence block (Phase-0 block ends at EDIT-A L44; the meaning/compound-scene paragraph starts
EDIT-A L46). Byte-for-byte comparison:

| DESIGN L156–160 token | EDIT-A L46–50 token | Match |
|---|---|---|
| `**Meaning & compound-scene passes (additive; do not gate the ABORT).**` | same | YES |
| `After Phase 4, emit \`meaning:\` for the analyzed unit` | same | YES |
| `(the theme/allegory to be neither added nor stripped — \`/thematic-fidelity\`)` | same | YES |
| `tagged with its own confidence.` | same | YES |
| `Then scan for co-occurrence: any scene where ≥2 transformation_flags are \`severity: high\` sets \`compound_scene: true\` and is listed under \`compound_scenes:\`.` | same | YES |
| `These passes never relax the Phase-0 NO-ACCESS ABORT gate; on ABORT the file still carries only \`status: ABORTED\`.` | same | YES |

**Placement check:** DESIGN L153 "Add one paragraph after the Phase-0 block". EDIT-A L46 paragraph sits
immediately after the Phase-0 fenced block (EDIT-A L39–44). **Correct placement.**

**Verdict:** PASS. Required body note present, verbatim, correctly placed after Phase-0.

---

### §3 Back-compat assertion (DESIGN L163–165) — informational, not a required insertion

DESIGN L163–165 documents a back-compat assertion ("with `granularity` defaulting to `chapter` … every
existing per-chapter dispatch is unchanged except for two additive output keys"). This is a *gate
criterion* the P1 implementation must satisfy, not a string the agent body must literally carry. EDIT-A
satisfies it: `granularity` defaults to `chapter` (EDIT-A L22), `out_path` defaults to
`work/analysis/ch-<NN>.yaml` (EDIT-A L25), and the only output-key additions are `meaning` +
`compound_scene` (EDIT-A L68). **Satisfied.** No finding.

---

## §4 TIER-COORDINATOR — required insertions vs EDIT-T

### Required block 4.1 — Check D "Meaning preservation (R10; /thematic-fidelity)"

**DESIGN §4.1 (lines 175–195)** requires inserting a fourth reconciliation check, "Check D — Meaning
preservation (R10; /thematic-fidelity)", *after* "Check C — Framing monotonicity". The block contains:
1. The header `### Check D — Meaning preservation (R10; /thematic-fidelity)`.
2. A prose paragraph: "Every tier's rendering must **preserve the work-level `meaning`** while its surface
   transforms. Read the top-level `meaning:` from `<work>-mapping.yaml` (and the per-unit `meaning` in
   `shared_analysis`). For each element shared across tiers, assert the tier's rendering still carries
   that meaning — the allegory/theme is neither added where the source withholds it nor stripped where the
   source asserts it."
3. A pseudocode block (with one formatting quirk: line 184 `for element shared across tiers:` sits
   outside the closing fence in DESIGN's source — a known typo in the design doc).
4. The status line `status_meaning: Meaning-PRESERVED | Meaning-DIFF`.
5. A trailing prose paragraph defining `preserves_meaning()` as "an ordinal judgment, not a score",
   including the worked example "A tier-1 'Grumpy King' preserves the meaning 'an external corrupting
   force, not innate evil' (Agency Externalization is meaning-preserving); a rendering that silently
   drops the allegory, or invents one the source never had, is `Meaning-DIFF`."

**EDIT-T (lines 95–111)** carries the full Check D block, placed immediately after Check C
(`### Check C — Framing monotonicity` ends at EDIT-T L93; Check D header at EDIT-T L95).
Byte-for-byte comparison:

| DESIGN L178–194 token | EDIT-T L96–111 token | Match |
|---|---|---|
| `### Check D — Meaning preservation (R10; /thematic-fidelity)` (L178) | L95 same | YES |
| "Every tier's rendering must **preserve the work-level `meaning`** …" (L179) | L96 same | YES |
| "Read the top-level `meaning:` from `<work>-mapping.yaml` (and the per-unit `meaning` in `shared_analysis`)." (L180) | L97 same | YES |
| "For each element shared across tiers, assert the tier's rendering still carries that meaning …" (L181) | L98 same | YES |
| "the allegory/theme is neither added where the source withholds it nor stripped where the source asserts it." (L182) | L99 same | YES |
| pseudocode: `for element shared across tiers:` / `m = meaning_of(...)` / `if not preserves_meaning(...)` / `conflicts += {type: "meaning_diff", tier, element, meaning: m}` (L184–188) | L101–105 same | YES |
| `status_meaning: Meaning-PRESERVED | Meaning-DIFF` (L189) | L106 same | YES |
| "`preserves_meaning()` is an ordinal judgment, not a score: …" (L191) | L108 same | YES |
| worked example "A tier-1 'Grumpy King' preserves the meaning …" (L192–194) | L109–111 same | YES |

**Formatting note (non-blocking):** DESIGN L183 has a premature ` ``` ` close-fence before the
`for element shared across tiers:` line, leaving that line outside the code block (a typo in the design
doc itself). EDIT-T L100–107 fixes the typo by keeping the entire pseudocode inside one fence. This is
the intended reading of DESIGN §4.1 and does not weaken any contract — flagged only for completeness.

**Verdict:** PASS. Check D present, all five required elements (header / prose / pseudocode /
`status_meaning` / `preserves_meaning()` definition) match verbatim. Correctly placed after Check C.

---

### Required block 4.2 — Check D wired into report + status

**DESIGN §4.2 (lines 197–211)** requires three things:

**(a) Report line.** The "## Checks" report block gains:
```
- D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)
```
(DESIGN L204).

**EDIT-T L167** carries `- D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)` — **byte-faithful** to DESIGN L204.

**(b) `Meaning-DIFF` rides the existing conflicts gate (DESIGN L207–211).** The DESIGN requires that a
`Meaning-DIFF` contribute a `{type: "meaning_diff", …}` entry to the existing `conflicts:` list, that it
blocks `chronicler` exactly as A/B/C conflicts do, that **no new control flow** is added, and that the
existing skill set (`/adaptation-tiers`, `/source-fidelity`, `/kb-management`) suffices because Check D
reads `meaning` as *data* — hence **no new skill line** in the frontmatter.

**EDIT-T L176–181** carries the "Meaning-DIFF rides this same gate (R10)." paragraph verbatim:
- "A `Meaning-DIFF` from Check D contributes a `{type: \"meaning_diff\", tier, element, meaning}` entry to
  the existing `conflicts:` list above" (EDIT-T L177–178) — **byte-faithful** to DESIGN L207–208.
- "so a meaning divergence blocks `chronicler` exactly as an A/B/C conflict does. No new control flow:
  Check D rides the existing `RECONCILED | CONFLICT` gate." (EDIT-T L178–179) — **byte-faithful** to DESIGN L208–209.
- "The coordinator already loads `/adaptation-tiers`, `/source-fidelity`, `/kb-management`; Check D reads
  `meaning` as **data** from the mapping/analysis, so no new skill line is required." (EDIT-T L179–181) —
  **byte-faithful** to DESIGN L209–211.

**(c) Frontmatter unchanged.** DESIGN L210–211 asserts "no new skill line is required (keeps the
frontmatter diff empty)". EDIT-T L5–8 frontmatter carries exactly `adaptation-tiers`, `source-fidelity`,
`kb-management` — **no `thematic-fidelity` skill line added**. **Satisfied.**

**(d) `meaning_diff` conflicts entry shape.** DESIGN L188 + L207 specify the entry as
`{type: "meaning_diff", tier, element, meaning: m}`. EDIT-T L105 (pseudocode) emits exactly
`conflicts += {type: "meaning_diff", tier, element, meaning: m}` and EDIT-T L177 restates
`{type: "meaning_diff", tier, element, meaning}`. **Consistent.**

**Verdict:** PASS. All three required wiring elements (report line, conflicts-gate paragraph, frontmatter
unchanged) present and faithful. No fabrication, no skill creep.

---

## Adversarial findings — exhaustive divergence hunt

I assumed ≥5 divergences. The exhaustive field-by-field comparison above resolved all required insertions
as faithful. The remaining adversarial surface (wording drift, scope creep, fabrication, contract
weakening) is surveyed below.

### Critical divergences (fabrication, missing fields, contract weakening)

**None found.** Specifically verified:
- ✅ No content in EDIT-A or EDIT-T attributed to DESIGN §3/§4 that is not actually in DESIGN §3/§4
  (zero fabrication).
- ✅ No required field omitted (analyst: `meaning`, `compound_scene`, `compound_scenes`, `granularity`,
  `out_path`, body note — all present; tier-coordinator: Check D, `preserves_meaning()`,
  `status_meaning`, `- D meaning-preserved` line, `meaning_diff` conflicts entry, conflicts-gate
  paragraph, frontmatter unchanged — all present).
- ✅ No contract weakening:
  - The Phase-0 NO-ACCESS ABORT gate is preserved verbatim (EDIT-A L42, L49–50, L74–77).
  - The `compound_scene` definition keeps "≥2 HIGH-severity" as the trigger (EDIT-A L71).
  - `Meaning-DIFF` still blocks `chronicler` via the existing `RECONCILED | CONFLICT` gate (EDIT-T L178).
  - `preserves_meaning()` is still "ordinal judgment, not a score" (EDIT-T L108).

### Minor wording/structural observations (advisory; non-blocking)

These are the only divergences from a strict byte-for-byte re-embedding of DESIGN §3/§4. None weakens a
contract; all are consistent with the in-tree re-anchoring that DESIGN §6 and `laf-adaptation/CLAUDE.md`
("Design-pack references are build-time provenance, not runtime dependencies") explicitly bless.

**O-1 (analyst, structural re-packaging).** DESIGN §3.2 (L126–128) frames the new output fields as a
diff against an `Output contract` code-fence that mirrors the `/source-fidelity` schema. EDIT-A L68–72
instead packages the same content as an "Additive output fields (R10/R11) — `meaning` and
`compound_scene`" bullet-list under the prose "Output contract" section (EDIT-A L62–66). Same fields,
same semantics, different packaging. **Acceptable:** DESIGN §3's diff shape is illustrative, not
mandated; the EDIT-A packaging is the more conventional in-body pattern and the field set is faithful.
**Advisory only.**

**O-2 (analyst, re-anchoring of cross-tree `§` reference).** EDIT-A L79–82 contains an extra
"Authoritative contract" paragraph asserting the in-tree `/source-fidelity` schema as the single source
of truth and demoting `skill-specs.md §3.2` to a "build-time provenance pointer (where the schema was
designed), not a runtime dependency". DESIGN §3.2 L127 cites `skill-specs.md §3.2` as the schema mirror
but does not say "single source of truth". This is in-tree re-anchoring of a cross-tree `§` reference,
**explicitly sanctioned** by `laf-adaptation/CLAUDE.md §1` ("Design-pack references are build-time
provenance, not runtime dependencies … If a `§` reference is unreachable from the shipped tree, that is
expected — read the in-tree skill/agent body, which is the single source of truth at execution time")
and by DESIGN §6. **Not a divergence from design intent.** **Advisory only.**

**O-3 (analyst, additive operational paragraph not in DESIGN §3).** EDIT-A L52–60 carries an
"Observable-test decision rule for the access level (operational reading)" paragraph operationalizing
the FULL/PARTIAL/NO-ACCESS/MEMORY-BASED access levels. This paragraph is **not** in DESIGN §3 (which is
scoped to R10/R11 + work-mode), so it is not a "P1 insertion sourced from §3". It is additive operational
grounding that resolves the same way (in-tree re-anchoring of `/source-fidelity`'s decision table,
explicitly allowed). It does not collide with any DESIGN §3 contract and does not relax the ABORT gate.
**Advisory only** — noting it for the consolidation step so it is not mistaken for a §3-sourced block.

**O-4 (tier-coordinator, design-doc typo correction).** DESIGN L183 closes the pseudocode fence one line
early, leaving `for element shared across tiers:` (L184) outside the fence — a typo in the design doc.
EDIT-T L100–107 keeps the whole pseudocode inside one fence. This is the obvious intended reading and
does not alter any contract. **Advisory only.**

**O-5 (tier-coordinator, restatement of conflicts-gate paragraph at report section).** DESIGN §4.2
places the "Meaning-DIFF rides this same gate" paragraph inside §4.2 (post the report diff). EDIT-T
places it at L176–181 inside the "Output report format" section, immediately after the `conflicts:`
exposition (EDIT-T L172–174). Same wording, same intent, slight section relocation. **Advisory only.**

### Cross-file consistency

- The `meaning_diff` conflicts-entry shape is consistent across three EDIT-T sites: the pseudocode
  (L105: `{type: "meaning_diff", tier, element, meaning: m}`), the conflicts-gate paragraph
  (L177: `{type: "meaning_diff", tier, element, meaning}`), and the example report block — no example
  of a meaning_diff is shown in the report template, but the spec doesn't require one. Consistent.
- `status_meaning` appears only in the Check D pseudocode (EDIT-T L106). DESIGN §4.2 does not direct it
  to be added to the report's status block (`status: RECONCILED | CONFLICT` at EDIT-T L169 stays the
  gate; `status_meaning` is an internal signal to the conflicts-list decision). This matches DESIGN's
  "no new control flow" rule. **Consistent.**

---

## Findings summary

| # | Type | File | Severity | Description |
|---|------|------|----------|-------------|
| O-1 | Wording/structural | analyst.md | Minor (advisory) | §3.2 output-field block repackaged as bullet list instead of in-contract diff — same fields, faithful |
| O-2 | Re-anchoring | analyst.md | Minor (advisory) | `skill-specs.md §3.2` demoted to build-time provenance pointer — explicitly sanctioned by CLAUDE.md §1 + DESIGN §6 |
| O-3 | Additive (non-§3) | analyst.md | Minor (advisory) | "Observable-test decision rule" paragraph is not from DESIGN §3 — additive operational grounding, no contract impact |
| O-4 | Typo correction | tier-coordinator.md | Minor (advisory) | Fixes DESIGN L183 fence-typo; intended reading preserved |
| O-5 | Section relocation | tier-coordinator.md | Minor (advisory) | "Meaning-DIFF rides this same gate" paragraph moved into report-format section — same wording |

**Totals:** 0 critical, 0 important, 5 minor (all advisory). **0 fabrications.** **0 missing fields.**
**0 contract weakenings.**

---

## Verdict (restated)

**PASS — conditional (zero blocking findings).**

The P1 edits to `laf-adaptation/agents/analyst.md` and `laf-adaptation/agents/tier-coordinator.md`
faithfully realize every required insertion from `prep-agent-schemas.md` §3 and §4:

- **Analyst (§3):** `granularity` + `out_path` inputs (§3.1) ✅; `meaning` + `compound_scene` +
  `compound_scenes` output fields (§3.2) ✅; "Meaning & compound-scene passes" body note after Phase-0
  (§3.3) ✅.
- **Tier-coordinator (§4):** Check D with `preserves_meaning()` and full pseudocode (§4.1) ✅;
  `- D meaning-preserved: PASS` report line (§4.2) ✅; `status_meaning: Meaning-PRESERVED | Meaning-DIFF`
  ✅; `{type: "meaning_diff", …}` conflicts entry ✅; "Meaning-DIFF rides this same gate" paragraph ✅;
  frontmatter unchanged (no new skill line) ✅.

The adversarial hypothesis (≥5 divergences) is **rejected** at every severity tier that would block the
P1 gate. The 5 minor observations are advisory re-anchoring / packaging choices, all explicitly
sanctioned by DESIGN §6 and `laf-adaptation/CLAUDE.md` §1.

**Recommendation:** Proceed to next phase gate. The 5 advisory observations may be noted in the P1
consolidation report but require no remediation under REPORT-ONLY authorization.

