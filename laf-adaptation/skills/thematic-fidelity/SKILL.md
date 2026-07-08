---
name: thematic-fidelity
description: |
  The meaning-preservation invariant for adaptation: a work's meaning (allegory, theme, moral center) is
  preserved under surface transformation — neither added where the source withholds it nor stripped where the
  source asserts it. Defines the analyst `meaning` field, the tier-coordinator Check D, and the DERIVED-marking
  rule for method exemplars. Load whenever authoring or reconciling tier renderings.
---

# Thematic Fidelity

Principle (Hutcheon / Bortolotti): **meaning is preserved under surface transformation; the environment is
the target tier.** Source-fidelity guards the FACTS; thematic-fidelity guards the MEANING. A faithful
adaptation transforms the surface (names, violence, vocabulary) while carrying the same meaning at the tier's
altitude — and neither invents an allegory the source lacks nor deletes one it has.

## The `meaning` field (analyst output)

Every analyzed unit (work / chapter / scene) emits:

```
meaning: {value: "<the theme/allegory beneath the surface>", confidence: CERTAIN|PROBABLE|UNCERTAIN}
```

Tagged like any source fact. At work level it is the top-level `meaning:` promoted with the mapping; the
rewrite-phase `muse` reads it as data — no adopted-body edit.

## Check D (tier-coordinator, rewrite phase)

For each element shared across tiers, assert every tier's rendering preserves the work-level meaning:
status `Meaning-PRESERVED | Meaning-DIFF`. A `Meaning-DIFF` is a conflict that blocks `chronicler` (rides the
existing `RECONCILED | CONFLICT` gate — no new control flow). Agency Externalization is meaning-preserving
("external cause, not innate evil"); silently dropping or inventing an allegory is `Meaning-DIFF`.

## Exemplar DERIVED-marking rule (contamination safety)

Method-illustration exemplars are NOT source truth. Every exemplar file MUST open with the structural marker:

```
<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->
```

and MUST live OUTSIDE the source-truth path (`work/`, `kb/canon/`). This prevents a downstream agent from
presenting an exemplar as verified source (closes the contamination risk).

## Relationship to source-fidelity

- **source-fidelity:** is this FACT true to the text? (`CERTAIN` / `PROBABLE` / `UNCERTAIN`)
- **thematic-fidelity:** is this MEANING preserved under the transform? (`Meaning-PRESERVED` / `Meaning-DIFF`)

Both are required; neither substitutes for the other.

## Boundary note

`thematic-fidelity` is a **standalone NATIVE skill**, not an edit to an adopted skill — bolting
meaning-preservation onto an adopted skill would break the boundary contract. It is loaded by the (native)
`prep-cordinator` and read as data by the (build-new) `tier-coordinator`.
