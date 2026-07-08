# Tier 1 — design commentary (ages 3-5, preoperational)

*Rationale only — the authoritative T1 constraint data lives in `kb/tiers/tier_1.yaml`. This file
explains WHY the thresholds sit where they do, carried from `docs/design_decisions/001-five-tier-system.md`
and `003-agency-externalization.md`.*

## Why Tier 1 is "maximum transformation, maximum safety"

Piaget places ages 3-5 in the **preoperational** stage; Kohlberg's moral reasoning is at **stage 1**
(obedience/punishment). This is the framework's origin tier — the original system was preschool-only
(001 §Context), and everything else scaled outward from it. At this stage a child cannot yet reliably
separate a character's inner motivation from its outward effect, so the adaptation leans on the strongest
transformation and the tightest safety envelope.

## Agency Externalization is MANDATORY here — the load-bearing T1 rule

Per 003, Agency Externalization is the **most important rule** for Tiers 1-2. Children 3-5 are egocentric
(Piaget): faced with a "bad" character they may fail to understand motivation, feel the raw emotional
impact, and **internalize "badness" as applying to themselves**. The mitigation is to attribute negative
outcomes never to internal malice but to a temporary **state** (grumpy, tired) or an **accident** — never
an innate quality. That gives the child a simple cause ("grumpy because dark"), a concrete solution ("let
the sunshine in"), and no character who is inherently bad to internalize. Worked example (003): *"Sauron
was evil"* → *"Grumpy King, no sunshine."*

## Consequence for the thresholds

Because complexity and internal-motivation framing are withheld, T1 carries the lowest vocabulary and
sentence ceilings and the strictest emotional-safety/nightmare-prevention constraints of any tier (the
concrete numbers are in `kb/tiers/tier_1.yaml`; the safety rubric reads them at runtime). This is a
deliberate trade — 003 notes it removes moral complexity, which is acceptable and appropriate at this age.
