# P1 Applied Diff

Files: `laf-adaptation/agents/analyst.md` (NATIVE) + `laf-adaptation/agents/tier-coordinator.md` (BUILD-NEW).
All changes are ADDITIVE (no existing line deleted or reworded).

```diff
diff --git a/laf-adaptation/agents/analyst.md b/laf-adaptation/agents/analyst.md
index ed7b5e4..61e0100 100644
--- a/laf-adaptation/agents/analyst.md
+++ b/laf-adaptation/agents/analyst.md
@@ -19,6 +19,11 @@ Phase-0 ABORT gate.
 - `source_path` — a `source/<work>/ch-<NN>.txt` file to analyze.
 - `work` — the work label.
 - `chapter` — the chapter number `<NN>`.
+- `granularity` — `chapter` (default) | `work`. `work` runs the 5-phase protocol over the whole-work
+  source declaration and emits the work-level schema. **Default `chapter` reproduces today's behavior
+  exactly.**
+- `out_path` — output file path. Default `work/analysis/ch-<NN>.yaml` (chapter mode);
+  `work/prep/<work-slug>/20-analysis-work-level.yaml` when `granularity: work`.
 
 **`active_tier` is NOT an input.** Analysis is **tier-invariant** (Q1.5): you produce one shared,
 tier-neutral source analysis that every tier's transform reads. Do not branch on tier.
@@ -38,6 +43,12 @@ Phase 0 — Source Declaration:
   IF MEMORY-BASED: every emitted fact MUST carry confidence: UNCERTAIN.
 ```
 
+**Meaning & compound-scene passes (additive; do not gate the ABORT).** After Phase 4, emit `meaning:`
+for the analyzed unit (the theme/allegory to be neither added nor stripped — `/thematic-fidelity`), tagged
+with its own confidence. Then scan for co-occurrence: any scene where ≥2 transformation_flags are
+`severity: high` sets `compound_scene: true` and is listed under `compound_scenes:`. These passes never
+relax the Phase-0 NO-ACCESS ABORT gate; on ABORT the file still carries only `status: ABORTED`.
+
 **Observable-test decision rule for the access level (operational reading).** Pick the level by an
 observable test on `source_path`, first match wins:
 - **FULL** — `source_path` passed; file exists, is readable, and is non-empty (readable end-to-end).
@@ -54,6 +65,12 @@ Write `work/analysis/ch-<NN>.yaml` conforming to the v2.0 schema documented in `
 `characters`, `events`, `summary`, `transformation_flags`, `uncertainties`. On NO-ACCESS the file carries
 `status: ABORTED` and nothing downstream proceeds.
 
+**Additive output fields (R10/R11) — `meaning` and `compound_scene`.** Between `transformation_flags` and
+`uncertainties`, also emit:
+- `meaning:` — `{value: "<what this unit MEANS beneath its surface — the allegory/theme to neither add nor strip>", confidence: CERTAIN | PROBABLE | UNCERTAIN}`. Grounded in `/thematic-fidelity`. At `granularity: work` this is the top-level work meaning; at `granularity: chapter` it is per-chapter (and per-scene where decomposed).
+- `compound_scene: true|false` — `true` iff ≥2 HIGH-severity `transformation_flags` co-occur in one scene.
+- `compound_scenes:` — present only when `compound_scene: true`; one entry per flagged scene, e.g. `{scene: "<name>", cooccurring_flags: [death, emotional], severity: high}`.
+
 **`status ∈ {OK, ABORTED}`.** `OK` is the **normal completion path** — a successful analysis emits
 `status: OK`. The Hard behavior block above only shows the `ABORTED` branch (the constraint #2 gate), but
 that is the exception, not the default: any FULL / PARTIAL / MEMORY-BASED run that completes emits
diff --git a/laf-adaptation/agents/tier-coordinator.md b/laf-adaptation/agents/tier-coordinator.md
index 38da510..973d2fe 100644
--- a/laf-adaptation/agents/tier-coordinator.md
+++ b/laf-adaptation/agents/tier-coordinator.md
@@ -92,6 +92,24 @@ for element shared across ≥2 tiers:
 (`mandatory`-transform < `optional`-transform < `preserve`), plus the tier's violence/moral-ambiguity
 threshold levels. A coarse ordinal comparison, not a score — enough to catch an inverted rendering.
 
+### Check D — Meaning preservation (R10; /thematic-fidelity)
+Every tier's rendering must **preserve the work-level `meaning`** while its surface transforms. Read the
+top-level `meaning:` from `<work>-mapping.yaml` (and the per-unit `meaning` in `shared_analysis`). For each
+element shared across tiers, assert the tier's rendering still carries that meaning — the allegory/theme is
+neither added where the source withholds it nor stripped where the source asserts it.
+```
+for element shared across tiers:
+    m = meaning_of(element, shared_analysis | mapping)
+    for tier in tiers:
+        if not preserves_meaning(render(element, tier), m):
+            conflicts += {type: "meaning_diff", tier, element, meaning: m}
+status_meaning: Meaning-PRESERVED | Meaning-DIFF
+```
+`preserves_meaning()` is an ordinal judgment, not a score: does the transformed surface still *mean* what
+the source unit means at the target tier's altitude? A tier-1 "Grumpy King" preserves the meaning "an
+external corrupting force, not innate evil" (Agency Externalization is meaning-preserving); a rendering that
+silently drops the allegory, or invents one the source never had, is `Meaning-DIFF`.
+
 ## Operational reading — grounding `maturity()`, `permitted_at`, and `disclosures`
 
 *(Operational-reading note, additive; the Check A/B/C pseudocode above is the spec-carried contract and
@@ -146,6 +164,7 @@ tiers: [1, 3, 5]     mode: parallel     source: work/analysis/ch-<NN>.yaml
 - A source-fidelity: PASS (all renderings trace to shared anchors)
 - B disclosure-leak:  PASS (no tier discloses beyond its threshold)
 - C monotonicity:     PASS (T1 ≤ T3 ≤ T5 maturity for every shared element)
+- D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)
 
 status: RECONCILED
 conflicts: []
@@ -154,6 +173,13 @@ On `CONFLICT`, `conflicts:` is non-empty and lists `{type, tier, element/disclos
 (muse) must resolve — by re-dispatching the offending tier's writer with the conflict as a revision note
 — **before** `chronicler` promotes anything (constraint #5: no promotion of inconsistent canon).
 
+**Meaning-DIFF rides this same gate (R10).** A `Meaning-DIFF` from Check D contributes a
+`{type: "meaning_diff", tier, element, meaning}` entry to the existing `conflicts:` list above — so a
+meaning divergence blocks `chronicler` exactly as an A/B/C conflict does. No new control flow: Check D rides
+the existing `RECONCILED | CONFLICT` gate. The coordinator already loads `/adaptation-tiers`,
+`/source-fidelity`, `/kb-management`; Check D reads `meaning` as **data** from the mapping/analysis, so no
+new skill line is required.
+
 ## Interaction with chronicler (never writes canon)
 You run **before** `chronicler` (step 10 → step 11). You **never write canon** — you only reconcile and
 report. Once `status: RECONCILED`, `chronicler` runs **per tier**, each writing that tier's
```
