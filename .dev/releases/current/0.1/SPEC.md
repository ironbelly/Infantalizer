# Literary Adaptation Framework (LAF) v1.0
## Complete System Specification

---

## Executive Summary

This specification defines a modular, age-configurable system for adapting complex literary works for different developmental audiences. The system extracts the age-invariant transformation logic from the original "Return of the King" preschool framework and parameterizes it across five developmental tiers.

**Core Innovation:** The framework treats developmental psychology as configuration, not code. The same transformation engine applies different rule sets based on the target age profile.

---

## Part I: Architectural Overview

### 1.1 Design Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                    LITERARY ADAPTATION FRAMEWORK                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   SOURCE     │───▶│ TRANSFORM    │───▶│   OUTPUT     │       │
│  │   ANALYSIS   │    │   ENGINE     │    │  GENERATION  │       │
│  └──────────────┘    └──────┬───────┘    └──────────────┘       │
│                             │                                    │
│                      ┌──────▼───────┐                           │
│                      │  AGE PROFILE │                           │
│                      │  SELECTOR    │                           │
│                      └──────┬───────┘                           │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ PRESCHOOL   │    │ ELEMENTARY  │    │   TEEN      │         │
│  │   (3-5)     │    │   (6-11)    │    │  (12-17)    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Principles:**

1. **Configuration over Code:** Age-specific rules live in YAML configs, not hardcoded logic
2. **Composable Modules:** Each transformation type is independent and stackable
3. **Verification Integration:** v2.0 anti-hallucination protocol embedded at source analysis
4. **Graceful Degradation:** System produces useful output even with partial source access
5. **Transparent Confidence:** All output tagged with certainty levels

### 1.2 Module Dependency Graph

```
source_analysis (v2.0 protocol)
       │
       ▼
age_profiles ◄──────────────────────┐
       │                            │
       ├───────────┬────────────────┤
       ▼           ▼                ▼
transformation  character_      concept_
_rules          mapping         mapping
       │           │                │
       └───────────┴────────────────┘
                   │
                   ▼
            linguistic_calibration
                   │
                   ▼
            output_generation
                   │
                   ▼
            verification_check
```

---

## Part II: Age Profile System

### 2.1 Developmental Psychology Foundation

The framework recognizes five distinct developmental tiers, each grounded in established cognitive development theory:

| Tier | Age Range | Piaget Stage | Kohlberg Stage | Key Cognitive Traits |
|------|-----------|--------------|----------------|---------------------|
| 1 | 3-5 | Preoperational | Pre-conventional (1) | Egocentric, concrete, animistic |
| 2 | 6-8 | Early Concrete Operational | Pre-conventional (2) | Declining egocentrism, conservation |
| 3 | 9-11 | Concrete Operational | Conventional (3) | Logical operations, perspective-taking |
| 4 | 12-14 | Early Formal Operational | Conventional (4) | Abstract emergence, hypotheticals |
| 5 | 15-17 | Formal Operational | Post-conventional (5) | Full abstraction, moral complexity |

### 2.2 Tier Comparison Matrix

This matrix shows how key parameters scale across tiers:

```
Parameter                    Tier 1  Tier 2  Tier 3  Tier 4  Tier 5
─────────────────────────────────────────────────────────────────────
Violence Level (0-10)           0       2       4       6       8
Emotional Complexity (0-10)     1       3       5       7       9
Moral Ambiguity (0-10)          0       2       4       7       9
Abstract Concepts (0-10)        0       2       5       8      10
Parallel Plotlines             NO      NO     YES     YES     YES
Character Death               NO    OFFSCREEN IMPLIED SHOWN  SHOWN
Villain True Malice           NO      NO    PARTIAL  YES     YES
Hero Failure Permitted        NO      NO     YES     YES     YES
Max Sentence Words            12      15      20      25      30+
Max Named Characters           8      12      20      30      50+
Agency Externalization     MAND.   MAND.   OPT.    OPT.   FORB.
```

### 2.3 Age Profile Schema

Each age profile is defined by a YAML configuration with:

- `profile`: Identification and metadata
- `developmental_basis`: Piaget/Kohlberg stage information
- `thresholds`: Violence, emotional, moral, abstract concept limits
- `linguistic`: Vocabulary, sentence structure, chapter length rules
- `transformation_rules`: Mode settings for each transformation type
- `safety`: Age-specific safety requirements

See `config/age_profiles/` for complete profile definitions.

---

## Part III: Transformation Rules Engine

### 3.1 Rule Categories

The transformation engine applies rules in five categories:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSFORMATION CATEGORIES                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. STRUCTURAL          2. THEMATIC           3. CHARACTER       │
│  ─────────────          ─────────────         ─────────────      │
│  • Linearization        • Violence→X          • Archetype map    │
│  • Consolidation        • Death→Y             • Motivation       │
│  • Pacing              • Conflict→Z          • Complexity        │
│                                                                  │
│  4. EMOTIONAL           5. LINGUISTIC                            │
│  ─────────────          ─────────────                            │
│  • Calibration          • Vocabulary                             │
│  • Resolution           • Sentence structure                     │
│  • Safety rails         • Chapter length                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Key Transformation Rules

#### Agency Externalization

The foundational rule for Tiers 1-2:

> Negative outcomes are NEVER attributed to internal malice or moral failing.
> "Badness" is always a STATE (grumpy, tired, sad, messy) or an ACCIDENT.
> Never an innate quality of a character.

**Mode by Tier:**
- Tier 1-2: MANDATORY
- Tier 3: OPTIONAL
- Tier 4-5: FORBIDDEN (patronizing)

#### Violence Transformation

| Tier | Battle → | Attack → | Death → |
|------|----------|----------|---------|
| 1 | Big Tidy-Up | Bumping/chasing | New adventure |
| 2 | Contest | Chase/struggle | Passed away |
| 3 | Battle (summarized) | Fought | Died |
| 4-5 | [Preserve] | [Preserve] | [Preserve] |

#### Heroism Translation

| Tier | Heroism Mode |
|------|--------------|
| 1 | Prosocial only (helping, sharing, comforting) |
| 2 | Prosocial + fair competition |
| 3 | Includes defense and sacrifice |
| 4-5 | Full spectrum including tragic |

---

## Part IV: Source Analysis Integration

### 4.1 v2.0 Protocol Integration

The source analysis module implements the Pragmatic Verification Protocol v2.0:

**Phase 0: Source Declaration**
- Access level: FULL / PARTIAL / MEMORY-BASED / NO ACCESS
- Confidence basis: Direct quotes / Paraphrase / Reconstruction

**Phase 1: Essential Verification**
- Core identifiers (title, author, chapter count)
- Opening/closing sentences
- 25% calculation for coverage

**Phase 2: Dual-Pass Documentation**
- Pass 1: Structure and events combined
- Pass 2: Validation and summary with confidence tags

**Phase 3: Consistency Validation**
- Binary checks (characters, timeline, locations)
- Optional external check

**Phase 4: Accuracy Verification**
- Single spot check per chapter
- Liberal use of UNCERTAIN tags

### 4.2 Confidence Tag Definitions

| Tag | Definition | Use When |
|-----|------------|----------|
| **CERTAIN** | Directly quoted/counted from text | Verbatim quotes, counted occurrences |
| **PROBABLE** | Consistent with multiple observations | Strong textual support |
| **UNCERTAIN** | Inferred, reconstructed, or from memory | Anything not directly verified |

---

## Part V: Output Generation

### 5.1 Generation Pipeline

```
Chapter Analysis Object
         │
         ▼
Transformation Rule Engine ◄── Age Profile Config
         │
         ▼
Draft Generation (applies linguistic rules)
         │
         ▼
Verification Check
         │
         ▼
Final Output with Confidence Tags
```

### 5.2 Output Format

Each adapted chapter includes:
- Adapted content
- Transformation log (what changed and why)
- Confidence report
- Verification results

---

## Part VI: Project Structure

```
literary-adaptation-framework/
├── config/
│   ├── age_profiles/           # Tier configurations
│   ├── transformation_rules/   # Rule definitions
│   ├── concept_mapping/        # Translation tables
│   └── linguistic/             # Language rules
├── prompts/
│   ├── analysis/               # Source analysis
│   ├── transformation/         # Generation prompts
│   └── verification/           # Safety checks
├── docs/                       # Documentation
├── templates/                  # Blank templates
├── examples/                   # Completed work
└── tests/                      # Validation
```

---

## Part VII: Quick Reference

### Tier Decision Matrix

```
QUESTION                          T1   T2   T3   T4   T5
────────────────────────────────────────────────────────
Can character die on page?        NO   NO  IMPL YES  YES
Can villain be truly evil?        NO   NO  PART YES  YES
Can hero fail morally?            NO   NO  YES  YES  YES
Can story end sadly?              NO   NO  BSWE YES  YES
Can conflict be violent?          NO  MILD YES  YES  YES
Must agency be externalized?     YES  YES  OPT  NO   NO
Parallel plotlines OK?            NO   NO  YES  YES  YES
Abstract concepts OK?             NO  SOME YES  YES  YES

Legend: IMPL=Implied, PART=Partial, BSWE=Bittersweet, OPT=Optional
```

### Transformation Quick Reference (Tier 1)

```
SOURCE ELEMENT          TIER 1 TRANSFORM
─────────────────────────────────────────
Battle                → Cleanup/Tidy-up
Death                 → New adventure/Rest
Evil                  → Grumpy/Sad state
Wound                 → Boo-boo
Enemy                 → Grumpy helper
War                   → Big project
Betrayal              → Accident/Game
Despair               → Very sad (fixable)
Monster               → Noisy creature
Curse                 → Very sleepy
```

---

*End of Specification Document*
