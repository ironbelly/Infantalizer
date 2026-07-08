# Research Notes: Build LAF 0.1 (CWS Hybrid Integration, Path C) — Phases 0-4

**Date:** 2026-07-03
**Scenario:** A (Explicit — full design pack of 7 specs)
**Depth Tier:** Deep
**Track Count:** 1 (single cohesive track — phases 0→4 build sequentially on each other; NOT independent work streams)

**Driving spec:** `.dev/releases/current/0.1/design/DESIGN.md` (+ 6 companion specs)

**User decisions (locked via AskUserQuestion):**
1. **Vendor source = "Task acquires CWS first"** — Phase 0 clones/pins the upstream CWS repo at a chosen SHA into a local checkout dir, then vendors 13 adopted files from it and runs `check_boundary.py --init --upstream <dir>`. Task is self-contained.
2. **Build scope = "Full Phases 0-4"** — one comprehensive task file: vendor → native spine → greenfield → compose-and-prove HARD GATE (live Tolkien chapter × 3 tiers) → upstream-sync protocol docs.

---

## GOAL

Build a task file that implements the LAF 0.1 architecture (Path C Hybrid) end-to-end, phases 0-4, producing the `laf-adaptation/` single-tree distribution: vendored ADOPTED subset (patch-clean), NATIVE adaptation spine (2 agents + 3 skills), BUILD-NEW greenfield (2 agents + 1 skill + genre resources), native kb layers (tiers, adaptation-mapping, per-tier canon graft G1), the `VENDOR.md` boundary contract + `check_boundary.py` enforcement gate, and the Phase-3 live-chapter proof.

## WHY

The design pack (`DESIGN.md` + 6 companions) is settled and is the buildable source of truth. It turns the Path-C decision into concrete artifacts. `next_step` in DESIGN.md frontmatter is `/sc:implement @DESIGN.md`. Implementation must proceed phase-by-phase (0→4) with the Phase-3 hard gate as the definition of "0.1 done".

---

## EXISTING_FILES

### Design pack (the spec — READ-ONLY inputs, buildable source of truth)
`.dev/releases/current/0.1/design/`:
- `DESIGN.md` (309 lines) — system overview, component inventory (11 agents / 16 skills), distribution layout §2, data-flow §3, traceability §4, constraint-enforcement map §5, residual risks §6, **build phases & gates §7 (Phase 0-4 table — the spine of the task file)**.
- `agent-schemas.md` (305 lines) — full frontmatter for `analyst`, `safety-verifier` (native, §2), `chronicler`, `tier-coordinator` (build-new, §5); `writer` frontmatter-only patch (§3, ADOPTED-PATCHED, the single additive `- laf-adaptation:adaptation-rules` line); `reader-sim` persona-as-data (§4, no file edit); dispatch-param summary §6.
- `skill-specs.md` (303 lines) — SKILL.md bodies for `/adaptation-tiers` (§1), `/adaptation-rules` (§2, + resources thematic/character/agency), `/source-fidelity` (§3, v2.0 5-phase protocol + output schema §3.2), `/adaptation-safety` (§4, + genre resources children.md/ya.md §4.1); skill→consumer map §5.
- `kb-formats.md` (282 lines) — `kb/tiers/tier_N.yaml` schema §2 (+ schema-drift handling §2.2, canonicity §2.3, T4 interpolation §2.4); `kb/adaptation-mapping/` cascade §3 (universal + <work> + resolution order §3.3); `kb/adaptations/<work>/tier-N/` per-tier canon graft G1 §4 (continuity.md, decisions.md, canon-delta.md, analysis.yaml, adapted.md); shared-vs-per-tier split §5.
- `boundary-contract.md` (203 lines) — `VENDOR.md` format §2 (manifest table, provenance classes §1); `check_boundary.py` §3 (3 modes §3.1, verify algorithm §3.2 rules A-F, body_of/frontmatter_line_diff §3.3); enforcement points §4; upstream-sync protocol §5.
- `safety-rubric.md` (144 lines) — 6-section rubric §1 (verbatim word lists/checklists), automatic failures §2, aggregation logic §3, verdict contract §4 (machine-parseable YAML block), workflow branch §4.1, traceability §5.
- `tier-coordinator.md` (174 lines) — reconciliation algorithm: inputs/outputs §1, fan-out modes §2 (parallel default / sequential fallback G2 §2.2 + selection heuristic), `reconcile()` 3 checks §3 (A source-fidelity, B disclosure-leak, C monotonicity), output report format §4, chronicler interaction §5, T4 handling §6.

### LAF port-source files (carried VERBATIM into native skills/kb — zero rework, ADR-006)
Repo root = `/config/workspace/Infantalizer` (git branch `main`, all untracked — first commit territory).
- `config/age_profiles/tier_1_preschool.yaml` (94 L) → `kb/tiers/tier_1.yaml`
- `config/age_profiles/tier_2_early_elementary.yaml` (84 L) → `kb/tiers/tier_2.yaml`
- `config/age_profiles/tier_3_middle_elementary.yaml` (87 L) → `kb/tiers/tier_3.yaml`
- `config/age_profiles/tier_5_young_adult.yaml` (87 L) → `kb/tiers/tier_5.yaml`  (T4 interpolated, never stored)
- `config/concept_mapping/universal_mappings.yaml` (56 L) → `kb/adaptation-mapping/universal-mappings.yaml`
- `config/concept_mapping/templates/tolkien_mapping.yaml` (81 L) → `kb/adaptation-mapping/tolkien-mapping.yaml` (at onboarding)
- `config/transformation_rules/thematic.yaml` (90 L) → `skills/adaptation-rules/resources/thematic.md` (fenced verbatim)
- `config/transformation_rules/character.yaml` (77 L) → `skills/adaptation-rules/resources/character.md` (fenced verbatim)
- `prompts/analysis/chapter_analysis.md` (86 L) → `/source-fidelity` body + analyst output schema
- `prompts/verification/safety_check.md` (90 L) → `/adaptation-safety` body + rubric
- `prompts/transformation/tier_1_transform.md`, `tier_3_transform.md` → genre resources source (children.md)
- `templates/work_mapping_template.yaml` (60 L) → `templates/work-mapping-template.yaml`
- `docs/design_decisions/001-five-tier-system.md`, `003-agency-externalization.md` → `/adaptation-tiers` resources/tier_N.md commentary

### Target tree (does NOT exist yet — greenfield creation)
`laf-adaptation/` — full layout in DESIGN.md §2. Must be created from scratch.

## PATTERNS_AND_CONVENTIONS

- **ADR-006: prompt + YAML-config framework — NOT software.** No Python/CLI runtime. The ONLY script is `scripts/check_boundary.py` (a validation tool, not a runtime). Do not add other scripts.
- **Frontmatter dialect: Claude-native (cw-lowered), NOT Mars.** Permitted agent keys (closed set): `name`, `description`, `model` (opus|sonnet|haiku|inherit only — never gpt/deepseek/opus46), `skills` (`laf-adaptation:<skill>` fully-qualified), `tools` (comma-sep Claude tool names). Skill frontmatter: `name` + `description` only. NO Mars keys (`model-policies`, `sandbox`, `effort`, `subagents`, `model-invocable`, `type`).
- **Boundary contract (constraint #6):** native knowledge enters ADOPTED agents ONLY via `skills:` frontmatter — never body edits. Adopted files vendored from CWS `cw/agents/` (already Claude-lowered), the ONE permitted vendor-time transform = uniform prefix rewrite `creative-writing-skills:` → `laf-adaptation:`. `writer.md` also gets ONE additive skill line (ADOPTED-PATCHED). Preserve upstream quirks verbatim (e.g. writer.md lists `creative-writing-craft` twice — do NOT "fix").
- **Provenance classes:** ADOPTED-CLEAN, ADOPTED-PATCHED (only writer.md), NATIVE, BUILD-NEW. Every `agents/*.md` and `skills/**/SKILL.md` must be in the VENDOR.md manifest.
- **Carried verbatim = zero rework.** Native tier/mapping YAML ports as pure copy; schema drift preserved (T1-T3 `conflict_to_cooperation`/`death_euphemism` vs T5 `conflict_handling`/`death_handling`) with key-tolerant lookups in consuming skill bodies.
- **Constraint invariants:** #1 tier axis first-class (`active_tier` explicit param); #2 uncertainty discipline (analyst Phase-0 ABORT on NO-ACCESS); #3 safety_check revision loop (safety-verifier FAIL blocks promotion → back to writer step 3); #4 quartet (4 distinct: critic/editor/reader-sim/continuity-checker) + 5th native safety-verifier, editor NEVER folded (G3); #5 work/ vs kb/ split (chronicler writes kb only on muse-accept); #6 skill-vs-agent boundary.
- **Grafts:** G1 per-tier canon (`kb/adaptations/<work>/tier-N/`, keyed (work,tier,chapter)); G2 sequential fan-out fallback; G3 editor-never-folded written invariant.
- **UV only** for the check_boundary.py invocations: `uv run python scripts/check_boundary.py`.

## GAPS_AND_QUESTIONS

- **[RESOLVED by user]** Upstream CWS acquisition: Phase 0 clones/pins upstream CWS at a chosen SHA into a local checkout, then vendors. Researcher must determine: exact adopted file list (13 = 10 clean agents + writer patched + which 12 skills), upstream repo URL (`https://github.com/haowjy/creative-writing-skills` per VENDOR.md §2), how `cw/agents/` vs `agents/` differ (Mars vs cw-lowered).
- The design lists "12 adopted skills" but §1.1 enumerates 13 skill names in the ADOPTED column (writing-principles, creative-writing-craft, creative-writing-modes, story-review, story-memory, kb-management, shared-dao, llm-writing, writing-staffing, intent-modeling, grill-with-docs, creative-research) = 12. Phase 0 says "12 adopted skills". Researcher: confirm the exact count and names, and whether all have `resources/` to hash.
- The exact content of vendored ADOPTED agent/skill bodies is unknown until the upstream is cloned — the task file must NOT author them; it copies them. Task items reference them by target path + provenance, not content.
- `check_boundary.py` is authored NATIVE (per boundary-contract.md §3.2 pseudocode) — this IS content to write. Researcher: extract full verify-algorithm rules A-F, --init/--report modes, body_of/frontmatter_line_diff defs.
- Phase 3 hard gate needs a real Tolkien source chapter under `source/<work>/ch-<NN>.txt`. Researcher: check if any source text exists; if not, the task must supply/stub one (a public-domain or short excerpt) or document it as an execution-time input.

## RECOMMENDED_OUTPUTS

The generated task file (`${TASK_DIR}/${TASK_ID}.md`), Template 02 (complex — discovery, build, prove phases, conditional flows, hard gate). Phases mirror DESIGN.md §7:
- Phase 0: Vendor (acquire CWS → copy adopted → write VENDOR.md → check_boundary.py --init passes)
- Phase 1: Native spine (3 native skills, analyst + safety-verifier agents, writer frontmatter patch, port kb/tiers + kb/adaptation-mapping)
- Phase 2: Greenfield (chronicler + tier-coordinator agents, /adaptation-safety + genre resources, native kb layers)
- Phase 3: Compose & prove HARD GATE (full 11-step run on 1 Tolkien chapter T1; then T1/3/5 via tier-coordinator; 5 gate conditions)
- Phase 4: Upstream-sync protocol docs
- Final phase: QA gates, validation, task-completion items, POST reflect gate.

## SUGGESTED_PHASES (researcher assignments — 6 researchers, Deep tier)

- **R1 (File Inventory + Target-Tree Mapping):** Enumerate every file the task must CREATE in `laf-adaptation/` from DESIGN.md §2 layout — one row per target file with provenance class (ADOPTED-CLEAN/PATCHED/NATIVE/BUILD-NEW), source (upstream path OR LAF port-source OR authored), and which spec section defines it. This is the master file→item map for granular checklist items. Scope: DESIGN.md §1.1-§2, boundary-contract.md §2 manifest, kb-formats.md §1 layout.
- **R2 (Native agents + skills content):** Extract exact authorable content for the 2 native agents (analyst, safety-verifier) and 3 native skills (/adaptation-tiers, /adaptation-rules, /source-fidelity): full frontmatter, body outlines, output schemas, hard-behavior blocks (Phase-0 ABORT, tier gate). Scope: agent-schemas.md §2, skill-specs.md §1-3.
- **R3 (Build-new agents + safety skill + genre resources):** Extract chronicler + tier-coordinator frontmatter + body invariants (write targets, (work,tier,chapter) key, reconcile() 3 checks, fan-out modes), /adaptation-safety skill + children.md/ya.md genre resources. Scope: agent-schemas.md §5, skill-specs.md §4, safety-rubric.md, tier-coordinator.md.
- **R4 (kb layers + port-source verbatim):** Read all LAF port-source files (config/, prompts/, templates/) and map each to its native kb/skill-resource target; document the tier_N.yaml schema, adaptation-mapping cascade, per-tier canon graft-G1 file formats (continuity.md/decisions.md/canon-delta.md). Confirm zero-rework carry + schema-drift/key-tolerance handling. Scope: kb-formats.md §2-5 + all config/prompts/templates files.
- **R5 (Boundary contract + check_boundary.py):** Extract the FULL authorable content of scripts/check_boundary.py (verify algorithm rules A-F, --init/--report modes, body_of/frontmatter_line_diff) and VENDOR.md manifest format (provenance table, invariants G3, prefix-rewrite recording). Document upstream CWS acquisition (repo URL, SHA-pinning, cw/agents vs agents dialect difference, exact 13-file adopted list). Scope: boundary-contract.md (full), DESIGN.md §2.1 + provenance note.
- **R6 (Phase-3 proof gate + Template & Examples):** Document the 11-step data-flow workflow (DESIGN.md §3), the safety revision loop §3.1, multi-tier fan-out §3.2, and the exact 5 Phase-3 gate conditions §7. Check for existing Tolkien source text; determine proof-chapter provisioning. Read MDTM Template 02 (PART 1 rules A3/A4/B2) + check .dev/tasks/to-do/ for prior examples. Scope: DESIGN.md §3, §7, §5-6; .claude/templates/workflow/02_mdtm_template_complex_task.md.

## TEMPLATE_NOTES

- **Template 02 (Complex Task)** — the build has discovery (clone upstream), multi-phase (vendor/native/greenfield/prove), conditional flows (safety FAIL loop, parallel vs sequential fan-out), and a hard gate. Not Template 01.
- **Deep tier** — 20+ target files across multiple subsystems (agents, skills, kb, scripts), a boundary-contract subsystem, a live-chapter proof. Justifies 6 researchers.
- **Granularity:** one checklist item per created file (each native agent, each native skill SKILL.md, each kb/tiers/tier_N.yaml, each genre resource, check_boundary.py, VENDOR.md). Adopted files may be batched per vendoring step BUT the VENDOR.md manifest rows are per-file — the vendoring copy step can be per-provenance-group with a per-file verification list.
- **QA gates in generated task file:** PER_PHASE (Template 02). Each gate ≥6 agents (3 rf-qa + 3 rf-qa-qualitative). check_boundary.py is a boundary-contract-critical artifact → its own validation. No document >500 lines expected per single artifact, but the aggregate build is large — encode a source-fidelity gate where port-source is carried verbatim (I21: source→target faithful-carry check for kb YAML + skill resources).
- **TESTING_REQUIREMENTS:** the framework is prompt+config (no unit tests), BUT `check_boundary.py` is real Python and MUST have verification (run `--init` then `--report` then `verify` on the built tree → exit 0). Phase 3 hard gate IS the integration test.
- **VALIDATION_REQUIREMENTS:** `check_boundary.py` green (all 6 rules A-F), writer.md diff frontmatter-only+additive, quartet intact (G3), every agents/*.md + skills/**/SKILL.md in manifest, native skills validate (frontmatter shape), UV used for python invocations.

## AMBIGUITIES_FOR_USER

None remaining — the two material scoping decisions (vendor-acquisition strategy and phase-scope) were resolved via AskUserQuestion. Remaining unknowns (exact adopted file bodies, Tolkien source-chapter provisioning) are execution-time details the researchers will bound and the task file will document as prerequisites/steps, not blockers.

---
**Status:** Complete
