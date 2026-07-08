---
title: "Prep Package File Schemas"
parent: DESIGN.md
status: draft
---

# Prep Package File Schemas

Concrete formats for all 8 files in `work/prep/<work-slug>/`, the challenge taxonomy with its confirmed
`human_judgment_dimension` flag defaults (Q3), the `30-mapping.yaml` `meaning:` extension and dual-form
promotion (spec-correction C2), and the seed exemplar set (R13). Paths are governed by
[`path-contract.md`](path-contract.md); do not restate them.

---

## 1. `00-work-context.md` — RESEARCH (context track)

Written by `prep-cordinator` from the `web-researcher` dispatch. Markdown with a YAML front-block.

```markdown
---
work: <work-slug>
title: "<full title>"
author: "<author>"
context_confidence: PROBABLE        # ceiling PARTIAL/MEMORY — secondary sources only
source_access_declaration: FULL | PARTIAL   # the TEXT-track access declared in Stage 1b (echoed here)
---

# Work Context — <title>

## Author & era
## Genre & form
## Reception & cultural weight   (why faithful adaptation matters — feeds meaning:)
## Known adaptation history      (prior adaptations, what they changed)
## Source-access declaration     (path, FULL/PARTIAL, how verified)
```

Every claim carries an inline confidence tag (CERTAIN/PROBABLE/UNCERTAIN); context-track claims **cannot**
exceed PROBABLE (secondary-source ceiling, R6).

---

## 2. `10-challenges.yaml` — DERIVED (the challenge taxonomy)

Derived from `20-analysis-work-level.yaml`. Each challenge is a typed entry; the `human_judgment_dimension`
flag drives the question gate (R7); `compound_scene` entries carry the §2.1 reconciliation result (R11).

```yaml
work: <work-slug>
derived_from: 20-analysis-work-level.yaml
challenges:
  - type: sacrifice-and-return          # matches an exemplar (see §7)
    governing_rule: death_handling        # /adaptation-rules category (or tier-profile rule)
    human_judgment_dimension: true        # → the gate MUST ask (death honor / how much to imply)
    per_tier_strategy:
      tier_1: "trade a long rest, wake warm; omit binding/knife/death"
      tier_2: "a long rest to fix a mistake; gentle stakes"
      tier_3: "gives his life; dies and returns by deeper magic"
      tier_5: "preserve — sacrificial death and resurrection intact"
    compound_scene: false
    meaning_ref: "redemptive substitution — must survive at every tier"
  - type: petrification-body-horror
    governing_rule: violence                # direct-payload category (no mode:) — applied MANDATORY
    human_judgment_dimension: true
    per_tier_strategy: { tier_1: "playing statues", tier_3: "real petrification", tier_5: "preserve" }
    compound_scene: false
  - type: mass-warfare
    governing_rule: conflict_to_cooperation | conflict_handling   # key-tolerant (schema drift)
    human_judgment_dimension: true          # battle-scope is human judgment
    per_tier_strategy: { tier_1: "The Big Tidy-Up", tier_3: "summarize, show stakes", tier_5: "preserve" }
    compound_scene: false
  - type: violence-level
    governing_rule: violence
    human_judgment_dimension: false         # DETERMINISTIC — the gate MUST NOT ask
    per_tier_strategy: { tier_1: "none on-page", tier_3: "bounded", tier_5: "preserve" }
    compound_scene: false
  - type: death-euphemism
    governing_rule: death_euphemism | death_handling
    human_judgment_dimension: false         # DETERMINISTIC (journey_or_sleep at T1) — MUST NOT ask
    per_tier_strategy: { tier_1: "journey_or_sleep", tier_3: "named, gentle", tier_5: "preserve" }
    compound_scene: false
compound_scenes:                            # populated when analyst sets compound_scene: true (R11)
  - scene: "<name>"
    cooccurring_flags: [death, emotional]
    reconciliation:                         # baked in from /prep §2.1
      emotional_core: "<what the reader must feel>"
      decomposition: ["<element 1>", "<element 2>"]
      per_tier: { tier_1: "...", tier_3: "...", tier_5: "..." }
      meaning_survives: true
```

### 2.1 `human_judgment_dimension` flag defaults (Q3 — CONFIRMED)

The shipped per-type flag set. The gate asks iff `true`; never asks the deterministic (`false`) rows.

| Challenge type | `human_judgment_dimension` | Rationale |
|---|---|---|
| `sacrifice-and-return` (death honor) | **true** | how much of the death to imply is an authorial-taste call |
| allegory-stance | **true** | "neither add nor strip the allegory" is a stance decision |
| omission-honor-set | **true** | *what* must be omitted vs preserved is judgment |
| target-age-nuance | **true** | precise age band within a tier shifts many calls |
| mass-warfare / battle-scope | **true** | how much battle to show is judgment |
| petrification-body-horror | **true** | reframe vs restore is a taste threshold |
| psychological-collapse | **true** | how much despair to imply (e.g. Denethor) |
| violence-level | **false** | deterministic tier-profile threshold |
| death-euphemism | **false** | deterministic (`journey_or_sleep` at T1) |

*(Matches the spec's confirmed set: death→yes, allegory→yes, violence-level→no, petrification→yes,
battle-scope→yes; extended with the coherent human-judgment items named in R7.)*

---

## 3. `20-analysis-work-level.yaml` — SOURCE (text track)

The `analyst` work-mode output. Extends the `/source-fidelity` v2.0 schema (the shared source of truth)
with `meaning` and `compound_scene` (R10/R11) and a work-level `metadata`.

```yaml
status: OK | ABORTED                    # ABORTED ⇒ Phase-0 NO-ACCESS; the whole prep halts
metadata:
  work: <work-slug>
  granularity: work                     # vs. per-chapter
  source_access: FULL | PARTIAL         # MEMORY-BASED/NO-ACCESS not acceptable at work level (Q1)
  confidence: CERTAIN | PROBABLE | UNCERTAIN   # min across essentials (mechanical, per /source-fidelity)
essentials:                             # work-level: title, author, structure
  title: {value: "...", confidence: CERTAIN}
  author: {value: "...", confidence: CERTAIN}
characters:
  - {name: "...", role: "...", confidence: CERTAIN}
events:                                 # major work-level beats
  - {seq: 1, event: "...", confidence: CERTAIN}
summary: {text: "...", confidence: PROBABLE}
transformation_flags:
  violence:  {instances: N, severity: low|med|high}
  death:     {instances: N, severity: low|med|high}
  emotional: {instances: N, severity: low|med|high}
  abstract:  {instances: N, severity: low|med|high}
meaning:                                # R10 — work-level meaning to preserve
  value: "<the allegory/theme/moral center to neither add nor strip>"
  confidence: PROBABLE
compound_scene: true                    # R11 — any scene with ≥2 high-severity flags co-occurring
compound_scenes:
  - {scene: "<name>", cooccurring_flags: [death, emotional], severity: high}
uncertainties:
  - "items the analyst could not verify"
```

On `status: ABORTED` the file carries only `status` + the NO-ACCESS reason; the prep-cordinator surfaces
the abort and stops.

---

## 4. `30-mapping.yaml` — DERIVED (the scored work-mapping) + dual-form promotion

Derived by `/prep §4` from `20` + `10`. Reuses the shipped `<work>_mapping` schema
(`work_metadata, characters, concepts, key_scenes, master_translation_table` — `ADDING_NEW_WORKS.md`) and
**adds a top-level `meaning:` key** (R10). Every entry carries dual confidence and the effective
`min(text,context)`.

```yaml
# 6-KEY 0.1 FORM (what lives at work/prep/<slug>/30-mapping.yaml and kb/adaptation-mapping/<slug>-mapping.yaml)
meaning:                                # ← the 6th key; 0.1-only extension
  value: "<work-level meaning>"
  text_confidence: PROBABLE
  context_confidence: PROBABLE
  confidence: PROBABLE                  # = min(text, context)
work_metadata:
  title: "..."
  author: "..."
  key_challenges: ["...", "..."]        # sourced from 10-challenges.yaml types
characters:
  <name>:
    tier_1: {name: "...", archetype: "...", _confidence: {text: CERTAIN, context: PROBABLE, eff: PROBABLE}}
    tier_3: {can_show: "...", _confidence: {text: PROBABLE, context: PROBABLE, eff: PROBABLE}}
concepts:
  <concept>: {tier_1: "...", tier_3: "...", _confidence: {text: ..., context: ..., eff: ...}}
key_scenes:
  <scene>:
    challenges: ["death", "emotional"]  # links to 10-challenges compound_scenes when applicable
    tier_1: {name: "...", framing: "...", omit: ["..."]}
    tier_3: {approach: "..."}
master_translation_table:
  - {original: "...", tier_1: "...", principle: "...", _confidence: {eff: PROBABLE}}
```

**Confidence inheritance (R12):** each entry's effective confidence = `min(text_confidence,
context_confidence)`. An entry derived from a MEMORY-BASED/UNCERTAIN fact **inherits** UNCERTAIN. This is
what "scores the mapping's quality" — the closure of eval gap #3.

### 4.1 Dual-form promotion (spec-correction C2)

On greenlight, `/kb-management` writes two forms:

| Target | Form | `meaning:`? | Schema |
|---|---|---|---|
| `kb/adaptation-mapping/<slug>-mapping.yaml` (0.1, hyphen) | 6-key | **kept** | 0.1 extension |
| `config/concept_mapping/templates/<slug>_mapping.yaml` (root, underscore) | 5-key | **STRIPPED** | frozen root schema (validates to the 5 keys per `ADDING_NEW_WORKS.md` step 6) |

The `_confidence` annotation keys are 0.1-only diagnostics; the root 5-key copy also drops them, so it
validates byte-identically against the shipped `tolkien_mapping.yaml` shape. Root gains **no** meaning
concept and **no** new machinery (R14).

---

## 5. `40-prep-brief.md` — SYNTHESIS  &  `60-handoff-prompt.md` — HANDOFF

**`40-prep-brief.md`** — the human-readable package (also one of the 3 files the rewrite phase reads):

```markdown
# Prep Brief — <title>  (<work-slug>)

## Decisions ratified            (from the question gate + greenlight)
## Cross-tier spine summary      (per-tier strategy at a glance, from 10-challenges)
## Meaning to preserve           (the work-level meaning: + confidence)
## Answered questions            (Q → answer | DEFAULTED)
## Open risks / low-confidence entries   (every UNCERTAIN mapping entry, surfaced)
```

**`60-handoff-prompt.md`** — exactly the paste-able text, nothing else:

```markdown
/laf:rewrite --work <work-slug>
```

---

## 6. `50-greenlight.md` — GATE

```markdown
---
work: <work-slug>
status: PENDING            # → CONFIRMED on user confirmation (Stage 7)
tiers_active: [1, 2, 3, 5] # default all four (Q4); greenlight may narrow
---

# Greenlight — <title>

## Checklist
- [ ] Source access declared (FULL | PARTIAL) and text-track grounded
- [ ] Mapping confidence ceiling acknowledged (lowest effective confidence = <tag>)
- [ ] Tier set confirmed (default {1,2,3,5}; narrowed to: …)
- [ ] Key decisions ratified (list)

## User confirmation
<confirmation text captured here; flips status PENDING → CONFIRMED>
```

`/laf:rewrite` refuses to proceed unless `status: CONFIRMED` (see [`prep-agent-schemas.md §5.2`](prep-agent-schemas.md)).

---

## 7. Seed exemplar set (R13)

Three challenge-typed **verified-method** exemplars, NATIVE files under the (NATIVE) `adaptation-rules`
skill — **not adopted** (spec-correction C3/C4). Path:

```
laf-adaptation/skills/adaptation-rules/resources/exemplars/
  sacrifice-and-return.md
  betrayal-and-redemption.md
  petrification-body-horror.md
```

Each file MUST open with the structural marker, then illustrate the reconciliation method per tier:

```markdown
<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->

# Exemplar — Sacrifice-and-Return (method illustration; NOT source truth)

## Challenge shape
<the general pattern: a sacrificial death followed by return>

## Method by tier
- Tier 1: <find emotional core → decompose → convert/omit → verify meaning>
- Tier 3: <restore>
- Tier 5: <preserve>

## Meaning that must survive
<the redemptive-substitution meaning; the tier changes the surface, not the meaning>
```

- The `writer` loads the matching exemplar via `/adaptation-rules` when `analyst` flags that challenge type
  (`writer` already imports `/adaptation-rules` — the ADOPTED-PATCHED line).
- Exemplars live **outside** `work/` and `kb/canon/` (the source-truth paths), so a downstream agent
  cannot present them as verified source (closes the Q2 contamination risk).
- **VENDOR:** covered by the existing `skills/adaptation-rules/**` NATIVE glob row — **no new row**.

---

## 8. `70-traceability.md` — DERIVED (audit only)

```markdown
# Traceability — <title>

Consumer: HUMAN review + the greenlight decision only (Q2). The rewrite-phase muse does NOT read this;
muse uses 30-mapping.yaml's inline per-entry confidence.

## Artifact provenance
| Artifact | Derived from | Gap closed | Confidence |
|---|---|---|---|
| 30-mapping characters.<x>.tier_1 | 20 §characters + 10 §<type> | #3 | PROBABLE (min(text,context)) |
| exemplar: sacrifice-and-return | method illustration (DERIVED) | #4 | n/a (not source) |

## Mapping entry ledger
<one row per mapping entry → its derived-from facts + effective confidence + any DEFAULTED question>

## DEFAULTED questions
<every [skip] from the question gate, recorded here>
```

The whole-package provenance matrix is B's "belt-and-suspenders" over the per-entry inline confidence
(R13): inline confidence travels with the mapping into rewrite; this matrix proves the package's
provenance for the human greenlight audit.
