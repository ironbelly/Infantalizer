# Adding a New Work

How to build a reusable **work mapping** so LAF can adapt any book — not just the ones that ship with
it. A work mapping is a single YAML file of per-character and per-concept translations that the
transform step loads on top of the universal rules. Two ship today:
[`tolkien_mapping.yaml`](../../config/concept_mapping/templates/tolkien_mapping.yaml) and
[`narnia_mapping.yaml`](../../config/concept_mapping/templates/narnia_mapping.yaml). This guide walks
you through making your own, using *The Lion, the Witch and the Wardrobe* as the running example.

> This is the most valuable contribution you can make to the framework — see
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

> **Automated alternative — `/laf:prep`.** The steps below are the **manual** work-mapping flow.
> LAF also ships a native automated onboarding phase: `/laf:prep "<novel title>" --source <path-or-url>`
> delegates to the `prep-cordinator` agent, which researches the work two-track (context + text),
> runs a source-fidelity-gated work-level analysis, classifies its adaptation challenges, derives the
> confidence-scored work-mapping (including the work-level `meaning:` to preserve), asks only the
> human-judgment questions, and emits the fixed-path `work/prep/<slug>/` package — then, on your
> greenlight, promotes the derived mapping in dual form (the 0.1 6-key copy that keeps `meaning:` and
> the root 5-key copy that strips it). Once prepped, `/laf:rewrite --work <slug>` begins the rewrite.
> Prefer `/laf:prep` for new works; the manual flow below remains useful for understanding, patching,
> or hand-curating a mapping the automated phase produced. The automated phase's path layout and
> promotion contract live in
> [`laf-adaptation/skills/prep/resources/path-contract.md`](../../laf-adaptation/skills/prep/resources/path-contract.md).
>
> **Two HALTs you'll hit (interactive command).** `/laf:prep` HALTs twice for human input: (1) the
> **question gate** after the work-mapping is derived (it asks only the human-judgment questions
> surfaced by the challenge taxonomy — deterministic rules are not asked), and (2) the **greenlight
> confirm** before the dual-form promotion. `/laf:rewrite` requires a **CONFIRMED** greenlight
> (`50-greenlight.md` `status: CONFIRMED`); a `PENDING` (un-greenlit) package is refused — re-run the
> confirm step before invoking `/laf:rewrite`.

## Why a work mapping

The universal rules ([`universal_mappings.yaml`](../../config/concept_mapping/universal_mappings.yaml))
know how to handle *death*, *war*, and *evil* in the abstract. They do **not** know that Jadis should
become "the Snow Queen," that Turkish Delight is the lever of Edmund's betrayal, or that the Stone
Table needs special care. A work mapping supplies that book-specific knowledge once, so every chapter
you adapt stays consistent.

**Cascade (most-specific wins):**
`universal_mappings.yaml` → **your `<work>_mapping.yaml`** → `age_profiles/tier_N` →
`transformation_rules`.

## Step 1: Copy the template

Start from [`templates/work_mapping_template.yaml`](../../templates/work_mapping_template.yaml):

```bash
cp templates/work_mapping_template.yaml \
   config/concept_mapping/templates/narnia_mapping.yaml
```

Name it `lowercase_with_underscores.yaml` (house style —
[CONTRIBUTING.md](../../CONTRIBUTING.md#style-guide)) and place it in
`config/concept_mapping/templates/`.

## Step 2: Fill `work_metadata` and name the challenges

Identify what makes this book *hard* to adapt — the challenges drive everything else.

```yaml
work_metadata:
  title: "The Lion, the Witch and the Wardrobe"
  author: "C.S. Lewis"
  key_challenges:
    - "Sacrificial death AND resurrection (Aslan on the Stone Table)"
    - "Petrification / turning creatures to stone (the White Witch's wand)"
    - "Betrayal of family for temptation (Edmund and the Turkish Delight)"
    - "Pitched battle (Beruna)"
    - "Wartime evacuation frame (the Blitz, children sent away)"
```

A good challenge list reads like a risk register: each item is a place a young tier will need a
deliberate move.

## Step 3: Map the characters

For each major character, give the **Tier 1** archetype (simplify) and what **Tier 3** may restore
(re-complexify). Use the archetypes in
[`character.yaml`](../../config/transformation_rules/character.yaml).

```yaml
characters:
  white_witch:
    tier_1: {name: "The Snow Queen", cause: "Grumpy because it was always cold and never Christmas",
             wand: "A silly wand that makes creatures play statues", omit: ["killing Aslan"]}
    tier_3: {name: "The White Witch (Jadis)", can_show: "True menace, real petrification"}
```

Note the pattern: Tier 1 externalizes agency (*grumpy because…*), neutralizes the nightmare
(petrification → "playing statues"), and **omits** what cannot be reframed. Tier 3 restores it.

## Step 4: Map concepts and key scenes

**Concepts** are the book's recurring nouns (Turkish Delight, the wardrobe, the Stone Table).
**Key scenes** are the set-pieces (Edmund's betrayal, the battle, the thaw). Give each a per-tier
translation:

```yaml
key_scenes:
  stone_table:
    tier_1: {name: "Aslan's Big Rest",
             framing: "Aslan trades a long rest to fix Edmund's mistake, then wakes up warm",
             omit: ["binding", "the knife", "death"]}
    tier_3: {approach: "Aslan gives his life for Edmund; he dies and returns by deeper magic"}
```

## Step 5: Write the master translation table

A flat summary row per headline transformation, each tagged with the **governing principle** from
[UNDERSTANDING_TRANSFORMATIONS.md](UNDERSTANDING_TRANSFORMATIONS.md):

```yaml
master_translation_table:
  - {original: "Aslan's sacrifice and resurrection", tier_1: "A big rest, then waking up",
     principle: "Death → Rest / Emotional Calibration"}
  - {original: "Edmund's betrayal", tier_1: "A silly mistake, then sorry",
     principle: "Betrayal → Accident"}
```

This table is your quick-reference and your fidelity audit in one place.

## Step 6: Validate the YAML

Confirm it parses and matches the shipped schema (same five top-level keys as
`tolkien_mapping.yaml`):

```bash
uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('config/concept_mapping/templates/narnia_mapping.yaml')); print(sorted(d))"
# → ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']
```

## Step 7: Test one chapter at Tier 1

The real test is a chapter, not a schema. Run the full workflow from the
[USER_GUIDE](USER_GUIDE.md#step-1-analyze-the-source) on a single chapter at Tier 1:

1. **Analyze** with [`chapter_analysis.md`](../../prompts/analysis/chapter_analysis.md).
2. **Transform** with [`tier_1_transform.md`](../../prompts/transformation/tier_1_transform.md) +
   your new mapping.
3. **Verify** with [`safety_check.md`](../../prompts/verification/safety_check.md) — it must come back
   **APPROVED** (no forbidden words, all agency external, positive ending).

If safety_check flags something your mapping didn't anticipate, that's a missing row — add it and
re-run. Tier 1 is the strictest gate; passing it is strong evidence the mapping is sound.

## Step 8: Submit (optional)

To contribute the mapping upstream, follow the
[CONTRIBUTING](../../CONTRIBUTING.md#pull-request-process) PR process: feature branch, include your
tested Tier 1 chapter in the PR description, submit.

## A complete example

The Narnia mapping is finished and documented — study it as a model:

- The file: [`config/concept_mapping/templates/narnia_mapping.yaml`](../../config/concept_mapping/templates/narnia_mapping.yaml)
- The guides built on it: [lion-witch-wardrobe/](lion-witch-wardrobe/)
