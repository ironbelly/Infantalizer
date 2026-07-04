# Decision: Adversarial Task List Refinement

## Status
Accepted

## Context

Initial task list had 22+ items. Used adversarial debate to refine.

## Initial List (22 Items)

- 3 remaining age profiles
- 3 transformation rule files
- 3 linguistic config files
- 3 work-specific templates
- 8 prompts
- Python/CLI stubs

## Adversarial Arguments

**Prosecution:**
> "This list is bloated. You're building a cathedral when Ryan needs a bicycle."

1. **Age Profiles 2, 4, 5**: Framework demonstrates principle with 1 and 3. Others are interpolations.
2. **Linguistic Configs**: Already in age profiles. Redundant.
3. **Four Transform Prompts**: Pattern established. Higher tiers need less.
4. **Python/CLI**: Wrong abstraction. This is a prompt framework.

**Defense:**
1. Tier 2 is genuinely distinct (contest paradigm)
2. Character archetypes aren't in thematic.yaml
3. Tier 3 needs its own prompt (different philosophy)

## Final Decision

### Kept (7 Items)

| Task | Rationale |
|------|-----------|
| Tier 2 profile | Distinct paradigm |
| Tier 5 profile | Bookends spectrum |
| Character rules | Not in thematic.yaml |
| Tolkien mapping | Extracts existing work |
| Chapter analysis | v2.0 protocol |
| Safety check | Critical for Tier 1-2 |
| Tier 3 prompt | Transition needs guidance |

### Cut (15 Items)
- Tier 4 (interpolate)
- Linguistic configs (redundant)
- Multiple transform prompts (pattern clear)
- Lewis mapping (premature)
- Python/CLI (wrong abstraction)

## Result

**68% reduction** with minimal quality loss.

## Lessons

1. Adversarial review is valuable
2. Distinguish principle from implementation
3. Redundancy is expensive
4. Right abstraction matters
