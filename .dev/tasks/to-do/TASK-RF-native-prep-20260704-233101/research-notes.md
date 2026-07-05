# Research Notes: Implement the native LAF adaptation-prep phase (from the DESIGN.md design pack)

**Date:** 2026-07-04
**Scenario:** A (Explicit — driving design pack fully specifies paths, phases P0–P4, gates, and 5 companion specs)
**Depth Tier:** Deep (spans laf-adaptation/{agents,skills}, .claude/commands/, config/, docs/, scripts/check_boundary.py)
**Track Count:** 1 (P0→P4 build sequentially on shared boundary-contract context — not independent streams)
**Spec (driving):** docs/native-prep/design/DESIGN.md (+ 5 companions)
**Template:** 02 (complex — discovery → build → verify with boundary + end-to-end gates)
**MDTM template location:** /config/.claude/templates/workflow/02_mdtm_template_complex_task.md (GLOBAL — project .claude/templates/ does not exist)
**Git start_commit:** b51633d40a64be488c30edbd0f803dbdc8feadc1 (git merge-base HEAD origin/main)
**executor_model_class:** sonnet (default executor)

---

## What this task implements (the deliverable of the built task file, when executed)

The design pack at `docs/native-prep/design/` (DESIGN.md + prep-agent-schemas.md + prep-skill-specs.md +
path-contract.md + package-schemas.md + boundary-verification.md) is the buildable spec. The task file must
implement it in 5 phases (P0→P4) exactly as DESIGN.md §7 sequences, with the boundary check green at P0/P1/P3.

Net changes to make:
- **NEW NATIVE agent:** `laf-adaptation/agents/prep-cordinator.md` (opus; 6 skills; Agent(web-researcher, analyst, tier-coordinator))
- **NEW NATIVE skills:** `laf-adaptation/skills/prep/SKILL.md` (+ `resources/path-contract.md`); `laf-adaptation/skills/thematic-fidelity/SKILL.md`
- **NEW NATIVE exemplars (×3):** `laf-adaptation/skills/adaptation-rules/resources/exemplars/{sacrifice-and-return,betrayal-and-redemption,petrification-body-horror}.md` (DERIVED-marked)
- **NATIVE body edit:** `laf-adaptation/agents/analyst.md` (+meaning, +compound_scene, +granularity/out_path work-mode; chapter defaults preserved)
- **BUILD-NEW body edit:** `laf-adaptation/agents/tier-coordinator.md` (+Check D meaning-preservation; no frontmatter change)
- **NEW commands (harness surface, OUTSIDE laf-adaptation/, NOT in VENDOR):** `.claude/commands/laf/prep.md`, `.claude/commands/laf/rewrite.md`
- **VENDOR regen:** `check_boundary.py --init` auto-writes exactly 3 NATIVE rows (prep-cordinator, prep/**, thematic-fidelity/**)
- **DOC pointer:** `docs/guides/ADDING_NEW_WORKS.md` (+1 paragraph → "use 0.1's /laf:prep")
- **UNCHANGED (must stay byte-identical):** `agents/writer.md` (ADOPTED-PATCHED), `agents/muse.md` (ADOPTED-CLEAN)

---

## EXISTING_FILES (verified on disk 2026-07-04)

**Design pack (SOURCE OF TRUTH for the build):**
- docs/native-prep/design/DESIGN.md — master (8-stage pipeline, R-traceability, spec-correction log, P0–P4 gates)
- docs/native-prep/design/prep-agent-schemas.md — prep-cordinator frontmatter + analyst/tier-coordinator diffs + command specs
- docs/native-prep/design/prep-skill-specs.md — prep + thematic-fidelity SKILL.md body outlines
- docs/native-prep/design/path-contract.md — the resource content to ship at skills/prep/resources/path-contract.md
- docs/native-prep/design/package-schemas.md — 8 package file schemas + taxonomy + exemplar spec
- docs/native-prep/design/boundary-verification.md — corrected change-list, VENDOR delta, per-rule A–F expectations

**Edit targets (present):**
- laf-adaptation/agents/analyst.md — NATIVE (VENDOR line 111: `agents/analyst.md | NATIVE | — | —`); 66 lines; has Inputs / Procedure / Hard behavior / Output contract sections
- laf-adaptation/agents/tier-coordinator.md — BUILD-NEW (VENDOR line 117); ~174 lines; has Checks A/B/C; report format block

**Reference targets (present, must NOT change):**
- laf-adaptation/agents/writer.md — ADOPTED-PATCHED (VENDOR line 65); byte-frozen body + 1 additive skill line
- laf-adaptation/agents/muse.md — ADOPTED-CLEAN (VENDOR line 60); reads meaning as data (D6)
- laf-adaptation/agents/web-researcher.md — ADOPTED; model sonnet; `/creative-research`; Read/WebSearch/WebFetch

**Boundary + schema references (present):**
- laf-adaptation/scripts/check_boundary.py — the ONLY script; classify() at lines 326-345; --init at 349-440; verify Rules A/A′/C′/D/E/F/F′
- laf-adaptation/VENDOR.md — manifest; NATIVE glob rows at 111-118; adopted-CLEAN rows above
- laf-adaptation/CLAUDE.md — provenance model + boundary contract + conventions (frontmatter dialect §3)
- laf-adaptation/templates/work-mapping-template.yaml — 5-key mapping template
- config/concept_mapping/templates/tolkien_mapping.yaml — ROOT promotion form (underscore, 5-key)
- laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml — 0.1 promotion form (hyphen)
- docs/guides/ADDING_NEW_WORKS.md — R14 pointer target; asserts 5-key schema (step 6)

**New targets (correctly ABSENT — to be created):**
- laf-adaptation/agents/prep-cordinator.md · skills/prep/ · skills/thematic-fidelity/ · skills/adaptation-rules/resources/exemplars/ · .claude/commands/laf/

## PATTERNS_AND_CONVENTIONS

- **Agent frontmatter dialect (Claude-native / cw-lowered):** keys = name (== filename stem), description, model ∈ {opus,sonnet,haiku,inherit}, skills (fully-qualified `laf-adaptation:<skill>`), tools (comma list; Agent(...) allowed for orchestrators — see muse.md). NO Mars keys. (laf-adaptation/CLAUDE.md §3; design agent-schemas.md §1)
- **Skill frontmatter:** name + description only. Structure = SKILL.md + optional resources/. No rules/ or templates/ subdirs.
- **Command files (Claude Code slash commands):** `.claude/commands/<ns>/<cmd>.md` → `/<ns>:<cmd>`. Frontmatter: description, argument-hint. Body = the delegation prompt. (No existing laf command to copy — .claude/commands is empty; format is standard Claude Code.)
- **DERIVED exemplar marker (verbatim):** `<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->` as line 1.
- **Mapping schema:** root = 5 keys (work_metadata, characters, concepts, key_scenes, master_translation_table); 0.1 form adds top-level `meaning:` (6th). Root file naming underscore; 0.1 kb naming hyphen.
- **Carried-verbatim / key-tolerant reads:** never normalize schema drift in data; absorb in readers (CLAUDE.md §3).

## GAPS_AND_QUESTIONS

- Confirm `check_boundary.py --init` requires a `--upstream <checkout>` (do_init returns 2 without it). P0 gate must account: `--init` needs an upstream checkout at the pinned SHA (3338495f…), OR the 3 NATIVE rows are appended by re-running the documented flow / Mode V verify covers them via Rule F. Researchers: confirm whether Mode V (no --upstream) can PASS with hand-added NATIVE rows, so P0/P1 gates are runnable without the upstream tree.
- Confirm a readable Narnia (or Tolkien) source text exists for the P3 end-to-end prove (laf-adaptation/source/tolkien/ch-01.txt present; a full-novel source may not be — P3 may use the available chapter text as the work-level source, or MEMORY-BASED is disallowed at work level so a real text file is required).
- Confirm root 5-key validation command from ADDING_NEW_WORKS step 6 (uv run --with pyyaml python -c "...sorted(d)").

## RECOMMENDED_OUTPUTS (researcher → file)

- research/01-file-inventory.md
- research/02-patterns-conventions.md
- research/03-boundary-integration.md
- research/04-template-and-examples.md
- research/05-design-pack-crossvalidation.md
- research/06-verification-and-proof-flow.md

## SUGGESTED_PHASES (researcher assignments — Deep = 6, no overlap)

- **R1 File Inventory** → 01-file-inventory.md. Scope: every file the task creates/edits/leaves-unchanged (list above). For each edit target (analyst.md, tier-coordinator.md) give exact section anchors + line ranges the diff touches. For each reference target, record the exact current bytes that must NOT change (writer.md, muse.md frontmatter/body). Covers WHAT files; not conventions (R2) or boundary logic (R3).
- **R2 Patterns & Conventions** → 02-patterns-conventions.md. Scope: agent/skill/command frontmatter dialects with real examples (muse.md, source-fidelity SKILL.md, web-researcher.md); the DERIVED marker; the mapping schema keys; Claude Code slash-command file format. Covers HOW to write each new file; not the file list (R1) or the boundary rules (R3).
- **R3 Boundary Integration** → 03-boundary-integration.md. Scope: check_boundary.py classify()/do_init/verify — trace exactly which rows --init writes for the 3 new NATIVE files, whether Mode V (no --upstream) PASSES, Rule E (no upstream name collision) and Rule F/F′ coverage for the new SKILL.md files; the dual-form promotion targets (root underscore 5-key vs kb hyphen 6-key) and the meaning-strip. Covers the boundary MECHANICS; not verification commands (R6).
- **R4 Template & Examples** → 04-template-and-examples.md. Scope: read /config/.claude/templates/workflow/02_mdtm_template_complex_task.md PART 1 (rules A3 granularity, B2 self-containment, L1–L6 handoff, M3/M4/I19/I20/I21 QA encoding); inspect prior TASK-RF-laf-hybrid-build task file for effective patterns. Covers the MDTM builder rules; nothing else.
- **R5 Design-Pack Cross-Validation** → 05-design-pack-crossvalidation.md. Scope: read all 6 design docs and verify EVERY concrete claim against live code — VENDOR line numbers (111/113/117), check_boundary classify logic, the 5-key root schema, the underscore/hyphen paths, the analyst/tier-coordinator section anchors the diffs target. Tag each [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]. This protects the builder from any design/code drift. Covers design↔code fidelity; not the MDTM template (R4).
- **R6 Verification & Proof Flow** → 06-verification-and-proof-flow.md. Scope: the exact commands each phase gate runs — `uv run python laf-adaptation/scripts/check_boundary.py` (Mode V), `--report` (expect +3 NATIVE rows), `git diff --stat` proving writer.md/muse.md unchanged, the root 5-key yaml validation, and the P3 end-to-end source availability (source/tolkien/ch-01.txt; whether a full-work source exists for work-level analysis). Covers the test/verification surface; not boundary internals (R3).

## TEMPLATE_NOTES

- Template **02** (complex): the build has discovery (read design pack + live tree), build (skills/agent/commands/exemplars), edits (analyst/tier-coordinator), and verification gates (boundary check Mode V, end-to-end prove). Phases should mirror DESIGN.md §7 P0→P4 plus a final QA/validation + reflect gate phase.
- Tier **Deep** (6 researchers) chosen because scope spans ≥4 subsystems (per skill rule "spans multiple subsystems → always Deep").
- Granularity (A3): one checklist item per NEW file (agent, 2 SKILL.md, path-contract.md, 3 exemplars, 2 commands, ADDING_NEW_WORKS edit), one per EDIT target (analyst.md diff, tier-coordinator.md diff), plus per-gate verification items. No batch items.
- QA gates in the generated task file: PER_PHASE (Template 02). Each phase-gate QA meets I19/I22 minimums; the P3 prove phase transforms a novel into a package (source-material transformation) → I21 fidelity gate applies to the package vs design-pack contract.

## AMBIGUITIES_FOR_USER

None blocking — the design pack fully specifies intent, paths, and gates, and the command-placement fork was already user-confirmed (2026-07-04: `.claude/commands/laf/`). The only open verification items (boundary --init vs Mode V; P3 source availability) are codebase questions the researchers resolve, not user-intent questions.
