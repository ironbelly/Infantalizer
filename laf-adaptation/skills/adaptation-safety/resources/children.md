# Children's Fiction Craft — Tiers 1-3

*Authored craft guidance (not a verbatim carry). Synthesizes the tier-1 and tier-3 transform prompts and
the tier profiles into "how to write children's fiction well across T1-3." This doc **informs** the
writer; it is distinct from the `/adaptation-safety` **rubric**, which **gates** (PASS/FAIL). Sourced from
`prompts/transformation/tier_1_transform.md`, `prompts/transformation/tier_3_transform.md`, and
`config/age_profiles/tier_1_preschool.yaml` + `tier_3_middle_elementary.yaml`.*

## The arc: protect from complexity (T1-2) → scaffold complexity (T3)

The single organizing idea across these tiers is a shift **from protecting the reader from complexity to
scaffolding them into it**. At T1-2 you remove or externalize what a preoperational/early-concrete child
cannot yet hold; at T3 — the transition tier — you reintroduce complexity deliberately, with support.

## Tier 1-2: prosocial centering, maximum safety

- **Externalize all negative agency.** Badness is a temporary state or an accident, never an innate
  quality. "Sauron was evil" → "The Grumpy King was grumpy because his land had no sunshine"; "Gollum
  attacked" → "The silly creature wanted to play a game." (This is the load-bearing rule — see
  `/adaptation-rules` `resources/agency.md`.)
- **Convert violence to cooperation.** Battle → Big Tidy-Up; War → Helping Adventure; Attack → making a
  mess; Enemy army → noisy, messy helpers.
- **Death → journey or rest.** "died" → "went on a new adventure"; "killed" → "needed to rest"; "dead" →
  "resting." Never use the direct death words at T1.
- **Simple characters.** Protagonist = Brave Friend on a Special Job; Hero-Leader = the Great Helper;
  Antagonist = the Grumpy/Messy Character (always redeemable).
- **Emotional resolution is mandatory.** Permitted emotions T1: happy, sad, scared, grumpy, tired,
  excited, brave, kind (T2 adds worried, lonely, embarrassed, proud, frustrated). Forbidden: despair,
  trauma, grief, rage. **Every negative emotion resolves positively by chapter end.** → this is what the
  rubric's **Section 3 (Emotional Safety)** gates.
- **Episodic structure, positive resolution.** Keep the chapter self-contained and end on safety and a
  solved problem.

**Worked T1 example** (from the tier-1 transform prompt):
> Source: "The orcs attacked. Many soldiers fell. Éowyn slew the Witch-king."
> Tier 1: "The noisy grumbles made a big mess at the city walls. Many helpers got very tired. Brave
> Éowyn helped everyone stay safe."

### Cross-references to the safety rubric (the gate)
- **Section 4 — Safe-Home schema:** home is a safe haven; if threatened it is restored; no permanent
  destruction; family relationships positive. Write the home this way from the start so the gate passes.
- **Section 5 — Nightmare prevention:** monsters are grumpy/silly, not terrifying; darkness is temporary
  and fixable; fear is manageable. Frame every scary beat this way.
- **Section 6 — Linguistic ceilings:** T1 max 12 words/sentence, max 1 clause, no passive voice,
  kindergarten vocabulary, ~800-word chapter ceiling. (The verifier reads these from
  `kb/tiers/tier_<N>.yaml.linguistic` at runtime — write to the profile's numbers, not a hard-coded one.)

## Tier 3: the transition — scaffold complexity

T3 (ages 9-11) unlocks what T1-2 withheld, with support:
- **Violence: weight, not gore.** Show stakes and consequences without graphic detail.
- **Death: direct but gentle.** Name death directly ("died" is now acceptable language); focus on
  meaning and emotional impact.
- **Villain motivation: understandable.** Villains can have internal motivations — show HOW they became
  this way.
- **Hero failure: with context.** Heroes can fail; show the failure, why it happened, and what redeemed
  it. Moral ambiguity (shades of gray) is permitted.

**Still required at T3:** consequences for actions, understandable motivations, hope even in dark content,
suffering that has purpose. **Still forbidden:** gratuitous violence/gore, torture or prolonged suffering,
suicidal ideation, despair without hope, sexual content.

**T3 linguistic parameters:** grade level 3-5, max 20 words/sentence, ~2,500-word chapter ceiling;
cliffhangers permitted.

**Worked T1→T3 example** (the Denethor scene, from `prompts/transformation/tier_3_transform.md`'s T1→T3
worked example) shows the scaffolding shift:
> Tier 1: "The city leader was very sad. He closed all the windows. Gandalf opened them and let the
> sunshine in."
> Tier 3: "Denethor had given up hope. The palantír had shown him only darkness. When Faramir was carried
> in wounded, something broke inside him. Gandalf found him preparing a terrible thing. But Pippin was
> already running to find help. They pulled Faramir from danger just in time. Denethor was lost to his
> despair. But Faramir survived."

The T3 rendering names the despair and its consequence directly (weight, not gore) while still landing on
hope (Faramir survives) — the transition tier's signature: complexity with a scaffold.
