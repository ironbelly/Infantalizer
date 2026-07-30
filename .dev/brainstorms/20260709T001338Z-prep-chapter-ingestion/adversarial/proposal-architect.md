# Proposal — ARCHITECT lens: `/laf:prep` v-next chapter materialization

> Lens priorities: systems design, boundary-contract fidelity, minimal justified extension of the
> frozen path contract. Position: **materialization is a new front stage of `/laf:prep`, not a fork;
> the chapter set is recorded as a `source/`-side sidecar manifest that the frozen `rewrite_phase_reads`
> does NOT read; analysis stays work-level for v-next.**

## 0. Governing stance (the architectural spine)

The seed brief tempts us toward two expensive commitments: (a) a second command (`/laf:ingest`), and
(b) per-chapter analysis. I reject both for v-next. The framework already has exactly one orchestrator
(`prep-cordinator`) and one analysis granularity (`granularity=work`). Adding a command forks the
lifecycle and duplicates the source-access ABORT gate; moving to per-chapter analysis is a *rewrite-phase*
concern (the analyst already reads a chapter as `source_path` at rewrite time) and would balloon prep's
scope. The disciplined move is: **prep grows one front stage that produces the canonical chapter set +
a manifest, and everything downstream is unchanged.** This keeps the 8-file package, the frozen read-set,
and `check_boundary.py` exactly as they are.

## OQ answers (stated up front, one line each)

- **OQ1 — Ownership:** `/laf:prep` owns it. No new command. New STAGE 0 inside the existing procedure,
  driven by `prep-cordinator`. The seam is a *stage boundary*, not a *command boundary*.
- **OQ2 — Granularity:** Stays **work-level**. Stage 0 materializes chapters + manifest; §3 analysis
  continues to run whole-work against `20-analysis-work-level.yaml`. Per-chapter analysis is deferred to
  the rewrite spec (out of scope here).
- **OQ3 — Split mechanism:** Agent-driven heading/TOC detection expressed as a NATIVE skill
  (`chapter-split`) + a declarative YAML boundary-ruleset. **No runtime, no second script.** Confidence
  is CERTAIN/PROBABLE/UNCERTAIN per boundary, not binary.
- **OQ4 — Manifest placement:** A **`source/<slug>/manifest.yaml` sidecar** — NOT a numbered package file,
  NOT a new `rewrite_phase_reads` entry. `rewrite_phase_reads` stays frozen at 3. Rationale in §3.
- **OQ5 — Format normalization:** Minimal, reversible-by-inspection cleaning; fidelity asserted by
  `/source-fidelity` on the *extracted text*, with the raw input retained under `source/<slug>/.raw/`.
- **OQ6 — Idempotency:** Content-hash-keyed re-run; existing `source/<slug>/` detected and adopted
  (backward compat); UNCERTAIN boundaries routed to the §5 question gate before greenlight.

## 1. Command surface

```
/laf:prep "<title>" [--source <path-or-url>] [--source-mode auto|folder|file|split]
```

`--source` is unchanged and still REQUIRED (elicited if omitted). One new optional flag:

- `--source-mode` (default `auto`). Auto-detection precedence, evaluated by the coordinator in STAGE 0:
  1. **`split`** — `--source` points at a dir already matching `source/<slug>/ch-<NN>.txt` (or the target
     `source/<slug>/` already exists and validates) → adopt, do not re-split (backward compat: narnia,
     tolkien).
  2. **`folder` (Mode A)** — `--source` is a directory of ≥2 files that are NOT the canonical layout
     (e.g. `Books/LWW/*.html`) → normalize/order/rename.
  3. **`file` (Mode B)** — `--source` is a single file → detect boundaries and split.

`argument-hint`: `"<title>" [--source <path>] [--source-mode auto|folder|file|split]`. The flag exists so
an operator can override a bad guess without editing files; `auto` is expected to be correct for the three
real cases in-tree.

## 2. New pipeline stage — STAGE 0 (materialization), and who owns it

Insert **STAGE 0: Source Materialization** *before* the current §3 two-track analysis. It is owned by
`prep-cordinator` (the only orchestrator; already has Read/Write/Glob/Grep). Stage sequence becomes:

```
STAGE 0  materialize chapters + write source/<slug>/manifest.yaml   [NEW]
STAGE 1  §2 challenge taxonomy → 10-challenges.yaml                 (unchanged)
STAGE 2  §3 two-track analysis → 00/20                             (unchanged; now reads materialized chapters)
STAGE 3  §4 mapping → 30                                            (unchanged)
STAGE 4  §5 question gate  ← receives STAGE-0 UNCERTAIN splits      (EXTENDED)
STAGE 5  §6 greenlight                                             (EXTENDED: manifest ratified)
STAGE 6  §7 handoff / §8 traceability                              (unchanged)
```

STAGE 0 has three sub-steps, each dispatched by the coordinator:

1. **Detect mode** (§1 precedence). Emits `source_mode`.
2. **Normalize + boundary-detect** — dispatch the NATIVE `chapter-split` skill (loaded by the coordinator;
   for boundary *reading* the coordinator may fan a scoped `analyst` sub-call since the analyst is the
   source-fidelity-bearing reader). Produces per-chapter text + per-boundary confidence.
3. **Materialize + manifest** — coordinator writes `source/<slug>/ch-<NN>.txt` and
   `source/<slug>/manifest.yaml`.

**Write-ownership:** `prep-cordinator` owns all STAGE-0 writes. This is a *new* write target for the
coordinator (`source/<slug>/*`) and MUST be added to the path-contract write-ownership table (§9). Crucially
this is the ONE place the framework writes into `source/` — justified because `source/README.md` already
says `source/` holds materialized chapters; today provisioning is "MANUAL"; STAGE 0 simply *automates the
provisioning that the README already specifies*, writing NEW files (never transforming in place).

## 3. Chapter manifest — placement, schema, and why `rewrite_phase_reads` does NOT change

**Placement: `source/<slug>/manifest.yaml` sidecar.** Two options were on the table (OQ4): a numbered
package file `05-chapters.yaml`, or a `source/` sidecar. I choose the sidecar, decisively:

- The manifest describes **`source/` state**, not **prep-package state**. It is a property of the
  materialized chapter set, which lives in `source/` and is read-only reference. Co-locating it with the
  chapters it indexes is the correct ownership boundary.
- A numbered package file would force a decision about whether `rewrite_phase_reads` gains a 4th entry.
  The frozen 3-file read-set is load-bearing and restated across three files by reference. **Do not touch
  it.** The rewrite phase does not need the manifest to *drive* work in v-next — it derives chapter N's
  source path by convention (`source/<slug>/ch-<NN>.txt`), exactly as the analyst does today. The manifest
  is for *materialization audit + human review + future rewrite enumeration*, not for the frozen contract.
- Keeping it out of the numbered package also keeps `check_boundary.py` untouched (the manifest is under
  `source/`, which is BUILD-NEW and outside the Rule-F hash-pin glob).

**Schema** (`source/<slug>/manifest.yaml`):

```yaml
work_slug: narnia
source_mode: folder            # folder | file | split-adopted
raw_source: .raw/lww.html      # relative to source/<slug>/; retained input (see §5)
chapter_count: 17
chapters:
  - id: ch-01                  # stable, zero-padded, order == numeric id
    title: "Lucy Looks into a Wardrobe"
    title_confidence: CERTAIN  # CERTAIN | PROBABLE | UNCERTAIN
    source_path: ch-01.txt     # relative to source/<slug>/
    boundary_confidence: CERTAIN
    order: 1
    provenance:
      class: NATIVE-materialized   # or SPLIT-ADOPTED for pre-existing
      derived_from: ".raw/lww.html#offset-or-file"   # raw input span / origin file
      fidelity_note: "markup stripped; text verbatim"
front_back_matter:             # explicitly recorded, NOT numbered as chapters
  - kind: prologue
    disposition: EXCLUDED       # EXCLUDED | INCLUDED-AS ch-00 | flagged-for-human
    confidence: PROBABLE
materialization_summary:
  certain: 15
  probable: 1
  uncertain: 1                 # any >0 forces the §5 question gate
```

`rewrite_phase_reads` remains **exactly** `[30-mapping.yaml, 40-prep-brief.md, 10-challenges.yaml]`.
Zero change. This is the single most important boundary-fidelity claim in this proposal.

## 4. Split mechanism under ADR-006 (no runtime)

Boundary detection is expressed as **a NATIVE skill body (`chapter-split`) + a declarative YAML ruleset**,
executed by the model — never a parser binary. The one allowed script (`check_boundary.py`) is untouched.

`skills/chapter-split/resources/boundary-rules.yaml` (declarative signals the agent applies):

```yaml
heading_signals:            # ordered; agent matches against normalized text
  - pattern_class: numbered-chapter    # "CHAPTER I", "Chapter 1", "1."
    confidence_when_regular: CERTAIN
  - pattern_class: titled-only         # a bare title line + following prose
    confidence_when_regular: PROBABLE
  - pattern_class: toc-derived         # boundaries inferred from a detected TOC
    confidence_when_regular: PROBABLE
folder_mode:
  order_by: [leading-number, filename-lexical, toc-order]
  title_from: [first-heading-line, filename, "UNCERTAIN"]
regularity_rule: >
  If detected boundaries form a contiguous 1..N run with consistent heading class,
  each boundary is CERTAIN. A gap, duplicate, or class-switch drops the affected
  boundary to PROBABLE; no boundary at an expected position → UNCERTAIN + human gate.
```

The skill instructs the agent to: read normalized text → find candidate boundaries by the ruleset →
assign per-boundary confidence → emit the chapter set + manifest confidence tallies. The `analyst`'s
`/source-fidelity` discipline is reused: every title/boundary is a *fact extraction* and carries a tag.
This is exactly "prompt + YAML-config, not software."

## 5. Format normalization + fidelity assertion

**Cleaning policy (minimal):** HTML → strip tags/scripts/style/nav boilerplate, decode entities, preserve
paragraph breaks; PDF → extract text stream, join hyphenated line-wraps, preserve paragraph breaks; output
UTF-8. **No rewording, no reflow of sentences, no editorial change.** The chapter *body text* is verbatim
source prose with markup removed — this keeps it consistent with the existing hand-provisioned narnia files.

**Fidelity assertion (`/source-fidelity`):** STAGE 0 runs the source-access declaration and ABORT-on-
NO-ACCESS *first* (identical to today's text track). The retained raw input at `source/<slug>/.raw/` is the
fidelity anchor: the manifest's per-chapter `fidelity_note` records that markup was discarded and text is
verbatim. Because markup discard is lossy w.r.t. *formatting* (not *prose*), the skill emits a
`fidelity_note` at CERTAIN only when the extraction is a pure tag-strip; any structural ambiguity (tables,
footnotes, embedded verse) drops to PROBABLE and is surfaced. This is the honest "transparent uncertainty >
false certainty" stance the anti-hallucination rule demands.

## 6. Idempotency, re-run, collision, backward compat

- **Backward compat (split-adopt):** if `source/<slug>/ch-*.txt` already exists and matches the canonical
  layout, STAGE 0 enters `split-adopted` mode: it does NOT re-split, it *reads* the existing files and
  writes/refreshes only `manifest.yaml` (provenance `class: SPLIT-ADOPTED`). narnia (ch-01..04) and tolkien
  (ch-01) work untouched.
- **Idempotency:** the manifest records `raw_source` and a content hash of each materialized chapter
  (extend schema with `sha256` if desired). A re-run with the same raw input + same detection is a no-op
  (hashes match). A changed raw input surfaces a diff to the human rather than silently overwriting.
- **Collision:** STAGE 0 never overwrites an existing `ch-<NN>.txt` whose hash differs without routing to
  the human gate. Write-once semantics on `source/`; conflicts are HALT-and-ask, not clobber.

## 7. Where ambiguous splits enter the human gate

STAGE 0 feeds the existing §5 question gate. Rule: **`materialization_summary.uncertain > 0` (or any
`front_back_matter` with `disposition: flagged-for-human`) is treated as a `human_judgment_dimension: true`
challenge** and MUST produce a question in the §5 block — e.g. "Chapter 12 boundary is UNCERTAIN (no heading
detected between ch-11 and ch-13 signals); confirm split point or supply." The greenlight checklist (§6)
gains one line: *"chapter manifest ratified: count N, all UNCERTAIN boundaries resolved."* Greenlight cannot
reach CONFIRMED while an UNCERTAIN boundary is unresolved. This reuses the interrupt-semantics gate exactly
as-is — no new gating machinery.

## 8. Boundary-contract compliance

- **No adopted body edited.** New capability is a **NATIVE skill `chapter-split`** + procedure text in the
  prep SKILL (NATIVE) + `prep-cordinator` body (NATIVE agent). The coordinator attaches the skill via its
  own `skills:` frontmatter (permitted — coordinator is NATIVE, not adopted).
- **check_boundary.py stays green.** `chapter-split/SKILL.md` is a new NATIVE skill dir → it IS in the
  Rule-F glob (`skills/**/SKILL.md`) and MUST be added to VENDOR.md as a NATIVE row (name must not collide
  with upstream — Rule E; "chapter-split" has no CWS analog). `boundary-rules.yaml` lives under the NEW
  skill's `resources/` (a NATIVE skill's own resources, not an *adopted* skill's — so no adopted-tree
  muddying). Everything under `source/` is BUILD-NEW, outside the hash-pin glob.
- **Still one script.** No runtime added; ADR-006 intact.
- **Provenance classes honored:** materialized chapters are NATIVE-materialized (or SPLIT-ADOPTED); no
  adopted-body edit; `source/` remains read-only-after-materialization reference.

## 9. Path-contract.md deltas (diff-style)

```
+ §2a  Source materialization sidecar (NEW section)
+   source/<work-slug>/manifest.yaml   — chapter manifest (schema in prep SKILL §0-materialize)
+   source/<work-slug>/ch-<NN>.txt     — materialized chapters (was: manually provisioned)
+   source/<work-slug>/.raw/<file>     — retained raw input (fidelity anchor)

  §4  rewrite_phase_reads  — UNCHANGED  (remains exactly the 3 files; manifest is NOT added)
+   (explicit note) "The chapter manifest is a source/ sidecar and is deliberately NOT in
+    rewrite_phase_reads; the rewrite phase derives ch-<NN>.txt by convention."

  §5  Write-ownership table:
+   | source/<slug>/ch-<NN>.txt        | prep-cordinator (STAGE 0, materialization) |
+   | source/<slug>/manifest.yaml      | prep-cordinator (STAGE 0, materialization) |
+   | source/<slug>/.raw/*             | prep-cordinator (STAGE 0, materialization) |
```

Three additive rows + one clarifying note. The frozen read-set line is untouched — that is the whole point.

## 10. Risks + open trade-offs

- **R1 — Manifest not read by rewrite = drift risk.** Because `rewrite_phase_reads` doesn't include the
  manifest, a rewrite phase could disagree with it. Mitigation: the rewrite phase already derives paths by
  convention, and the manifest is a human/audit artifact; if v-next-rewrite later needs enumeration, that is
  the point to justify a 4th read-entry — deliberately deferred, not denied.
- **R2 — Model-driven splitting is fallible on messy input.** No parser guarantees. Mitigation: the
  confidence ladder + mandatory human gate on UNCERTAIN is the designed backstop; we prefer surfacing over
  guessing.
- **R3 — PDF extraction quality varies** and can silently mangle prose (ligatures, columns). Mitigation:
  PDF extractions default to PROBABLE fidelity, forcing a review touch; the `.raw/` retention lets a human
  diff.
- **R4 — Writing into `source/` widens prep's write surface.** This is the biggest boundary concession.
  Justified because README already designates `source/` as the materialization target and the writes are
  new-file-only; but it does mean `source/` is no longer purely operator-provisioned. Accepted trade-off.
- **R5 — New NATIVE skill = one more VENDOR.md row to maintain.** Trivial cost; the alternative (dropping
  logic into an adopted skill's resources) would be worse for the sync boundary.
