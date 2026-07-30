# Proposal B — Manifest as Trust Boundary: loud-halt over silent-canon-corruption (analyzer lens)

> Archived verbatim from the analyzer-lens agent (opus). Variant B of 3. Selected as the **merge base**.

## Thesis
The *actual* problem is **trust boundary management across a phase seam**: prep made frozen claims about source (`output_sha256`, `chapter_count`, `needs_human_review`), and rewrite is about to promote derivatives into **cumulative canon** via the only canon writer (`chronicler`). A silent source error at chapter N becomes a latent canon contradiction surfacing chapters later — the hardest bug class. The design must make every drift class **loud and recoverable**, never silent. The frozen read-set **gains a 4th entry**, justified because the manifest is the *only* artifact that can convert three silent-corruption modes (hash drift, partial set, un-greenlit source) into detectable halts.

## RQ1 — 4th entry; the failure-mode argument

`rewrite_phase_reads` → 4-file set with `source/<slug>/chapter-manifest.yaml` added. C5 requires surviving prep §12's default. It survives because the options are **not symmetric in failure mode**:

**Option A (convention-discovery, frozen) — three SILENT-corruption modes.** Glob returns a claim-free set, so nothing contradicts reality:
- **Source drift**: `ch-03.txt` edited after prep → analyst reads new text → chronicler promotes into per-tier `continuity.md`. The `output_sha256` that would catch this is never read. Surfaces chapters later as unattributable `disclosure_leak`/`meaning_diff`.
- **Partial set mistaken for complete**: narnia's 4-of-17 adapted as "complete LWW"; `chapter_count:17` never read. Silent scope corruption.
- **Un-greenlit/needs-review source**: `review.status:PENDING` or `needs_human_review:true` invisible; rewrite canonizes unvetted chapters.

**Option B (4th entry) — the same three modes become LOUD halts.** The manifest makes a claim, reality contradicts it, the contradiction is a halt: D1 hash mismatch → HALT chapter before step 1; D3 count mismatch → HALT at set construction; D2 PENDING/needs-review → HALT before loop.

**Why this survives prep §12:** prep §12 defaulted without weighing **canon cumativity** — `chronicler`'s per-tier `continuity.md` is running state across chapters, so a silent source error compounds. The default is rational for a stateless rewrite; unsafe where rewrite writes cumulative canon.

**Missing-manifest reality (E4) — loud-degrade, not silent-fallback.** `--allow-no-manifest` → convention-discover + loud warning + **force every `analyst` to PARTIAL access** (facts ≤ PROBABLE, never CERTAIN), riding `/source-fidelity` into reconciliation as visible lower-confidence facts. Default (no flag, no manifest) = HALT with instruction to prep or flag.

## RQ2 — inline at step 1, with a loop-entry pre-flight
Analyst stays inline at step 1 (near-free, C6). New driver skill adds a **loop-entry pre-flight**: confirm each in-scope `ch-NN.txt` exists and is non-empty before the loop body. Missing → halt at set construction. Analyst's Phase-0 ABORT remains the authoritative per-chapter gate. UNCERTAIN analysis propagates (doesn't halt) — tags ride into tier-coordinator Check A as CONFLICT.

## RQ3 — resume predicate + selection
Selection: `--chapter N` / `--chapters range` / `--tier N` / `--tiers set`; default = all manifest chapters. Selection intersects the declared set. Resume = skip DONE, re-run in-flight, via Glob over accept-triples; `--force` re-runs DONE.

## RQ4 — trust & drift (detect → decide → act), three classes
- **D1 content drift**: recompute sha256 at loop entry vs `output_sha256`. Mismatch → HALT ch C with named diff. Accept via `--accept-source-drift ch-NN` (recorded; analyst→PARTIAL; facts ≤PROBABLE). Never auto-proceed.
- **D2 un-greenlit manifest**: `review.status:PENDING` or in-scope `needs_human_review:true` → HALT before loop (stricter, source-side gate, additional to greenlight per C7). Override `--accept-review-flag ch-NN` (facts UNCERTAIN).
- **D3 partial set**: `len(Glob)` vs `chapter_count`, N<M → HALT at set construction; `--chapters 1-4` proceeds, every downstream artifact records `scope: partial (4 of 17)`.
- **Trust principle**: manifest is trusted-as-claim, verified-against-filesystem at runtime. Zero-trust at the phase seam.

## RQ5 — command surface (no path overrides)
```
/laf:rewrite --work <slug> [--chapter N | --chapters range] [--tier N | --tiers set]
               [--allow-no-manifest] [--accept-source-drift ch-list] [--accept-review-flag ch-list] [--force]
```
No `--source`/`--manifest` overrides (invite unvetted source = reopen silent-corruption surface). Greenlight guard retained; manifest guard additional, ordered after greenlight.

## RQ6 — tier fan-out inner loop; safety per (chapter,tier)
Confirmed: chapter=OUTER (now manifest-driven), tier=INNER. Safety gate per (chapter,tier); T4-T5 SKIP (N/A) and must NOT be required by the DONE predicate. Chronicler per tier only on RECONCILED.

## Resume correctness proof
`DONE(work,C,T) := exists(adapted.md) AND exists(canon-delta.md) AND exists(analysis.yaml)` under `kb/adaptations/<work>/tier-<T>/chapters/ch-<C>/`. Three-way AND. False-positive analysis closes every case (stale `work/analysis` never promoted; partial triple = NOT-DONE; pre-accept `adapted.md` lacks siblings; T4/T5 safety-skip is by design not a false-positive; `--force` is intentional). Only `chronicler` writes these paths, only on accept-after-RECONCILED, so triple existence proves the full 1→11 pipeline ran.

## BOM / ACs / risks
New NATIVE skill `rewrite-chapter-driver` + `resources/drift-rules.yaml`; +1 `skills:` line on `muse` (NATIVE) + pointer paragraph; path-contract §4 +4th entry cross-ref; `.claude/commands/laf/rewrite.md` +flags; VENDOR.md +1 NATIVE row. Zero adopted-body edits; Mode V green. Lead risks are the [SILENT] ones: D1 implemented as cached-compare instead of fresh recompute; DONE predicate degraded to one-of-three; `--allow-no-manifest` failing to force PARTIAL. Rejected: convention-discovery (silent canon corruption); pre-rewrite stage; path overrides.
