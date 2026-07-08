# P3 Fidelity Consolidated Findings (Phase Gate P3 — Source-Document Fidelity)

**Overall consolidated verdict: FAIL** (fidelity-agent-1 reported 2 IMPORTANT + 3 MINOR defects).

Source reports:
- `qa/qa-source-fidelity-report-1.md` (package structure + path-contract coverage) — **FAIL**, 2 IMPORTANT + 3 MINOR.
- `qa/qa-source-fidelity-report-2.md` (dual-form promotion + meaning-preservation) — **PASS**, 0 defects (10/10 checks; meaning source-grounded, dual-form correct, non-vacuous).

## Deduplicated findings (classification + resolution)

### SF1 — `60-handoff-prompt.md` has a heading before the literal prompt — IMPORTANT (fidelity-agent-1 #1)
- **Classification: GENUINE fidelity defect — clear contract violation.** `package-schemas.md` §5: "`60-handoff-prompt.md` — exactly the paste-able text, nothing else: `/laf:rewrite --work <work-slug>`". The file currently has a `# Handoff — tolkien` heading + blank line before the literal prompt (53 bytes vs the contract's literal-only form).
- **Resolution:** Re-write `work/prep/tolkien/60-handoff-prompt.md` to contain ONLY the literal `/laf:rewrite --work tolkien` (a single H1 line is the convention elsewhere, but the §5 contract explicitly says "nothing else" — so literal text only). Re-run the handoff step.

### SF2 — Tier 2 silently dropped; default [1,2,3,5] not honored, no recorded narrowing — IMPORTANT (fidelity-agent-1 #2)
- **Classification: GENUINE fidelity gap.** `package-schemas.md` §6 + `prep-skill-specs.md` §6: default `tiers_active: [1, 2, 3, 5]`, narrowed only by an explicit greenlight decision. The prove set `[1, 3, 5]` with no recorded narrowing decision and no `tier_2` rows in `30-mapping.yaml`. The prove auto-confirmed greenlight without making (or recording) a narrowing judgment, so the contract default should hold.
- **Resolution:** Add `tier_2` entries to `30-mapping.yaml` for each character/concept/scene (per the shipped prior-art body style — `tier_2` for concepts is plain string; for characters/key_scenes inline-flow rows). Set `50-greenlight.md` `tiers_active: [1, 2, 3, 5]`. Re-promote the kb hyphen copy (`tolkien-mapping.yaml`, 6-key, meaning KEPT) from the corrected `30-mapping.yaml`. (The root underscore copy already strips meaning; tier_2 rows there are fine and consistent.)

### SF3 — `meaning:` "corrupting nature of power" possibly overclaimed vs fixture — MINOR (fidelity-agent-1 #3)
- **Classification: NOT a defect — source-grounded per fidelity-agent-2's independent verification.** fidelity-agent-2 traced every load-bearing phrase in `meaning.value` to `laf-adaptation/source/tolkien/ch-01.txt`; "Sauron's will presses down cold and patient" is verbatim from the fixture (lines 4–6: "every soldier felt the weight of his will pressing down, cold and patient"). The oppressive-power meaning IS in the text. The package's Open Risk #1 already concedes absent Ring/Frodo arc. fidelity-agent-1's concern and fidelity-agent-2's grounding sweep disagree; the grounding sweep is evidence-based. The phrase is acceptable.
- **Resolution:** No action required — source-grounded. (Optional: the wording already distinguishes "unshown but felt", which is accurate.)

### SF4 — Character tier_1 field sets heterogeneous vs §4 example uniform {name, archetype} — MINOR (fidelity-agent-1 #4)
- **Classification: NOT a defect — illustrative example vs prior art.** `package-schemas.md` §4 shows `{name, archetype}` as an EXAMPLE; the shipped `tolkien-mapping.yaml` prior art uses richer, varied inline-flow rows per character. The contract example is illustrative, not a strict uniform-shape mandate. The framework is key-tolerant (CLAUDE.md §3).
- **Resolution:** No action required — the heterogeneous field sets match the shipped prior-art body style.

### SF5 — Some `governing_rule` values outside the §2 example vocabulary — MINOR (fidelity-agent-1 #5)
- **Classification: NOT a defect — illustrative example.** `package-schemas.md` §2 lists example rule names (death_handling, violence, …); the framework is explicitly key-tolerant and the example is illustrative. `thematic_fidelity` as a governing_rule for the meaning-preservation challenge is sensible and grounded in the `/thematic-fidelity` skill.
- **Resolution:** No action required — reasonable vocabulary extensions.

## Fix scope for the serialized fix agent (I20 — single agent)

Apply SF1 + SF2 to the RUNTIME P3 package outputs (these are runtime outputs, not build-time files; per the PG3.2 note, fidelity fixes re-run the relevant P3 step rather than editing build-time instruction files — there is no build-time instruction defect here, the prep procedure correctly produced outputs that need the two contract-fidelity corrections):

1. `work/prep/tolkien/60-handoff-prompt.md` — rewrite to contain ONLY the literal `/laf:rewrite --work tolkien` (per package-schemas.md §5 "exactly the paste-able text, nothing else").
2. `work/prep/tolkien/30-mapping.yaml` — add `tier_2` entries for each character/concept/scene (matching the shipped prior-art body style), so all four default tiers are authored.
3. `work/prep/tolkien/50-greenlight.md` — set `tiers_active: [1, 2, 3, 5]` (the default; the prove made no narrowing decision).
4. Re-promote the kb hyphen copy `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` (6-key, meaning KEPT) from the corrected `30-mapping.yaml`. (The root underscore copy `config/concept_mapping/templates/tolkien_mapping.yaml` strips meaning regardless; leave its 5-key form, the tier_2 rows there remain consistent.)

MUST NOT touch: build-time instruction files (the prep procedure is correct), adopted files, VENDOR rows, the boundary. After the fix, re-run `uv run python laf-adaptation/scripts/check_boundary.py` (final line must begin `BOUNDARY CONTRACT: PASS`) and the dual-form assertions (30-mapping 6-key meaning; kb 6-key meaning; root 5-key no meaning).
