# Research Enrichment (deep) — prep-phase design patterns

> Source: deep-research agent via WebFetch + Context7. Tavily unavailable this session
> (`fallback_1: WebFetch/WebSearch`). Findings are design-relevant, citable precedents for the prep-phase
> design. Quality tier: fallback_1 (primary Tavily missing, fell back to direct doc/repo fetches).

## 1. Onboarding / intake — "research autonomously, THEN clarify"

- **CrewAI `planning=True` + AgentPlanner** (docs.crewai.com/concepts/crews): all crew data goes to a
  planner BEFORE any agent works; the plan is appended to each task. Plus a hierarchical `manager_agent`
  that "validates outcomes before proceeding." → *Precedent for a planner→executor two-step + a gate.*
- **BabyAGI create→execute→reprioritize loop** (github.com/yoheinakajima/babyagi): the canonical
  "agent builds its own task list from a goal" loop. → *Justifies "framework emits its own prep roadmap
  from just the novel name."*
- **Spec-kit `/speckit.clarify`** (github.com/github/spec-kit): runs coverage-based clarification BEFORE
  `/speckit.plan`, appends answers to a "Clarifications" section, and explicitly supports a `[skip]`
  semantic so the agent doesn't block on missing input. → *Direct analog for the "question gate": ask
  only what changes the work, after gathering; allow skip.*

## 2. Interactive pause / question gate WITHOUT a runtime

LangGraph's `interrupt()` / `Command(resume=...)` machinery (Context7 /langchain-ai/langgraph) is NOT
portable (it needs a checkpoint runtime), but its **semantics** map cleanly to prompt-only:
- interrupt emits a question value; the caller resumes with an answer that injects as a return value.
- In a no-runtime framework this becomes: **the agent emits a `## Questions for the user` block in its
  output and halts; the user replies in chat; the agent resumes.** No code required.
- **Cursor `.mdc` rules** (cursor.com/docs/context/rules) are the prompt-only gate primitive: YAML
  frontmatter rules the model obeys with no runtime. A greenlight checkpoint = a rule: *"Do not proceed
  past PACKAGE until the user types GREENLIGHT."*

## 3. Standardized output contract / handoff prompt (most directly transferable)

**Spec-kit** (github.com/github/spec-kit) operationalizes spec-driven dev as slash commands each writing a
**fixed-path markdown artifact**:
`constitution.md → spec.md → (clarify appends) → plan.md + data-model.md + research.md + contracts/ +
quickstart.md → tasks.md ([P] parallel markers) → implement reads all by hardcoded path`.
**Three load-bearing design points:**
1. **Hardcoded paths ARE the handoff protocol.** No agent re-interprets prose to find its input.
   → Our prep phase emits a fixed-path package the next phase reads verbatim.
2. **Constitution-as-global-context** (`constitution.md`) = our `governing-rules.yaml` / tier policy,
   referenced by every downstream phase.
3. **The paste-able handoff prompt** is a command template that says "Read `prep/<fixed-files>`. Do not
   ask the user to restate anything." That IS the spec-kit next-phase pattern.

**OpenAI Swarm / Agents SDK `handoffs`** (github.com/openai/swarm, openai.github.io/openai-agents-python/handoffs):
handoff = function returns an Agent; new agent gets a fresh system prompt but sees prior history;
`on_handoff` fires before the new agent begins. → *Justifies: handoff prompt replaces the system prompt,
and the prep package is the only "history" the next fresh session needs.*

## 4. Challenge taxonomy + exemplar library (CSM rubric)

**Common Sense Media's rating rubric** (commonsensemedia.org/.../about-our-ratings) is the cleanest
typed taxonomy precedent:
- **Fixed typed dimensions** (each 0–5): Violence & Scariness; Sex/Romance/Nudity; Language;
  Products/Purchases; Drinking/Drugs/Smoking; Positive Messages; Positive Role Models; Diverse
  Representations; Educational Value.
- Each dimension has **explicit guiding questions** reviewers apply per-title.
- **Verdict routing**: a dimension score routes the title to an age band; "no dots" ≠ "zero dots" — it
  means "not applicable / doesn't rate."
→ *Adopt this shape for `CHALLENGES.yaml`: each challenge type declares governing rule + guiding
questions + ONE verified exemplar, with a SEPARATE field for illustrative-only exemplars. The
"didn't-rate vs rated-zero" distinction is exactly our "challenge-type-absent vs
illustrative-not-yet-verified" anti-hallucination distinction.*

## 5. Meaning-preservation invariant (grounding for "Check D")

Adaptation theory reframes success **away from fidelity** ("faithful to plot/detail") **toward meaning
preserved under surface transformation**:
- **Hutcheon & Bortolotti, "Rethinking Fidelity Discourse"** (2007; via en.wikipedia.org/wiki/Film_adaptation):
  biological-adaptation metaphor — the *environment* (target audience / age tier) determines fitness.
- **Robert Stam's "dialogic process"**: adaptation as dialogue; departures are explained by audience /
  cultural context.
→ *Check D should NOT be a fidelity check ("did it preserve the sentence?"). It should be a
meaning-preservation check ("did the transform preserve what the source MEANT?"), evaluated against the
target tier as the 'environment'. Caution: cite the concept, not specific Stam/Hutcheon terminology
without primary-text verification.*

## Relevance to each design tension (cross-link to seed-brief Open Tensions)

- **T1 (which layer):** spec-kit/CrewAI precedent ⇒ the layer WITH orchestration (0.1) owns the prep
  phase; root gets at most a thin entry stub.
- **T2 (work-level vs chapter-level):** CrewAI AgentPlanner ⇒ a dedicated work-level planner/researcher
  agent runs BEFORE the per-chapter `analyst`.
- **T3 (orchestrator shape):** Cursor-rules + spec-kit clarify ⇒ orchestrator is a NATIVE agent driven by
  a command/skill; the question gate is a prompt-emitted block + a greenlight rule, not code.
- **T4 (derived content topology):** CSM "didn't-rate vs zero" + spec-kit fixed paths ⇒ separate
  verified-source path (`work/`, `kb/`) from method-illustration path (`adaptation-rules/resources/`),
  marked explicitly.
- **T5 (path contract):** spec-kit hardcoded-path handoff ⇒ a fixed `prep/<work>/` file set.
- **T6 (mechanize mapping authoring):** CSM typed-taxonomy + guiding-questions ⇒ challenge taxonomy routes
  to governing rules; the mapping is a derived output, scored against the taxonomy.
- **T7 (root parity):** out of scope unless root must match; spec-kit precedent says one substrate is
  enough.
- **T8 (handoff command):** spec-kit/Swarm ⇒ a named command that hardcodes the prep package paths.

## Sources

- [CrewAI — Crews, processes, planning](https://docs.crewai.com/concepts/crews)
- [BabyAGI repo](https://github.com/yoheinakajima/babyagi)
- [GitHub spec-kit](https://github.com/github/spec-kit)
- [LangGraph interrupt/Command(resume) via Context7](https://github.com/langchain-ai/langgraph)
- [OpenAI Swarm](https://github.com/openai/swarm) · [Agents SDK Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [Cursor — project rules](https://cursor.com/docs/context/rules)
- [Common Sense Media — about our ratings](https://www.commonsensemedia.org/about-us/our-mission/about-our-ratings)
- [Wikipedia — Film adaptation (Stam, Hutcheon & Bortolotti)](https://en.wikipedia.org/wiki/Film_adaptation)
