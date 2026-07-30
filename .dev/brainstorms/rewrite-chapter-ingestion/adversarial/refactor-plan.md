# Refactor Plan — base B, restructured by C, grafted with A

> Step 4 of the adversarial pipeline. The merge edits applied to base B to produce the merged spec.

## E1. Restructure the read-set contract (C's graft onto B's base)

**From (base B):** a flat 4-entry `rewrite_phase_reads`:
```
work/prep/<slug>/30-mapping.yaml
work/prep/<slug>/40-prep-brief.md
work/prep/<slug>/10-challenges.yaml
source/<slug>/chapter-manifest.yaml        # 4th entry
```
**To (merged, C's two-group framing):**
```
PREP-PACKAGE READS (frozen 3 — byte-unchanged):
  work/prep/<slug>/30-mapping.yaml
  work/prep/<slug>/40-prep-brief.md
  work/prep/<slug>/10-challenges.yaml

SOURCE-SIDE ENUMERATION READS (the chapter set, consumed by chapter-iterate):
  source/<slug>/chapter-manifest.yaml      # the iteration-domain descriptor
  source/<slug>/ch-<NN>.txt                # the per-chapter source files (one per chapter, read inline at step 1)
```
**Rationale:** honors B's "manifest is a declared structural input" (discoverability) AND C's "it is not a
prep-package member and is not Rule-F hash-pinned" (provenance accuracy). The frozen-3 prep-package set is
byte-unchanged; the manifest is added to a clearly-labeled source-side group, with an explicit note that it is
outside the Rule-F hash-pin glob (check_boundary.py scope unchanged → ADR-006 honored).

## E2. Soften B's D3 partial-set default to A/C's WARN+intersect (A's graft)

**From (base B):** D3 (manifest declares M, disk has N<M) → HALT unless `--chapters 1-4`.
**To (merged):**
- **Default (no `--chapter`/`--chapters`):** WARN + intersect (run the chapters that both manifest-declare and
  exist on disk). Downstream artifacts stamp `scope: partial (N of M)`. → keeps the pilot runnable.
- **Explicit selection:** `--chapters 1-5` against 4 files → runs 1-4, WARNS ch-05 requested-but-absent.
- **Explicit-requested-but-absent chapter:** `--chapter 9` on a 4-file set → HALT (the operator named a chapter
  that does not exist; not a silent skip).
**Rationale:** A/C's runnability for the legitimate partial-scope case; B's "explicit request of a missing
chapter halts" rule (no silent skip of something the operator asked for).

## E3. Graft A's extension framing onto the manifest-driver skill

The new NATIVE skill (`chapter-iterate`) documents that the manifest schema is the extension channel for future
per-chapter metadata (cross-chapter dependencies, compound-scene flags), so future needs are schema additions,
not new discovery mechanisms. (A Arg 3.)

## E4. Keep B's uncertainty-propagation + AND-predicate + T4/T5 fix (B's load-bearing grafts)

Carried verbatim from base B:
- `--allow-no-manifest` and `--accept-source-drift`/`--accept-review-flag` force `analyst` to PARTIAL access
  (facts ≤ PROBABLE, never CERTAIN), riding `/source-fidelity` into reconciliation as *visible* lower confidence.
- Formal DONE predicate: three-way AND of the chronicler accept-triple
  (`adapted.md` ∧ `canon-delta.md` ∧ `analysis.yaml`), per (work, tier, chapter); chapter DONE iff triple exists
  for all requested tiers.
- T4/T5 safety-SKIP: the DONE predicate does NOT require a T4/T5 safety report (T4-T5 SKIP with verdict N/A by
  `safety-verifier.md` design; the triple — not the safety report — is the unified DONE signal).

## E5. Keep C's minimal default command surface, graft B's flags as optional escapes

**Default surface (C):** `/laf:rewrite --work <slug> [--chapter N | --chapters <range>] [--tiers <set>]`
**Optional escapes (B):** `--allow-no-manifest`, `--accept-source-drift ch-NN,ch-MM`,
`--accept-review-flag ch-NN`, `--force`. Per-chapter, auditable, never blanket.

## E6. Keep A+B's loop-entry pre-flight; C's redundancy objection overruled

Cheap set-wide existence/non-empty check before the chapter loop body (missing file → halt at construction,
zero drafts written). The analyst's Phase-0 NO-ACCESS remains the authoritative per-chapter gate.

## E7. Keep the universal consensus (A, B, C)

- RQ2: analyst inline at step 1; no pre-rewrite stage.
- RQ3: filesystem-derived resume, no state file; chronicler accept-triple = DONE.
- RQ5: no `--source`/`--manifest` path overrides; manifest convention-discovered from `--work`.
- RQ6: tier fan-out inner loop; safety per (chapter, tier); chronicler per tier only on RECONCILED.
- Greenlight guard retained (C7); manifest guard is additional, ordered after greenlight.
- New NATIVE skill + 1 additive `skills:` line on `muse` + path-contract §4 restructure (not a list edit to the
  frozen-3) + `.claude/commands/laf/rewrite.md` mirror + VENDOR.md row. Zero adopted-body edits; Mode V green.

## E8. Naming

Skill name: `chapter-iterate` (C's name — clearest, most minimal; A's `chapter-ingest` and B's
`rewrite-chapter-driver` describe behavior more than role). The `muse` line: `- laf-adaptation:chapter-iterate`.

## What this merge does NOT carry

- C's silent convention-fallback on a missing manifest → replaced by B's loud-degrade-with-uncertainty (E4).
- B's D3 hard-halt on partial sets → softened to A/C WARN+intersect (E2).
- A's NOTICE-only degrade (no confidence consequence) → upgraded to B's PARTIAL-forcing (E4).
- Any new script/runtime/state-file → none (ADR-006).

These edits produce the merged spec (Step 5).
