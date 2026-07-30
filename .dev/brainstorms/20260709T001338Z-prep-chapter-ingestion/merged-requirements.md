---
topic: "Next version of /laf:prep — chapter materialization (folder ingest OR single-file split)"
domain: architecture
strategy: systematic
depth: standard
proposals: 3
models: [claude-opus-4-8, gpt-5.5, glm-5.2]
convergence_score: 0.86
adversarial_status: pass
created: 2026-07-09T00:13:38Z
---

# Merged Requirements — `/laf:prep` v-next: Chapter Materialization

## 1. Summary

`/laf:prep` gains a **Stage 0: Source Materialization** that turns whatever `--source` resolves to — a
folder of per-chapter files (**Mode A**), a single monolithic file (**Mode B**), or an already-split
`source/<slug>/` set (**Mode C, adopt**) — into the canonical `source/<slug>/ch-<NN>.txt` set plus a
first-class, confidence-tagged **`source/<slug>/chapter-manifest.yaml`** sidecar. No new command, no new
script/runtime, no adopted-body edit, and **the frozen `rewrite_phase_reads` set is unchanged**. Ambiguous
splits route to the existing question/greenlight gate; no `ch-NN.txt` for a non-CERTAIN boundary is
committed before human confirmation.

This spec is intentionally scoped to **materialization + manifest at work-level analysis granularity**.
Per-chapter *analysis* and per-chapter *rewrite iteration* are explicitly out of scope and handed to the
follow-on rewrite brainstorm (`rewrite-brainstorm-prompt.md`).

## 2. Goals & Non-Goals

**Goals**
- G1. One `/laf:prep` run materializes the canonical chapter set from Mode A / B / C with no manual pre-split.
- G2. Emit a first-class chapter manifest carrying, per chapter: id, title, order, source provenance,
  output hash, and split/title confidence — plus mode/normalization/omitted-matter records.
- G3. Preserve every hard contract: 8-file package, frozen 3-file `rewrite_phase_reads`, write-ownership,
  `check_boundary.py` green, one script, `source/` read-only-after-materialize (new files only).
- G4. Route all non-CERTAIN decisions to the existing human question/greenlight gate; never silently guess.
- G5. Backward compatible: existing `source/narnia/ch-01..04.txt` and `source/tolkien/ch-01.txt` are
  adopted with **zero re-split**.

**Non-Goals**
- N1. No per-chapter source-fidelity analysis in prep (stays `granularity=work`). → rewrite spec.
- N2. No new command (`/laf:ingest` rejected). No second script / parser binary / runtime (ADR-006).
- N3. No 4th `rewrite_phase_reads` entry and no 9th numbered package file.
- N4. No adopted-body edit; the analyst is **not** repurposed as the splitter.

## 3. Command Surface

```
/laf:prep "<title>" [--source <path-or-url>] [--source-mode auto|folder|file|adopt]
```

- `--source` unchanged and still REQUIRED (elicited if omitted); may resolve to a **directory**, a
  **single file**, or an already-split **`source/<slug>/`** set; a URL is fetched to `.raw/` first.
- `--source-mode` (NEW, optional, default `auto`) — operator override for when auto-detect is ambiguous.
- `argument-hint`: `"<title>" [--source <path-or-url>] [--source-mode auto|folder|file|adopt]`.

**Auto-detection precedence (conservative — must not guess):**
1. `adopt` — `source/<slug>/ch-*.txt` already exists and validates → Mode C (backward compat).
2. `folder` (Mode A) — `--source` is a directory of ≥2 non-canonical per-chapter files.
3. `file` (Mode B) — `--source` is a single file.
4. **Ambiguity → HALT-ask, do not guess.** If a directory contains *both* split chapter-like files and a
   dominating monolith (the real `Books/LWW/` case: `-1..-4.html` **and** `...copy*.html`), auto-detect
   emits `mode_confidence: UNCERTAIN` and raises a mode question at the gate. Detection itself is
   confidence-tagged; PROBABLE/UNCERTAIN mode blocks any `source/` write until resolved.

## 4. Pipeline: Stage 0 — Source Materialization

Inserted **before** the current §3 two-track analysis, owned by `prep-cordinator` (NATIVE orchestrator;
`laf_sha256 = —`, so body edits are boundary-clean). Sub-steps:

- **0.1 Inventory** — list raw inputs (sizes, extensions, hashes); identify candidate sets; run the
  `/source-fidelity` source-access declaration and **ABORT-on-NO-ACCESS** first (unchanged discipline).
- **0.2 Detect mode** — §3 precedence → `input_mode` + `mode_confidence`.
- **0.3 Boundary/plan** — dispatch the NEW NATIVE skill `chapter-materialize` (executed inline in the
  coordinator's context) to build a chapter **plan**: candidate boundaries, titles, order, per-boundary
  confidence, normalization events, omitted-matter dispositions. **No writes yet.**
- **0.4 Commit (gated)** — materialize **CERTAIN** chapters immediately as new `source/<slug>/ch-<NN>.txt`;
  retain raw input under `source/<slug>/.raw/`; write `chapter-manifest.yaml`. Any
  **PROBABLE/UNCERTAIN/collision/mode-ambiguity** item is recorded as an `ambiguous_split` and its
  `ch-NN.txt` write is **deferred** to greenlight.
- **0.5 → gate** — deferred items are injected into the existing **§5 question gate**; **greenlight cannot
  reach CONFIRMED** while any is unresolved; on confirm, `prep-cordinator` commits the deferred writes and
  sets `chapter-manifest.review.status: CONFIRMED`.

Stage sequence:
```
STAGE 0  materialize chapters + chapter-manifest.yaml            [NEW]
STAGE 1  §2 challenge taxonomy → 10-challenges.yaml              (unchanged)
STAGE 2  §3 two-track work-level analysis → 00/20               (unchanged; reads materialized set)
STAGE 3  §4 mapping → 30                                         (unchanged)
STAGE 4  §5 question gate  ← also receives Stage-0 ambiguous_splits   (EXTENDED)
STAGE 5  §6 greenlight     ← ratifies manifest; commits deferred writes (EXTENDED)
STAGE 6  §7 handoff / §8 traceability                            (unchanged)
```

**Separation of concerns:** `chapter-materialize` owns boundary detection + normalization; the `analyst`
keeps its single-`source_path`, tier-invariant, ABORT-on-NO-ACCESS contract **untouched** (it analyzes an
already-materialized set, it does not detect boundaries).

## 5. Chapter Manifest (`source/<slug>/chapter-manifest.yaml`)

Source-side sidecar (BUILD-NEW, outside the Rule-F hash-pin glob), co-located with the chapters it indexes.
**Not** a numbered package file; **not** a `rewrite_phase_reads` member.

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

## 6. Split Mechanism (ADR-006 compliant — prompt + YAML, no runtime)

New NATIVE skill `laf-adaptation:chapter-materialize` (`SKILL.md` + `resources/boundary-rules.yaml`),
attached to `prep-cordinator` via **one additive `skills:` frontmatter line**. The procedure is executed
by the model; `check_boundary.py` remains the sole script and a validator only.

**Multi-signal evidence layers** (the skill applies, in order):
1. TOC / anchor map (e.g. `I. <a href="#chap01">…</a>` … `XVII`).
2. Body heading map (`CHAPTER I`, `Chapter 1`, `Chapter One`, `<h1>/<h2 class=chapter>`; roman/arabic/spelled).
3. Filename map (Mode A) — **natural sort**, never lexicographic (`ch-2` before `ch-10`).
4. Content sanity — each chapter starts with expected heading, non-empty body, plausible length,
   non-overlapping ranges.
5. Count reconciliation — TOC vs body-heading vs filename counts must agree or gate.

**Confidence rule (merged, load-bearing):** **CERTAIN requires ≥2 independent agreeing signals and no
contradiction.** One strong signal + plausible content → **PROBABLE**. Missing/contradictory signals,
manual repair, or PDF garble → **UNCERTAIN**. Single-signal boundaries are **capped at PROBABLE**. Every
boundary/title/order is a `/source-fidelity`-tagged fact.

## 7. Failure-Mode Table (release-gating behaviors)

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

## 8. Format Normalization & Fidelity

- HTML → strip tags/scripts/style/nav/boilerplate, decode entities, preserve paragraph breaks. PDF →
  extract text stream, rejoin hyphenated wraps, preserve paragraph breaks. Output UTF-8. **No rewording,
  no reflow, no editorial change** — chapter body is verbatim prose with markup removed (consistent with
  the existing hand-provisioned narnia files).
- **Raw retention:** original input retained at `source/<slug>/.raw/<file>` as the fidelity anchor.
- **`/source-fidelity` coverage:** markup loss is expected and must be recorded — every discard is a
  `normalization_event` with a `source_fidelity_risk` label. Italics-in-titles, verse indentation,
  letters, footnotes, illustrations, page breaks may carry meaning; if stripped, the manifest says so.
  **High-risk losses block greenlight** unless the operator accepts them in `50-greenlight.md`
  (`70-traceability.md` records the accepted risk). Pure tag-strip → CERTAIN; structural ambiguity
  (tables, footnotes, verse) → PROBABLE and surfaced.

## 9. Idempotency, Collisions, Backward Compatibility

- **Mode C adopt (zero re-split):** if `source/<slug>/ch-*.txt` exists, read titles/ordinals from the
  existing files and write/refresh only `chapter-manifest.yaml` (`provenance.class: ADOPTED`). narnia
  (ch-01..04) and tolkien (ch-01) adopt untouched; a manifest-less existing set adopts with
  `split_confidence: CERTAIN` for existence but `provenance` gaps flagged for review until raw provenance
  is supplied.
- **Re-run:** read the manifest first; if raw-source and output hashes match → no-op (`review.status:
  CONFIRMED` short-circuits Stage 0). If raw changed but output exists → produce a diff-style replacement
  plan and gate it; **never overwrite by default**.
- **Collision:** an existing `ch-NN.txt` whose hash differs from a proposed resplit is **never clobbered**
  — HALT-and-ask at the gate.

## 10. Gate Integration (reuse the existing §5 / greenlight)

- No new gate, no new HALT machinery. Stage-0 `ambiguous_splits` + `needs_human_review` items are folded
  into the existing §5 coverage-constrained question block (each ambiguous split is a
  `human_judgment_dimension: true`-equivalent input). Each allows `[skip] → DEFAULTED` recorded in
  `70-traceability.md`.
- **Deferred-write safety invariant:** no `ch-NN.txt` for a PROBABLE/UNCERTAIN boundary is committed
  before the human resolves it. CERTAIN chapters commit immediately; the rest commit on greenlight-confirm.
- Greenlight checklist gains one line: *"chapter manifest ratified: count N; all UNCERTAIN boundaries and
  high-risk normalization losses resolved."* Greenlight CONFIRMED ⇒ manifest `review.status: CONFIRMED`.

## 11. Boundary-Contract Compliance & Bill of Materials

| File | Provenance | Change |
|---|---|---|
| `laf-adaptation/skills/chapter-materialize/SKILL.md` | **NEW NATIVE** | split/normalize/adopt procedure |
| `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` | NEW NATIVE | declarative signal ruleset |
| `laf-adaptation/agents/prep-cordinator.md` | NATIVE (`laf_sha256=—`) | +1 `skills:` line + Stage-0 procedure paragraph |
| `laf-adaptation/skills/prep/SKILL.md` | NATIVE | +Stage-0 note in §1; pointer to `chapter-materialize` |
| `laf-adaptation/skills/prep/resources/path-contract.md` | NATIVE | +write-ownership rows; +new "source-side manifest" subsection; **§4 read-set UNCHANGED** |
| `laf-adaptation/source/README.md` | BUILD-NEW | +manifest + `.raw/` subsection |
| `.claude/commands/laf/prep.md` | NATIVE mirror | +`--source-mode`; `--source` may be dir/file/adopt-set |
| `laf-adaptation/VENDOR.md` | NATIVE | +1 NATIVE row for `chapter-materialize/SKILL.md` (Rule F) |

- **Zero ADOPTED-CLEAN bodies touched; `writer.md` untouched; `check_boundary.py` untouched (sole script,
  validator).** New skill clears Rule E (no upstream `chapter-materialize` collision) and Rule F
  (manifested). **Mode V green by construction.** `.claude/` mirror updated in lockstep (existing mirroring).

## 12. path-contract.md Deltas (diff-style)

```
  §1, §2 (package location, 8-file table) ................ UNCHANGED (no 05-chapters.yaml, no 9th file)
  §4 rewrite_phase_reads ................................. UNCHANGED (exactly the 3 files)
+   (explicit note) "chapter-manifest.yaml is a source/ sidecar, deliberately NOT in rewrite_phase_reads;
+    the rewrite phase discovers chapters by the source/<slug>/ch-<NN>.txt convention."
  §5 write-ownership:
+   | source/<slug>/ch-<NN>.txt          | prep-cordinator (Stage 0) |
+   | source/<slug>/chapter-manifest.yaml| prep-cordinator (Stage 0) |
+   | source/<slug>/.raw/*               | prep-cordinator (Stage 0) |
+ §6 (NEW) "Source-side chapter manifest" — path, schema summary, non-membership-in-read-set note.
```

## 13. Acceptance Criteria

- AC1. `/laf:prep "<title>" --source <dir-of-chapters>` (Mode A) and `--source <monolith>` (Mode B) each
  yield identical canonical `source/<slug>/ch-<NN>.txt` + `chapter-manifest.yaml`, no manual pre-split.
- AC2. `--source Books/LWW/` (split files + monolith copies both present) does **not** auto-pick; it raises
  a mode question. (Analyzer release-blocker #1.)
- AC3. Re-running against `source/narnia/` and `source/tolkien/` adopts with zero byte rewrites (Mode C).
- AC4. No `ch-NN.txt` for a non-CERTAIN boundary is written before greenlight; single-signal boundaries are
  never CERTAIN. (Analyzer release-blockers #2, #3.)
- AC5. Every manifest chapter row carries confidence + provenance + `needs_human_review`; every markup
  discard is a `normalization_event` with a fidelity-risk label. (Analyzer release-blockers #4, #5.)
- AC6. `uv run python scripts/check_boundary.py` exits 0; `rewrite_phase_reads` is byte-unchanged; no 9th
  package file; no second script. (Analyzer release-blockers #6, #7.)
- AC7. Greenlight cannot reach CONFIRMED while any `ambiguous_split`, `needs_human_review`, or high-risk
  normalization loss is unresolved.

## 14. Release-Blocking Risks (carried from the analyzer lens)

1. Auto mode choosing between split-folder and monolith when both are present.
2. Any write path overwriting existing canonical source without explicit approval.
3. Any single-signal CERTAIN boundary.
4. Any manifest chapter lacking confidence / provenance / `needs_human_review`.
5. Any normalization stripping footnotes/illustrations/poetry/italics without a recorded fidelity risk.
6. Any expansion of the fixed 8-file package or silent change to the frozen rewrite read-set.
7. Any second script, parser CLI, or adopted-body edit.

## 15. Open Tensions Deferred to the Rewrite Spec

- The manifest is authoritative for the chapter set but is **not** in `rewrite_phase_reads`. Whether the
  rewrite phase should read it (justifying a 4th read-entry) or discover chapters purely by convention is
  **the** seam between this spec and the next — the follow-on rewrite brainstorm must resolve it.
- Per-chapter analysis granularity (deferred here) is a rewrite-phase decision.

## Next Step

Run the follow-on brainstorm to spec the rewrite command that ingests these individual chapter files:
see `rewrite-brainstorm-prompt.md` in this directory.
