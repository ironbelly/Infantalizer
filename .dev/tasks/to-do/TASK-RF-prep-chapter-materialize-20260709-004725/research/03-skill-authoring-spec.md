# Research 03 — Skill Authoring Spec (chapter-materialize + manifest schema + failure modes)

Status: Complete

Scope: authoring blueprint for (a) `laf-adaptation/skills/chapter-materialize/SKILL.md`,
(b) `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml`,
(c) `source/<slug>/chapter-manifest.yaml` schema.
Source of truth: `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md` §5–§10
(read in full; line cites below).

Deliverables directory (Builder to create): `laf-adaptation/skills/chapter-materialize/` — confirmed
NOT to exist yet (`ls` returned "No such file or directory"). Sibling skill dirs live under
`laf-adaptation/skills/` (18 present: adaptation-rules … writing-staffing).

---

## A. House-style facts the builder MUST match (from the two model skills)

Read: `laf-adaptation/skills/source-fidelity/SKILL.md` (NATIVE, the confidence vocabulary the manifest
reuses) and `laf-adaptation/skills/adaptation-safety/SKILL.md` + `resources/children.md` (BUILD-NEW with
a `resources/` file — the SKILL.md + resources/ pattern). Also spot-checked `prep/SKILL.md:1-20`.

### A.1 Frontmatter shape — `name` + `description` ONLY

Both model skills use exactly two keys. Verbatim (`source-fidelity/SKILL.md:1-8`):

```yaml
---
name: source-fidelity
description: |
  The v2.0 anti-hallucination protocol for source analysis. Mandates CERTAIN/PROBABLE/UNCERTAIN
  confidence tags on every extracted fact ...
---
```

`adaptation-safety/SKILL.md:1-8` is identical in shape (`name:` scalar, `description:` block `|`).
This matches the CLAUDE.md rule (`laf-adaptation/CLAUDE.md` §3): *"Skills: `name` + `description` only."*
NO `model`, NO `skills`, NO `tools`, NO Mars keys (`type`, `effort`, etc.). The description block `|` is
a 3–4 line abstract that ends with a "Load when …" trigger clause. **The `skills:` attachment that wires
this skill onto `prep-cordinator` lives in the AGENT frontmatter (spec §6 line 158–160), NOT here.**

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

### A.2 Section conventions

- **H1 title line** = human name + one-line gloss (e.g. `# Source Fidelity — v2.0 Pragmatic Verification
  Protocol`; `# Adaptation Safety — 6-section rubric`). Follow with a one-line **Principle:** or purpose
  sentence.
- **Section headers**: `source-fidelity` uses `## Phase 0 …`, `## Phase 1 …` (numbered *phases* for a
  procedure). `adaptation-safety` uses `## Section 1 — …` (numbered *sections* for a rubric). Pick
  procedure-phase numbering for chapter-materialize because it IS a procedure — recommend
  `## Stage 0.1 …` through `## Stage 0.5 …` mirroring spec §4 sub-steps (line 72–84), so the skill's
  headers map 1:1 to the coordinator's Stage-0 sub-steps.
- **Tables** are the house workhorse: `source-fidelity` uses a confidence-tag table and an
  observable-test table; `adaptation-safety` uses per-section checklists + an aggregation code block +
  a fenced verdict-contract YAML. chapter-materialize should carry: the evidence-layer table, the
  failure-mode table (spec §7, 16 rows — carry verbatim), and the manifest-schema fenced YAML.
- **Fenced YAML output-contract block near the end** is the established close: `source-fidelity` ends on
  its `work/analysis/ch-<NN>.yaml` schema block (lines 53–88); `adaptation-safety` ends on its `verdict`
  contract block (lines 90–108). chapter-materialize should likewise END on the `chapter-manifest.yaml`
  schema block (see §D below), preceded by the boundary/confidence rules.
- **Provenance/self-sufficiency footnote** is idiomatic. `source-fidelity:103-105` and CLAUDE.md both
  state design-pack `§` cites are build-time provenance and the in-tree body is self-sufficient. Add the
  same footnote so a reader never treats spec-`§` cites as runtime deps.

### A.3 How they reference resources/

`adaptation-safety/SKILL.md` is the SKILL.md + resources/ exemplar. Key facts:
- The rubric SKILL.md **gates**; the `resources/children.md` doc **informs** — the SKILL.md explicitly
  distinguishes them (`children.md:4-6`: *"This doc **informs** the writer; it is distinct from the
  `/adaptation-safety` **rubric**, which **gates**"*). So resources/ = reference data the SKILL.md's
  procedure consults, not a duplicate of the procedure.
- Reference style is by relative path in prose (e.g. `resources/children.md`, `resources/ya.md` named in
  `adaptation-safety/SKILL.md:16`). For chapter-materialize, the SKILL.md refers to
  `resources/boundary-rules.yaml` the same way: *"the declarative signal ruleset in
  `resources/boundary-rules.yaml`"* — the SKILL.md carries the PROCEDURE + confidence rule + failure
  table; the YAML carries the DECLARATIVE signal patterns the model applies.
- **Boundary-contract note (CLAUDE.md):** a `resources/` file under a NATIVE skill is a NATIVE addition,
  must not collide with an upstream filename (Rule E), and (for SKILL.md) is hash-pinned by Rule F.
  `resources/boundary-rules.yaml` is NOT under the Rule-F glob (glob = `agents/*.md` +
  `skills/**/SKILL.md` only), so only `chapter-materialize/SKILL.md` gets a Rule-F manifest row + hash;
  the `.yaml` resource is manifested separately per the `resources/**` superset rule (CLAUDE.md "Why
  VENDOR.md has more rows"). Researcher-02 owns the exact VENDOR.md rows.

### A.4 Prose register

Terse, declarative, second-person-imperative or definitional. Load-bearing rules are **bolded inline**
("**CERTAIN requires ≥2 independent agreeing signals**"). Confidence tags are ALL-CAPS
(CERTAIN/PROBABLE/UNCERTAIN). Contracts are machine-parseable fenced blocks. No hedging, no filler, no
meta-narration. Sentences are short. Every rule a downstream reader branches on is stated once, exactly,
and cross-referenced by `§`/path rather than restated.

---

## B. OUTLINE for `chapter-materialize/SKILL.md` (Builder to author from this)

Ordered sections. Each maps to a spec section (cited). "Builder to author" = prose the builder writes;
everything else is carried/derived from the spec.

1. **Frontmatter** — the `name`+`description` block in §A.1 above (verbatim shape).

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

**Coverage self-check vs the researcher brief:** mode-detect precedence (§B5) ✓; 5 evidence layers
(§B6) ✓; CERTAIN-≥2-signals / single-signal-capped-PROBABLE (§B6) ✓; Stage-0 sub-steps 0.1–0.5
(§B4–B8) ✓; deferred-write safety invariant (§B7) ✓; failure-mode handling (§B11) ✓; `check_boundary.py`
sole-script/validator + no new runtime ADR-006 (§B3 + Principle §B2) ✓.

---

## C. Failure-mode table — 16 rows to carry VERBATIM (spec §7, lines 178–194)

Builder: paste this table into SKILL.md §11 unchanged. (Reproduced here so the builder has it inline.)

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

Real-case anchors the builder should keep intact: the `-1..-4.html` + `…copy*.html` `Books/LWW/` case
(rows "Split set incomplete", "Monolith duplicates", "Mode ambiguity") maps to spec §3 lines 62–64 and
AC2 (spec §13 lines 270–271, release-blocker #1 §14 line 283).

---

## D. `chapter-manifest.yaml` v1 schema — VERBATIM authoring target (spec §5, lines 106–154)

`schema_version: laf.chapter_manifest.v1`. **Source-side sidecar** (BUILD-NEW, outside the Rule-F
hash-pin glob), co-located with the chapters it indexes. **NOT** a numbered package file; **NOT** a
`rewrite_phase_reads` member (spec §5 line 104; reinforced §12 lines 256–257, §15 line 293). Builder
authors this as (a) the schema block at the end of SKILL.md and (b) the concrete emission target for
`source/<slug>/chapter-manifest.yaml`.

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
  (CERTAIN/PROBABLE/UNCERTAIN) — `source-fidelity/SKILL.md:14-19`. Do not invent new levels.
- **Every chapter row MUST carry** confidence + provenance + `needs_human_review` (AC5 spec lines 274–275,
  release-blocker #4 line 286). A row missing any of the three is a release-blocking defect.
- **Every markup discard MUST be a `normalization_event` with a `source_fidelity_risk` label** (AC5 line
  275, release-blocker #5 line 287).
- `provenance.class` enum is `MATERIALIZED | ADOPTED` (Mode C adopt writes `ADOPTED`; §9 line 213).
- `review.status: CONFIRMED` is set by `prep-cordinator` on greenlight, NOT by this skill (spec §4 line
  84, §10 line 232). The skill emits `PENDING`.

---

## E. `resources/boundary-rules.yaml` — declarative signal ruleset skeleton (Builder to flesh out)

Purpose (spec §6 line 158, §11 line 239 "declarative signal ruleset"): the SKILL.md carries the
PROCEDURE + confidence rule + failure table; **this YAML carries the DECLARATIVE patterns** each evidence
layer matches on. It is data, not code (ADR-006 — no runtime; the model reads these patterns and applies
them). This mirrors the adaptation-safety split where `resources/children.md` is reference data the
SKILL.md consults. The five top-level keys are the five evidence layers (spec §6 lines 164–168) plus a
confidence-rule mirror. **All regex/pattern content below is "Builder to author"** — the shape is fixed by
the spec's evidence layers; the concrete patterns are the builder's to fill.

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
- Keep this file NON-executable and hint-only; it is read by the model, never by `check_boundary.py`
  (ADR-006 — spec §2 N2 line 44, §11 line 247).
- Rule E (no upstream filename collision): `boundary-rules.yaml` is a novel name — only
  `chapter-materialize/` will hold it. Researcher-02 owns the definitive Rule-E / VENDOR check.
- The `confidence_rule` block is a convenience mirror; the SKILL.md §B6 copy is authoritative (state this
  in a comment so the two never drift into disagreement).

---

## F. Summary of invariants the builder must not violate (all spec-cited)

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

---

## G. Open items / hand-offs (not this researcher's scope)
- Exact VENDOR.md rows + Rule-E/Rule-F manifest entries for the new SKILL.md and `.yaml` → Researcher-02.
- The `prep-cordinator.md` `skills:` frontmatter line + Stage-0 procedure paragraph, `prep/SKILL.md`
  Stage-0 note, `path-contract.md` write-ownership rows → Researcher-01 (edit loci) + Researcher-04
  (task phases). This researcher confirms only that the wiring is a **single additive `skills:` line**
  (spec §6 lines 158–160) and that the manifest read-set is UNCHANGED (spec §12 line 255).
