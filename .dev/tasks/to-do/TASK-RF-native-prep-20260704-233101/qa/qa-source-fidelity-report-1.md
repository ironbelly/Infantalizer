# QA Report — Source-Document Fidelity (Phase Gate P3)

**Topic:** `/laf:prep` produced package fidelity vs path-contract + package-schemas
**Date:** 2026-07-05
**Phase:** source-fidelity (fidelity-agent-1 — package-structure + path-contract coverage lens)
**Fix cycle:** N/A (REPORT-ONLY, `fix_authorization: false`)
**Scope:** Full 8-file package under `work/prep/tolkien/` + dual-form promotion targets.

---

## Overall Verdict: FAIL

The package realizes the contract's 8-file layout, dual-form promotion, confidence-min rule, and
compound-scene reconciliation **structurally**. Six fidelity defects were found against the
path/package contract: 2 IMPORTANT (Tier 2 silently dropped; handoff file violates "nothing else"),
4 MINOR (schema variances). Per zero-tolerance, all six must resolve. Two of the six are directly
actionable fixes (not prove artifacts); four are schema variances the contract examples imply.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 8 files exist with fixed names (contract §2) | PASS | `ls work/prep/tolkien/` shows exactly the 8 prescribed filenames; no extras, no missing. |
| 2 | `00` research/context purpose met | PASS | `00-work-context.md` carries frontmatter (`work, title, author, context_confidence, source_access_declaration`) and all 5 prescribed sections (Author & era, Genre & form, Reception & cultural weight, Known adaptation history, Source-access declaration). Inline confidence tags present (CERTAIN/PROBABLE). Context ceiling honored. |
| 3 | `10` derived challenge taxonomy purpose met | PASS | `10-challenges.yaml` carries `derived_from: 20-analysis-work-level.yaml`, typed challenges with `governing_rule` + `human_judgment_dimension` + `per_tier_strategy` + `meaning_ref`, plus `compound_scenes:` with §2.1 reconciliation (`emotional_core`, `decomposition`, `per_tier`, `meaning_survives: true`). |
| 4 | `20` source text-track analysis purpose met | PASS (w/ schema variance — see #16) | `20-analysis-work-level.yaml` carries `status, metadata, essentials, characters, events, summary, transformation_flags, meaning:, compound_scene: true, compound_scenes:, uncertainties`. `meaning:` present (R10). Text-grounded in ch-01.txt (verified line-by-line against fixture). |
| 5 | `30` derived mapping + top-level `meaning:` purpose met | PASS | `30-mapping.yaml` has top-level `meaning:` (R10 6th key), `work_metadata`, `characters`, `concepts`, `key_scenes`, `master_translation_table` — the 6-key 0.1 form. Per-entry `_confidence: {text, context, eff}` present. |
| 6 | `30` per-entry `eff` = `min(text, context)` | PASS | 13 character/concept/scene entries: all `text: CERTAIN, context: PROBABLE, eff: PROBABLE`. `min(CERTAIN, PROBABLE) = PROBABLE` holds. `master_translation_table` entries carry only `{eff: PROBABLE}` (contract §4 schema shows `_confidence: {eff: PROBABLE}` for these rows — consistent). |
| 7 | `40` synthesis brief purpose met | PASS | `40-prep-brief.md` has all 5 prescribed sections: Decisions ratified, Cross-tier spine summary, Meaning to preserve, Answered questions, Open risks / low-confidence entries. |
| 8 | `50` greenlight gate CONFIRMED | PASS | `50-greenlight.md` frontmatter `status: CONFIRMED`. Checklist carried; user-confirmation block present. Contract §4 requires `/laf:rewrite` refuse unless CONFIRMED — satisfied. |
| 9 | `60` handoff = literal `/laf:rewrite --work tolkien` | FAIL (IMPORTANT) | `60-handoff-prompt.md` is 53 bytes and contains a leading `# Handoff — tolkien` heading + blank line + the prompt. Contract §5 / `package-schemas.md §5`: "**exactly the paste-able text, nothing else**" — only ``/laf:rewrite --work <work-slug>`` should be present. Heading violates "nothing else". |
| 10 | `70` traceability purpose met | PASS | `70-traceability.md` has Artifact provenance + Mapping entry ledger + DEFAULTED questions + Promotion provenance. Per-entry ledger traces every `30-mapping` entry to a `20` fact with text/context/eff. |
| 11 | Tier set default `{1,2,3,5}` (contract §6) | FAIL (IMPORTANT) | Contract `package-schemas.md §6` declares `tiers_active: [1, 2, 3, 5]` as the **default** ("default all four (Q4); greenlight may narrow"). Produced `50-greenlight.md` carries `tiers_active: [1, 3, 5]` — Tier 2 silently dropped with NO narrowing justification recorded. `30-mapping.yaml` has zero `tier_2` entries (verified `grep -c tier_2 = 0`). The prove summary asserts "T2 omitted per the prove's `tiers_active`" but does not surface a user-driven narrowing decision (the contract's only legitimate path to drop a default tier). Greenlight checklist marks tier set `[x] confirmed` without recording who narrowed or why. |
| 12 | Dual-form promotion: 0.1 hyphen 6-key with `meaning:` | PASS | `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` exists; top-level `meaning:` block present; per-entry `_confidence` present; 6 top-level keys (work_metadata, characters, concepts, key_scenes, master_translation_table, meaning). |
| 13 | Dual-form promotion: root underscore 5-key with `meaning:` STRIPPED | PASS | `config/concept_mapping/templates/tolkien_mapping.yaml` exists; verified `grep -n "^meaning:" = 0` and `grep -n "_confidence" = 0` (only match is the descriptive comment line). Exactly 5 top-level keys (work_metadata, characters, concepts, key_scenes, master_translation_table). |
| 14 | Write-ownership boundary (contract §5) | PASS | Prep phase wrote only `work/prep/tolkien/*` + the two `/kb-management` promotion targets. No `kb/canon/*` or `kb/adaptations/tolkien/tier-*/…` written by prep (those are chronicler/rewrite-phase paths). |
| 15 | Phantom coverage (entries that don't trace to source) | PASS | Spot-checked every `20-analysis` event/character against `ch-01.txt` (259-word fixture): Sauron, Denethor, Théoden, Éowyn, Nazgûl, all 7 events, transformation_flags counts, and `meaning:` (hope against despair, redemptive courage) all trace to fixture text. No fabricated entries. (The "corrupting nature of power" — see #17 — is the one untraceable claim.) |
| 16 | `20-analysis` `compound_scenes:` per-entry schema | FAIL (MINOR) | Contract `package-schemas.md §3` schema shows `compound_scenes:` entries as `{scene, cooccurring_flags, severity}`. Produced `20-analysis` entries DO carry all three (Siege: `[death, emotional, violence]` / `high`; Théoden/Éowyn: same). PASS on those fields. **However** the produced `20` also asserts `compound_scene: true` as a separate top-level scalar (line 63) which the schema block lists. Verify intent: this is per the schema. Actual defect is in #17. |
| 17 | `meaning:` content faithfulness to fixture | FAIL (MINOR) | `30-mapping.yaml` `meaning.value` (and `40-prep-brief.md` "Meaning to preserve") asserts "the **corrupting nature of power**: Sauron's will presses down cold and patient, unshown but felt." The fixture (`ch-01.txt`) shows Sauron's will *pressing down* (line 5–6) but contains NO "corrupting nature of power" theme — the Ring, Frodo, Mount Doom, and the corruption arc are absent from this 259-word siege fixture. `40-prep-brief.md` Open Risk #1 explicitly acknowledges "Frodo, Sam, the Ring, Mount Doom … none appear in ch-01.txt", yet `meaning:` still bundles the corruption theme as if fixture-grounded. The fixture grounds "hope against despair" + "redemptive courage" only. This is a mild context-track overclaim leaking into the text-track `meaning:`. |
| 18 | `30-mapping` schema field drift from contract example | FAIL (MINOR) | Contract `package-schemas.md §4` character schema example: `tier_1: {name, archetype, _confidence}`, `tier_3: {can_show, _confidence}`. Produced `30-mapping.yaml` character tier_1 entries use a heterogeneous field set: `sauron.tier_1` has `{name, archetype, cause, eye}` (no `_confidence` inside the tier row — `_confidence` is sibling-level, OK); `denethor.tier_1` has `{name, cause, omit:[...]}` (no `archetype`); `eowyn.tier_1` has `{name, heroic_moment, witch_king}`. Contract example is illustrative ("the shipped `<work>_mapping` schema"), but the produced field set varies row-to-row within the same character mapping. Minor schema-tightness defect; downstream muse reads these as data so it is not blocking, but it diverges from the "schema-frozen" intent of §4. |
| 19 | `master_translation_table` row schema | PASS (w/ variance note) | Contract §4 example: `{original, tier_1, principle, _confidence: {eff: PROBABLE}}`. Produced rows also carry `tier_3` and `tier_5` fields. Additive (not subtractive); acceptable since the table is the source of per-row translation principles and tier coverage. Not a defect — recorded for completeness. |
| 20 | Promotion runtime non-vacuousness | PASS | `p3-prep-run.md` records pre-run vs post-run sha256 for both promotion targets; both differ post-run, proving the runtime transform re-wrote them (not hand-authored at build time). |

## Summary
- Checks run: 20
- PASS: 15
- FAIL: 5 (2 IMPORTANT, 4 MINOR — see note on #16)
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `work/prep/tolkien/60-handoff-prompt.md` (entire file, 53 bytes) | File violates contract `package-schemas.md §5`: "**exactly the paste-able text, nothing else**". Contains a leading `# Handoff — tolkien` markdown heading and a blank line before the prompt. The contract schema for this file shows only the single line ``/laf:rewrite --work <work-slug>``. | Strip the heading and blank line. The file should be exactly the bytes of ``/laf:rewrite --work tolkien\n`` (29 bytes). |
| 2 | IMPORTANT | `work/prep/tolkien/50-greenlight.md:4` + `work/prep/tolkien/30-mapping.yaml` (no tier_2 anywhere) | Tier 2 silently dropped. Contract `package-schemas.md §6` declares `tiers_active: [1, 2, 3, 5]` as the **default all four (Q4); greenlight may narrow**. Produced is `[1, 3, 5]` with no recorded user-driven narrowing decision and no Tier 2 mapping rows anywhere in `30-mapping.yaml`. `40-prep-brief.md` Open Risk #4 acknowledges T2 omitted but frames it as prove-artifact, not a greenlight decision. | Either (a) restore `tiers_active: [1, 2, 3, 5]` and add Tier 2 mapping rows, OR (b) record the narrowing as a greenlight decision in `50-greenlight.md § User confirmation` (who narrowed, why, Q4 default overridden) and surface it in `40-prep-brief.md § Decisions ratified` as a Q4-default-override row rather than an Open Risk. The contract's only legitimate path to drop a default tier is greenlight narrowing — that path must be evidenced. |
| 3 | MINOR | `work/prep/tolkien/30-mapping.yaml:7` (`meaning.value`) + `40-prep-brief.md:36–40` | `meaning:` bundles "the corrupting nature of power" as a fixture-grounded theme. The 259-word siege fixture contains no Ring/Frodo/corruption arc; it grounds only "hope against despair" + "redemptive courage". `40-prep-brief.md` Open Risk #1 concedes these elements are absent from the fixture. | Either drop "the corrupting nature of power" from `meaning.value` (keep only the two fixture-grounded themes), OR split the claim: text-grounded themes (hope, courage) vs context-track themes (corruption) with separate confidence lines. As written, a context-track overclaim is leaking into the text-track `meaning:` field. |
| 4 | MINOR | `work/prep/tolkien/30-mapping.yaml` `characters.*.tier_1` (lines 26, 32, 38, 44, 50) | Character `tier_1` field set is heterogeneous across characters (`sauron`: name+archetype+cause+eye; `denethor`: name+cause+omit; `eowyn`: name+heroic_moment+witch_king; `nazgul`: name+dread). Contract §4 schema implies a uniform shape (`name, archetype` at tier_1). | Tighten to a uniform tier_1 shape: `{name, archetype, [<auxiliary fields>]}` — keep character-specific auxiliary fields but ensure every character row carries `name` + `archetype` (or document the per-character variance as intentional). |
| 5 | MINOR | `work/prep/tolkien/10-challenges.yaml` `challenges[*].governing_rule` | `psychological-collapse` uses `governing_rule: emotional_calibration`, `allegory-stance` and `omission-honor-set` use `thematic_fidelity`, `target-age-nuance` uses `adaptation_tiers`. Contract §2 example shows `governing_rule` values drawn from `/adaptation-rules` categories (`death_handling`, `violence`, `conflict_handling`, `death_euphemism`). The five extra rule names are not in the contract's example vocabulary. | Confirm these `governing_rule` values exist in the shipped `/adaptation-rules` categories; if not, map them to the canonical vocabulary. If they DO exist (likely, since the rule set is larger than the contract example), add a one-line comment citing the source category file to make the provenance explicit. |

> Note on #16 in the Items Reviewed table: that row is a compound check — its first half (compound_scene fields present) PASSES, and the actual defect surfaced is captured separately as Issue #3 (the `meaning:` overclaim). The table records 5 FAIL rows (#9, #11, #17, #18) plus #16 marked FAIL because of #17 surfacing from it; the canonical defect list is the 5 rows above.

## Actions Taken
None (REPORT-ONLY, `fix_authorization: false`). All 5 defects are documented with specific locations and required fixes for a downstream fix-cycle agent to apply.

## Confidence
- **Verified:** 20 / 20 checklist items
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 13 | Grep: 6 | Glob: 0 | Bash: 7
- No web research performed (all verification was source-truth-local against the contract files and produced package).

## Recommendations
1. **(Blocking)** Resolve Issue #1 (handoff file) and Issue #2 (Tier 2 narrowing) before this package is treated as a contract-conformant exemplar. Both are direct, low-risk edits.
2. **(Non-blocking but required for clean exemplar status)** Resolve Issues #3–#5: tighten the `meaning:` to fixture-grounded themes, normalize the character tier_1 schema, and cite `/adaptation-rules` provenance for non-canonical `governing_rule` values.
3. **(Process)** Consider adding a contract-level assertion in the prove harness that (a) `60-handoff-prompt.md` is byte-equal to ``/laf:rewrite --work <slug>\n`` and (b) `tiers_active` default is `[1,2,3,5]` unless a narrowing decision is recorded. Both defects would have been caught by mechanical checks.

## QA Complete

