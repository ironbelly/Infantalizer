# Research Notes: LAF Adaptation Framework

**Date:** 2026-07-08
**Scenario:** A (explicit feature, well-known structure — focused discovery; deep investigation partitioned to Phase 2 agents)
**Depth Tier:** Standard (user-selected; note: the framework is cross-cutting and the skill heuristic would suggest Heavyweight — honor Standard, mark frontend-only template sections N/A, keep subsystem sections dense but within budget)

**Feature:** The **LAF (Literary Adaptation Framework)** under `laf-adaptation/` — a prompt + YAML-config framework (NOT software, per ADR-006) for **tier-aware literary adaptation**: it takes a source novel and produces developmentally-graded adaptations (Tiers 1/2/3/5, T4 interpolated) via two pipelines (prep → rewrite), a multi-agent review workflow, a native kb layer, and a hash-pinned boundary contract that keeps a vendored CWS (creative-writing-skills) subset patch-clean.

**Output doc:** `docs/laf/LAF-ADAPTATION-FRAMEWORK-TECHNICAL-REFERENCE.md`
**Template:** `/config/.claude/templates/documents/technical_reference_template.md` (user-global; project has no local `.claude/templates/`)

> **IMPORTANT for all Phase 2 agents:** Use ABSOLUTE paths. The project root is `/config/workspace/Infantalizer`. The template and MDTM templates live under `/config/.claude/`, not the project `.claude/`. The framework being documented is under `/config/workspace/Infantalizer/laf-adaptation/`.

---

## EXISTING_FILES

### Top-level `laf-adaptation/`
| Path | Purpose | ~Lines |
|---|---|---|
| `laf-adaptation/CLAUDE.md` | Provenance model (ADOPTED/NATIVE/BUILD-NEW), boundary-contract summary, conventions, the 6 constraints, tree map | 191 |
| `laf-adaptation/VENDOR.md` | THE boundary contract manifest: pinned upstream SHA + per-file sha256 (laf + upstream), provenance class per file | ~ |
| `laf-adaptation/UPSTREAM-SYNC.md` | The 6-step upstream-sync procedure for the vendored CWS subset | ~ |
| `laf-adaptation/NOTICE`, `LICENSE-CWS` | Apache-2.0 attribution for the vendored CWS files | — |
| `laf-adaptation/.githooks/pre-commit` | Opt-in boundary-check enforcement wrapper | — |

### `agents/` (16 files — NOTE: CLAUDE.md §1 says "15" — STALE, see cross-val)
Rewrite-workflow agents (the 11-step order): `analyst` (NATIVE), `muse` (ADOPTED — orchestrator), `writer` (ADOPTED-PATCHED — the ONE demonstration of the boundary contract, +1 skills line), `critic`, `editor`, `continuity-checker`, `reader-sim` (ADOPTED quartet + reader), `safety-verifier` (NATIVE — distinct 5th reviewer), `tier-coordinator` (BUILD-NEW), `chronicler` (BUILD-NEW). Prep: `prep-cordinator` (NATIVE — the prep orchestrator; NOTE the intentional-looking spelling "cordinator"). Supporting ADOPTED: `brainstormer`, `character-sim`, `outliner`, `style-creator`, `web-researcher`. Total agent bodies ≈ 929 lines.
- Frontmatter dialect: Claude-native (`name`, `description`, `model` ∈ {opus,sonnet,haiku,inherit}, `skills` fully-qualified `laf-adaptation:<skill>`, `tools`). NO Mars keys.
- Key per-agent facts to extract: model, skills list, tools (esp. which agents are READ-ONLY: critic/reader-sim/continuity-checker have Read/Glob/Grep only; writer/chronicler/tier-coordinator/safety-verifier can Write), run-gate, inputs/outputs.

### `skills/` (18 dirs — NOTE: CLAUDE.md §1 says "16" — STALE, see cross-val)
- **NATIVE (3):** `adaptation-tiers` (5-tier axis, Piaget/Kohlberg), `adaptation-rules` (transform rules incl. Agency Externalization; key-tolerant schema-drift reader), `source-fidelity` (v2.0 anti-hallucination protocol, CERTAIN/PROBABLE/UNCERTAIN, ABORT-on-NO-ACCESS, the analysis v2.0 schema).
- **BUILD-NEW (1):** `adaptation-safety` (6-section safety rubric, T1-2 blocking / T3 advisory / T4-5 skip).
- **NATIVE prep-related:** `prep` (8-stage onboarding procedure), `thematic-fidelity` (meaning-preservation invariant, the analyst `meaning` field + tier-coordinator Check D).
- **ADOPTED (~12 CWS):** `creative-writing-craft`, `creative-writing-modes`, `writing-principles`, `writing-staffing`, `llm-writing`, `story-memory`, `story-review`, `kb-management`, `shared-dao`, `intent-modeling`, `grill-with-docs`, `creative-research`. Skill bodies ≈ 1262 lines total.
- Each skill: `SKILL.md` with `name` + `description` frontmatter only; NATIVE skills have `resources/`.

### `kb/` layers
- **NATIVE:** `tiers/` (`tier_1.yaml`, `tier_2.yaml`, `tier_3.yaml`, `tier_5.yaml` — thresholds, linguistic limits, transformation_rules; T4 interpolated at request time, never stored); `adaptation-mapping/` (`universal-mappings.yaml` + `<work>-mapping.yaml`, e.g. `narnia-mapping.yaml` 6-key form with `meaning:`); `adaptations/<work>/tier-<N>/` (graft G1 — per-tier divergent canon: `continuity.md`, `decisions.md`, `chapters/ch-<NN>/{adapted.md,analysis.yaml,canon-delta.md}`).
- **ADOPTED scaffold (runtime-populated):** `canon/<work>/`, `characters/`, `world/`, `timeline/<work>.md`, `styles/`, `issues/`, `vocab.md`.
- Live example present: `kb/adaptations/narnia/tier-{1,2,3,5}/` and `kb/canon/narnia/ch-01.md` + `kb/timeline/narnia.md` (produced this session), plus `kb/adaptations/tolkien/` (exemplar).

### `scripts/`
- `check_boundary.py` (737 lines) — THE only runtime script (ADR-006: a validation tool, not a runtime). Rules A/A′/B/C/C′/D/E/F/F′ + CH-1..6 hardening. Modes: verify (default, "Mode V"), `--init --upstream`, `--report`, `--upstream <dir>` ("Mode U"). Path-rooted to `laf-adaptation/`.
- `test_check_boundary.py` — its test suite.

### `source/`, `work/`, `templates/`
- `source/<work>/ch-<NN>.txt` — BUILD-NEW: the work being adapted (read-only reference). `source/narnia/ch-01.txt`, `source/tolkien/`.
- `work/` — ADOPTED lifecycle: `analysis/` (NATIVE, `ch-<NN>.yaml` + `ch-<NN>-cross-tier.md`), `drafts/`, `critique-reports/`, `safety-reports/` (NATIVE). Also `work/prep/<slug>/` (the prep package: 8 fixed files `00-work-context.md` … `70-traceability.md`).
- `templates/work-mapping-template.yaml` (NATIVE, carried verbatim).

### Pipeline entry points (in the repo, NOT under laf-adaptation/)
- `.claude/commands/laf/prep.md` → `/laf:prep` → delegates to `prep-cordinator`.
- `.claude/commands/laf/rewrite.md` → `/laf:rewrite --work <slug>` → reads the prep package by hardcoded path, greenlight-gates, hands to `muse` for the 11-step per-chapter workflow.

### Supporting docs (for Doc Analyst cross-validation — treat as HINTS, verify against code)
- `docs/design_decisions/001-five-tier-system.md`, `003-agency-externalization.md`, `006-adversarial-task-review.md` (ADRs).
- `docs/native-prep/design/` — `path-contract.md`, `package-schemas.md`, `prep-agent-schemas.md`, `prep-skill-specs.md`, `boundary-verification.md`, `DESIGN.md` (BUILD-TIME design pack; provenance pointers, not runtime deps).
- `docs/native-prep/30-current-framework-map.md` (a prior framework map — likely partially stale).
- `docs/guides/CHOOSING_A_TIER.md`, `docs/guides/lion-witch-wardrobe/ADAPTATION_GUIDE.md`.

---

## PATTERNS_AND_CONVENTIONS

- **Provenance model (load-bearing):** every file is ADOPTED (vendored CWS, never edit body), ADOPTED-PATCHED (exactly one: `agents/writer.md`, +1 additive skills line), NATIVE (LAF-authored domain spine), or BUILD-NEW (greenfield). Enforced by `check_boundary.py` against `VENDOR.md` hashes. Evidence: `laf-adaptation/CLAUDE.md` §1, `VENDOR.md`.
- **Boundary contract (constraint #6):** NATIVE knowledge enters ADOPTED agents ONLY via `skills:` frontmatter — never by editing an adopted body. Keeps the vendored subset a clean 3-way-merge fast-forward.
- **Tier axis first-class (constraint #1):** `active_tier` is an explicit param for `safety-verifier`/`chronicler`; `tier-coordinator` fans a `tiers` set; `writer` gets tier via scene brief + `/adaptation-rules`; `analyst` is tier-INVARIANT (no active_tier). Tier profiles in `kb/tiers/`. T4 interpolated (T3 floor, T5 ceiling, conservative midpoint; agency_externalization FORBIDDEN), never stored.
- **Intentional schema drift (key-tolerant reads):** T1-3 use `conflict_to_cooperation`/`death_euphemism`; T5 uses `conflict_handling`/`death_handling`. Normalization lives in the READER skills (`.get(a) or .get(b)`), never in the vendored YAML. Evidence: CLAUDE.md §3, adaptation-rules SKILL.md.
- **The 6 constraints** (CLAUDE.md §3): (1) tier axis first-class, (2) uncertainty discipline (source-fidelity ABORT gate), (3) safety_check (safety-verifier gates kb promotion), (4) quartet-of-4-distinct + 5th (critic/editor/reader-sim/continuity-checker + safety-verifier; editor never folded — Rule D), (5) work/ vs kb/ split (chronicler writes kb only on muse-accept), (6) skill-vs-agent boundary.
- **UV-only for Python** (`uv run python scripts/check_boundary.py`).
- **Frontmatter dialect:** Claude-native only; NO Mars keys (`type`, `model-invocable`, `effort`, etc.).

---

## FEATURE_ANALYSIS

**Subsystems (this is the Section 5 backbone):**

1. **The rewrite pipeline & 11-step workflow** — `/laf:rewrite` → `muse` orchestrates per-chapter: analyst → muse → writer → critic → editor → writer(rev) → continuity-checker → safety-verifier → reader-sim → tier-coordinator → chronicler. Cross-tier reconciliation (Checks A/B/C/D) then canon promotion on accept. COMPLEXITY: complex (state machine + multi-agent, 120-200 line budget).
2. **The prep pipeline** — `/laf:prep` → `prep-cordinator` 8-stage onboarding: two-track research → source-fidelity analysis → challenge taxonomy → derived confidence-scored mapping → question gate (HALT) → greenlight (HALT) → dual-form promotion → handoff. Emits `work/prep/<slug>/` (8 files). COMPLEXITY: complex.
3. **The tier axis** — 5-tier Piaget/Kohlberg developmental model; `kb/tiers/*.yaml` profiles (thresholds, linguistic, transformation_rules); T4 interpolation; the transformation-mode ladder (Agency Externalization: mandatory T1-2 → optional T3 → forbidden T4-5). COMPLEXITY: standard.
4. **The transformation rules & meaning-preservation** — `adaptation-rules` (violence/conflict/death/villain/heroism/character + Agency Externalization), `source-fidelity` (v2.0 analysis schema + confidence tags), `adaptation-safety` (6-section rubric), `thematic-fidelity` (meaning invariant, Check D). COMPLEXITY: complex.
5. **The kb layer & work/kb split** — dual-layer canon (shared tier-neutral `kb/canon/` + per-tier `kb/adaptations/<work>/tier-<N>/`), the 3 chronicler invariants, adaptation-mapping cascade, `work/` staging vs `kb/` durable. COMPLEXITY: standard.
6. **The boundary contract & provenance** — `check_boundary.py` Rules A-F, `VENDOR.md` manifest, ADOPTED/NATIVE/BUILD-NEW model, Mode V vs Mode U, the pre-commit hook + CI. COMPLEXITY: complex.

**Integration boundaries:** the two `/laf:*` slash commands (harness → pipeline); the `path-contract.md` hardcoded read/write ownership; the greenlight gate (prep→rewrite handoff); the safety-verifier verdict gating kb promotion; the tier-coordinator RECONCILED gate gating chronicler; the boundary check gating commits/CI.

**Not applicable (mark N/A):** Section 6 State Management, Section 7 Component Inventory (no client-side state / UI components — this is a prompt+YAML framework). Section 11 Performance is minimal (no runtime; "performance" = prompt/token & agent-parallelism shape) — include a short note, not a full profile.

---

## RECOMMENDED_OUTPUTS

**Phase 2 — Codebase research files (6 agents, top of Standard range — justified by ~3300-line corpus + 6 distinct subsystems):**
| # | File | Type | Scope |
|---|---|---|---|
| 01 | `research/01-agents-rewrite-workflow.md` | Code Tracer + Architecture Analyst | All 16 `agents/*.md`: frontmatter (model/skills/tools), the 11-step workflow order + branch gates, muse orchestration, per-agent run-gates & I/O, which agents are read-only vs write-capable |
| 02 | `research/02-skills-layer.md` | Code Tracer | All 18 `skills/*/SKILL.md`: NATIVE vs ADOPTED split, the domain skills (adaptation-rules/tiers/safety/source-fidelity/thematic-fidelity/prep), the skill-vs-agent boundary mechanism, key-tolerant schema-drift readers |
| 03 | `research/03-tier-axis-and-kb.md` | Architecture Analyst | `kb/tiers/*.yaml` (all 4 profiles + T4 interpolation), the transformation-mode ladder, `kb/adaptation-mapping/`, `kb/adaptations/<work>/tier-<N>/` graft G1, dual-layer canon, chronicler's 3 invariants, work/ vs kb/ split |
| 04 | `research/04-prep-pipeline.md` | Integration Mapper | `/laf:prep` + `prep-cordinator.md` 8-stage procedure, `work/prep/<slug>/` 8-file package, `docs/native-prep/design/path-contract.md` read/write ownership, the two HALT gates, dual-form promotion (6-key kb copy vs 5-key root copy) |
| 05 | `research/05-boundary-contract.md` | Architecture Analyst | `scripts/check_boundary.py` Rules A/A′/B/C/C′/D/E/F/F′ + CH-1..6, Modes V/U, `VENDOR.md` manifest semantics, ADOPTED/NATIVE/BUILD-NEW, `.githooks/pre-commit`, CI location, UPSTREAM-SYNC 6 steps |
| 06 | `research/06-docs-crossval.md` | Doc Analyst | Cross-validate `docs/` (ADRs, native-prep/design, framework-map, guides) + `CLAUDE.md` claims against the ACTUAL tree. MANDATORY: verify the provenance counts — CLAUDE.md §1 claims "15 agent files" and "16 skill dirs" but the tree has 16 agents / 18 skills → tag `[CODE-CONTRADICTED]`. Apply the Documentation Staleness Protocol to every architectural claim. |

**Phase 4 — Web research (1 agent, optional, gap-driven):**
- `research/web-01-developmental-tiers.md` — Piaget preoperational/concrete-operational/formal-operational stages + Kohlberg moral stages, to ground/verify the tier axis's developmental basis claims (the `kb/tiers/*.yaml developmental_basis` blocks). MARK as external context; codebase is source of truth.

**Phase 5 — Synthesis files (5 files; backend-style framework → skip Sections 6, 7; Section 11 minimal):**
| Synth file | Template sections | Source research |
|---|---|---|
| `synthesis/synth-01-overview-architecture.md` | 1 Overview, 2 Architecture (2.1 diagram, 2.2 subsystem map, 2.3 design decisions, 2.4 stack) | 01, 03, 05, 06 |
| `synthesis/synth-02-directory-dataflow.md` | 3 Directory Structure, 4 Data Flow (prep flow + rewrite flow diagrams) | 01, 02, 03, 04 |
| `synthesis/synth-03-subsystems.md` | 5 Subsystem Reference (5.1 rewrite workflow, 5.2 prep pipeline, 5.3 tier axis, 5.4 transform rules & meaning, 5.5 kb layer, 5.6 boundary contract) | 01, 02, 03, 04, 05 |
| `synthesis/synth-04-integration-config-errors.md` | 8 API & Integration (the /laf:* commands, path-contract, gates), 9 Configuration (kb/tiers profiles, VENDOR.md, greenlight), 10 Error Handling (ABORT gate, FAIL→revise loop, CONFLICT gate, boundary-check failures) | 04, 05, 03 |
| `synthesis/synth-05-conventions-extension-debt.md` | 12 Conventions (provenance rules, schema-drift, UV-only, frontmatter dialect), 13 Extension Guide (add a work / add a NATIVE skill / add an agent via boundary / add/adjust a tier), 14 Tech Debt (stale CLAUDE.md counts, prep-cordinator spelling, T4-never-stored caveat, any [CODE-CONTRADICTED]) | 02, 05, 06 |
- Sections 6, 7 → N/A (no client state / UI components). Section 11 → minimal note. Sections 15 (Verification), 16 (Glossary — tier, active_tier, ADOPTED/NATIVE/BUILD-NEW, graft G1/G2/G3, Agency Externalization, Deep/Deeper Magic-style work terms, compound scene, meaning, Mode V/U) → written at assembly.

---

## SUGGESTED_PHASES

- **Phase 1 Preparation:** confirm scope from these notes; read the template at `/config/.claude/templates/documents/technical_reference_template.md`; confirm Standard tier; task folder already created at `.dev/tasks/to-do/TASK-TECHREF-laf-framework-20260708-164258/` with research/synthesis/qa/reviews subfolders.
- **Phase 2 Deep Investigation:** spawn the 6 codebase research agents above IN PARALLEL (one checklist item each), each with the Codebase Research Agent Prompt + Incremental Writing + Documentation Staleness protocols. Read-only investigation.
- **Phase 3 Completeness Verification (Standard gate = 3 agents):** 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth), parallel, fix_authorization:false → consolidate → gap-fill → verify. Max 2 fix cycles. (6 research files ≤ 6 threshold → no partitioning.)
- **Phase 4 Web Research:** 1 optional agent (developmental-tiers grounding) if Phase 3 flags the developmental_basis claims as needing external confirmation.
- **Phase 5 Synthesis + gate (Standard gate = 3 agents):** 5 synthesis agents in parallel (>4 files → partition the gate). Then 1 rf-analyst (synthesis-accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) → consolidate → 1 fix agent → 2-agent verify. Max 2 cycles.
- **Phase 6 Assembly + Lens QA + Fidelity (Standard):** rf-assembler → doc. Then Gate 3 = 7 agents (3 rf-qa structural: template-conformance, internal-consistency, evidence-quality; 3 rf-qa-qualitative: actionability, domain-accuracy, crossref-chain; 1 domain lens: code-example-accuracy) → consolidate → 1 fix → 2 verify (max 2 cycles). Then Gate 4 fidelity = 2 rf-qa (semantic-coverage + detail-preservation), reading actual `laf-adaptation/` source + the assembled doc → consolidate → fix → verify (max 2 cycles).
- **Phase 7 Present & Complete:** summary, Task Log, frontmatter → 🟢 Done, artifact locations, gaps for manual review. Anti-orphaning: completion items inside Phase 7.

---

## TEMPLATE_NOTES

- **Tier:** Standard (user-selected). Line budget 800–1200. Sections required: all numbered; skip conditional `(if applicable)` sections that don't apply.
- **N/A sections (with rationale):** §6 State Management — N/A (framework has no client-side runtime state; "state" is on-disk kb artifacts, covered in §5.5). §7 Component Inventory — N/A (no UI components). §11 Performance — near-N/A (no runtime; include one short subsection on agent-parallelism/token shape and the "one script" ADR-006 constraint, not a measured profile).
- **Feature Type:** "Framework / Prompt-and-Config System" (not Frontend/Backend). Source Location: `laf-adaptation/`.
- **Subsystem depth:** 6 subsystems in §5; keep complex ones (rewrite workflow, prep pipeline, boundary contract, transform rules) at 120-200 lines, standard ones (tier axis, kb layer) at 80-120. Total §5 is the bulk of the budget.
- **Evidence discipline:** every claim cites `laf-adaptation/...:line` or a `SKILL.md`/agent body. Doc-sourced claims (from `docs/`) carry `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]`.
- **ASCII diagrams** for: the 11-step workflow, the prep 8-stage flow, the dual-layer canon, the provenance/boundary enforcement.

---

## AMBIGUITIES_FOR_USER

1. **Tier tension (noted, not blocking):** user chose Standard for a cross-cutting framework the skill heuristic would call Heavyweight. Honored Standard by marking frontend sections N/A and keeping §5 dense. If the assembled doc can't fit the subsystems within ~1200 lines without losing fidelity, Phase 6 should flag it and recommend either an upgrade to Heavyweight or splitting the boundary-contract subsystem into its own reference. Do NOT silently overflow.
2. **Known stale-doc finding (pre-identified, must be surfaced not resolved-away):** `laf-adaptation/CLAUDE.md` §1 provenance counts ("15 agent files", "16 skill dirs") contradict the live tree (16 agents, 18 skills — `prep-cordinator` + prep-era skills were added after that text). This is a `[CODE-CONTRADICTED]` doc-staleness item for Tech Debt §14, NOT a defect in the framework. The tech reference documents the ACTUAL tree (16/18) and records the CLAUDE.md drift as tech debt. Phase 2 Agent 06 owns confirming the exact current counts and classification split.
3. **Output domain:** chose `docs/laf/`. If the user prefers `docs/architecture/` or `docs/native-prep/`, the final path can be moved — not blocking.
