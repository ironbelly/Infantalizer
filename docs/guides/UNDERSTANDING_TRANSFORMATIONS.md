# Understanding Transformations

The *why* behind LAF's rules. The [USER_GUIDE](USER_GUIDE.md) tells you which files to load; this
guide explains what those files are doing to the story and why it is safe and faithful rather than
merely censored. Every rule here lives in
[`config/transformation_rules/`](../../config/transformation_rules/) and
[`config/concept_mapping/universal_mappings.yaml`](../../config/concept_mapping/universal_mappings.yaml).

## The one principle underneath everything

> **A transformation preserves the *emotional journey* while changing what a young reader cannot yet
> safely hold.**

LAF never asks "what can we cut?" It asks "what is this scene *doing* to the reader, and how do we do
the same thing within this tier's limits?" Sam carrying Frodo must survive every tier because the
*meaning* — love that keeps going when strength runs out — is tier-independent. Only its surface
(exhaustion, a wound, a mountain of ash) gets re-rendered.

## Agency externalization

**The framework's signature rule.** Defined in
[`thematic.yaml`](../../config/transformation_rules/thematic.yaml): *"Badness is always a STATE or
ACCIDENT, never innate."*

| Tier | Mode | Meaning |
|------|------|---------|
| 1–2 | **Mandatory** | No character is *bad*; they are grumpy, sad, confused, or mistaken — for an external, fixable reason |
| 3 | Optional | You may show real internal motive, or keep externalizing — your call |
| 4–5 | **Forbidden** | Externalizing a real villain's malice is patronizing; preserve the original |

```
❌ "The Witch was cruel and evil."
✅ "The Snow Queen was grumpy because it was always cold and never Christmas."   (Tier 1)
```

Why it matters: a 4-year-old cannot yet model *stable inner malice* in another mind (pre-theory-of-
mind, in Piaget's terms). Telling them a character is "evil" doesn't teach caution — it teaches that
some beings are simply, permanently frightening. Externalizing to a *state* keeps the antagonist
legible and, crucially, **redeemable**. Above Tier 3 the same move becomes a lie the reader can see
through. See [ADR-003](../design_decisions/003-agency-externalization.md).

## Violence → cooperation

From [`thematic.yaml`](../../config/transformation_rules/thematic.yaml) `violence_transformation` and
`conflict_transformation`:

| Source | Tier 1 | Tier 2 | Tier 3 | Tier 4–5 |
|--------|--------|--------|--------|----------|
| Battle | The Big Tidy-Up | A contest / race | Battle, *summarized* (stakes, not gore) | Preserve |
| Enemy army | Noisy, messy helpers | The opposing team | — | Preserve |
| War | A helping project | A contest | — | Preserve |
| Weapons | Removed entirely | — | — | Preserve |

The battle doesn't vanish — its *function* (a hard shared effort with something at stake) is re-cast
as a tidy-up or a contest. At Tier 3 the battle returns by name but the camera pulls back: **stakes,
not gore**.

## Death → journey or rest

From [`thematic.yaml`](../../config/transformation_rules/thematic.yaml) `death_handling` and
[`universal_mappings.yaml`](../../config/concept_mapping/universal_mappings.yaml):

| Tier | Strategy | Language |
|------|----------|----------|
| 1 | Journey or sleep | "went on a new adventure", "a very long rest" — **never** die/dead/killed |
| 2 | Gentle acknowledgment | "passed away", "was lost", "gone" |
| 3 | Direct but gentle | "died", "death" — focus on **emotional impact** |
| 4–5 | Preserve original | — |

This is the rule most people expect to feel like a cop-out and it is the most carefully staged. At
Tier 1, death becomes *continuation* (rest, a new adventure) because permanence is exactly the part a
preschooler cannot process without distress. At Tier 3 the euphemism is *removed on purpose*: a
9–11-year-old is served better by "he died, and it hurt" than by a dodge they've outgrown.

## Heroism translation

Heroism is never defined as violence at the young tiers. From `heroism_definition` in
[`thematic.yaml`](../../config/transformation_rules/thematic.yaml) and the `heroism_translation`
subroutine in [`character.yaml`](../../config/transformation_rules/character.yaml):

```
IDENTIFY core positive intent  →  LOOKUP tier expression  →  TRANSLATE, preserving intent
```

| "slays the enemy" | → Tier 1 | → Tier 2 | → Tier 3 |
|-------------------|----------|----------|----------|
| | "helps the grumpy character feel better" | "wins the contest" | "defeats the villain" |

The *intent* — protect the people you love — is constant. Only its expression moves from prosocial
(helping, comforting, persevering) up to defense and sacrifice at Tier 3, and the full spectrum at
4–5.

## Archetypes: simplify the cast, keep the roles

[`character.yaml`](../../config/transformation_rules/character.yaml) maps complex characters onto a
small set of Tier 1 archetypes — *Brave Friend on a Special Job*, *The Great Helper*, *The Wise
Teacher*, *The Grumpy/Messy Character* — each with permitted and **forbidden** traits (the
protagonist may not be "vengeful" or "traumatized"; the antagonist may not be "cruel"). A hero-leader
draws authority from *helping ability, not lineage*. As the tier rises, `tier_3_unlocks` restores
flawed heroes, complex villains, and moral ambiguity.

### Hard cases

Some characters resist simple archetypes — Tolkien's Gollum (playful vs. murderous) and Denethor
(despair, suicide). `character.yaml` gives each a `special_handling` block: at Tier 1 Gollum is "a
Silly Creature" and the Ring's destruction is "an accident during a game"; Denethor is "a Sad Leader"
whose cause is "closed windows," with suicide and the pyre omitted. LWW's **Stone Table** is the same
kind of hard case — sacrifice, death, and resurrection at once — and gets its own deep-dive:
[STONE_TABLE.md](lion-witch-wardrobe/STONE_TABLE.md).

## Confidence tags

Adaptation is worthless if it quietly invents source material. LAF's **v2.0 anti-hallucination
protocol** ([`chapter_analysis.md`](../../prompts/analysis/chapter_analysis.md)) tags every claimed
fact:

| Tag | Meaning | So you should… |
|-----|---------|----------------|
| **CERTAIN** | Directly quoted from the text | Trust it |
| **PROBABLE** | Supported by multiple observations | Sanity-check |
| **UNCERTAIN** | Inferred or reconstructed (e.g., working from memory) | Verify against the real book |

> **Transparent uncertainty > false certainty.**

If Phase 0 declares `MEMORY`-based access, *everything* is tagged `UNCERTAIN` by rule. If access is
`NONE`, the analysis **aborts** — LAF will not adapt a chapter it cannot actually read.

## Putting it together

These rules compose in a cascade (most-specific wins):

```
universal_mappings.yaml  →  <work>_mapping.yaml  →  age_profiles/tier_N  →  transformation_rules
```

To watch all of them act on real scenes across all five tiers, read the
[LWW adaptation guide](lion-witch-wardrobe/ADAPTATION_GUIDE.md).
