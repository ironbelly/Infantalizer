# Tier 5 — design commentary (ages 15-17, formal operational)

*Rationale only — the authoritative T5 constraint data lives in `kb/tiers/tier_5.yaml`. Carried from
`docs/design_decisions/001-five-tier-system.md` and `003-agency-externalization.md`.*

## Why Tier 5 is "minimal transformation — preserve author intent"

Piaget places ages 15-17 in full **formal operational** reasoning; Kohlberg reaches **stage 5**
(social contract / principled reasoning). At this stage the reader can handle abstraction, irony,
unreliable narration, and genuine moral ambiguity, so the adaptation does the least: it preserves the
author's intent and intervenes only for genuine access barriers (archaic language, missing historical
context), never to sanitize difficult themes, moral complexity, or character deaths. Adaptation here means
**accessibility, not sanitization** — the full philosophy lives in `kb/tiers/tier_5.yaml`'s
`adaptation_philosophy` block.

## Agency Externalization is FORBIDDEN here

T5 is the far end of the ladder (MANDATORY T1-2 → OPTIONAL T3 → **FORBIDDEN T4-5**). Per 003,
externalizing agency for a formal-operational reader would be actively **patronizing and undermine
character complexity**: a 15-17-year-old is expected to understand good people doing bad things and
internal, morally-mixed motivation. Relabeling malice as a temporary "state" would strip exactly the
complexity this tier exists to preserve. So negative agency is left as the source presents it.

## Why T5 anchors the top of the interpolation range

Because T5 is the near-source ceiling, it serves as the upper bound for the Tier-4 interpolation (see
`tier_4.md`): T4 constraints are computed between the T3 floor and the T5 ceiling. 001's rationale for
distinct, defensible tier boundaries applies here too — T5's near-source posture is what makes the whole
axis meaningful rather than a single flattening transform.
