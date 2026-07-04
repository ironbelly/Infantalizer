# `source/` — the work being adapted (read-only reference)

Layout: `source/<work>/ch-<NN>.txt` — one chapter per file, UTF-8.

- The analyst reads a chapter as its `source_path` input (e.g. `source/tolkien/ch-01.txt`) and treats it
  as an external/provisioned, read-only reference (DESIGN.md §2, §6).
- Nothing in `source/` is transformed in place; the pipeline writes adaptations under `work/` and `kb/`.

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
