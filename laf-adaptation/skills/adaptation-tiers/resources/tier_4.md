# Tier 4 — design commentary (ages 12-14, early formal) — INTERPOLATION, not a stored profile

*This file explains a DERIVATION. Tier 4 has **no stored profile** — there is deliberately no
`kb/tiers/tier_4.yaml`. Do NOT read this as a canonical constant set; it documents how a T4 constraint
set is computed at request time. Carried from the `/adaptation-tiers` SKILL.md §Interpolation block, the
T3 and T5 profiles it interpolates between, and `docs/design_decisions/001-five-tier-system.md` (which
authorizes the interpolation) + `003-agency-externalization.md`.*

## Why Tier 4 is interpolated rather than stored

001 lists "five profiles to maintain" as a cost of the five-tier system and offers the explicit
mitigation: **"Tier 4 can be interpolated from 3+5."** Ages 12-14 (early formal operational) sit between
the concrete-operational transition (T3) and full formal operational reasoning (T5); rather than author
and maintain a sixth stored file whose values would just be a blend, the framework derives T4 on demand.

## The derivation rule (from SKILL.md §Interpolation)

At request time, for each threshold:
- Take **T3's permitted set as the floor** and **T5's as the ceiling**.
- Choose the value at the **T3→T5 midpoint**, **rounding toward the more conservative (lower) bound**
  when a clean midpoint is ambiguous.
- Emit the result as a **derived** profile for that request only — **never persist it** as a stored tier
  file.

## The one non-interpolated value: agency_externalization

`agency_externalization` at T4 is **FORBIDDEN** — it is not midpoint-blended. T4 inherits the `tier_4_5`
bucket, and per the ladder in 003 (MANDATORY T1-2 → OPTIONAL T3 → **FORBIDDEN T4-5**), externalizing
agency at this age would be patronizing and would undermine the character complexity a 12-14-year-old can
now handle. So the interpolation floor/ceiling rule governs the graded thresholds (vocabulary, sentence
limits, permitted intensity), while agency_externalization is pinned to the T4_5 value directly.
