# Literary Adaptation Framework (LAF) v1.0
## Complete System Specification

## Executive Summary

A modular, age-configurable system for adapting complex literary works. Treats developmental psychology as configuration, not code.

## Part I: Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LITERARY ADAPTATION FRAMEWORK                 │
├─────────────────────────────────────────────────────────────────┤
│  SOURCE ANALYSIS ──▶ TRANSFORM ENGINE ──▶ OUTPUT GENERATION     │
│                            │                                     │
│                      AGE PROFILE                                 │
│                      SELECTOR                                    │
│         ┌──────────────────┼──────────────────┐                 │
│         ▼                  ▼                  ▼                 │
│    PRESCHOOL         ELEMENTARY            TEEN                 │
│      (3-5)             (6-11)             (12-17)               │
└─────────────────────────────────────────────────────────────────┘
```

**Key Principles:**
1. Configuration over code
2. Composable modules
3. Transparent confidence
4. Graceful degradation

## Part II: Five-Tier System

| Tier | Age | Piaget Stage | Key Traits |
|------|-----|--------------|------------|
| 1 | 3-5 | Preoperational | Egocentric, concrete, animistic |
| 2 | 6-8 | Early Concrete | Declining egocentrism, conservation |
| 3 | 9-11 | Concrete | Perspective-taking, moral complexity |
| 4 | 12-14 | Early Formal | Abstract emergence |
| 5 | 15-17 | Formal | Full abstraction |

### Tier Comparison Matrix

```
Parameter                    T1   T2   T3   T4   T5
─────────────────────────────────────────────────────
Violence Level (0-10)         0    2    4    6    8
Moral Ambiguity (0-10)        0    2    4    7    9
Parallel Plotlines           NO   NO  YES  YES  YES
Character Death              NO  OFF  IMP  YES  YES
Villain True Malice          NO   NO PART  YES  YES
Hero Failure Permitted       NO   NO  YES  YES  YES
Agency Externalization     MAND MAND  OPT  OPT FORB
```

## Part III: Core Rules

### Agency Externalization

**The foundational rule for Tiers 1-2:**

> Badness is always a STATE (grumpy, tired) or ACCIDENT.
> Never an innate quality.

| Tier | Mode |
|------|------|
| 1-2 | MANDATORY |
| 3 | OPTIONAL |
| 4-5 | FORBIDDEN |

### Violence Transformation

| Tier | Battle → | Death → |
|------|----------|---------|
| 1 | Big Tidy-Up | New adventure |
| 2 | Contest | Passed away |
| 3 | Battle (summarized) | Died |
| 4-5 | [Preserve] | [Preserve] |

### Heroism Translation

| Tier | Mode |
|------|------|
| 1 | Prosocial only |
| 2 | + Competition |
| 3 | + Defense |
| 4-5 | Full spectrum |

## Part IV: v2.0 Protocol

**Phase 0:** Source declaration
**Phase 1:** Essential verification
**Phase 2:** Two-pass documentation
**Phase 3:** Consistency validation

### Confidence Tags

| Tag | Definition |
|-----|------------|
| CERTAIN | Directly quoted |
| PROBABLE | Multiple observations |
| UNCERTAIN | Inferred |

**Principle:** Transparent uncertainty > false certainty

## Part V: Quick Reference

### Transformation Table (Tier 1)

```
SOURCE              TIER 1 TRANSFORM
──────────────────────────────────────
Battle            → Cleanup/Tidy-up
Death             → New adventure/Rest
Evil              → Grumpy/Sad state
Wound             → Boo-boo
Enemy             → Grumpy helper
War               → Big project
Betrayal          → Accident/Game
Monster           → Noisy creature
```

### Tier Decision Matrix

```
QUESTION                          T1   T2   T3   T4   T5
────────────────────────────────────────────────────────
Can character die on page?        NO   NO  IMP  YES  YES
Can villain be truly evil?        NO   NO PART  YES  YES
Can hero fail morally?            NO   NO  YES  YES  YES
Must agency be externalized?     YES  YES  OPT   NO   NO
```
