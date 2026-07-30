# Discovery Consolidation: Edit Loci & Three-Way Numbering Map

**Task:** TASK-RF-prep-chapter-materialize-20260709-004725
**Step:** 1.3 (consolidation)
**Date:** 2026-07-09
**Sources:** `research/01-file-inventory-and-edits.md` (verified per-file edit loci + `.claude/` symlink mirror map), `research/04-mdtm-template-and-gate.md` (resolved STAGE-0 renumber decision Approach A + three-way numbering map)
**Spec:** `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md`

This artifact consolidates the verified edit loci (line numbers AND stable content anchors), the `.claude/` mirror mechanism per file, the three-way numbering map (agent STAGE 0..8 / prep SKILL §1..§8 / spec STAGE 0..6 conceptual), and the BYTE-UNCHANGED spans. Every locus and anchor below is copied VERBATIM from the research; no invented line numbers.

---

## (a) Per-File Edit Loci Table — all nine authored/edited files

| File Path | Edit ID | Line Anchor | Content Anchor | Exact Change Summary | `.claude` Mirror Mechanism |
|---|---|---|---|---|---|
| `laf-adaptation/skills/chapter-materialize/SKILL.md` | NEW (author) | NEW — CONFIRMED ABSENT | `ls laf-adaptation/skills/chapter-materialize` -> "No such file or directory"; frontmatter `name` + `description` ONLY (CLAUDE.md §3) | Author NEW skill body (split/normalize/adopt procedure, multi-signal evidence layers, confidence rule) — researcher 03's scope; path is Rule-E clean (no upstream `chapter-materialize` collision) | symlink-auto (create after authoring: `.claude/skills/chapter-materialize -> ../../laf-adaptation/skills/chapter-materialize`, matching the `.claude/skills/prep` symlink pattern) |
| `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` | NEW (author) | NEW — CONFIRMED ABSENT | parent dir does not exist | Author NEW declarative signal ruleset — researcher 03's scope; manifest coverage via the single `skills/chapter-materialize/**` VENDOR.md glob row (no separate row) | symlink-auto (covered by the skill-dir symlink above once created; no separate copy) |
| `.claude/skills/chapter-materialize` (symlink) | NEW (create symlink) | NEW — `.claude/skills/chapter-materialize` **ABSENT** | mirror pattern is a **per-skill symlink** (e.g. `.claude/skills/prep -> ../../laf-adaptation/skills/prep`) | After authoring the new skill, create symlink `.claude/skills/chapter-materialize -> ../../laf-adaptation/skills/chapter-materialize` to match existing pattern | symlink-auto (this IS the explicit symlink-creation action) |
| `laf-adaptation/agents/prep-cordinator.md` | EDIT-A (`skills:` line) | Insert after **line 11** (`- laf-adaptation:thematic-fidelity`), before the `tools: >` line at 12 | `skills:` block lines 5-11; six entries `- laf-adaptation:source-fidelity` (6), `-adaptation-tiers` (7), `-adaptation-rules` (8), `-kb-management` (9), `-prep` (10), `-thematic-fidelity` (11) | Insert `  - laf-adaptation:chapter-materialize` into the `skills:` block. Additive to a NATIVE agent — no boundary hash impact (row is `—`) | symlink-auto (`.claude/agents/prep-cordinator.md` -> `../../laf-adaptation/agents/prep-cordinator.md`; edit source only, auto-mirrors) |
| `laf-adaptation/agents/prep-cordinator.md` | EDIT-B (STAGE-0 block + renumber) | Insert `STAGE 0 MATERIALIZE` line at TOP of fenced block (after line 46 ```` ``` ````, before `STAGE 1 RESEARCH` at 47); update count words at **line 20** ("8-stage" -> reword), **line 25** ("8-section" ref — see numbering note), **heading at line 44** (`## The 8 stages`); add Stage-0 note bullet before Stage-1 note at **line 66**; cross-gate refs at lines **55**, **57-60**, **80-82**, **83-97** | `## The 8 stages` heading line 44; fenced block lines 46-62 (```` ``` ```` at 46 and 62) listing STAGE 1..STAGE 8; `### Stage notes` line 64, bullets 66-98; HALT gate #1 = STAGE 5 Q-GATE (line 55) + note 80-82; HALT gate #2 = STAGE 7 GREENLIGHT (57-60) + notes 83-97 | Prepend STAGE 0 MATERIALIZE (0.1-0.5 sub-steps: run `/source-fidelity` Phase-0 ABORT-on-NO-ACCESS first, detect mode, dispatch `chapter-materialize` inline for a plan no writes, commit CERTAIN chapters + write `chapter-manifest.yaml`, defer PROBABLE/UNCERTAIN to greenlight); keep STAGE 1..8 byte-stable; EXTEND STAGE 5 note ("also receives Stage-0 `ambiguous_splits`") and STAGE 7 note (+1 greenlight checklist line, deferred `ch-NN.txt` commit-on-confirm, `chapter-manifest.review.status: CONFIRMED`) without renumbering | symlink-auto (same file symlink; edit source only) |
| `laf-adaptation/skills/prep/SKILL.md` | EDIT-A (§1 Stage-0 note) | Insert after **line 19** (end of §1 body, before blank line preceding `## §2` at line 21) | `## §1 Path contract (single source of truth)` line 15; body 17-19 (ends describing "8 fixed-name files `00`-`70`") | State that a new **Stage 0: Source Materialization** precedes §3, materializes `source/<slug>/ch-<NN>.txt` + `chapter-manifest.yaml`, and that the manifest is a source sidecar (NOT a 9th package file, NOT in `rewrite_phase_reads`). Keep the "8 fixed-name files 00-70" statement at line 19 intact (spec N3 forbids a 9th package file) | symlink-auto (`.claude/skills/prep/SKILL.md` via parent-dir symlink; edit source only) |
| `laf-adaptation/skills/prep/SKILL.md` | EDIT-B (chapter-materialize pointer) | Add bullet under `## Resources`, after **line 125** (EOF) | `## Resources` line 122; single bullet 124-125 pointing at `resources/path-contract.md` | Add a bullet under `## Resources` pointing at the new `laf-adaptation:chapter-materialize` skill as the Stage-0 boundary-detection/normalization procedure | symlink-auto (same parent-dir symlink; edit source only) |
| `.claude/commands/laf/prep.md` | EDIT-A (extend `argument-hint`) | Change **line 3** | `argument-hint: "<novel title>" [--source <path-or-url>]` : line 3; line 20 notes `<path-or-url>` arg-hint is "kept verbatim per `prep-agent-schemas.md §5.1`" | Change line 3 to: `argument-hint: "<novel title>" [--source <path-or-url>] [--source-mode auto|folder|file|adopt]` (spec §3 line 56). Keep `<path-or-url>` intact; only append the new flag | canonical-direct (this file IS the canonical copy — NO `laf-adaptation/commands/` dir; edit `.claude/commands/laf/prep.md` directly) |
| `.claude/commands/laf/prep.md` | EDIT-B (`--source-mode` + broadened `--source`) | Extend/replace the paragraph at lines **18-20** and/or append a new paragraph after **line 20** | `--source` accepts local path / URL fetched first: 18-20; EOF line 20 | State `--source-mode auto|folder|file|adopt` (NEW, optional, default `auto`) is the operator override for ambiguous auto-detect; `--source` may now resolve to a **directory** (Mode A folder), a **single file** (Mode B), or an already-split **`source/<slug>/`** set (Mode C adopt); a URL is fetched to `.raw/` first. Spec §3 lines 50-65 | canonical-direct (edit `.claude/commands/laf/prep.md` directly) |
| `laf-adaptation/skills/prep/resources/path-contract.md` | EDIT-A (§4 explanatory note) | Append as a new paragraph AFTER **line 73** (end of §4 body), BEFORE `## 5.` at line 76 | `## 4. rewrite_phase_reads (the hardcoded read-set)` line 62; body 64-73; 3-file read-set fenced block lines 66-70 (`30-mapping.yaml`, `40-prep-brief.md`, `10-challenges.yaml`); line 72 confirms greenlight; line 73 excludes `70-traceability.md` | Add explicit note that `chapter-manifest.yaml` is a `source/` sidecar deliberately NOT in `rewrite_phase_reads`; the rewrite phase discovers chapters by the `source/<slug>/ch-<NN>.txt` convention. Additive prose after the read-set — leaves the read-set fenced block 66-70 byte-untouched | symlink-auto (`.claude/skills/prep/resources/path-contract.md` via parent-dir symlink; edit source only) |
| `laf-adaptation/skills/prep/resources/path-contract.md` | EDIT-B (§5 three write-ownership rows) | Insert immediately after **line 80** (`work/prep/<slug>/*` row), before the promotion-target rows | `## 5. Write-ownership` line 76; table header 78, `|---|---|` 79, rows 80-82 | Insert THREE rows: `| source/<slug>/ch-<NN>.txt | prep-cordinator (Stage 0) |`, `| source/<slug>/chapter-manifest.yaml | prep-cordinator (Stage 0) |`, `| source/<slug>/.raw/* | prep-cordinator (Stage 0) |` (spec §12 lines 259-261; `|`-free, OK) | symlink-auto (same parent-dir symlink; edit source only) |
| `laf-adaptation/skills/prep/resources/path-contract.md` | EDIT-C (NEW §6 subsection) | Append at EOF after the §5 Form-transform note (after **line 91/92**) | `## 6. Source-side chapter manifest` does NOT exist yet (NEW subsection); §5 prose 84-85 + "Form-transform operator" note 87-91 (EOF at 91/92) | Add NEW `## 6. Source-side chapter manifest`: manifest path `source/<slug>/chapter-manifest.yaml`, schema pointer (`schema_version: laf.chapter_manifest.v1`, defer full schema to the chapter-materialize skill), restate NOT a numbered package file and NOT a `rewrite_phase_reads` member (spec §12 line 262) | symlink-auto (same parent-dir symlink; edit source only) |
| `laf-adaptation/source/README.md` | EDIT (manifest + `.raw/` subsection) | Insert new subsection after **line 7** (before `## Provisioning contract` at line 9) — OR append at EOF (after **line 23**) | Title line 1; layout line 3 (`source/<work>/ch-<NN>.txt`); intro bullets 5-7; `## Provisioning contract (Phase-3 proof, ...)` line 9; body 11-23 (EOF line 23) | Add new `## Materialization outputs` (or similar) subsection documenting `source/<slug>/chapter-manifest.yaml` (confidence-tagged sidecar, written by prep-cordinator Stage 0) and `source/<slug>/.raw/` (retained original inputs as the fidelity anchor; read-only after materialize; new files only, never in-place edits). Spec §4.0.4 & §8 | no-mirror (`source/` not mirrored under `.claude`; edit source only) |
| `laf-adaptation/VENDOR.md` | EDIT (1 NATIVE manifest row) | Insert into the NATIVE-rows block (**116-126**); natural spot right after **line 118** (`skills/adaptation-rules/**`) | `## Manifest` line 56; table header `| path | class | upstream_sha256 | laf_sha256 |` line 58; separator line 59; NATIVE/BUILD-NEW rows (glob-form, both hashes `—`) lines 116-126; `agents/prep-cordinator.md` NATIVE (121); `skills/prep/**` NATIVE (122); `## Format constraint` 40-42 (`|`-in-cell rule) | Add ONE NATIVE row `| skills/chapter-materialize/** | NATIVE | — | —` (glob form covers SKILL.md + boundary-rules.yaml in one Rule-F/F′-satisfying line; both hashes `—` per Hash-semantics rule lines 18-19; `|`-free per Format constraint) | no-mirror (not under `.claude`; edit source only) |

Note: the task's nine-file enumeration is captured above. The `.claude/skills/chapter-materialize` symlink is a distinct explicit action row (listed after the two NEW files it mirrors); the multi-locus files (`prep-cordinator.md`, `prep/SKILL.md`, `.claude/commands/laf/prep.md`, `path-contract.md`) appear once per Edit ID for locus precision.

---

## (b) Three-Way Numbering Map

**Explicit rule:** *prepend STAGE 0, keep STAGE 1..8 byte-stable, Q-gate stays STAGE 5, greenlight stays STAGE 7.*

Resolved authoring decision (research 04, Step 3): **Approach A — a new numbered STAGE 0 (prepended; the agent pipeline becomes STAGE 0..8, i.e. 9 stages).**

**CRITICAL FINDING — three distinct numbering systems are in play (verbatim, research 04 L106-110):**

1. **prep-cordinator agent body:** STAGE **1..8** (Q-gate=STAGE 5, greenlight=STAGE 7). ← the numbers the builder physically edits.
2. **prep SKILL.md:** §**1..§8** (question-gate=§5, greenlight=§6). ← unchanged section labels.
3. **spec §4 table:** STAGE **0..6** (a re-map of the prep SKILL §-sequence, NOT the agent's stage numbers; its "STAGE 4 §5 question gate / STAGE 5 §6 greenlight" columns confirm it is indexing the SKILL §-sequence).

The spec's STAGE 0..6 table is a **conceptual pipeline view**, not an instruction to renumber the agent's 8-stage block to 0..6. Conflating the two is the trap the builder must avoid.

| Numbering system | Range | Q-gate location | Greenlight location | Change under Approach A |
|---|---|---|---|---|
| Agent body (prep-cordinator.md) — what the builder physically edits | STAGE **0..8** (9 stages after prepend) | STAGE 5 (unchanged) | STAGE 7 (unchanged) | Prepend STAGE 0 MATERIALIZE; STAGE 1..8 byte-stable; zero downstream renumber; no "Stage 5"/"Stage 7" note-reference breakage |
| prep SKILL.md — section labels | §**1..§8** | §5 | §6 | UNCHANGED (spec §11 L241 only adds a "§1 Stage-0 note + pointer") |
| spec §4 table — conceptual only | STAGE **0..6** | STAGE 4 (indexes SKILL §5) | STAGE 5 (indexes SKILL §6) | Conceptual view only; NOT transcribed as literal renumbering into agent or skill |

**Net three-way mapping (research 04 L140):** agent = STAGE 0..8 (9 stages); skill = §1..§8 (unchanged); spec table = 0..6 (conceptual only). The builder edits each artifact in its own numbering system.

**Consistency contract the builder MUST honor under Approach A (verbatim, research 04 L132-138):**
- Change the two "8 stages"/"8-section procedure" prose mentions (agent L20 "the 8-stage prep pipeline", L22, L25 "8-section procedure" — note L25 refers to the **SKILL's** §-count which is still 8, so **leave L25 as "8-section procedure"**; only the **agent stage count** L20/L22 becomes 9). Verify each mention's referent before editing (skill §-count = 8, unchanged; agent stage-count = 9).
- Insert `STAGE 0 MATERIALIZE …` as the first entry of the fenced "## The N stages" block (agent L46-62), keeping STAGE 1..8 lines byte-identical.
- Add a `### Stage notes` bullet for **Stage 0** (mirroring the 0.1-0.5 sub-steps, the inline `chapter-materialize` dispatch, the deferred-write invariant, and the 0.5→Stage-5 gate hook) WITHOUT renumbering any existing "Stage N" note.
- In the STAGE 5 Q-GATE note (agent L80-82) add the spec §10 fold ("also receives Stage-0 `ambiguous_splits`") — this EXTENDS the existing STAGE 5, it does not renumber it.
- In the STAGE 7 GREENLIGHT note (agent L83-97) add: the +1 greenlight checklist line, the deferred `ch-NN.txt` commit-on-confirm, and `chapter-manifest.review.status: CONFIRMED` — EXTENDS STAGE 7, no renumber.
- Add the additive `skills:` line `- laf-adaptation:chapter-materialize` to frontmatter (agent L5-11) — additive only, boundary-clean per CLAUDE.md §2.

---

## (c) BYTE-UNCHANGED Spans

Per spec §12 & AC6, the following spans MUST stay byte-identical:

| Span | Location | Requirement |
|---|---|---|
| path-contract §1 Package location | `path-contract.md` **lines 7-20** (`## 1. Package location` line 7; body 9-20; fenced `work/prep/<work-slug>/` 11-13; slug rule 18-20) | READ-SET-ADJACENT: BYTE-UNCHANGED per spec |
| path-contract §2 The 8 package files | `path-contract.md` **lines 22-33** (`## 2. The 8 package files (fixed names, fixed order)` line 22; table 24-33) | BYTE-UNCHANGED per spec §12 (no 05-chapters.yaml, no 9th file) |
| path-contract §4 rewrite_phase_reads (the 3-file read-set) | `path-contract.md` **lines 66-70** (fenced read-set block: `30-mapping.yaml`, `40-prep-brief.md`, `10-challenges.yaml`) | THE 3-FILE READ-SET MUST STAY BYTE-UNCHANGED (spec §12, AC6) |
| path-contract whole §4 | `path-contract.md` **lines 62-73** (`## 4. rewrite_phase_reads (the hardcoded read-set)` line 62; body 64-73; line 72 confirms greenlight; line 73 excludes `70-traceability.md`) | UNCHANGED (assert byte-identical): whole §4 (62-73) per spec §12 & AC6 |
| The 8-file package table | `path-contract.md` §2 table **lines 24-33** (the 8 fixed-name package files) | Byte-unchanged; consistent with spec AC6 / N3 |

**Additional boundary-clean invariants (research 01 §Summary L234):** No ADOPTED body is touched by any of these edits. `writer.md`, `check_boundary.py`, the frozen 3-file `rewrite_phase_reads` (path-contract §4 L66-70), and the 8-file package table (path-contract §2 L24-33) all stay byte-unchanged — consistent with spec AC6 / N3.

**Edits that must NOT disturb these spans:** path-contract EDIT-A is additive prose AFTER line 73 (leaves read-set fenced block 66-70 byte-untouched); EDIT-B inserts §5 rows after line 80 (below §4); EDIT-C appends NEW §6 at EOF. None touches §1 (7-20), §2 (22-33), or §4 (62-73).
