# creative-writing-skills (CWS) — Definitive Analysis

> **Report 2 of 2.** Companion to `INFANTALIZER_ANALYSIS.md`. Both reports share the same 12-category structure (cross-reference key at §14).
>
> **Source basis:** vendored clone at `/config/workspace/Infantalizer/.dev/releases/current/0.1/creative-writing-skills/` (originally `haowjy/creative-writing-skills`, Apache 2.0). All 16 skills, 11 agents, 4 slash commands, and the architecture doc were read in full.
>
> **License note:** Apache 2.0 — permits fork + modification with attribution. Compatible with LAF's MIT.
>
> **Generated:** 2026-07-03.

---

## 0. TL;DR

**creative-writing-skills (CWS)** is a Mars-distributed plugin package providing a complete **agent-and-skill orchestration system for long-form fiction writing**. Where LAF (Report 1) is a domain theory with thin artifact, CWS is the inverse: a **rich operational machinery with no domain theory about adaptation or developmental psychology**. Its thesis: a small set of clean cognitive roles (muse/writer/critic/editor/reader-sim/continuity-checker/brainstormer/outliner/character-sim/style-creator/chronicler), backed by deeper craft skills, can carry an author from first idea to polished draft while preserving voice and tracking canon.

CWS's load-bearing innovations are: (1) the **Product Lead (muse) pattern** — one author-facing coordinator that routes work to specialist subagents; (2) a **durable knowledge base (`kb/`)** with explicit canon/wiki/styles/vocab/issues layers; (3) an **adversarial review quartet** (critic for focused craft, editor for holistic priority, reader-sim for felt experience, continuity-checker for canon); (4) **style extraction** (style-creator analyzes prose samples to produce voice reference files); (5) **intentional language discipline** (`llm-writing` catches unchosen LLM defaults without flattening deliberate ambiguity).

The system is designed for a human author writing one novel at a time. It is **not** designed for parameterized adaptation of an existing work into multiple age-tiered versions. But its operational primitives map almost 1:1 onto LAF's gaps.

---

## 1. Intent

### 1.1 What it is

A composable agent + skill package for writing novels, short stories, and serial fiction with AI assistance that preserves author voice, tracks continuity, and improves with use.

### 1.2 What problem it solves

LLMs are bad at long-form fiction for systemic reasons ( documented in `writing-principles/resources/failure-modes.md`): they over-explain, resolve tension too early, drift in voice, lose canon across chapters, and produce prose that "feels AI." CWS addresses each failure mode with a dedicated agent role or skill.

### 1.3 Origin / posture

Mars source package, also distributed as a Claude Code plugin and Claude.ai skill uploads. Apache 2.0. Actively maintained (CI workflows, release pipeline, pre-commit hooks).

### 1.4 Core innovations (claimed)

- **"Compact worker set backed by richer craft skills"** (architecture.md). Not many near-duplicate writer agents; one writer with mode-switching, surrounded by clean cognitive roles.
- **Muse as Product Lead** — single author-facing coordinator that interprets intent, routes work, owns the verdict.
- **Persistent kb as project memory** that grows with the story.
- **Intentional language discipline** as a separate concern from prose craft.

### 1.5 What it is NOT

- Not a domain theory about adaptation or age-appropriateness.
- Not a single-shot generator. Every artifact goes through draft → critique → revision.
- Not stateless. The kb is the project's memory and it grows.
- Not hands-off. Muse coordinates but the author has final say on every decision.

---

## 2. Mental Model

### 2.1 The macro loop (3 phases)

```
                 ┌──────────────── EXPLORE & PLAN ─────────────────┐
                 │  brainstormer · character-sim · outliner        │
                 │  (muse routes; options before commitment)       │
                 └────────────────────┬────────────────────────────┘
                                      │ direction confirmed
                                      ▼
       ┌────────────────────────── DRAFT & REVISE ───────────────────────────┐
       │  muse → writer → critic ─────────────┐                              │
       │                  ↘ editor ───────────┼──→ writer (revised draft)    │
       │                  ↘ reader-sim ───────┤                              │
       │                  ↘ continuity-check ─┘                              │
       └──────────────────────────────┬──────────────────────────────────────┘
                                        │ decisions & facts
                                        ▼
                 ┌──────────────── MAINTAIN KNOWLEDGE ──────────────┐
                 │  chronicler · style-creator                     │
                 │  (kb grows; context for next session)           │
                 └─────────────────────────────────────────────────┘
                                      ▲
                                      │ context for next session
                                      └─────── (feeds back into Explore)
```

### 2.2 The draft loop (the inner cycle)

```
muse → writer → [critic | editor | reader-sim | continuity-checker] → writer → ...
```

- `writer` owns ALL prose production modes (fresh draft, revision, bridge, alternate take, line polish).
- `critic` stays separate because adversarial diagnosis benefits from fresh context.
- `editor` stays separate because holistic editorial priority ≠ focused critique.
- `reader-sim` stays separate because felt-experience ≠ analytical critique.
- `continuity-checker` stays separate when canon search must be broader than critic's context.

### 2.3 Skill vs Agent (the key distinction)

> "Agents are spawned as independent processes (orchestrators, writers, critics). Skills are reference material loaded into agent context (craft knowledge, patterns, conventions)." — AGENTS.md

Skills are *passive knowledge*; agents are *active stances with their own context windows*. One writer agent reads multiple craft skills; the same skill can be loaded into many agents. This separation is foundational.

---

## 3. Architecture

### 3.1 Component shape

```
creative-writing-skills/
├── cw/                          # Claude-plugin distribution
│   ├── agents/                  # 11 agent definitions (.md with YAML frontmatter)
│   ├── skills/                  # 16 skill packages (each = SKILL.md + optional resources/)
│   └── .claude-plugin/          # plugin manifest
├── skills/                      # Mars source (mirrors cw/skills for Mars consumers)
├── agents/                      # Mars source (mirrors cw/agents)
├── .claude/commands/            # 4 slash commands (bs, write, critique, kb)
├── bootstrap/project-setup/     # one-time guided setup
├── docs/                        # architecture, research, workflow HTML
├── scripts/                     # sync_cw_skills.py, create_skill_zips.py, release.sh
└── {mars.toml, meridian.toml}   # Mars package manifests
```

### 3.2 The muse-centered orchestration graph (from architecture.md)

```
                    muse (model: opus)
                       │
       ┌───────────────┼───────────────────┐
       ▼               ▼                   ▼
   [Explore]       [Draft]             [Knowledge]
   brainstormer    writer              chronicler
   character-sim   critic              style-creator
   outliner        editor
                   reader-sim
                   continuity-checker
```

Muse is the only author-facing agent. Everything else is dispatched via the `Agent(...)` tool. Each spawn gets its own context window, model, and skill set.

### 3.3 The artifact flow

```
work/brainstorm ─┐
work/outline ────┼──→ muse ───→ writer ───→ work/drafts ──┐
                                                       ├──→ critic ──┐
                                                       ├──→ editor ──┤
                                                       ├──→ reader-sim┤
                                                       └──→ continuity┤
                                                                       ▼
                                                            work/critique-reports
                                                                       │
                                                            ┌──────────┴───────┐
                                                            ▼                  ▼
                                                          muse              writer
                                                       (synthesis)         (revision)

       style-creator ──→ kb/styles ──→ writer + critic (voice reference)

       chronicler ──→ kb/{characters, world, timeline, canon} (durable facts)
```

### 3.4 Architectural style

**Multi-agent orchestration with skill-augmented prompts.** Skills are loaded on demand ("load only the resource needed for the task") to keep context windows lean. Each agent is a clean cognitive role with a constrained tool set.

---

## 4. Components — what, why, how

### 4.1 AGENTS (11 total)

Every agent has YAML frontmatter declaring `name`, `description`, `model` (opus / sonnet / inherit), `skills` (which skill packages to load), and `tools` (constrained allowlist).

#### 4.1.1 `muse` (model: opus, 16 skills, full toolset)

**What:** The author-facing Product Lead. Interprets intent, coordinates specialists, judges results, speaks back to author.

**Why:** Without a single coordinator, specialist spawns would each interpret the author's intent differently. Muse is the only agent that *must* preserve the author's intent across the entire session.

**How (3 stances):**
- **Preserve Author Intent** — before routing, understand desired reader simulation, emotional target, constraints, taste signals, open uncertainty, failure boundary. Use `/grill-with-docs` to ground in project artifacts.
- **Own the Verdict** — read drafts/reports directly, synthesize conflicts, decide next move (ask / revise / explore / critique / update memory / present).
- **After Work Settles** — dispatch knowledge updates via `/story-memory`. "Do not let provisional brainstorms harden into canon."

**Critical pattern:** `<delegate>` block in the agent file explicitly tells muse how to dispatch — each spawn gets its own context, model, skill set. Stances stay separate to prevent contamination.

#### 4.1.2 `writer` (model: opus, 6 skills)

**What:** Production prose. Owns all 5 modes: fresh draft, revision, bridge, alternate take, line polish.

**Why one writer (not many):** "Keeping one prose worker preserves voice continuity better than splitting fresh drafting, bridges, and revision across separate agents" (architecture.md). The *stance* changes via the prompt; the *agent* stays the same.

**How:** Reads brief + critique notes (when present) + adjacent scenes + style files + canon → writes to specified location → notes mode used and judgment calls.

#### 4.1.3 `critic` (model: sonnet, 4 skills, Read-only tools)

**What:** Deep adversarial craft diagnosis, one focus area at a time.

**Why separate from writer:** "adversarial diagnosis benefits from fresh context" (architecture.md). Same agent writing can't objectively critique its own work.

**Why separate from editor:** critic is *focused* (one dimension); editor is *holistic* (priority across dimensions).

**How:** Reads draft against brief + style files + reader-reward channels. Anchors every finding to a specific location. Severity: critical / significant / minor. "Only flag issues you can tie to a concrete reader cost."

**Focus areas:** voice consistency, pacing, character, continuity (defers to continuity-checker for deep work).

#### 4.1.4 `editor` (model: sonnet, 5 skills, Read-only tools)

**What:** Holistic third-party book-editor pass. Returns an editorial memo.

**Why:** Editorial priority ordering (what to fix first) is a different mode from focused critique. Editor protects "author's intent and reader promise" then names revision order.

**How:** Identifies requested edit level (developmental / line / copyedit / proofreading / holistic). Output structure: overall diagnosis → priority queue → developmental notes → line/voice notes → copy/proof notes → suggested revision order.

**Edit levels (from story-review skill):** editorial review (what kind of revision) → developmental (right shape?) → line edit (does prose move?) → copyedit (is it correct?) → proofreading (what slipped through?). "Each level assumes the levels above it are stable."

#### 4.1.5 `reader-sim` (model: opus, 3 skills)

**What:** Experiential first-time reader response. Reports what it *felt* like to read.

**Why:** "A scene can be technically clean and leave a reader cold" (writing-staffing). Reader-sim catches what critic and editor structurally cannot.

**How:** Reads from beginning to end as a caller-specified persona (genre familiarity, taste, age, knowledge boundary). Tracks 5 reader reward channels: transportation, aesthetic, social simulation, curiosity/prediction, flow. Reports moment-by-moment: leaned in / drifted / held questions / question shifts. Stays in the *felt experience*, does not become a craft critic.

**Critical:** runs AFTER the write/critique loop converges, not before. Running it early wastes the signal.

#### 4.1.6 `continuity-checker` (model: inherit, 4 skills, +Bash)

**What:** Cross-references draft against established canon for contradictions.

**Why separate from critic:** "canon search must be broader than the critic's provided context" (architecture.md). Continuity-checker reads broadly; critic reads the draft.

**How:** Reads draft + canon files + vocab files. Reports every contradiction. Severity classification:
- **breaks canon** — factual contradiction
- **term drift** — canonical-name or meaning conflict
- **suspicious** — might conflict, needs author judgment

Distinguishes hard contradictions (text says Tuesday, timeline says Wednesday) from soft tensions (character seems to know something they might not have learned).

#### 4.1.7 `brainstormer` (model: sonnet)

**What:** Creative option generation for a scoped question. Job is **breadth, not convergence**.

**Why:** Before commitment, authors need multiple angles explored. Brainstormer pushes past the obvious.

**How:** Reads context, pushes past constraints, presents possibilities + tradeoffs. Tags all content `<AI>` (source-tagging convention). Output is a structured report, not a decision.

**Key principle:** "Three perspectives beats five instances of one" (writing-staffing). Fan out on different *angles*.

#### 4.1.8 `outliner` (model: sonnet)

**What:** Sequences confirmed direction into arc/chapter/beat-level outlines.

**Why:** Outlining starts AFTER direction is chosen — brainstormer first, then outliner. The outliner's output feeds the writer.

**How:** Each beat identifies: what happens / what changes (state, relationship, info revealed) / emotional register. Captures: why scene exists for larger story, key beats in emotional-trajectory order, character state in/out, information the reader gains.

#### 4.1.9 `character-sim` (model: sonnet)

**What:** In-character conversation for voice discovery and relationship testing.

**Why:** Discovering a character's voice by writing *about* them is weaker than speaking *as* them. Character-sim enters the character.

**How:** Builds character from evidence: style files (how they talk) + character state (where they are). Speaks first-person from the character's knowledge, NOT the full story's. "When they would be confused, be confused. When they would deflect, deflect. When they would misunderstand, misunderstand."

**Key:** matches speech to age/class/education/stress. "Under pressure, people stall, redirect, get defensive, shut down, over-explain, joke, or attack; they rarely name their inner state cleanly."

#### 4.1.10 `style-creator` (model: opus)

**What:** Analyzes prose samples → produces style reference files in `kb/styles/`.

**Why:** Voice consistency across chapters requires a reference. Without style files, every writer invocation drifts.

**How:** Uses `/creative-writing-craft → resources/style-analysis.md`. Distinguishes specified vs inferred when working without samples.

#### 4.1.11 `chronicler` (implied — referenced in README/architecture/agents dir but not in cw/agents)

**What:** Extracts factual state changes from completed chapters into kb.

**Why:** The kb's canon/timeline/characters/world layers grow chapter-by-chapter. Without extraction, the kb is stale after chapter 1.

**How:** Uses `/story-memory`. Updates kb/{characters, world, timeline, canon}. (Source: architecture.md artifact-flow diagram + README agent table.)

> **Note:** `chronicler.md` appears in `agents/` and `cw/agents/` per the file inventory, but the file is not present at the expected path in `cw/agents/`. It may exist in the `agents/` (Mars source) directory only. The brainstorming agent should verify before depending on it.

### 4.2 SKILLS (16 total)

Skills are passive knowledge loaded into agent context. Each has YAML frontmatter (`name`, `description`, optional flags) followed by directive content. Most reference `resources/` for deeper material.

#### 4.2.1 `writing-principles` (the diagnostic layer)

**What:** Reader-reward model + AI-fiction failure modes.

**Why:** LLMs systematically damage fiction through helpfulness impulses (explain, resolve, clarify, complete). This skill names the failure modes.

**Core model — 5 reader reward channels:**
- **Transportation** — entering the story world. Protected by coherent narrative, consistent POV, sensory grounding.
- **Aesthetic** — sentence-level pleasure. Protected by rhythm/word-choice variety.
- **Social simulation** — modeling characters as minds. Protected by behavior+interiority access, distinct voices.
- **Flow** — challenge-skill fit. Protected by pacing that matches scene work.
- **Curiosity/prediction** — wanting to know what happens. Protected by information gaps, setup/payoff, withheld implications.

**Key principle — Trust the Reader:** "the helpfulness instinct wants to explain, resolve, clarify, complete. In fiction, every one of those impulses can damage the reading experience by doing work the reader wanted to do themselves."

**Sub-skill — Economy:** every element does more than one thing. "What can you leave out and still have the scene work?"

**Punctuation Tells:** flags em-dash overuse as AI-residue.

#### 4.2.2 `creative-writing-craft` (the how-to-write layer)

**What:** Prose technique, scene mechanics, style analysis. References `resources/{prose-writing.md, scene-construction.md, style-analysis.md, genre/}`.

**Why:** Principles diagnose *what's wrong*; craft skills execute *how to write*.

**How:** load-on-demand. Each resource covers one craft dimension. Genre resources (`fantasy.md`, `horror.md`, `litfic.md`, `mystery.md`, `romance.md`, `thriller.md`) cover genre-specific page-level technique.

> **Note:** there is NO `childrens.md` or `ya.md` genre resource. This is a documented gap relevant to LAF's use case.

#### 4.2.3 `creative-writing-modes` (the production-mode layer)

**What:** Five prose execution modes: fresh draft, revision, bridge/connective tissue, alternate take, line polish.

**Why:** "Use the smallest mode that fits the task." Different production needs require different stances from the same writer agent.

**How:** references `resources/prose-modes.md`. Each mode is a section; writer reads only the relevant section per pass.

#### 4.2.4 `creative-writing-muse` (single-agent muse mode)

**What:** A skill (not agent) that lets one conversation act as muse by switching stances. `disable-model-invocation: true` — only user-activated.

**Why:** Claude.ai and other skills-only environments can't spawn agents. This skill gives them muse-mode in one conversation.

**How:** explicitly enumerates which skills to load per stance (Direction / Drafting / Critique / Research / Voice / Memory). Self-prompt before each stance: what is the author's intent / what reader effect / what constraints / what should remain ambiguous / what output / what would be wrong-kind-of-success.

**Key principle — Keep Stances Separate:** "Explore without committing too early. Draft before judging. Critique from the reader's experience. Revise the highest-impact issue. Update memory only for settled facts."

#### 4.2.5 `story-planning` (pre-page decisions)

**What:** Direction, brainstorming capture, outlining, story architecture.

**Resources:** `creative-direction.md`, `brainstorming.md` (+ chapter-planning, character-development, continuity-timeline, worldbuilding sub-resources), `story-architecture.md` (+ arc-design, chapter-and-scene, structural-problems).

**Why:** before pages exist, decisions about *what should happen* are a different mode from writing.

#### 4.2.6 `story-review` (review work after prose exists)

**What:** Five edit levels + adversarial craft critique + reader-sim signal synthesis.

**Resources:** `editorial-review.md`, `developmental-edit.md`, `line-edit.md`, `copyedit.md`, `proofreading.md`, `prose-critique.md` (+ per-area: structure, character, voice, prose, continuity), `reader-sim-signal.md`.

**Key discipline:** "Start big before small unless the caller explicitly asks for a late-stage pass. The edit levels move from structural to surface, and each assumes the levels above it is stable."

#### 4.2.7 `story-memory` (durable story state)

**What:** Knowledge that must survive the current pass: canon facts, context handoffs, vocab/reference, project layout, persistent issues.

**Resources:** `story-context.md` (handoff context), `fact-extraction.md` (durable facts from chapters), `story-reference-writing.md` (wiki/vocab/decisions), `writing-artifacts.md` (where things live), `writing-issues.md` (persistent tracking).

#### 4.2.8 `character-sim` / `reader-sim` (skill versions for skills-only environments)

Mirror the agent behavior but as loadable skills. Character-sim enters a specified character; reader-sim reads as a specified persona.

#### 4.2.9 `writing-staffing` (the dispatch reference)

**What:** Teaches which skills to load for each subagent, which resources to reference, when to fan out.

**Why:** muse needs to know how to compose teams. This skill is the meta-layer.

**Key principles:**
- One writer per scene (voice consistency degrades with multiple writers on adjacent content).
- Critic: fan out with different focus areas simultaneously. "1–2 for low-stakes, 3 for standard chapters, 4–5 for pivotal scenes with duplicated coverage on the critical dimension."
- Editor: name the edit level. Use for priority order across concerns.
- Continuity-checker: "more expensive than a critic with continuity focus — reads broadly. Use the critic for routine checks."
- Brainstormer: fan out on different *angles*, not the same angle.
- Outliner: starts after direction chosen — brainstormer first.
- Reader-sim: "run after the write/critique loop converges, before presenting to the author."

#### 4.2.10 `llm-writing` (intentional language discipline)

**What:** Catches unchosen LLM defaults: filler structure, vague language, polished transitions that smooth away tension, explanation that tells the reader what the scene should make them feel.

**Why:** separate from prose craft. "In fiction, ambiguity, omission, repetition, and broken rhythm remain valid when they create the intended effect."

**4-step process:** Scope (beats) → Ground (source material) → Draft (to disk) → Revise (whole→structure→beats→paragraphs→sentences→words).

**What to Delete (8 anti-patterns):** fill-because-section-exists, labeling-without-explaining, conclusions-without-evidence, uncertainty-behind-confident-language, softening-qualifiers, summary-conclusions, transition-word-connectors, half-clauses.

#### 4.2.11 `shared-dao` (vocabulary discipline)

**What:** Canonical story terms + aliases + ambiguity resolution.

**Why:** "Ambiguous, overloaded, drifting, or misleading terms corrupt drafts early: magic systems get renamed, factions blur together, genre terms mean different things."

**Where vocab lives:** project (`kb/vocab.md`) → domain (`kb/<domain>/vocab.md`) → work notes (`work/...`, promoted when settled).

**Each entry:** canonical name, definition (1–3 sentences), aliases, source.

**Terms to watch:** magic/tech/powers, factions/places/cultures, titles/ranks, relationship labels, character catchphrases, genre terms with project-specific meaning, chapter/arc/POV labels.

#### 4.2.12 `kb-management` (the kb maintenance layer)

**What:** Creating/updating/organizing wiki-style reference pages in `kb/`.

**Layers:** Canon (committed facts), Wiki (synthesized reference), Styles (voice files), Vocab (canonical terms), Issues (cross-chapter problems).

**Conventions:**
- One concept per document.
- Name files by what they describe, not when written.
- Self-contained, scannable, concrete, current.
- Split when > ~200 lines or multi-topic.
- **kb vs work:** finalized knowledge → kb; draft iterations / brainstorms / critique reports → work.

#### 4.2.13 `intent-modeling` (read for outcome, not words)

**What:** Separate what the human said from what they meant. Use conversation context to infer underlying goal.

**Why:** directional corrections usually calibrate a balance ("less X, more Y"), not a permanent ban. Vague requests are rough drafts of real needs.

**Critical:** "When intent and output diverge, scan other artifacts for the same pattern. One misread often repeats."

#### 4.2.14 `grill-with-docs` (adversarial plan interview)

**What:** Challenges a plan relentlessly against documented decisions and sharpens terminology.

**Why:** plans fail on unresolved dependencies and vague terms. Grill-with-docs walks the decision tree branch-by-branch.

**How (6 steps per branch):** state branch + dependency context → ask focused questions with recommended answers → wait → drill into sub-questions → verify against project materials → update documentation immediately when branch resolves.

#### 4.2.15 `creative-research` (web research for fiction)

**What:** Gathers primary sources, reference works, history/lore, wikis, community discussion, domain expertise, place/culture detail.

**Output structure:** usable detail → source notes (type, reliability, confidence) → conflicts (with both sides cited) → contradictions (with story's current assumptions) → gaps.

#### 4.2.16 `project-setup` (one-time kb bootstrap)

**What:** Interviews author about project, collects writing samples, proposes kb structure, creates CLAUDE.md.

**kb complexity tiers:**
- Simple (short story, single POV): `characters/`, `canon/`, `styles/`, root `vocab.md`.
- Medium (novel, few POVs): add `timeline/`.
- Complex (series, large world): add `world/`, `issues/`, domain vocab.

### 4.3 SLASH COMMANDS (4)

User-facing shortcuts mapping to skills:

| Command | Skill | Purpose |
|---------|-------|---------|
| `/bs` | story-planning | Brainstorm ideas with `<AI>` / `<hidden>` source tagging |
| `/write [style]` | creative-writing-modes | Enter prose mode; auto-discovers style files in `kb/styles/` |
| `/critique` | story-review | Adversarial critique; calibrated to draft stage |
| `/kb` | kb-management | Create/update kb pages; only finalized knowledge |

### 4.4 KB STRUCTURE (the durable project layout)

```
my-story/
├── CLAUDE.md           # Project conventions (created by project-setup)
├── story/              # Chapters and manuscript
├── work/               # Current drafting effort
│   ├── outline/
│   ├── drafts/
│   ├── critique-reports/
│   └── brainstorm/
└── kb/                 # Durable knowledge base
    ├── styles/         # Voice reference files
    ├── characters/     # Character state and profiles
    ├── world/          # Locations, lore, systems
    ├── timeline/       # Chronology
    ├── canon/          # Established facts
    ├── vocab.md        # Project-wide terms
    └── issues/         # Tracked writing problems
```

---

## 5. Workflows

### 5.1 The full novel-writing workflow

```
1. /project-setup → CLAUDE.md + kb/ skeleton + initial style files
2. /bs → brainstorm direction (brainstormer, multiple angles)
3. /grill-with-docs → resolve decision tree
4. @outliner → arc/chapter/beat outlines
5. @style-creator → kb/styles/ from samples
6. @writer → fresh draft (work/drafts/)
7. @critic (×N, parallel) → work/critique-reports/ (focused areas)
8. @editor → editorial memo (priority order)
9. @writer → revised draft (revision mode)
10. @continuity-checker → canon pass
11. @reader-sim → felt-experience report
12. @writer → final polish (line-polish mode)
13. @chronicler → kb update (canon, timeline, characters, world)
14. Loop 6–13 per chapter
```

### 5.2 Workflow characteristics

- **Multi-agent:** muse dispatches via `Agent(...)` tool.
- **Iterative:** draft → critique → revise is the inner cycle.
- **Stateful:** kb grows across chapters.
- **Parallel:** critics fan out simultaneously with different focus areas.
- **Reviewer separation:** craft critique / editorial priority / felt experience / canon verification are four distinct modes run by four distinct agents.

### 5.3 Effort scaling (from writing-staffing)

| Stakes | Critic count | Notes |
|--------|--------------|-------|
| Low-stakes | 1–2 | Single focus area OK |
| Standard chapter | 3 | Different focus areas in parallel |
| Pivotal scene | 4–5 | Duplicated coverage on critical dimension |

Knowledge maintenance waits until direction/chapters settle.

---

## 6. Knowledge & State

### 6.1 What persists

- **`kb/canon/`** — hard facts per chapter/arc. Once committed, contradicting breaks reader trust.
- **`kb/characters/<name>.md`** — one file per character: state, profile, arc.
- **`kb/world/`** — locations, lore, systems, factions.
- **`kb/timeline/`** — chronology per arc/period.
- **`kb/styles/`** — voice reference files (writer + critic depend on these).
- **`kb/vocab.md` + `kb/<domain>/vocab.md`** — canonical terms, aliases, sources.
- **`kb/issues/`** — tracked cross-chapter problems (recurring tics, pacing patterns).
- **`work/`** — draft iterations, brainstorm captures, critique reports (provisional, not promoted to kb until settled).
- **`CLAUDE.md`** — project conventions, every agent reads for context.

### 6.2 Knowledge lifecycle

```
work/ (provisional)  ──[decision crystallizes]──►  kb/ (durable)
work/brainstorm      ──[direction chosen]─────►  kb/canon + kb/characters + kb/world
work/drafts          ──[chapter finalized]────►  kb/canon + kb/timeline (via chronicler)
work/critique-reports ──[patterns recur]──────►  kb/issues
```

**Discipline:** "Do not let provisional brainstorms harden into canon" (muse). Chronicler runs only after work settles.

### 6.3 Citation discipline

- Chapter references: `Chapter 3: Scene where X discovers Y`.
- Document references: `magic-system.md`.
- Brainstorm source tagging: `<AI>...</AI>` for AI suggestions, `<hidden>...</hidden>` for author-only (twists), untagged = author stated.

---

## 7. Conventions & Standards

### 7.1 Skill package structure

- Every skill = `SKILL.md` (YAML frontmatter + directive content) + optional `resources/` (deeper material, load-on-demand).
- Self-contained: "no cross-skill dependencies" (AGENTS.md).
- Skills declare `name` + `description`; Claude-native flags like `disable-model-invocation` when needed.

### 7.2 Agent profile structure

- YAML frontmatter: `name`, `description`, `model`, `skills[]`, `tools`.
- Constrained tool allowlists — most reviewers are Read-only.
- Short directive body (some as short as "Use `/skill-name`").

### 7.3 Distribution structure

- Two parallel trees: `skills/` + `agents/` (Mars source) and `cw/skills/` + `cw/agents/` (Claude-plugin distribution).
- `scripts/sync_cw_skills.py` keeps them in sync; CI fails on drift.
- `cw/.claude-plugin/plugin.json` required for marketplace add-from-GitHub.

### 7.4 Process conventions

- One concept per document.
- Files named by what they describe, not when written.
- Split documents > ~200 lines.
- Pre-commit hook validates cw skill sync + plugin manifest.

---

## 8. Gaps & Open Questions

### 8.1 Documented gaps / intentional choices

- **No age-tiered anything.** CWS treats "audience" as a free-form reader-sim persona, not a parameterized axis. There is no developmental-psychology model.
- **No source adaptation mode.** CWS assumes the author is *writing original work*, not adapting an existing work. There is no "source analysis" concept.
- **No genre resources for children's/YA.** The `resources/genre/` dir has fantasy, horror, litfic, mystery, romance, thriller — no `childrens.md` or `ya.md`.
- **No safety-verification layer.** There is no equivalent to LAF's safety_check; CWS trusts the author to set taste boundaries.
- **No confidence/uncertainty tagging.** Where LAF's v2.0 protocol tags every claim CERTAIN/PROBABLE/UNCERTAIN, CWS has no equivalent discipline.

### 8.2 Operational gaps

- **`chronicler.md` presence.** Referenced in README/architecture but the agent file may exist only in `agents/` (Mars source), not `cw/agents/`. The brainstorming agent should verify before depending on it.
- **No automated dispatch.** Muse routes work but the actual `Agent(...)` calls are muse's responsibility, not scripted.

### 8.3 Open questions for the brainstorming agent

1. **Where does LAF's tier system live in CWS's structure?** As a new skill (`/adaptation-tiers`)? As kb/vocab.md? As a config layer above CLAUDE.md?
2. **How should the source-adaptation workflow be modeled?** A new `analyst` agent that runs before brainstormer? A pre-muse phase?
3. **Where do LAF's transformation rules live?** As a new skill `/adaptation-rules` loaded by writer? As kb/styles/ extensions? As a per-tier overlay?
4. **How to integrate LAF's confidence tagging?** Into story-memory's fact-extraction? Into a new `/source-fidelity` skill?
5. **Who runs the safety_check in CWS's agent set?** A new `safety-verifier` agent? A mode of continuity-checker? A critic focus area?
6. **Should the workflow be chapter-driven (LAF) or session-driven (CWS)?** LAF thinks one chapter at a time; CWS thinks one session at a time.
7. **Multi-tier output coordination.** Should one source chapter produce 5 tier outputs in parallel (CWS-style fan-out), or sequentially (LAF's manual model)?

---

## 9. Design-Decision Ledger

CWS does not use ADRs, but its architecture encodes several load-bearing decisions:

| Implicit Decision | Source | Rationale |
|-------------------|--------|-----------|
| **One writer, not many** | architecture.md | Voice continuity > specialization |
| **Muse as Product Lead** | muse.md | Single intent-preserving coordinator |
| **Skills ≠ Agents** | AGENTS.md | Knowledge (passive) vs stance (active) |
| **Compact worker set** | architecture.md | "Not many near-duplicate writer agents" |
| **Reader-sim is a separate agent from critic** | architecture.md | Felt experience ≠ analytical critique |
| **Continuity-checker is a separate agent from critic** | architecture.md | Deep canon search ≠ focused critique |
| **Editor ≠ Critic** | architecture.md | Holistic priority ≠ focused diagnosis |
| **CLAUDE.md as universal context** | project-setup | Every agent reads project conventions |
| **`work/` vs `kb/` split** | kb-management | Provisional vs durable knowledge |
| **Brainstormer is breadth, not convergence** | brainstormer.md | Author decides, not the agent |
| **Outliner starts after brainstormer** | outliner.md | Direction before structure |
| **Source tagging: `<AI>` / `<hidden>` / untagged** | story-planning | Provenance discipline for brainstorm capture |
| **Reader-sim runs AFTER write/critique converges** | writing-staffing | Early running wastes signal |
| **Plugin manifest required even though Claude auto-discovers** | AGENTS.md | Marketplace add-from-GitHub path validates it |

---

## 10. Strengths, Weaknesses, Posture

### 10.1 Strengths

- **Operational maturity.** 11 agents with constrained tool sets, 16 skills with load-on-demand resources, 4 slash commands, CI pipeline, plugin distribution.
- **Clean cognitive roles.** Each agent has one job; the boundaries are well-defended (writer vs critic vs editor vs reader-sim vs continuity-checker).
- **Durable knowledge layer.** The kb/ structure with canon/wiki/styles/vocab/issues is a real memory substrate.
- **Voice consistency via style-creator + style files.** Solves a real LLM failure mode (voice drift across chapters).
- **Intentional language discipline.** `llm-writing` and `writing-principles` explicitly counter LLM prose defaults.
- **Iterative draft→critique→revise loop** is the right shape for fiction production.
- **Source-tagging and citation conventions** make brainstorm captures auditable.
- **Mars packaging** is mature (CI-gated sync, plugin manifests, release pipeline).

### 10.2 Weaknesses

- **No domain theory about adaptation.** CWS cannot, as-is, produce age-tiered versions of a work.
- **No safety verification.** Trust-the-author posture; no equivalent to LAF's safety_check.
- **No source-fidelity discipline.** No confidence tagging, no source-access declaration, no anti-hallucination protocol.
- **No children's/YA genre resources.** The genre library is adult-fiction-shaped.
- **Reader-sim persona is under-specified** for developmental tiers — "age or audience segment when relevant" is the only nod.
- **Reader-sim is expensive** (model: opus) and runs only after convergence — late signal.
- **Continuity-checker reads only what it's given** — scope-limited by what muse passes.

### 10.3 Posture

An **operational machinery** with **no adaptation domain theory**. Where LAF is conceptually rich and operationally sparse, CWS is operationally rich and conceptually thin (about adaptation specifically — it has deep craft knowledge about fiction in general). The two systems are *complementary* more than they are competing.

---

## 11. Bridge to Brainstorming

CWS's operational primitives map onto LAF's gaps almost directly:

| LAF gap (Report 1 §8.2) | CWS primitive that fills it |
|--------------------------|------------------------------|
| No continuity layer | `kb/canon/`, `kb/timeline/`, `kb/characters/`, chronicler agent |
| No quality critique | critic agent (focused), editor agent (holistic), reader-sim (felt) |
| No revision loop | writer → critic → writer inner cycle (architecture.md) |
| No knowledge persistence | kb/ with canon/wiki/styles/vocab/issues layers |
| No automation | muse + Agent(...) dispatch; slash commands |
| No style/voice reference | kb/styles/ + style-creator agent |

And LAF's domain theory maps onto CWS's extension points:

| LAF domain concept | CWS extension point |
|--------------------|---------------------|
| Five-tier system | New skill `/adaptation-tiers` OR kb/vocab.md OR CLAUDE.md section |
| Transformation rules (thematic, character) | New skill `/adaptation-rules` loaded by writer + critic |
| Concept mapping (universal + work-specific) | New `kb/adaptation-mapping/` directory |
| v2.0 Pragmatic Verification Protocol | New skill `/source-fidelity` OR pre-writer `analyst` agent |
| safety_check (6-section) | New `safety-verifier` agent OR continuity-checker mode |
| Agency Externalization rule | New craft principle in writing-principles OR its own skill |
| Work-mapping template | New `templates/` or part of project-setup interview |

The brainstorming agent should weigh:

- **(A) Fork CWS.** Keep its 11 agents + 16 skills intact. Add LAF's domain theory as a new skill set (`/adaptation-tiers`, `/adaptation-rules`, `/source-fidelity`) + new agent (`analyst`, `safety-verifier`) + kb extension (`kb/adaptation-mapping/`). LAF's configs become kb data. Pro: reuses mature machinery. Con: CWS is general-purpose; LAF's adapter concerns may feel grafted-on.

- **(B) Write a 0.1 spec with CWS strategies natively.** Define LAF-native agents (analyst, transformer, verifier, continuity-tracker, critic, editor) and a kb structure, but designed ground-up for parameterized adaptation. Pro: coherent postured for adaptation. Con: rebuilds machinery CWS already has.

The shared 12-category structure (§12 in Report 1, §14 below) is the data needed to choose.

---

## 12. Failure Modes CWS Explicitly Counts

These are the LLM-fiction failure modes CWS is engineered to counter. Any brainstorming output should preserve these countermeasures.

| Failure mode | CWS countermeasure |
|---------------|---------------------|
| Voice drift across chapters | style-creator + kb/styles/ + writer-only-per-scene |
| Helpful over-explanation | writing-principles: Trust the Reader + Economy |
| Em-dash / AI-residue prose | writing-principles: Punctuation Tells |
| Unchosen LLM defaults | llm-writing skill |
| Canon contradictions | continuity-checker agent + kb/canon/ |
| Term drift | shared-dao skill + kb/vocab.md |
| Single-purpose prose | writing-principles: Economy |
| Resolving tension too early | writing-principles: curiosity/prediction channel |
| Telling what scene should make reader feel | llm-writing: "What to Delete" |
| Vague brainstorm capture | source-tagging: `<AI>` / `<hidden>` / untagged |
| Provisional ideas hardening into canon | muse discipline + work/ vs kb/ split |
| Reader-sim signal coming too late | writing-staffing: runs after convergence |
| Critic contaminating drafting | architecture: separate spawns with fresh context |
| Editor muddling priority | architecture: editor distinct from critic |
| Continuity scope too narrow | architecture: continuity-checker distinct from critic |

---

## 13. Cross-Reference: LAF gap → CWS primitive (the integration map)

This is the single most important table for the brainstorming agent. It maps every LAF weakness to the CWS component that addresses it.

| LAF weakness (Report 1 §10.2) | CWS primitive | Integration effort |
|--------------------------------|---------------|---------------------|
| "Operationally sparse — no agents, no orchestration" | muse + 11-agent dispatch | Low: adopt as-is |
| "Stateless — no cross-chapter memory" | kb/{canon, characters, timeline, world} + chronicler | Low: adopt as-is |
| "No quality verification" | critic + editor + reader-sim trio | Low: adopt as-is |
| "No revision loop" | writer → critic → writer inner cycle | Low: adopt as-is |
| "Single-axis — every behavior is f(tier)" | (no equivalent; CWS is multi-axis by design) | **High: LAF innovation must be preserved** |
| "Incomplete corpus" | (orthogonal — CWS doesn't help here) | Out of scope for fork decision |

And the reverse — every CWS gap that LAF fills:

| CWS gap (§10.2) | LAF primitive |
|------------------|---------------|
| "No domain theory about adaptation" | Five-tier system + transformation rules engine |
| "No safety verification" | safety_check.md (6-section) |
| "No source-fidelity discipline" | v2.0 Pragmatic Verification Protocol |
| "No children's/YA genre resources" | Tier 1–5 developmental profiles |
| "Reader-sim persona under-specified for developmental stages" | Piaget/Kohlberg developmental_basis in each tier profile |
| "No source-adaptation workflow" | analysis → transform → verify pipeline |

---

## 14. Category Map (cross-reference key)

Shared 12-category structure. Each category has a CWS posture (this report) and an LAF posture (Report 1).

| # | Category | CWS posture (this report) | LAF posture (Report 1 §) |
|---|----------|---------------------------|--------------------------|
| A | **Intent** | Help author write one original novel (§1) | Adapt source works for age tiers (R1 §1) |
| B | **Pipeline shape** | Iterative draft→critique→revise, stateful (§2.1, §5) | Linear single-pass, stateless (R1 §2.1, §5) |
| C | **Parameterization** | Multi-axis: persona, genre, taste, canon (§2.3) | One axis: tier (R1 §2.2) |
| D | **Configs / data** | kb/{canon,characters,world,timeline,styles,vocab,issues} + CLAUDE.md (§4.4, §6) | 4 age_profiles + 2 rule files + 2 concept maps (R1 §3.3) |
| E | **Prompts / engine** | 16 skills + 11 agents + 4 slash commands (§4.2, §4.1, §4.3) | 4 prompts (R1 §4.6–4.8) |
| F | **Knowledge / state** | Durable kb with lifecycle (work→kb promotion) (§6) | Per-work templates only (R1 §6) |
| G | **Verification** | critic + editor + reader-sim + continuity-checker quartet; no safety check (§4.1.3–4.1.6) | v2.0 confidence tagging + 6-section safety check; no quality critique (R1 §4.6, §4.8) |
| H | **Revision loop** | Inner cycle: writer→critic→writer (§2.2, §5.2) | None prescribed (R1 §5.3) |
| I | **Agents / orchestration** | muse-centered, 11 agents, Agent(...) dispatch (§3.2, §4.1) | None (R1 §3.4) |
| J | **Conventions** | Skill = SKILL.md + resources/; agent = frontmatter + directive; one concept per doc; CLAUDE.md universal (§7) | YAML 2-space; ATX MD; lowercase_with_underscores (R1 §7) |
| K | **Gaps** | No adaptation theory; no safety; no source fidelity; no children's genre (§8) | No continuity; no quality critique; no examples; no automation (R1 §8) |
| L | **Strengths** | Operational maturity; clean roles; durable kb; voice consistency; intentional language discipline (§10.1) | Domain rigor; uncertainty discipline; signature rule (R1 §10.1) |

---

*End of Report 2.*
