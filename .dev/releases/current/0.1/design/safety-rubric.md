---
title: "/adaptation-safety Rubric — machine-checkable verdict contract"
parent: DESIGN.md
status: draft
---

# `/adaptation-safety` Rubric

The 6-section safety rubric carried verbatim from `prompts/verification/safety_check.md`, specified here
as a **machine-checkable verdict contract** so `safety-verifier` emits a parseable PASS/FAIL that the
workflow can branch on (constraint #3: the revision loop). Content (word lists, sections, automatic
failures) is unchanged from the source prompt — this spec adds the verdict structure and the tier gate.

**Gate (from source):** "Run on ALL Tier 1 and Tier 2 outputs before delivery." → T1-2 blocking, T3
advisory, T4-5 N/A ([`agent-schemas.md §2.2`](agent-schemas.md)).

---

## 1. The six sections (verbatim content)

### Section 1 — Forbidden Content Scan
Scan the draft for forbidden tokens (case-insensitive, whole-word).

- **TIER 1 FORBIDDEN:** `kill, killed, slay, slew, murder, wound, blood, gore, stab, attack, fight,
  sword, weapon, die, died, dead, death`
- **TIER 2 FORBIDDEN:** `kill, killed, murder, slay, slew, blood, gore, torture, stab, die, died`
  (permitted alternatives: "passed away", "lost")

Emit one row per hit: `{word, location, result: FAIL}`. Any hit ⇒ section FAIL.

### Section 2 — Agency Externalization Check
Negative outcomes must be external states or accidents, never innate character qualities. Per
character/event: `{subject, cause_given, external: yes|no, result}`. Any `external: no` on a negative
outcome ⇒ FAIL. Violation examples (auto-fail phrasings): "He was evil", "Driven by greed", "She betrayed
them".

### Section 3 — Emotional Safety
Permitted emotions — T1: `happy, sad, scared, grumpy, tired, excited, brave, kind`; T2: adds `worried,
lonely, embarrassed, proud, frustrated`. Every negative emotion must resolve. Chapter ending checklist
(all required): positive emotional state · sense of safety · problem resolved. Any unresolved negative
emotion, or any failed ending item ⇒ FAIL.

### Section 4 — Safe Home Schema
Checklist (all required): home as safe haven · if threatened, restored · no permanent destruction ·
family relationships positive. Any unchecked ⇒ FAIL.

### Section 5 — Nightmare Prevention
Checklist (all required): monsters grumpy/silly not terrifying · darkness temporary and fixable · fear
manageable. Any unchecked ⇒ FAIL.

### Section 6 — Linguistic Compliance
T1: max 12 words/sentence. Per over-limit sentence: `{sentence, word_count, result: FAIL}`. Checklist:
no passive voice · no complex clauses · kindergarten vocabulary. Any over-limit sentence or failed
checklist item ⇒ FAIL.

> Section 6 thresholds are tier-parameterized from `kb/tiers/tier_<N>.yaml.linguistic` (T1:
> `max_words_per_sentence: 12`, `max_clauses: 1`, `passive_voice: false`). The verifier reads the profile
> rather than hard-coding — so T2's limits come from `tier_2.yaml`.

---

## 2. Automatic Failures (override sections)

Regardless of section tallies, these force `result: FAIL`:

- **Tier 1:** death language · violence · "evil" · unresolved fear · internal motivation
- **Tier 2:** graphic violence · "kill/murder/slay" · prolonged hopelessness

An automatic failure is recorded in `verdict.automatic_failures[]`; if that list is non-empty the overall
verdict is FAIL even if all six section rollups read PASS.

---

## 3. Rubric aggregation logic

```
per section S:  S.result = FAIL if any row/checklist item in S failed, else PASS
automatic_failures = [ f for f in AUTO_FAIL[tier] if detected(f, draft) ]

overall =
    N/A   if tier in {4, 5}
    else FAIL if automatic_failures != []           # auto-fails dominate
    else FAIL if any section.result == FAIL
    else PASS

next = "revise" if overall == FAIL else "promote"    # tier 3 advisory: next always "promote", report-only
```

---

## 4. Verdict contract (emitted to `work/safety-reports/ch-<NN>-t<N>.md`)

The report body is the human-readable 6-section fill-in (the source prompt's tables). It **ends** with
this fenced, machine-parseable block that the workflow reads to branch:

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

### 4.1 How the workflow branches on it

```
run safety-verifier(draft, active_tier) → verdict
if verdict.mode == "skipped":            proceed to reader-sim (step 9)          # T4-5
elif verdict.result == "PASS":           proceed to reader-sim (step 9)
elif verdict.mode == "advisory":         attach report; proceed (T3, non-blocking)
else:  # FAIL, blocking (T1-2)
    block kb promotion
    return to workflow step 3 (writer) with verdict.evidence as revision notes   # constraint #3 loop
```

`verdict.evidence` feeds directly back to the writer as concrete, located revision targets — the loop is
actionable, not just a boolean.

---

## 5. Traceability

| Rubric element | Source (verbatim) | Cross-check |
|---|---|---|
| 6 sections, word lists, checklists | `prompts/verification/safety_check.md` §1-6 | — |
| Automatic Failures | `safety_check.md` "Automatic Failures" | — |
| Section 2 rule | `config/transformation_rules/thematic.yaml → agency_externalization` | `/adaptation-rules/resources/agency.md` |
| Section 3 permitted emotions | `tier_N.yaml.thresholds.emotional_complexity.permitted_emotions` | `kb/tiers/` |
| Section 6 limits | `tier_N.yaml.linguistic` | `kb/tiers/` |
| Tier gate (T1-2 only) | `safety_check.md` "Run on ALL Tier 1 and Tier 2 outputs" | `safety-verifier` body |
