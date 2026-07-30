# M4 Fidelity Verification (Content) — Independent Confirmation Round

**Date:** 2026-07-09
**Round:** M4 source-fidelity gate — content confirmation (post-PASS)
**Driving spec:** `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md` (§1–§15)
**fix_authorization:** false (report-only)
**Prior gate:** M4 returned PASS with no fixes (both fidelity agents PASS). This round independently spot-checks a §1–§15 sample.

---

## Overall Verdict: PASS

No missing coverage. No phantom/fabricated coverage. The assembled output faithfully represents the driving spec across all six sampled dimensions.

---

## Items Reviewed

| # | Dimension | Result | Evidence |
|---|-----------|--------|----------|
| 1 | §3/§14 split+monolith HALT genuinely enforced in Stage 0.2 | PASS | SKILL.md Stage 0.2 rule 2 has an explicit **Negative guard (both-present)**: fires ONLY when ≥2 non-canonical files AND no co-present dominating monolith; if BOTH present, rule 2 does NOT fire, falls through to rule 4 (ambiguity → HALT-ask). Rule 4 sets `mode_confidence: UNCERTAIN`, "blocks any `source/` write until resolved (no ch-<NN>.txt, no manifest, no .raw/)". Load-bearing control flow, not a mention. `Books/LWW/` case named. Matches spec §3 rule 4 + §14 risk #1. |
| 2 | §5 every manifest field present (semantic coverage) | PASS | SKILL.md L224–272 reproduces the v1 schema byte-identical to spec §5: schema_version, work, slug, title, materialized_at, input_mode, mode_confidence, raw_sources[](path/role/sha256/mime_hint), normalization_policy(output_format/preserved_as_text/discarded), chapter_count, chapters[](id/order/title/title_confidence/file/output_sha256/provenance{class/raw_path/source_kind/start_marker/end_marker}/split_confidence/order_confidence/normalization_events[]/needs_human_review/review_reason), omitted_material[], ambiguous_splits, review{status/accepted_risks}. Zero fields missing. |
| 3 | §6 confidence rule verbatim + operable | PASS | SKILL.md L117: "CERTAIN requires ≥2 independent agreeing signals and no contradiction" = spec L170 verbatim. PROBABLE/UNCERTAIN/single-signal-cap clauses = spec L171–173 verbatim. Operable: defines *contradiction* concretely (disagreeing boundary offset / count / title-ordinal) and is mirrored in boundary-rules.yaml `confidence_rule` with "SKILL.md wins on drift" note. |
| 4 | §9/§10 idempotency + gate reuse faithfully present | PASS | §9: SKILL.md covers adopt/zero-re-split, re-run (hash-match no-op; raw-changed→gated diff plan, never overwrite by default), collision (differing hash → never clobbered → HALT-and-ask). §10: Stage 0.5 "injected into existing §5 gate — no new gate or HALT machinery"; deferred-write invariant present; "Greenlight cannot reach CONFIRMED while any unresolved". All three §10 elements present + mirrored in prep-cordinator STAGE 5/7 + one-line ratification checklist. |
| 5 | §13 AC1 "identical" reading is a faithful non-contradiction | PASS | SKILL.md L218–222 disambiguates AC1: chapter TEXT identical across Mode A/B; manifest NOT byte-identical (mode/provenance fields legitimately differ). Correct — spec §5's manifest is itself mode-specific (input_mode, source_kind, start/end_marker differ by mode), so a "manifest byte-identical" reading would contradict §5. Faithful non-contradiction, not a weakening. |
| 6 | §15 two deferred seams recorded OUT-OF-SCOPE and NOT built | PASS | Both seams left unbuilt. (a) manifest-in-read-set: every `rewrite_phase_reads` reference is a non-membership/no-4th-entry assertion (path-contract §4 L77 "no 4th entry"; SKILL.md L213–214; prep §1 note "8 fixed-name files unchanged"). (b) per-chapter analysis: grep for `granularity=chapter`/`per-chapter analysis`/`per-chapter source-fidelity` = 0 hits; prep-cordinator STAGE 3 remains `granularity: work` (L102–104). |

---

## Summary

- Dimensions passed: 6 / 6
- Dimensions failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only round)

**Phantom/fabricated coverage check:** No manifest field beyond spec §5 invented (schema byte-identical). No new gate/HALT machinery beyond reused §5/greenlight. No 4th read-entry, no 9th package file (path-contract §2 unchanged 8 files), no per-chapter analysis, no second script (boundary-rules.yaml is data-only; SKILL.md L24 "check_boundary.py remains the sole script"). Clarifying elaborations present (Mode-A completeness axis, duplicate-monolith sha256 tie-break, adopted-set null-`.raw/`, PDF native-read) are faithful derivations of spec §7/§8/§9 rows + the ADR-006 no-runtime constraint — not fabricated requirements.

---

## Issues Found

None.

---

## Self-Audit

**(a) Reliance list — prior M4 PASS relied on:**
- Relied on prior M4 source-fidelity PASS (both fidelity agents) for the overall structural fidelity claim — but did NOT skip content re-checking; every dimension re-read against the spec text.

**(b) Independent semantic checks (≥1 required):**
- Confidence-rule verbatim match — verified by Reading SKILL.md L117 + spec L170 and byte-comparing the load-bearing sentence.
- AC1 non-contradiction — verified by Reading SKILL.md L218–222 and reasoning against spec §5 mode-specific fields + AC1 wording (spec L267–268).
- §15 seams-not-built — verified by grep across chapter-materialize/ + path-contract.md + prep-cordinator.md returning only non-membership assertions and zero per-chapter-analysis tokens.

**Verification stats:**
- Factual claims independently verified: 6/6 dimensions, each cross-read against driving spec text.
- Files read: merged-requirements.md, qa-input-inventory.md, chapter-materialize/SKILL.md (full), prep-cordinator.md (full), path-contract.md (full), boundary-rules.yaml (full), prep/SKILL.md §1, CLAUDE.md (context). Grep for phantom-seam tokens.
- Web research: none required (fidelity check is local-file-bound); Tavily not invoked; no fallback needed.

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep: 1 | Glob: 0 | Bash: 1

---

## Recommendations

None. The M4 PASS-with-no-fixes verdict is corroborated by this independent content spot-check. Proceed.

## QA Complete
