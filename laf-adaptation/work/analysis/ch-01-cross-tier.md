# Cross-Tier Reconciliation — narnia ch-01

tiers: [1, 2, 3, 5]     mode: parallel     source: work/analysis/ch-01.yaml

*Produced by tier-coordinator (step 10). Parallel fan-out (default) against the single shared analysis
(analyst ran once, tier-invariant). This report reconciles the four tiers' `adapted.md` outputs before
chronicler (step 11) promotes any canon. The coordinator never writes canon.*

Chapter 1 ("Lucy Looks into a Wardrobe") is a gentle portal chapter: `compound_scene: false`,
violence instances = 0, death instances = 0. There is no violence/death/allegory-machinery in this
chapter to gate. Tier differences here are **register** (war framing, Edmund's temper handling,
ending resolution, detail retention, Faun reassurance), not content-disclosure. The work-level
allegory (Aslan / Passion / Deep Magic) correctly does NOT appear at any tier — the source withholds
it here too.

## Shared source anchors (from analysis)
- Four children Peter, Susan, Edmund, Lucy — CERTAIN (characters[])
- Wartime evacuation from London — CERTAIN (events[seq:1]; summary)
- Edmund bad-tempered / prickly — CERTAIN (characters[Edmund])
- The Professor, shaggy white hair, large country house — CERTAIN (characters[Professor])
- Mrs. Macready, the housekeeper — CERTAIN (characters[Mrs. Macready])
- Rainy day → indoor exploration through a series of rooms — CERTAIN (events[seq:4,5])
- Empty room holds one big wardrobe (looking-glass door) — CERTAIN (events[seq:5])
- Peter "Nothing there!"; all leave but Lucy — CERTAIN (events[seq:6])
- Lucy enters among the fur coats; wardrobe gives way to snow + branches — CERTAIN (events[seq:6,7])
- Snowy night wood; keeps wardrobe doorway in sight; walks to a distant light — CERTAIN (events[seq:8])
- The light is a lamp-post in the wood — CERTAIN (events[seq:9])
- A startled Faun (goat-legs, horns, umbrella, parcels) drops parcels: "Goodness gracious me!" — CERTAIN (events[seq:10]; closing_sentence)

Work-level meaning (kb/adaptation-mapping/narnia-mapping.yaml): Christian redemption allegory
(Passion / Resurrection / Deep Magic) — but per mapping it stays IMPLICIT at T1–T2, MAY be named only
at T3+, and structurally it does not surface in ch-01 at any tier.
Chapter-level meaning (analysis ch-01.yaml `meaning`): the portal/wonder beat — a child's first
threshold-crossing out of the ordinary wartime house into a magical reality, curiosity over fear.

## Per-tier renderings (traceability)
| Element | T1 | T2 | T3 | T5 | shared anchor |
|---------|----|----|----|----|---------------|
| War framing | "went to live far away … left the city on a train" (no war word) | "Because of the war, they left the city on a train" | "during the war … sent away from London because of the air-raids" | preserve (air-raids, as source) | events[seq:1]; summary |
| Edmund's temper | "grumpy and tired that first night … next day he felt bright again" (externalized + resolved) | "tired and grumpy … everyone was too sleepy to mind for long" (externalized, mild) | "tired and pretending not to be tired, which always made him bad-tempered" (own trait) | preserve (sarcasm intact) | characters[Edmund] |
| The wardrobe / portal | "one big cupboard … coats soft and furry … Crunch, crunch … Snow!" | "one big wardrobe with a mirror in the door … soft crunched … Snow?" | "one big wardrobe … looking-glass in the door … soft and powdery and extremely cold" | preserve | events[seq:5,6,7] |
| The Faun | "little hoofs, just like a goat! … kind Faun … kind face and a warm smile" (reassuring) | "very strange little person … furry like a goat's … two neat little hoofs" (uncommitted) | "very strange person … legs shaped like a goat's … goat's hoofs … a tail too" (uncommitted, full detail) | preserve (full description) | characters[Faun]; events[seq:10] |
| The ending | "'Goodness gracious me!' … Lucy laughed … 'Hello, Lucy,' said the kind Faun" (resolved to friendship) | ends on "'Goodness gracious me!' exclaimed the Faun" (mild hook) | ends on "'Goodness gracious me!' exclaimed the Faun" (genuine cliffhanger) | preserve (Lewis's cliffhanger) | closing_sentence |

## Checks
- **A source-fidelity:** PASS. Every transformed element in T1/T2/T3 traces to a CERTAIN fact in
  `shared_analysis`. No tier introduces a fact absent from the analysis (no invented character, event,
  or Ch-II content). T5 is a preservation record pointing at `source/narnia/ch-01.txt` — source-faithful
  by construction, so Check A holds trivially for T5.
- **B disclosure-leak:** PASS. No tier discloses beyond its envelope. Critically: NO tier names the
  Faun "Mr. Tumnus", and NO tier includes Ch-II content (the Faun's cave, the Witch's errand, the
  Faun's conflict). All four correctly stop at the Faun's "Goodness gracious me!". T1's short friendly
  coda ("Hello, Lucy," said the kind Faun) introduces no plot disclosure — it is register/reassurance,
  not forward Ch-II content. There is no death / battle / allegory disclosure in this chapter to gate.
- **C monotonicity:** PASS. maturity(T1) ≤ maturity(T2) ≤ maturity(T3) ≤ maturity(T5) for every shared
  element. War framing: no-war-word ≤ "war" ≤ "air-raids" ≤ preserve. Edmund: externalized+resolved
  (T1 `agency_externalization: mandatory`) ≤ externalized-mild (T2 mandatory) ≤ own-trait/internal
  (T3 `optional`) ≤ preserve (T5 `forbidden`). Ending: resolved-friendship ≤ mild-hook ≤ cliffhanger ≤
  cliffhanger-preserved. Faun reassurance: T1 "kind/friend" (max reassurance = least mature = the
  correct floor) ≤ T2/T3 "very strange"/uncommitted ≤ T5 preserve. No inverted rendering.
- **D meaning-preserved:** PASS. Every tier preserves the chapter-level portal/wonder beat — a child's
  first threshold-crossing, curiosity over fear (the feel/smell of fur, "a step or two further", the
  wardrobe doorway kept in sight, the lamp-post among the trees). No tier adds the work-level allegory
  where ch-01 withholds it, and no tier strips the wonder. status_meaning: Meaning-PRESERVED.

status: RECONCILED
conflicts: []
