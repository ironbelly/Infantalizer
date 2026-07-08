# Literary Adaptation Framework (LAF)

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
| 1 | 3-5 | Preoperational | Full transformation. Violence → cleanup. Death → "adventure". |
| 2 | 6-8 | Early Concrete | Violence → contests. Death → "passed away". Villains misunderstand. |
| **3** | **9-11** | **Concrete** | **TRANSITION TIER.** Moral ambiguity OK. "Died" acceptable. |
| 4 | 12-14 | Early Formal | Near-adult. Tragedy permitted. Full villain complexity. |
| 5 | 15-17 | Formal | Minimal transformation. Preserve author intent. |

## Core Concepts

### Agency Externalization (Tiers 1-2)

Negative outcomes are **never** attributed to internal malice:

```
❌ "Sauron was evil"
✅ "The Grumpy King was grumpy because his land had no sunshine"
```

### Anti-Hallucination Protocol (v2.0)

All source analysis uses confidence tagging:

| Tag | Definition |
|-----|------------|
| **CERTAIN** | Directly quoted from text |
| **PROBABLE** | Consistent with multiple observations |
| **UNCERTAIN** | Inferred or reconstructed |

## Repository Structure

```
literary-adaptation-framework/
├── config/
│   ├── age_profiles/           # Tier-specific developmental configs
│   ├── transformation_rules/   # Thematic, character rules
│   └── concept_mapping/        # Universal + work-specific translations
├── docs/
│   ├── design_decisions/       # Architecture rationale
│   ├── conversation_logs/      # Development discussion records
│   └── guides/                 # How-to documentation
├── prompts/
│   ├── analysis/               # Source analysis prompts
│   ├── transformation/         # Tier-specific generation prompts
│   └── verification/           # Safety checks
└── templates/                  # Blank templates for new works
```

## Documentation

- [**SPEC.md**](docs/SPEC.md) - Complete system specification
- [**Quick Start Guide**](docs/guides/QUICK_START.md) - Get started in 5 minutes
- [**Design Decisions**](docs/design_decisions/) - Why the framework works this way

## License

MIT License - see [LICENSE](LICENSE) for details.
