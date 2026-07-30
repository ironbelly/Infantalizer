---
name: chapter-materialize
description: |
  The Stage-0 source-materialization procedure for /laf:prep: detect input mode (adopt/folder/file),
  apply multi-signal boundary detection, normalize HTML/PDF to plain text, and emit the confidence-tagged
  source/<slug>/chapter-manifest.yaml + canonical ch-<NN>.txt set. Prompt+YAML only, no runtime (ADR-006);
  check_boundary.py stays the sole script. Load when onboarding a work whose chapters are not yet split.
---

# Chapter Materialize — Stage-0 Source Materialization

Principle: Turn whatever `--source` resolves to into the canonical `ch-<NN>.txt` set + a confidence-tagged
manifest — without guessing. Prompt + YAML only; no new runtime; `check_boundary.py` stays the sole script
and a validator only (ADR-006).

## Scope & non-runtime invariant

This skill is a **procedure executed by the model inline** in the `prep-cordinator`'s context. It adds
**no** script, parser binary, or CLI. The declarative patterns each evidence layer matches on live in
`resources/boundary-rules.yaml` as data the model reads — never as code the boundary script executes. The
`analyst` agent is **not** repurposed as the splitter; it continues to produce one shared, tier-neutral
source analysis and takes no part in boundary detection here.

**`check_boundary.py` remains the sole script and a validator only; this skill emits no code.**

## Stage 0.1 — Inventory & source-access declaration

1. **List every raw input** the `--source` argument resolves to, recording for each: path, byte size,
   file extension, and `sha256`. **URL `--source`:** when `--source` resolves to a URL (not a local
   path), it is FETCHED to a local file under `source/<slug>/.raw/` FIRST, and that local path becomes
   the working `source_path` for all downstream stages; the original URL is recorded in
   `provenance` (the `.raw/` copy is the fidelity anchor and the URL is retained as its origin). All
   inventory fields (byte size, extension, `sha256`) are then computed on the fetched local file.
2. **Run the `/source-fidelity` source-access declaration FIRST** (its Phase 0). Declare exactly one
   access level (FULL / PARTIAL / MEMORY-BASED / NO ACCESS) by the observable test on the resolved path,
   and **ABORT on NO-ACCESS** before any further work — the unchanged uncertainty discipline. A
   MEMORY-BASED declaration forces every downstream fact UNCERTAIN.
3. **Identify the candidate set(s)** — the file or files that could constitute the work's chapters, and
   any front matter / duplicate monoliths sitting alongside them.
4. **Populate `raw_sources[]`** — one entry per input, tagging its `role` ∈
   `monolith | chapter_file | front_matter | ignored_duplicate`. This `raw_sources[].role` is a
   PROVISIONAL classification finalized after the Stage 0.3 evidence pass (e.g. `front_matter` vs
   `chapter_file` can flip once headings are mapped).

## Stage 0.2 — Detect input mode

Apply the auto-detect **precedence** in this exact order — load-bearing, evaluate top-to-bottom and pick
the first that holds:

1. `adopt` (Mode C) — `source/<slug>/ch-*.txt` already exists and validates. **`validates` = every
   file matches the canonical `ch-<NN>.txt` name (zero-padded, contiguous ordinals from 01, no gaps),
   each is non-empty, and `order == numeric id`.** Adopt only when validation passes; otherwise fall
   through to `folder` / ambiguity.
2. `folder` (Mode A) — `--source` is a directory of ≥2 non-canonical per-chapter files. **`non-canonical`
   = a per-chapter file whose name does NOT already match the canonical `source/<slug>/ch-<NN>.txt` form
   (i.e. it needs materialization, not adoption)** — this distinguishes Mode A input from an
   already-adopted Mode C set. **Negative guard (both-present): rule 2 fires ONLY when the directory holds
   ≥2 non-canonical per-chapter files AND NO co-present dominating monolith. If BOTH a split chapter-set
   AND a dominating monolith are present in the same directory, rule 2 does NOT fire — fall through to
   rule 4 (ambiguity → HALT-ask). Auto-detect must not guess `folder` in the both-present case.**
3. `file` (Mode B) — `--source` is a single file.
4. **Ambiguity → HALT-ask, do not guess.** Directory with BOTH split-like files AND a dominating
   monolith (the real `Books/LWW/` case: `-1..-4.html` **and** `…copy*.html`) → `mode_confidence:
   UNCERTAIN` → mode question at the gate. This both-present case is reached by construction: rule 2's
   negative guard (above) prevents `folder` from firing when a co-present dominating monolith exists, so
   the split+monolith directory falls through to here rather than auto-picking `folder`. Detection is
   itself confidence-tagged; PROBABLE/UNCERTAIN mode **blocks any `source/` write until resolved** (no
   `ch-<NN>.txt`, no manifest, no `.raw/` copy is written while mode is unresolved). `--source-mode`
   operator override is honored here (auto must HALT; the operator may still force a mode explicitly).

Output: `input_mode` + `mode_confidence`.

**`--source-mode` override → `input_mode` mapping.** When the `prep-cordinator` forwards a `source_mode`
value (from the command's `--source-mode` flag; see the coordinator's `## Inputs`), it maps to the
manifest `input_mode` and forces that mode, bypassing the auto-precedence above:

| `--source-mode` value | forced `input_mode` |
|---|---|
| `folder` | `folder` |
| `file` | `single-file` |
| `adopt` | `adopt-existing` |
| `auto` (default) | run the auto-precedence 1–4 above |

An explicit `folder` / `file` / `adopt` override sets `mode_confidence: CERTAIN` for the mode itself
(the operator asserted it); `auto` leaves `mode_confidence` derived by the precedence rules (and an
unresolved both-present ambiguity still HALTs under `auto`).

## Stage 0.3 — Boundary & plan (NO writes)

The core stage: derive chapter boundaries, titles, and order by corroborating multiple independent
signals. This stage **plans only — no writes**.

### The five evidence layers

Apply all applicable layers; each layer's declarative patterns live in `resources/boundary-rules.yaml`.

| # | Layer | Signal / note |
|---|-------|---------------|
| 1 | TOC / anchor map | Table-of-contents list items and in-doc anchors give an expected chapter count and ordinal set. |
| 2 | Body-heading map | Match `CHAPTER I`, `Chapter 1`, `Chapter One`, `<h1>`/`<h2 class=chapter>`; roman / arabic / spelled numbering. Heading must be an isolated structural line, not a heading-like string inside prose. |
| 3 | Filename map (Mode A) | Ordinals extracted from filenames, sorted by **NATURAL sort, never lexicographic** — so `ch-2` before `ch-10`. |
| 4 | Content sanity | Each chapter starts with its expected heading, has a non-empty body, a plausible length, and non-overlapping ranges. |
| 5 | Count reconciliation | TOC vs body-heading vs filename counts must agree or the item goes to the gate. |

**Mode A completeness (single-source count is not a completeness proof).** In Mode A (folder), a filename
count alone (e.g. `-1..-4`, four files) cannot certify that the split is *complete* — a partial export of
4-of-17 chapters presents four internally-consistent files with no self-evident gap. Therefore: when Mode A
has **NO corroborating expected-count signal** (no TOC entry count, no cross-checkable body-heading count
that spans the whole work), chapter-set **COMPLETENESS is treated as UNCERTAIN** and an `ambiguous_split`
gate item is raised — "possible incomplete split; operator confirm partial scope." Per-boundary confidence
may still read CERTAIN for the files that ARE present; completeness is a separate axis and its UNCERTAIN
status blocks greenlight until the operator confirms the scope. (Matches the "Split set incomplete" and
count-reconciliation failure-mode rows.)

### Confidence rule (load-bearing)

**"CERTAIN requires ≥2 independent agreeing signals and no contradiction."** A *contradiction* = two
independent signals disagree on the same fact — different boundary offsets for the same chapter, different
chapter counts (TOC vs body-heading vs filename), or different titles/ordinals. Any contradiction caps the
affected boundary at UNCERTAIN regardless of signal count. One strong signal + plausible
content → **PROBABLE**. Missing/contradictory signals, manual repair, or PDF garble → **UNCERTAIN**.
**Single-signal boundaries are capped at PROBABLE** (never CERTAIN). Every boundary / title / order is a
`/source-fidelity`-tagged fact — reuse the CERTAIN/PROBABLE/UNCERTAIN vocabulary; invent no new levels.
**No writes in this stage** (plan only).

## Stage 0.4 — Commit (gated)

The deferred-write safety invariant governs this stage:

**"No `ch-NN.txt` for a PROBABLE/UNCERTAIN boundary is committed before the human resolves it."**

- **CERTAIN chapters materialize immediately** as new `source/<slug>/ch-<NN>.txt`.
- The **raw input is retained** under `source/<slug>/.raw/` as the fidelity anchor.
- `chapter-manifest.yaml` is written with `review.status: PENDING`.
- Any **PROBABLE / UNCERTAIN / collision / mode-ambiguity** item is recorded as an `ambiguous_splits[]`
  entry, and its write is **deferred** — never committed at this stage.

## Stage 0.5 — Route to gate

Deferred `ambiguous_splits[]` items and every `needs_human_review` item are injected into the **existing
§5 question gate** — this skill introduces **no new gate or HALT machinery**. **Greenlight cannot reach
CONFIRMED while any of these is unresolved.** On confirm, the `prep-cordinator` (not this skill) commits
the deferred writes and sets `chapter-manifest.review.status: CONFIRMED`. Each ambiguous split allows a
`[skip] → DEFAULTED` disposition recorded in `70-traceability.md`.

## Format normalization & fidelity

- **HTML** → strip tags, scripts, style, and nav/boilerplate; decode entities; preserve paragraph breaks.
- **PDF** → extract the text stream, rejoin hyphenated line-wraps, preserve paragraph breaks. PDF text is
  obtained by the model reading the PDF directly (the executing model's native PDF-read capability); NO
  extraction script is added (ADR-006). PDF sources are inherently lower-fidelity: extraction garble
  (broken words, ligatures, repeated page headers) caps the affected boundaries at UNCERTAIN and blocks
  greenlight until a human accepts the result or supplies a cleaner source (per the PDF failure-mode row).
- Output is **UTF-8 plain text**.
- **No rewording, no reflow, no editorial change** — verbatim prose with markup removed.
- The **raw input is retained at `.raw/`** as the fidelity anchor.
- **Every discard is a `normalization_event` with a `source_fidelity_risk` label.** Italics-in-titles,
  verse indentation, letters, footnotes, illustrations, and page breaks may carry meaning.
- **High-risk losses block greenlight** unless accepted in `50-greenlight.md` (recorded in
  `70-traceability.md`).
- Confidence: a pure tag-strip → **CERTAIN**; structural ambiguity (tables / footnotes / verse) →
  **PROBABLE** and surfaced.

## Idempotency, collisions, backward-compat

- **Mode C adopt (zero re-split):** if `source/<slug>/ch-*.txt` exists, read titles/ordinals from the
  existing files and write/refresh ONLY `chapter-manifest.yaml` with `provenance.class: ADOPTED`. narnia
  (ch-01..04) + tolkien (ch-01) adopt untouched. A manifest-less existing set adopts with
  `split_confidence: CERTAIN` for existence, but `provenance` gaps are flagged for review.
- **Adopted sets may have no raw source (`raw_path` / `.raw/` MAY be absent/null).** For
  `provenance.class: ADOPTED`, the canonical `ch-<NN>.txt` files are the origin — there is no retained
  upstream monolith to anchor to. Adopt therefore writes/refreshes ONLY the manifest and does NOT create
  a `.raw/` copy; the `provenance.raw_path` field and the `source/<slug>/.raw/` directory MAY legitimately
  be absent/null for an adopted set (a manifest-less adopted set has no retained raw). The `raw_path` /
  `.raw/` fields are structurally present in the schema for MATERIALIZED chapters; for ADOPTED chapters
  their absence is expected, not a fidelity gap.
- **Re-run:** read the manifest first. Raw + output hashes match → **no-op** (`review.status: CONFIRMED`
  short-circuits Stage 0). Raw changed but output exists → a diff-style replacement **PLAN**, gated;
  **never overwrite by default.**
- **Duplicate-monolith canonical pick (deterministic):** when duplicates are byte-identical (same
  sha256), pick the canonical by **shortest filename → lexicographic order** on ties (so the un-suffixed
  base name wins over `... copy N`); the rest are `role: ignored_duplicate`. The byte-identity is itself
  resolved by sha256 (only same-sha256 files are treated as duplicates in the first place). (Matches the
  `ignore_globs` intent; see the identically-worded tie-break note in `boundary-rules.yaml`.)
- **Collision:** an existing `ch-NN.txt` whose hash differs from a proposed resplit is **never
  clobbered** → **HALT-and-ask** at the gate.

## Failure modes (release-gating)

This table is the release-gating contract — carried verbatim.

| Failure mode | Detection | Resolution / gate |
|---|---|---|
| HTML boilerplate as chapter | first output before first body heading; high tag/meta density | exclude as front matter only after human confirm |
| TOC entries split as chapters | tiny anchor-only "chapters" before first body heading | classify as contents; gate if no body headings |
| Missing chapter heading | gap in roman/arabic run (IV→VI) | UNCERTAIN; ask missing/merged/variant |
| Duplicate heading | two `CHAPTER I` markers | block write; ask which is real |
| Unnumbered prologue/epilogue | non-boilerplate prose outside chapter ranges | gate disposition: ch-00 / attach / omit / back matter |
| `Chapter One` vs `CHAPTER I` | heading map supports spelled/roman/arabic; unmatched listed | PROBABLE/UNCERTAIN per corroboration |
| Numbered-only headings | isolated `I`/`1` line + TOC match | require title/count corroboration else review |
| Footnotes/illustrations lost | `footnote`/`img`/caption markup | normalization_event; gate medium/high risk |
| PDF extraction garble | broken words, ligatures, repeated page headers | UNCERTAIN; block greenlight until accepted or cleaner source |
| Multi-file sort wrong | lexicographic ≠ natural sort; heading sequence mismatch | natural sort; if headings contradict filenames, ask |
| Split set incomplete | file count < TOC count (`-1..-4` but TOC says 17) | block Mode A unless operator confirms partial scope |
| Monolith duplicates | `copy.html`, `copy 2.html` hash-identical | pick one canonical; others `ignored_duplicate` |
| Existing source collision | `ch-NN.txt` exists, differs from resplit | adopt if hash matches; else explicit overwrite plan at gate |
| Boundary inside poem/quote | heading-like string not isolated/structural | reject weak marker; mark UNCERTAIN if ambiguous |
| Back matter in final chapter | license/boilerplate after final body | omit as back matter; gate if real prose present |
| Mode ambiguity (split + monolith both present) | both candidate sets exist | `mode_confidence: UNCERTAIN`; ask folder vs file |

## Manifest output contract

**"`chapter-manifest.yaml` is a `source/` sidecar — NOT a numbered package file, NOT a
`rewrite_phase_reads` member."** It is co-located with the chapters it indexes, outside the Rule-F
hash-pin glob. The skill emits the v1 schema below (`review.status: PENDING`); `prep-cordinator` flips it
to `CONFIRMED` on greenlight.

**AC1 "identical" scope.** The canonical `ch-<NN>.txt` chapter TEXT is identical across Mode A (folder)
and Mode B (single-file) input for the same work — that is the AC1 equivalence. The **manifest itself is
NOT byte-identical** across modes: its mode/provenance fields (`input_mode`, `provenance.source_kind`,
`raw_sources[].role`, per-chapter `start_marker`/`end_marker`) legitimately differ by input mode. AC1
constrains the chapter text set, not the manifest's mode-specific provenance.

```yaml
schema_version: laf.chapter_manifest.v1
work: narnia
slug: narnia
title: "The Lion, the Witch and the Wardrobe"
materialized_at: <ISO-8601>
input_mode: folder | single-file | adopt-existing
mode_confidence: CERTAIN | PROBABLE | UNCERTAIN
raw_sources:
  - path: "Books/LWW/....html"      # retained at source/<slug>/.raw/<file>
    role: monolith | chapter_file | front_matter | ignored_duplicate
    sha256: "..."
    mime_hint: text/html
normalization_policy:
  output_format: utf-8-plain-text
  preserved_as_text: [chapter_heading, chapter_title]
  discarded: [html_tags, anchors, css, nav]
chapter_count: 17
chapters:
  - id: ch-01                       # stable, zero-padded; order == numeric id
    order: 1
    title: "Lucy Looks into a Wardrobe"
    title_confidence: CERTAIN
    file: ch-01.txt                 # relative to source/<slug>/
    output_sha256: "..."
    provenance:
      class: MATERIALIZED | ADOPTED
      raw_path: ".raw/...html"
      source_kind: html_monolith | html_split | txt | pdf_text
      start_marker: "CHAPTER I"
      end_marker: "CHAPTER II"
    split_confidence: CERTAIN | PROBABLE | UNCERTAIN
    order_confidence: CERTAIN | PROBABLE | UNCERTAIN
    normalization_events:
      - type: html_tag_strip | italic_loss | footnote_inline | boilerplate_removed | pdf_garble_repaired
        source_fidelity_risk: low | medium | high
        confidence: CERTAIN | PROBABLE | UNCERTAIN
    needs_human_review: false
    review_reason: []
omitted_material:
  - label: gutenberg_license | contents | illustration | front_matter | back_matter
    disposition: excluded | included_as_ch-00 | separate_unassigned
    confidence: PROBABLE
    needs_human_review: true
ambiguous_splits: []                # items raised into the §5 question gate
review:
  status: PENDING | CONFIRMED       # CONFIRMED only after greenlight resolves all ambiguity
  accepted_risks: []
```

---

*Provenance footnote: any `§`-style cross-tree reference in this skill (to the skill spec, DESIGN, or
ADR-006) is **build-time design-pack provenance**, not a runtime dependency. The in-tree body is
**self-sufficient** — everything needed to run this Stage-0 procedure is present here.*
