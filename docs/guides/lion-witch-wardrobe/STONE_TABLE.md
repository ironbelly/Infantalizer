# Deep Dive: The Stone Table

Aslan's sacrifice, death, and resurrection is the defining scene of *The Lion, the Witch and the
Wardrobe* — and the single hardest case in the whole framework. It stacks four things a young tier
handles separately, all into one sequence:

1. **Sacrifice** — Aslan offers his life *in Edmund's place*.
2. **A killing** — the Witch binds, shears, and slays him on the Stone Table.
3. **Death** — he is really, unmistakably dead.
4. **Resurrection** — the Table cracks and he returns by a "deeper magic."

This is the LWW analogue of the framework's other hard cases — Tolkien's Gollum and Denethor, which
get their own `special_handling` blocks in
[`character.yaml`](../../../config/transformation_rules/character.yaml). Handle this scene well and the
rest of the book is easy.

> The renderings below are **illustrative of the method**. A real adaptation must run the
> [anti-hallucination protocol](../UNDERSTANDING_TRANSFORMATIONS.md#confidence-tags) against Lewis's
> text.

## Why it resists a single rule

Most scenes trigger *one* transformation. The Stone Table trips **four rules at once**, and they
interact:

| Component | Rule engaged | The tension |
|-----------|--------------|-------------|
| Sacrifice | `heroism_definition` | At T1, heroism is prosocial *helping* — but this is giving up one's life |
| The killing | `violence_transformation` | T1 removes weapons and violence entirely |
| Death | `death_handling` | T1 forbids `die/dead/killed`; death becomes rest or a journey |
| Resurrection | (emotional resolution) | The *return* is a gift to every tier — it's the death that's the problem |

The key insight: **the resurrection is not the hard part — the killing and the death are.** The
return maps cleanly onto "waking from rest." So the adaptation problem is really *"how do we get Aslan
onto and off the Table without a killing?"*

---

## Tier 1 (ages 3–5): "Aslan's Big Rest"

**Strategy:** `journey_or_sleep` (`death_handling` T1). **Omit** the binding, the shearing, the
knife, and the killing entirely (`stone_table.tier_1.omit` in
[`narnia_mapping.yaml`](../../../config/concept_mapping/templates/narnia_mapping.yaml)). Keep the
sacrifice as a **generous trade**, and the resurrection as **waking up**.

> **Source (illustrative):** "The Witch bound Aslan and slew him upon the Stone Table with her knife.
> But at dawn the Table cracked, and Aslan was alive again."

> **Tier 1:** "Aslan had a kind idea to fix Edmund's mistake. He went to the big stone table for a
> very long, deep rest. The Snow Queen thought her cold would last forever. But when the morning sun
> came up, the table went *crack!* — and Aslan woke up, bigger and warmer and stronger than before.
> He gave a great, happy roar."

Notice what's preserved and what's converted:

- **Preserved:** the *sacrifice* (a kind idea to fix Edmund's mistake), the sunrise turn, the crack
  of the Table, the joy of the return.
- **Converted:** the killing → *a long, deep rest*; the Witch's cruelty → *grumpiness that thinks the
  cold will last*; death → *sleep that ends in waking*.
- **Omitted:** binding, shearing, the knife.

**Safety check (T1):** no forbidden words (`slew`, `knife`, `bound`, `die/dead` all gone); agency
externalized (the Snow Queen is grumpy, not cruel); ends warm and resolved →
[**APPROVED**](../../../prompts/verification/safety_check.md).

---

## Tier 3 (ages 9–11): a named sacrifice

**Strategy:** `direct_but_gentle` (`death_handling` T3, `can_use: died`). The transition tier is
built for exactly this — a hero who *gives his life*, dies, and returns, with the emotional weight
left intact but the gore pulled back. Agency externalization is now **optional**, so the Witch can be
a real antagonist.

> **Tier 3:** "Aslan offered his own life in Edmund's place. That night the White Witch bound him and
> killed him on the Stone Table, sure she had won. But she did not know the deeper magic: at sunrise
> the Table split in two, and Aslan was alive again — for a willing sacrifice made in another's place
> turns death itself backward."

- **Named:** the sacrifice, the death (`killed`), the Witch's agency, the deeper magic.
- **Restrained:** the method is stated, not dwelt on — "stakes, not gore"
  (`violence_transformation` T3).
- **Kept whole:** the theological logic (a *willing* substitution) is preserved, not explained away —
  this is the "neither add nor strip the allegory" discipline from the
  [set README](README.md#a-note-on-the-allegory).

**Note:** Tier 3 outputs do **not** require `safety_check.md` (it is mandatory only for Tiers 1–2),
but the analysis still carries confidence tags.

---

## Tier 5 (ages 15–17): preserve

**Strategy:** `preserve_original`. No transformation. Lewis's language, pacing, and the full force of
the sacrifice stand as written. The framework's job at Tier 5 is **accessibility, not sanitization**
— at most a footnote for archaic phrasing (per the Tier 5 age profile). Trust the reader.

---

## The pattern to reuse

The Stone Table teaches the general move for any *sacrifice-and-return* scene:

1. **Find the emotional core** — here, love that gives itself away, and the joy of its return. That
   core is tier-independent and must survive every tier.
2. **Locate which rules the surface trips** — often several at once (violence + death + more).
3. **Convert the surface at low tiers, name it at the transition tier, preserve it at the top** —
   killing → rest → death; cruelty → grumpiness → real menace.
4. **Never let the transformation delete the meaning.** A rest that ends in a bigger, warmer waking
   still *means* "love that outlasts the worst thing" — which is the point.

For the other challenges in this book, see [ADAPTATION_GUIDE.md](ADAPTATION_GUIDE.md). For the rules
themselves, see [UNDERSTANDING_TRANSFORMATIONS.md](../UNDERSTANDING_TRANSFORMATIONS.md).
