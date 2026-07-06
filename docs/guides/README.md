# LAF User Guides

Practical, task-oriented guides for **using** the Literary Adaptation Framework to turn a complex
book into an age-appropriate version. These guides cover the **root v1.0 layer** — the
prompt + YAML workflow in `config/`, `prompts/`, and `templates/`. No code required; you drive the
framework by loading configs and prompts into an LLM.

> New to LAF? For the big picture read the top-level [README](../../README.md); for the canonical
> specification read [SPEC.md](../SPEC.md). These guides are the *how-to* layer on top of both.

## Start here

1. **[QUICK_START.md](QUICK_START.md)** — the 5-step workflow at a glance (2 minutes).
2. **[USER_GUIDE.md](USER_GUIDE.md)** — the full walkthrough: analyze → transform → verify, and how
   to read what comes out. Read this once end to end.
3. **[CHOOSING_A_TIER.md](CHOOSING_A_TIER.md)** — pick the right tier for your child, class, or
   purpose before you adapt anything.

## Understand the method

4. **[UNDERSTANDING_TRANSFORMATIONS.md](UNDERSTANDING_TRANSFORMATIONS.md)** — the *why* behind the
   rules: agency externalization, violence → cooperation, death → journey, heroism translation, and
   the CERTAIN / PROBABLE / UNCERTAIN confidence tags.

## Adapt your own book

5. **[ADDING_NEW_WORKS.md](ADDING_NEW_WORKS.md)** — build a reusable *work mapping* for any book,
   from the blank template to a tested Tier 1 chapter.

## Worked example — *The Lion, the Witch and the Wardrobe*

6. **[lion-witch-wardrobe/](lion-witch-wardrobe/)** — a complete example set: how to rewrite C.S.
   Lewis's *The Lion, the Witch and the Wardrobe* across tiers, backed by the loadable
   [`narnia_mapping.yaml`](../../config/concept_mapping/templates/narnia_mapping.yaml).

## The five tiers at a glance

| Tier | Ages | Use case | Headline rule |
|------|------|----------|---------------|
| 1 | 3–5 | Bedtime stories, maximum safety | Violence → cleanup, death → "new adventure" |
| 2 | 6–8 | Early readers, mild tension OK | Violence → contest, death → "passed away" |
| **3** | **9–11** | **Chapter books — the transition tier** | "Died" acceptable, moral ambiguity OK |
| 4 | 12–14 | Middle grade, near-adult | Tragedy permitted (interpolated tier) |
| 5 | 15–17 | Young adult — preserve the original | Accessibility, not sanitization |

See [CHOOSING_A_TIER.md](CHOOSING_A_TIER.md) for how to decide, and
[SPEC.md](../SPEC.md) for the full tier-comparison matrix.
