# Changelog

## [1.0.0] - 2026-01-25

### Added

#### Core Framework
- Five-tier age profile system (Tiers 1-5, ages 3-17)
- Configuration-driven architecture using YAML
- Developmental psychology foundation (Piaget, Kohlberg, Vygotsky)

#### Age Profiles
- `tier_1_preschool.yaml` - Full transformation, maximum safety (ages 3-5)
- `tier_2_early_elementary.yaml` - Contest/competition paradigm (ages 6-8)
- `tier_3_middle_elementary.yaml` - Transition tier, complexity unlocked (ages 9-11)
- `tier_5_young_adult.yaml` - Minimal transformation mode (ages 15-17)

#### Transformation Rules
- `thematic.yaml` - Violence, death, conflict, agency externalization rules
- `character.yaml` - Archetype mappings, heroism translation by tier

#### Concept Mapping
- `universal_mappings.yaml` - Cross-work concept translations
- `tolkien_mapping.yaml` - Lord of the Rings specific mappings

#### Prompts
- `chapter_analysis.md` - Source analysis with v2.0 anti-hallucination protocol
- `tier_1_transform.md` - Preschool adaptation prompt
- `tier_3_transform.md` - Transition tier adaptation prompt
- `safety_check.md` - Tier 1-2 verification checklist

#### Documentation
- Complete system specification (SPEC.md)
- Design decision documentation
- Conversation logs from development
- Quick start guide

### Design Decisions
- Tier 4 profile deferred (interpolate from Tiers 3 and 5)
- Linguistic config files consolidated into age profiles
- Framework is prompt-based, not software package
