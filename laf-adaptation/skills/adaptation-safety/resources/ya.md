# Young-Adult Craft — Tier 5

*Authored craft guidance (not a verbatim carry). Synthesizes the Tier-5 profile into "how to write for
15-17-year-olds well." This doc **informs** the writer; it is distinct from the `/adaptation-safety`
rubric (which does not apply at T5 — safety_check is T1-2 only). Sourced from
`config/age_profiles/tier_5_young_adult.yaml` (`adaptation_philosophy` + `supplementary_approach` +
`narrative_complexity`).*

## Meaning, not sanitization — the core principle

The Tier-5 paradigm is **minimal transformation, preserve author intent**. Its `adaptation_philosophy`
states the whole posture: **"Adaptation means accessibility, not sanitization."** A formal-operational
reader (Piaget) with social-contract moral reasoning (Kohlberg stage 5) can hold full complexity, so the
writer's job is to remove *access barriers*, not *difficulty*. Concretely, the profile permits full
emotional spectrum (`trauma_portrayed`, `despair_explored` with `meaningful_treatment`), moral ambiguity
at level 9 (`tragic_endings`, `antiheroes`, `no_clear_right_answer`), and violence at level 8 focused on
meaning (forbidding only `gratuitous_sexual_violence` and `torture_pornography`).

## Unreliable narrator and the full range of irony

The Tier-5 `narrative_complexity` block explicitly enables devices that lower tiers cannot support:
`unreliable_narrator: true`, `irony: "full_range"`, plus `parallel_plotlines` and `flashbacks`. Use them.
A T5 adaptation may withhold, mislead through a narrator, and run dramatic/structural irony at full
strength — the reader is expected to detect the gap between narration and truth. This is the opposite of
the T1-2 posture, where clarity and safety dominate.

## When TO intervene (remove access barriers only)

Per `adaptation_philosophy.when_to_intervene`, intervene for:
- **Genuinely archaic language** (the profile's `linguistic.archaic_handling: footnote_optional` — gloss
  or footnote rather than rewrite).
- **Historical context needed.**
- **Cultural references now obscure.**

These are accessibility aids. Note `linguistic.approach: preserve_original` and
`sentence_structure.approach: preserve_author_voice` — you preserve the prose and add support around it,
you do not rewrite the voice.

## When NOT to intervene (preserve the work)

Per `adaptation_philosophy.when_not_to_intervene`, do **not** soften or remove:
- **Difficult themes.**
- **Moral complexity.**
- **Character deaths.**

And critically, `transformation_rules.agency_externalization.mode: "forbidden"` — the profile's stated
reason is **"Patronizing; undermines character complexity."** At T5, relabeling malice as a temporary
state would strip exactly the complexity this tier preserves. Conflict, death, and villain motivation all
carry `mode: preserve`.

## Supplementary approach (support around, not inside, the text)

Rather than altering the prose, offer the `supplementary_approach.recommended` scaffolds *alongside* it:
- **Character guide** for large casts.
- **Timeline** for complex chronology.
- **Context notes** for historical background.
- **Discussion questions** for themes.

This is the T5 craft signature: keep the author's text intact and difficult, and add optional apparatus
that makes it *accessible* without making it *simpler*.
