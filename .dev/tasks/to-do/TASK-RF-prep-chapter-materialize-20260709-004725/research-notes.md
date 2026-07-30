# Research Notes: Implement `/laf:prep` v-next Stage 0 — Chapter Materialization + chapter-manifest.yaml

**Date:** 2026-07-09
**Scenario:** A (Explicit — full merged-requirements spec supplied)
**Depth Tier:** Deep (8-file bill of materials, boundary-contract subsystem, multi-signal split mechanism)
**Track Count:** 1 (single cohesive feature; all files interlock via the path-contract + boundary-contract)

**Driving spec:** `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md`

---

## EXISTING_FILES

Verified via Read/Bash during scope discovery (2026-07-09). Paths are repo-root-relative
(repo root = `/config/workspace/Infantalizer`; the LAF tree is the subdir `laf-adaptation/`).

### Files the spec MODIFIES (all exist, all NATIVE / not-hash-pinned bodies)
- `laf-adaptation/skills/prep/SKILL.md` (125 lines) — NATIVE. §1–§8 procedure. Spec adds a Stage-0 note in §1 + a pointer to `chapter-materialize`. Currently §1 says "the package lives at `work/prep/<work-slug>/` and contains the 8 fixed-name files `00`–`70`". Stage-0 note must NOT imply a 9th package file (manifest is a `source/` sidecar).
- `laf-adaptation/agents/prep-cordinator.md` (98 lines) — NATIVE, `model: opus`, has a `skills:` frontmatter block (lines 5–11, currently 6 skills). Spec: +1 additive `skills:` line (`- laf-adaptation:chapter-materialize`) and a Stage-0 procedure paragraph. The "8 stages" block (lines 46–62) becomes 9 (Stage 0 inserted before Stage 1) OR Stage 0 is described as a sub-phase of Stage 1 RESEARCH — spec §4 says Stage 0 is "inserted before the current §3 two-track analysis". Builder must reconcile the stage numbering carefully (spec §4 stage-sequence table shows STAGE 0..STAGE 6 as a re-map). `laf_sha256 = —` confirmed (NATIVE agent, not hash-pinned; body edits are boundary-clean).
- `laf-adaptation/skills/prep/resources/path-contract.md` (91 lines) — NATIVE. §1 pkg location, §2 the 8 files, §3 promotion targets, §4 `rewrite_phase_reads` (EXACTLY 3 files — MUST stay byte-unchanged), §5 write-ownership table. Spec §12 deltas: §1/§2/§4 UNCHANGED; add a §4 explanatory note (manifest NOT in read-set); add 3 write-ownership rows (`ch-<NN>.txt`, `chapter-manifest.yaml`, `.raw/*` → prep-cordinator Stage 0); add a NEW §6 "Source-side chapter manifest" subsection.
- `laf-adaptation/source/README.md` (23 lines) — BUILD-NEW. Currently documents `source/<work>/ch-<NN>.txt` layout + Tolkien provisioning. Spec: +manifest + `.raw/` subsection.
- `.claude/commands/laf/prep.md` (20 lines) — NATIVE mirror. `argument-hint: "<novel title>" [--source <path-or-url>]`. Spec: add `--source-mode auto|folder|file|adopt`; note `--source` may resolve to dir/file/adopt-set. Delegates to prep-cordinator; must NOT restate pipeline.
- `laf-adaptation/VENDOR.md` (126 lines) — NATIVE. Manifest table. Spec: +1 NATIVE row for the new skill. **Verified row format** (line 118–126): `| skills/<name>/** | NATIVE | — | — |` where `—` is EM DASH (U+2014, the `NO_HASH` sentinel). NATIVE skills get ONE `/**` glob row (NOT per-file rows) — confirmed by `check_boundary.py` line 430 and existing rows for `prep`, `thematic-fidelity`, `source-fidelity`.

### Files the spec CREATES (NEW)
- `laf-adaptation/skills/chapter-materialize/SKILL.md` — NEW NATIVE. Confirmed absent. The split/normalize/adopt procedure (spec §6 multi-signal evidence layers, §8 normalization, confidence rule).
- `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` — NEW NATIVE. Declarative signal ruleset. Covered by the `skills/chapter-materialize/**` VENDOR glob row (no separate manifest row needed).

### Untouched-by-contract (must be verified UNCHANGED)
- `laf-adaptation/scripts/check_boundary.py` — the ONLY script (ADR-006). MUST stay byte-unchanged. See PATTERNS below for why no edit is needed.
- `laf-adaptation/agents/writer.md` — the sole ADOPTED-PATCHED file. Untouched.
- All ADOPTED-CLEAN bodies — untouched.

### Reference / fixture inputs
- `laf-adaptation/source/narnia/` — `ch-01.txt`..`ch-04.txt` (existing hand-provisioned split set → Mode C adopt, zero re-split).
- `laf-adaptation/source/tolkien/` — `ch-01.txt` (existing → Mode C adopt).
- `Books/LWW/` (repo root) — the real ambiguous case: `...-1.html`..`-4.html` split files AND `...copy*.html` monolith duplicates both present (AC2 / release-blocker #1: must NOT auto-pick, must raise mode question). NOTE: git status shows these as untracked/deleted churn; builder should treat `Books/LWW/` as an input fixture directory, not a committed artifact.

### MDTM template (CRITICAL — non-obvious location)
- Template lives at the GLOBAL path `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` (and `01_...generic_task.md`). The PROJECT has NO `.claude/templates/workflow/` dir. The rf-task-builder and any template researcher MUST be given the absolute `/config/.claude/...` path — the skill's default `.claude/templates/workflow/...` relative path does NOT resolve in this repo.

---

## PATTERNS_AND_CONVENTIONS

- **Boundary contract (laf-adaptation/CLAUDE.md §2):** NATIVE knowledge enters ADOPTED agents ONLY via `skills:` frontmatter — never by editing an adopted body. The new skill attaches to `prep-cordinator` (a NATIVE agent) via one additive `skills:` line. prep-cordinator being NATIVE (`laf_sha256 = —`) means its BODY may be edited freely (unlike an ADOPTED agent). This is why the Stage-0 procedure paragraph can be added directly to the agent body.
- **check_boundary.py classify() — NO EDIT NEEDED (verified, load-bearing):** `classify()` (lines 349–368) returns `"NATIVE"` by DEFAULT for any non-upstream skill not in `BUILD_NEW_SKILLS` (line 367). The `NATIVE_SKILLS` set (line 46: only `adaptation-tiers`, `adaptation-rules`, `source-fidelity`) is NOT an allowlist — existing NATIVE rows `prep` and `thematic-fidelity` are NOT in that set yet still classify NATIVE. Therefore `chapter-materialize` auto-classifies NATIVE at `--init` with ZERO script edit. The spec's "check_boundary.py untouched" claim is CORRECT. **The task must NOT add `chapter-materialize` to the `NATIVE_SKILLS` set** (that would be an unnecessary script edit and violate ADR-006's "validator only").
- **VENDOR.md manifest hand-edit vs --init:** `--init` requires an `--upstream <checkout>` and regenerates the whole manifest. For a single NATIVE-row addition, the row is hand-authored: `| skills/chapter-materialize/** | NATIVE | — | — |` placed in the NATIVE group (after other `skills/*/** NATIVE` rows, before BUILD-NEW). The em dash MUST be U+2014 (matches existing NO_HASH rows) or the parser (CH-6) flags it. Rule F then passes because the SKILL.md is manifest-covered by the `/**` glob row.
- **`.claude/` mirror convention:** LAF skills are mirrored into `.claude/skills/` (verified: `adaptation-rules`, `adaptation-safety`, `adaptation-tiers`, `prep`, `source-fidelity` present). Agents mirrored into `.claude/agents/` (prep-cordinator.md, analyst.md, etc.). Commands in `.claude/commands/laf/` (prep.md, rewrite.md). **The new `chapter-materialize` skill and the edited prep-cordinator/prep/command MUST be mirrored to `.claude/` in lockstep** (spec §11: "`.claude/` mirror updated in lockstep"). NOTE: `.claude/skills/prep/` mirrors the SKILL.md; verify whether the mirror also carries `resources/` (path-contract.md) — builder/researcher must check mirror granularity.
- **NATIVE skill resources/ layout:** existing NATIVE/BUILD-NEW skills use `skills/<name>/SKILL.md` + `skills/<name>/resources/<file>` (e.g. `adaptation-safety/resources/children.md`). `chapter-materialize/resources/boundary-rules.yaml` follows this.
- **Skill frontmatter dialect (CLAUDE.md §3):** skills carry ONLY `name` + `description`. Agents carry `name`, `description`, `model` (∈ opus/sonnet/haiku/inherit), `skills` (fully-qualified `laf-adaptation:<skill>`), `tools`. NEVER Mars keys.
- **path-contract is single-source-of-truth:** never restate a path literally in skill/command/agent bodies — import path-contract.md by reference. The Stage-0 write paths (`ch-<NN>.txt`, `chapter-manifest.yaml`, `.raw/`) get defined ONCE in path-contract §5/§6 and referenced elsewhere.
- **Confidence-tagging (`/source-fidelity`):** every extracted fact carries CERTAIN/PROBABLE/UNCERTAIN. The manifest reuses this vocabulary for split/title/order/mode confidence. CERTAIN requires ≥2 independent agreeing signals; single-signal capped at PROBABLE (AC4 / release-blocker #3).
- **No new runtime (ADR-006):** the split procedure is model-executed prose in SKILL.md; `check_boundary.py` stays the sole script and a validator only. No parser binary, no CLI.

---

## GAPS_AND_QUESTIONS (for researchers to close)

1. **Exact `.claude/` mirror granularity** — does `.claude/skills/prep/` carry only SKILL.md or also `resources/path-contract.md`? Determines whether the path-contract edit needs a mirror copy. (Researcher: File Inventory / Integration.)
2. **prep-cordinator stage renumber** — should Stage 0 be a new numbered stage (making 9 stages) or a sub-phase of Stage 1? Spec §4 shows a STAGE 0..6 re-map for the prep SKILL's §-sequence, but the agent body uses its own "8 stages" numbering. Researcher must document the current numbering precisely so the builder edits consistently without breaking the two HALT-gate references.
3. **check_boundary.py invocation for verification** — confirm `uv run python scripts/check_boundary.py` (verify/Mode V) is the AC6 gate and that it must be run FROM `laf-adaptation/` (working-directory) with exit 0. Document the exact command + cwd.
4. **`rewrite_phase_reads` byte-unchanged proof** — how to verify path-contract §4 is byte-identical after edits (the 3-file read-set). Researcher documents a diff/grep verification approach.
5. **MDTM template rules** — read the global `02_mdtm_template_complex_task.md` PART 1: confirm A3 granularity, B2 self-containment, M3/M4/I19–I22 QA-gate encoding rules the builder must follow.
6. **chapter-manifest.yaml schema** — the spec §5 gives a full schema; researcher extracts it verbatim as the authoring target so the builder can create a per-field checklist (no invention).

## RECOMMENDED_OUTPUTS (researcher assignments → `research/NN-*.md`)

- `01-file-inventory-and-edits.md` — File Inventory: every BOM file, current state (line counts, key sections/anchors), exact edit locus per file, whether a `.claude/` mirror copy exists and its granularity.
- `02-boundary-contract-and-verification.md` — Integration Points + Test/Verification: check_boundary.py Rule E/F mechanics for a new NATIVE skill, VENDOR.md row format + placement, the AC6 verification command (cwd, exit code), rewrite_phase_reads byte-stability check, `.claude/` mirror lockstep requirement.
- `03-skill-authoring-spec.md` — Patterns & Template: the chapter-materialize SKILL.md structure (mirroring existing NATIVE skills), the boundary-rules.yaml shape, the chapter-manifest.yaml v1 schema (verbatim from spec §5), the confidence rule, the failure-mode table (spec §7), normalization policy (spec §8).
- `04-mdtm-template-and-gate.md` — Template & Examples: read the global MDTM 02 template PART 1; document required sections, B2 pattern, QA-gate encoding (M3/M4/I19–I22), and how the Stage-0 → §5 question-gate / §6 greenlight integration (spec §10) maps to task phases.

## SUGGESTED_PHASES (for the builder — indicative, builder finalizes)

- Phase 1 — Author the NEW `chapter-materialize` skill (SKILL.md + resources/boundary-rules.yaml) + mirror to `.claude/`.
- Phase 2 — Wire it into prep-cordinator (skills: line + Stage-0 procedure) + prep SKILL.md §1 note + command `--source-mode` + `.claude/` mirrors.
- Phase 3 — path-contract.md §4 note + §5 rows + new §6; source/README.md manifest+.raw subsection; VENDOR.md +1 NATIVE row.
- Phase 4 — Verification: `check_boundary.py` exits 0; rewrite_phase_reads byte-unchanged; no 9th package file; no second script; `.claude/` mirror parity; AC1–AC7 walkthrough.
- Phase 5 (final) — QA gate + POST reflect + status→Done.

## TEMPLATE_NOTES

- **MDTM Template: 02 (Complex).** The work has discovery-ish reconciliation, multiple interdependent edits across subsystems, a boundary-contract verification gate, and conditional (mode-ambiguity) behavior baked into the authored procedure — Template 02 is correct.
- **Tier: Deep.** 8 BOM files across the prep skill, agent, command, path-contract, source docs, VENDOR manifest, plus a new skill dir — multiple subsystems and a load-bearing boundary contract. Deep researcher set (4).
- **QA_GATE_REQUIREMENTS: FINAL_ONLY** — this task authors prompt+YAML framework files (no code, no tests). A single final-document QA gate (min 6 agents) validating boundary-contract compliance + AC coverage is appropriate; PER_PHASE would be overkill for doc/prompt authoring. TESTING_REQUIREMENTS: NONE (the AC6 `check_boundary.py` run is a VALIDATION item, not a unit test — ADR-006 forbids adding test scripts).
- **VALIDATION_REQUIREMENTS:** `uv run python scripts/check_boundary.py` exits 0 (run from `laf-adaptation/`); `rewrite_phase_reads` byte-unchanged; no 9th numbered package file; no second script; `.claude/` mirror parity.
- **POST_REFLECT_GATE: ENABLED**, `reflect_post_mode: skill` (default). SPEC_PATH = the merged-requirements.md.

## AMBIGUITIES_FOR_USER

None blocking. The spec is unusually complete (goals, non-goals, BOM, deltas, AC, release-blockers). Two design seams are explicitly deferred by the spec itself (§15: whether rewrite reads the manifest; per-chapter analysis granularity) and are OUT OF SCOPE for this task — the builder records them as documented non-goals, not open questions. The prep-cordinator stage-renumbering choice (gap #2) is an authoring detail the builder resolves from researcher findings, not a user-intent question.
