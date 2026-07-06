# Infantalizer / Literary Adaptation Framework (LAF) — Definitive Analysis

> **Report 1 of 2.** Companion to `CREATIVE_WRITING_SKILLS_ANALYSIS.md`. Both reports share the same category structure so a brainstorming agent can cross-reference them.
>
> **Source basis:** project tree under `/config/workspace/Infantalizer/` (excluding `.dev/`) analyzed against the v0.1 specification at `.dev/releases/current/0.1/SPEC.md`. Index at `docs/INDEX.md` was used as a structural primer and cross-checked against source files.
>
> **Generated:** 2026-07-03.

---

## 0. TL;DR

Infantalizer is the **Literary Adaptation Framework (LAF)** — a configuration-driven, **non-software** system for transforming mature literary works into age-appropriate versions across five developmental tiers (ages 3–17). Its thesis: *developmental psychology (Piaget, Kohlberg) is expressed as YAML configuration, not code*. The "engine" is a chain of Markdown prompts executed by an LLM (Claude Code). It ships **no agents, no orchestrator, no runtime, no knowledge base, and no critique loop** — only static configs, prompts, and templates. Its center of gravity is a single transformation rule, *Agency Externalization*, and a single epistemic discipline, the *v2.0 Pragmatic Verification Protocol*.

The project's v1.0 release shipped a usable-but-minimal corpus (4 of 5 tiers, 2 of 5 transform prompts). The v0.1 spec is more architecturally complete than the v1.0 condensed spec — it describes subsystems (linguistic config files, examples, tests) that v1.0 cut or consolidated. The project is **conceptually rich and operationally sparse**: a strong domain theory packaged as a thin artifact.

---

## 1. Intent

### 1.1 What it is

A framework that takes a **source literary work** (e.g., Tolkien's *The Return of the King*) and produces **age-tiered adaptations** preserving narrative integrity while conforming to developmental-psychology constraints. The unit of work is one chapter.

### 1.2 What problem it solves

Children's literary adaptation is normally a hand-craft performed by a skilled human per work per age band. LAF abstracts the *age-invariant transformation logic* out of any specific work and parameterizes it by tier. The same engine that turns orcs into "noisy grumps" for a 4-year-old preserves Denethor's despair for a 15-year-old.

### 1.3 Origin story (provenance)

Evolved from a concrete project — *"The Happiness Project"* — a preschool adaptation of *The Return of the King*. The generalization step extracted the age-invariant transformation logic, parameterized by tier, and produced the modular system. (Source: README §Development History, CHANGELOG.)

### 1.4 Core innovation (claimed)

> "The framework treats developmental psychology as configuration, not code." — SPEC Executive Summary

The same conceptual transform engine applies different rule sets based on the target age profile. There is exactly one parameterization axis: **age tier**.

### 1.5 What it is NOT

- Not software (no executable code, no CLI, no runtime).
- Not a knowledge base (no persistent state across chapters, no learning loop).
- Not a critique framework (no reviewer agents, no adversarial debate).
- Not a project-management tool (no workflow beyond a 7-step manual procedure in QUICK_START).

---

## 2. Mental Model

### 2.1 The pipeline (3 stages, linear)

```
SOURCE TEXT → [analysis prompt] → analysis object (YAML, confidence-tagged)
                                       │
                                       ▼
                                [transform prompt] ← age profile + rules + concept maps
                                       │
                                       ▼
                                  adapted draft
                                       │
                                       ▼
                              [safety-check prompt] (Tier 1–2 mandatory)
                                       │
                                       ▼
                          adapted chapter + transformation log + confidence report
```

This is a **single-pass, linear, stateless pipeline**. Each chapter is processed independently. There is no cross-chapter memory, no iteration loop, no agent coordination.

### 2.2 The config cascade (most-specific wins)

```
config/concept_mapping/universal_mappings.yaml   ← work-agnostic defaults
                          ↓ overlaid by
config/concept_mapping/templates/<work>.yaml     ← work-specific overrides
                          ↓ overlaid by
config/age_profiles/tier_N.yaml                  ← tier-specific thresholds + linguistic rules
                          ↓ overlaid by
config/transformation_rules/{thematic,character}.yaml  ← engine rules
```

### 2.3 The five-tier axis

The system has exactly **one parameterization axis**: tier. Every behavior — vocabulary ceiling, permitted emotions, heroism mode, agency-externalization mode, sentence length, chapter length, parallel-plotline permission — is a function of tier.

| Tier | Ages | Paradigm | The defining shift |
|------|------|----------|--------------------|
| 1 | 3–5 | Full transform / max safety | Violence→cleanup, death→"new adventure" |
| 2 | 6–8 | Contest paradigm | Violence→competition, "passed away" |
| 3 | 9–11 | **TRANSITION** — complexity unlocked | "Died" acceptable, moral ambiguity OK |
| 4 | 12–14 | Near-adult | *(deferred — interpolate 3+5)* |
| 5 | 15–17 | Minimal transform / preserve author intent | Agency externalization FORBIDDEN |

Tier 3 is the load-bearing inflection point. Tiers 1–2 *protect from* complexity; Tier 3+ *scaffolds* it.

---

## 3. Architecture

### 3.1 Module dependency graph (from SPEC §1.2)

```
source_analysis (v2.0 protocol)
       │
       ▼
age_profiles ◄──────────────────────┐
       │                            │
       ├───────────┬────────────────┤
       ▼           ▼                ▼
transformation  character_      concept_
_rules          mapping         mapping
       │           │                │
       └───────────┴────────────────┘
                   │
                   ▼
            linguistic_calibration
                   │
                   ▼
            output_generation
                   │
                   ▼
            verification_check
```

### 3.2 The five transformation categories

| Category | What it does |
|----------|--------------|
| **Structural** | Linearization, consolidation, pacing |
| **Thematic** | Violence→X, Death→Y, Conflict→Z |
| **Character** | Archetype map, motivation, complexity |
| **Emotional** | Calibration, resolution, safety rails |
| **Linguistic** | Vocabulary, sentence structure, chapter length |

### 3.3 Component inventory (actual, v1.0)

**Configs (8 files):**
- `config/age_profiles/` — tier_1, tier_2, tier_3, tier_5 (tier_4 deferred).
- `config/transformation_rules/{thematic,character}.yaml`.
- `config/concept_mapping/{universal_mappings.yaml, templates/tolkien_mapping.yaml}`.

**Prompts (4 files):**
- `prompts/analysis/chapter_analysis.md` — 4-phase source analysis.
- `prompts/transformation/{tier_1,tier_3}_transform.md` — only T1 and T3 shipped.
- `prompts/verification/safety_check.md` — post-gen verification (T1–2).

**Templates (1 file):**
- `templates/work_mapping_template.yaml` — blank scaffold for new works.

**Docs:** README, CHANGELOG, CONTRIBUTING, LICENSE, SPEC (v1.0 condensed at 131 lines), QUICK_START, 3 design-decision records, 2 conversation logs.

### 3.4 Architectural style

**Configuration-over-code with prompt-as-engine.** The configs are declarative data; the "engine" is an LLM reading the configs and a transformation prompt. There is no algorithmic code anywhere in the project.

---

## 4. Components — what, why, how

### 4.1 `config/age_profiles/tier_N_*.yaml`

**What:** Per-tier developmental configuration. Each file carries 6 sections: `profile`, `developmental_basis` (Piaget stage + Kohlberg stage), `thresholds` (violence / emotional_complexity / moral_ambiguity / narrative_complexity), `linguistic` (vocabulary, sentence structure, chapter structure), `transformation_rules` (mode per rule type), `safety`.

**Why:** The single parameterization axis. Swapping tier_N for tier_M changes every behavior without touching engine logic.

**How (read order):** caller loads `profile` for orientation → `thresholds` to know what's permitted → `transformation_rules` for the active mode → `linguistic` for output constraints → `safety` for verification gates.

**Notable design:** each tier has a `KEY PARADIGM` comment naming its gestalt (e.g., Tier 2 = "contest paradigm", Tier 3 = "transition tier"). Tier 5 explicitly inverts Tier 1's signature rule (`agency_externalization: forbidden` — patronizing at that age).

### 4.2 `config/transformation_rules/thematic.yaml`

**What:** The translation table core. Per-tier transforms for `violence_transformation`, `conflict_transformation`, `agency_externalization`, `death_handling`, `villain_motivation`, `heroism_definition`. Six top-level categories × five tiers.

**Why:** This is where the "engine" lives. Each cell is a `(source concept, tier) → target concept` mapping. Example: `(battle, tier_1) → cooperative_activity → "Big Tidy-Up"`.

**How:** Loaded wholesale as engine reference; the transform prompt cross-references against this when adapting each source element.

**Key cell — Agency Externalization (the signature rule):**
> "Badness is always a STATE or ACCIDENT, never innate."

- Tier 1–2: MANDATORY.
- Tier 3: OPTIONAL.
- Tier 4–5: FORBIDDEN (patronizing).

### 4.3 `config/transformation_rules/character.yaml`

**What:** Archetype system + `heroism_translation` subroutine + `special_handling` for hard cases.

**Why:** Thematic rules handle events; character rules handle *who does them and how*. Distinct file because archetypes compose differently than events.

**How:** Maps complex characters to age-appropriate archetypes per tier. The `heroism_translation` block is the most algorithmic thing in the project — a 3-step subroutine: IDENTIFY core positive intent → LOOKUP tier-appropriate expression → TRANSLATE preserving intent.

**`special_handling`** carries pre-computed answers for hard cases (Gollum, Denethor) where naive rules would fail. This is project's only piece of work-specific knowledge that leaked into the universal layer.

### 4.4 `config/concept_mapping/universal_mappings.yaml`

**What:** Cross-work concept translations for abstract concepts (death, evil, war, despair, injury, betrayal, burden, supernatural_terror, martial_heroism). Work-agnostic.

**Why:** Common literary concepts have tier-stable transformation patterns. Universal mappings capture the default so work-specific mappings only override exceptions.

**How:** Each concept has `tier_1` / `tier_2` / `tier_3` / `tier_4_5` keys with `{translation, framing/agency/cause}` subfields. The `tier_4_5` value is almost always `[preserve]`.

### 4.5 `config/concept_mapping/templates/tolkien_mapping.yaml`

**What:** Per-character tier-N archetypes and per-concept overrides for LOTR. Includes work_metadata (key_challenges), per-character overrides (frodo, sam, aragorn, gandalf, sauron, gollum, eowyn, denethor), per-concept overrides (the_one_ring, mordor, mount_doom, nazgul, army_of_dead, …), and key_scenes.

**Why:** The "most valuable contribution" per CONTRIBUTING.md — extending the framework to a new work is mostly filling in this template.

**How:** Overlays `universal_mappings.yaml`. Most specific wins. The template at `templates/work_mapping_template.yaml` is the canonical blank version.

### 4.6 `prompts/analysis/chapter_analysis.md`

**What:** 4-phase source-analysis prompt implementing the **Pragmatic Verification Protocol v2.0**.

**Why:** Without disciplined source analysis, the transform engine hallucinates. This prompt forces the LLM to declare its access level, verify essentials, and tag every claim with confidence.

**How (the 4 phases):**
- **Phase 0 — Source Declaration:** FULL / PARTIAL / MEMORY-BASED / NO ACCESS. NO ACCESS → ABORT. MEMORY-BASED → all output requires UNCERTAIN tags.
- **Phase 1 — Essential Verification:** title, chapter number, opening/closing sentences (with confidence).
- **Phase 2 — Dual-Pass Documentation:** Pass 1 = structure+events. Pass 2 = summary.
- **Phase 3 — Transformation Flags:** violence / death / emotional / abstract severity.
- **Phase 4 — Consistency Check + Confidence Tags.**

**Output:** YAML with `metadata`, `transformation_flags`, `uncertainties`.

### 4.7 `prompts/transformation/tier_N_transform.md`

**What:** Tier-specific generation prompt. Only Tier 1 and Tier 3 shipped.

**Why:** Tier 1 and Tier 3 are the two genuinely distinct philosophies (full-transform vs. transition). Tiers 2/4/5 are interpolations — pattern is established, omitted by design (see design decision 006).

**How:** Each prompt lists mandatory rules, linguistic constraints, safety checklist, and a worked example. The Tier 1 example: "The orcs attacked. Many soldiers fell." → "The noisy grumbles made a big mess... Many helpers got very tired."

### 4.8 `prompts/verification/safety_check.md`

**What:** 6-section post-generation check, mandatory for Tier 1–2.

**Why:** Catching LLM drift on safety-critical output (children's content) requires an explicit verification pass.

**How (the 6 sections):** Forbidden Content Scan, Agency Externalization Check, Emotional Safety, Safe Home Schema, Nightmare Prevention, Linguistic Compliance. Each section has its own PASS/FAIL rubric. Automatic failure triggers listed at the bottom.

### 4.9 `templates/work_mapping_template.yaml`

**What:** Blank scaffold with five sections: `work_metadata`, `characters` (with tier_1/tier_3/tier_4_5 subfields per character), `concepts`, `key_scenes`, `master_translation_table`.

**Why:** The framework's extension surface. Per CONTRIBUTING.md, copying this template is step 1 of adding any new work.

**How:** Fill in work-specific overrides; place in `config/concept_mapping/templates/`; test with one chapter at Tier 1; submit PR.

---

## 5. Workflows

### 5.1 The 7-step manual workflow (from QUICK_START)

1. Pick tier.
2. Load `config/age_profiles/tier_N.yaml`.
3. Load `config/transformation_rules/{thematic,character}.yaml`.
4. Load `config/concept_mapping/{universal,work-specific}.yaml`.
5. Analyze source chapter with `prompts/analysis/chapter_analysis.md`.
6. Transform with `prompts/transformation/tier_N_transform.md`.
7. Verify (T1–2 mandatory, T3+ recommended) with `prompts/verification/safety_check.md`.

### 5.2 Workflow characteristics

- **Manual:** every step is initiated by a human.
- **Linear:** no iteration loop, no draft→critique→revise cycle.
- **Stateless:** no cross-chapter memory. Each chapter is processed in isolation.
- **Single-agent:** no orchestration. One LLM session per step.
- **No verification loop:** safety_check produces PASS/FAIL but there is no prescribed re-transform path on FAIL.

### 5.3 Where the workflow breaks

- On FAIL in step 7, the framework says "REVISION REQUIRED" but provides no revision prompt, no critique pass, no automated path back to step 6. Operator must hand-drive the revision.
- Across chapters, character state (e.g., "Gandalf died in chapter X") is not tracked. Operator must remember to apply canon in subsequent chapter_analysis runs.

---

## 6. Knowledge & State

### 6.1 What persists

- **Per-work knowledge:** `config/concept_mapping/templates/<work>.yaml` — durable character/concept/scene overrides.
- **Per-tier knowledge:** `config/age_profiles/tier_N.yaml` — durable tier configuration.
- **Universal knowledge:** `config/concept_mapping/universal_mappings.yaml` + `config/transformation_rules/*.yaml`.

### 6.2 What does NOT persist

- **Per-chapter state.** No character state file, no timeline, no canon log. Each chapter analysis is from-scratch.
- **Cross-chapter memory.** No "what happened last chapter" context.
- **Style/voice reference.** No prose samples, no voice files.
- **Issues/tracking.** No persistent log of what transformations were applied, what failed verification, what was revised.
- **Decision history.** ADRs capture system-level decisions; no project-level decision log per adaptation.

### 6.3 Confidence / uncertainty model

The v2.0 protocol tags every analytical claim: `CERTAIN` (directly quoted), `PROBABLE` (multiple observations support), `UNCERTAIN` (inferred/reconstructed). The confidence propagates from analysis output through transformation. **This is the project's strongest idea** — it is an explicit, layered uncertainty model that refuses false certainty.

---

## 7. Conventions & Standards

### 7.1 File conventions

- YAML: 2-space indent, comments for complex sections.
- Markdown: ATX headers, fenced code blocks.
- Naming: `lowercase_with_underscores.yaml|.md`.

### 7.2 Output conventions

- Confidence tags uppercase: `CERTAIN` / `PROBABLE` / `UNCERTAIN`.
- Tier references capitalized: `Tier 1`, `Tier 3`.

### 7.3 Process conventions

- PRs require testing "with one chapter at Tier 1" before submission (CONTRIBUTING.md).
- New works use `templates/work_mapping_template.yaml` as starting point.

---

## 8. Gaps & Open Questions

### 8.1 Documented gaps (intentional cuts)

| Gap | Reason | Source |
|-----|--------|--------|
| Tier 4 profile (`tier_4_*.yaml`) | Interpolate from 3+5 | CHANGELOG; ADR 001 |
| T2/T4/T5 transform prompts | Pattern established at T1+T3; higher tiers need less | ADR 006 |
| `config/linguistic/` (separate dir) | Consolidated into age profiles in v1.0 | CHANGELOG |
| `examples/` | Referenced in README/spec; not yet created | README |
| `tests/` | Referenced in spec; not yet created | SPEC §VI |
| `docs/guides/ADDING_NEW_WORKS.md` | Referenced in v0.1 README; not written | v0.1 README |

### 8.2 Structural gaps (opportunities)

These are **not** documented as gaps but are missing relative to the project's stated ambitions:

- **No state/continuity layer.** Adapting a novel chapter-by-chapter without canon tracking guarantees drift. The Tolkien mapping says "Gandalf death_resurrection: OMIT" for Tier 1, but nothing ensures that decision persists across chapters 5, 12, 30.
- **No critique or adversarial pass.** safety_check verifies forbidden-word compliance but does not critique *adaptation quality*. Did the T1 transform preserve emotional resonance? Did the T3 transform earn its weight-not-gore? No prompt asks.
- **No revision loop.** safety_check produces FAIL but there is no prescribed path back.
- **No examples.** The README says "examples/" but no worked adaptation exists to imitate.
- **No automation.** Every step is manual; no script, no CLI, no orchestration.

### 8.3 Open questions for the brainstorming agent

1. **Continuity:** how should cross-chapter canon be tracked? (CWS has an answer — see Report 2.)
2. **Quality assurance:** how should adaptation quality (not just safety) be verified? (CWS has critic + reader-sim — see Report 2.)
3. **Iteration:** what is the revision loop on FAIL? (CWS has writer→critic→writer loop — see Report 2.)
4. **Knowledge persistence:** where does per-work, per-chapter state live?
5. **Multi-tier coordination:** should one source chapter produce all 5 tier outputs in a coordinated way, or remain 5 independent runs?

---

## 9. Design-Decision Ledger

| ADR | Topic | Decision | Rationale |
|-----|-------|----------|-----------|
| 001 | Five-tier system | 5 tiers grounded in Piaget/Kohlberg; Tier 4 interpolable | Neither 3 nor 7+ fit developmental reality |
| 003 | Agency externalization | MANDATORY T1–2, OPTIONAL T3, FORBIDDEN T4–5 | Protects developing egocentric minds; patronizing once perspective-taking develops |
| 006 | Adversarial task review | Cut 22→7 items (68%) | Established "this is a prompt framework, not software" |

The adversarial-review ADR (006) is the load-bearing scope decision. It explicitly rejected Python/CLI stubs as "wrong abstraction." This is the most-likely-to-be-revisited decision if the project adopts CWS's plugin architecture.

---

## 10. Strengths, Weaknesses, Posture

### 10.1 Strengths

- **Domain rigor.** Developmental-psychology grounding is real and well-cited (Piaget, Kohlberg). Tier boundaries are defensible.
- **Conceptual clarity.** The config-cascade + single-axis (tier) model is unusually clean.
- **Uncertainty discipline.** The v2.0 protocol's CERTAIN/PROBABLE/UNCERTAIN tagging is best-in-class for prompt-based work.
- **Signature rule.** Agency Externalization is a genuinely novel, well-reasoned transformation primitive.
- **Scope discipline.** ADR 006's 68% scope cut kept the project shippable.

### 10.2 Weaknesses

- **Operationally sparse.** No agents, no orchestration, no memory, no critique loop. The "engine" is entirely in the LLM's head per invocation.
- **Stateless.** Adapting a 30-chapter book chapter-by-chapter without continuity tracking is brittle.
- **No quality verification.** safety_check verifies rule compliance, not adaptation quality.
- **Single-axis.** Every behavior is a function of tier alone. No axis for source genre, audience background, or adaptation intent.
- **Incomplete corpus.** 4 of 5 tiers, 2 of 5 prompts, 1 of N work-mappings shipped.

### 10.3 Posture

A **domain theory** with a **thin artifact**. The domain theory (developmental psychology → transformation rules) is mature and defensible. The artifact (configs + prompts) is minimal and ships no operational machinery. The project is positioned for a researcher or skilled operator to apply manually, not for an unsophisticated user to drive through a workflow.

---

## 11. Bridge to Brainstorming

This project's **domain theory** (Part II–III of the SPEC: tiers, transformation rules, agency externalization, v2.0 protocol) is the valuable intellectual property. Its **operational machinery** is the gap.

The companion report (`CREATIVE_WRITING_SKILLS_ANALYSIS.md`) analyzes a system with the *opposite* posture: rich operational machinery (11 agents, 16 skills, durable kb, critic/editor/reader-sim review loop, style extraction, chronicler) but **no domain theory about adaptation or developmental psychology**.

The brainstorming agent's job is to determine whether to:

**(A) Fork CWS and graft LAF's domain theory into it.** LAF's tiers become configs in CWS's `kb/`. LAF's transformation rules become a new skill. CWS's agents (writer/critic/editor/continuity-checker/chronicler) run unchanged but load LAF rules. Adaptation canon flows into CWS's `kb/canon/`.

**(B) Write a 0.1 spec that incorporates CWS's strategies natively.** Define LAF-native agents (analyst/transformer/verifier/continuity-tracker/critic), a per-work kb structure, a draft→critique→revise loop, and chronicler-based canon persistence — without adopting CWS's plugin packaging.

The category-by-category alignment in §12 below is the data the brainstorming agent needs to choose.

---

## 12. Category Map (cross-reference key)

This is the shared structure both reports use. Each category has an LAF posture (this file) and a CWS posture (the companion file).

| # | Category | LAF posture (this report) |
|---|----------|---------------------------|
| A | **Intent** | Adapt source works for age tiers (§1) |
| B | **Pipeline shape** | Linear, single-pass, stateless (§2.1, §5) |
| C | **Parameterization** | One axis: tier (§2.2) |
| D | **Configs / data** | 4 age_profiles + 2 rule files + 2 concept maps (§3.3, §4) |
| E | **Prompts / engine** | 4 prompts (analysis, 2× transform, safety_check) (§4.6–4.8) |
| F | **Knowledge / state** | Per-work templates only; no chapter state (§6) |
| G | **Verification** | v2.0 confidence tagging + 6-section safety check; no quality critique (§4.6, §4.8, §6.3) |
| H | **Revision loop** | None prescribed (§5.3) |
| I | **Agents / orchestration** | None (§3.4) |
| J | **Conventions** | YAML 2-space; ATX MD; lowercase_with_underscores (§7) |
| K | **Gaps** | No continuity, no quality critique, no examples, no automation (§8) |
| L | **Strengths** | Domain rigor; uncertainty discipline; signature rule (§10.1) |

---

*End of Report 1.*
