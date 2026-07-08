# Conversation Log: Modularization Planning

**Date:** January 25, 2026  
**Topic:** Porting Framework to Claude Code

## Context

Two artifacts existed:
1. AI Adaptation Primer (ROTK preschool)
2. Refactored Implementation Guide v2.0

Goal: Modular system for any work, any age.

## Key Discussion Points

### 1. Decomposing Original Framework

Implicit layers made explicit:
1. Developmental Psychology Layer
2. Transformation Rules Layer
3. Domain Knowledge Layer
4. Linguistic Calibration Layer
5. Source Analysis Layer
6. Output Generation Layer

### 2. Configuration vs Code

**Decision:** Developmental psychology as configuration.
- Same engine, different rule sets
- YAML readable by non-programmers
- Easy to add tiers

### 3. Five-Tier System

| Tier | Age | Key Paradigm |
|------|-----|--------------|
| 1 | 3-5 | Full transformation |
| 2 | 6-8 | Contest/competition |
| 3 | 9-11 | **Transition** - complexity unlocks |
| 4 | 12-14 | Near-adult |
| 5 | 15-17 | Minimal transformation |

**Critical insight:** Tier 3 is inflection point.

## Decisions Made

1. Configuration-driven architecture
2. Five tiers based on Piaget/Kohlberg
3. Agency Externalization as foundational rule
4. v2.0 protocol integrated at source analysis
5. Prompt framework, not Python package

## Key Quotes

> "The framework assumes preschool, but the structure of the rules is age-agnostic."

> "Transparent uncertainty is better than false certainty."

> "Tier 3 is where major unlocks occur."
