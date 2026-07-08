# Rewriting *The Lion, the Witch and the Wardrobe*

A complete worked example of the Literary Adaptation Framework applied to C.S. Lewis's *The Lion, the
Witch and the Wardrobe* (1950). Where the [Tolkien mapping](../../../config/concept_mapping/templates/tolkien_mapping.yaml)
demonstrates LAF on epic warfare, LWW exercises a different and in some ways harder set of
challenges: a **sacrificial death followed by resurrection**, **petrification**, and an intimate
**betrayal within a family**.

> **New to LAF?** Read the [USER_GUIDE](../USER_GUIDE.md) and
> [UNDERSTANDING_TRANSFORMATIONS](../UNDERSTANDING_TRANSFORMATIONS.md) first — this set assumes you
> know the analyze → transform → verify workflow and the core rules.

## This document set

| Document | What it covers |
|----------|----------------|
| **README.md** (this file) | The challenges, and the mapping that drives everything |
| **[ADAPTATION_GUIDE.md](ADAPTATION_GUIDE.md)** | Every key challenge walked through Tier 1 / Tier 3 / Tier 5, with before → after |
| **[STONE_TABLE.md](STONE_TABLE.md)** | Deep-dive on the single hardest scene: Aslan's death and resurrection |

The loadable configuration behind all three:
**[`config/concept_mapping/templates/narnia_mapping.yaml`](../../../config/concept_mapping/templates/narnia_mapping.yaml)**.

## The book's adaptation challenges

Each challenge maps to a framework rule. This is the `key_challenges` list from `narnia_mapping.yaml`,
annotated with the rule that governs it:

| Challenge | Why it's hard | Governing rule |
|-----------|---------------|----------------|
| **Aslan's death & resurrection** (Stone Table) | Sacrifice, killing, *and* return — all at once | Death handling + hard-case handling → [STONE_TABLE.md](STONE_TABLE.md) |
| **Petrification** (the Witch's wand turns creatures to stone) | Body-horror image; a real nightmare risk | Nightmare prevention ([safety_check §5](../../../prompts/verification/safety_check.md)) |
| **Edmund's betrayal** for Turkish Delight | Betrayal of siblings — intimate, not abstract | Agency externalization + Betrayal → Accident |
| **The Battle of Beruna** | Pitched, named battle with deaths | Violence → cooperation |
| **The wartime frame** (children evacuated from the Blitz) | Real-world war in the opening pages | Conflict transformation / omission at low tiers |
| **The Christian-allegory layer** | Aslan as a Christ figure | *Neither add nor strip* — see below |

## A note on the allegory

LWW is a deliberate Christian allegory. LAF's job is to adapt the **narrative and emotional** surface
to a developmental tier — **not** to preach it and **not** to scrub it. The framework therefore takes
one position: *neither add nor strip the allegory*.

- At **Tier 1–3**, the surface story is adapted (a rest, a sacrifice, a return); the allegorical
  reading remains available to any reader or adult who brings it, exactly as in the original.
- At **Tier 5**, the text is preserved and the allegory stands as Lewis wrote it.

This mirrors the framework's core discipline: transform *how the story lands*, never *what the author
meant it to mean*.

## How the tiers reshape this book

| Element | Tier 1 (3–5) | Tier 3 (9–11) | Tier 5 (15–17) |
|---------|--------------|---------------|----------------|
| The White Witch | The grumpy Snow Queen | The White Witch (Jadis), truly menacing | Jadis, preserved |
| Turning to stone | Playing statues (warm breath un-freezes) | Real petrification, frightening | Preserved |
| Edmund | Made a silly mistake, said sorry | Betrayed his family, then redeemed | Preserved |
| Aslan at the Stone Table | Has a big rest, then wakes up | Gives his life, dies, returns | Preserved |
| The Battle of Beruna | The Big Tidy-Up | Battle summarized (stakes, not gore) | Preserved |

Full before → after text for each row is in [ADAPTATION_GUIDE.md](ADAPTATION_GUIDE.md).

## Fidelity note

The adaptations in this set are **illustrative of the method**, not a canonical edition. They show
*how* the rules resolve each challenge. Any real adaptation must run the
[anti-hallucination protocol](../UNDERSTANDING_TRANSFORMATIONS.md#confidence-tags) against the actual
book: quote the source, tag every claim `CERTAIN / PROBABLE / UNCERTAIN`, and verify before delivery.
