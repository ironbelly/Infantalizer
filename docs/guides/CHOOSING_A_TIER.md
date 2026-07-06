# Choosing a Tier

The single most important decision you make before adapting anything. The tier sets every downstream
limit — what vocabulary is allowed, whether anyone can die on the page, how long a sentence may be,
and whether a villain can be genuinely villainous. Pick it first.

## The five tiers

| Tier | Ages | Piaget stage | Use case | Feel |
|------|------|--------------|----------|------|
| 1 | 3–5 | Preoperational | Bedtime stories | Everything is safe, warm, and fixable |
| 2 | 6–8 | Early Concrete | Early readers | Mild tension; contests, not battles |
| **3** | **9–11** | **Concrete** | **Chapter books** | **Complexity unlocked — the turning point** |
| 4 | 12–14 | Early Formal | Middle grade | Near-adult; tragedy permitted |
| 5 | 15–17 | Formal | Young adult | Preserve the original; don't sanitize |

Grounded in Piaget's cognitive stages and Kohlberg's moral reasoning. See
[ADR-001](../design_decisions/001-five-tier-system.md) for why there are five.

## Decide by what the child can hold

Match the tier to the reader's developmental reality, not just their birthday. Ask:

| Question | T1 | T2 | T3 | T4 | T5 |
|----------|----|----|----|----|----|
| Can a character die on the page? | No | No | Implied | Yes | Yes |
| Can a villain be genuinely bad? | No | No | Partly | Yes | Yes |
| Can a hero fail — morally or otherwise? | No | No | Yes | Yes | Yes |
| Must blame be externalized (states/accidents, never malice)? | **Yes** | **Yes** | Optional | No | No |
| Are parallel plotlines / flashbacks OK? | No | No | Yes | Yes | Yes |

(Condensed from the Tier Decision Matrix in [SPEC.md](../SPEC.md).) If your honest answers straddle
two tiers, **go lower** — it is easier to add complexity next year than to un-frighten a child.

## Tier 3 is the load-bearing decision

Tier 3 (ages 9–11) is the **transition tier**, and choosing it is a real commitment, not a midpoint.

- **Tiers 1–2 protect the reader from complexity.** Blame is externalized (the villain is *grumpy
  because…*), death becomes rest or a new adventure, battles become tidy-ups and contests.
- **Tier 3 and up scaffold complexity instead of hiding it.** "Died" may be named. Moral ambiguity
  is allowed. A hero may fail. Agency externalization becomes *optional* — and above Tier 3 it is
  **forbidden**, because pretending a 13-year-old's villain is "just grumpy" is patronizing.

If you are unsure whether a reader is ready for a named death or a villain with real motives, that
uncertainty itself points at the T2/T3 boundary. See
[ADR-003](../design_decisions/003-agency-externalization.md) and
[UNDERSTANDING_TRANSFORMATIONS.md](UNDERSTANDING_TRANSFORMATIONS.md#agency-externalization).

## Purpose, not just age

The same reader may want different tiers for different purposes:

- **Read-aloud at bedtime** → lean lower (calm, resolved, safe-home preserved).
- **Independent reading for confidence** → match the tier to reading level, not content tolerance.
- **A shared family read of a hard book** (e.g., a war story) → a lower tier lets you introduce it
  years early, then re-read at a higher tier later.

## Tier 4: interpolate, don't look for a file

There is deliberately **no Tier 4 profile** in the repo. Tier 4 is *interpolated*: take Tier 3 as the
floor and Tier 5 as the ceiling and pick the conservative midpoint. If you need a Tier 4 adaptation,
load both `tier_3` and `tier_5` configs and aim between them. (Rationale:
[ADR-001](../design_decisions/001-five-tier-system.md).)

## Once you've chosen

Head to the [USER_GUIDE](USER_GUIDE.md#step-2-load-the-configuration) and load
`config/age_profiles/tier_N_*.yaml` for your tier. To see all five tiers applied to the *same*
scenes, read the [LWW adaptation guide](lion-witch-wardrobe/ADAPTATION_GUIDE.md).
