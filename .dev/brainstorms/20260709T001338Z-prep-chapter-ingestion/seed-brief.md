---
topic: "Next version of /laf:prep that either ingests a folder of per-chapter source files, or splits a single source file into per-chapter files"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-07-09T00:13:38Z
---

# Seed Brief: prep-chapter-ingestion

## Problem Statement

`/laf:prep` today onboards a work at **work granularity**: it takes a single `--source <path>`, runs a
work-level source-fidelity analysis (`20-analysis-work-level.yaml`), and emits the fixed 8-file package
`work/prep/<slug>/`. The per-chapter source layout (`source/<work>/ch-<NN>.txt`, one chapter per file,
documented in `source/README.md`) is assumed to **already exist** — the operator must hand-split the book
before prep runs. Reality (see `Books/LWW/`) is messier: a work arrives as a monolithic HTML/PDF, OR as a
loose folder of per-chapter HTML files with inconsistent names. Nothing in the pipeline owns the step that
turns raw source into the canonical `source/<work>/ch-<NN>.txt` set, and nothing records the resulting
chapter set as first-class prep state that the rewrite phase can trust.

The next version of `/laf:prep` must own **chapter materialization** in two input modes, emit a canonical
**chapter manifest**, and remain faithful to the LAF boundary contract (prompt+YAML framework, one script
max, no runtime, source is read-only, adopted bodies never edited).

## Known Context

- **Two input modes required by the ask:**
  - **Mode A — folder ingest:** a directory of individual per-chapter source files (e.g. the split
    `Books/LWW/*.html`) → normalize/order/rename into `source/<slug>/ch-<NN>.txt`.
  - **Mode B — single-file split:** one source file (monolithic HTML/PDF/txt) → detect chapter
    boundaries and split into `source/<slug>/ch-<NN>.txt`.
- **Canonical target layout already fixed** by `source/README.md`: `source/<work>/ch-<NN>.txt`, UTF-8,
  one chapter per file, read-only reference; nothing in `source/` is transformed in place.
- **Prep package layout is a hard contract** (`skills/prep/resources/path-contract.md`): 8 fixed files
  `00`–`70`; `rewrite_phase_reads` is exactly `[30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]`;
  greenlight gates promotion; write-ownership is explicit. Any new chapter artifact must slot into this
  contract without breaking the frozen read-set.
- **Analyst is tier-invariant and currently work-level** (`granularity=work`). It reads a chapter file as
  `source_path` in the rewrite phase; the source-fidelity protocol ABORTS on NO-ACCESS.
- **LAF constraints (CLAUDE.md, ADR-006):** prompt+YAML framework, NOT software; exactly one script
  (`check_boundary.py`, a validator, not a runtime) — a new heavy splitter script would violate this;
  adopted files are patch-clean and never edited; native knowledge enters adopted agents only via
  `skills:` frontmatter; source is read-only.
- **Anti-hallucination discipline** (`/source-fidelity`): every extracted fact gets CERTAIN/PROBABLE/
  UNCERTAIN; splitting decisions (where a chapter starts/ends, its title, its number) are exactly the
  kind of extraction that must carry confidence and a human-verifiable gate.
- **Existing prepped works:** `work/prep/narnia/`, `work/prep/tolkien/` already exist at work-level;
  `source/narnia/ch-01..04.txt` and `source/tolkien/ch-01.txt` exist. Backward compatibility with these
  is desirable.

## Constraints

- MUST stay within the LAF "framework not software" rule (ADR-006): no second script/runtime; splitting
  logic expressed as a prompt-driven agent procedure + confidence-gated verification, not a parser binary.
- MUST NOT edit any adopted agent/skill body; new capability enters via a NATIVE skill and/or the
  `prep-cordinator` procedure + `skills:` frontmatter, honoring `check_boundary.py`.
- MUST NOT transform files in `source/` in place; materialized chapters are new files under `source/<slug>/`.
- MUST preserve the existing 8-file package contract and the frozen `rewrite_phase_reads` set (extend, do
  not break). A chapter manifest must be added in a contract-compatible way.
- MUST keep the source-access ABORT gate and confidence tagging (splitting is fallible; boundaries/titles
  need CERTAIN/PROBABLE/UNCERTAIN + a human verification gate before greenlight).
- MUST produce a deterministic, reviewable chapter set: stable `ch-<NN>` numbering, recorded titles,
  provenance back to the raw source, and an idempotent re-run story.

## Success Criteria

- Running the next `/laf:prep` against (a) a folder of per-chapter files OR (b) a single monolithic file
  yields the same canonical `source/<slug>/ch-<NN>.txt` set plus a first-class chapter manifest, with no
  manual pre-splitting.
- The chapter manifest is consumable by the (future) rewrite phase to drive per-chapter work: it records
  chapter count, order, `ch-<NN>` id, title, source path, and per-chapter split confidence.
- Boundary contract (`check_boundary.py`) still passes; no adopted body edited; still one script.
- Ambiguous splits (missing/duplicate chapter headings, front/back matter, unnumbered prologues) are
  surfaced to the human at the existing question/greenlight gate rather than silently guessed.
- Backward compatible: an already-split `source/<slug>/` (narnia, tolkien) is detected and adopted without
  re-splitting.
- A clean handoff exists to the next `/laf:rewrite` that consumes individual chapter files.

## Open Questions (deliberately left for parallel proposals to diverge on)

- **OQ1 — Ownership:** Does `/laf:prep` itself own materialization, or a distinct pre-prep step/skill
  (e.g. `/laf:ingest`) that runs first and feeds prep? (Prompt implies prep owns it — proposals should
  still weigh the seam.)
- **OQ2 — Analysis granularity:** Does the new prep stay work-level (materialize chapters + manifest only,
  analysis stays whole-work), or move to per-chapter analysis now? This directly shapes the rewrite spec.
- **OQ3 — Split mechanism under ADR-006:** How is boundary detection expressed without adding a runtime —
  agent-driven heading/TOC heuristics with confidence, a YAML-config-declared boundary ruleset, or an
  extension to the single allowed script? Where is the "not software" line?
- **OQ4 — Manifest placement in the frozen contract:** New numbered package file (e.g. `05-chapters.yaml`),
  a section of an existing file, or a `source/<slug>/manifest.yaml` sidecar? Does `rewrite_phase_reads`
  gain a 4th entry, and how is that frozen-set change justified?
- **OQ5 — Format normalization:** HTML/PDF → clean UTF-8 text (strip boilerplate/markup) — how much
  cleaning, and how is fidelity to the source asserted (`/source-fidelity`) when markup is discarded?
- **OQ6 — Idempotency & confidence gating:** Re-run semantics, collision handling with existing chapter
  files, and exactly where low-confidence splits enter the human question/greenlight gate.
