# `source/` — the work being adapted (read-only reference)

Layout: `source/<work>/ch-<NN>.txt` — one chapter per file, UTF-8.

- The analyst reads a chapter as its `source_path` input (e.g. `source/tolkien/ch-01.txt`) and treats it
  as an external/provisioned, read-only reference (DESIGN.md §2, §6).
- Nothing in `source/` is transformed in place; the pipeline writes adaptations under `work/` and `kb/`.

## Materialization outputs (Stage 0)

`/laf:prep` Stage 0 (owned by `prep-cordinator`, procedure in `laf-adaptation:chapter-materialize`)
materializes chapters from a folder / monolith / adopt-set and writes two source-side outputs per work:

- `source/<slug>/chapter-manifest.yaml` — the confidence-tagged provenance sidecar (per-chapter id, order,
  title, output hash, provenance, split/title/order confidence, plus mode, normalization events, omitted
  matter, `ambiguous_splits`, and `review.status`). It is a `source/` sidecar, NOT a numbered prep-package
  file and NOT in the rewrite read-set.
- `source/<slug>/.raw/` — the retained original inputs (HTML/PDF/etc.) kept as the fidelity anchor.

`source/` stays read-only-after-materialize: materialization adds NEW files (chapters, manifest, `.raw/`),
never edits existing chapter bodies in place. Existing hand-provisioned sets (`narnia/ch-01..04.txt`,
`tolkien/ch-01.txt`) are adopted with zero re-split.

## Provisioning contract (Phase-3 proof, DESIGN.md §7 Phase 3)

The Phase-3 hard gate runs on "one Tolkien chapter." Because Tolkien is **not public domain** (do NOT
commit copyrighted Tolkien prose), the proof chapter is provisioned by one of two paths:
- **PATH A (preferred, execution-time external input):** the operator supplies a real chapter under their
  own access rights at run time (not committed).
- **PATH B (committable fallback):** a public-domain / original synthetic stand-in, purely to prove the
  pipeline mechanics.

**This tree ships a PATH-B fixture:** `source/tolkien/ch-01.txt` is an **ORIGINAL SYNTHETIC proof
fixture** authored for LAF — it is NOT Tolkien's copyrighted prose. It is written in a Tolkien-adjacent
high-fantasy register so it aligns with the committed Tolkien work-mapping
(`kb/adaptation-mapping/tolkien-mapping.yaml`) and exercises every transform class the pipeline must prove
(violence→cooperation, agency externalization, death handling, martial→prosocial heroism, nightmare
framing). Replace it with a PATH-A operator-supplied chapter for a real adaptation run.
