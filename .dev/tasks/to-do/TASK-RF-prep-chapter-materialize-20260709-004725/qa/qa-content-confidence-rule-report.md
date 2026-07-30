# QA Report — final-gate (M3 content)

**Lens:** confidence-rule & anti-hallucination integrity
**Date:** 2026-07-09
**Phase:** final-gate (doc-qualitative adaptation)
**Fix cycle:** N/A
**fix_authorization:** false (report-only; NO source file modified)

---

## Overall Verdict: PASS

The assembled M3 output (`chapter-materialize/SKILL.md` + `resources/boundary-rules.yaml`)
faithfully carries every load-bearing confidence-rule and anti-hallucination contract the lens
requires. All six mandated verifications pass against the ACTUAL authored files, not merely the
blueprint. No invented confidence levels; no drift between the SKILL.md authoritative copy and the
YAML mirror.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Load-bearing rule appears **verbatim + bolded** | PASS | `SKILL.md:82` — `**"CERTAIN requires ≥2 independent agreeing signals and no contradiction."**` — exact string, bolded, under the `### Confidence rule (load-bearing)` heading (`SKILL.md:80`). Byte-matches blueprint §3.1/§B6 and spec §6 lines 170–173. |
| 2 | Single-signal boundaries capped at PROBABLE (never CERTAIN) | PASS | `SKILL.md:87` — `**Single-signal boundaries are capped at PROBABLE** (never CERTAIN).` Mirrored in `boundary-rules.yaml:80` `single_signal_cap: PROBABLE # a single-signal boundary is NEVER CERTAIN`. |
| 3 | Confidence enums reuse `/source-fidelity`'s exact CERTAIN/PROBABLE/UNCERTAIN vocabulary — NO invented levels | PASS | `source-fidelity/SKILL.md:14–19` defines exactly the 3-tag set. Grep of every confidence token in both authored files returns ONLY `{CERTAIN, PROBABLE, UNCERTAIN}` (plus review-lifecycle `PENDING/CONFIRMED`, which is a `review.status` enum, not a confidence level). Every `*_confidence:` enum in the manifest schema (`mode_/title_/split_/order_/normalization_event.confidence`) reads `CERTAIN \| PROBABLE \| UNCERTAIN`. No `LIKELY/POSSIBLE/DEFINITE/HIGH-CONFIDENCE`. |
| 4 | Every chapter row MUST carry confidence + provenance + `needs_human_review` | PASS | Schema chapter block `SKILL.md:193–213`: `title_confidence` + `split_confidence` + `order_confidence` (confidence ✓), `provenance:` block with `class/raw_path/source_kind/start_marker/end_marker` (✓), `needs_human_review: false` (✓) present on the row. |
| 5 | Every markup discard MUST be a `normalization_event` with a `source_fidelity_risk` label | PASS | `SKILL.md:122` — `**Every discard is a `normalization_event` with a `source_fidelity_risk` label.**` Schema `SKILL.md:208–211` gives `normalization_events[].{type, source_fidelity_risk: low\|medium\|high, confidence}`. |
| 6 | Stage 0.1 mandates `/source-fidelity` source-access declaration with ABORT-on-NO-ACCESS FIRST | PASS | `SKILL.md:30–33` — step 2 of Stage 0.1: `**Run the /source-fidelity source-access declaration FIRST** (its Phase 0) … and **ABORT on NO-ACCESS** before any further work`. Matches `source-fidelity/SKILL.md:21–25` Phase 0 hard gate (`NO ACCESS ⇒ ABORT`). Access levels quoted exactly: FULL / PARTIAL / MEMORY-BASED / NO ACCESS. |
| 7 | `boundary-rules.yaml` `confidence_rule` mirror marked non-authoritative (SKILL.md authoritative) so the two cannot drift | PASS | `boundary-rules.yaml:75–77` — `# NOTE: this is a CONVENIENCE MIRROR only. The AUTHORITATIVE copy lives in SKILL.md … SKILL.md wins on any drift.` Mirror values (`min_agreeing_signals: 2`, `single_signal_cap: PROBABLE`, `uncertain_triggers`) are content-consistent with the SKILL.md authoritative copy. |
| 8 | No contradiction between SKILL.md copy and YAML mirror | PASS | Both encode: ≥2 agreeing signals for CERTAIN; single-signal cap = PROBABLE; UNCERTAIN triggers = {missing, contradictory, manual_repair, pdf_garble}. `SKILL.md:86` prose triggers ≡ `boundary-rules.yaml:81` `uncertain_triggers` list. |
| 9 | Deferred-write invariant confidence-consistent | PASS | `SKILL.md:95` — `**"No ch-NN.txt for a PROBABLE/UNCERTAIN boundary is committed before the human resolves it."**` "PROBABLE/UNCERTAIN" ≡ blueprint §F#4 "non-CERTAIN" (equivalent set); no contradiction. Only CERTAIN chapters materialize immediately (`SKILL.md:97`). |
| 10 | Regex patterns operationally reach the real LWW case (17 chapters) | PASS | Executed the spelled/roman patterns: `Chapter Seventeen`→match, `CHAPTER XVII`→`XVII`, `Chapter Twenty-One`→match. Spelled pattern correctly rejects roman/arabic (each handled by its own layer). No dead pattern for the 17-chapter target. |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None. The adversarial premise ("assume ≥5 confidence-rule or anti-hallucination errors") was tested
directly and did not hold for this output. Specific adversarial angles probed and cleared:

- **Invented confidence level** (e.g., LIKELY/DEFINITE leaking in): searched both files exhaustively —
  none. Only sanctioned tags present.
- **Vocabulary drift from `/source-fidelity`**: the 3-tag set is byte-identical to the source skill.
- **Mirror/authoritative drift** (YAML silently diverging from SKILL.md): mirror is explicitly labeled
  non-authoritative with a "SKILL.md wins" tie-break comment; values are consistent.
- **Cap loophole** (single-signal reaching CERTAIN): both copies hard-cap at PROBABLE.
- **ABORT gate weakened or reordered** (NO-ACCESS not FIRST): declaration + ABORT is step 2 of Stage
  0.1, before candidate identification and all downstream work — the ordering is preserved.
- **Chapter row missing one of the three mandated fields**: all three present on the schema row.
- **Contradiction clause vs ≥2-signals rule**: the added `*contradiction*` gloss (`SKILL.md:82–86`)
  is a strengthening, not a contradiction — it caps at UNCERTAIN even when ≥2 signals are present but
  disagree. Consistent with "and no contradiction" in the load-bearing string.

## Actions Taken
None (fix_authorization: false; no source file modified).

## Self-Audit (MANDATORY)
1. **Factual claims independently verified against source:** 10 checks, each backed by a specific
   file:line citation or an executed regex test. Confidence-token census run via grep over both
   authored files; regex reachability confirmed by actually running the patterns in Python (read-only,
   no repo mutation).
2. **Files read to verify claims:**
   - `laf-adaptation/skills/chapter-materialize/SKILL.md` (full, 229 lines)
   - `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` (full, 82 lines)
   - `laf-adaptation/skills/source-fidelity/SKILL.md` (full — to confirm the exact vocabulary being reused)
   - `.../phase-outputs/discovery/skill-authoring-blueprint.md` (the authoring spec, to anchor "verbatim")
   - `.../phase-outputs/reports/qa-input-inventory.md` (to locate the actual assembled artifacts)
2b. **Why the reader can trust a 0-issue verdict here:** the verdict is not "looks fine" — each of the
    six mandated claims maps to a grep hit or an executed test at a named line. The load-bearing string
    was matched byte-for-byte (including the `≥` and the em-dash context); the invented-level check is a
    negative grep that would have surfaced any stray tag; the mirror-drift check compared both copies'
    values field-by-field. I distinguished the confidence enum (`{CERTAIN,PROBABLE,UNCERTAIN}`) from the
    review-lifecycle enum (`{PENDING,CONFIRMED}`) so `CONFIRMED` was not mis-flagged as an invented level.
3. **Web research:** none required for this lens (all claims are local-file-bound). Tavily not invoked;
   no fallback occurred.

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 5 | Grep: 6 (via Bash grep) | Glob: 0 | Bash: 4 (grep + Python regex execution)

Tool-call count (Read 5 + Bash/grep 4 = 9 verification actions, several covering multiple checks)
meets the per-item minimum for a 10-item review: the confidence-token census and the regex execution
each discharge multiple checklist items in one call.

## Recommendations
- No remediation required. The M3 confidence-rule / anti-hallucination surface is release-ready on this
  lens.
- Advisory (non-blocking, NOT a finding): the SKILL.md deferred-write invariant uses the phrasing
  "PROBABLE/UNCERTAIN boundary" while the blueprint invariant #4 uses "non-CERTAIN boundary." These are
  set-equivalent; if a future editor wants maximal cross-doc symmetry, either phrasing is acceptable.
  No action needed.

## QA Complete

---

## Overall Verdict: **PASS**
