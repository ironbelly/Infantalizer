# Agency Externalization — the signature adaptation rule (ADR-003)

Agency Externalization is the most important transformation rule for Tiers 1-2: **negative outcomes are
never attributed to internal malice — "badness" is always a temporary STATE (grumpy, tired) or an
ACCIDENT, never an innate quality.** The rule payload below is carried VERBATIM from
`config/transformation_rules/thematic.yaml`'s `agency_externalization` section (byte-identical; only this
prose wrapper is added).

```yaml
agency_externalization:
  core_principle: "Badness is always a STATE or ACCIDENT, never innate."
  tier_1:
    mode: "mandatory"
    examples:
      - {source: "Dark Lord, evil", target: "Grumpy King, no sunshine"}
      - {source: "driven mad by despair", target: "very sad, windows closed"}
      - {source: "consumed by greed", target: "really wanted to play"}
  tier_2:
    mode: "mandatory"
    softening: "permits_misunderstanding_as_cause"
  tier_3:
    mode: "optional"
  tier_4_5:
    mode: "forbidden"
```

## Why this lives in the native `/adaptation-rules` skill (not adopted `writing-principles`)

Per `skill-specs.md §2.3`: bolting Agency Externalization onto an adopted skill (e.g.
`writing-principles`) would edit an adopted body and **break the boundary contract** — adopted files must
stay patch-clean and upstream-syncable. So the rule rides here, in the native `/adaptation-rules`, and is
**loaded additively** by the adopted `writer` and `critic` via their `skills:` frontmatter (constraint
#6: native knowledge enters adopted agents only as a loadable skill, never a body edit).

## How it is enforced

- **`writer`** applies the rule when drafting an adaptation (loads `/adaptation-rules`, reads the active
  tier's `mode:`, and externalizes agency when the mode is `mandatory`/`optional`).
- **`safety-verifier`** audits it — **Section 2** of the safety rubric checks Agency Externalization for
  T1-2 drafts and can FAIL the draft (blocking kb promotion, re-entering the writer revision loop).
- **`critic`** audits it from the adaptation-quality angle.

## The developmental rationale (ADR-003)

Children ages 3-8 are egocentric (Piaget). Faced with a "bad" character they may fail to understand
motivation, feel the raw emotional impact, and **internalize "badness" as applying to themselves**.
Externalizing to a temporary state gives the child a simple cause ("grumpy because dark"), a concrete
solution ("let the sunshine in"), and no character who is inherently bad to internalize — e.g. *"Sauron
was evil"* → *"Grumpy King, no sunshine."* The ladder scales the rule back (MANDATORY T1-2 → OPTIONAL T3
→ FORBIDDEN T4-5): once full perspective-taking develops around age 9-11, externalization becomes
**patronizing** and, at T4-5, would undermine the character complexity those readers can handle.
