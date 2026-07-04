# Project Index — Infantalizer / Literary Adaptation Framework (LAF)

> Auto-generated knowledge base. Treat as a map, not a substitute for reading source.
> Last indexed: 2026-07-03 against working tree at `HEAD` (no commits yet — all files untracked).

---

## 1. What this project is

**Infantalizer** (repo directory name) ships as the **Literary Adaptation Framework (LAF) v1.0** — a prompt-and-config system for adapting complex literary works into age-appropriate versions across five developmental tiers (ages 3–17). It is **not software**: there is no executable code, CLI, or runtime. It is a set of YAML configs + Markdown prompts designed to be loaded into Claude Code (or any LLM) as the operating instructions for an adaptation workflow.

**Core innovation:** developmental psychology (Piaget, Kohlberg) is encoded as **YAML configuration, not code**. The same conceptual transform engine applies different rule sets per tier.

**Provenance:** generalized from a one-off preschool adaptation of Tolkien's *The Return of the King* ("The Happiness Project") into a modular, work-agnostic framework.

---

## 2. Quick orientation (read these first)

| File | Role |
|------|------|
| `README.md` | Public face. Quick start, tier table, repo layout. |
| `docs/SPEC.md` | **Canonical** v1.0 system specification (131 lines, condensed). |
| `docs/guides/QUICK_START.md` | 5-step workflow: pick tier → load configs → analyze → transform → verify. |
| `CHANGELOG.md` | v1.0.0 release contents (what was added, what was deferred). |
| `CONTRIBUTING.md` | PR process + style guide (YAML/Markdown/naming). |

---

## 3. Repository layout (actual)

```
Infantalizer/
├── README.md                          # Public entry
├── CHANGELOG.md                       # v1.0.0 release log
├── CONTRIBUTING.md                    # PR + style guide
├── LICENSE                            # MIT
├── .gitignore
├── ISSUE_TEMPLATE/
│   └── new_work_mapping.md            # Issue template for new work-mapping requests
│
├── config/                            # The "configuration over code" layer
│   ├── age_profiles/                  # Per-tier developmental configs (YAML)
│   │   ├── tier_1_preschool.yaml          # ages 3-5  — full transform, max safety
│   │   ├── tier_2_early_elementary.yaml   # ages 6-8  — contest paradigm
│   │   ├── tier_3_middle_elementary.yaml  # ages 9-11 — TRANSITION tier
│   │   └── tier_5_young_adult.yaml        # ages 15-17 — minimal transform
│   ├── transformation_rules/
│   │   ├── thematic.yaml              # Violence/death/conflict/agency/heroism by tier
│   │   └── character.yaml             # Archetype mappings + heroism translation
│   └── concept_mapping/
│       ├── universal_mappings.yaml    # Cross-work concept translations (death, evil, war…)
│       └── templates/
│           └── tolkien_mapping.yaml   # LOTR-specific character/concept overrides
│
├── prompts/                           # The runtime workflow (Markdown prompts)
│   ├── analysis/
│   │   └── chapter_analysis.md        # v2.0 anti-hallucination protocol (Phases 0–4)
│   ├── transformation/
│   │   ├── tier_1_transform.md        # Preschool adaptation rules + example
│   │   └── tier_3_transform.md        # Transition-tier adaptation rules + example
│   └── verification/
│       └── safety_check.md            # Post-generation check for Tier 1–2 (6 sections)
│
├── templates/
│   └── work_mapping_template.yaml     # Blank scaffold for new literary works
│
├── docs/
│   ├── SPEC.md                        # v1.0 condensed spec (canonical)
│   ├── guides/QUICK_START.md
│   ├── design_decisions/              # ADR-style records
│   │   ├── 001-five-tier-system.md    # Why 5 tiers, not 3 or 7
│   │   ├── 003-agency-externalization.md  # The foundational T1–2 rule
│   │   ├── 006-adversarial-task-review.md # 68% scope cut via adversarial debate
│   │   └── README.md
│   └── conversation_logs/             # Development discussion archives
│       ├── 02-v2-protocol-development.md
│       ├── 03-modularization-planning.md
│       └── README.md
│
└── .dev/releases/current/0.1/         # Vendored v0.1 release archive (see §8)
    ├── README.md
    ├── SPEC.md                        # Older 314-line spec (PRE-v1.0)
    ├── CHANGELOG.md
    └── creative-writing-skills/       # Vendored fork of haowjy/creative-writing-skills
```

---

## 4. Core mental model

The framework is a three-stage pipeline. Every tier-specific behavior is configured, not coded:

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
    │   forbidden-word scan, agency externalization, emotional safety,
    │   safe-home schema, nightmare prevention, linguistic compliance
    ▼
ADAPTED CHAPTER + transformation log + confidence report
```

**Config cascade (most-specific wins):** universal_mappings.yaml → work-specific mapping (e.g. tolkien_mapping.yaml) → age_profile rules → transformation_rules.

---

## 5. Tier system at a glance

| Tier | Ages | File | Piaget stage | Paradigm | Headline rule |
|------|------|------|--------------|----------|---------------|
| 1 | 3–5 | `tier_1_preschool.yaml` | Preoperational | Full transform, max safety | Violence→cleanup, death→"new adventure", agency externalization MANDATORY |
| 2 | 6–8 | `tier_2_early_elementary.yaml` | Early Concrete | **Contest paradigm** | Violence→competition, death→"passed away", misunderstanding as conflict |
| 3 | 9–11 | `tier_3_middle_elementary.yaml` | Concrete | **TRANSITION** — complexity unlocked | "Died" acceptable, moral ambiguity OK, agency externalization OPTIONAL |
| 4 | 12–14 | *(deferred — interpolate 3+5)* | Early Formal | Near-adult | Tragedy permitted, full villain complexity |
| 5 | 15–17 | `tier_5_young_adult.yaml` | Formal | Minimal transform | Preserve author intent; accessibility, not sanitization |

**Tier 3 is the load-bearing inflection point.** Tiers 1–2 protect from complexity; Tier 3+ scaffolds it. See `docs/design_decisions/001-five-tier-system.md`.

**Agency Externalization** is the framework's signature rule (Tiers 1–2): negative outcomes are *never* attributed to innate malice — always to a temporary state (grumpy, tired) or accident. See `docs/design_decisions/003-agency-externalization.md`.

---

## 6. File-by-file capability map

### 6.1 `config/age_profiles/*.yaml` — tier definitions
Each profile carries: `profile` metadata, `developmental_basis` (Piaget + Kohlberg), `thresholds` (violence/emotional/moral/narrative), `linguistic` rules (vocabulary, sentence structure, chapter length), `transformation_rules` (mode per rule type), `safety` constraints.

- **tier_1** — forbidden vocab list, ≤12-word sentences, ≤800-word chapters, positive resolution required.
- **tier_2** — contest vocabulary added (team, challenge), ≤15-word sentences, mild cliffhangers allowed.
- **tier_3** — `requires_clear_good_bad: false`, parallel plotlines + flashbacks permitted, ≤20-word sentences.
- **tier_5** — `agency_externalization: forbidden` (patronizing), preserves authorial voice, footnotes for archaic language.

### 6.2 `config/transformation_rules/`
- **thematic.yaml** — per-tier translations for violence, conflict, agency, death-handling, villain-motivation, heroism. The "translation table" core of the engine.
- **character.yaml** — archetype system (protagonist/mentor/antagonist/companion) + `heroism_translation` subroutine + special handling for hard cases (Gollum, Denethor).

### 6.3 `config/concept_mapping/`
- **universal_mappings.yaml** — abstract concepts (death, evil, war, despair, injury, betrayal, burden, supernatural_terror, martial_heroism) translated per tier. Work-agnostic.
- **templates/tolkien_mapping.yaml** — per-character tier-N archetypes and per-concept overrides for LOTR. Example template for future work-specific mappings.

### 6.4 `prompts/`
- **analysis/chapter_analysis.md** — 4-phase source-analysis prompt. Produces structured YAML output with confidence tags. Aborts on NO ACCESS.
- **transformation/tier_1_transform.md** — 5 mandatory rules + linguistic constraints + safety checklist + worked example.
- **transformation/tier_3_transform.md** — transition-tier guidance; lists what becomes permitted vs. still forbidden.
- **verification/safety_check.md** — 6-section post-gen verification (forbidden words, agency, emotional safety, safe-home schema, nightmare prevention, linguistic compliance). Mandatory for T1–2.

### 6.5 `templates/`
- **work_mapping_template.yaml** — blank scaffold: `work_metadata`, `characters` (with tier_N subfields), `concepts`, `key_scenes`, `master_translation_table`. Starting point for adapting any new literary work.

---

## 7. Workflow (how to use the framework)

1. **Pick tier** → load `config/age_profiles/tier_N_*.yaml`.
2. **Load engine rules** → `config/transformation_rules/{thematic,character}.yaml`.
3. **Load concept maps** → `universal_mappings.yaml` + work-specific `templates/<work>_mapping.yaml` (if exists).
4. **Analyze source chapter** with `prompts/analysis/chapter_analysis.md`. Produces transformation flags + confidence report.
5. **Transform** with `prompts/transformation/tier_N_transform.md` applied to the analysis output.
6. **Verify** (Tier 1–2 mandatory; Tier 3+ recommended) with `prompts/verification/safety_check.md`.
7. **Emit** adapted chapter + transformation log + confidence tags.

---

## 8. The `.dev/releases/current/0.1/` archive — important caveat

This directory contains an **archived pre-v1.0 release** and a **vendored third-party repository**. It is not part of the shipping v1.0 framework:

| Path | What it is | Why it matters |
|------|-----------|----------------|
| `.dev/releases/current/0.1/SPEC.md` (314 lines) | **Older v0.1 spec** — fuller Part I–VII structure | **Read this for design rationale**, but the canonical spec is `docs/SPEC.md` (131 lines, v1.0 condensed). Do not cite v0.1 spec sections as current. |
| `.dev/releases/current/0.1/README.md` | v0.1 README | References aspirational dirs (`examples/`, `tests/`, `docs/guides/ADDING_NEW_WORKS.md`) that **do not exist** in the v1.0 tree. |
| `.dev/releases/current/0.1/CHANGELOG.md` | v0.1 changelog | Superseded by root `CHANGELOG.md`. |
| `.dev/releases/current/0.1/creative-writing-skills/` | **Full vendored clone** of `haowjy/creative-writing-skills` (a Claude Code plugin — fork-donor candidate surfaced by the prior `/sc:recommend --plugin` run) | Includes its own `.git/` directory (nested repo). Contains: `cw/skills/` (16 skills), `cw/agents/` (12 agents), `.claude/commands/`, scripts, docs. **Not authored by this project** — see its own `LICENSE`. |

**Cross-reference rule:** when a doc in `.dev/releases/current/0.1/` disagrees with `docs/` or root, the **root / `docs/` version wins** for v1.0.

---

## 9. Gaps and aspirational structure

These are documented in the README/spec but **not present** in the working tree:

- `examples/` — referenced in README; would hold completed adaptations.
- `tests/` — referenced in spec; would hold validation tests.
- `config/linguistic/` — referenced in spec §VI; consolidated into age profiles in v1.0 (see CHANGELOG design decision).
- `docs/guides/ADDING_NEW_WORKS.md` — referenced in v0.1 README; not yet written. Use `CONTRIBUTING.md` + `templates/work_mapping_template.yaml` instead.
- **Tier 4 profile** (`tier_4_*.yaml`) — intentionally **deferred**. Per `docs/design_decisions/001-five-tier-system.md` and CHANGELOG: "interpolate from Tiers 3 and 5."
- `prompts/transformation/tier_2_transform.md`, `tier_5_transform.md` — only T1 and T3 prompts shipped (pattern established; higher tiers need less). See `docs/design_decisions/006-adversarial-task-review.md` for the 68% scope-cut rationale.

---

## 10. Key design decisions (ADR index)

| ADR | Topic | Takeaway |
|-----|-------|----------|
| `001-five-tier-system.md` | Tier boundaries | 5 tiers grounded in Piaget/Kohlberg; Tier 3 is the natural inflection; Tier 4 interpolable. |
| `003-agency-externalization.md` | The signature rule | MANDATORY T1–2, OPTIONAL T3, FORBIDDEN T4–5 (becomes patronizing). |
| `006-adversarial-task-review.md` | Scope discipline | Adversarial debate cut initial task list from 22 → 7 items (68%). Established that this is a prompt framework, not software. |

Conversation logs in `docs/conversation_logs/` preserve the development discussion that produced these decisions.

---

## 11. Conventions

- **YAML:** 2-space indent, comments for complex sections.
- **Markdown:** ATX headers (`#`), fenced code blocks.
- **Naming:** `lowercase_with_underscores.yaml` / `.md`.
- **Tier references in prose:** `Tier 1`, `Tier 3`, etc. (capitalized).
- **Confidence tags:** `CERTAIN` / `PROBABLE` / `UNCERTAIN` — always uppercase in output.

---

## 12. Index freshness

This index was generated from a **single full-tree read** of the working directory at HEAD (initial commit not yet made; all files untracked per `git status`). If you add Tiers, prompts, or work-mappings, or sync a newer `.dev/releases/current/` archive, re-run `/sc:index`.
