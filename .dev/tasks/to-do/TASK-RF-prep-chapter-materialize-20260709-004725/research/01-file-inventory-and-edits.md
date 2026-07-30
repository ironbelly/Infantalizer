# Research: File Inventory & Edit Loci
Status: Complete
Date: 2026-07-09
Track: 1 of 1 — File Inventory & Exact Edit Loci
Spec: `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md` §11

---

## 0. MIRROR MAP (DEFINITIVE) — read this first

The `.claude/` tree mirrors `laf-adaptation/` via **directory/file symlinks**, NOT copies. This is the
single most important operational fact for the builder: editing the `laf-adaptation/` source file
updates the `.claude/` view automatically. There is NO `make sync-dev` step here and NO byte-copy to
keep in lockstep for the symlinked files. Verified 2026-07-09:

| Edited/new file (laf-adaptation-relative) | `.claude/` mirror | Mechanism | Builder action |
|---|---|---|---|
| `skills/prep/SKILL.md` | `.claude/skills/prep/SKILL.md` | `.claude/skills/prep` is a **symlink** -> `../../laf-adaptation/skills/prep` | Edit source only; mirror auto-updates. **No separate copy.** |
| `skills/prep/resources/path-contract.md` | `.claude/skills/prep/resources/path-contract.md` | same parent-dir symlink | Edit source only; auto-mirrors. **No separate copy.** |
| `agents/prep-cordinator.md` | `.claude/agents/prep-cordinator.md` | **symlink** -> `../../laf-adaptation/agents/prep-cordinator.md` | Edit source only; auto-mirrors. **No separate copy.** |
| `.claude/commands/laf/prep.md` | (IS the canonical file) | **real file, NO laf-adaptation source** — commands live ONLY under `.claude/` (no `laf-adaptation/commands/` dir exists) | Edit `.claude/commands/laf/prep.md` DIRECTLY. It is the only copy. |
| `VENDOR.md` | **no mirror** | not under `.claude` | Edit `laf-adaptation/VENDOR.md` only. |
| `source/README.md` | **no mirror** | not under `.claude` | Edit `laf-adaptation/source/README.md` only. |
| `skills/chapter-materialize/SKILL.md` (NEW) | none yet — `.claude/skills/chapter-materialize` **ABSENT** | mirror pattern is a **per-skill symlink** (e.g. `.claude/skills/prep -> ../../laf-adaptation/skills/prep`) | After authoring the new skill, create symlink `.claude/skills/chapter-materialize -> ../../laf-adaptation/skills/chapter-materialize` to match existing pattern. |
| `skills/chapter-materialize/resources/boundary-rules.yaml` (NEW) | covered by the above skill-dir symlink once created | — | No separate copy; the dir symlink covers `resources/`. |

Evidence:
- `ls -la .claude/skills/prep` -> `.claude/skills/prep -> ../../laf-adaptation/skills/prep` (symlink).
- `ls -la .claude/agents/prep-cordinator.md` -> `-> ../../laf-adaptation/agents/prep-cordinator.md` (symlink). Sibling agents (`analyst.md`, `chronicler.md`, `safety-verifier.md`, `tier-coordinator.md`) are all symlinks too — confirms the per-file symlink convention for agents.
- `find . -name prep.md -path '*commands*'` -> only `./.claude/commands/laf/prep.md`; `find laf-adaptation -type d -name commands` -> none. The command file has NO source-of-truth under `laf-adaptation/`.
- `find .claude -name VENDOR.md` -> empty; source `README.md` -> empty. VENDOR.md and source/README.md are NOT mirrored.
- `.claude/skills/chapter-materialize` and `laf-adaptation/skills/chapter-materialize` both ABSENT (confirmed NEW).

**Note on spec §11 wording** ("`.claude/` mirror updated in lockstep (existing mirroring)"): "existing mirroring" = the symlink scheme. For symlinked files the lockstep is automatic. The ONLY file requiring an explicit `.claude/` action is the NEW `chapter-materialize` skill dir, which needs a new symlink created to match convention.

---

## 1. `laf-adaptation/skills/prep/SKILL.md` — 125 lines — NATIVE

Mirror: `.claude/skills/prep/SKILL.md` via parent-dir symlink (auto). Edit source only.

### Section map (anchors -> line)
- Frontmatter: lines 1-8 (`name: prep`, description block).
- `# Adaptation Prep` title + intro: 10-13.
- `## §1 Path contract (single source of truth)`: **line 15**; body 17-19 (ends describing "8 fixed-name files `00`-`70`").
- `## §2 Challenge taxonomy`: line 21 (through table + §2.1 compound-scene, ends ~line 52).
- `## §3 Two-track work-level analysis (anti-hallucination)`: line 54; body 56-62.
- `## §4 Mapping authoring (derive + score)`: line 64.
- `## §5 Question-gate coverage rule`: line 77.
- `## §6 Greenlight`: line 87.
- `## §7 Handoff`: line 110.
- `## §8 Traceability`: line 116.
- `## Resources`: line 122; single bullet 124-125 pointing at `resources/path-contract.md`.

### Spec-required edits (§11 row: "+Stage-0 note in §1; pointer to `chapter-materialize`")
- **EDIT-A — §1 Stage-0 note.** Insert after **line 19** (end of §1 body, before blank line preceding `## §2` at line 21). State that a new **Stage 0: Source Materialization** precedes §3, materializes `source/<slug>/ch-<NN>.txt` + `chapter-manifest.yaml`, and that the manifest is a source sidecar (NOT a 9th package file, NOT in `rewrite_phase_reads`). Keep the "8 fixed-name files 00-70" statement at line 19 intact (spec N3 forbids a 9th package file).
- **EDIT-B — pointer to `chapter-materialize`.** Add a bullet under `## Resources`, after line 125 (EOF), pointing at the new `laf-adaptation:chapter-materialize` skill as the Stage-0 boundary-detection/normalization procedure.
- Lowest-collision loci: (a) after line 19, (b) after line 125.

---

## 2. `laf-adaptation/agents/prep-cordinator.md` — 98 lines — NATIVE (`laf_sha256 = —`, body edits boundary-clean)

Mirror: `.claude/agents/prep-cordinator.md` via file symlink (auto). Edit source only.

### Section map (anchors -> line)
- **Frontmatter: lines 1-15.**
  - `name`/`description`/`model`: 2-4.
  - **`skills:` block: lines 5-11** — six entries:
    - `- laf-adaptation:source-fidelity` (6), `-adaptation-tiers` (7), `-adaptation-rules` (8), `-kb-management` (9), `-prep` (10), `-thematic-fidelity` (11).
  - `tools: >` block: lines 12-14. `---` close: 15.
- `# Prep-Cordinator` title + intro: 17-28 (intro says "Owns the **8-stage** prep pipeline"; explicitly names "the two HALT gates (question gate, greenlight)" at line 26).
- `## Inputs` table: 30-36.
- `## Write scope`: 38-42.
- **`## The 8 stages`** heading: **line 44**. Fenced code block **lines 46-62** (```` ``` ```` at 46 and 62) listing STAGE 1..STAGE 8:
  - STAGE 1 RESEARCH: 47-49; STAGE 2 ROADMAP: 50; STAGE 3 ANALYZE (+CLASSIFY): 51-53; STAGE 4 MAPPING: 54; STAGE 5 Q-GATE (HALT gate #1): 55; STAGE 6 PACKAGE: 56; STAGE 7 GREENLIGHT (HALT gate #2): 57-60; STAGE 8 HANDOFF: 61.
- `### Stage notes`: line 64; bullets 66-98 (Stage 1 a/b, Stage 1c/3, Stage 3+CLASSIFY, Stage 4, Stage 5 [HALT], Stage 7 [HALT/CONFIRM], Stage 7 operator-clarity, Stage 8).

### The "8 stages" numbering block + both HALT gates (for consistency, per task note)
- The count "8-stage(s)" appears at: **line 20** (intro), **line 25** ("execute its 8-section procedure"), **heading line 44** (`## The 8 stages`), and the fenced block 46-62 numbers STAGE 1–8.
- HALT gate #1 = STAGE 5 Q-GATE (line 55) + Stage-5 note (line 80-82).
- HALT gate #2 = STAGE 7 GREENLIGHT (lines 57-60) + Stage-7 notes (83-97).
- Line 22 intro also enumerates the pipeline verbs ("research... classify... derive... ask... emit... gate... print").

### Spec-required edits (§11 row: "+1 `skills:` line + Stage-0 procedure paragraph")
- **EDIT-A — `skills:` line.** Insert `  - laf-adaptation:chapter-materialize` into the `skills:` block (lines 5-11). Precise locus: after **line 11** (`- laf-adaptation:thematic-fidelity`), before the `tools: >` line at 12. Spec §6/§11 says "one additive `skills:` frontmatter line." (Additive to a NATIVE agent — no boundary hash impact; row is `—`.)
- **EDIT-B — Stage-0 procedure paragraph + renumber.** The spec (§4) inserts STAGE 0 *before* the current STAGE 1 and RENUMBERS: STAGE 0 materialize; the current STAGE 1–8 become STAGE 1–... under the spec's new sequence (spec §4 "Stage sequence" maps old §2→STAGE1, §3→STAGE2, etc.). **Consistency-critical loci:**
  - Insert a `STAGE 0 MATERIALIZE` line at the TOP of the fenced block (after line 46 ```` ``` ````, before `STAGE 1 RESEARCH` at 47).
  - Update the count words at **line 20** ("8-stage" -> "9-stage" or reword to "Stage 0 + 8 stages"), **line 25** ("8-section" ref), and the **heading at line 44** (`## The 8 stages`).
  - Add a Stage-0 note bullet under `### Stage notes` (insert before the Stage-1 note at line 66, or as the first bullet). The Stage-0 paragraph must: run `/source-fidelity` Phase-0 ABORT-on-NO-ACCESS first (matches existing Stage-1b discipline at 66-68), detect mode, dispatch `chapter-materialize` inline for a plan (no writes), commit CERTAIN chapters + write `chapter-manifest.yaml`, defer PROBABLE/UNCERTAIN to the greenlight gate.
  - **Cross-gate consistency:** the spec (§4.0.5, §10) folds deferred `ambiguous_splits` into STAGE 5 Q-GATE (line 55 + note 80-82) and greenlight-commit into STAGE 7 (57-60 + notes 83-97). If the builder extends those gate descriptions, they must edit lines 55, 57-60, 80-82, 83-97 to reference Stage-0 deferred writes — but the task note says keep the "8 stages numbering block and both HALT gates consistent," so at minimum the renumber and the two gate references must stay coherent.
  - NOTE for builder: whether to renumber to "STAGE 0..8" (9 entries) vs "STAGE 1..9" is an authoring choice owned by researcher 04 (gate integration) / the builder; this inventory flags every locus that mentions the count so none is missed. The spec's own §4 diagram uses "STAGE 0..6" (it collapses old §7/§8 into one "STAGE 6"); the agent body uses a finer 8-stage decomposition. Reconcile deliberately.

---

## 3. `laf-adaptation/skills/prep/resources/path-contract.md` — 91 lines — NATIVE

Mirror: `.claude/skills/prep/resources/path-contract.md` via parent-dir symlink (auto). Edit source only.

### Section map (anchors -> line)
- Title `# Path Contract` + import note: 1-5 (note names the three importers: prep SKILL §1, `.claude/commands/laf/prep.md`, `.claude/commands/laf/rewrite.md`).
- **`## 1. Package location`: line 7**; body 9-20 (fenced `work/prep/<work-slug>/` 11-13; slug rule 18-20). **READ-SET-ADJACENT: BYTE-UNCHANGED per spec.**
- **`## 2. The 8 package files (fixed names, fixed order)`: line 22**; table 24-33. **BYTE-UNCHANGED per spec §12 (no 05-chapters.yaml, no 9th file).**
- `## 3. Promotion targets (on greenlight — dual-form)`: line 35; body 37-60.
- **`## 4. rewrite_phase_reads (the hardcoded read-set)`: line 62**; body 64-73. The 3-file read-set fenced block is **lines 66-70** (`30-mapping.yaml`, `40-prep-brief.md`, `10-challenges.yaml`); line 72 confirms greenlight; line 73 excludes `70-traceability.md`. **THE 3-FILE READ-SET MUST STAY BYTE-UNCHANGED (spec §12, AC6).**
- **`## 5. Write-ownership`: line 76**; table header 78, `|---|---|` 79, rows **80-82**:
  - row 80: `work/prep/<slug>/*` -> prep-cordinator
  - row 81: `kb/adaptation-mapping/<slug>-mapping.yaml` -> dual-form transform
  - row 82: `config/concept_mapping/templates/<slug>_mapping.yaml` -> dual-form
  - `kb/canon/*`, `kb/adaptations/...` row: 82? — actually the chronicler row is **line 82** in the read (line 82 = `| kb/canon/*, kb/adaptations/<slug>/tier-*/… | chronicler ...|`). Table body spans 80-82; then prose 84-85, and a "Form-transform operator" note 87-91 (EOF at 91/92).
- (No `## 6` exists yet — the NEW subsection.)

### Spec-required edits (§11 + §12 diff-style)
- **UNCHANGED (assert byte-identical):** §1 (lines 7-20), §2 (22-33), §4 read-set fenced block (66-70) and the whole §4 (62-73). Spec §12 & AC6 require these byte-unchanged.
- **EDIT-A — §4 explanatory note (manifest NOT in read-set).** Spec §12 adds an *explicit note* that `chapter-manifest.yaml` is a `source/` sidecar deliberately NOT in `rewrite_phase_reads`; the rewrite phase discovers chapters by the `source/<slug>/ch-<NN>.txt` convention. **Locus:** append as a new paragraph AFTER line 73 (end of §4 body), BEFORE `## 5.` at line 76 — this leaves the read-set fenced block 66-70 byte-untouched while adding the clarifying note in-section. (The note is additive prose after the read-set, not inside it.)
- **EDIT-B — §5 three write-ownership rows.** Insert THREE rows into the §5 table (78-82). **Locus:** insert after the existing `work/prep/<slug>/*` row (line 80), before the promotion-target rows, OR grouped with the source rows — simplest is to insert immediately after line 80:
  - `| source/<slug>/ch-<NN>.txt | prep-cordinator (Stage 0) |`
  - `| source/<slug>/chapter-manifest.yaml | prep-cordinator (Stage 0) |`
  - `| source/<slug>/.raw/* | prep-cordinator (Stage 0) |`
  (Exact rows dictated by spec §12 lines 259-261.) Ensure `|`-free per VENDOR.md format constraint — these paths contain no `|`, OK.
- **EDIT-C — NEW `## 6. Source-side chapter manifest` subsection.** Spec §12 line 262: NEW §6 "Source-side chapter manifest" — path, schema summary, non-membership-in-read-set note. **Locus:** append at EOF after the §5 Form-transform note (after line 91/92). Content: manifest path `source/<slug>/chapter-manifest.yaml`, schema pointer (`schema_version: laf.chapter_manifest.v1`, defer full schema to the chapter-materialize skill authored by researcher 03), and restate it is NOT a numbered package file and NOT a `rewrite_phase_reads` member.

---

## 4. `laf-adaptation/source/README.md` — 23 lines — BUILD-NEW

Mirror: **NONE** (`source/` not mirrored under `.claude`). Edit source only.

### Section map (anchors -> line)
- Title `# source/ — the work being adapted (read-only reference)`: line 1.
- Layout line: 3 (`source/<work>/ch-<NN>.txt` — one chapter per file, UTF-8).
- Intro bullets: 5-7 (analyst reads a chapter as `source_path`; nothing transformed in place — writes go to `work/`/`kb/`).
- `## Provisioning contract (Phase-3 proof, ...)`: line 9; body 11-23 (PATH A / PATH B, tolkien fixture note). EOF line 23.

### Spec-required edits (§11 row: "+manifest + `.raw/` subsection")
- **EDIT — new subsection describing the manifest + `.raw/` retention.** Spec §4.0.4 & §8: raw input retained at `source/<slug>/.raw/<file>`; `chapter-manifest.yaml` co-located with chapters. **Locus:** insert a new `## Materialization outputs` (or similar) subsection. Cleanest placement: after the layout/intro bullets (after line 7), before `## Provisioning contract` at line 9 — OR append at EOF (after line 23). Because line 3 states the layout, the natural spot to extend the layout description is right after line 7. Content: document `source/<slug>/chapter-manifest.yaml` (the confidence-tagged sidecar, written by prep-cordinator Stage 0) and `source/<slug>/.raw/` (retained original inputs as the fidelity anchor; read-only after materialize; new files only, never in-place edits).

---

## 5. `.claude/commands/laf/prep.md` — 20 lines — NATIVE mirror (but IS the canonical file; NO laf-adaptation source)

Mirror: **this file IS the canonical copy.** There is no `laf-adaptation/commands/` dir. Edit
`.claude/commands/laf/prep.md` directly.

### Section map (anchors -> line)
- **Frontmatter: lines 1-4.**
  - `description:` line 2.
  - **`argument-hint: "<novel title>" [--source <path-or-url>]` : line 3** — THIS is the arg-hint to extend.
  - `---` close: line 4.
- `# /laf:prep` title: line 6.
- Delegation paragraph (delegate to prep-cordinator, pass positional + `--source`): 8-9.
- "owns 8-stage procedure + two HALT gates" paragraph: 11-13 (mentions the two gates; references SKILL.md + path-contract.md).
- `--source` omitted -> elicit as required input: 15-16.
- `--source` accepts local path / URL fetched first: 18-20. Line 20 notes the `<path-or-url>` arg-hint is "kept verbatim per `prep-agent-schemas.md §5.1`". EOF line 20.

### Spec-required edits (§11 row: "+`--source-mode`; `--source` may be dir/file/adopt-set")
- **EDIT-A — extend `argument-hint` (line 3).** Change line 3 to:
  `argument-hint: "<novel title>" [--source <path-or-url>] [--source-mode auto|folder|file|adopt]`
  (Spec §3 line 56 gives this exact hint.) **Caveat:** line 20 says the `<path-or-url>` hint is "kept verbatim per `prep-agent-schemas.md §5.1`" — appending `--source-mode` is additive and preserves the verbatim `<path-or-url>` token, so it's consistent; the builder should keep `<path-or-url>` intact and only append the new flag.
- **EDIT-B — document `--source-mode` + broadened `--source` semantics.** In the body (the `--source` paragraph 18-20, or a new paragraph after 20), state: `--source-mode auto|folder|file|adopt` (NEW, optional, default `auto`) is the operator override for ambiguous auto-detect; and `--source` may now resolve to a **directory** (Mode A folder), a **single file** (Mode B), or an already-split **`source/<slug>/`** set (Mode C adopt); a URL is fetched to `.raw/` first. **Locus:** extend/replace the paragraph at lines 18-20 and/or append a new paragraph after line 20. Spec §3 lines 50-65 are the source text.

---

## 6. `laf-adaptation/VENDOR.md` — 126 lines — NATIVE

Mirror: **NONE** (not under `.claude`). Edit source only.

### Section map (anchors -> line)
- Header block (upstream_repo/sha/license/prefix_rewrite): 1-7.
- `## Hash semantics`: 9-24.
- `### What Mode V catches — and what it does NOT`: 26-38.
- `## Format constraint`: 40-42 (the `|`-in-cell rule — relevant to new rows).
- `## Invariants (asserted by check_boundary.py)`: 44-49.
- Re-vendor HTML comment: 51-54.
- **`## Manifest`: line 56**; table header `| path | class | upstream_sha256 | laf_sha256 |` **line 58**; separator `|------|...` **line 59**.
- ADOPTED rows: 60-115.
- **NATIVE / BUILD-NEW rows (glob-form, both hashes `—`): lines 116-126.**
  - `agents/analyst.md` NATIVE (116); `agents/safety-verifier.md` NATIVE (117); `skills/adaptation-rules/**` (118); `skills/adaptation-tiers/**` (119); `skills/source-fidelity/**` (120); **`agents/prep-cordinator.md` NATIVE (121)**; **`skills/prep/**` NATIVE (122)**; `skills/thematic-fidelity/**` (123); `agents/chronicler.md` BUILD-NEW (124); `agents/tier-coordinator.md` BUILD-NEW (125); `skills/adaptation-safety/**` BUILD-NEW (126). EOF line 126 (no trailing newline shown).

### Spec-required edit (§11 row: "+1 NATIVE row for `chapter-materialize/SKILL.md` (Rule F)")
- **EDIT — add ONE NATIVE manifest row** so Rule F (every managed `skills/**/SKILL.md` is manifested) stays green for the new skill. **Locus:** insert into the NATIVE-rows block (116-126). Existing NATIVE skill rows use the **glob form** `skills/<name>/**` (e.g. line 118 `skills/adaptation-rules/** | NATIVE | — | —`). Match that convention:
  `| skills/chapter-materialize/** | NATIVE | — | —`
  Insert alphabetically/logically among the NATIVE skill rows — natural spot is right after line 118 (`skills/adaptation-rules/**`) or grouped with the other `skills/*` NATIVE rows (118-120, 122-123). The `**` glob form covers BOTH `SKILL.md` and `resources/boundary-rules.yaml` in one row, satisfying Rule F/F′ (CH-2: every file under a skill's resources/** manifested) with a single line — matches how `skills/adaptation-rules/**` covers its whole tree.
  - **Format constraint (lines 40-42):** the path/hashes must contain no literal `|`. `skills/chapter-materialize/**` is `|`-free. OK.
  - **Class:** NATIVE per spec §11 ("NEW NATIVE"). Both hash columns `—` (NO_HASH) per Hash-semantics rule (lines 18-19): NATIVE rows carry `—` for both.

---

## 7. `laf-adaptation/skills/chapter-materialize/SKILL.md` — NEW (CONFIRMED ABSENT)

Mirror: none yet. After authoring, create `.claude/skills/chapter-materialize` symlink ->
`../../laf-adaptation/skills/chapter-materialize` (matches the `.claude/skills/prep` symlink pattern).

- Confirmed absent: `ls laf-adaptation/skills/chapter-materialize` -> "No such file or directory"; `.claude/skills/chapter-materialize` also absent.
- Authoring (SKILL.md body: split/normalize/adopt procedure, multi-signal evidence layers, confidence rule) is **researcher 03's scope** — NOT this track. This inventory only confirms the path is free (Rule E: no upstream `chapter-materialize` collision — none of the 12 ADOPTED skill dirs is named `chapter-materialize`; verified against VENDOR.md rows 71-115 and the `.claude/skills` listing).
- Frontmatter dialect (CLAUDE.md §3): skills use `name` + `description` ONLY.

## 8. `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` — NEW (CONFIRMED ABSENT)

Mirror: covered by the skill-dir symlink above once created (no separate copy).

- Confirmed absent (parent dir does not exist).
- Authoring (declarative signal ruleset) is **researcher 03's scope**.
- Manifest coverage: the single `skills/chapter-materialize/** | NATIVE | — | —` VENDOR.md row (see §6 EDIT) covers this file via the `**` glob — no separate manifest row needed.

---

## Summary

**Mirror mechanics (the load-bearing operational finding):** `.claude/` mirrors `laf-adaptation/` by
**symlink**, not copy. `.claude/skills/prep` and `.claude/agents/prep-cordinator.md` are symlinks, so
editing the `laf-adaptation/` source auto-updates the mirror — no lockstep copy step. The ONLY files
NOT auto-mirrored / needing explicit `.claude/` action:
1. `.claude/commands/laf/prep.md` — the canonical command file (no laf source); edit directly.
2. The NEW `chapter-materialize` skill dir — after authoring, create `.claude/skills/chapter-materialize`
   symlink to match convention.
`VENDOR.md` and `source/README.md` have no `.claude` mirror at all.

**Per-file edit-locus quick index (all line numbers verified 2026-07-09):**
| File | Lines | Edit loci |
|---|---|---|
| `skills/prep/SKILL.md` | 125 | §1 note after L19; Resources pointer after L125 |
| `agents/prep-cordinator.md` | 98 | `skills:` line after L11; STAGE-0 in fenced block after L46; count words at L20/L25/L44; Stage-0 note before L66; gate refs L55, L57-60, L80-82, L83-97 |
| `skills/prep/resources/path-contract.md` | 91 | §4 note after L73 (read-set L66-70 & §1/§2/§4 BYTE-UNCHANGED); +3 §5 rows after L80; NEW §6 at EOF (after L91) |
| `source/README.md` | 23 | new subsection after L7 or EOF |
| `.claude/commands/laf/prep.md` | 20 | arg-hint L3; `--source-mode`/`--source` body L18-20 + after L20 |
| `VENDOR.md` | 126 | +1 NATIVE row in block L116-126 (glob form `skills/chapter-materialize/**`) |
| `skills/chapter-materialize/SKILL.md` | NEW | absent — author (r03); path Rule-E clean |
| `skills/chapter-materialize/resources/boundary-rules.yaml` | NEW | absent — author (r03) |

**Boundary-contract notes:**
- `prep-cordinator.md` is NATIVE (`laf_sha256 = —`, VENDOR.md L121) — body edits are boundary-clean (no hash to update). Same for `skills/prep/**` (L122).
- The new skill row must use the `**` glob form (like L118 `skills/adaptation-rules/**`), covering SKILL.md + boundary-rules.yaml in one Rule-F/F′-satisfying line; both hashes `—`.
- No ADOPTED body is touched by any of these edits. `writer.md`, `check_boundary.py`, the frozen 3-file `rewrite_phase_reads` (path-contract §4 L66-70), and the 8-file package table (path-contract §2 L24-33) all stay byte-unchanged — consistent with spec AC6 / N3.

Status: Complete
