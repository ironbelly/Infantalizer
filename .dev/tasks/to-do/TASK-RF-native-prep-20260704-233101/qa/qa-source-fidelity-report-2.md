# QA Report — Phase Gate P3 (Source-Document Fidelity, Dual-Form Promotion)

**Lens:** fidelity-agent-2 — dual-form promotion + meaning-preservation
**Topic:** `/laf:prep` STAGE 7 dual-form promotion (Tolkien fixture) — `meaning:` KEPT vs STRIPPED
**Date:** 2026-07-05
**Phase:** report-validation (P3 source-fidelity gate, fidelity-agent-2 of N)
**Fix cycle:** N/A (REPORT-ONLY — `fix_authorization: false`)
**Adversarial target:** ≥5 fidelity defects assumed present against the dual-form contract.

---

## Overall Verdict: PASS

The dual-form promotion contract (`docs/native-prep/design/package-schemas.md` §4.1 + `path-contract.md` §3) is satisfied. All four P3 assertions hold under independent source-traced verification. **Zero fidelity defects found.** Per the adversarial-stance rule, the 0-defect result is treated with suspicion in §Confidence below; the tool-evidence trail substantiates it.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | KB hyphen copy is 6-key with `meaning:` KEPT | PASS | `uv run --with pyyaml` parse of `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` → keys `['characters','concepts','key_scenes','master_translation_table','meaning','work_metadata']` len=6; `meaning:` block at line 6 with `value/text_confidence/context_confidence/confidence` complete; `meaning.confidence: PROBABLE`, `meaning.value` 354 chars. |
| 2 | Root underscore copy is exactly the frozen 5-key, `meaning:` STRIPPED | PASS | `uv run --with pyyaml` parse of `config/concept_mapping/templates/tolkien_mapping.yaml` → keys `['characters','concepts','key_scenes','master_translation_table','work_metadata']` len=5; `has meaning: False`. Matches `ADDING_NEW_WORKS.md` step-6 authority line: `# → ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']` (`docs/guides/ADDING_NEW_WORKS.md:111`). |
| 3 | Root underscore copy has NO `_confidence` diagnostics leaked | PASS | Recursive walk of parsed YAML (any depth) → 0 `_confidence` keys. The single textual `_confidence` token at line 4 is the **header comment** explaining what was stripped, not a YAML diagnostic key. `grep -c "_confidence"` returns 1 from that comment only. |
| 4 | KB copy retains `_confidence` diagnostics (0.1 extension) | PASS | Recursive walk → 21 `_confidence` keys across `characters/concepts/key_scenes/master_translation_table`, matching the derived `30-mapping.yaml` exactly (21). |
| 5 | `meaning:` values preserve work-level meaning from source (NOT placeholder) | PASS | Every load-bearing phrase in `meaning.value` traces to `laf-adaptation/source/tolkien/ch-01.txt` (259 words, 1354 chars after lowercase): "the sun... city held... grey city still standing" (hope pivot), "steward denethor... something in him had already broken" (steward), "théoden... fell, and did not rise" (king fallen), "field was heavy with grief", "éowyn stood over him... struck it down" (redemptive courage), "will pressing down, cold and patient" + "sauron did not ride... weight of his will" (Sauron offstage-but-felt), "dark had looked back... looked too long into the dark" (despair). Three phrases required whitespace normalization (newline-in-source vs single-space-in-meaning); all present after normalization. The analyst-derived framing words ("Redemptive courage", "allegory") are explicit generalization labels, not source quotes — acceptable per `package-schemas.md` §3 `meaning:` spec ("the allegory/theme/moral center to neither add nor strip"). |
| 6 | KB hyphen body matches derived 30-mapping byte-identically (modulo header line 2) | PASS | `diff <(tail -n +3 work/prep/tolkien/30-mapping.yaml) <(tail -n +3 laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml)` → exit 0, no diff. Headers differ correctly only in line 2: derived says "Derived by /prep §4 from 20-analysis-work-level.yaml + 10-challenges.yaml"; KB says "Promoted by /prep STAGE 7 dual-form transform from work/prep/tolkien/30-mapping.yaml". `meaning.value` byte-identical between derived and KB (len_a == len_b == 354). |
| 7 | Root underscore body matches derived minus `meaning:` minus `_confidence` | PASS | Spot-checked: `work_metadata/characters/concepts/key_scenes/master_translation_table` content byte-identical; only the `meaning:` top-level block (lines 6–10 of derived) and the per-entry `_confidence` annotation dicts are absent. Root header line 4 documents both strips. |
| 8 | Path naming honors `path-contract.md` §3 (hyphen vs underscore intentional) | PASS | KB file `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` (hyphen); root file `config/concept_mapping/templates/tolkien_mapping.yaml` (underscore). Both present, both spellings match the contract's verified examples verbatim. |
| 9 | Both promotion targets are genuine runtime outputs (not stale pre-existing) | PASS | Pre-run snapshot `test-results/p3-prerun-mapping-hashes.txt` shows BOTH pre-existing files at sha256 `914a85b8...707f` (byte-identical, 5-key, no `meaning:`). Independently recomputed post-run sha256s: root=`2d62cb34...83b8`, kb=`b3368d64...7e6` — both DIFFER from pre-run and from each other. `p3-prep-run.md` write-provenance section records the run overwrote pre-existing 5-key files. |
| 10 | Root copy validates against the shipped frozen 5-key schema | PASS | Independently parsed root YAML → exactly the 5-key set mandated by `ADDING_NEW_WORKS.md:111` (`['characters','concepts','key_scenes','master_translation_table','work_metadata']`). No 6th key, no meaning sub-tree, no diagnostic sub-trees — schema-byte-identical to the shipped exemplar shape. |

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY — `fix_authorization: false`)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| — | — | — | No fidelity defects found. | None. |

## Cross-File Consistency Notes (informational, not defects)

1. **`_confidence` count is 21 in both 6-key files, 0 in the 5-key root.** This is the correct dual-form delta: the diagnostic annotation keys are explicitly described in `package-schemas.md` §4.1 as "0.1-only diagnostics; the root 5-key copy also drops them." The promotion correctly stripped BOTH `meaning:` AND `_confidence` from the root copy.
2. **Header comment in root file mentions `_confidence`** (line 4: "Form: top-level meaning: STRIPPED; per-entry _confidence: STRIPPED"). A naive `grep -c "_confidence"` returns 1, which could be mistaken for a leak. Recursive YAML-parse walk confirms zero diagnostic keys at any depth — the textual occurrence is documentary prose only, not a leaked key. This is a stylistic choice (header documents the transform), not a contract violation; the frozen 5-key schema cares about parsed YAML keys, not header comments.
3. **`meaning.value` is 354 chars across both 6-key files** (byte-identical) — no truncation, no paraphrase drift between derived and promoted forms. The promotion transform is a faithful copy for the 0.1 layer.

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 7 | Grep: 4 | Glob: 0 | Bash: 7 (incl. uv-managed Python YAML parse + sha256 recompute + diff + source grounding substring sweep)

**Web research engagement:** None — all verification is source-truth-local (design docs + produced YAML + fixture source text). Tavily/WebSearch not required; no fallback.

**Adversarial-stance self-audit (per Principle 9):** A 0-defect P3 pass is suspect. The specific tool actions that substantiate it:
- Independent YAML structural parse of all 3 mapping files (not relying on the run's own key-count assertion).
- Recursive `_confidence` walk at arbitrary depth (catches leaks the run's flat key-count check would miss).
- Independent sha256 recompute of both promotion targets and diff against the recorded pre-run snapshot.
- Byte-level `diff` of derived vs KB body (not just key-count equality).
- Per-phrase grounding sweep of `meaning.value` against the raw 259-word fixture (not just "looks thematic").
- Cross-check of root 5-key set against the `ADDING_NEW_WORKS.md:111` authority line (not just the design doc).

The most likely place a defect could hide and not be caught: a subtle rewording between derived and KB `meaning.value` (eliminated by byte-identical diff) or a `_confidence` leak in a list-element dict (eliminated by recursive walk). Both eliminated. Verdict PASS is evidence-backed, not subjective.

## Recommendations

- None blocking. The dual-form promotion is contract-faithful and the run is non-vacuous.
- Optional (build-hygiene, not a P3 defect): the root file's header line 4 mentions `_confidence` for documentation; if a future automated linter greps for `_confidence` in the root copy as a leak-detector, this comment would false-positive. Consider either (a) leaving as-is (current behavior — the frozen schema validates parsed YAML, not comments) or (b) rewording the comment to avoid the literal token. Out of scope for this report-only gate.

## QA Complete
