# Merge Log

**Inputs:** proposal-A-architect.md, proposal-B-analyzer.md, proposal-C-scribe.md
**Base:** A. **Grafts:** B (rigor), C (consolidation).
**Convergence:** 0.85 (PASS).

## Resolved decisions (debate outcomes)

| # | Decision | Source | Rationale |
|---|---|---|---|
| D1 | 2 new NATIVE skills (`prep`, `thematic-fidelity`), not 4, not 1 | C + A-partial | `prep` is cohesive + prep-only; `thematic-fidelity` is cross-phase (Check D runs in rewrite) |
| D2 | Path contract = referenced doc imported by 3 consumers | C | single source of truth, no drift |
| D3 | 8 files `00..70` (+traceability) | B | contamination fix needs full provenance |
| D4 | Two-track work-level analysis (context + text), per-entry min(text,context) | B | honesty about grounded vs inferred |
| D5 | Coverage-constrained question gate via `human_judgment_dimension` flag | B | guarantees meaning decisions surface |
| D6 | Meaning → adopted agents via promoted mapping file, NO 2nd `writer` patch | C | cleanest boundary respect; muse reads mapping already |
| D7 | Compound-scene protocol = section in `prep` skill §2.1 | C | avoids muddying adopted-skill sync boundary |
| D8 | Exemplar library = `adaptation-rules/resources/exemplars/<type>.md` with DERIVED markers | A | outside source-truth path; explicit marking |
| D9 | Check D in `tier-coordinator` (BUILD-NEW edit); meaning field in `analyst` (NATIVE edit) | A/B/C consensus | only editable bodies touched |
| D10 | Root parity OUT OF SCOPE (ADR-006) | A/B/C consensus | deliberate T1+T3-only ship |
| D11 | Handoff = `/laf:rewrite --work <slug>` reading fixed paths | A/B/C consensus | spec-kit pattern |

## Carried-forward open questions (for the user / design phase)

1. Should work-level analysis REQUIRE the source text, or remain MEMORY-BASED-allowed with per-entry
   confidence? (Merge: allowed-but-declared, B's two-track — but the user may want to mandate text.)
2. Does the rewrite-phase muse actually consume per-entry confidence, or is `70-traceability.md` human-only?
   (Merge: human+greenlight-only; muse reads `30-mapping.yaml`'s inline confidence.)
3. Is the `human_judgment_dimension` taxonomy flag's default set correct? (Ship pre-set; revisit per work.)
4. Tier set: does prep default to authoring for {1,2,3,5} or only the tiers the user names at greenlight?
   (Merge: author for all four by default, let greenlight narrow.)
5. Exemplar placement: inside adopted `adaptation-rules/resources/` or standalone NATIVE skill? (Merge:
   in-resources with DERIVED markers.)
6. `prep-cordinator` model: opus or sonnet? (Merge: opus.)

## User resolutions (confirmed 2026-07-04) — all six locked

All six confirmed. Five affirm merged defaults; **Q1 changes the design** (source text now mandatory):

- **Q1 = Yes (source required):** entry point elicits source path as mandatory input; MEMORY-BASED not
  acceptable at work level; Phase-0 ABORT-on-NO-ACCESS applies. → R1, R6, Stage 1 updated; this is a
  substantive design change, not a confirmation.
- **Q2 = Human+Greenlight audit:** `70-traceability.md` not consumed by rewrite muse. (confirms default)
- **Q3 = Yes:** `human_judgment_dimension` default flag set accepted. (confirms default)
- **Q4 = All four, greenlight narrows:** mapping authored for {1,2,3,5} by default. (confirms default)
- **Q5 = inside adopted `adaptation-rules/resources/`:** exemplars stay in-resources, DERIVED-marked.
  (confirms default; change-list #7 upgraded ⚠️→✅)
- **Q6 = opus:** `prep-cordinator` model opus. (confirms default)

## Unresolved conflicts: none blocking. (Convergence 0.85 ≥ 0.65.)
