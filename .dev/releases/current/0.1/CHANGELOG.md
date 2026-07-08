# Changelog

All notable changes to the Literary Adaptation Framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- `universal_mappings.yaml` - Cross-work concept translations (death, evil, war, etc.)
- `tolkien_mapping.yaml` - Lord of the Rings specific character/concept mappings

#### Prompts
- `chapter_analysis.md` - Source analysis with v2.0 anti-hallucination protocol
- `tier_1_transform.md` - Preschool adaptation operational prompt
- `tier_3_transform.md` - Transition tier adaptation prompt
- `safety_check.md` - Tier 1-2 verification checklist

#### Documentation
- Complete system specification (SPEC.md)
- Design decision documentation
- Conversation logs from development
- Quick start and workflow guides

### Design Decisions
- Tier 4 profile deferred (interpolate from Tiers 3 and 5)
- Linguistic config files consolidated into age profiles (avoid redundancy)
- Python/CLI stubs deferred (framework is prompt-based)
- Work-specific mappings created on-demand using templates

## [0.2.0] - 2026-01-25 (Pre-release)

### Added
- Anti-Hallucination Protocol v2.0
- Streamlined two-pass verification (down from four)
- CERTAIN/PROBABLE/UNCERTAIN confidence tags
- Graceful degradation for limited source access

### Changed
- Replaced v1.0 over-engineered verification with pragmatic approach
- Reduced verification time from 2+ hours to ~45 minutes per chapter
- Principle shift: "Transparent uncertainty > false certainty"

### Removed
- Mandatory external validation requirement
- Four-pass documentation system
- Unrealistic accuracy thresholds

## [0.1.0] - 2026-01-24 (Pre-release)

### Added
- Original "Return of the King" preschool adaptation framework
- Core pedagogical directives based on developmental psychology
- Character Archetype Translation Matrix
- Thematic Concept Translation Guide
- Chapter-by-chapter directive sets
- Master Translation Table

### Foundation Documents
- Part I: Foundational Adaptation Framework
- Part II: Lexicon of Translation
- Part III: Chapter-by-Chapter Directives
- Appendix: Master Translation Table

---

## Development Notes

### Version Numbering
- **1.x.x**: Stable, production-ready framework
- **0.x.x**: Pre-release development versions
- Breaking changes increment major version
- New features increment minor version
- Bug fixes increment patch version

### Roadmap

#### Planned for 1.1.0
- Tier 4 (Middle School) age profile
- Tier 2 and Tier 4 transformation prompts
- Consistency verification prompt
- Additional work-specific mappings (Narnia, Harry Potter)

#### Planned for 1.2.0
- Interactive learning module integration
- Caregiver discussion guide generator
- Automated vocabulary analysis tools

#### Under Consideration
- Web interface for non-technical users
- API for programmatic access
- Community-contributed work mappings
