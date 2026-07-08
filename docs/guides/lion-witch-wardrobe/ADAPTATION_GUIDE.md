# LWW Adaptation Guide

Every key challenge in *The Lion, the Witch and the Wardrobe*, walked through **Tier 1 (3–5)**,
**Tier 3 (9–11)**, and **Tier 5 (15–17)**, with before → after examples and the rule that drives each
choice. The translations come from
[`narnia_mapping.yaml`](../../../config/concept_mapping/templates/narnia_mapping.yaml); the rules come
from [`config/transformation_rules/`](../../../config/transformation_rules/).

> All example text is **illustrative of the method**, not a canonical rewrite. See the
> [fidelity note](README.md#fidelity-note).

Legend: **T1** = ages 3–5 · **T3** = ages 9–11 (transition tier) · **T5** = ages 15–17 (preserve).

---

## 1. The wartime frame

The book opens with the Pevensie children sent away from London because of wartime air raids.

> **Source (illustrative):** "The four children were sent away from London because of the air-raids."

- **T1** — *Omit the war; keep the journey.* Conflict transformation removes the threat; the "safe
  home" schema stays intact.
  > "The four children went to stay at a big, friendly house in the countryside."
- **T3** — *Name it, gently.* A 9–11-year-old can hold real-world stakes.
  > "The four children were sent from London to the country to keep them safe during the war."
- **T5** — *Preserve.* Lewis's frame stands as written.

**Rule:** `conflict_transformation` (T1 omission) → direct naming at T3 →
[preserve](../UNDERSTANDING_TRANSFORMATIONS.md#violence--cooperation) at T5.

---

## 2. The White Witch

Jadis rules Narnia in an endless winter and turns those who defy her to stone.

> **Source (illustrative):** "The White Witch was cruel. It was always winter, and never Christmas."

- **T1** — *Externalize the badness to a fixable state.* She is not cruel; she is **grumpy for a
  reason**, and the reason can be mended.
  > "The Snow Queen was grumpy because it was always cold and never Christmas."
- **T3** — *Restore the menace.* The transition tier allows a genuine antagonist with an
  understandable motive (she wants to rule; the thaw would end her power).
  > "The White Witch had frozen all of Narnia. She meant to keep it 'always winter and never
  > Christmas' — because the thaw would end her reign."
- **T5** — *Preserve* Jadis in full.

**Rule:** [agency externalization](../UNDERSTANDING_TRANSFORMATIONS.md#agency-externalization) —
**mandatory** at T1, **optional** at T3, **forbidden** at T5.

---

## 3. Turning to stone (petrification)

The Witch's wand petrifies creatures — Mr. Tumnus among them. A vivid image, and a real nightmare
risk for the youngest readers.

> **Source (illustrative):** "She touched them with her wand and they were turned to stone."

- **T1** — *Convert the nightmare to a game with a warm, reversible ending.*
  > "The Snow Queen waved her silly wand, and the creatures had to hold very still, like statues.
  > Later, warm friends breathed on them and they could move and laugh again."
- **T3** — *Keep it frightening, keep the rescue.* Petrification is named and real; Aslan's breath
  reverses it.
  > "The Witch turned them to stone where they stood. Only Aslan's warm breath could bring them
  > back."
- **T5** — *Preserve.*

**Rule:** [safety_check §5, Nightmare Prevention](../../../prompts/verification/safety_check.md) —
"monsters are grumpy/silly, not terrifying; darkness is temporary and fixable."

---

## 4. Edmund's betrayal

Enchanted Turkish Delight leads Edmund to side with the Witch against his own brother and sisters —
the book's most intimate wound.

> **Source (illustrative):** "Edmund betrayed his brother and sisters to the Witch for more Turkish
> Delight."

- **T1** — *Betrayal → accident.* He is not disloyal; he is **carried away** by the treat, and the
  arc ends in repair. (The `narnia_mapping.yaml` archetype: "Friend Who Makes a Mistake.")
  > "Edmund wanted the yummiest treat so much that he wandered off and forgot to tell his family.
  > Soon he felt sorry, and everyone forgave him."
- **T3** — *Show the betrayal, its cost, and the earned reconciliation.* The transition tier can hold
  a hero who genuinely fails and genuinely mends.
  > "Edmund betrayed his brother and sisters for the enchanted sweets, and it put them all in
  > danger. Later he understood what he had done, and worked to make it right."
- **T5** — *Preserve.*

**Rule:** `betrayal` mapping (T1: "Accident / Silly mistake") in
[`universal_mappings.yaml`](../../../config/concept_mapping/universal_mappings.yaml); `tier_3_unlocks`
`hero_with_flaws` in [`character.yaml`](../../../config/transformation_rules/character.yaml).

---

## 5. Aslan at the Stone Table

The heart of the book — and the framework's hardest single case. Aslan gives his life in Edmund's
place, is bound and slain on the Stone Table by the Witch, and returns by a deeper magic. Because it
combines **sacrifice + a killing + death + resurrection**, it gets its own document.

**Summary of the tier treatment:**

- **T1** — *A big rest, then waking up.* Omit the binding, the shaving, and the knife. Aslan trades a
  long rest to fix Edmund's mistake, then wakes warm and strong.
- **T3** — *Aslan gives his life for Edmund; he dies and returns.* Named, with the emotional weight
  intact.
- **T5** — *Preserve.*

➡ **Full treatment: [STONE_TABLE.md](STONE_TABLE.md).**

---

## 6. The Battle of Beruna

Peter leads Aslan's army against the Witch's forces in a pitched, named battle with casualties.

> **Source (illustrative):** "The two armies met in battle, and many fell before Aslan arrived."

- **T1** — *Battle → cooperative tidy-up; heroism → helping.* No weapons, no casualties; the
  statue-friends are woken and the mess is cleared together.
  > "Everyone worked together in one big tidy-up. Aslan came and helped, and the woken statue-friends
  > cheered."
- **T3** — *Summarize: stakes, not gore.* The battle is real and named, but the camera pulls back and
  Aslan's arrival turns the tide.
  > "The two armies clashed, and it went badly until Aslan arrived with those he had freed. Together
  > they turned the battle."
- **T5** — *Preserve.*

**Rule:** `violence_transformation` (T1 battle → "cooperative_activity"; T3 → "battle_summarized,
stakes not gore") and `heroism_definition` (T1 "prosocial_only") in
[`thematic.yaml`](../../../config/transformation_rules/thematic.yaml).

---

## 7. The thaw

Aslan's return breaks the Witch's winter; Father Christmas appears; spring comes to Narnia.

- **T1** — *A warm, happy ending.* The cold melts, Father Christmas visits, everyone is warm — a
  clean positive resolution (required at T1).
  > "The cold melted away at last. Father Christmas came, and all of Narnia grew warm and green."
- **T3** — *The thaw as the Witch's power breaking.* The same event, carrying its meaning.
  > "As Aslan grew stronger, the endless winter broke. The thaw itself was the Witch's power melting
  > away."
- **T5** — *Preserve.*

**Rule:** T1 requires a positive emotional resolution by chapter end
([safety_check §3](../../../prompts/verification/safety_check.md)).

---

## Verify before you ship

Any Tier 1 or Tier 2 rendering above must pass
[`safety_check.md`](../../../prompts/verification/safety_check.md): no forbidden words
(`kill/die/dead/evil/wound/blood/weapon`), all agency externalized, a positive ending, and sentences
within the tier's length limit. Run it — don't assume it.

For the mechanics of the workflow that produced these, return to the [USER_GUIDE](../USER_GUIDE.md).
