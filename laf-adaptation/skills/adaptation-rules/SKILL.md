---
name: adaptation-rules
description: |
  Thematic and character transformation rules for literary adaptation, keyed by tier. Covers violence,
  conflict, death, villain motivation, heroism, and character-archetype mapping. Includes Agency
  Externalization (the signature rule). Load when writing or critiquing an adaptation draft.
---

# Adaptation Rules

Transform source content to the active tier using these rules. Every rule is keyed by tier and carries a
`mode:` value. Read the active tier's row; apply MANDATORY rules, honor OPTIONAL ones per editorial
judgment, and never apply FORBIDDEN ones.

Resources:
- `resources/thematic.md`  — violence, conflict, death, villain, heroism (carried from thematic.yaml)
- `resources/character.md` — archetype mapping + heroism-translation subroutine (carried from character.yaml)
- `resources/agency.md`    — Agency Externalization, the signature rule (§2.3)

## Applying a rule
1. Identify the source element's category (violence | conflict | death | villain | heroism | character).
2. Look up `<category>.tier_<N>.mode`.
3. Apply the tier's `translations`/`target`/`strategy` for that category.
4. For characters, run the heroism-translation subroutine (§character): IDENTIFY intent → LOOKUP
   tier-appropriate expression → TRANSLATE action preserving intent.

**Schema-tolerant step 2 (operational reading, mirrors the Key-tolerant lookup note below).** Not every
category carries a `mode:` key — the carried-verbatim payloads deliberately differ. When resolving step 2:
read `<category>.tier_<N>.mode` **if the key is present**; **otherwise the category's tier row IS the rule
payload** — apply its `target` / `strategy` / `translations` directly (there is no separate mode to gate
on; a payload with no `mode:` is applied unconditionally as MANDATORY for that tier). Categories that carry
an explicit `mode:` enum: **conflict, agency, villain, heroism**. Categories that present a **direct
payload** (no `mode:` — apply the row directly): **violence, and death at tiers 1–3** (T5 death/conflict
use the drift-keyed `*_handling` payload resolved via the Key-tolerant lookup below). Do NOT add a `mode:`
key to a payload that lacks one to "normalize" it — that would break the byte-faithful carry.

## Key-tolerant lookup (schema drift is deliberate)
The carried-verbatim tier profiles and rule groups contain **intentional schema drift** and are NEVER
normalized in the vendored/ported files. Tiers 1-3 use `conflict_to_cooperation` / `death_euphemism`,
while Tier 5 uses `conflict_handling` / `death_handling` (per `kb-formats.md §2.2`). Absorb this drift
**here, in the reader**, not in the data: when resolving a conflict- or death-category rule, look the key
up tolerantly — e.g. `profile.get("conflict_to_cooperation") or profile.get("conflict_handling")` and
`profile.get("death_euphemism") or profile.get("death_handling")`. Do NOT rename a key in `kb/tiers/*.yaml`
or in `resources/thematic.md` to "fix" the drift — that would break the byte-faithful carry.

## Cascade with work mappings
Work-specific overrides in `kb/adaptation-mapping/<work>-mapping.yaml` take precedence over these
universal rules (most-specific-wins). See `/source-fidelity` and kb-formats for the cascade order.
