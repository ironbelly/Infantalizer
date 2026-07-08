# Proposal B — Analyzer voice ("ground every change in a named gap")

> Persona: analyzer. Lens: every proposed change must trace to a named gap in
> `10-findings-and-evaluation.md` or a named step in the user story, with a cited framework path. This
> proposal is the **evidence-first** counterweight to A's structural minimalism and C's radical
> consolidation. It adds a **traceability matrix** as a first-class deliverable and is the most aggressive
> about the **anti-hallucination topology**.

## B.1 Headline

Proposal A is structurally sound but **under-specifies provenance discipline** and **leaves the work-level
analysis ambiguous** (A.13 Q2). Proposal B's differences from A:

1. The prep package includes a **traceability matrix** (`70-traceability.md`) mapping every package
   artifact + every mapping entry to (a) the gap it closes and (b) the confidence-tagged fact it derives
   from. This is the *enforcement* of the contamination fix — not just marking exemplars DERIVED, but
   proving the *whole package's* provenance.
2. Work-level analysis is **two-track, not one**: a `web-researcher`-sourced **context track**
   (secondary sources, MEMORY-BASED ceiling) AND a `source-fidelity`-sourced **text track** that requires
   the user to point at the source text (or a representative excerpt). The mapping is only as confident
   as its weakest track. A's "allow MEMORY-BASED, propagate the ceiling" is correct but incomplete — B
   makes the **two tracks explicit and separately tagged** so the rewrite phase knows which mapping
   entries are text-grounded vs context-grounded.
3. The **question gate is constrained by a coverage rule**, not free-form: the gate MUST ask about any
   challenge type that the taxonomy flagged but where the governing rule has a known human-judgment
   dimension (allegory stance, omission honor set, target-age nuance). This prevents the gate from either
   over-asking (annoying) or under-asking (missing the meaning-preservation decision).

## B.2 Traceability matrix — the deliverable A omits

`work/prep/<work-slug>/70-traceability.md`:

```yaml
artifacts:
  30-mapping.yaml:
    derived_from: [20-analysis-work-level.yaml, 10-challenges.yaml]
    confidence_ceiling: PROBABLE   # lowest tag across inputs
  40-prep-brief.md:
    derived_from: [00-work-context.md, 30-mapping.yaml]
    kind: SYNTHESIS                # human-readable; never source truth
mapping_entries:
  - entry: "characters[Jadis].tier_1_archetype"
    value: "the Snow Queen"
    derived_from_fact: "20-analysis: characters[Jadis].role = antagonist (CERTAIN)"
    gap_closed: "Q1-row3 per-work decisions"
    confidence: PROBABLE
  - entry: "challenge[sacrificial_death].governing_rule"
    value: "death_handling + compound-scene protocol"
    derived_from_fact: "10-challenges: compound_scene=true on Stone Table"
    gap_closed: "gap#2 compound-scene protocol"
    confidence: CERTAIN
gaps_addressed:
  - gap: "thematic/meaning-preservation"
    closed_by: "thematic-fidelity skill + tier-coordinator Check D + analyst meaning field"
    evidence: "30-mapping: meaning per scene; 40-prep-brief: meaning-preservation stance"
```

**Why this matters (the analyzer's core argument):** the Q2 contamination risk is not just about
exemplars — it is about *any* derived content. A marks exemplars DERIVED but leaves the prep-brief and
the mapping's prose unmarked. The traceability matrix is what lets the rewrite phase **mechanically
distinguish** "this is text-grounded source truth" from "this is a derived decision." Without it, the
prep package is just a better-organized version of the same contamination risk.

## B.3 Two-track work-level analysis

```
00-work-context.md       ← web-researcher track (secondary sources; MEMORY-BASED or PARTIAL ceiling)
20-analysis-work-level.yaml  ← source-fidelity track (the novel text; FULL/PARTIAL/MEMORY ceiling)
                           BOTH feed 30-mapping; each mapping entry carries BOTH a text_confidence
                           and a context_confidence; the entry's confidence = min(text, context)
```

This resolves A.13 Q2 definitively: **the prep phase does NOT require the source text, but it REQUIRES
the user to declare source access**, and the mapping's per-entry confidence reflects whether that entry
is text-grounded, context-grounded, or both. A user who supplies only the title gets a
context-grounded-only mapping (every entry ceiling PROBABLE-or-worse); a user who points at the text
gets text-grounded entries (CE RTAIN possible). This is more honest than A's single ceiling.

## B.4 Coverage-constrained question gate

The `prep-protocol` skill encodes a **gate-coverage rule** (the spec-kit clarify-coverage pattern,
enrichment §1, made rigorous):

```
GATE COVERAGE:
  FOR each challenge in 10-challenges.yaml:
    IF challenge.governing_rule has a human_judgment_dimension (allegory, omission, target-age):
      THEN the gate MUST include a question resolving that dimension
    ELSE: do not ask (the rule decides deterministically)
  PLUS: source-access declaration confirmation (did the user supply text? which tier set?)
  ALLOW [skip] per entry — but record [skip] in 70-traceability so the rewrite phase knows it was
        defaulted, not decided.
```

This is the analyzer's answer to "ask only what changes the work": the **taxonomy itself** determines
what is ask-worthy. A's free-form gate risks missing the allegory decision; B's coverage rule guarantees
it surfaces iff the challenge type demands it.

## B.5 Where B AGREES with A (to anchor the merge)

- 0.1 owns the phase; root gets a pointer (T1, T7).
- A NATIVE `prep-cordinator` agent + NATIVE skills (`prep-protocol`, `work-mapping`, `challenge-taxonomy`,
  `thematic-fidelity`).
- The fixed-path contract — B ADDS `70-traceability.md` but keeps A's `00..60`.
- Check D in `tier-coordinator`; meaning field in `analyst`.
- Compound-scene protocol as a resource + analyst flag.
- The `/laf:rewrite --work <slug>` handoff.

## B.6 Where B DIFFERS from A (the debate axes)

| Axis | A | B | B's argument |
|---|---|---|---|
| Provenance enforcement | mark exemplars DERIVED | full traceability matrix + per-entry dual-track confidence | contamination risk applies to ALL derived content, not just exemplars |
| Work-level analysis | single track, MEMORY-BASED-allowed | two-track (context + text), per-entry min(text,context) | honesty about what is grounded vs inferred |
| Question gate | free-form, "[skip] allowed" | coverage-constrained by taxonomy's human-judgment dimensions | guarantees meaning-preservation decisions surface; prevents over/under-asking |
| Source-text requirement | optional | optional but DECLARED, with per-entry confidence consequence | makes the "thin entry" honest — thin entry ≠ unaccountable entry |
| Deliverable count | 7 files (00..60) | 8 files (00..70) | traceability is a first-class artifact, not a nicety |

## B.7 Risk B introduces (self-critique, for the debate)

- **Complexity cost.** Two-track analysis + a traceability matrix is more surface area than A. If the
  user just wants a mapping fast, B's rigor may be over-engineered. *Mitigation:* the
  traceability matrix is auto-generated by the `work-mapping` skill (it's a derivative artifact, not
  extra human work); the two-track split is just two dispatches the orchestrator already does.
- **Coverage-rule brittleness.** The "human_judgment_dimension" flag on each challenge type is a new
  taxonomy field that must be authored correctly. If mis-flagged, the gate over- or under-asks.
  *Mitigation:* the `challenge-taxonomy` skill ships with the flag pre-set per challenge type (death →
  yes, violence-level → no, allegory → yes).

## B.8 Positions on T1–T8

Same as A except:
- **T2:** two-track work-level analysis (context + text), not single-track.
- **T3:** coverage-constrained gate (taxonomy-driven question set), not free-form.
- **T4:** contamination fix = traceability matrix + dual-track confidence + DERIVED markers (belt and
  suspenders), not just markers.
- **T5:** path contract = A's 00..60 **+ 70-traceability.md**.

## B.9 Open questions B adds

1. Does the rewrite phase's `muse` actually CONSUME per-entry confidence, or is the traceability matrix
   only for human audit? (If only human, it may not need to be in the hardcoded handoff path.)
2. Is the dual-track confidence worth the schema complexity in `30-mapping.yaml`?
