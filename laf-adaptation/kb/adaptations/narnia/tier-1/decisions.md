# Decisions — narnia / tier-1

> **Key:** `(work=narnia, tier=1)`. Encoded as: directory path `kb/adaptations/narnia/tier-1/`.
> **Adaptation decisions log:** the greenlit decisions applied per chapter. Each entry is **stamped with its chapter** (Inv.1 — chapter on the entry, not the path).
> **Scope:** Tier-1 decisions only. Decisions are keyed `(work=narnia, tier=1, chapter=01)` on this entry.

---

## ch-01 — greenlit decisions applied

### D1. "Cupboard" gloss for the wardrobe
- **Decision:** Render the source "big wardrobe" as **"cupboard"** throughout.
- **Rationale:** Target-age-nuance (T1 vocabulary); "cupboard" is the more familiar word for the youngest reader and is the term used in `concepts.the_wardrobe_threshold.tier_1` ("a magic cupboard").
- **Status:** Applied. Carries forward: the portal object is "the cupboard" at T1 for the remainder of the work.

### D2. Gentle evacuation (war → "went to live far away")
- **Decision:** OMIT war, air-raids, London, and the evacuation frame. Render the relocation as **"went to live far away in a big old house."**
- **Rationale:** The wartime frame is a background stressor; introducing it at T1 adds dread without narrative payoff at this tier. The Professor and Mrs. Macready are KEPT and rendered as kind so Lucy's safety is established at entry.
- **T1 warmth-addition (flag for reconcile):** Mrs. Macready's "biscuit and a smile" and "Lucy felt safe right away" are T1 additions (source has Mrs. Macready as housekeeper but not this beat). Source-neutral fact about Mrs. Macready's role stays in `analysis.yaml`.
- **Status:** Applied. The T1 reader does not know about the war.

### D3. Faun-as-friend commitment (T1 PROMISE)
- **Decision:** Render the Faun as an **unnamed kind friend**: "a kind face and a warm smile"; "the kind Faun"; shared laughter; mutual "Hello" + smile. His goat-hoofs and red scarf are KEPT (wonder); his strangeness is delightful, not uncanny.
- **Rationale:** Maps to `characters.mr_tumnus.tier_1` archetype ("The Best Friend (a kind faun)") and `key_scenes.lucy_enters_narnia.tier_1` framing ("wonder and friendship only"). The source's startle-and-drop is retained physically but reframed as comic.
- **reader-sim downstream commitment (LOAD-BEARING):** T1 commits hard to "the Faun is a friend" — kind face, warm smile, shared laughter. **This is a T1 PROMISE.** Later chapters must keep the Faun / Mr. Tumnus **friendly at tier-1** (cooperation reframing) or route source danger elsewhere, **because this promise cannot be broken for this reader.** Specifically: ch-02 (source: Tumnus's cave, the Witch's errand reveal, the temptation-and-repentance conflict) must at T1 either omit the errand, reframe it as cooperation, or route the danger off-Faun — the Faun cannot become a threat at T1.
- **Status:** Applied + PROMISE logged.

### D4. Cliffhanger → comic-friendship reframe
- **Decision:** The source chapter closes on the Faun's exclamatory cliffhanger ("Goodness gracious me!") with the encounter unresolved. T1 instead **closes on a completed comic-friendship beat**: Lucy laughs, the Faun laughs, they exchange names, the Faun smiles. The exclamation is retained but followed through to warmth.
- **Rationale:** T1 readers do not get an unresolved/ominous beat at chapter end; the encounter is closed with warmth and safety. Maps to `key_scenes.lucy_enters_narnia.tier_1` ("wonder and friendship only").
- **Status:** Applied. ch-01 ends on a smile, not a cliffhanger, at T1.

### D5. Agency Externalization on Edmund
- **Decision:** Render Edmund's source meanness (bad-tempered, sarcastic, mocking) as a **transient external mood**: "grumpy and tired that first night … But next day he felt bright again." No sarcasm, no mockery.
- **Rationale:** Agency Externalization (T1). At T1, Edmund's meanness is a passing mood (external state), not an internal trait — this seeds the T1 archetype "The Mixed-Up Friend" (`characters.edmund.tier_1`) without pathologizing him and without seeding a sibling-conflict thread the T1 reader would have to carry.
- **Status:** Applied. Edmund is "grumpy-but-recovered" at T1; no meanness seeded yet.

### D6. "armour" — British spelling retained
- **Decision:** Retain **"armour"** (British spelling) verbatim from source in the "shiny suit of armour" exploration beat.
- **Rationale:** Setting-anchoring (the house is English); the spelling carries quiet world-flavor without being a comprehension obstacle. Matches source exactly.
- **Status:** Applied.

### D7. Safety-rope visibility (Lucy's retreat path)
- **Decision:** Make Lucy's **retreat path explicit** at T1: the cupboard door remains visible from the wood, and "She could go home." (Source keeps the doorway in sight but does not spell out the reassurance.)
- **Rationale:** T1 safety discipline — the youngest reader can always see the way back. The wonder-threshold is preserved (Lucy still goes forward into the wood) but the safety-rope is visible.
- **Status:** Applied. Flag for continuity: later chapters that strand Lucy (e.g. Mr. Tumnus's cave) must honor the same safety-rope discipline or explicitly flag the break.

---

## ch-02 — greenlit decisions applied
> Decisions keyed `(work=narnia, tier=1, chapter=02)`.

### D8. Introduce the names "Mr. Tumnus" and "Narnia" at T1
- **Decision:** Name the kind Faun **"Mr. Tumnus"** and the snowy land **"Narnia"** — both withheld at ch-01.
- **Rationale:** ch-02 is the authorized naming point; mapping `characters.mr_tumnus.tier_1` supplies "Mr. Tumnus" and the `concepts`/`lucy_enters_narnia.tier_1` rows use "Narnia." ch-01 continuity explicitly logged the name as deferred to ch-02.
- **Status:** Applied. The Faun is "Mr. Tumnus" and the place is "Narnia" at T1 from here on.

### D9. Errand → externalized "rule," honoring the ch-01 T1 friend-promise
- **Decision:** Render the source kidnap-errand as **"a rule the Grumpy Witch gave me"** which Mr. Tumnus **rejects instantly** on the friendship ground ("Not to a friend! You are my friend now"). Lucy is **never framed as prey/target**; her source fright is OMITTED.
- **Rationale:** Agency Externalization (mandatory at T1) + the ch-01 D3 **T1 FRIEND-PROMISE** (the Faun cannot become a threat at T1). The errand is disclosed only as an external rule he refuses — no kidnap-threat feel, no fear left unresolved, Tumnus stays a kind friend, Lucy gets home safely.
- **Status:** Applied. safety-verifier (blocking): PASS.

### D10. Omit the Witch's punishment/petrification list
- **Decision:** OMIT the source's punishment list entirely (tail cut off, horns sawn off, turned to stone). No petrification at T1.
- **Rationale:** T1 omission-honor-set + violence-level 0 + nightmare-prevention. Turning-to-stone would be a nightmare payload; it is cut, not reframed, at this tier (the "long nap" reframe is reserved for if/when petrification is unavoidably load-bearing later).
- **Status:** Applied.

### D11. Grumpy-Witch external-state framing
- **Decision:** Render the White Witch as **"the Grumpy Witch"** (off-page): she "makes it snow" and "never lets it be Christmas." Never called evil; never acts on-page.
- **Rationale:** mapping `white_witch.tier_1` (external-state archetype); Agency Externalization. The "always winter, never Christmas" enchantment is kept (meaning-preserving) but attributed to a grumpy character, not innate evil.
- **Status:** Applied.

### D12. Safe-home / safety-rope honored at the cave and return
- **Decision:** Keep the cave a **safe cosy haven**, and make the retreat path **visible** at the lamp-post ("the cupboard door … the way home") before Lucy leaves; close with **home restored** ("I'm back! I'm all right!").
- **Rationale:** Honors the ch-01 D7 safety-rope discipline flagged specifically for "Mr. Tumnus's cave." Lucy is never stranded without a visible way home.
- **Status:** Applied.
