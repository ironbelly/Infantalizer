# Design Decisions

Key architectural decisions for the Literary Adaptation Framework.

## Index

1. [001-five-tier-system.md](001-five-tier-system.md) - Why five tiers
2. [003-agency-externalization.md](003-agency-externalization.md) - The key preschool rule
3. [006-adversarial-task-review.md](006-adversarial-task-review.md) - Task list refinement

## Key Principles

### 1. Configuration over Code
Age rules in YAML, not hardcoded logic.

### 2. Composable Modules
Each transformation type independent.

### 3. Transparent Uncertainty
CERTAIN/PROBABLE/UNCERTAIN tags.

### 4. Graceful Degradation
Useful output with partial source access.
