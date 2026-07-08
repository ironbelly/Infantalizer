# HARD-GATE Condition 1 — v2.0 CERTAIN/PROBABLE/UNCERTAIN tags present

**Verdict:** ✅ **PASS**

**Evidence** (`laf-adaptation/work/analysis/ch-01.yaml`, per skill-specs.md §3.2):
- `status: OK` (NOT ABORTED) — the analyst ran the v2.0 protocol to completion.
- `source_access: FULL` — a valid source-access declaration is present (the Phase-0 gate resolved to FULL,
  not NO-ACCESS).
- Confidence tags present on essentials/characters/events/summary: **16 `confidence: CERTAIN`** + **3
  `confidence: PROBABLE`** across the analysis. Every essential fact carries a tag.
- `metadata.confidence: PROBABLE` (overall = worst-case across essentials, per the F5 rule).

**Gaps:** none. The v2.0 Pragmatic Verification Protocol tags are present and the status is OK — proving
the analyst ran the anti-hallucination protocol (constraint #2).
