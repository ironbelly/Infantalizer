# Diff Analysis — 3 Variants on `/laf:rewrite` v-next

> Step 1 of the adversarial pipeline. Compares Proposal A (architect), B (analyzer), C (refactorer) across the
> 6 open questions. Divergence is concentrated on RQ1; strong consensus elsewhere.

## Consensus (all 3 agree — low-debate, high-confidence)

| Question | Consensus position |
|---|---|
| **RQ2** (per-chapter analysis) | **Inline at workflow step 1.** The `analyst` already runs once per chapter (tier-invariant, ABORT-on-NO-ACCESS). No separate pre-rewrite analysis stage. (A, B, C all reject the stage.) |
| **RQ3** (resume) | **Filesystem-derived done-state, no new state file.** The chronicler accept-triple (`adapted.md`+`canon-delta.md`+`analysis.yaml` under `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/`) is the definitive per-(chapter,tier) DONE marker. DONE iff triple exists for all requested tiers. Glob+Read walk. |
| **RQ6** (tier fan-out) | **Tier fan-out is the INNER loop** (one chapter → tiers → chronicler-per-tier). Chapter is the OUTER loop (now manifest-driven, formerly informal). Safety gate per (chapter,tier); chronicler per tier only on RECONCILED. Do not invert. |
| **RQ5 partial** (no path overrides) | **No `--source`/`--manifest` overrides.** The manifest is convention-discovered from `--work` at `source/<slug>/chapter-manifest.yaml`. Single source of truth. |
| **C1-C4,C7** (constraints) | All three: no new script/runtime/CLI (ADR-006); no adopted-body edits; `source/` read-only; chronicler sole canon writer; tier axis first-class; greenlight guard retained. |

## Divergence (the actual debate)

### Axis 1 — RQ1: does `rewrite_phase_reads` gain a 4th entry? (THE crux)

| Variant | Position | Core argument |
|---|---|---|
| **A** (architect) | **4th entry.** Manifest is the "iteration-domain descriptor" → first-class read. | (1) A real, authoritative artifact ignored by its consumer rots silently (write-only manifest). (2) Convention-discovery creates two sources of truth (prep's manifest vs rewrite's glob) that diverge. (3) Drift detection (`output_sha256`), completeness (`chapter_count`), per-chapter review gating (`needs_human_review`) are only reachable through the manifest — integrity properties + an extension channel convention-discovery lacks. |
| **B** (analyzer) | **4th entry.** Manifest is a "trust boundary." | **Failure-mode asymmetry.** Convention-discovery's failures (source drift, partial set, un-greenlit source) are *silent* and land in *cumulative canon* via `chronicler` (running state across chapters → errors compound and surface chapters later, unattributable). The 4th entry converts those three silent-corruption modes (D1/D2/D3) into *loud, recoverable, diagnosable* halts. prep §12's default was written without weighing canon cumativity. |
| **C** (refactorer) | **No change.** Read-set stays frozen at 3; manifest is a separate "source-enumeration" surface. | **Category distinction.** `rewrite_phase_reads` (path-contract §4) is literally the list of *prep-package files* under `work/prep/<slug>/`. The manifest lives at `source/<slug>/` — a source-side sidecar. The analyst already reads `source/<slug>/ch-NN.txt` without it being "in the read-set." "Rewrite reads the manifest" ≠ "the manifest is a 4th read-set member." Resolve with a §4 NOTE, not a list edit. |

**Structural note:** A and B agree *mechanically* (4th entry) but B's justification (failure-mode / canon-cumativity) is more load-bearing than A's (single-source-of-truth + extension). C's objection targets the *framing*, not the read — C concedes the manifest must be read (for S5 drift) and disputes only *where it's declared*.

### Axis 2 — drift strictness & missing-manifest behavior (secondary)

| Behavior | A | B | C |
|---|---|---|---|
| Missing manifest (E4 reality — none exists today) | **Degrade** to convention-discovery + NOTICE | **HALT by default**; `--allow-no-manifest` → loud degrade **forcing analyst→PARTIAL** (facts ≤ PROBABLE) | **Degrade** to convention-discovery + note |
| Partial source set (narnia 4-of-17) | **WARN**, run intersection | **D3 HALT** at set-construction unless explicitly scoped (`--chapters 1-4`); stamps `scope: partial` downstream | Iterate intersection, **non-blocking note** |
| Hash drift (`output_sha256` mismatch) | HALT per chapter; accept-risk in transcript | HALT per chapter; `--accept-source-drift ch-NN` (recorded, analyst→PARTIAL) | HALT per chapter; "re-prep or edit manifest hash" |
| `review.status: PENDING` | HALT whole run (separate gate) | **D2 HALT** before loop (stricter source-side gate) | HALT (folds into greenlight gate) |
| Richness of accept/override flags | moderate | **richest** (`--accept-source-drift`, `--accept-review-flag`, `--force`, `--tier`/`--tiers`) | **minimal** (`--chapter`/`--chapters` only) |

### Axis 3 — analyst pre-flight (RQ2 minor)

A and B add a **loop-entry pre-flight** (confirm in-scope `ch-NN.txt` exist/non-empty before the loop body). C cuts it as redundant with the analyst's Phase-0 NO-ACCESS gate. B notes the pre-flight gives a clean set-wide abort (missing file → halt at construction, zero drafts); the authoritative per-chapter ABORT stays the analyst's Phase-0.

### Axis 4 — DONE predicate rigor (RQ3 minor)

All use the accept-triple, but only **B** (a) states the three-way AND formally, (b) runs a full false-positive analysis, and (c) discovers from the live filesystem that **T4/T5 safety reports must NOT be required by the DONE predicate** (narnia has no `ch-*-t5.md` because T4-T5 SKIP by design — a naive "all-tier safety reports present" predicate would false-positive).

## Divergence summary

- **One real fork:** RQ1 (4th entry vs frozen). A+B say 4th entry; C says frozen-with-NOTE.
- **One gradient:** drift strictness (B strictest → A middle → C most permissive) + command-surface richness (B richest → A moderate → C minimal).
- **Everything else:** consensus.

The merge decision is therefore: (1) adjudicate RQ1, (2) pick a point on the strictness gradient, (3) graft the best mechanism from each (B's uncertainty-propagation, A's extension framing, C's operational minimalism + provenance NOTE).
