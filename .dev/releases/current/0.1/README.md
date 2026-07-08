# Literary Adaptation Framework (LAF)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modular, configuration-driven system for adapting complex literary works for different developmental audiences, from preschool (ages 3-5) through young adult (ages 15-17).

## Overview

The Literary Adaptation Framework provides a systematic approach to transforming mature literary content into age-appropriate versions while preserving narrative integrity and emotional journey. Built on established developmental psychology (Piaget's cognitive stages, Kohlberg's moral reasoning), the framework treats age-appropriateness as **configuration, not code**.

### Key Features

- **Five-Tier System**: Covers ages 3-17 with developmentally-grounded profiles
- **Configuration-Driven**: Age profiles and transformation rules in YAML
- **Anti-Hallucination Protocol**: v2.0 verification system for source fidelity
- **Work-Agnostic Core**: Universal mappings work across any literary source
- **Claude Code Ready**: Designed for AI-assisted adaptation workflows

## Quick Start

```bash
# 1. Choose your target tier
#    Tier 1 (3-5): Full transformation, maximum safety
#    Tier 2 (6-8): Contest/competition framing
#    Tier 3 (9-11): Moral complexity unlocked
#    Tier 4 (12-14): Near-adult treatment
#    Tier 5 (15-17): Minimal transformation

# 2. Load the age profile
cat config/age_profiles/tier_1_preschool.yaml

# 3. Load transformation rules
cat config/transformation_rules/thematic.yaml

# 4. Load work-specific mappings (if available)
cat config/concept_mapping/templates/tolkien_mapping.yaml

# 5. Run analysis prompt on source chapter
# 6. Run transformation prompt
# 7. Run safety verification (Tier 1-2)
```

## The Five-Tier System

| Tier | Ages | Piaget Stage | Key Characteristics |
|------|------|--------------|---------------------|
| 1 | 3-5 | Preoperational | Full transformation. Violence → cleanup. Death → "adventure". Villains are grumpy. |
| 2 | 6-8 | Early Concrete | Violence → contests. Death → "passed away". Villains misunderstand. |
| **3** | **9-11** | **Concrete** | **TRANSITION TIER.** Moral ambiguity OK. "Died" acceptable. Complexity unlocked. |
| 4 | 12-14 | Early Formal | Near-adult. Tragedy permitted. Full villain complexity. |
| 5 | 15-17 | Formal | Minimal transformation. Preserve author intent. Accessibility focus. |

## Core Concepts

### Agency Externalization (Tiers 1-2)

The most important transformation rule for young children. Negative outcomes are **never** attributed to internal malice:

```
❌ "Sauron was evil"
✅ "The Grumpy King was grumpy because his land had no sunshine"

❌ "Gollum attacked out of greed"  
✅ "The silly creature wanted to play a game with the shiny ring"
```

**Why?** Children ages 3-8 are still developing perspective-taking. They may internalize character flaws as self-blame.

### The Tier 3 Inflection Point

Tier 3 (ages 9-11) is where major developmental shifts occur:

- ✅ Moral ambiguity now permitted (`requires_clear_good_bad: false`)
- ✅ "Died" is acceptable language
- ✅ Villains can have internal motivation
- ✅ Heroes can fail morally
- ✅ Parallel plotlines and flashbacks allowed

This maps to concrete operational stage where children can handle perspective-taking and moral complexity.

### Anti-Hallucination Protocol (v2.0)

All source analysis uses confidence tagging:

| Tag | Definition | Use When |
|-----|------------|----------|
| **CERTAIN** | Directly quoted from text | Verbatim quotes |
| **PROBABLE** | Consistent with multiple observations | Strong support |
| **UNCERTAIN** | Inferred or reconstructed | Not directly verified |

**Core principle:** *Transparent uncertainty is better than false certainty.*

## Repository Structure

```
literary-adaptation-framework/
├── config/
│   ├── age_profiles/           # Tier-specific developmental configs
│   ├── transformation_rules/   # Thematic, character, emotional rules
│   ├── concept_mapping/        # Universal + work-specific translations
│   └── linguistic/             # Vocabulary and structure rules
├── docs/
│   ├── design_decisions/       # Architecture and design rationale
│   ├── conversation_logs/      # Development discussion records
│   └── guides/                 # How-to documentation
├── prompts/
│   ├── analysis/               # Source analysis prompts
│   ├── transformation/         # Tier-specific generation prompts
│   └── verification/           # Safety and consistency checks
├── templates/                  # Blank templates for new works
├── examples/                   # Completed adaptations
└── tests/                      # Validation tests
```

## Documentation

- [**SPEC.md**](docs/SPEC.md) - Complete system specification (1,200+ lines)
- [**Design Decisions**](docs/design_decisions/) - Why the framework works this way
- [**Quick Start Guide**](docs/guides/QUICK_START.md) - Get started in 5 minutes
- [**Adding New Works**](docs/guides/ADDING_NEW_WORKS.md) - Create work-specific mappings

## Development History

This framework evolved from a specific adaptation of Tolkien's "The Return of the King" for preschool audiences into a generalized, modular system. Key development phases:

1. **Proof of Concept**: "The Happiness Project" - full ROTK → preschool adaptation
2. **Anti-Hallucination Protocol**: v1.0 (over-engineered) → v2.0 (pragmatic)
3. **Modularization**: Extract age-invariant logic, parameterize by tier
4. **Claude Code Integration**: Configuration-driven for AI workflow

See [CHANGELOG.md](CHANGELOG.md) and [docs/conversation_logs/](docs/conversation_logs/) for full history.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-work-mapping`)
3. Add your changes with appropriate tests
4. Submit a pull request

For new work mappings, use `templates/work_mapping_template.yaml` as starting point.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Developmental psychology foundations: Piaget, Vygotsky, Kohlberg
- Original adaptation framework: "The Return of the King" preschool project
- Anti-hallucination methodology: Pragmatic Verification Protocol v2.0
