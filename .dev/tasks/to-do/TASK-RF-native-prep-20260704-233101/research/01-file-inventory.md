# Research: File Inventory

Status: Complete
Date: 2026-07-04
Topic: File Inventory — every file the native LAF adaptation-prep phase implementation touches
Repo root: /config/workspace/Infantalizer

---

## Method

- Design pack read: `docs/native-prep/design/*.md` (6 files: DESIGN.md, prep-agent-schemas.md, prep-skill-specs.md, path-contract.md, package-schemas.md, boundary-verification.md).
- Existence probe via `find laf-adaptation -type f` + `ls .claude/commands/laf/` (see run at task start).
- Edit anchors verified against the actual current file contents (line numbers cited below).

---

## Category 1 — NEW files to CREATE (all confirmed ABSENT)

Existence probe: `find laf-adaptation -type f` at task start + `ls .claude/commands/laf/` (returned "No such file or directory"). None of the paths below appear in the tree. All ABSENT. Design layout authority: `docs/native-prep/design/DESIGN.md` §2 (lines 98–130) and §1.1 (lines 55–70).

| # | Full relative path | Purpose (1 sentence) | Existence | Provenance / VENDOR row |
|---|---|---|---|---|
| N1 | `laf-adaptation/agents/prep-cordinator.md` | NATIVE opus orchestrator that owns the 8-stage prep pipeline (research→handoff). | **ABSENT** | NEW NATIVE. `--init` writes 1 row: `agents/prep-cordinator.md \| NATIVE \| — \| —` (DESIGN §5 line 267). Note the deliberate spelling `prep-cordinator` (name = filename stem; prep-agent-schemas.md lines 44–47). |
| N2 | `laf-adaptation/skills/prep/SKILL.md` | NATIVE skill body: the 8-section prep procedure the coordinator loads. | **ABSENT** | NEW NATIVE. `--init` writes 1 row: `skills/prep/** \| NATIVE \| — \| —` (DESIGN §5 line 268). |
| N3 | `laf-adaptation/skills/prep/resources/path-contract.md` | Single-source-of-truth path layout resource (8-file package + promotion targets), imported by reference (R3). | **ABSENT** | NEW NATIVE. No new row — covered by the `skills/prep/**` glob (DESIGN §5 line 272). |
| N4 | `laf-adaptation/skills/thematic-fidelity/SKILL.md` | NATIVE skill carrying the meaning-preservation concept (Hutcheon/Bortolotti). | **ABSENT** | NEW NATIVE. `--init` writes 1 row: `skills/thematic-fidelity/** \| NATIVE \| — \| —` (DESIGN §5 line 269). |
| N5 | `laf-adaptation/skills/adaptation-rules/resources/exemplars/sacrifice-and-return.md` | Seed exemplar (DERIVED-marked) for the sacrifice-and-return theme (R13). | **ABSENT** | NEW NATIVE. No new row — covered by existing `skills/adaptation-rules/**` NATIVE glob (VENDOR.md line 113; DESIGN §5 line 272, spec-correction C3/C4). |
| N6 | `laf-adaptation/skills/adaptation-rules/resources/exemplars/betrayal-and-redemption.md` | Seed exemplar for the betrayal-and-redemption theme (R13). | **ABSENT** | NEW NATIVE. Same glob coverage as N5. |
| N7 | `laf-adaptation/skills/adaptation-rules/resources/exemplars/petrification-body-horror.md` | Seed exemplar for the petrification/body-horror theme (R13). | **ABSENT** | NEW NATIVE. Same glob coverage as N5. |
| N8 | `.claude/commands/laf/prep.md` | Thin `/laf:prep` delegator → dispatches to `prep-cordinator` (R1). | **ABSENT** (dir `.claude/commands/laf/` does not exist) | NEW harness surface. **NOT VENDOR-manifested** — lives outside `laf-adaptation/` (DESIGN §6 C1 line 291; §5 line 277). |
| N9 | `.claude/commands/laf/rewrite.md` | Thin `/laf:rewrite --work <slug>` delegator that reads the 3 hardcoded package paths and hands to `muse` (R9). | **ABSENT** | NEW harness surface. NOT VENDOR-manifested (same as N8). |

**Existence caveat (parent dirs):** `laf-adaptation/skills/prep/`, `laf-adaptation/skills/thematic-fidelity/`, `laf-adaptation/skills/adaptation-rules/resources/exemplars/`, and `.claude/commands/laf/` are all ABSENT and must be created. `laf-adaptation/skills/adaptation-rules/resources/` DOES exist (holds `agency.md`, `character.md`, `thematic.md`) — only the `exemplars/` subdir is new.

---

## Category 2 — EDIT targets (exact anchor headings + line ranges)

Both edit targets read in full. Both are NO_HASH in VENDOR.md, so body edits are boundary-safe and require NO VENDOR change (DESIGN §1.1 lines 76–78).

### E1 — `laf-adaptation/agents/analyst.md`  (NATIVE; VENDOR.md line 111 = `NATIVE | — | —`; 65 lines total)

Purpose: NATIVE entry-point agent — pre-orchestration source-chapter analysis producing confidence-tagged facts and the Phase-0 ABORT gate. Diff authority: `docs/native-prep/design/prep-agent-schemas.md §3` (lines 104–165).

Three additive changes, each preserving current per-chapter behavior by default:

| Change | Anchor heading (current) | Exact line span in current file | What lands |
|---|---|---|---|
| **E1a — new Inputs** | `## Inputs (passed by the caller)` (line **18**) | insert AFTER `- \`chapter\` — the chapter number \`<NN>\`.` (line **21**); before blank line 22 / the `active_tier is NOT an input` note (line 23) | Add two bullets: `- \`granularity\` — \`chapter\` (default) \| \`work\`…` and `- \`out_path\` — output file path. Default \`work/analysis/ch-<NN>.yaml\`…` (schema-lines from prep-agent-schemas.md lines 117–121). |
| **E1b — new output fields** | `## Output contract` (line **51**) — specifically the `transformation_flags:` schema it references | The schema block being extended is the `transformation_flags`→`uncertainties` block shown in prep-agent-schemas.md lines 130–143. In the analyst body this is described prose at lines **51–65** (Output contract §); the literal YAML schema lives in `/source-fidelity` + `package-schemas.md §3`. Add `meaning:` (value+confidence), `compound_scene: true\|false`, and `compound_scenes:` list between `transformation_flags` and `uncertainties`. | Two additive output keys `meaning` + `compound_scene` (R10, R11). |
| **E1c — Hard-behavior paragraph** | `## Hard behavior (in this agent body, not delegated to a skill)` (line **33**), specifically AFTER the Phase-0 fenced block ending at line **39** | insert the new paragraph after the Phase-0 code block (line 39), before the `Observable-test decision rule…` paragraph (line 41) | One markdown paragraph: `**Meaning & compound-scene passes (additive; do not gate the ABORT).**…` (verbatim in prep-agent-schemas.md lines 155–160). |

**Anchor line ledger for analyst.md (verified from Read this turn):**
- Line 18: `## Inputs (passed by the caller)`
- Lines 19–21: the three existing input bullets (`source_path`, `work`, `chapter`) — E1a inserts after line 21.
- Line 33: `## Hard behavior (in this agent body, not delegated to a skill)`
- Lines 34–39: Phase-0 fenced block (opening fence at 34, closing fence at 39) — E1c inserts after line 39.
- Line 51: `## Output contract` — E1b extends the schema this section governs.

### E2 — `laf-adaptation/agents/tier-coordinator.md`  (BUILD-NEW; VENDOR.md line 117 = `BUILD-NEW | — | —`; 173 lines total)

Purpose: BUILD-NEW opus agent — fans transforms across tiers and runs `reconcile()` Checks A/B/C against shared source-canon before `chronicler`. Diff authority: `docs/native-prep/design/prep-agent-schemas.md §4` (lines 169–211).

| Change | Anchor heading (current) | Exact insertion point in current file | What lands |
|---|---|---|---|
| **E2a — Check D subsection** | `### Check C — Framing monotonicity` (line **82**); its content + fenced block run through line **93** | insert the new `### Check D — Meaning preservation…` subsection AFTER Check C's fenced block (ends line **93**), before `## Operational reading — grounding maturity()…` (line **95**) | New `### Check D — Meaning preservation (R10; /thematic-fidelity)` subsection with `preserves_meaning()` pseudocode + `status_meaning: Meaning-PRESERVED \| Meaning-DIFF` (verbatim in prep-agent-schemas.md lines 178–194). |
| **E2b — report line** | `## Output report format` → the `## Checks` list inside the report template (lines **145–148**) | insert `- D meaning-preserved: PASS …` AFTER the `- C monotonicity:` line (line **148**), before the `status: RECONCILED` line (line 150) | One report line: `- D meaning-preserved: PASS (every shared element preserves work-level meaning across tiers)` (prep-agent-schemas.md line 204). |
| **E2c — conflicts note** | prose after the report template (lines **153–155**) describing the `conflicts:` list | augment the existing `On CONFLICT, conflicts: is non-empty and lists {type, tier, element/disclosure, detail}` prose (lines 153–155) | Note that `Meaning-DIFF` contributes a `{type: "meaning_diff", …}` entry to the existing `conflicts:` list — rides the existing `RECONCILED|CONFLICT` gate, no new control flow, no new skill line (prep-agent-schemas.md lines 207–211). |

**Anchor line ledger for tier-coordinator.md (verified from Read this turn):**
- Line 82: `### Check C — Framing monotonicity`; Check C fenced block opens at 85, closes at 90; trailing prose 91–93 — E2a inserts after line 93.
- Line 95: `## Operational reading — grounding maturity()…` — the boundary E2a must NOT cross.
- Line 128: `## Output report format`; report template `## Checks` list at lines 145–148 (`- A` 146, `- B` 147, `- C` 148); `status: RECONCILED` at line 150 — E2b inserts after line 148.
- Lines 153–155: the `On CONFLICT, conflicts: …` prose — E2c anchor.

---

## Category 3 — UNCHANGED reference targets (must stay byte-identical)

These must NOT be edited. Byte-identity is machine-enforced by `check_boundary.py` Mode V (Rules A/A′ for ADOPTED, C′ for ADOPTED-PATCHED). Proof they are hash-pinned:

| # | Full relative path | Purpose (1 sentence) | Existence | Provenance + hash-pin proof |
|---|---|---|---|---|
| U1 | `laf-adaptation/agents/writer.md` | ADOPTED-PATCHED prose-writer agent; reused by rewrite phase; meaning reaches it as DATA only, never via edit. | PRESENT (36 lines) | **ADOPTED-PATCHED** — VENDOR.md line 65 pins both `laf_sha256` (373e605b…) AND `upstream_sha256` (c1b3e12f…). DESIGN D6 (line 72) + §6 D-muse note: "`writer.md` is NOT touched." Rule C′ reserves ADOPTED-PATCHED for writer.md only. Its body carries the upstream duplicate `creative-writing-craft` skill line verbatim (confirmed head lines 6–7) — must stay. |
| U2 | `laf-adaptation/agents/muse.md` | ADOPTED-CLEAN author-facing orchestrator; the rewrite phase reads `meaning:` as data from the promoted mapping — no skill line, no frontmatter change (D-muse-untouched). | PRESENT (67 lines) | **ADOPTED-CLEAN** — VENDOR.md line 60 pins `laf_sha256` (c8819ec8…) + `upstream_sha256` (18cafdc2…). DESIGN line 74: `muse` is ADOPTED-CLEAN and CANNOT receive a skill line (ADOPTED-PATCHED reserved for writer.md, Rule C′). Any byte change fails Mode V Rule A/A′. |
| U3 | `laf-adaptation/agents/web-researcher.md` | ADOPTED-CLEAN web-research agent, dispatched on the prep **context track** → `00-work-context.md`; reused unchanged. | PRESENT (12 lines) | **ADOPTED-CLEAN** — VENDOR.md line 64 pins `laf_sha256` (0219d3d2…) + `upstream_sha256` (fe371680…). DESIGN §1.2 (line 85) lists it as reused-unchanged (ADOPTED). Model `sonnet` (confirmed head line 4). Any byte change fails Mode V. |

**Boundary rationale (why byte-identity is load-bearing):** `laf-adaptation/CLAUDE.md §2` — NATIVE knowledge enters ADOPTED agents ONLY via `skills:` frontmatter, never by editing an adopted body; this keeps the adopted subset patch-clean for 3-way upstream merges. `check_boundary.py` Mode V (`uv run python scripts/check_boundary.py`) exits non-zero on any drift of a pinned body.

---

## Summary

Status: Complete

- **Category 1 (NEW, 9 files):** all confirmed ABSENT. 7 live inside `laf-adaptation/` (1 agent, 2 SKILL.md, 1 path-contract resource, 3 exemplars); 2 are `.claude/commands/laf/` harness commands outside the boundary contract. `--init` adds exactly 3 VENDOR rows (prep-cordinator, skills/prep/**, skills/thematic-fidelity/**); the exemplars + path-contract need no new row (glob-covered); commands are never manifested.
- **Category 2 (EDIT, 2 files):** `analyst.md` (NATIVE, 65 lines) gets 3 additive changes at anchors `## Inputs` (after line 21), `## Hard behavior` (after Phase-0 block line 39), and `## Output contract` (line 51 schema). `tier-coordinator.md` (BUILD-NEW, 173 lines) gets Check D after Check C's fenced block (after line 93), a `- D meaning-preserved` report line (after line 148), and a `meaning_diff` conflicts note (lines 153–155). Both NO_HASH → no VENDOR change.
- **Category 3 (UNCHANGED, 3 files):** `writer.md` (ADOPTED-PATCHED, hash line 65), `muse.md` (ADOPTED-CLEAN, hash line 60), `web-researcher.md` (ADOPTED-CLEAN, hash line 64) — all hash-pinned and enforced byte-identical by `check_boundary.py` Mode V.
- **Total files touched: 14** (9 create + 2 edit + 3 must-not-touch).

All line numbers verified against the current file contents read this turn. No item marked Unverified.

---
