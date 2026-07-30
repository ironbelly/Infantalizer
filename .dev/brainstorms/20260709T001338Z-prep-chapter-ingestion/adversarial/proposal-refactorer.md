# Proposal — REFACTORER lens: `/laf:prep` v-next owns chapter materialization

> Stance: **extend prep, do not fork it.** One new NATIVE skill, one new stage absorbed by an existing
> NATIVE orchestrator, one source-side sidecar manifest. Zero adopted-body edits. The frozen
> `rewrite_phase_reads` set is untouched. No new command, no new script, no new runtime.

The REFACTORER test this proposal is graded against: smallest diff, maximum reuse, backward compat,
zero scope creep. Every new concept below is weighed against "can the existing prep-cordinator stage
flow + the existing question/greenlight gate + the existing `source/<slug>/ch-NN.txt` convention already
carry this?" If yes, we extend; we do not invent.

---

## 1. Command surface — extend prep, NO new command

**Decision: `/laf:prep` absorbs both modes. No `/laf:ingest`.**

The existing command already takes `--source <path-or-url>` and already says "if omitted, elicit it."
The operator's raw input today is *ambiguous between folder, monolith, and already-split set* — the
coordinator just never resolved that ambiguity. The smallest possible change is to let `--source`
point at any of:

- a **directory** (Mode A — folder of per-chapter files), or
- a **single file** (Mode B — monolithic HTML/PDF/txt), or
- a **`source/<slug>/` dir already holding `ch-*.txt`** (Mode C — already-split, adopt).

That is **zero new flags**. `--source <path>` already accepts a path; a path can be a directory.
`prep.md` gains ~3 lines of disambiguation prose; `prep-cordinator.md` Stage-1 gains a mode-detect
paragraph. No `argument-hint` change, no new positional, no new command file.

**Why not a thin new command:** a new `/laf:ingest` would have to re-derive the slug, re-emit a
package-adjacent artifact, re-open the question gate seam, and hand off to prep — duplicating exactly
the coordinator machinery that already owns slug derivation, HALT gates, and the `source_path`
required-input elicit. A command-per-concern split sounds clean and is, here, pure surface inflation.
The prep phase *is* the onboarding phase; materialization is the first onboarding act. One command.

---

## 2. Materialization is absorbed by `prep-cordinator` as a new **Stage 0** — not a new stage-type, not a new agent

The coordinator already owns an 8-stage flow (`STAGE 1 RESEARCH … STAGE 8 HANDOFF`) and already owns
the source-path required-input elicit at Stage-1(a). Materialization is the natural **Stage 0** that
runs *before* Stage-1(a)'s source declaration: "turn whatever `--source` resolved to into the canonical
`source/<slug>/ch-<NN>.txt` set, then hand Stage 1 a clean per-chapter source layout."

**Why not a new orchestrator agent:** `prep-cordinator.md` is **NATIVE** (`VENDOR.md`: `laf_sha256 = —`),
so editing its body is boundary-clean — no adopted-body violation. It already loads `laf-adaptation:prep`
and already dispatches sub-agents (`Agent(analyst, web-researcher, tier-coordinator)`). A second
orchestrator would split the HALT-gate ownership and the write-scope invariants the path contract
guarantees for `work/prep/<slug>/`. One orchestrator, one write scope, one gate owner.

The new Stage 0 does **not** dispatch a new analyzer — it dispatches the new NATIVE skill (§4) **inline
in the coordinator's own context** (the skill is a procedure the coordinator executes, like `prep`
itself), producing files under `source/<slug>/` (BUILD-NEW territory, already write-allowed by
`source/README.md` semantics — new files, not in-place transforms).

---

## 3. Chapter manifest — a **source-side sidecar**, `rewrite_phase_reads` UNCHANGED

**Decision: `source/<slug>/manifest.yaml`. The frozen 3-file read-set does NOT gain a 4th entry.**

This is the load-bearing refactorer call. The path-contract §4 `rewrite_phase_reads` is
`[30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]` and is described as "frozen." Adding a
4th entry (`05-chapters.yaml`) would (a) re-open a contract the design pack froze on purpose, (b)
require a justification the boundary between *prep-derived* and *source-provisioned* doesn't need, and
(c) couple the rewrite read-set to a new artifact when the rewrite already discovers chapter files by
globbing `source/<slug>/ch-*.txt`.

The manifest is **source provenance, not a derived prep artifact.** It lives next to the chapters it
describes, under the read-only `source/` tree — the same place `source/README.md` already documents
the convention. The future `/laf:rewrite` discovers it the same way the analyst discovers a
`source_path`: by convention, as part of source access, not as a member of the derived package.

**Schema (deliberately tiny):**

```yaml
# source/<slug>/manifest.yaml — NATIVE, BUILD-NEW, read-only once written
work: narnia
slug: narnia
provenance:
  input_mode: folder | single-file | already-split   # Mode A/B/C
  raw_source: "Books/LWW/*.html"                      # original path/glob the operator gave
  normalized: true                                    # HTML/PDF → UTF-8 applied (§5)
chapters:
  - id: "01"
    title: "Lucy Looks into a Wardrobe"               # extracted; confidence-tagged below
    file: ch-01.txt
    source_span: "The Lion…-1.html"                   # raw file this chapter came from (Mode A/B)
    split_confidence: CERTAIN                         # CERTAIN | PROBABLE | UNCERTAIN
  - id: "02"
    title: "What Lucy Found There"
    file: ch-02.txt
    source_span: "The Lion…-2.html"
    split_confidence: CERTAIN
gate:
  ambiguous_splits: []        # entries routed through the §5 question gate
  status: RESOLVED            # RESOLVED after greenlight; PENDING if any UNCERTAIN unanswered
```

`source/README.md` gains a ~6-line "manifest" subsection pointing here. No package file added, no
read-set entry added, no path-contract §2 (the 8-file table) change.

---

## 4. Split mechanism — one new **NATIVE skill** (`chapter-matrix`), driven by the coordinator, under ADR-006

**Decision: a prompt+YAML procedure in a new NATIVE skill `laf-adaptation:chapter-matrix`, attached
to `prep-cordinator` via one additive `skills:` frontmatter line. No new script.**

ADR-006's "not software" line is: **no second script, no runtime, no parser binary.** `check_boundary.py`
stays the sole script and stays a *validator*. The split is expressed exactly the way every other LAF
capability is — a NATIVE skill body (prompt procedure) + YAML-declared rules, executed by an agent.
The new skill's procedure:

1. **Detect mode** (Stage 0, step 1): is `--source` a dir with `ch-*.txt` (Mode C), a dir of arbitrary
   per-chapter files (Mode A), or a single monolith (Mode B)?
2. **Mode C → adopt** (§6). **Mode A → order/rename/normalize** each input file into `ch-<NN>.txt`,
   reading the heading/ordinal from each file (confidence-tagged). **Mode B → boundary-detect**:
   locate chapter-heading lines (`CHAPTER I`, `Chapter 1`, `<h1>`, `<h2 class="chapter">`, TOC
   cross-ref) and split; front/back matter and unnumbered prologues become `ambiguous_splits`.
3. **Tag every boundary** CERTAIN/PROBABLE/UNCERTAIN per `/source-fidelity` vocabulary — a split
   decision is an extracted fact, exactly the kind the protocol already governs.
4. **Emit** `source/<slug>/ch-<NN>.txt` + the `manifest.yaml` of §3.

Why a skill and not "just more prose in prep-cordinator.md": the procedure is reusable reasoning
(heading heuristics, ordinal normalization, matter-detection) and it is exactly what a NATIVE skill is
for under the boundary contract — it keeps the coordinator body lean and lets the capability be
frontmatter-attached, the contract's blessed injection point. **One new NATIVE skill, one additive
frontmatter line on a NATIVE agent.** That is the entire new surface area.

The analyst is **not** the splitter. The analyst's job is source-fidelity analysis of an *already
materialized* chapter; using it to also detect boundaries conflates two confidence-tagged acts and
risks relaxing its Phase-0 ABORT semantics. The new skill owns boundaries; the analyst keeps owning
analysis. (Reuse-auditor's dream: each capability is still one thing.)

---

## 5. Format normalization — least machinery: inline in `chapter-matrix`, no new tooling

HTML/PDF → clean UTF-8 is done **inside the `chapter-matrix` skill procedure as a prompt step** ("strip
markup/boilerplate, preserve paragraph breaks, drop nav/footers"), not by a vendored parser or a new
script. Fidelity is asserted the only way LAF ever asserts it: the normalized `ch-<NN>.txt` carries
`normalized: true` in the manifest, and any region where markup was ambiguous (tables, embedded
illustrations, dropped footnotes) is tagged **PROBABLE** on the chapter's `split_confidence` and
surfaced at the question gate. We do **not** claim byte-fidelity to a markup source we just discarded;
we claim transparent-uncertainty, which is the protocol's stated principle. No new machinery.

For PDF specifically: if the coordinator cannot extract usable text via its existing Read tool, that
chapter is tagged UNCERTAIN and routed to the gate — same NO-ACCESS-shaped failure mode the analyst
already uses, no new path.

---

## 6. Idempotency + zero-resplit adoption of narnia/tolkien

**Mode C detection is the backward-compat story.** Stage 0 step 1 checks: does `source/<slug>/`
already contain one or more `ch-*.txt`? If yes → **adopt, do not resplit.**

- `source/narnia/ch-01..04.txt` and `source/tolkien/ch-01.txt` are detected; the coordinator
  **reads titles/ordinals from the existing files** and writes/refreshes only `manifest.yaml`.
  Zero existing chapter bytes are rewritten. (Tolkien's synthetic PATH-B fixture is adopted as-is —
  its `CHAPTER I / Lucy Looks…`-style heading is read, not regenerated.)
- Re-running prep on an already-materialized slug is a manifest refresh: existing `ch-<NN>.txt`
  hashes are compared; **identical files are never rewritten**; collisions (a new split proposes a
  `ch-03.txt` where one exists) are NOT silently overwritten — they route to the question gate
  ("existing ch-03.txt differs from resplit; keep existing, or replace?").
- The manifest's `gate.status: RESOLVED` is the idempotency marker: a re-run that sees `RESOLVED`
  and unchanged raw source short-circuits Stage 0 entirely.

---

## 7. Ambiguous splits reuse the EXISTING question/greenlight gate — no new gate

There is already one HALT-with-human gate in prep: **Stage 5 §5 question gate** (coverage-constrained,
interrupt semantics, no runtime). The manifest's `ambiguous_splits` list is **folded into the same
Stage-5 question block** as the taxonomy-driven human-judgment questions. Zero new gate, zero new
HALT semantics. Each ambiguous split (missing ordinal, duplicate heading, front/back matter, unnumbered
prologue) becomes one question with a `[skip] → DEFAULTED` path recorded in `70-traceability.md`,
exactly like a skipped taxonomy question.

This is the strongest refactorer argument against a new gate: the framework already has a
confidence-routing-to-human mechanism, and splitting ambiguity is just another `human_judgment_dimension: true`
input by another name.

---

## 8. Boundary-contract compliance — zero adopted-body edits

Concrete bill of materials, every one NATIVE or BUILD-NEW (none hash-pinned):

| File | Provenance | Change |
|---|---|---|
| `skills/chapter-matrix/SKILL.md` | **NEW NATIVE** | the split/normalize/adopt procedure |
| `agents/prep-cordinator.md` | NATIVE (`laf_sha256=—`) | +1 `skills:` line (`- laf-adaptation:chapter-matrix`); +Stage 0 paragraph |
| `skills/prep/SKILL.md` | NATIVE | +1 line in §1 noting Stage 0 materialization; pointer to `chapter-matrix` |
| `skills/prep/resources/path-contract.md` | NATIVE | manifest row in a **new §6**; `rewrite_phase_reads` §4 **unchanged** |
| `source/README.md` | BUILD-NEW | +manifest subsection |
| `.claude/commands/laf/prep.md` | NATIVE (mirror) | +3 lines: `--source` may be dir/file/split-set |

**Zero ADOPTED-CLEAN bodies touched. `writer.md` untouched. `check_boundary.py` untouched (still the
sole script, still a validator). No new `scripts/` file.** The new skill registers cleanly under
Rule E (no upstream name collision — `chapter-matrix` is LAF-native) and Rule F (its `SKILL.md` is
manifested). Mode V stays green by construction.

The `.claude/` mirror is updated in lockstep (the table's right-column files all have `.claude/`
twins) — no new sync concept, just the existing `laf-adaptation/ → .claude/` mirroring.

---

## 9. `path-contract.md` deltas — as few as possible

- **§1, §2** (package location, 8-file table): **unchanged.** No `05-chapters.yaml`.
- **§4** (`rewrite_phase_reads`): **unchanged.** Still exactly 3 files.
- **§5** (write-ownership): **+1 row** — `source/<slug>/*` (chapters + `manifest.yaml`) written by
  `prep-cordinator` (prep phase, Stage 0). This codifies what `source/README.md` already implies.
- **§6 (NEW)**: a 4-line "Source-side chapter manifest" subsection naming
  `source/<slug>/manifest.yaml`, its schema summary, and the explicit note "not a member of
  `rewrite_phase_reads`; consumed by rewrite as source-discovery convention."

That is the entire contract delta: one new row, one new short subsection, one explicit non-membership
note. The frozen read-set is named **unchanged** in bold.

---

## 10. What I explicitly REFUSE to add (scope discipline)

- **No new command** (`/laf:ingest`). Prep is the onboarding phase; materialization is Stage 0 of it.
- **No new script / runtime / parser binary.** ADR-006 stays at one validator script. Splitting is a
  prompt+YAML procedure in a NATIVE skill.
- **No 4th `rewrite_phase_reads` entry.** The manifest is a source sidecar; the rewrite discovers it
  by convention. Re-opening a frozen contract for a convenience read is not justified.
- **No per-chapter analysis in prep v-next (OQ2).** Analysis stays `granularity=work`. Moving the
  analyst per-chapter is a *rewrite-phase* concern (the rewrite already re-reads the package per
  chapter) and belongs in the `/laf:rewrite` spec, not this one. Prep materializes + manifests; it
  does not re-shape its analysis track here.
- **No new gate.** Ambiguous splits reuse Stage-5 §5.
- **No `05-chapters.yaml` package file.** The 8-file table is fixed; a 9th breaks the contract for no
  gain over a sidecar.
- **No analyst-body edit.** The analyst keeps its single-`source_path`, tier-invariant,
  ABORT-on-NO-ACCESS contract untouched. Boundary detection is a different act and lives in
  `chapter-matrix`.
- **No in-place `source/` transforms.** Materialized chapters are new files under `source/<slug>/`;
  existing narnia/tolkien bytes are never rewritten.

---

## OQ position summary (one line each)

- **OQ1 (ownership):** prep owns it; one new NATIVE skill, no new command.
- **OQ2 (granularity):** analysis stays work-level; chapters are materialized + manifested only.
- **OQ3 (split mechanism):** prompt+YAML procedure in NATIVE skill `chapter-matrix`; no script, no
  runtime; `check_boundary.py` untouched.
- **OQ4 (manifest placement):** source sidecar `source/<slug>/manifest.yaml`; `rewrite_phase_reads`
  unchanged (no 4th entry).
- **OQ5 (normalization):** inline markup-strip in the skill; transparent-uncertainty tagging, no new
  tooling.
- **OQ6 (idempotency/gating):** Mode C detects existing `ch-*.txt` and adopts zero-resplit; manifest
  `gate.status` is the idempotency marker; low-confidence/ambiguous splits fold into the existing
  Stage-5 question gate.

**Total new surface: 1 NATIVE skill, 1 source-side sidecar, 1 contract subsection, 1 frontmatter line.
Everything else is prose on existing NATIVE files.** That is the refactorer's floor.
