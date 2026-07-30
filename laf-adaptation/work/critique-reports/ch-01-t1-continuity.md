# Continuity Check — ch-01-t1-v2.md ("Lucy Finds the Snowy Land")

**Reviewer:** continuity-checker
**Draft:** `laf-adaptation/work/drafts/ch-01-t1-v2.md`
**Date:** 2026-07-08

## Canon files consulted

| Source | Path | Role |
|---|---|---|
| Source truth (tier-invariant) | `laf-adaptation/work/analysis/ch-01.yaml` | Authority for facts, 10-event order, characters/roles, opening/closing sentences |
| Work mapping | `work/prep/narnia/30-mapping.yaml` | T1 concept glosses; character T1 names; key-scene T1 framing |
| Tier profile | `laf-adaptation/kb/tiers/tier_1.yaml` | Preschool age band, linguistic + narrative constraints |
| Source text (spot-check) | `Books/LWW/The Lion, the Witch and the Wardrobe, by C. S. Lewis.html` | Used to verify Faun name-reveal timing (lines 471-532) |
| Prior tier-1 continuity | `kb/adaptations/narnia/tier-1/continuity.md` | **NOT PRESENT** (see note below) |

## Prior-chapter continuity note (PASS-by-construction)

This is **Chapter 1** of the work. The prior-tier-1 continuity file
`kb/adaptations/narnia/tier-1/continuity.md` does not exist, which is **correct and expected**:
there is no preceding chapter to carry running canon forward from. Cross-chapter continuity
checks are therefore **PASS-by-construction** for ch-01. The substantive checks below cover
(a) internal consistency of the draft, (b) agreement with the source analysis (facts, event
order, characters, opening/closing sentences), and (c) term/vocabulary consistency against the
T1 mapping.

## Authorized T1 transforms (NOT flagged as errors)

Per the task brief and the mapping, the following deviations from the source text are
**intentional, greenlit adaptation decisions** and were excluded from the findings below:

- "wardrobe" → "cupboard" (T1 gloss of `the_wardrobe_threshold` = "a magic cupboard that goes to a snowy land").
- Source cliffhanger (`"Goodness gracious me!" exclaimed the Faun`) reframed into a friendly comic beat — greenlit by `key_scenes.lucy_enters_narnia.tier_1.framing` ("wonder and friendship only").
- "armour" retained (British source-fidelity, not a T1 vocab violation — `tier_1.yaml` bans specific words like "kill/die/evil", not British spellings).
- Wartime evacuation simplified to "went to live far away" (T1 `conflict_to_cooperation` rule: war → big tidy-up / removal).
- Mothballs source detail ("dropping two moth-balls") rendered as "they smelled of fur and mothballs" (sensory integration, faithful).
- Edmund's sarcasm softened to "grumpy and tired" then "bright again" (T1 `agency_externalization`: badness as state, not trait).
- Lucy's "small fear" of the Professor replaced with "Lucy felt safe right away" (T1 `safe_home_schema: mandatory`).

---

## Findings

**Breaks canon: 0**
**Term drift: 0**
**Suspicious: 0**

No findings. The draft is clean.

---

## What was checked (substance, not boilerplate)

### 1. Opening sentence — PASS
- **Required (essentials.opening_sentence):** "Once there were four children whose names were Peter, Susan, Edmund and Lucy."
- **Draft:** "Once there were four children. Their names were Peter, Susan, Edmund, and Lucy." — split across two short sentences.
- T1 `max_words_per_sentence: 12` and `max_clauses: 1` require this split; the wording and name order are faithful. Source-fidelity skill accepts clause-count splits at T1. Not a contradiction.

### 2. Closing sentence — PASS (authorized transform)
- **Required (essentials.closing_sentence):** `"Goodness gracious me!" exclaimed the Faun.`
- **Draft:** The exclamation `"Oh!" said the Faun. "Goodness gracious me!"` is preserved verbatim, then followed by a friendly resolution beat (Lucy laughs, the Faun laughs, mutual "Hello"). The cliffhanger-to-comic reframe is the greenlit T1 `lucy_enters_narnia` framing.

### 3. Event sequence (all 10 events in order) — PASS

| Seq | Source event (ch-01.yaml) | Draft realization | Verdict |
|---|---|---|---|
| 1 | Four children sent from London to Professor's country house during the war | "Once there were four children… They went to live far away in a big old house" | PASS (T1 war simplification) |
| 2 | First evening: meet the Professor; Lucy a little afraid; Edmund tries not to laugh | "A kind old man lived there. He was the Professor… Mrs. Macready… gave Lucy a biscuit and a smile. Lucy felt safe right away" | PASS (T1 `safe_home_schema`) |
| 3 | That night children gather, agree to explore; Edmund prickly; owl calls | "Edmund was grumpy and tired that first night… next day he felt bright again" | PASS (T1 state-not-trait) |
| 4 | Next morning rain; explore indoors | "Next day it rained and rained. So the children explored inside" | PASS |
| 5 | Series of rooms (pictures, suit of armour, green room with harp, balcony), then empty room with one big wardrobe | "They found a room full of pictures. They found a shiny suit of armour. Then they found a small, empty room. In it stood one big cupboard" | PASS (T1 condensation; greenlit cupboard gloss) |
| 6 | Peter says "Nothing there!", others leave, Lucy stays, opens door, moth-balls drop | `"Nothing here!" said Peter. The others all ran out. But Lucy stayed behind… She pulled the cupboard door. It creaked open` | PASS |
| 7 | Lucy steps in among fur coats, feel and smell, walks deeper expecting wooden back, feels snow and branches | "The coats were soft and furry… smelled of fur and mothballs… She walked deeper in… Crunch, crunch… It was cold and white. Snow! Something rough brushed her face. It felt like branches" | PASS |
| 8 | Snowy wood at night, snowflakes falling, keeps wardrobe door in sight, walks toward distant light | "Lucy stepped out of the cupboard. She stood in a wood at night. Snow fell on her nose… She could still see the cupboard door. She could go home… She walked toward the light" | PASS |
| 9 | Reaches lamp-post; hears footsteps; strange figure steps out | "The light was a lamp-post… Then she heard a sound. Pit-pat, pit-pat… Out of the trees stepped a little person" | PASS |
| 10 | Faun: goat-legged, horned, parcels, umbrella; drops parcels, exclaims | "Little hoofs, just like a goat! Up went his big umbrella. Brown paper parcels… He dropped all his parcels… `Goodness gracious me!`" | PASS |

No event is omitted, reordered, or contradicted.

### 4. Characters and roles — PASS

All seven named characters appear with correct roles per `ch-01.yaml` and `30-mapping.yaml`:
- **Peter** — leads exploration ("Let us explore!", "Nothing here!"). PASS.
- **Susan** — named in the roll-call; no speaking part, consistent with source (Susan does not act in ch-01). PASS.
- **Edmund** — "grumpy and tired that first night… bright again". Consistent with T1 archetype "The Mixed-Up Friend" and `agency_externalization` rule. PASS.
- **Lucy** — curious and brave; the one who enters the cupboard. PASS.
- **the Professor** — "kind old man… wild white hair". Source says "shaggy white hair" and "very old"; T1 softens "shaggy"→"wild" and adds "kind" (T1 `villain_treatment`/safe schema). PASS.
- **Mrs. Macready** — housekeeper ("kept the house tidy"). PASS.
- **the Faun** — correctly unnamed (see §5 below); described with goat hoofs, red scarf, umbrella, parcels. PASS.

No character knows anything they shouldn't. Lucy is the only child who enters the wood; the others never see Narnia in this chapter, matching source.

### 5. Faun name-reveal timing — PASS (subtle, worth recording)

The draft never calls the Faun "Mr. Tumnus" — only "the Faun" and "the kind Faun". Source text confirms the name-reveal happens in ch-02 (line 532 of source HTML: "My name is Tumnus"), well after the ch-01 closing line (line 477). The T1 mapping entry `mr_tumnus.tier_1.name = "Mr. Tumnus"` applies once the character is *introduced by name* in-chapter, which ch-01 does not do. The draft's restraint is **correct** — naming him here would be a forward-reference contradiction.

### 6. Internal consistency — PASS

- "cupboard" used consistently throughout (intro, "She pulled the cupboard door", "Lucy stepped out of the cupboard", "She could still see the cupboard door"). No wardrobe/cupboard flip-flop.
- Lamp-post established as "the light" then resolved ("The light was a lamp-post") — no contradiction.
- Snow established inside the cupboard ("Crunch, crunch… Snow!") then continues outside ("Snow fell on her nose") — internally continuous.
- Faun's parcels set up ("Brown paper parcels swung from his arms") before being dropped ("He dropped all his parcels") — consistent.
- Timeline: first night → next day (explore) → next day (rain) — strictly linear, matches T1 `timeline: strictly_linear` and source.

### 7. Term / vocabulary consistency — PASS

- `the_wardrobe_threshold` T1 gloss "a magic cupboard that goes to a snowy land" → draft renders "cupboard" + "snowy land" verbatim. No drift.
- `lucy_enters_narnia.tier_1.name` = "Lucy Finds the Snowy Land" → matches draft title exactly. No drift.
- `eternal_winter` T1 gloss ("always snowing") → draft renders falling snow throughout. (Note: the full "always winter, no Christmas" framing is not invoked in ch-01 — appropriate, since ch-01 is the *entry* beat, not the witch-reign exposition.)
- No forbidden T1 vocab (`kill/die/dead/evil/wound/blood/weapon`) appears anywhere in the draft.
- "armour" (British) retained — source-fidelity, not a T1 violation (T1 word-ban list is specific; British spelling is permitted).

### 8. Factual / geographic checks — PASS

- "wood at night" + "lamp-post in the middle of the wood" — matches source (the lamp-post is in the wood, not on a street or village).
- Faun "only as tall as Lucy" — consistent with source faun stature (Lucy-size per ch-01 description: a strange little person).
- Snow falling on nose and hair — physically consistent with standing outside in falling snow.
- "She could still see the cupboard door" — matches source's "she could still see the open doorway" (Lucy keeps the portal in sight). No geographic impossibility introduced.

---

## Missing-context notes

None. The four canon files provided (source analysis, work mapping, tier profile, and the
prior-continuity path — correctly absent for ch-01) were sufficient to verify the draft
end-to-end. The source HTML spot-check on Faun name-reveal timing was confirmatory only;
it did not surface any gap in the provided canon.

## Verdict

**PASS.** The draft is internally consistent and agrees with the source analysis on every
checked axis: opening/closing sentences, all 10 events in order, character names and roles,
Faun name-reveal restraint, term glosses, and T1-authorized transforms. No breaks-canon,
no term drift, no suspicious findings. The draft may proceed to safety-verifier.
