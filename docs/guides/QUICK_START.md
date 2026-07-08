# Quick Start Guide

Get started in 5 minutes.

## Step 1: Choose Tier

| Tier | Ages | Use Case |
|------|------|----------|
| 1 | 3-5 | Bedtime stories. Maximum safety. |
| 2 | 6-8 | Early readers. Mild tension OK. |
| 3 | 9-11 | Chapter books. Complexity OK. |
| 4 | 12-14 | Middle grade. Near-adult. |
| 5 | 15-17 | YA. Preserve original. |

## Step 2: Load Configuration

```bash
# Age profile
cat config/age_profiles/tier_1_preschool.yaml

# Transformation rules
cat config/transformation_rules/thematic.yaml

# Work mappings (if available)
cat config/concept_mapping/templates/tolkien_mapping.yaml
```

## Step 3: Analyze Source

Use `prompts/analysis/chapter_analysis.md`

1. Declare source access
2. Document structure and events
3. Flag transformation needs
4. Tag confidence levels

## Step 4: Transform

Use tier-appropriate prompt:
- `prompts/transformation/tier_1_transform.md`
- `prompts/transformation/tier_3_transform.md`

## Step 5: Verify (Tier 1-2)

Use `prompts/verification/safety_check.md`

## Example

**Source:** "The orcs attacked. Many soldiers fell."

**Tier 1:** "The noisy grumbles made a big mess. Many helpers got very tired."

## Tips

### Tier 1
- Everything is fixable
- No one is evil (just grumpy)
- Always end happy

### Tier 3
- Complexity unlocked
- Death can be named
- Show consequences

### Tier 5
- Preserve, don't sanitize
- Trust the reader
