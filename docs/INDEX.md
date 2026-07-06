# Project Index — Infantalizer / Literary Adaptation Framework (LAF)

> Auto-generated knowledge base. Treat as a map, not a substitute for reading source.
> Last indexed: 2026-07-04 against working tree at `HEAD` = `604e25f` (branch `feature/laf-0.1-cws-hybrid`).
> Untracked at index time: `.claude/`, `.dev/`.

---

## 0. TL;DR — the repo now has TWO layers

This repository ships **two related but distinct adaptation systems**. Do not conflate them.

| Layer | Location | What it is | Status |
|-------|----------|-----------|--------|
| **LAF v1.0** (root framework) | `config/`, `prompts/`, `templates/`, `docs/` | The original **prompt + YAML-config** framework. No executable code. Load configs + prompts into an LLM to run an adaptation workflow. | Shipped (CHANGELOG `1.0.0`) |
| **LAF 0.1 — CWS Hybrid** (Path C) | `laf-adaptation/` | An **agent + skill** system that vendors the `haowjy/creative-writing-skills` (CWS) machinery and grafts LAF's tier/safety spine on top via a hard **boundary contract**. Added in commit `604e25f`. | 0.1 DONE (Phases 0–2) |

The two layers encode the **same domain model** (five developmental tiers, agency externalization, anti-hallucination / source-fidelity, safety verification) in two different substrates: **flat prompts+YAML** (root) vs. **Claude Code agents+skills+kb** (`laf-adaptation/`). The tier YAMLs in `laf-adaptation/kb/tiers/` are byte-faithful carried copies of the root `config/` — see §12.

---

## 1. What this project is

**Infantalizer** (repo directory name) is the **Literary Adaptation Framework (LAF)** — a system for adapting complex literary works into age-appropriate versions across developmental tiers (ages 3–17), grounded in developmental psychology (Piaget's cognitive stages, Kohlberg's moral reasoning).

**Core innovation:** age-appropriateness is treated as **configuration, not code**. The same conceptual transform engine applies different rule sets per tier.

**Provenance:** generalized from a one-off preschool adaptation of Tolkien's *The Return of the King* ("The Happiness Project") into a modular, work-agnostic framework — then (0.1) re-expressed as a vendored-CWS agent/skill hybrid.

**It is not software.** There is no runtime, CLI, or application. The *only* executable file in the entire repo is `laf-adaptation/scripts/check_boundary.py`, and it is a **validation tool** for the boundary contract, not a runtime (ADR-006).

---

## 2. Quick orientation (read these first)

| File | Role |
|------|------|
| `README.md` | Public face of the **root v1.0** framework. Quick start, tier table, repo layout. |
| `docs/SPEC.md` | **Canonical** v1.0 system specification (condensed). |
| `docs/guides/QUICK_START.md` | 5-step root workflow: pick tier → load configs → analyze → transform → verify. |
| `laf-adaptation/CLAUDE.md` | **Canonical** guide to the 0.1 hybrid: provenance model, boundary contract, conventions, layout. Read before touching `laf-adaptation/`. |
| `laf-adaptation/VENDOR.md` | The boundary contract's data: pinned upstream SHA + per-file class/hash manifest. |
| `laf-adaptation/UPSTREAM-SYNC.md` | The 6-step procedure for re-vendoring a newer CWS upstream. |
| `CHANGELOG.md` | v1.0.0 release contents (root layer). |
| `CONTRIBUTING.md` | PR process + style guide (YAML/Markdown/naming). |

---

## 3. Repository layout (actual, at `604e25f`)

```
Infantalizer/
├── README.md                          # Public entry (root v1.0 framework)
├── CHANGELOG.md                       # v1.0.0 release log
├── CONTRIBUTING.md                    # PR + style guide
├── LICENSE                            # MIT (root project)
├── .gitignore
├── ISSUE_TEMPLATE/new_work_mapping.md # Issue template for new work-mapping requests
├── .github/workflows/boundary.yml     # CI: runs laf-adaptation boundary check (working-dir: laf-adaptation)
│
├── config/                            # ROOT LAYER — "configuration over code"
│   ├── age_profiles/                  # Per-tier developmental configs (YAML)
│   │   ├── tier_1_preschool.yaml          # ages 3-5  — full transform, max safety
│   │   ├── tier_2_early_elementary.yaml   # ages 6-8  — contest paradigm
│   │   ├── tier_3_middle_elementary.yaml  # ages 9-11 — TRANSITION tier
│   │   └── tier_5_young_adult.yaml        # ages 15-17 — minimal transform
│   ├── transformation_rules/
│   │   ├── thematic.yaml              # Violence/death/conflict/agency/heroism by tier
│   │   └── character.yaml             # Archetype mappings + heroism translation
│   └── concept_mapping/
│       ├── universal_mappings.yaml    # Cross-work concept translations
│       └── templates/tolkien_mapping.yaml # LOTR-specific overrides
│
├── prompts/                           # ROOT LAYER — the runtime workflow (Markdown prompts)
│   ├── analysis/chapter_analysis.md   # v2.0 anti-hallucination protocol (Phases 0–4)
│   ├── transformation/
│   │   ├── tier_1_transform.md        # Preschool adaptation rules + example
│   │   └── tier_3_transform.md        # Transition-tier adaptation rules + example
│   └── verification/safety_check.md   # Post-generation check for Tier 1–2 (6 sections)
│
├── templates/work_mapping_template.yaml   # Blank scaffold for new literary works (root)
│
├── docs/
│   ├── INDEX.md                       # THIS FILE
│   ├── SPEC.md                        # v1.0 condensed spec (canonical)
│   ├── guides/QUICK_START.md
│   ├── design_decisions/              # ADR-style records (001, 003, 006 + README)
│   └── conversation_logs/             # Development discussion archives (02, 03 + README)
│
├── laf-adaptation/                    # ═══ LAF 0.1 CWS HYBRID (see §11–§13) ═══
│   ├── CLAUDE.md  VENDOR.md  UPSTREAM-SYNC.md  NOTICE  LICENSE-CWS
│   ├── agents/    (15 .md files)      # 11 adopted-provenance + 2 NATIVE + 2 BUILD-NEW
│   ├── skills/    (16 dirs)           # 12 ADOPTED + 3 NATIVE + 1 BUILD-NEW
│   ├── kb/                            # tiers/ adaptation-mapping/ adaptations/ + adopted layers
│   ├── source/                        # BUILD-NEW: the work being adapted (read-only)
│   ├── work/                          # lifecycle: analysis/ drafts/ critique-reports/ safety-reports/
│   ├── templates/work-mapping-template.yaml
│   ├── scripts/check_boundary.py      # the ONLY script — boundary-contract enforcement
│   └── .githooks/pre-commit           # opt-in enforcement wrapper
│
└── .dev/releases/current/0.1/         # Vendored v0.1 archive + design pack (see §10)
```

---

## 4. Core mental model (root v1.0 layer)

The root framework is a three-stage pipeline. Every tier-specific behavior is configured, not coded:

```
SOURCE TEXT
    │
    ▼
[ prompts/analysis/chapter_analysis.md ]   ← v2.0 anti-hallucination protocol
    │   Phase 0: source-access declaration (FULL / PARTIAL / MEMORY / NONE)
    │   Phase 1: essential verification (title, chapter, opening/closing lines)
    │   Phase 2: dual-pass documentation (structure+events, then summary)
    │   Phase 3: transformation flags (violence / death / emotional / abstract)
    │   Phase 4: consistency check + confidence tags (CERTAIN/PROBABLE/UNCERTAIN)
    ▼
[ prompts/transformation/tier_N_transform.md ]   ← applies age profile
    │   loads: config/age_profiles/tier_N_*.yaml
    │   loads: config/transformation_rules/{thematic,character}.yaml
    │   loads: config/concept_mapping/{universal,work-specific}.yaml
    ▼
[ prompts/verification/safety_check.md ]   ← mandatory for Tier 1–2
    ▼
ADAPTED CHAPTER + transformation log + confidence report
```

**Config cascade (most-specific wins):** universal_mappings.yaml → work-specific mapping → age_profile rules → transformation_rules.

---

## 5. Tier system at a glance (shared by both layers)

| Tier | Ages | Root file | 0.1 file | Piaget stage | Paradigm | Headline rule |
|------|------|-----------|----------|--------------|----------|---------------|
| 1 | 3–5 | `tier_1_preschool.yaml` | `kb/tiers/tier_1.yaml` | Preoperational | Full transform, max safety | Violence→cleanup, death→"new adventure", agency externalization MANDATORY |
| 2 | 6–8 | `tier_2_early_elementary.yaml` | `kb/tiers/tier_2.yaml` | Early Concrete | **Contest paradigm** | Violence→competition, death→"passed away" |
| 3 | 9–11 | `tier_3_middle_elementary.yaml` | `kb/tiers/tier_3.yaml` | Concrete | **TRANSITION** | "Died" acceptable, moral ambiguity OK, agency externalization OPTIONAL |
| 4 | 12–14 | *(deferred — interpolate 3+5)* | *(interpolated at request time)* | Early Formal | Near-adult | Tragedy permitted, full villain complexity; `agency_externalization = FORBIDDEN` |
| 5 | 15–17 | `tier_5_young_adult.yaml` | `kb/tiers/tier_5.yaml` | Formal | Minimal transform | Preserve author intent; accessibility, not sanitization |

**Tier 3 is the load-bearing inflection point.** Tiers 1–2 protect from complexity; Tier 3+ scaffolds it. See `docs/design_decisions/001-five-tier-system.md`.

**Tier 4 is never stored as a file** in either layer — it is interpolated (T3 floor, T5 ceiling, conservative midpoint).

**Agency Externalization** is the framework's signature rule: MANDATORY T1–2, OPTIONAL T3, FORBIDDEN T4–5 (patronizing above T3). See `docs/design_decisions/003-agency-externalization.md`.

---

## 6. File-by-file capability map (root v1.0 layer)

### 6.1 `config/age_profiles/*.yaml` — tier definitions
Each carries: `profile` metadata, `developmental_basis` (Piaget + Kohlberg), `thresholds`, `linguistic` rules, `transformation_rules` (mode per rule type), `safety` constraints.
- **tier_1** — forbidden vocab list, ≤12-word sentences, ≤800-word chapters, positive resolution required.
- **tier_2** — contest vocabulary, ≤15-word sentences, mild cliffhangers allowed.
- **tier_3** — `requires_clear_good_bad: false`, parallel plotlines + flashbacks, ≤20-word sentences.
- **tier_5** — `agency_externalization: forbidden`, preserves authorial voice, footnotes for archaic language.

### 6.2 `config/transformation_rules/`
- **thematic.yaml** — per-tier translations for violence, conflict, agency, death-handling, villain-motivation, heroism. The "translation table" core.
- **character.yaml** — archetype system + `heroism_translation` subroutine + hard cases (Gollum, Denethor).

### 6.3 `config/concept_mapping/`
- **universal_mappings.yaml** — abstract concepts (death, evil, war, despair…) translated per tier. Work-agnostic.
- **templates/tolkien_mapping.yaml** — per-character tier-N archetypes and per-concept overrides for LOTR.

### 6.4 `prompts/`
- **analysis/chapter_analysis.md** — 4-phase source-analysis prompt with confidence tags. Aborts on NO ACCESS.
- **transformation/tier_1_transform.md** / **tier_3_transform.md** — tier-specific generation with worked examples.
- **verification/safety_check.md** — 6-section post-gen verification. Mandatory for T1–2.

### 6.5 `templates/work_mapping_template.yaml`
Blank scaffold: `work_metadata`, `characters` (tier_N subfields), `concepts`, `key_scenes`, `master_translation_table`.

---

## 7. Workflow (root v1.0)

1. **Pick tier** → load `config/age_profiles/tier_N_*.yaml`.
2. **Load engine rules** → `config/transformation_rules/{thematic,character}.yaml`.
3. **Load concept maps** → `universal_mappings.yaml` + work-specific `templates/<work>_mapping.yaml`.
4. **Analyze** with `prompts/analysis/chapter_analysis.md`.
5. **Transform** with `prompts/transformation/tier_N_transform.md`.
6. **Verify** (T1–2 mandatory) with `prompts/verification/safety_check.md`.
7. **Emit** adapted chapter + transformation log + confidence tags.

---

## 8. Key design decisions (ADR index)

| ADR | Topic | Takeaway |
|-----|-------|----------|
| `001-five-tier-system.md` | Tier boundaries | 5 tiers grounded in Piaget/Kohlberg; Tier 3 is the natural inflection; Tier 4 interpolable. |
| `003-agency-externalization.md` | The signature rule | MANDATORY T1–2, OPTIONAL T3, FORBIDDEN T4–5. |
| `006-adversarial-task-review.md` | Scope discipline | Adversarial debate cut the task list 22 → 7 (68%). Established that this is a prompt framework, not software — and that there is exactly one script. |

Conversation logs in `docs/conversation_logs/` preserve the discussion behind these decisions.

---

## 9. Conventions (root)

- **YAML:** 2-space indent, comments for complex sections.
- **Markdown:** ATX headers, fenced code blocks.
- **Naming (root):** `lowercase_with_underscores.yaml` / `.md`. **Note:** the `laf-adaptation/` layer uses `lowercase-with-hyphens` for skills/agents/kb (CWS convention) — the two naming styles are intentional, per layer.
- **Tier references in prose:** `Tier 1`, `Tier 3`, capitalized.
- **Confidence tags:** `CERTAIN` / `PROBABLE` / `UNCERTAIN` — always uppercase.

---

## 10. The `.dev/releases/current/0.1/` archive — caveat

Contains an **archived pre-v1.0 release** plus the **build-time design pack** for the 0.1 hybrid. Not part of any shipping runtime tree.

- Older v0.1 `SPEC.md` (~314 lines) is good for **design rationale**, but the canonical spec is `docs/SPEC.md`. Do not cite v0.1 spec sections as current.
- `.dev/releases/current/0.1/design/` holds the **design pack** (`DESIGN.md`, `boundary-contract.md`, `kb-formats.md`, `safety-rubric.md`, `skill-specs.md`, `agent-schemas.md`, ADR-006). `laf-adaptation/` bodies cite these as **build-time provenance pointers, not runtime dependencies** — the shipped tree is self-sufficient (every contract is restated in-tree).
- May contain a nested vendored clone with its own `.git/` and license — not authored by this project.

**Cross-reference rule:** when `.dev/` disagrees with `docs/` or a shipped tree, the **shipped / `docs/` version wins**.

---

## 11. `laf-adaptation/` — the LAF 0.1 CWS Hybrid (overview)

A Claude-Code-native **agent + skill** system that vendors the domain-agnostic machinery from `haowjy/creative-writing-skills` (CWS) and grafts LAF's domain spine (tiers, source-fidelity, safety) on top **without editing any vendored body**. Canonical guide: `laf-adaptation/CLAUDE.md`.

### 11.1 Provenance model — every file is one of four classes

| Class | Meaning | Editing rule |
|-------|---------|--------------|
| **ADOPTED-CLEAN** | CWS file vendored byte-identical after one uniform prefix rewrite (`creative-writing-skills:` → `laf-adaptation:`). | Never edit the body. |
| **ADOPTED-PATCHED** | Exactly one file: `agents/writer.md`. Adopted body + **one** additive `skills:` frontmatter line. | Frontmatter-additive only; body byte-identical. |
| **NATIVE** | LAF-authored domain spine. | Author freely; must not collide with an upstream filename (Rule E); not hash-pinned. |
| **BUILD-NEW** | Greenfield in *both* systems (tier-aware canon + cross-tier reconciliation). | Same rules as NATIVE. |

**The load-bearing rule (constraint #6, the "boundary contract"):** NATIVE knowledge enters ADOPTED agents **only via `skills:` frontmatter — never by editing an adopted body**. This is what keeps the adopted subset patch-clean and upstream-syncable. *If you think you must edit an adopted file: STOP. Add a skill instead.*

### 11.2 Enforcement

- `uv run python laf-adaptation/scripts/check_boundary.py` (verify mode) — exits non-zero on any violation of **Rules A–F**: adopted-hash match, ADOPTED-CLEAN == upstream-after-rewrite, `writer.md` diff is frontmatter-only + additive, G3 quartet intact + `editor.md` never folded, no NATIVE/BUILD-NEW name collision, every managed file manifested.
- Opt-in pre-commit hook: `git config core.hooksPath laf-adaptation/.githooks`. Bypass once with `git commit --no-verify`.
- CI: `.github/workflows/boundary.yml` at the **repo root**, runs with `working-directory: laf-adaptation`.
- **UV-only** for the script (never `python -m`, bare `pip`, or `python script.py`).

---

## 12. `laf-adaptation/` — agent & skill inventory

**15 agents** (`laf-adaptation/agents/*.md`): 11 adopted-provenance + 2 NATIVE + 2 BUILD-NEW.

| Agent | Class | Role / tier handling |
|-------|-------|----------------------|
| `brainstormer`, `character-sim`, `continuity-checker`, `critic`, `editor`, `muse`, `outliner`, `reader-sim`, `style-creator`, `web-researcher` | ADOPTED-CLEAN | Vendored CWS review/orchestration crew. `editor.md` is **never** folded/modified (G3 invariant). |
| `writer` | ADOPTED-PATCHED | The sole demonstration of the boundary contract: one added line `- laf-adaptation:adaptation-rules`. Receives the operative tier via scene brief + `/adaptation-rules`, not a declared param. |
| `analyst` | NATIVE | **Tier-invariant** — takes NO `active_tier`; produces one shared, tier-neutral source analysis. Phase-0 ABORT-on-NO-ACCESS. |
| `safety-verifier` | NATIVE | Distinct **5th reviewer** (never merged into the adopted quartet). Consumes explicit `active_tier`; verdict blocks kb promotion on FAIL. |
| `chronicler` | BUILD-NEW | Consumes explicit `active_tier`; writes to `kb/` **only on muse-accept**. |
| `tier-coordinator` | BUILD-NEW | Fans across a **`tiers` set** (subset of {1,2,3,5}) to reconcile cross-tier renderings — does not take a single `active_tier`. |

**16 skills** (`laf-adaptation/skills/<name>/SKILL.md` + `resources/`): 12 ADOPTED + 3 NATIVE + 1 BUILD-NEW.

- **ADOPTED (12):** `creative-research`, `creative-writing-craft`, `creative-writing-modes`, `grill-with-docs`, `intent-modeling`, `kb-management`, `llm-writing`, `shared-dao`, `story-memory`, `story-review`, `writing-principles`, `writing-staffing`.
- **NATIVE (3):** `adaptation-tiers`, `adaptation-rules`, `source-fidelity` (the domain spine — tier axis, transformation rules, CERTAIN/PROBABLE/UNCERTAIN discipline).
- **BUILD-NEW (1):** `adaptation-safety` (the safety rubric).

Authoritative per-file class + hashes: `laf-adaptation/VENDOR.md` (upstream SHA `3338495…`, vendored 2026-07-03). The manifest has **more rows (64) than the Rule-F glob set (31)** because it also hashes adopted `resources/**` for diff integrity.

---

## 13. `laf-adaptation/kb/`, `source/`, `work/` — data layout

```
kb/
├── tiers/               NATIVE  — tier_1/2/3/5.yaml (byte-faithful copies of root config/; T4 interpolated)
├── adaptation-mapping/  NATIVE  — universal-mappings.yaml + tolkien-mapping.yaml (cascade)
├── adaptations/<work>/tier-<N>/   NATIVE graft G1 — per-tier canon keyed (work, tier, chapter):
│     chapters/ch-01/{adapted.md, analysis.yaml, canon-delta.md}, continuity.md, decisions.md
│     (present: tolkien tier-1, tier-3, tier-5)
├── canon/ characters/ world/ timeline/ styles/ issues/  ADOPTED layers (runtime-populated; .gitkeep + sample tolkien data)
└── vocab.md
source/    BUILD-NEW — the work under adaptation, read-only (source/tolkien/ch-01.txt + README)
work/      lifecycle — analysis/ (NATIVE), drafts/, critique-reports/, safety-reports/ (NATIVE)
templates/work-mapping-template.yaml   NATIVE, carried verbatim
```

**Carried-verbatim = zero rework.** `kb/tiers/*.yaml` and `kb/adaptation-mapping/*` are byte-faithful copies of root `config/`, including deliberate schema drift (T1–T3 `conflict_to_cooperation`/`death_euphemism` vs T5 `conflict_handling`/`death_handling`). Normalization belongs in the **reader skills** (key-tolerant `.get(a) or .get(b)`), never in the vendored file.

**`work/` vs `kb/` split (constraint #5):** the adopted `kb-management` lifecycle governs promotion; `chronicler` writes to `kb/` only on muse-accept. In-flight artifacts live under `work/`.

The sample `tolkien/ch-01` data across `source/`, `work/`, and `kb/adaptations/` is a **worked end-to-end example** (T1/T3/T5 drafts, critiques, safety reports) demonstrating the full pipeline.

---

## 14. Gaps and aspirational structure

Referenced somewhere but **not present** in the working tree:

- **Root layer:** `examples/`, `tests/`, `config/linguistic/` (consolidated into age profiles in v1.0), `docs/guides/ADDING_NEW_WORKS.md` (use `CONTRIBUTING.md` + template instead), root prompts `tier_2_transform.md` / `tier_5_transform.md` (only T1 + T3 shipped; see ADR-006).
- **Tier 4 profile** — intentionally deferred in both layers (interpolated, never stored).
- **Design-pack `§` references** inside `laf-adaptation/` (e.g. `DESIGN.md`, `boundary-contract.md`, `ADR-006`) resolve to `.dev/releases/current/0.1/design/`, not the shipped tree. Unreachable `§` refs are expected — the in-tree skill/agent body is the single source of truth at execution time.

---

## 15. Index freshness

Generated from a full-tree read at `HEAD` = `604e25f` on branch `feature/laf-0.1-cws-hybrid`. Re-run `/sc:index` when you: add tiers/prompts/work-mappings (root), add or re-vendor `laf-adaptation/` files (then also re-check `VENDOR.md` + `scripts/check_boundary.py`), or sync a newer `.dev/releases/current/` archive.
