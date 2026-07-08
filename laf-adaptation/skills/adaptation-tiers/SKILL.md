---
name: adaptation-tiers
description: |
  The five-tier developmental adaptation axis (Piaget/Kohlberg grounded). Load whenever choosing or
  applying tier-appropriate constraints: vocabulary, sentence limits, permitted violence/emotion/moral
  ambiguity, and the transformation-mode ladder. Tier 4 is interpolated from tiers 3 and 5.
---

# Adaptation Tiers

One axis, five tiers, grounded in developmental psychology. The active tier is always passed as an
explicit `active_tier` parameter — never inferred from genre or persona.

| Tier | Ages | Piaget | Kohlberg | Paradigm |
|------|------|--------|----------|----------|
| 1 | 3-5   | preoperational          | 1 | Maximum transformation, maximum safety |
| 2 | 6-8   | early concrete operational | 2 | Conflict as contest/competition |
| 3 | 9-11  | concrete operational    | 3 | TRANSITION — complexity unlocked |
| 4 | 12-14 | early formal (interpolated) | 4 | Interpolated from T3+T5 (see §Interpolation) |
| 5 | 15-17 | formal operational      | 5 | Minimal transformation — preserve author intent |

## Loading a tier profile
Read `kb/tiers/tier_<N>.yaml` for the full profile (thresholds, linguistic limits, transformation_rules).
The profile is the authoritative per-tier constraint set. See `resources/tier_<N>.md` for the design
commentary on WHY each threshold is set where it is.

## The transformation-mode ladder (cross-cutting)
Every transformation rule uses a per-tier `mode:` enum. The Agency-Externalization ladder is the
signature case: MANDATORY (T1-2) → OPTIONAL (T3) → FORBIDDEN (T4-5). Full rules live in
`/adaptation-rules`; this skill only supplies the tier definitions they key against.

## Interpolation (Tier 4)
Tier 4 has no stored profile. Interpolate at request time: take T3's permitted set as the floor and T5's
as the ceiling; for each threshold, choose the value at the T3→T5 midpoint, rounding toward the more
conservative (lower) bound when ambiguous. `agency_externalization` at T4 = FORBIDDEN (inherits the T4_5
bucket). Emit interpolated T4 constraints as a derived profile; never persist them as a stored tier file.

### Interpolation by threshold type (operational reading of "round toward conservative")
The rule above is authoritative; this subsection makes it executable by naming, per threshold TYPE, what
"midpoint, rounding toward the more conservative bound" concretely means. It does not add or change any
constraint — it is the operational reading of the already-present rule.

- **Numeric scalar** (e.g. `max_sentence_length`, `max_syllables`, any integer/float limit): take the
  arithmetic midpoint of the T3 and T5 values, then **floor-round** (round down toward the more
  conservative / more restrictive bound). Example: T3=15, T5=25 → midpoint 20 → T4=20; T3=15, T5=20 →
  midpoint 17.5 → floor → T4=17.
- **Enumerated permitted / forbidden lists** (e.g. permitted-vocabulary sets, allowed-theme lists):
  T4 = **T3's permitted set (the floor)**. Items that are unique to T5 (present at T5 but absent at T3)
  are **EXCLUDED** from T4. This keeps T4 no more permissive than the concrete-operational T3 floor.
- **Boolean flags** (e.g. a permit/forbid toggle): T4 **inherits the T3 value**. `agency_externalization`
  is the pinned exception and stays **FORBIDDEN** per the rule above (it does not inherit T3's OPTIONAL).
- **Grade-level / other string values** (e.g. reading-grade band, register label): inherit the **T3
  (more restrictive)** value; do not average or blend strings.

In all four cases, when a value is genuinely ambiguous or unclassifiable, default to the T3 (lower/more
conservative) bound — never the T5 ceiling.
