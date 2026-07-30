# Skill Authoring Blueprint — chapter-materialize

Consolidated from `research/03-skill-authoring-spec.md`. This blueprint reproduces the load-bearing
authoring targets for `laf-adaptation/skills/chapter-materialize/SKILL.md`, its
`resources/boundary-rules.yaml`, and the `source/<slug>/chapter-manifest.yaml` schema.

CRITICAL fidelity note: the 16-row failure-mode table (§C) and the `chapter-manifest.yaml` v1 schema
block (§D) are reproduced BYTE-FOR-BYTE inside fenced blocks below — nothing paraphrased.

---

## 1. Frontmatter shape — `name` + `description` ONLY

Both model skills use exactly two keys. NO `model`, NO `skills`, NO `tools`, NO Mars keys
(`type`, `effort`, etc.). The `description` block `|` is a 3–4 line abstract ending in a
"Load when …" trigger clause. The `skills:` attachment that wires this skill onto
`prep-cordinator` lives in the AGENT frontmatter (spec §6 lines 158–160), NOT here.

Builder's frontmatter (author this verbatim shape):

```yaml
---
name: chapter-materialize
description: |
  The Stage-0 source-materialization procedure for /laf:prep: detect input mode (adopt/folder/file),
  apply multi-signal boundary detection, normalize HTML/PDF to plain text, and emit the confidence-tagged
  source/<slug>/chapter-manifest.yaml + canonical ch-<NN>.txt set. Prompt+YAML only, no runtime (ADR-006);
  check_boundary.py stays the sole script. Load when onboarding a work whose chapters are not yet split.
---
```

---

## 2. SKILL.md section outline (§B) — 13 ordered sections

Each maps to a spec section. "Builder to author" = prose the builder writes; everything else is
carried/derived from the spec.

1. **Frontmatter** — the `name`+`description` block above (verbatim shape).

2. **H1 + Principle line** — `# Chapter Materialize — Stage-0 Source Materialization`. Principle
   (Builder to author, grounded in spec §1 lines 17–23 + §6 lines 170–173): *"Turn whatever `--source`
   resolves to into the canonical `ch-<NN>.txt` set + a confidence-tagged manifest — without guessing.
   Prompt + YAML only; no new runtime; `check_boundary.py` stays the sole script and a validator only
   (ADR-006)."* — This sentence discharges spec §6 lines 159–161 + §11 line 247 and MUST appear.

3. **`## Scope & non-runtime invariant`** (spec §2 N2 line 44, §6 lines 159–161, §11 line 247, §14 risk
   #7 line 289). State: this skill is a *procedure executed by the model inline in the coordinator's
   context* (spec §4 line 76 "executed inline"); it adds **no** script, parser binary, or CLI; the
   `analyst` is NOT repurposed as the splitter (§2 N4 line 45, §4 lines 97–99). One line:
   **"`check_boundary.py` remains the sole script and a validator only; this skill emits no code."**

4. **`## Stage 0.1 — Inventory & source-access declaration`** (spec §4 lines 72–73). Sub-steps: list raw
   inputs (sizes/extensions/sha256); run the `/source-fidelity` **source-access declaration** and
   **ABORT-on-NO-ACCESS FIRST** (unchanged discipline — reference `source-fidelity` Phase 0). Identify
   candidate sets. Populate `raw_sources[]` (role ∈ monolith|chapter_file|front_matter|ignored_duplicate).

5. **`## Stage 0.2 — Detect input mode`** (spec §3 lines 58–65, §4 line 74). Carry the auto-detect
   **precedence** verbatim as an ordered list — load-bearing, must be exact:
   1. `adopt` (Mode C) — `source/<slug>/ch-*.txt` already exists and validates.
   2. `folder` (Mode A) — `--source` is a directory of ≥2 non-canonical per-chapter files.
   3. `file` (Mode B) — `--source` is a single file.
   4. **Ambiguity → HALT-ask, do not guess.** Directory with BOTH split-like files AND a dominating
      monolith (the real `Books/LWW/` case: `-1..-4.html` **and** `…copy*.html`) → `mode_confidence:
      UNCERTAIN` → mode question at the gate. Detection is itself confidence-tagged; PROBABLE/UNCERTAIN
      mode **blocks any `source/` write until resolved** (spec line 65). `--source-mode` operator override
      is honored here (spec §3 line 55).
   Output: `input_mode` + `mode_confidence`.

6. **`## Stage 0.3 — Boundary & plan (NO writes)`** (spec §4 lines 76–78, §6 lines 162–173). The core.
   Two subsections:
   - **`### The five evidence layers`** — carry spec §6 lines 164–168 as an ordered table (layer, signal,
     note). Verbatim layers: (1) TOC/anchor map; (2) body-heading map (`CHAPTER I`, `Chapter 1`,
     `Chapter One`, `<h1>/<h2 class=chapter>`; roman/arabic/spelled); (3) filename map (Mode A) —
     **natural sort, never lexicographic** (`ch-2` before `ch-10`); (4) content sanity (starts with
     expected heading, non-empty body, plausible length, non-overlapping ranges); (5) count reconciliation
     (TOC vs body-heading vs filename counts agree or gate). Point at `resources/boundary-rules.yaml` as
     the declarative pattern source for each layer.
   - **`### Confidence rule (load-bearing)`** — carry spec §6 lines 170–173 VERBATIM and bold it:
     **"CERTAIN requires ≥2 independent agreeing signals and no contradiction."** One strong signal +
     plausible content → **PROBABLE**. Missing/contradictory signals, manual repair, or PDF garble →
     **UNCERTAIN**. **Single-signal boundaries are capped at PROBABLE** (never CERTAIN — spec §13 AC4
     line 273, §14 risk #3 line 285). Every boundary/title/order is a `/source-fidelity`-tagged fact
     (reuse the CERTAIN/PROBABLE/UNCERTAIN vocabulary — this is why the skill imports source-fidelity's
     tags). **No writes in this stage** (plan only).

7. **`## Stage 0.4 — Commit (gated)`** (spec §4 lines 79–81, §10 lines 229–230). State the **deferred-write
   safety invariant** as its own bolded rule: **"No `ch-NN.txt` for a PROBABLE/UNCERTAIN boundary is
   committed before the human resolves it."** CERTAIN chapters materialize immediately as new
   `source/<slug>/ch-<NN>.txt`; raw input retained under `source/<slug>/.raw/`; `chapter-manifest.yaml`
   written with `review.status: PENDING`. Any PROBABLE/UNCERTAIN/collision/mode-ambiguity item →
   recorded as an `ambiguous_splits[]` entry, its write **deferred**.

8. **`## Stage 0.5 — Route to gate`** (spec §4 lines 82–84, §10 lines 224–232). Deferred items + every
   `needs_human_review` item are injected into the existing **§5 question gate** (no new gate/HALT
   machinery — spec §10 line 224). **Greenlight cannot reach CONFIRMED while any is unresolved.** On
   confirm, `prep-cordinator` (not this skill) commits the deferred writes and sets
   `chapter-manifest.review.status: CONFIRMED`. Each ambiguous split allows `[skip] → DEFAULTED` in
   `70-traceability.md` (spec line 227).

9. **`## Format normalization & fidelity`** (spec §8 lines 196–208). HTML → strip tags/scripts/style/nav/
   boilerplate, decode entities, preserve paragraph breaks. PDF → extract text stream, rejoin hyphenated
   wraps, preserve paragraph breaks. Output UTF-8. **No rewording, no reflow, no editorial change** —
   verbatim prose with markup removed. Raw retained at `.raw/` as the fidelity anchor. **Every discard is
   a `normalization_event` with a `source_fidelity_risk` label**; italics-in-titles, verse indentation,
   letters, footnotes, illustrations, page breaks may carry meaning. **High-risk losses block greenlight**
   unless accepted in `50-greenlight.md` (recorded in `70-traceability.md`). Pure tag-strip → CERTAIN;
   structural ambiguity (tables/footnotes/verse) → PROBABLE and surfaced.

10. **`## Idempotency, collisions, backward-compat`** (spec §9 lines 210–221). Three named modes:
    - **Mode C adopt (zero re-split):** if `source/<slug>/ch-*.txt` exists, read titles/ordinals from the
      existing files; write/refresh ONLY `chapter-manifest.yaml` (`provenance.class: ADOPTED`). narnia
      (ch-01..04) + tolkien (ch-01) adopt untouched. Manifest-less existing set adopts with
      `split_confidence: CERTAIN` for existence but `provenance` gaps flagged for review.
    - **Re-run:** read the manifest first; raw+output hashes match → no-op (`review.status: CONFIRMED`
      short-circuits Stage 0). Raw changed but output exists → diff-style replacement PLAN, gated; **never
      overwrite by default.**
    - **Collision:** existing `ch-NN.txt` whose hash differs from a proposed resplit is **never clobbered**
      → HALT-and-ask at the gate (spec §14 risk #2 line 284).

11. **`## Failure modes (release-gating)`** (spec §7 lines 176–194). **Carry the full 16-row table
    VERBATIM** (columns: Failure mode | Detection | Resolution/gate). Do not paraphrase — this is the
    release-gating contract. The 16 rows are enumerated in §C below for the builder's convenience.

12. **`## Manifest output contract`** (spec §5 lines 101–154). END the skill on the fenced
    `chapter-manifest.yaml` v1 schema block (see §D — carry VERBATIM). Precede with the one-line
    non-membership note: **"`chapter-manifest.yaml` is a `source/` sidecar — NOT a numbered package file,
    NOT a `rewrite_phase_reads` member"** (spec §5 line 104, §12 lines 256–257, §15 line 293).

13. **Provenance footnote** (house idiom, per `source-fidelity:103-105`): spec-`§` cites are build-time
    design provenance; the in-tree body is self-sufficient.

---

## 3. Load-bearing rules (consolidated callouts)

### 3.1 Confidence rule (load-bearing)
**"CERTAIN requires ≥2 independent agreeing signals and no contradiction."** One strong signal +
plausible content → **PROBABLE**. Missing/contradictory signals, manual repair, or PDF garble →
**UNCERTAIN**. **Single-signal boundaries are capped at PROBABLE** (never CERTAIN — spec §13 AC4
line 273, §14 risk #3 line 285). Reuses `/source-fidelity` CERTAIN/PROBABLE/UNCERTAIN tags; no new
levels invented.

### 3.2 Mode-detect precedence: adopt > folder > file > ambiguity-HALT
1. `adopt` (Mode C) — `source/<slug>/ch-*.txt` already exists and validates.
2. `folder` (Mode A) — `--source` is a directory of ≥2 non-canonical per-chapter files.
3. `file` (Mode B) — `--source` is a single file.
4. **Ambiguity → HALT-ask, do not guess.** Directory with BOTH split-like files AND a dominating
   monolith → `mode_confidence: UNCERTAIN` → mode question at the gate. PROBABLE/UNCERTAIN mode
   **blocks any `source/` write until resolved**. `--source-mode` operator override honored.

### 3.3 The five evidence layers (spec §6.1–§6.5)
1. **TOC / anchor map.**
2. **Body-heading map** — `CHAPTER I`, `Chapter 1`, `Chapter One`, `<h1>/<h2 class=chapter>`;
   roman/arabic/spelled.
3. **Filename map (Mode A)** — **natural sort, never lexicographic** (`ch-2` before `ch-10`).
4. **Content sanity** — starts with expected heading, non-empty body, plausible length,
   non-overlapping ranges.
5. **Count reconciliation** — TOC vs body-heading vs filename counts agree or gate.

Each layer's declarative patterns live in `resources/boundary-rules.yaml`.

### 3.4 Deferred-write safety invariant
**"No `ch-NN.txt` for a PROBABLE/UNCERTAIN boundary is committed before the human resolves it."**
CERTAIN chapters materialize immediately; raw retained under `source/<slug>/.raw/`; manifest written
`review.status: PENDING`. Any PROBABLE/UNCERTAIN/collision/mode-ambiguity item → `ambiguous_splits[]`
entry, write **deferred**. `review.status: CONFIRMED` set by `prep-cordinator` on greenlight only.

---

## C. Failure-mode table — 16 rows (VERBATIM from spec §7)

Builder: paste this table into SKILL.md §11 unchanged.

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

Real-case anchors to keep intact: the `-1..-4.html` + `…copy*.html` `Books/LWW/` case (rows
"Split set incomplete", "Monolith duplicates", "Mode ambiguity").

---

## D. `chapter-manifest.yaml` v1 schema — VERBATIM authoring target (spec §5)

`schema_version: laf.chapter_manifest.v1`. **Source-side sidecar** (BUILD-NEW, outside the Rule-F
hash-pin glob), co-located with the chapters it indexes. **NOT** a numbered package file; **NOT** a
`rewrite_phase_reads` member. Builder authors this as (a) the schema block at the end of SKILL.md and
(b) the concrete emission target for `source/<slug>/chapter-manifest.yaml`.

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

### D.1 Schema field notes the builder must honor (cross-cut from §7–§10)
- Confidence enums (`mode_confidence`, `title_confidence`, `split_confidence`, `order_confidence`,
  per-`normalization_event.confidence`) reuse `/source-fidelity`'s exact vocabulary
  (CERTAIN/PROBABLE/UNCERTAIN). Do not invent new levels.
- **Every chapter row MUST carry** confidence + provenance + `needs_human_review` (AC5 spec lines 274–275,
  release-blocker #4 line 286). A row missing any of the three is a release-blocking defect.
- **Every markup discard MUST be a `normalization_event` with a `source_fidelity_risk` label** (AC5 line
  275, release-blocker #5 line 287).
- `provenance.class` enum is `MATERIALIZED | ADOPTED` (Mode C adopt writes `ADOPTED`; §9 line 213).
- `review.status: CONFIRMED` is set by `prep-cordinator` on greenlight, NOT by this skill. The skill
  emits `PENDING`.

---

## E. `resources/boundary-rules.yaml` — declarative signal ruleset skeleton

The SKILL.md carries the PROCEDURE + confidence rule + failure table; **this YAML carries the
DECLARATIVE patterns** each evidence layer matches on. Data, not code (ADR-006 — no runtime; the model
reads these patterns, `check_boundary.py` does NOT). Five top-level keys = the five evidence layers +
a confidence-rule mirror. All regex/pattern content is "Builder to author"; the shape is fixed.

```yaml
# resources/boundary-rules.yaml — declarative signal ruleset for chapter-materialize.
# ADR-006: data only, no runtime. The model applies these patterns; check_boundary.py does NOT read this.
schema_version: laf.boundary_rules.v1

# Layer 1 — TOC / anchor map (spec §6.1)
toc_anchor_map:
  # Builder to author: patterns for TOC list items linking to in-doc anchors,
  #   e.g. roman/arabic list entries with href="#chapNN".
  html_anchor_patterns: []          # e.g. ['<a\s+href="#(chap\d+)">']
  toc_list_container_hints: []      # e.g. ['id="toc"', 'class="contents"']
  min_entries_to_trust: 2

# Layer 2 — body heading map (spec §6.2) — roman / arabic / spelled
body_heading_map:
  roman:   { pattern: 'Builder to author', examples: ['CHAPTER I', 'CHAPTER XVII'] }
  arabic:  { pattern: 'Builder to author', examples: ['Chapter 1', 'CHAPTER 17'] }
  spelled: { pattern: 'Builder to author', examples: ['Chapter One', 'Chapter Seventeen'] }
  html_heading_hints: []            # e.g. ['<h1', '<h2 class="chapter"']
  case_insensitive: true
  must_be_isolated_line: true       # spec §7 "Boundary inside poem/quote" — reject non-structural matches

# Layer 3 — filename map (Mode A) — NATURAL sort, never lexicographic (spec §6.3)
filename_map:
  sort: natural                     # ch-2 before ch-10; NEVER lexicographic
  ordinal_extract_patterns: []      # Builder to author: e.g. '-(\d+)\.html$', 'ch-?0*(\d+)'
  canonical_output_pattern: 'ch-<NN>.txt'   # zero-padded; order == numeric id
  ignore_globs: []                  # e.g. duplicate 'copy*' monoliths handled by Layer 5

# Layer 4 — content sanity (spec §6.4)
content_sanity:
  must_start_with_expected_heading: true
  min_body_chars: 1                 # Builder to author: a real plausible-length floor
  plausible_length_range: { min_chars: 0, max_chars: 0 }   # Builder to author
  ranges_must_not_overlap: true

# Layer 5 — count reconciliation (spec §6.5)
count_reconciliation:
  sources: [toc, body_heading, filename]
  rule: all_present_counts_must_agree_else_gate
  on_mismatch: raise_ambiguous_split          # → §5 question gate

# Confidence rule mirror (spec §6, lines 170–173) — authoritative copy lives in SKILL.md
confidence_rule:
  CERTAIN_requires_min_agreeing_signals: 2    # AND no contradiction
  single_signal_cap: PROBABLE                 # single-signal boundary NEVER CERTAIN
  uncertain_triggers: [missing_signal, contradictory_signal, manual_repair, pdf_garble]
```

Builder notes:
- Keep NON-executable and hint-only; read by the model, never by `check_boundary.py`.
- Rule E (no upstream filename collision): `boundary-rules.yaml` is a novel name.
- The `confidence_rule` block is a convenience mirror; the SKILL.md §B6 copy is authoritative (state
  this in a comment so the two never drift into disagreement).

---

## F. The 10 invariants the builder must not violate (all spec-cited)

1. Skill frontmatter = `name` + `description` ONLY (CLAUDE.md §3; both model skills).
2. This skill is a model-executed PROCEDURE; **no new script, parser, or CLI** — `check_boundary.py` stays
   the sole script and validator only (spec §2 N2 line 44, §6 lines 160–161, §11 line 247, ADR-006).
3. **CERTAIN requires ≥2 agreeing signals; single-signal capped at PROBABLE** (spec §6 lines 170–173, AC4
   line 273, risk #3 line 285).
4. **Deferred-write safety invariant:** no `ch-NN.txt` for a non-CERTAIN boundary committed before human
   resolution (spec §4 lines 79–81, §10 lines 229–230, AC4 line 272).
5. Mode-detect precedence adopt > folder > file > **ambiguity-HALT** (spec §3 lines 58–65).
6. Manifest is a `source/` sidecar — NOT numbered package file, NOT in `rewrite_phase_reads` (spec §5
   line 104, §12, §15).
7. Every chapter row carries confidence + provenance + `needs_human_review`; every discard is a
   `normalization_event` with a fidelity-risk label (spec §5, AC5 lines 274–275).
8. Reuse `/source-fidelity` CERTAIN/PROBABLE/UNCERTAIN tags; do not invent new confidence levels.
9. Failure-mode table carried VERBATIM (16 rows, spec §7).
10. `resources/boundary-rules.yaml` is data-only, hint-only, never read by the boundary script.
