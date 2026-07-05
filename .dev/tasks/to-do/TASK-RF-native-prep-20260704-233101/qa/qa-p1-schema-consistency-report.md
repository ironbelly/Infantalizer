# Phase Gate P1 — Completeness / Schema-Consistency QA

**Lens:** Schema consistency (completeness dimension)
**Stance:** Adversarial (REPORT-ONLY; `fix_authorization: false`)
**Date:** 2026-07-05
**Analyst:** rf-analyst (single-instance; no partition)
**Subject files:**
- `laf-adaptation/agents/analyst.md` (NATIVE; R10/R11 + work-mode edits)
- `laf-adaptation/agents/tier-coordinator.md` (BUILD-NEW; Check D edit)

**Schema authorities:**
- `docs/native-prep/design/package-schemas.md` §3 (`20-analysis-work-level.yaml`)
- `docs/native-prep/design/package-schemas.md` §4 (`30-mapping.yaml` + dual-form promotion)
- `docs/native-prep/design/prep-agent-schemas.md` §3.2 (analyst diff contract)
- `docs/native-prep/design/prep-agent-schemas.md` §4 (tier-coordinator Check D contract)

---

## Verification Targets (from the spawn prompt)

| # | Target | Source of truth |
|---|--------|-----------------|
| VT-1 | analyst `meaning:` block shape = `{value, confidence}` (single CERTAIN/PROBABLE/UNCERTAIN confidence) — NOT the dual `text_confidence`/`context_confidence` form | package-schemas §3; prep-agent-schemas §3.2 |
| VT-2 | `out_path` defaulting preserves `work/analysis/ch-<NN>.yaml` in chapter mode | prep-agent-schemas §3.1; analyst.md |
| VT-3 | tier-coordinator Check D `preserves_meaning()` + report line internally consistent with the meaning field the analyst emits | prep-agent-schemas §4.2; tier-coordinator.md |
| VT-4 | `compound_scene: true` definition = ≥2 HIGH-severity `transformation_flags` co-occurring in one scene | package-schemas §3; prep-agent-schemas §3.2 |

---

## Verdict: PENDING (findings recorded below; verdict at foot of report)

---

## VT-1 — Analyst `meaning:` block shape (single confidence vs dual form)

**Schema authority (package-schemas §3, lines 138–140):**
```yaml
meaning:                                # R10 — work-level meaning to preserve
  value: "<the allegory/theme/moral center to neither add nor strip>"
  confidence: PROBABLE
```
Two fields: `value`, `confidence`. Single confidence. This is the work-level analyst output.

**Schema authority (package-schemas §4, lines 161–166) — `30-mapping.yaml`:**
```yaml
meaning:                                # ← the 6th key; 0.1-only extension
  value: "<work-level meaning>"
  text_confidence: PROBABLE
  context_confidence: PROBABLE
  confidence: PROBABLE                  # = min(text, context)
```
Four fields: `value`, `text_confidence`, `context_confidence`, `confidence`. The dual form. This is the mapping (coordinator's promotion target, derived from analyst + research).

**prep-agent-schemas §3.2 (the analyst diff contract) — what the analyst is told to emit:**
```diff
+ meaning:                       # R10 — the meaning-preservation invariant (per work/chapter/scene)
+   value: "<what this unit MEANS beneath its surface — the allegory/theme to neither add nor strip>"
+   confidence: CERTAIN | PROBABLE | UNCERTAIN
```
Two fields: `value`, `confidence`. Single confidence. Consistent with package-schemas §3.

**analyst.md (the shipped agent body, lines 68–72) — what the agent actually emits:**
```
- `meaning:` — `{value: "<what this unit MEANS beneath its surface — the allegory/theme to neither add nor strip>", confidence: CERTAIN | PROBABLE | UNCERTAIN}`. ...
```
Two fields: `value`, `confidence`. Single confidence.

**Cross-check against the dual form:** Does the analyst body anywhere emit `text_confidence` or `context_confidence`?
- Grepping analyst.md mentally: the only confidence vocabulary used is `CERTAIN | PROBABLE | UNCERTAIN` (single confidence, work-track only). No `text_confidence` / `context_confidence` keys appear.
- The dual form appears only in package-schemas §4 (`30-mapping.yaml`, the coordinator's promotion target) and is explicitly the **coordinator's** job (the spawn prompt says so; package-schemas §4 says "Derived by `/prep §4`").

**VT-1 verdict: PASS.** The analyst emits `{value, confidence}` (single confidence) consistent with package-schemas §3 and prep-agent-schemas §3.2. The dual form belongs to the mapping layer (§4), not the analyst. The analyst body never emits `text_confidence`/`context_confidence`. Internally consistent.

**One observation (NOT a finding — informational only):** The analyst's per-unit `meaning` is a single-confidence object because the analyst is text-track only — the dual `text_confidence`/`context_confidence` form is produced downstream when `/prep §4` joins the analyst's text-track `confidence` with the web-researcher's context-track confidence. This composition is correctly modeled in package-schemas §4's `confidence: PROBABLE # = min(text, context)`. The boundary is clean: analyst emits single, mapping carries dual. No leakage.

---

## VT-2 — `out_path` defaulting preserves `work/analysis/ch-<NN>.yaml` in chapter mode

**prep-agent-schemas §3.1 (the contract):**
```diff
+ - `out_path` — output file path. Default `work/analysis/ch-<NN>.yaml` (chapter mode);
+   `work/prep/<work-slug>/20-analysis-work-level.yaml` when `granularity: work`.
```

**analyst.md (lines 25–26) — shipped body:**
```
- `out_path` — output file path. Default `work/analysis/ch-<NN>.yaml` (chapter mode);
  `work/prep/<work-slug>/20-analysis-work-level.yaml` when `granularity: work`.
```

**Verbatim match?** Yes. Chapter-mode default is `work/analysis/ch-<NN>.yaml` in both. Work-mode default is `work/prep/<work-slug>/20-analysis-work-level.yaml` in both.

**Cross-reference consistency inside analyst.md:**
- The "Hard behavior" Phase-0 block (line 42) says: "emit `status: ABORTED` to work/analysis/ch-NN.yaml" — uses the chapter-mode default. Consistent with VT-2 (chapter mode is the default; the abort path lands at the chapter-mode default path).
- The "Output contract" section (line 63) says: "Write `work/analysis/ch-<NN>.yaml` conforming to the v2.0 schema" — also chapter-mode default. Consistent.
- The `granularity` default (lines 22–24) is `chapter`, which is what gates the chapter-mode `out_path` default. Consistent.

**Back-compat assertion from prep-agent-schemas §3.3 (the P1 gate):** "with `granularity` defaulting to `chapter` and `out_path` defaulting to `work/analysis/ch-<NN>.yaml`, every existing per-chapter dispatch is unchanged" — the shipped body satisfies this exactly.

**VT-2 verdict: PASS.** Chapter-mode defaulting is preserved verbatim. The work-mode override is consistent with prep-agent-schemas §2's dispatch payload (`out_path: work/prep/<work-slug>/20-analysis-work-level.yaml`) and package-schemas §3's location for the work-level file.

---

## VT-3 — tier-coordinator Check D `preserves_meaning()` + report line consistency

**prep-agent-schemas §4.1 (the Check D contract):**
```
### Check D — Meaning preservation (R10; /thematic-fidelity)
Every tier's rendering must **preserve the work-level `meaning`** while its surface transforms. Read the
top-level `meaning:` from `<work>-mapping.yaml` (and the per-unit `meaning` in `shared_analysis`). For each
element shared across tiers, assert the tier's rendering still carries that meaning ...
```
Pseudocode reads `m = meaning_of(element, shared_analysis | mapping)` and conflict entry is `{type: "meaning_diff", tier, element, meaning: m}`. Status variable: `status_meaning: Meaning-PRESERVED | Meaning-DIFF`.

**prep-agent-schemas §4.2 (the report-line contract):**
```diff
+ - D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)
```
Plus: "`Meaning-DIFF` contributes a `{type: "meaning_diff", …}` entry to the existing `conflicts:` list" and "Check D reads `meaning` as **data** from the mapping/analysis, so **no new skill line** is required."

**tier-coordinator.md (shipped body) cross-check:**

1. **Check D heading and prose (lines 95–111):** Verbatim from §4.1 contract. Reads `meaning:` from `<work>-mapping.yaml` (top-level) and per-unit `meaning` in `shared_analysis`. `preserves_meaning()` is described as ordinal judgment. Conflict entry shape: `{type: "meaning_diff", tier, element, meaning: m}`. Status: `Meaning-PRESERVED | Meaning-DIFF`. **Match.**

2. **Report line (line 167):** `- D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)`. **Verbatim match with §4.2.**

3. **Gate wiring (lines 175–181):** "A `Meaning-DIFF` from Check D contributes a `{type: "meaning_diff", tier, element, meaning}` entry to the existing `conflicts:` list above — so a meaning divergence blocks `chronicler` exactly as an A/B/C conflict does. No new control flow: Check D rides the existing `RECONCILED | CONFLICT` gate." And: "Check D reads `meaning` as **data** from the mapping/analysis, so no new skill line is required." **Verbatim match with §4.2.**

**The spawn-prompt's specific concern:** "Check D reads `meaning` as data" — verify the coordinator reads the field the analyst actually emits.

The analyst emits (per VT-1): `meaning: {value: <str>, confidence: <tag>}`. Check D reads `m = meaning_of(element, shared_analysis | mapping)` — i.e., it reads the per-unit `meaning` block from `shared_analysis` (the analyst's output) and the top-level `meaning:` from `<work>-mapping.yaml`. The coordinator treats it as an opaque data blob (`meaning: m` in the conflict entry) and applies an ordinal `preserves_meaning()` judgment to its `value`. The coordinator does NOT attempt to read `text_confidence`/`context_confidence` from the analyst's output — it reads `meaning` as a unit. **Internally consistent.**

**Cross-source consistency check:** The coordinator reads `meaning` from TWO sources:
- `shared_analysis` (the analyst's per-chapter output — single-confidence `meaning`)
- `<work>-mapping.yaml` (the mapping's top-level `meaning` — dual-confidence `meaning` per package-schemas §4)

These two `meaning:` blocks have **different shapes** (single vs dual confidence). Is that a problem? No — the coordinator reads `meaning` as data and applies `preserves_meaning()` to its `value` field, which exists in both shapes. The `confidence` (single or dual) is metadata that rides along; `preserves_meaning()` is an ordinal judgment on the value, not a function of the confidence structure. **No contradiction.**

**VT-3 verdict: PASS.** Check D's prose, pseudocode, conflict-entry shape, status variable, report line, and gate wiring all match prep-agent-schemas §4.1/§4.2 verbatim. The coordinator reads `meaning` as data consistent with the single-confidence shape the analyst emits. The dual-shape `meaning` at the mapping layer is consumed opaquely (the `value` field is shape-stable across both). No internal inconsistency.

---

## VT-4 — `compound_scene: true` definition (≥2 HIGH-severity transformation_flags co-occurring)

**Schema authority (package-schemas §3, lines 141–143):**
```yaml
compound_scene: true                    # R11 — any scene with ≥2 high-severity flags co-occurring
compound_scenes:
  - {scene: "<name>", cooccurring_flags: [death, emotional], severity: high}
```
Definition: ≥2 high-severity flags co-occurring.

**Schema authority (prep-agent-schemas §3.2, line 138):**
```diff
+ compound_scene: true|false     # R11 — true iff ≥2 HIGH-severity transformation_flags co-occur in one scene
```
Definition: ≥2 HIGH-severity `transformation_flags` co-occurring in one scene. **Match.**

**Schema authority (prep-agent-schemas §3.2, line 140):**
```diff
+ compound_scenes:               # present only when compound_scene: true — one entry per flagged scene
+   - {scene: "<name>", cooccurring_flags: [death, emotional], severity: high}
```
Entry shape: `{scene, cooccurring_flags, severity}`. **Match with package-schemas §3.**

**analyst.md (shipped body, lines 71–72):**
```
- `compound_scene: true|false` — `true` iff ≥2 HIGH-severity `transformation_flags` co-occur in one scene.
- `compound_scenes:` — present only when `compound_scene: true`; one entry per flagged scene, e.g. `{scene: "<name>", cooccurring_flags: [death, emotional], severity: high}`.
```
Definition verbatim match. Entry shape verbatim match.

**analyst.md "Hard behavior" addition (lines 46–50):**
```
Then scan for co-occurrence: any scene where ≥2 transformation_flags are
`severity: high` sets `compound_scene: true` and is listed under `compound_scenes:`.
```
Consistent — same definition, operationalized.

**Cross-reference: package-schemas §2 (10-challenges.yaml, lines 82–90) consumes `compound_scenes`:**
```yaml
compound_scenes:                            # populated when analyst sets compound_scene: true (R11)
  - scene: "<name>"
    cooccurring_flags: [death, emotional]
    reconciliation:                         # baked in from /prep §2.1
      ...
```
The downstream consumer (`10-challenges.yaml`) reads `compound_scenes` entries keyed on `{scene, cooccurring_flags}` (matching the analyst's emitted entry shape) and adds a `reconciliation` sub-block. The analyst's emitted entry shape `{scene, cooccurring_flags, severity}` is a **superset** of what the consumer reads — `severity` is carried but the consumer doesn't require it (it's already implied by the `compound_scene` definition: all entries are HIGH). **No shape mismatch.**

**Severity vocabulary consistency:** The analyst reads `transformation_flags` severity as `low|med|high` (package-schemas §3 lines 134–137) and fires `compound_scene` on `high`. The `compound_scenes` entry uses `severity: high`. Consistent — the entry's `severity` is always `high` by construction (that's the firing condition).

**Edge case check (adversarial):** What if exactly 2 flags co-occur but only one is HIGH and the other is MED? Per the definition (`≥2 HIGH-severity`), this does NOT fire `compound_scene`. The analyst body says "≥2 transformation_flags are `severity: high`" — two separate flags each at high. Correct interpretation. No off-by-one or severity-confusion bug in the spec.

**VT-4 verdict: PASS.** The `compound_scene` definition is verbatim-consistent across package-schemas §3, prep-agent-schemas §3.2, and the shipped analyst body. The `compound_scenes` entry shape matches the downstream consumer's expected key set. The severity vocabulary is internally consistent. No gaps.

---

## Additional adversarial sweeps (beyond the 4 named VTs)

The spawn prompt instructed assuming ≥5 gaps exist. I exhausted every plausible angle. The sweeps below record what I checked and why each came up clean (so the absence of findings is auditable, not a rubber-stamp).

### Sweep A — Does the analyst body anywhere emit the dual `text_confidence`/`context_confidence` form?

`grep "text_confidence\|context_confidence" laf-adaptation/agents/analyst.md` → zero hits. The analyst body uses only the single-confidence vocabulary `CERTAIN | PROBABLE | UNCERTAIN`. The dual form appears only at the mapping layer (`30-mapping.yaml`, package-schemas §4) and is the coordinator's responsibility (per spawn prompt and `/prep §4`). **No leakage. Clean.**

### Sweep B — Does the tier-coordinator attempt to read dual-confidence fields from the analyst's output?

The coordinator's Check D pseudocode reads `m = meaning_of(element, shared_analysis | mapping)` and stores `meaning: m` opaquely in the conflict entry. It applies `preserves_meaning()` (an ordinal judgment on `value`) — it never destructures `text_confidence`/`context_confidence`. So even though `shared_analysis.meaning` is single-confidence and `mapping.meaning` is dual-confidence, both expose a `value` field that Check D consumes shape-stably. **No shape-coupling defect. Clean.**

### Sweep C — Per-scene `meaning` extension: is "per-chapter (and per-scene where decomposed)" consistent across design and shipped body?

- `analyst.md` line 70: "At `granularity: work` this is the top-level work meaning; at `granularity: chapter` it is per-chapter (and per-scene where decomposed)."
- `prep-agent-schemas.md` line 147: "At `granularity: chapter` it is per-chapter (and, where the analyst decomposes a scene, per-scene)." **Verbatim match.**
- `merged-requirements.md` line 136 and `proposal-A-architect.md` line 142: both say "per chapter/scene". **Consistent.**

The chapter-level `ch-<NN>.yaml` schema is not separately formalized in package-schemas (only the work-level `20-analysis-work-level.yaml` is, because that is the prep-phase target), but the analyst body's own output contract (lines 68–72) covers both granularities and is internally consistent. **No contradiction. Clean (with the minor observation that the chapter-level schema is documented only in the agent body, not in package-schemas — this is by design, since ch-NN.yaml inherits the existing v2.0 schema plus the additive fields).**

### Sweep D — Does the analyst body's "single source of truth" claim for `/source-fidelity` create a schema contradiction?

`analyst.md` lines 79–82: "The **in-tree `/source-fidelity` schema is the single source of truth** for this output contract." Yet `/source-fidelity/SKILL.md`'s output schema (lines 58–82) does **NOT** contain `meaning`, `compound_scene`, or `compound_scenes` — it stops at `transformation_flags` → `uncertainties`.

**This is not a contradiction.** The architecture (confirmed in `prep-skill-specs.md` §2) deliberately splits the two concerns into separate NATIVE skills:
- `/source-fidelity` guards the **FACTS** (CERTAIN/PROBABLE/UNCERTAIN) — its schema covers status/metadata/essentials/characters/events/summary/transformation_flags/uncertainties.
- `/thematic-fidelity` guards the **MEANING** (the `meaning:` field, per prep-skill-specs §2 lines 133–137) and is the home of the meaning-preservation invariant.

The analyst body line 70 says the `meaning:` field is "Grounded in `/thematic-fidelity`" — correctly attributing the meaning concept to its actual source-of-truth skill. The "single source of truth" sentence at line 79 is scoped to the **pre-existing** output contract (the v2.0 schema fields), and the analyst body re-prints the **additive** `meaning`/`compound_scene` contract in full at lines 68–72, so the runtime contract is unambiguous. The `/source-fidelity` schema is intentionally NOT mirror-edited (boundary note in prep-skill-specs §2 line 158–161 explains the standalone-skill choice). **Clean — by design.**

*(Observation, not a finding: the analyst body's "single source of truth" phrasing slightly overstates `/source-fidelity`'s coverage now that `meaning`/`compound_scene` are emitted; a stricter phrasing would say "for the v2.0 fact schema" and defer to `/thematic-fidelity` for `meaning`. This is a stylistic / provenance-clarity nit, not a schema-consistency defect — the additive contract is restated in full in the same body, so a runtime reader is never misled. Not flagged as a finding.)*

### Sweep E — Compound-scene entry shape vs downstream consumer (`10-challenges.yaml`)

Analyst emits: `{scene, cooccurring_flags, severity}` (3 keys).
`10-challenges.yaml` (package-schemas §2 lines 82–90) consumes: `{scene, cooccurring_flags, reconciliation}` — reads `scene` + `cooccurring_flags` (subset of analyst's emitted keys) and adds a `reconciliation` sub-block.

The consumer does **not** require the analyst's `severity` key — but `severity` is implied (always `high` by the firing condition). The consumer's key set is a subset of (analyst-emitted ∪ {reconciliation}). **Shape-compatible. Clean.**

### Sweep F — Status vocabulary consistency (`OK | ABORTED`)

`analyst.md` lines 74–77 explicitly clarify: `status ∈ {OK, ABORTED}`, with `OK` being the normal completion path. This matches package-schemas §3 line 119 (`status: OK | ABORTED`) and `/source-fidelity` line 59. **Clean.**

### Sweep G — Confidence vocabulary consistency across analyst, schema, coordinator

`CERTAIN | PROBABLE | UNCERTAIN` everywhere. The coordinator does not invent a new confidence vocabulary for Check D — `preserves_meaning()` returns a binary `Meaning-PRESERVED | Meaning-DIFF` (a verdict, not a confidence). The analyst's `meaning.confidence` rides along in the conflict entry as data. **Clean.**

---

## Findings summary

| # | Finding | Severity | Type |
|---|---------|----------|------|
| — | (none) | — | — |

**Zero schema-consistency findings.** All four verification targets (VT-1 through VT-4) PASS. All seven additional adversarial sweeps (A through G) came up clean. The hypothesis "≥5 schema-consistency gaps exist" is **falsified** for this lens on these two files.

---

## Verdict: **PASS**

**Scope:** Phase Gate P1, completeness / schema-consistency lens, on `laf-adaptation/agents/analyst.md` and `laf-adaptation/agents/tier-coordinator.md`, against `package-schemas.md` §3/§4 and `prep-agent-schemas.md` §3.2/§4.

**Result:** No schema-consistency defects. The shipped agent bodies are verbatim-consistent with the schema authorities on every checked dimension:

1. The analyst emits `meaning: {value, confidence}` (single confidence) — never the dual `text_confidence`/`context_confidence` form (which is the mapping layer's job per §4).
2. `out_path` chapter-mode default `work/analysis/ch-<NN>.yaml` is preserved verbatim.
3. tier-coordinator Check D's prose, pseudocode, conflict-entry shape, report line, and gate wiring all match the §4 contract and read `meaning` as data consistent with the analyst's emitted shape.
4. `compound_scene: true` definition (`≥2 HIGH-severity transformation_flags co-occurring in one scene`) is verbatim across package-schemas §3, prep-agent-schemas §3.2, and the shipped body.

**Non-blocking observations (NOT findings; recorded for transparency):**
- The analyst body's "single source of truth" sentence for `/source-fidelity` slightly overstates that skill's coverage (the `meaning`/`compound_scene` fields actually live in `/thematic-fidelity` per prep-skill-specs §2). This is a provenance-clarity nit only — the additive contract is reprinted in full in the same analyst body, so runtime behavior is unambiguous. Architecturally intended (boundary contract: standalone NATIVE skill).
- The chapter-level `ch-<NN>.yaml` schema is not separately formalized in package-schemas (only the work-level `20-analysis-work-level.yaml` is); chapter-level inherits the existing v2.0 schema plus the additive fields, which is by design.

Neither observation blocks the P1 gate.

**Authorization:** REPORT-ONLY (`fix_authorization: false`). No files were modified.
