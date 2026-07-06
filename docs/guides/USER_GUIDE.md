# LAF User Guide

The complete walkthrough for adapting a book with the Literary Adaptation Framework. If
[QUICK_START.md](QUICK_START.md) is the map, this is the tour. Read it once end to end; afterward
you can work from QUICK_START alone.

## What LAF actually is

LAF is **not an app**. There is no button to press. It is a set of **prompts** and **YAML
configuration** you load into a capable LLM (e.g., Claude) to run a disciplined, repeatable
adaptation workflow. The core idea — spelled out in [SPEC.md](../SPEC.md) — is that
*age-appropriateness is configuration, not code*: the same three-stage pipeline produces a
preschool version or a young-adult version depending only on which tier config you load.

```
SOURCE CHAPTER
    │
    ▼  ANALYZE      prompts/analysis/chapter_analysis.md
    │               (what happens, what needs transforming, how sure are we)
    ▼  TRANSFORM    prompts/transformation/tier_N_transform.md
    │               + config/age_profiles/tier_N_*.yaml
    │               + config/transformation_rules/{thematic,character}.yaml
    │               + config/concept_mapping/{universal, <work>}_mapping.yaml
    ▼  VERIFY       prompts/verification/safety_check.md   (Tier 1–2, mandatory)
    │
    ▼
ADAPTED CHAPTER  +  transformation log  +  confidence report
```

## Before you start

You need three things:

1. **A source chapter** you can quote from. LAF's anti-hallucination protocol *requires* real access
   to the text — see [Step 1](#step-1-analyze-the-source). Working from memory is allowed but every
   claim gets tagged `UNCERTAIN`.
2. **A target tier.** Decide *before* you adapt — see [CHOOSING_A_TIER.md](CHOOSING_A_TIER.md).
3. **A work mapping (optional but recommended).** A per-book YAML of character/concept translations.
   One ships for *The Lion, the Witch and the Wardrobe*
   ([`narnia_mapping.yaml`](../../config/concept_mapping/templates/narnia_mapping.yaml)) and for
   Tolkien. To make your own, see [ADDING_NEW_WORKS.md](ADDING_NEW_WORKS.md).

## Step 1: Analyze the source

Load **[`prompts/analysis/chapter_analysis.md`](../../prompts/analysis/chapter_analysis.md)** and run
it against your chapter. It walks five phases:

- **Phase 0 — Source declaration.** Declare your access: `FULL` / `PARTIAL` / `MEMORY` / `NONE`.
  `NONE` **aborts** — LAF will not invent a chapter it cannot see.
- **Phase 1 — Essential verification.** Title, chapter, and the exact opening/closing sentences,
  each with a confidence tag.
- **Phase 2 — Dual-pass documentation.** First the characters and 5–10 sequential events, then a
  100–150 word summary.
- **Phase 3 — Transformation flags.** Marks where the chapter carries violence, death, heavy
  emotion, or abstraction that a young tier will need reframed.
- **Phase 4 — Consistency check + confidence tags.** Every element is `CERTAIN`, `PROBABLE`, or
  `UNCERTAIN`. See [UNDERSTANDING_TRANSFORMATIONS.md](UNDERSTANDING_TRANSFORMATIONS.md#confidence-tags).

The output is a small YAML block (metadata + `transformation_flags` + `uncertainties`). Keep it — the
transform step consumes it.

## Step 2: Load the configuration

Load these, in this order (**most-specific wins** where they overlap):

```
config/concept_mapping/universal_mappings.yaml          # generic: death, evil, war, despair…
config/concept_mapping/templates/<work>_mapping.yaml    # this book's names & scenes (if you have one)
config/age_profiles/tier_N_*.yaml                       # the tier's limits & linguistics
config/transformation_rules/thematic.yaml               # violence/death/agency/heroism by tier
config/transformation_rules/character.yaml              # archetypes + heroism translation
```

The **age profile** carries the hard limits (sentence length, forbidden vocabulary, chapter length,
whether death may be named). The **transformation rules** and **concept mappings** carry the
translations. You do not edit these per chapter — you *select* the tier and *load* the mapping.

## Step 3: Transform

Load the tier-appropriate prompt:

- **[`prompts/transformation/tier_1_transform.md`](../../prompts/transformation/tier_1_transform.md)**
  — ages 3–5, maximum transformation.
- **[`prompts/transformation/tier_3_transform.md`](../../prompts/transformation/tier_3_transform.md)**
  — ages 9–11, the transition tier.
- Tiers 2, 4, 5: interpolate from the shipped prompts using the tier's age profile and the rule
  tables. (Only Tier 1 and Tier 3 ship as standalone prompts by design — see
  [ADR-006](../design_decisions/006-adversarial-task-review.md).)

Feed the transform prompt your Step 1 analysis + the Step 2 configs. It produces the adapted chapter
plus a **transformation log** recording which rule drove each change.

## Step 4: Verify (Tier 1–2 — mandatory)

For any Tier 1 or Tier 2 output, run
**[`prompts/verification/safety_check.md`](../../prompts/verification/safety_check.md)**. It scans six
sections:

1. **Forbidden content** — Tier 1 rejects `kill, die, dead, evil, wound, blood, weapon`, etc.
2. **Agency externalization** — no innate malice; every bad outcome is an external state or accident.
3. **Emotional safety** — negative emotions resolve; the chapter ends positively.
4. **Safe-home schema** — home stays (or is restored as) a haven.
5. **Nightmare prevention** — monsters are grumpy/silly, darkness is temporary.
6. **Linguistic compliance** — sentence length and vocabulary within the tier's limits.

The check ends **APPROVED** or **REVISION REQUIRED**. A single automatic-failure item (death
language, real violence, "evil", internal motivation at Tier 1) fails the whole chapter — revise and
re-run.

## Step 5: Read the output

A finished run gives you three things:

| Artifact | What it is | Use it to… |
|----------|------------|------------|
| **Adapted chapter** | The rewritten text at your tier | Read to the child / hand to the reader |
| **Transformation log** | Each change + the rule/principle behind it | Audit fidelity; explain your choices |
| **Confidence report** | The `CERTAIN/PROBABLE/UNCERTAIN` tags | Know which details to double-check against the source |

**Transparent uncertainty beats false certainty.** A `PROBABLE` or `UNCERTAIN` tag is not a
failure — it is the framework telling you where to verify against the real book.

## A short worked example (Tier 1)

> **Source (illustrative):** "The Witch raised her wand and the faun turned to stone. Edmund had
> betrayed them for the enchanted sweets."

- Analysis flags: petrification (nightmare risk), betrayal (forbidden framing at Tier 1).
- `narnia_mapping.yaml` supplies: petrification → *"playing statues"*; Edmund's betrayal →
  *"a silly mistake, then sorry"*; the Witch → *"the grumpy Snow Queen"*.

> **Tier 1:** "The Snow Queen waved her silly wand, and kind Mr. Tumnus had to hold very still, like
> a statue. Edmund had wandered off after the yummiest treat and forgot to tell his family. Soon he
> felt sorry, and warm friends came to help."

Run that through `safety_check.md`: no forbidden words, all agency external, ends on repair and
warmth → **APPROVED**. The same scene at Tier 3 keeps the real menace and names the betrayal — see
[the LWW adaptation guide](lion-witch-wardrobe/ADAPTATION_GUIDE.md).

## Where to go next

- **Pick a tier:** [CHOOSING_A_TIER.md](CHOOSING_A_TIER.md)
- **Understand the rules:** [UNDERSTANDING_TRANSFORMATIONS.md](UNDERSTANDING_TRANSFORMATIONS.md)
- **Map your own book:** [ADDING_NEW_WORKS.md](ADDING_NEW_WORKS.md)
- **See a full example:** [lion-witch-wardrobe/](lion-witch-wardrobe/)
