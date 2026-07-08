# Prep Brief — The Lord of the Rings  (tolkien)

> This package was produced by a Phase-3 SMOKE PROVE of the `/laf:prep` pipeline on a synthetic
> 259-word Tolkien pastiche fixture ("The Siege at the Grey City"). The fixture is a proof text,
> not copyrighted LOTR prose; Phase-0 source access is FULL. The work-level framing is grounded in
> the readable fixture (text track) with context-track context at the PROBABLE ceiling.

## Decisions ratified

| # | Decision | Source |
|---|---|---|
| 1 | Source access = FULL (Phase-0 PASSED); text track grounded in `laf-adaptation/source/tolkien/ch-01.txt`. | 20-analysis metadata |
| 2 | Work-level `meaning:` = hope against despair + redemptive courage + the corrupting nature of power. Effective confidence = PROBABLE. | 20-analysis `meaning:` |
| 3 | Tier set active = {1, 2, 3, 5} (the contract default; no narrowing — T2 authored, T4 interpolated at request time). | 50-greenlight |
| 4 | Compound scenes: Siege of the Grey City; Théoden's fall and Éowyn's stand. §2.1 reconciliation baked into `10-challenges.yaml`. | 10-challenges compound_scenes |
| 5 | Allegory-stance: adopt Tolkien's anti-allegory position (the meaning is carried by events, not authorial gloss). | Question gate → answered |
| 6 | Death-honor for Théoden: at T1 a "long rest", at T3 a named gentle death, at T5 preserved. | Question gate → answered |
| 7 | Battle-scope: T1 tidy-up, T3 summarize-at-altitude, T5 preserve. | Question gate → answered |
| 8 | Target-age nuance: T1 young (4–6), T3 older (10–12), T5 teen/adult. | Question gate → answered |

## Cross-tier spine summary

| Challenge | Tier 1 | Tier 2 | Tier 3 | Tier 5 |
|---|---|---|---|---|
| mass-warfare | Big Tidy-Up; tide of grumbles | A stern scolding; the tide turns | Summarize, show stakes, foreground the holding | Preserve — terrible battle, splintering spears, wet ground |
| psychological-collapse (Denethor) | Sad Leader has a rest; omit "All is ended" | A heavy heart; withdraws quietly | Imply despair; too sad to answer | Preserve — broken, wall-turned |
| sacrifice-and-return (Théoden) | Long rest after the helping | Falls back spent; helped up | Falls and does not rise; Éowyn foregrounded | Preserve — struck by the Nazgûl, dies |
| petrification-body-horror (Nazgûl) | Grumpy Riders; loud grumble | Unsettling riders; a chill | Named dread, bound paralysis | Preserve — cry unmen brave men |
| allegory-stance | No moral inserted | Light touch; meaning via outcome | Surface meaning through outcome | Preserve anti-allegory |
| omission-honor-set | Omit slaughter, Denethor detail, fall imagery | Omit gore and the darkest detail | Omit gore only | Preserve as written |
| target-age-nuance | 4–6 | 7–9 | 10–12 | Teen/adult |
| violence-level (deterministic) | None on-page | Mild, brief | Bounded | Preserve |
| death-euphemism (deterministic) | journey_or_sleep | rest_or_sleep | Named, gentle | Preserve (no euphemism) |

## Meaning to preserve

> Hope against despair — the city holds and the sun returns even when the steward has broken, the
> king has fallen, and the field is heavy with grief. Redemptive courage: standing over the fallen
> at one's own cost. The corrupting nature of power: Sauron's will presses down cold and patient,
> unshown but felt. **Neither add nor strip this meaning at any tier.**

- `text_confidence`: PROBABLE
- `context_confidence`: PROBABLE
- effective `confidence`: PROBABLE (= min)

## Answered questions

> This prove auto-confirms the gate; the human-judgment answers below are the coordinator's
> defaults, recorded as ANSWERED (not DEFAULTED) in `70-traceability.md`.

| Q | A |
|---|---|
| Allegory-stance — what is the stance? | Adopt Tolkien's anti-allegory position: the meaning is intrinsic to events; no tier adds a moral frame, no tier strips the resonance. |
| Omission-honor-set — what MUST be omitted vs preserved at low tiers? | T1 omits the slaughter, Denethor's wall-turning, Théoden's fall imagery; preserves the holding, the helper's stand, the sun's return. T3 omits only the gore. |
| Target-age-nuance — precise age band within each tier? | T1 young (4–6); T3 older (10–12); T5 teen/adult. |
| Mass-warfare — how much battle to show? | T1 tidy-up at community scale; T3 summarize at altitude; T5 preserve the terrible battle as written. |
| Sacrifice-and-return — how much of Théoden's death to imply? | T1 long rest; T3 named gentle death with Éowyn foregrounded; T5 preserved. |
| Psychological-collapse — how much of Denethor's despair to imply? | T1 reframed as needing rest; T3 acknowledged, cost felt; T5 preserved. |
| Petrification-body-horror — reframe or restore the Nazgûl? | T1 reframe (Grumpy Riders); T3 named with bounded paralysis; T5 preserve. |

## Open risks / low-confidence entries

Every mapping entry currently sits at effective PROBABLE because the context track is capped at
PROBABLE (secondary-source ceiling, R6). No entry is currently UNCERTAIN.

Open risks:

1. **Fixture scope.** The package is grounded in a 259-word single-scene fixture; the full
   work-level framing (the whole LOTR arc) is context-track inference at the PROBABLE ceiling. A
   future run against the full novel would tighten the text-track confidence on characters/concepts
   not present in this fixture (Frodo, Sam, the Ring, Mount Doom, etc. — none appear in ch-01.txt).
2. **Compound-scene reconciliation.** The §2.1 protocol bakes in a per-tier reconciliation; the
   `meaning_survives: true` verdict is the coordinator's, not yet independently verified. The
   rewrite phase's `safety-verifier` is the downstream gate on this.
3. **Prior-art overwrite.** This run OVERWRITES the shipped `tolkien-mapping.yaml` (0.1 kb) and
   `tolkien_mapping.yaml` (root) files. The pre-run 5-key body style (inline-flow tier rows) is
   preserved; only the data changes (and the kb copy gains `meaning:`).
4. **Tier 4.** T4 is not stored as its own tier rows; it is interpolated at request time (T3 floor,
   T5 ceiling, conservative midpoint) and never stored as a file. (T2 IS authored: the active set is
   the contract default {1, 2, 3,5}.)
