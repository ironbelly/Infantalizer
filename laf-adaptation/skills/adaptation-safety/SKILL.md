---
name: adaptation-safety
description: |
  The 6-section post-generation safety rubric for Tier 1-2 children's adaptations: forbidden-content
  scan, agency-externalization check, emotional safety, safe-home schema, nightmare prevention, and
  linguistic compliance. Emits a PASS/FAIL verdict. Load when verifying children's-tier output before
  delivery. Runs on ALL Tier 1 and Tier 2 output.
---

# Adaptation Safety — 6-section rubric

The post-generation safety gate for Tier 1-2 children's adaptations, carried verbatim from
`prompts/verification/safety_check.md` and specified as a machine-checkable verdict contract. **Run on ALL
Tier 1 and Tier 2 outputs before delivery.** Loaded ONLY by the native `safety-verifier` agent (it is the
rubric the verifier executes; it is not loaded by the writer — the writer is *informed* by the genre
resources `resources/children.md` / `resources/ya.md`, which are distinct from this gate).

## Section 1 — Forbidden Content Scan
Scan the draft for forbidden tokens (case-insensitive, whole-word).
- **TIER 1 FORBIDDEN:** `kill, killed, slay, slew, murder, wound, blood, gore, stab, attack, fight,
  sword, weapon, die, died, dead, death`
- **TIER 2 FORBIDDEN:** `kill, killed, murder, slay, slew, blood, gore, torture, stab, die, died`
  (permitted alternatives: "passed away", "lost")

Emit one row per hit: `{word, location, result: FAIL}`. Any hit ⇒ section FAIL.

## Section 2 — Agency Externalization Check
Negative outcomes must be external states or accidents, never innate character qualities. Per
character/event: `{subject, cause_given, external: yes|no, result}`. Any `external: no` on a negative
outcome ⇒ FAIL. Violation examples (auto-fail phrasings): "He was evil", "Driven by greed", "She betrayed
them".

## Section 3 — Emotional Safety
Permitted emotions — T1: `happy, sad, scared, grumpy, tired, excited, brave, kind`; T2: adds `worried,
lonely, embarrassed, proud, frustrated`. Every negative emotion must resolve. Chapter ending checklist
(all required): positive emotional state · sense of safety · problem resolved. Any unresolved negative
emotion, or any failed ending item ⇒ FAIL.

## Section 4 — Safe Home Schema
Checklist (all required): home as safe haven · if threatened, restored · no permanent destruction ·
family relationships positive. Any unchecked ⇒ FAIL.

## Section 5 — Nightmare Prevention
Checklist (all required): monsters grumpy/silly not terrifying · darkness temporary and fixable · fear
manageable. Any unchecked ⇒ FAIL.

## Section 6 — Linguistic Compliance
T1: max 12 words/sentence. Per over-limit sentence: `{sentence, word_count, result: FAIL}`. Checklist:
no passive voice · no complex clauses · kindergarten vocabulary. Any over-limit sentence or failed
checklist item ⇒ FAIL.

> Section 6 thresholds are **tier-parameterized from `kb/tiers/tier_<N>.yaml.linguistic`** (T1:
> `max_words_per_sentence: 12`, `max_clauses: 1`, `passive_voice: false`). The verifier **reads the
> profile at runtime rather than hard-coding** — so T2's limits come from `tier_2.yaml`.

## Automatic Failures (override sections)
Regardless of section tallies, these force `result: FAIL`:
- **Tier 1:** death language · violence · "evil" · unresolved fear · internal motivation
- **Tier 2:** graphic violence · "kill/murder/slay" · prolonged hopelessness

An automatic failure is recorded in `verdict.automatic_failures[]`; if that list is non-empty the overall
verdict is FAIL even if all six section rollups read PASS.

## Aggregation logic
```
per section S:  S.result = FAIL if any row/checklist item in S failed, else PASS
automatic_failures = [ f for f in AUTO_FAIL[tier] if detected(f, draft) ]

overall =
    N/A   if tier in {4, 5}
    else FAIL if automatic_failures != []           # auto-fails dominate
    else FAIL if any section.result == FAIL
    else PASS

next = "revise" if overall == FAIL else "promote"    # shorthand — see "Operational reading of next" below: revise ONLY when mode==blocking AND result==FAIL; tier 3 advisory always "promote", report-only
```

**Operational reading of `next` — align with `safety-verifier.md`'s deterministic rule (additive note).**
The one-line formula above is a shorthand; the authoritative, deterministic predicate (matching
`safety-verifier.md`'s "Deterministic `next` rule") is: **`next = revise` ONLY when
(`mode == blocking` AND `result == FAIL`); in every other case `next = promote`.** Concretely:
`mode == advisory` (T3) → `promote` even on a rubric FAIL (advisory never blocks — the report is attached,
not looped); `mode == skipped` (T4-5) → `promote`; `result == PASS` (any mode) → `promote`. Only the
blocking-AND-FAIL combination re-enters the writer loop. Read the shorthand `overall == FAIL` above as
scoped to blocking mode; the two files agree that a T3-advisory FAIL still promotes.

## Verdict contract (emitted to `work/safety-reports/ch-<NN>-t<N>.md`)
The report body is the human-readable 6-section fill-in. It **ends** with this fenced, machine-parseable
block that the workflow reads to branch:
```yaml
verdict:
  work: <work>
  chapter: <NN>
  tier: <N>
  result: PASS | FAIL | N/A
  sections:
    forbidden_content:       PASS | FAIL
    agency_externalization:  PASS | FAIL
    emotional_safety:        PASS | FAIL
    safe_home:               PASS | FAIL
    nightmare_prevention:    PASS | FAIL
    linguistic:              PASS | FAIL
  automatic_failures: []          # e.g. ["tier1:death_language", "tier1:internal_motivation"]
  mode: blocking | advisory | skipped   # blocking (T1-2), advisory (T3), skipped (T4-5)
  next: promote | revise
  evidence:
    - {section: forbidden_content, word: "sword", location: "para 4, sentence 2"}
    - {section: agency_externalization, subject: "the king", cause_given: "was cruel", external: false}
```
`verdict.evidence` feeds directly back to the writer as concrete, located revision targets on a blocking
FAIL (the constraint #3 revision loop).
