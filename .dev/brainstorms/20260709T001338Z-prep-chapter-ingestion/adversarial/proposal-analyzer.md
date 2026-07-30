# Proposal: `/laf:prep` v-next — adversarial analyzer spec for chapter ingestion

## Core stance

`/laf:prep` should own chapter materialization, but only as an explicit pre-analysis stage with a hard human review gate for any non-CERTAIN boundary. Splitting is source-fidelity extraction, not clerical cleanup: the framework must treat chapter boundaries, titles, order, and omitted matter as confidence-tagged facts with provenance. The release should block on any design that can silently guess a boundary, overwrite an existing `source/<slug>/ch-<NN>.txt`, or discard markup without a declared fidelity loss record.

## Positions on OQ1-OQ6

- **OQ1 ownership:** `/laf:prep` owns materialization. A separate `/laf:ingest` would create another handoff where uncertainty can be dropped. Internally, prep adds Stage 0: `chapter_materialization`, owned by `prep-cordinator`, before current two-track work-level prep.
- **OQ2 granularity:** keep prep analysis work-level for v-next; do not jump to per-chapter analysis yet. The manifest prepares rewrite to iterate chapters, but current `20-analysis-work-level.yaml` remains the source-fidelity analysis product. Per-chapter analysis can be a later rewrite/pre-rewrite stage.
- **OQ3 split mechanism:** no new runtime and no splitter script. Use a prompt-driven, YAML-declared procedure in the native prep skill: enumerate candidate boundaries, cross-check them against TOC/anchors/headings/filename order, tag confidence, then write only after gate approval. The one allowed script remains `check_boundary.py` only.
- **OQ4 manifest placement:** add a sidecar `laf-adaptation/source/<slug>/chapter-manifest.yaml` as canonical chapter-source metadata, plus a summary reference inside `work/prep/<slug>/40-prep-brief.md` and audit details in `70-traceability.md`. Do **not** add a ninth fixed prep package file. Future `/laf:rewrite` may extend its hardcoded read-set to read the source sidecar, but v-next prep must not break the current frozen three-file set.
- **OQ5 normalization:** normalize HTML/PDF/txt to UTF-8 plain text conservatively. Markup loss is expected and must be tracked by `/source-fidelity`: headings, italics, block quotes, poems, footnotes, page breaks, illustrations, anchors, and boilerplate removals become `normalization_events` with confidence and risk.
- **OQ6 idempotency/gating:** default re-runs are no-overwrite. Existing canonical chapters are adopted only when hashes match the manifest or the operator explicitly approves a replacement plan. Any PROBABLE or UNCERTAIN chapter, count, order, title, omitted-matter, or normalization-loss item is injected into the existing question gate and blocks greenlight until answered or explicitly accepted.

## Command surface and mode auto-detection

Proposed surface:

```text
/laf:prep "<title>" --source <path-or-url> [--slug <slug>] [--ingest-mode auto|folder|single|adopt-existing] [--chapter-count <N>] [--allow-overwrite]
```

`--source` may be a directory, a single local file, or a fetched URL materialized to local raw storage. Auto-detection is deliberately conservative:

1. If `laf-adaptation/source/<slug>/ch-*.txt` already exists, choose `adopt-existing` unless `--source` explicitly names a new raw source.
2. If `--source` is a directory with multiple plausible text/html files and no monolithic file dominates by size, choose **Mode A folder ingest**.
3. If `--source` is one file, choose **Mode B single-file split**.
4. If a directory contains both split chapter-like files and monolithic copies, as the LWW folder does, auto-detection must not guess. It emits an ambiguity question listing candidate sets and asks the operator to choose `folder` or `single`.

Detection can misfire when filenames are misleading (`copy 2.html`, `-1.html`), chapter files omit headings, a folder contains front matter plus chapters, or one monolithic file sits alongside exports. Therefore detection itself gets `mode_confidence: CERTAIN|PROBABLE|UNCERTAIN`; PROBABLE/UNCERTAIN detection enters the human gate before any source writes.

## Pipeline stage and owner

Add native prep Stage 0 before current §3:

1. **Stage 0.1 Source inventory:** `prep-cordinator` lists raw inputs, identifies candidate sets, records byte sizes, extensions, and provenance.
2. **Stage 0.2 Boundary candidate extraction:** `analyst` or a new native `chapter-materializer` procedure under prep inspects TOC, anchors, heading patterns, filename numbers, and text starts/ends.
3. **Stage 0.3 Normalization dry-run:** produce proposed plain-text chapters in memory conceptually; record transformations and omitted regions.
4. **Stage 0.4 Human gate:** ask about all uncertain mode, order, count, boundary, title, omitted matter, overwrite, and markup-loss decisions.
5. **Stage 0.5 Materialize:** `prep-cordinator` writes `source/<slug>/ch-<NN>.txt` and `source/<slug>/chapter-manifest.yaml` only after gate clearance.
6. Continue current work-level prep using the materialized chapter set as the text source collection.

## Manifest placement and schema

Canonical path: `laf-adaptation/source/<slug>/chapter-manifest.yaml`. This is a source sidecar, not canon and not an adaptation draft. `work/prep/<slug>/70-traceability.md` links to it; `40-prep-brief.md` summarizes chapter count and any accepted risks.

Schema:

```yaml
schema_version: laf.chapter_manifest.v1
work_slug: narnia
title: The Lion, the Witch and the Wardrobe
materialized_at: 2026-07-09T00:00:00Z
ingest_mode: folder|single|adopt-existing
mode_confidence: CERTAIN|PROBABLE|UNCERTAIN
raw_sources:
  - path: Books/LWW/...
    role: monolith|chapter_file|front_matter|ignored_duplicate
    sha256: "..."
    mime_hint: text/html
normalization_policy:
  output_format: utf-8-plain-text
  markup_preserved_as_text: [chapter_heading, chapter_title]
  markup_discarded: [html_tags, anchors, css]
chapters:
  - id: ch-01
    index: 1
    title: Lucy Looks into a Wardrobe
    title_confidence: CERTAIN
    output_path: laf-adaptation/source/narnia/ch-01.txt
    output_sha256: "..."
    source_provenance:
      raw_path: Books/LWW/The Lion...html
      source_kind: html_monolith|html_split|txt|pdf_text
      start_marker: "CHAPTER I"
      end_marker: "CHAPTER II"
      raw_line_start: 227
      raw_line_end: 484
      anchor_start: chap01
    split_confidence: CERTAIN|PROBABLE|UNCERTAIN
    order_confidence: CERTAIN|PROBABLE|UNCERTAIN
    normalization_events:
      - type: html_tag_strip|italic_loss|footnote_inline|boilerplate_removed|pdf_garble_repaired
        confidence: CERTAIN|PROBABLE|UNCERTAIN
        source_fidelity_risk: low|medium|high
    needs_human_review: true|false
    review_reason: []
omitted_material:
  - label: Project Gutenberg license/header|contents|illustration|front matter|back matter
    disposition: excluded|included_in_chapter|separate_unassigned
    confidence: CERTAIN|PROBABLE|UNCERTAIN
    needs_human_review: true|false
review:
  status: PENDING|CONFIRMED
  accepted_risks: []
```

## Split mechanism under ADR-006

The split procedure is a written native skill protocol, not executable parser logic. It uses evidence layers:

- **Layer 1 TOC/anchor map:** table of contents entries and links, e.g. `I. <a href="#chap01">...` through `XVII` in the LWW monolith.
- **Layer 2 body heading map:** repeated heading blocks, e.g. `<h3>CHAPTER I</h3>` followed by `<h4><i>Lucy Looks into a Wardrobe</i></h4>`.
- **Layer 3 filename map:** Mode A filenames parsed with natural sort, not lexicographic sort.
- **Layer 4 content sanity:** each chapter starts with expected heading/title, non-empty body, plausible length, and non-overlapping ranges.
- **Layer 5 count reconciliation:** expected count from TOC, body headings, filenames, and optional `--chapter-count` must agree or be gated.

Confidence rules: CERTAIN requires at least two independent signals agreeing (TOC+body, filename+heading) and no contradictions. PROBABLE has one strong signal plus plausible content. UNCERTAIN has missing/contradictory signals, manual repair, or PDF garble.

## Failure-mode table

| Failure mode | Symptom | Detection | Resolution/gate |
|---|---|---|---|
| HTML boilerplate mistaken as chapter | first output contains title page/license/CSS | first chapter begins before first body heading; high tag/metadata density | exclude as front matter only after human confirmation if not matched to TOC |
| TOC entries split as chapters | tiny chapters containing only linked titles | candidate range before first body heading, anchor-only content | classify as contents; gate if no body headings found |
| Missing chapter heading | jump from Chapter IV to VI | count gap in roman/arabic sequence | UNCERTAIN; ask operator whether chapter is missing, merged, or heading variant |
| Duplicate heading | two `CHAPTER I` markers | duplicate normalized chapter number | block write; ask which marker is real or whether front matter repeats title |
| Unnumbered prologue/epilogue | text before Chapter I or after final chapter | non-boilerplate prose outside chapter ranges | gate disposition: ch-00/prologue, attach to ch-01, omit, or back matter |
| `Chapter One` vs `CHAPTER I` | pattern mismatch | heading map supports roman, arabic, spelled numbers; unmatched headings listed | PROBABLE/UNCERTAIN depending corroboration; ask if count differs |
| Numbered-only headings | file starts `I` or `1` | short centered/isolated line plus TOC match | require title/count corroboration; otherwise human review |
| Footnotes/illustrations lost | markup contains `footnote`, `img`, captions | normalization event scan | gate medium/high fidelity risk; decide inline text, omit, or separate note |
| PDF extraction garble | broken words, ligatures, headers repeated | high OCR-garble indicators, page headers inside prose | UNCERTAIN; block greenlight until operator accepts or supplies cleaner source |
| Multi-file sort wrong | `ch-10` before `ch-2` | compare lexicographic vs natural sort; heading sequence mismatch | natural sort; if headings contradict filenames, ask |
| Split files not complete | only `-1..-4.html` present but TOC says 17 chapters | file count vs expected count mismatch | block Mode A unless operator confirms partial prep scope |
| Monolith duplicates | `copy.html`, `copy 2.html` identical | hash duplicates | choose one canonical raw source; record others as ignored duplicates |
| Existing source collision | `source/<slug>/ch-01.txt` already exists | path exists before write | adopt if hash matches manifest; otherwise require explicit overwrite plan |
| Boundary cuts inside poem/quote | next heading-like string appears in prose | candidate heading not isolated/structural | reject weak marker; if ambiguous mark UNCERTAIN |
| Back matter swallowed by final chapter | license appears after final chapter | boilerplate/license markers after final body | omit as back matter; gate if non-boilerplate prose exists |

## Format normalization and source-fidelity risk

Plain text is acceptable only as an adaptation input, not as a claim that formatting was irrelevant. `/source-fidelity` must cover the loss by requiring: raw-source provenance, output hashes, transformation event inventory, and fidelity-risk labels. Italics in titles, verse indentation, letters, footnotes, illustrations, and page breaks may carry meaning. If stripped, the manifest must say so. High-risk losses block greenlight unless the operator accepts them in `50-greenlight.md` and `70-traceability.md` records the accepted risk.

## Idempotency, re-run, collisions, backward compatibility

Re-runs first read `chapter-manifest.yaml` if present. If raw-source hashes and output hashes match, the stage is a no-op. If raw changed but output exists, produce a diff-style replacement plan and gate it; never overwrite by default. Existing `source/narnia/ch-01..04.txt` or `source/tolkien/ch-01.txt` without a manifest are adopted as `ingest_mode: adopt-existing` with `split_confidence: CERTAIN` only for file existence and `provenance_confidence: UNCERTAIN` until raw provenance is supplied. Partial existing chapter sets are allowed only as partial scope with explicit human confirmation.

## Low-confidence gate placement

Low confidence enters twice: immediately after Stage 0.3, before materialization, and again in the normal §5 question gate before greenlight. The first gate prevents writing guessed chapter files. The second gate prevents downstream prep/rewrite from treating accepted-but-risky materialization as invisible. Any chapter row with `needs_human_review: true` blocks Stage 0.5; any accepted risk is copied into `50-greenlight.md` so greenlight confirms source-access, chapter count, boundary confidence, overwrite decisions, and normalization-loss acceptance.

## Boundary-contract compliance

This is native prep procedure and native resource schema only. It edits no adopted bodies, adds no runtime, and does not change `check_boundary.py`. `prep-cordinator` remains the writer of prep artifacts and source materialization outputs; `chronicler` still does not write during prep. `source/` is not transformed in place: raw sources remain external/raw; canonical `source/<slug>/ch-<NN>.txt` files are new materialized read-only references.

## `path-contract.md` deltas

Update the contract to add a **source sidecar** section, not a ninth prep file:

- canonical chapter files: `laf-adaptation/source/<slug>/ch-<NN>.txt`;
- canonical manifest: `laf-adaptation/source/<slug>/chapter-manifest.yaml`;
- writer: `prep-cordinator` during Stage 0;
- consumer: prep human audit now, future rewrite chapter driver later;
- `rewrite_phase_reads` remains the current three prep files for v-next, with a note that rewrite may additionally consult the source manifest when chapter iteration is implemented.

## Release-blocking risks

1. Any auto mode that chooses between split-folder and monolith when both are present.
2. Any write path that overwrites existing canonical source without explicit approval.
3. Any splitter that allows single-signal CERTAIN boundaries.
4. Any manifest lacking per-chapter confidence, provenance, and `needs_human_review`.
5. Any normalization policy that strips footnotes/illustrations/poetry/italics without recording fidelity risk.
6. Any design that expands the prep fixed 8-file package or silently changes the current rewrite read-set before rewrite is updated.
7. Any implementation requiring a second script, parser CLI, or adopted-body edit.
