# Merge Log — rewrite-chapter-ingestion

> Step 5 of the adversarial pipeline. Provenance-annotated record of the merge that produced
> `merged-requirements.md`.

## Inputs
- **Seed:** `seed-brief.md` (domain: architecture, strategy: systematic, depth: deep)
- **Enrichment:** `enrichment/codebase-context.md` (primary tier; 6 findings E1-E6, validated against live `work/` + `kb/adaptations/` + `source/`)
- **3 variants:** `proposal-architect.md` (A, opus), `proposal-analyzer.md` (B, opus), `proposal-refactorer.md` (C, haiku)
- **Grounding:** current `rewrite.md`, `path-contract.md`, `CLAUDE.md`, 5 agents, upstream prep-v-next `merged-requirements.md`

## Diff → Debate → Selection
- **diff-analysis.md:** consensus on RQ2/RQ3/RQ6; one real fork (RQ1: 4th entry vs frozen) + one gradient (drift strictness B→A→C).
- **debate-transcript.md:** 4 rounds. Round 3 found the convergent seam — two-group read-set (frozen-3 prep-package reads + source-side enumeration group), satisfying A/B's discoverability demand and C's provenance-accuracy demand simultaneously. Round 4 adjudicated the strictness gradient: B's uncertainty-propagation adopted as the unifying mechanism; B's D3 hard-halt softened to A/C's WARN+intersect; B's AND-predicate + T4/T5-fix adopted; C's minimal surface kept as default with B's accept-flags as optional escapes; A+B's loop-entry pre-flight kept.
- **base-selection.md:** hybrid scoring (constraint fidelity ×3, correctness ×3, maintainability ×2, minimalism ×2, runnability ×2, resume-rigor ×1, grounding ×1). B=116, C=117, A=114 — near-tied. **B selected as base** (load-bearing correctness/canon-integrity dimension: B=10, C=6; safer to soften strictness than to harden silence), **restructured by C's two-group framing**, with A/C grafts.

## Merge edits (refactor-plan.md, §E1-E8)
| Edit | Source | What it does |
|---|---|---|
| E1 read-set two-group restructure | C (grafted onto B) | manifest declared structural input; frozen-3 byte-unchanged; not Rule-F hash-pinned |
| E2 D3 WARN+intersect default | A/C (softens B) | keeps 4-of-17 pilot runnable; explicit-missing-chapter still halts |
| E3 extension framing | A | manifest schema = future per-chapter-metadata channel |
| E4 uncertainty-propagation + AND-predicate + T4/T5 fix | B (load-bearing) | `--allow-no-manifest`/accept-flags → analyst PARTIAL → facts ≤ PROBABLE; three-way AND; no t5 safety-report requirement |
| E5 minimal default surface + optional escapes | C (base) + B (escapes) | `--work`/`--chapter`/`--chapters`/`--tiers` default; accept-flags optional |
| E6 loop-entry pre-flight | A+B | zero-cost, zero-draft abort on missing/empty file |
| E7 universal consensus | A,B,C | inline analyst; filesystem resume; no path overrides; tier inner loop; greenlight retained |
| E8 skill name `chapter-iterate` | C | clearest/minimal |

## Convergence
**0.86 (PASS, > 0.75 threshold).** No unresolved conflicts. Every open question (RQ1-RQ6) explicitly resolved.

## Provenance of the merged spec
The merged `merged-requirements.md` is **base B's structure + safety model**, **reframed by C's category
distinction** (the §4 two-group restructure is the merge's central innovation — neither A, B, nor C proposed it
flatly; it emerged in debate Round 3 as the synthesis of A/B's "manifest must be declared" and C's "manifest is
not a prep-package member"), with **A's extension framing and partial-set WARN** grafted, and **B's D3
partial-set hard-halt softened** to A/C's runnability-friendly default. All three contributors' load-bearing
ideas are carried; none of the three's rejected-alternative failure modes survive.

## Artifacts
- `merged-requirements.md` (26,263 bytes) — the deliverable
- `seed-brief.md` (12,395)
- `enrichment/codebase-context.md` (6,129)
- `adversarial/{diff-analysis, debate-transcript, base-selection, refactor-plan}.md` + 3 proposals
