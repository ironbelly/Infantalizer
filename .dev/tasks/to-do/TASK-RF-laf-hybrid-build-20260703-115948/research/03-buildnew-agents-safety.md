# Research: Build-New Agents + /adaptation-safety + Genre Resources
**Topic type:** Content Extraction
**Scope:** chronicler, tier-coordinator, /adaptation-safety, children.md, ya.md, safety rubric
**Status:** Complete
**Date:** 2026-07-03

**Spec sources (CWD `/config/workspace/Infantalizer`):**
- `.dev/releases/current/0.1/design/agent-schemas.md` (§5.1 chronicler, §5.2 tier-coordinator, §6 dispatch)
- `.dev/releases/current/0.1/design/tier-coordinator.md` (FULL)
- `.dev/releases/current/0.1/design/safety-rubric.md` (FULL)
- `.dev/releases/current/0.1/design/skill-specs.md` (§4 /adaptation-safety + §4.1 genre resources)

**Ownership boundaries (per task brief):**
- I own: chronicler AGENT BODY (targets + invariants); R4 owns kb file schemas (continuity.md/decisions.md/canon-delta.md FORMAT via kb-formats §4).
- I own: the safety RUBRIC content; R2 owns the safety-verifier AGENT that runs it.
- I own: tier-coordinator agent, /adaptation-safety SKILL.md, resources/children.md, resources/ya.md.

---

## FILE 1 — `agents/chronicler.md` (BUILD-NEW, graft G1)

**Source:** agent-schemas.md §5.1 (lines 213-254), §6 dispatch table (line 300).

### Role (agent-schemas.md:215-218)
Populates durable canon **after a chapter settles and muse accepts** (workflow step 11, constraint #5:
promotion only on accept). **Tier-partitioned**: same character holds divergent canonical state per tier
(Sauron = "Grumpy King" in tier-1 canon, "the Dark Lord" in tier-5 canon). Closes the divergent-canon
bug = **graft G1**.

### Frontmatter — VERBATIM (agent-schemas.md:222-233)
```yaml
---
name: chronicler
description: Tier-aware canon extraction. After a chapter is accepted, promotes durable facts into shared kb/canon and per-tier kb/adaptations/<work>/tier-N/continuity.md. Keys all per-tier state by (work, tier, chapter).
model: sonnet
skills:
  - laf-adaptation:story-memory
  - laf-adaptation:kb-management
  - laf-adaptation:adaptation-tiers
tools: Read, Write, Glob, Grep
---
```
- `model: sonnet` (line 226). **NO Bash tool.** Skills: story-memory, kb-management, adaptation-tiers.
- Filename stem must equal `name` (§1 dialect contract, agent-schemas.md:26).

### Inputs (agent-schemas.md:235-237)
- `work`
- `chapter`
- `active_tier`  ← the partitioning key (§6 table line 300: "Yes — partitioning key: (work, tier, chapter)")
- `adapted_path` = `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/adapted.md`
- `analysis_path` = `work/analysis/ch-<NN>.yaml`

### Write targets — DUAL-LAYER (agent-schemas.md:239-249; FORMATS owned by R4/kb-formats §4)
```
SHARED (tier-invariant source truth):
  kb/canon/<work>/ch-<NN>.md        — hard source facts (APPEND; tier-neutral)
  kb/timeline/<work>.md             — chronological source entries

PER-TIER (graft G1 — the divergent layer):
  kb/adaptations/<work>/tier-<N>/continuity.md                      — running "what a Tier-N reader now knows"
  kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/canon-delta.md    — what THIS chapter changed at THIS tier
  kb/adaptations/<work>/tier-<N>/decisions.md                       — adaptation decisions log (APPEND)
```
> OWNERSHIP: FILE FORMAT/schema of continuity.md, canon-delta.md, decisions.md belongs to R4
> (kb-formats §4). This documents ONLY what the chronicler agent body WRITES (targets + invariants).

### The (work, tier, chapter) key rule + INVARIANT (agent-schemas.md:251-254) — VERBATIM
> "every per-tier write is keyed `(work, tier, chapter)`. The chronicler MUST NOT write a tier-N fact into
> another tier's `continuity.md`, and MUST NOT promote a tier-transformed name (e.g. "Grumpy King") into
> shared `kb/canon/` — shared canon holds source truth; transformed names live only in the per-tier layer."

Three body invariants to author:
1. **Keying:** every per-tier write MUST carry `(work, tier, chapter)`.
2. **No cross-tier bleed:** NEVER write a tier-N fact into another tier's `continuity.md`.
3. **No transformed-name promotion:** NEVER promote a tier-transformed name into shared `kb/canon/`
   (shared canon = source truth only; transformed names stay per-tier).

### Run gate (constraint #5)
- Runs **on muse-accept only** (agent-schemas.md:215 "after a chapter settles and muse accepts", step 11).
- Runs **per tier**, AFTER tier-coordinator returns `status: RECONCILED` (tier-coordinator.md:151-164):
  ```
  tier-coordinator.reconcile() == RECONCILED
        │
        ▼
  for tier in tiers:  chronicler(work, chapter, tier)   # writes per-tier canon, keyed (work,tier,chapter)
  ```

---

## FILE 2 — `agents/tier-coordinator.md` (BUILD-NEW, graft G2)

**Source:** agent-schemas.md §5.2 (lines 256-284) + FULL tier-coordinator.md (§1-6). Full algorithm lives
in tier-coordinator.md; frontmatter in agent-schemas.md §5.2.

### Role (agent-schemas.md:258-260; tier-coordinator.md:9-13)
Fans the transform across tiers and reconciles their outputs against shared source-canon while preserving
tier-differentiated framing (**workflow step 10**). Parallel fan-out by default; documented sequential
fallback for state-heavy works (**graft G2**). Because `analyst` runs once per chapter (tier-invariant
source truth), every tier's transform derives from the same facts — the coordinator proves they stay
consistent with source-canon while remaining tier-differentiated.

### Frontmatter — VERBATIM (agent-schemas.md:264-275)
```yaml
---
name: tier-coordinator
description: Coordinates multi-tier adaptation of one source chapter. Fans transforms across tiers (parallel default; sequential fallback for state-heavy works) and reconciles them against shared source-canon while preserving tier-differentiated framing.
model: opus
skills:
  - laf-adaptation:adaptation-tiers
  - laf-adaptation:source-fidelity
  - laf-adaptation:kb-management
tools: Read, Write, Glob, Grep, Bash
---
```
- `model: opus` (line 269). **HAS Bash tool** (line 273) — unlike chronicler. Skills: adaptation-tiers,
  source-fidelity, kb-management.

### Inputs / Outputs (tier-coordinator.md:19-32; agent-schemas.md:277-284)
```
INPUT:
  work, chapter
  tiers        ⊆ {1, 2, 3, 5}     # T4 interpolated on demand if requested
  mode         ∈ {parallel, sequential}    default = parallel
  shared_analysis = work/analysis/ch-<NN>.yaml   # the single, tier-invariant source truth

OUTPUT:
  work/analysis/ch-<NN>-cross-tier.md
  status: RECONCILED | CONFLICT
  conflicts: [ ... ]               # MUST be empty before chronicler (step 11) runs
```

### Fan-out modes (tier-coordinator.md §2, lines 36-63)

**2.1 Parallel (DEFAULT)** — each requested tier runs transform pipeline (workflow steps 3-9)
independently and concurrently, all reading the same `shared_analysis`. Common case, because source truth
is shared, not derived tier-to-tier.
```
                  ┌──► tier-1 : steps 3-9 ──► adapted.md (t1) ─┐
shared_analysis ──┼──► tier-3 : steps 3-9 ──► adapted.md (t3) ─┼──► reconcile() ──► cross-tier report
                  └──► tier-5 : steps 3-9 ──► adapted.md (t5) ─┘
```

**2.2 Sequential (FALLBACK, graft G2)** — for state-heavy works where a tier's running canon must settle
before the next is written (e.g. a mystery whose tier-1 simplification collapses a subplot tier-3 must
still reference coherently). Runs tiers **in ASCENDING order**, letting each tier's `continuity.md` settle.
```
tier-1 (steps 3-9, settle continuity) ──► tier-3 (steps 3-9, may read t1 decisions) ──► tier-5 ...
```

**Selection heuristic (tier-coordinator.md:60-63) — VERBATIM logic:**
> default `parallel`; switch to `sequential` when the work's
> `<work>-mapping.yaml.work_metadata.key_challenges` includes state-heavy markers
> (`parallel_plotlines`, `unreliable_narrator`, `nested_timeline`) **OR** the author sets
> `mode: sequential`. Sequential is strictly slower; it is a correctness fallback, not the default.

State-heavy markers (author-overridable): `parallel_plotlines`, `unreliable_narrator`, `nested_timeline`.

### reconcile() — the THREE consistency checks (tier-coordinator.md §3, lines 67-112)

**Check A — Source-fidelity consistency (single source truth)** (lines 71-82):
Every tier's transformed element must trace to the SAME shared source fact in `shared_analysis`. A tier
introducing a fact ABSENT from `shared_analysis` = hallucination ⇒ CONFLICT (violates constraint #2
downstream).
```
for tier in tiers:
    for element in transformed_elements(adapted[tier]):
        if source_trace(element) not in shared_analysis:
            conflicts += {type: "unsourced", tier, element}
```

**Check B — No downward disclosure leak** (lines 84-95):
A lower tier must not reveal what only a higher-tier reader should know at this point. The set of plot
disclosures in tier-N must be ⊆ disclosures permitted for tier-N by its `thresholds`/tier profile. A
tier-1 chapter must not disclose a death that tier-1 defers ("journey_or_sleep"), even if tier-5 states it.
```
for tier in tiers:
    for disclosure in disclosures(adapted[tier]):
        if not permitted_at(disclosure, tier_profile[tier]):
            conflicts += {type: "disclosure_leak", tier, disclosure}
```

**Check C — Framing monotonicity** (lines 97-112):
Framing maturity must be NON-DECREASING in tier. For any element transformed at multiple tiers,
`maturity(tier_N) ≤ maturity(tier_M)` whenever `N < M`. A tier-1 rendering may never be MORE mature than
the tier-3 rendering of the same element.
```
for element shared across ≥2 tiers:
    ms = [(tier, maturity(render(element, tier))) for tier in tiers]
    if not nondecreasing_by_tier(ms):
        conflicts += {type: "monotonicity", element, renderings: ms}
```
`maturity()` = ordinal, derived from element's governing `mode:` on the transformation ladder
(`mandatory`-transform < `optional`-transform < `preserve`), PLUS the tier's violence/moral-ambiguity
threshold levels from the profile. Coarse ordinal comparison, not a score — enough to catch an inverted
rendering (tier-coordinator.md:109-112).

### Output report format (tier-coordinator.md §4, lines 116-147) — VERBATIM template
`work/analysis/ch-<NN>-cross-tier.md`:
```markdown
# Cross-Tier Reconciliation — <Work> ch-<NN>

tiers: [1, 3, 5]     mode: parallel     source: work/analysis/ch-<NN>.yaml

## Shared source anchors (from analysis)
- Sauron (antagonist) — CERTAIN
- The Ring corrupts its bearer — CERTAIN
- Battle of Pelennor Fields — CERTAIN

## Per-tier renderings (traceability)
| Element | T1 | T3 | T5 | shared anchor |
|---------|----|----|----|---------------|
| Sauron  | "Grumpy King" | "Sauron (a dark lord)" | "Sauron" | characters[Sauron] |
| battle  | "The Big Tidy-Up" | "the battle (summarized)" | "the battle" | events[Pelennor] |

## Checks
- A source-fidelity: PASS (all renderings trace to shared anchors)
- B disclosure-leak:  PASS (no tier discloses beyond its threshold)
- C monotonicity:     PASS (T1 ≤ T3 ≤ T5 maturity for every shared element)

status: RECONCILED
conflicts: []
```
On **CONFLICT** (lines 145-147): `conflicts:` non-empty, lists `{type, tier, element/disclosure, detail}`.
Caller (muse) must resolve — re-dispatch offending tier's writer with the conflict as a revision note —
**BEFORE** `chronicler` promotes anything (constraint #5: no promotion of inconsistent canon).

### Ordering + chronicler interaction (tier-coordinator.md §5, lines 151-164)
`tier-coordinator` runs **BEFORE** `chronicler` (step 10 → step 11). It **NEVER writes canon**; it only
reconciles and reports. Once `RECONCILED`, `chronicler` runs per tier keyed `(work, tier, chapter)`.
Check B is the runtime enforcement of graft G1's promise (keeps each tier's continuity.md within its
disclosure envelope).

### Tier-4 handling (tier-coordinator.md §6, lines 168-173)
If `tiers` includes 4: coordinator requests an interpolated T4 profile from `/adaptation-tiers`
(skill-specs.md §1) BEFORE fan-out, treats it as an ordinary tier for Checks A/B/C. Its maturity sits
between T3 and T5 by construction (monotonicity holds by the interpolation's conservative-midpoint rule).
**No T4 profile is persisted.**

### T4 interpolation rule (from skill-specs.md:73-77, referenced by coordinator)
Take T3's permitted set as floor, T5's as ceiling; per threshold choose T3→T5 midpoint, rounding toward
the more conservative (lower) bound when ambiguous. `agency_externalization` at T4 = FORBIDDEN (inherits
T4_5 bucket). Emit as derived profile; never persist.

---

## FILE 3 — `skills/adaptation-safety/SKILL.md` (BUILD-NEW; constraint #3)

**Source:** skill-specs.md §4 (lines 251-286). Directory `skills/adaptation-safety/`. Owned by native
`safety-verifier` agent (R2 owns that agent; I own THIS skill wrapper + the rubric body content).
Carries `prompts/verification/safety_check.md`.

### Skill dialect (skill-specs.md §0, lines 14-30)
Claude-native frontmatter: `name` + `description` ONLY. NO Mars keys (`type`, `model-invocable`,
`effort`). Structure = `SKILL.md` + optional `resources/` subdir. **NO `rules/` or `templates/` subdirs**
(they don't exist in CWS; match vendored convention). Tier-conditional rule data lives as YAML inside
`resources/` markdown fences, carried verbatim from `config/`.

### Frontmatter — VERBATIM (skill-specs.md:257-266)
```yaml
---
name: adaptation-safety
description: |
  The 6-section post-generation safety rubric for Tier 1-2 children's adaptations: forbidden-content
  scan, agency-externalization check, emotional safety, safe-home schema, nightmare prevention, and
  linguistic compliance. Emits a PASS/FAIL verdict. Load when verifying children's-tier output before
  delivery. Runs on ALL Tier 1 and Tier 2 output.
---
```

### Body (skill-specs.md:268-269)
> "the 6 sections + Automatic-Failures list + verdict contract, carried **verbatim** from
> `safety_check.md`. Detailed rubric → `safety-rubric.md`."

The FULL machine-checkable rubric content = FILE 6 below (safety-rubric.md). The skill body carries the
6 sections + auto-failures + verdict contract verbatim.

### Gate: "runs on ALL T1-2" (skill-specs.md:264; safety-rubric.md:14-15)
Gate from source prompt: **"Run on ALL Tier 1 and Tier 2 outputs before delivery."** →
T1-2 **blocking**, T3 **advisory**, T4-5 **N/A**. Tier gate enforcement lives in the safety-verifier
AGENT body (R2), agent-schemas.md:102-107.

### Skill → consumer (skill-specs.md:296)
`/adaptation-safety` is loaded ONLY by `safety-verifier` (native).

---

## FILES 4 & 5 — Genre resources (BUILD-NEW; skill-specs.md §4.1, lines 271-286)

**Context (skill-specs.md:273-274):** CWS ships genre resources for
litfic/thriller/horror/fantasy/mystery/romance but **NONE for children or YA** (verified). LAF fills the
gap. These are genre *reference* resources (how to write these age bands well), **distinct from the safety
*rubric*** (the pass/fail gate). The rubric gates; the genre resources inform the writer (skill-specs.md:284-285).

Both live under `skills/adaptation-safety/resources/`.

### FILE 4 — `resources/children.md` (skill-specs.md:276-278)
Children's-fiction craft for **Tiers 1-3**. Content dimensions to author:
- prosocial centering
- episodic structure
- positive resolution
- safe-home schema
- nightmare-prevention framing
- vocabulary/sentence ceilings

**Sourcing (skill-specs.md:278):** "Sourced from the **tier-1/tier-3 transform prompts** and **tier
profiles**." Concretely:
- tier-1 / tier-3 transform prompts (the per-tier transform prompt files)
- tier profiles = `kb/tiers/tier_1.yaml` … `tier_3.yaml` (thresholds, linguistic limits) — R4's schemas
- Cross-references the rubric's Section 4 (safe-home) + Section 5 (nightmare-prevention) checklists
  (safety-rubric.md §1 sections 4-5) and Section 6 linguistic ceilings.

### FILE 5 — `resources/ya.md` (skill-specs.md:279-282)
Young-adult craft for **Tier 5**. Content dimensions to author:
- meaning-not-sanitization
- unreliable narrator + FULL irony range permitted
- **when-TO-intervene**: archaic language, historical context
- **when-NOT-to-intervene**: difficult themes, moral complexity, character deaths

**Sourcing (skill-specs.md:281-282):** "Sourced from the **tier-5 profile's `adaptation_philosophy` +
`supplementary_approach`.**" Concretely:
- `kb/tiers/tier_5.yaml` → `adaptation_philosophy` field
- `kb/tiers/tier_5.yaml` → `supplementary_approach` field
- (tier_5 profile also basis for `agency_externalization: forbidden` — "Patronizing; undermines character
  complexity", ref skill-specs.md:154)

---

## FILE 6 — Safety Rubric content (safety-rubric.md, FULL — machine-checkable verdict contract)

**Source:** safety-rubric.md §1-5. This is the content the `/adaptation-safety` SKILL body carries and the
`safety-verifier` AGENT (R2) executes. Content (word lists, sections, auto-failures) is UNCHANGED from
`prompts/verification/safety_check.md`; the spec ADDS the verdict structure + tier gate.

**Gate (safety-rubric.md:14-15):** source "Run on ALL Tier 1 and Tier 2 outputs before delivery." →
T1-2 blocking, T3 advisory, T4-5 N/A.

### The SIX sections — VERBATIM word-lists/checklists (safety-rubric.md §1, lines 19-58)

**Section 1 — Forbidden Content Scan** (lines 21-29). Scan draft for forbidden tokens
(case-insensitive, whole-word):
- **TIER 1 FORBIDDEN:** `kill, killed, slay, slew, murder, wound, blood, gore, stab, attack, fight,
  sword, weapon, die, died, dead, death`
- **TIER 2 FORBIDDEN:** `kill, killed, murder, slay, slew, blood, gore, torture, stab, die, died`
  (permitted alternatives: "passed away", "lost")
- Emit one row per hit: `{word, location, result: FAIL}`. **Any hit ⇒ section FAIL.**

**Section 2 — Agency Externalization Check** (lines 31-36). Negative outcomes must be external states or
accidents, never innate character qualities. Per character/event:
`{subject, cause_given, external: yes|no, result}`. **Any `external: no` on a negative outcome ⇒ FAIL.**
Auto-fail phrasings (violation examples): "He was evil", "Driven by greed", "She betrayed them".

**Section 3 — Emotional Safety** (lines 37-41). Permitted emotions:
- T1: `happy, sad, scared, grumpy, tired, excited, brave, kind`
- T2: adds `worried, lonely, embarrassed, proud, frustrated`
- Every negative emotion must resolve. Chapter ending checklist (ALL required): positive emotional
  state · sense of safety · problem resolved. **Any unresolved negative emotion, or any failed ending
  item ⇒ FAIL.**

**Section 4 — Safe Home Schema** (lines 43-45). Checklist (ALL required): home as safe haven · if
threatened, restored · no permanent destruction · family relationships positive. **Any unchecked ⇒ FAIL.**

**Section 5 — Nightmare Prevention** (lines 47-49). Checklist (ALL required): monsters grumpy/silly not
terrifying · darkness temporary and fixable · fear manageable. **Any unchecked ⇒ FAIL.**

**Section 6 — Linguistic Compliance** (lines 51-58). T1: max 12 words/sentence. Per over-limit sentence:
`{sentence, word_count, result: FAIL}`. Checklist: no passive voice · no complex clauses · kindergarten
vocabulary. **Any over-limit sentence or failed checklist item ⇒ FAIL.**
> Section 6 thresholds are TIER-PARAMETERIZED from `kb/tiers/tier_<N>.yaml.linguistic` (T1:
> `max_words_per_sentence: 12`, `max_clauses: 1`, `passive_voice: false`). Verifier READS the profile
> rather than hard-coding — so T2's limits come from `tier_2.yaml` (safety-rubric.md:56-58).

### Automatic Failures (override sections) — VERBATIM (safety-rubric.md §2, lines 62-70)
Regardless of section tallies, these force `result: FAIL`:
- **Tier 1:** death language · violence · "evil" · unresolved fear · internal motivation
- **Tier 2:** graphic violence · "kill/murder/slay" · prolonged hopelessness

An automatic failure is recorded in `verdict.automatic_failures[]`; if that list is non-empty the overall
verdict is FAIL even if all six section rollups read PASS.

### Aggregation logic — VERBATIM pseudocode (safety-rubric.md §3, lines 74-87)
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

### Verdict contract — MACHINE-PARSEABLE YAML block (safety-rubric.md §4, lines 91-115) — VERBATIM
Report body = human-readable 6-section fill-in (source prompt's tables). It **ENDS** with this fenced
block that the workflow reads to branch. Emitted to `work/safety-reports/ch-<NN>-t<N>.md`:
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
> NOTE: agent-schemas.md:112-119 shows a SHORTER verdict variant (no work/chapter/mode fields, inline
> `sections: { ... }`). The AUTHORITATIVE full contract is safety-rubric.md §4 (above). The skill/agent
> should emit the full §4 form; the §2.2 snippet is an abbreviated illustration.

### Workflow branch logic — VERBATIM (safety-rubric.md §4.1, lines 117-130)
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
actionable, not just a boolean (safety-rubric.md:129-130).

### Traceability table (safety-rubric.md §5, lines 134-143)
| Rubric element | Source (verbatim) | Cross-check |
|---|---|---|
| 6 sections, word lists, checklists | `prompts/verification/safety_check.md` §1-6 | — |
| Automatic Failures | `safety_check.md` "Automatic Failures" | — |
| Section 2 rule | `config/transformation_rules/thematic.yaml → agency_externalization` | `/adaptation-rules/resources/agency.md` |
| Section 3 permitted emotions | `tier_N.yaml.thresholds.emotional_complexity.permitted_emotions` | `kb/tiers/` |
| Section 6 limits | `tier_N.yaml.linguistic` | `kb/tiers/` |
| Tier gate (T1-2 only) | `safety_check.md` "Run on ALL Tier 1 and Tier 2 outputs" | `safety-verifier` body |

---

## SUMMARY

Six authorable BUILD-NEW content artifacts fully specified with verbatim frontmatter/algorithms/rubric,
each cited to spec `file:line`:

1. **`agents/chronicler.md`** (sonnet, NO Bash) — dual-layer canon writer. SHARED: `kb/canon/<work>/ch-NN.md`,
   `kb/timeline/<work>.md`; PER-TIER (graft G1): `continuity.md`, `chapters/ch-NN/canon-delta.md`,
   `decisions.md`. Invariants: key every per-tier write `(work,tier,chapter)`; NEVER cross-tier bleed;
   NEVER promote transformed name to shared canon. Runs on muse-accept only, per tier, after RECONCILED.

2. **`agents/tier-coordinator.md`** (opus, HAS Bash, graft G2) — fan-out (parallel default / sequential
   fallback via key_challenges markers `parallel_plotlines`/`unreliable_narrator`/`nested_timeline`).
   `reconcile()` 3 checks: A source-fidelity (unsourced⇒CONFLICT), B disclosure-leak, C monotonicity
   (ordinal maturity). Emits `ch-NN-cross-tier.md` with `status: RECONCILED|CONFLICT`. Runs BEFORE
   chronicler; never writes canon. T4 interpolated on demand, not persisted.

3. **`skills/adaptation-safety/SKILL.md`** (build-new) — name+description dialect, NO rules/templates
   subdirs. Body carries 6 sections + auto-failures + verdict contract verbatim from safety_check.md.
   Loaded only by safety-verifier. Gate: runs on ALL T1-2.

4. **`resources/children.md`** — T1-3 craft (prosocial, episodic, positive resolution, safe-home,
   nightmare-prevention, vocab/sentence ceilings). Sourced from tier-1/tier-3 transform prompts + tier
   profiles.

5. **`resources/ya.md`** — T5 craft (meaning-not-sanitization, unreliable narrator/full irony,
   when-to/not-to-intervene). Sourced from tier_5.yaml `adaptation_philosophy` + `supplementary_approach`.

6. **Safety rubric** (consumed by safety-verifier) — 6 sections with verbatim word-lists/checklists,
   auto-failures (T1/T2), aggregation pseudocode (N/A T4-5 → auto-fail dominates → section-fail → PASS),
   full machine-parseable `verdict:` YAML block, and workflow branch (skipped/PASS/advisory/FAIL-block-revise).

**Key cross-references for downstream researchers:**
- File FORMATS of continuity.md/canon-delta.md/decisions.md = **R4** (kb-formats §4); I own only WHAT
  chronicler writes (targets+invariants).
- safety-verifier AGENT body + tier gate = **R2**; I own the RUBRIC it runs.
- Two verdict-block variants exist: agent-schemas.md §2.2 (abbreviated) vs safety-rubric.md §4
  (authoritative full). Emit the §4 form.
- reader-sim persona payload (agent-schemas.md §4) uses `continuity.md` — cross-check with R2/R4.

**Constraint anchors:** #1 (active_tier explicit param, §6 table), #2 (source-fidelity/no hallucination,
Check A), #3 (revision loop via verdict.next=revise), #5 (promotion only on accept + only when RECONCILED).
Grafts: G1 (tier-partitioned canon, chronicler), G2 (sequential fallback, tier-coordinator).
