<!-- Canonical thematic transformation rule source — carried VERBATIM from config/transformation_rules/thematic.yaml (zero rework; no key renamed, no value altered). This is the authoritative rule source per kb-formats.md §2.3. -->

```yaml
# Thematic Transformation Rules
# Core engine rules for violence, death, conflict, and moral content

violence_transformation:
  tier_1:
    battle: {target: "cooperative_activity", example: "Battle → Big Tidy-Up"}
    attack: {target: "bumping_or_chasing"}
    injury: {target: "pratfall", example: "wounded → got a boo-boo"}
    death: {target: "going_away_or_sleeping"}
    weapons: {action: "remove_entirely"}
  tier_2:
    battle: {target: "contest_or_race"}
    attack: {target: "chase_or_struggle"}
    death: {target: "passed_away_offscreen"}
  tier_3:
    battle: {target: "battle_summarized", approach: "Stakes, not gore"}
    death: {target: "died_stated_gently", focus: "emotional impact"}
  tier_4_5:
    mode: "minimal_transformation"

conflict_transformation:
  tier_1:
    mode: "mandatory"
    translations: {war: "helping_project", siege: "big_cleanup", enemy_army: "noisy_helpers"}
  tier_2:
    mode: "mandatory"
    translations: {war: "contest", siege: "challenge", enemy_army: "opposing_team"}
  tier_3:
    mode: "optional"
  tier_4_5:
    mode: "preserve"

agency_externalization:
  core_principle: "Badness is always a STATE or ACCIDENT, never innate."
  tier_1:
    mode: "mandatory"
    examples:
      - {source: "Dark Lord, evil", target: "Grumpy King, no sunshine"}
      - {source: "driven mad by despair", target: "very sad, windows closed"}
      - {source: "consumed by greed", target: "really wanted to play"}
  tier_2:
    mode: "mandatory"
    softening: "permits_misunderstanding_as_cause"
  tier_3:
    mode: "optional"
  tier_4_5:
    mode: "forbidden"

death_handling:
  tier_1:
    strategy: "journey_or_sleep"
    never_use: ["die", "dead", "death", "kill"]
    translations: {death: "new adventure", dying: "very long rest"}
  tier_2:
    strategy: "gentle_acknowledgment"
    can_use: ["passed away", "lost", "gone"]
  tier_3:
    strategy: "direct_but_gentle"
    can_use: ["died", "death", "killed"]
    focus: "emotional_impact"
  tier_4_5:
    strategy: "preserve_original"

villain_motivation:
  tier_1:
    mode: "external_state"
    villains_are: "grumpy, sad, confused"
    always_redeemable: true
  tier_2:
    mode: "misunderstanding"
    villains_are: "mean because they don't understand"
  tier_3:
    mode: "can_be_internal"
    requirements: ["motivation must be understandable"]
  tier_4_5:
    mode: "complex_internal"

heroism_definition:
  tier_1:
    mode: "prosocial_only"
    heroic: ["helping", "sharing", "comforting", "persevering"]
    never_heroic: ["violence", "killing"]
  tier_2:
    mode: "prosocial_with_competition"
    heroic: ["tier_1 + fair_play, sportsmanship"]
  tier_3:
    mode: "includes_defense"
    heroic: ["tier_2 + defending_others, sacrifice"]
  tier_4_5:
    mode: "full_spectrum"
```
