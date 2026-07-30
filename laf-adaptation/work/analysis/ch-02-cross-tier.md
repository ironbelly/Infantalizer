# Cross-Tier Reconciliation — narnia ch-02

tiers: [1, 2, 3, 5]     mode: parallel     source: work/analysis/ch-02.yaml

*Produced by tier-coordinator (step 10). Parallel fan-out (default) against the single shared analysis
(analyst ran once, tier-invariant). This report reconciles the four tiers' `adapted.md` outputs before
chronicler (step 11) promotes any canon. The coordinator never writes canon.*

Chapter II ("What Lucy Found There") is the **temptation-and-repentance** chapter:
`compound_scene: false`, violence instances = 0, death instances = 0. The two flagged elements are
`emotional` (Tumnus's breakdown + confession) and `abstract` (the Witch's-pay errand + the
temptation/repentance moral machinery), both MODERATE and both resolving safely (Lucy returns home
unharmed). The gate-relevant axis here is therefore **disclosure of the kidnap-errand and the Witch's
threatened punishments** across the tier ladder — not violence/death content, of which there is none.
The work-level allegory (Aslan / Passion / Deep Magic) correctly does NOT appear at any tier: the
source withholds it here, and per `narnia-mapping.yaml` it is named openly only from the
sacrifice/resurrection chapters. Ch-02's redemption meaning is carried by EVENTS (confess → repent →
freely forgiven), not by naming.

## Shared source anchors (from analysis ch-02.yaml)
- The Faun is named **Mr. Tumnus** and confirms Lucy is a Human ("Daughter of Eve") — CERTAIN (events[seq:1])
- The land is **Narnia** (lamp-post to Cair Paravel); Lucy came "through the wardrobe" (Spare Oom / War Drobe) — CERTAIN (events[seq:2])
- Tumnus invites Lucy to **tea at his cave**; they walk arm-in-arm under his umbrella — CERTAIN (events[seq:3])
- The **cosy firelit cave**: reddish stone, carpet, two chairs, father's grey-bearded portrait, shelf of books — CERTAIN (events[seq:4])
- A **wonderful tea** + Tumnus's **tales of forest life** (Nymphs/Dryads, the milk-white Stag, Red Dwarfs, Silenus/summer) — CERTAIN (events[seq:5])
- The **straw flute**; hours pass; Lucy rouses and says she must go home — CERTAIN (events[seq:6])
- Tumnus **breaks down weeping**; confesses he is **in the pay of the White Witch**, who keeps Narnia "always winter and never Christmas" — CERTAIN (events[seq:7])
- Tumnus confesses he is a **kidnapper**: ordered to catch any Human and hand them over; Lucy is the first; he had **planned to lull her asleep and betray her** — CERTAIN (events[seq:8])
- The Witch's **threatened punishments** (tail/horns/beard/hoofs; **turned to stone** until the four thrones at Cair Paravel are filled) — CERTAIN (events[seq:9])
- Tumnus **repents** — "I hadn't known what Humans were like before I met you" — and leads Lucy quietly back through the **spy-filled wood** to the lamp-post — CERTAIN (events[seq:10])
- At the lamp-post Lucy **sees the daylight of the wardrobe door**; forgives Tumnus; lets him keep her **handkerchief** — CERTAIN (events[seq:11])
- Lucy runs back, tumbles out of the wardrobe into the **same empty room**, calls that she is back and "all right" — CERTAIN (events[seq:12])

Work-level meaning (kb/adaptation-mapping/narnia-mapping.yaml): Christian redemption allegory
(Passion / Resurrection / Deep Magic) — IMPLICIT at T1–T2, MAY be named at T3+, but structurally it
does not surface in ch-02 at any tier (this is not a sacrifice chapter).
Chapter-level meaning (analysis ch-02.yaml `meaning`): temptation-and-repentance — a host secretly
enlisted by evil is redeemed by coming to know his intended victim as a friend; friendship + truthful
kindness melt a betrayal in motion; conscience overrides the enemy's orders at real cost; seeds the
larger confession-repentance-forgiveness arc in miniature.

## Per-tier renderings (traceability)
| Element | T1 | T2 | T3 | T5 | shared anchor |
|---------|----|----|----|----|---------------|
| The Faun named | "Mr. Tumnus" (authorized at T1 by mapping mr_tumnus.tier_1) | "Mr. Tumnus" | "Mr. Tumnus" ("Daughter of Eve" address kept) | preserve | events[seq:1] |
| The Witch | "the Grumpy Witch … makes it snow … never Christmas" (external-state) | "the White Witch … holds Narnia under her spell … always winter, never Christmas" (mean antagonist) | "the White Witch … all Narnia under her thumb … always winter and never Christmas" (named tyrant) | preserve | events[seq:7] |
| The kidnap-errand | "a rule the Grumpy Witch gave me … bring her any girl I met" — abandoned instantly for friendship; Lucy never framed as prey | "a mean thing … I planned to keep you until you slept, then fetch the Witch" — a mean plan he abandons; ashamed | "I'm a kidnapper for her … I meant to wait until you were asleep, and then go and tell her" — named openly; owns it | preserve (full confession, "doing it now, this very moment") | events[seq:8] |
| Lucy's fright | omitted (Lucy never frightened for herself at T1) | "jumped up, a little frightened" (bounded, resolves at once) | "turning rather pale" (real, survivable) | preserve ("turning very white") | events[seq:8] |
| The Witch's punishments | OMITTED entirely (no tail/horns/stone) | OMITTED (off-page; not mentioned) | "cruel punishments … might even turn me to stone … a statue until the four thrones are filled" (petrification named, mutilation list CUT — "no dwelling") | preserve (tail/horns/beard/hoofs/stone in full) | events[seq:9] |
| The repentance | "I could never do that. Not to a friend! You are my friend now." | "I couldn't. Not now that I know you … I could never hand a friend to the Witch." | "I hadn't known what Humans were like before I met you. Now that I know you, I could never hand you over." | preserve | events[seq:10] |
| Safe return | sees "the cupboard door … the way home" then tumbles into the empty room | sees "the wardrobe door" then tumbles into the empty room | sees "the wardrobe door" then jumps out into the empty room | preserve | events[seq:11,12] |
| Ending resolution | fully resolved + warm (Tumnus's happy smile, no open worry) | mild hook ("hope you won't get into trouble") | genuine delayed-resolution thread (Tumnus now at real risk) | preserve (Lewis's beat) | events[seq:11,12] |

## Checks

- **A source-fidelity:** **PASS.** Every transformed element in T1/T2/T3 traces to a CERTAIN fact in
  the shared analysis (`work/analysis/ch-02.yaml`). No tier introduces a fact absent from the analysis:
  no invented character, no event outside seq 1–12, no forward content beyond Lucy's return. The
  errand, the Witch, the tea, the tales, the flute, the repentance, the spy-wood, the handkerchief, and
  the safe return all map to numbered events. T5 is a preservation record pointing at
  `source/narnia/ch-02.txt` — source-faithful by construction, so Check A holds trivially for T5.

- **B disclosure-leak (no downward leak — each tier defers what its envelope requires):** **PASS.**
  - **T1 correctly DEFERS** everything its envelope requires deferred: the *word* "kidnapper," the
    framing of Lucy *as prey/target*, Lucy's own fright, and the entire punishment/petrification list
    are all absent at T1. The errand is disclosed only as an externalized "rule" the Grumpy Witch gave,
    abandoned on the friendship ground — no downward leak of the menace T1 must withhold.
  - **T2** discloses the "mean plan" and Lucy's bounded fright but still DEFERS the punishment list and
    the petrification (off-page) — correct for the misunderstanding/contest envelope.
  - **T3** names the errand ("kidnapper"), the petrification threat, and the thrones-prophecy hint, but
    DEFERS the graphic mutilation detail ("no dwelling") — correct for the transition envelope.
  - **No upward content appears anywhere it shouldn't:** no tier surfaces the work-level allegory
    (Aslan / Passion / Deep Magic) — correct, since ch-02 is not a sacrifice chapter and the source
    withholds it here. No tier introduces ch-III+ content (Edmund, the Witch on-page, the Stone Table).
  - The name "Mr. Tumnus" appearing at ALL FOUR tiers is **not** a leak: ch-02 is the authorized
    naming point (mapping `characters.mr_tumnus.tier_*` each supply "Mr. Tumnus"; the ch-01 continuity
    files each recorded the name as *deferred to ch-02*). Introducing it here at every tier is the
    intended, coordinated disclosure.

- **C monotonicity (maturity T1 ≤ T2 ≤ T3 ≤ T5 for every shared element):** **PASS.**
  - *The Witch:* "Grumpy Witch"/external-state (T1) ≤ "mean antagonist under her spell" (T2) ≤ "tyrant,
    all Narnia under her thumb" (T3) ≤ preserve (T5). Monotone.
  - *The errand:* externalized "rule," abandoned, Lucy-not-prey (T1) ≤ "a mean thing" planned then
    abandoned (T2) ≤ "I'm a kidnapper … I meant to wait until you were asleep" owned openly (T3) ≤
    preserve, "doing it now, this very moment" (T5). Monotone.
  - *Lucy's fright:* omitted (T1) ≤ "a little frightened," resolves at once (T2) ≤ "turning rather
    pale," survivable (T3) ≤ preserve, "turning very white" (T5). Monotone.
  - *The punishments:* omitted (T1) ≤ omitted/off-page (T2) ≤ petrification named, mutilation cut (T3)
    ≤ full list preserved (T5). Monotone (T1 = T2 on this element is permitted — non-strict ≤).
  - *Ending:* fully-resolved-warm (T1) ≤ mild hook (T2) ≤ genuine delayed-resolution thread (T3) ≤
    preserve Lewis's beat (T5). Monotone.
  - *Agency of Tumnus's wrongdoing:* fully externalized (T1, `agency_externalization: mandatory`) ≤
    externalized-with-ownership-of-the-plan (T2, mandatory + `permits_misunderstanding_as_cause`) ≤
    owned (T3, `optional` — not applied) ≤ preserve (T5, `forbidden`). Monotone.
  No inverted rendering on any shared element.

- **D meaning-preserved:** **PASS.** Read the work `meaning:` from
  `kb/adaptation-mapping/narnia-mapping.yaml` (redemption/forgiveness arc; do NOT strip the
  betrayal-forgiveness structure at any tier; allegory implicit at T1–T2, nameable at T3+, absent where
  the source withholds it). Every tier preserves the chapter-level temptation-and-repentance beat: a
  host enlisted by evil is turned by coming to know his intended victim as a friend, and is freely
  forgiven.
  - **T1** keeps it in miniature and externalized: a mixed-up friend has a "rule" he rejects *because*
    Lucy is his friend; she forgives; no allegory imposed (correct — implicit at T1). Betrayal-forgiveness
    structure INTACT (not stripped), just softened at the surface.
  - **T2** keeps the abandoned-mean-plan + forgiveness explicitly ("changed your mind … the brave thing
    to do"), allegory still implicit — correct.
  - **T3** names the errand and the repentance in full ("I hadn't known what Humans were like before I
    met you"); the redemption meaning is event-carried, allegory correctly NOT named here (ch-02 is not
    a sacrifice chapter). No meaning added where the source withholds it; none stripped.
  - **T5** preserves the confession-repentance-forgiveness whole.
  No tier strips the betrayal-forgiveness structure; no tier adds allegory the source withholds here.
  status_meaning: **Meaning-PRESERVED.**

## Verdict

status: RECONCILED
conflicts: []
