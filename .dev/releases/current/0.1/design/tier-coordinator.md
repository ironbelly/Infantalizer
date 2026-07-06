---
title: "tier-coordinator — reconciliation algorithm"
parent: DESIGN.md
status: draft
---

# `tier-coordinator` — Multi-Tier Reconciliation

The build-new agent that fans one source chapter across tiers and reconciles the outputs (workflow step
10). Resolves Q1.5 / Q2.7: **parallel fan-out by default, sequential fallback for state-heavy works**
(graft G2). Because `analyst` runs once per chapter (tier-invariant source truth), every tier's transform
derives from the same facts — the coordinator's job is to prove they stay consistent with source-canon
while remaining tier-differentiated.

Agent frontmatter: [`agent-schemas.md §5.2`](agent-schemas.md).

---

## 1. Inputs / outputs

```
INPUT:
  work, chapter
  tiers        ⊆ {1, 2, 3, 5}     # T4 interpolated on demand if requested
  mode         ∈ {parallel, sequential}    default = parallel
  shared_analysis = work/analysis/ch-<NN>.yaml   # the single, tier-invariant source truth

OUTPUT:
  work/analysis/ch-<NN>-cross-tier.md
  status: RECONCILED | CONFLICT
  conflicts: [ ... ]               # must be empty before chronicler (step 11) runs
```

---

## 2. Fan-out modes

### 2.1 Parallel (default)

Each requested tier runs the transform pipeline (workflow steps 3-9) **independently and concurrently**,
all reading the same `shared_analysis`. Suitable when tier-N canon does not depend on tier-N being written
first — the common case, because source truth is shared, not derived tier-to-tier.

```
                  ┌──► tier-1 : steps 3-9 ──► adapted.md (t1) ─┐
shared_analysis ──┼──► tier-3 : steps 3-9 ──► adapted.md (t3) ─┼──► reconcile() ──► cross-tier report
                  └──► tier-5 : steps 3-9 ──► adapted.md (t5) ─┘
```

### 2.2 Sequential (fallback, graft G2)

For **state-heavy works** where a tier's running canon must settle before the next tier is written (e.g.
a mystery whose tier-1 simplification collapses a subplot that tier-3 must still be able to reference
coherently). Runs tiers **in ascending order**, letting each tier's `continuity.md` settle first.

```
tier-1 (steps 3-9, settle continuity) ──► tier-3 (steps 3-9, may read t1 decisions) ──► tier-5 ...
```

**Selection heuristic (documented degradation, author-overridable):** default `parallel`; switch to
`sequential` when the work's `<work>-mapping.yaml.work_metadata.key_challenges` includes state-heavy
markers (`parallel_plotlines`, `unreliable_narrator`, `nested_timeline`) **or** the author sets
`mode: sequential`. Sequential is strictly slower; it is a correctness fallback, not the default.

---

## 3. `reconcile()` — the three consistency checks

For the set of per-tier `adapted.md` outputs of one chapter, assert:

### Check A — Source-fidelity consistency (single source truth)
Every tier's transformed element must trace to the **same** shared source fact in `shared_analysis`. If
tier-1 "Grumpy King wants the shiny tidied away" and tier-5 "Sauron seeks the Ring's power" both trace to
`shared_analysis.characters[Sauron]` + the ring event — consistent. If a tier introduces a fact **absent
from `shared_analysis`**, that's a hallucination ⇒ CONFLICT (the tier violated constraint #2 downstream).

```
for tier in tiers:
    for element in transformed_elements(adapted[tier]):
        if source_trace(element) not in shared_analysis:
            conflicts += {type: "unsourced", tier, element}
```

### Check B — No downward disclosure leak
A lower tier must not reveal what only a higher-tier reader should know at this point. Concretely: the set
of **plot disclosures** in tier-N must be ⊆ the disclosures permitted for tier-N by its
`thresholds`/tier profile. A tier-1 chapter must not disclose a death that tier-1 defers
("journey_or_sleep"), even if tier-5 states it plainly.

```
for tier in tiers:
    for disclosure in disclosures(adapted[tier]):
        if not permitted_at(disclosure, tier_profile[tier]):
            conflicts += {type: "disclosure_leak", tier, disclosure}
```

### Check C — Framing monotonicity
Framing maturity must be **non-decreasing** in tier. For any element transformed at multiple tiers,
`maturity(tier_N) ≤ maturity(tier_M)` whenever `N < M`. A tier-1 rendering may never be *more* mature
than the tier-3 rendering of the same element.

```
for element shared across ≥2 tiers:
    ms = [(tier, maturity(render(element, tier))) for tier in tiers]
    if not nondecreasing_by_tier(ms):
        conflicts += {type: "monotonicity", element, renderings: ms}
```

`maturity()` is ordinal, derived from the element's governing `mode:` on the transformation ladder
(`mandatory`-transform < `optional`-transform < `preserve`), plus the tier's violence/moral-ambiguity
threshold levels from the profile. It is a coarse ordinal comparison, not a score — enough to catch an
inverted rendering.

---

## 4. Output report format

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

On `CONFLICT`, `conflicts:` is non-empty and lists `{type, tier, element/disclosure, detail}`. The caller
(muse) must resolve — by re-dispatching the offending tier's writer with the conflict as a revision note —
**before** `chronicler` promotes anything (constraint #5: no promotion of inconsistent canon).

---

## 5. Interaction with chronicler and the (work, tier, chapter) key

`tier-coordinator` runs **before** `chronicler` (step 10 → step 11). It never writes canon; it only
reconciles and reports. Once `status: RECONCILED`, `chronicler` runs **per tier**, each writing that
tier's `continuity.md` / `canon-delta.md` keyed `(work, tier, chapter)` ([`kb-formats.md §4`](kb-formats.md)).
The coordinator's Check B is what guarantees each tier's `continuity.md` stays within that tier's
disclosure envelope — the runtime enforcement of graft G1's promise.

```
tier-coordinator.reconcile() == RECONCILED
        │
        ▼
for tier in tiers:  chronicler(work, chapter, tier)   # writes per-tier canon, keyed (work,tier,chapter)
```

---

## 6. Tier-4 handling

If `tiers` includes 4, the coordinator requests an interpolated T4 profile from `/adaptation-tiers`
([`skill-specs.md §1`](skill-specs.md)) before fan-out, and treats it as an ordinary tier for Checks
A/B/C (its maturity sits between T3 and T5 by construction, so monotonicity holds by the interpolation's
conservative-midpoint rule). No T4 profile is persisted.
