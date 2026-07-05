# Research 02 — Patterns & Conventions (Authoring Dialect)

**Track goal:** Build an MDTM task file to implement the LAF adaptation-prep phase per `docs/native-prep/design/DESIGN.md` (+ companions).
**This file:** concrete, copy-followable authoring conventions for each new file, with `file:line` evidence.
**Scope boundary:** Authoring conventions ONLY. (R1=file inventory/edit anchors; R3=check_boundary/VENDOR; R4=MDTM template; R5=design↔code cross-val; R6=verification commands.)

Status: **Complete.**

## Quick-reference checklist (copy-followable, for the task author)

- **New agent** (`prep-cordinator.md`): 5 keys `name/description/model/skills/tools`; `model: opus`; `skills:` block-list all `laf-adaptation:<skill>`; `tools: >` folded form because it has `Agent(...)`. NO Mars keys. `name:` MUST equal filename stem (spelling `prep-cordinator` intentional).
- **Agent body edits** (`analyst.md` NATIVE, `tier-coordinator.md` BUILD-NEW): additive body/frontmatter only; both bodies are not hash-pinned → boundary-safe, no VENDOR row change.
- **New skill** (`prep`, `thematic-fidelity` if authored): frontmatter = `name` + `description: |` (literal block) ONLY; dir = `SKILL.md` [+ `resources/`]; NO `rules/` or `templates/` subdirs.
- **New commands** (`.claude/commands/laf/prep.md`, `rewrite.md`): must CREATE `.claude/commands/laf/`; frontmatter `description` + `argument-hint`; body = thin delegation prompt. Path `<ns>/<cmd>.md` → `/<ns>:<cmd>`.
- **Exemplar files** (`skills/adaptation-rules/resources/exemplars/*.md`): line 1 verbatim `<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->`. No new VENDOR row.
- **Mapping**: 5 root keys `work_metadata/characters/concepts/key_scenes/master_translation_table`; hyphen `<slug>-mapping.yaml` (0.1, 6-key with `meaning:`) vs underscore `<slug>_mapping.yaml` (root, 5-key, `meaning:` stripped).

---

## 1. AGENT frontmatter dialect (Claude-native, cw-lowered — NOT Mars)

**Rule source (injected CLAUDE.md §3):** `laf-adaptation/CLAUDE.md` §3 "LAF Conventions" states:
> Agents: `name`, `description`, `model` (∈ {opus, sonnet, haiku, inherit} — never a Mars alias), `skills` (fully-qualified `laf-adaptation:<skill>`), `tools`. Skills: `name` + `description` only. **Never** introduce Mars keys — `type`, `model-invocable`, `effort`, `model-policies`, `sandbox`, `subagents`.

**CONFIRMED: CLAUDE.md §3 forbids the Mars keys** `type`, `model-invocable`, `effort`, `model-policies`, `sandbox`, `subagents`. A new prep agent MUST NOT use any of these.

### 1.1 Exact key set (5 keys, in observed order)

Order observed across all four files: `name` → `description` → `model` → `skills` → `tools`.

| Key | Required? | Value form |
|-----|-----------|-----------|
| `name` | yes | bare lowercase-hyphen identifier, matches filename stem. |
| `description` | yes | single-line prose; may be long (routing description for the muse). |
| `model` | yes | one of `opus` / `sonnet` / `haiku` / `inherit`. |
| `skills` | yes (when agent loads skills) | YAML list of fully-qualified `laf-adaptation:<skill>` entries. |
| `tools` | yes | comma-separated tool list; multiline `>` folded form when it includes `Agent(...)`. |

### 1.2 Model values in use (evidence)

- `laf-adaptation/agents/muse.md:4` → `model: opus`
- `laf-adaptation/agents/analyst.md:4` → `model: opus`
- `laf-adaptation/agents/tier-coordinator.md:4` → `model: opus`
- `laf-adaptation/agents/web-researcher.md:4` → `model: sonnet`

So `opus` is the default for orchestrators/analysts; `sonnet` for the lighter web-researcher. `haiku`/`inherit` are permitted by §3 but not observed in these four.

### 1.3 Fully-qualified `laf-adaptation:<skill>` skills syntax (block-list form)

Every `skills:` entry is `laf-adaptation:<skill>` (never a bare skill name, never the upstream `creative-writing-skills:` prefix). Block-list style with `-` bullets:

- `laf-adaptation/agents/analyst.md:5-9`:
  ```yaml
  skills:
    - laf-adaptation:source-fidelity
    - laf-adaptation:adaptation-tiers
    - laf-adaptation:story-memory
  tools: Read, Write, Glob, Grep
  ```
- `laf-adaptation/agents/tier-coordinator.md:5-9` — same shape, 3 skills (`adaptation-tiers`, `source-fidelity`, `kb-management`).
- `laf-adaptation/agents/web-researcher.md:5-7` — single-entry list (`- laf-adaptation:creative-research`).
- `laf-adaptation/agents/muse.md:5-21` — 16-entry block list, all `laf-adaptation:` prefixed.

### 1.4 The multiline `tools: >` Agent(...) orchestrator form (muse)

Orchestrators that can spawn subagents use the YAML folded-block scalar `>` so the `Agent(...)` spawn list plus the plain tools read as one folded string. Verbatim from `laf-adaptation/agents/muse.md:22-26`:

```yaml
tools: >
  Agent(writer, critic, reader-sim, character-sim, continuity-checker,
  brainstormer, outliner, style-creator, editor, web-researcher),
  Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
```

Key points for authoring a NEW orchestrator prep agent:
- Use `tools: >` (folded) whenever the tool string contains an `Agent(...)` clause spanning lines.
- `Agent(...)` lists the spawnable subagent **names** (bare, comma-separated), then a comma, then the plain tools.
- Non-orchestrator agents use the **inline single-line** `tools:` form instead:
  - `analyst.md:9` → `tools: Read, Write, Glob, Grep`
  - `tier-coordinator.md:9` → `tools: Read, Write, Glob, Grep, Bash`
  - `web-researcher.md:7` → `tools: Read, WebSearch, WebFetch`

### 1.5 Body conventions

- After the `---` fence, an H1 title matching the agent name (`# Muse`, `# Analyst`, `# Tier Coordinator`, `# Web Researcher`).
- Body is a delegation/procedure prompt in prose + fenced pseudocode blocks (see `analyst.md:33-49`, `tier-coordinator.md:26-37`). No frontmatter-level behavioral keys — behavior lives in the body and attached skills.
- Web-researcher shows the **minimal** viable body: `# Web Researcher` + one line pointing at its skill (`web-researcher.md:9-11`). A thin agent that just loads one skill is an accepted pattern.

---

## 2. SKILL frontmatter + body/dir conventions

### 2.1 Frontmatter: `name` + `description` ONLY (no other keys)

Per CLAUDE.md §3: "Skills: `name` + `description` only." Both sampled skills obey exactly:

- `laf-adaptation/skills/source-fidelity/SKILL.md:1-8` — frontmatter is `name:` then `description: |` block, `---` close. No `model`, no `tools`, no Mars keys.
- `laf-adaptation/skills/adaptation-rules/SKILL.md:1-7` — same two-key shape.

A NEW prep skill's frontmatter MUST be exactly these two keys.

### 2.2 The `description: |` literal-block style

Both skills use the YAML literal block scalar `|` for a multi-line description (not a single-line string):

- `source-fidelity/SKILL.md:3-7`:
  ```yaml
  description: |
    The v2.0 anti-hallucination protocol for source analysis. Mandates CERTAIN/PROBABLE/UNCERTAIN
    confidence tags on every extracted fact, a source-access declaration with ABORT-on-NO-ACCESS, and a
    dual-pass documentation procedure. Load before any source transform. Transparent uncertainty > false
    certainty.
  ```
- `adaptation-rules/SKILL.md:3-7` — same `description: |` multi-line form.

Convention: the description ends with a short "Load when/before …" cue (`Load before any source transform.` / `Load when writing or critiquing an adaptation draft.`).

### 2.3 Directory structure: `SKILL.md` + optional `resources/` (NO `rules/` or `templates/` subdirs)

Observed layouts (from `ls -R`):
- `laf-adaptation/skills/source-fidelity/` → **only** `SKILL.md` (no subdirs at all — a skill can be a single file).
- `laf-adaptation/skills/adaptation-rules/` → `SKILL.md` + `resources/` containing `agency.md`, `character.md`, `thematic.md`.

Conventions:
- The skill package root file is always `SKILL.md` (uppercase).
- Auxiliary content lives under `resources/` ONLY. `adaptation-rules/SKILL.md:15-19` names each resource file and its purpose ("carried from …") inline.
- **No `rules/` or `templates/` subdirs** — this is the SuperClaude/Mars skill layout, which the LAF tree deliberately does not use. The LAF flat convention is `SKILL.md [+ resources/]`. (CLAUDE.md §1 also warns: prefer a NATIVE standalone skill over dropping files into an adopted skill's `resources/`.)

### 2.4 Body conventions

- H1 title after the fence (`# Source Fidelity — v2.0 …`, `# Adaptation Rules`).
- A `Resources:` bullet list enumerating each `resources/<file>.md` with a one-line purpose when `resources/` exists (`adaptation-rules/SKILL.md:15-19`).
- Cross-tree `§` design-pack references are explicitly called **build-time provenance, not runtime deps** (`source-fidelity/SKILL.md:92-94`); the in-tree body is self-sufficient. New skills should restate their runtime contract in-tree, not rely on `§` pointers.

---

## 3. COMMAND file format (Claude Code slash commands)

**Present state:** `.claude/commands/` is **EMPTY** — verified `ls -la .claude/commands/` shows only `.` and `..`, and `find .claude/commands -type f` returns nothing. **No LAF command file exists yet**; the prep phase must author it/them from scratch.

### 3.1 Path → invocation mapping (Claude Code standard)

A command file at `.claude/commands/<ns>/<cmd>.md` resolves to the slash command `/<ns>:<cmd>`. (e.g. `.claude/commands/laf/prep.md` → `/laf:prep`). This project already uses this namespace convention for `sc:*` commands (see `sc:*` skill/command list), confirming the `<ns>/<cmd>.md → /<ns>:<cmd>` resolution is the active dialect here.

### 3.2 Command frontmatter keys

Standard Claude Code command frontmatter keys to use:
- `description` — one-line summary shown in the command menu.
- `argument-hint` — the argument placeholder shown after the command name (e.g. `argument-hint: <source-path>`).

Body = the delegation prompt (the instructions Claude runs when the command is invoked; typically dispatches to the prep agent). `$ARGUMENTS` / `$1` positional substitution is the Claude Code mechanism for injecting invocation args into the body.

### 3.3 Target content = design command specs

The exact content for the LAF command(s) is specified in the design pack: **`docs/native-prep/design/prep-agent-schemas.md §5`** (command specs). Author the command file(s) to match that section.

### 3.4 Design command specs — verified verbatim (`prep-agent-schemas.md §5`)

Two thin-delegator commands under `.claude/commands/laf/` (harness surface; NOT in `VENDOR.md` — `prep-agent-schemas.md:216-218`). Frontmatter uses `description` + `argument-hint` exactly.

**`.claude/commands/laf/prep.md` → `/laf:prep`** (`prep-agent-schemas.md:221-240`) — frontmatter:
```yaml
---
description: Onboard a new literary work — research, analyze, and derive its adaptation prep package.
argument-hint: "<novel title>" [--source <path-or-url>]
---
```
Body: H1 `# /laf:prep`, then a delegation prompt to the `prep-cordinator` agent (do not restate the pipeline; it lives in `laf-adaptation/skills/prep/SKILL.md`).

**`.claude/commands/laf/rewrite.md` → `/laf:rewrite`** (`prep-agent-schemas.md:242-263`) — frontmatter:
```yaml
---
description: Begin the chapter rewrite phase for a work already prepped by /laf:prep.
argument-hint: --work <work-slug>
---
```
Body: H1 `# /laf:rewrite`, delegation prompt that reads the 3 hardcoded package files then hands to `muse`, with a `status: CONFIRMED` greenlight guard (`prep-agent-schemas.md:265-266`).

**Authoring notes for these commands:**
- Both are "thin delegators" — the body is the delegation prompt, NOT the procedure. The procedure lives in the skill/agent.
- Confirm the target dir `.claude/commands/laf/` must be **created** (currently `.claude/commands/` is empty — no `laf/` subdir).
- Header block on the two commands (`prep-agent-schemas.md:1-13`) restates the §3 rule: Claude-native dialect, permitted-key set `name/description/model/skills/tools`, **no Mars keys**.

---

## 4. DERIVED exemplar marker (verbatim line-1 requirement)

**Source of truth:** `docs/native-prep/design/package-schemas.md §7` "Seed exemplar set (R13)".

Each exemplar file under `laf-adaptation/skills/adaptation-rules/resources/exemplars/` (files: `sacrifice-and-return.md`, `betrayal-and-redemption.md`, `petrification-body-horror.md` — `package-schemas.md:257-262`) **MUST open with this exact structural marker on line 1** (`package-schemas.md:267`):

```
<!-- @kind method-illustration; source-fidelity: DERIVED; do-not-treat-as-source-truth -->
```

Then a blank line, then `# Exemplar — <Type> (method illustration; NOT source truth)`, followed by `## Challenge shape`, `## Method by tier` (Tier 1 / Tier 3 / Tier 5 bullets), `## Meaning that must survive` (`package-schemas.md:266-281`).

**Why the marker matters (authoring rationale, `package-schemas.md:283-287`):**
- Exemplars are NATIVE `DERIVED` method illustrations — **not source truth**. The marker is what stops a downstream agent from presenting them as verified source (closes the Q2 contamination risk).
- They live **outside** `work/` and `kb/canon/` (the source-truth paths).
- **VENDOR:** covered by the existing `skills/adaptation-rules/**` NATIVE glob row — **no new VENDOR.md row**.
- The `writer` (ADOPTED-PATCHED, already imports `/adaptation-rules`) loads the matching exemplar when `analyst` flags that challenge type.

A new exemplar file that omits or alters this line-1 marker is a defect — the marker is a fixed contract string, copy it byte-for-byte.

---

## 5. MAPPING schema conventions (underscore vs hyphen split)

### 5.1 The 5 top-level keys (frozen root schema)

The shipped `<work>_mapping` schema has **5 top-level keys**, in this order (verified by `grep -nE '^[a-zA-Z_]+:'`):

1. `work_metadata` (`title`, `author`, `key_challenges[]`)
2. `characters`
3. `concepts`
4. `key_scenes`
5. `master_translation_table`

Evidence — all three files agree on the same 5 keys:
- `laf-adaptation/templates/work-mapping-template.yaml:4,11,39,47,57`
- `config/concept_mapping/templates/tolkien_mapping.yaml:4,13,43,64,77` (underscore name)
- `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml:4,13,43,64,77` (hyphen name)

**VERIFIED: the two Tolkien files are byte-identical** (`diff` → IDENTICAL). So the 5-key body is shared; the difference between them is **file name + tree location + (in 0.1 target state) an added `meaning:` key**, not the current body.

### 5.2 The underscore-vs-hyphen file-naming split

Two distinct naming+location conventions for the SAME logical mapping:

| Tree / location | Filename convention | Key count | `meaning:`? | Evidence |
|---|---|---|---|---|
| **ROOT** `config/concept_mapping/templates/` (frozen root schema, pre-0.1) | **underscore**: `<work>_mapping.yaml` (e.g. `tolkien_mapping.yaml`, `narnia_mapping.yaml`) | **5-key** | STRIPPED (root gains no meaning) | `config/concept_mapping/templates/{tolkien_mapping,narnia_mapping}.yaml` |
| **0.1** `laf-adaptation/kb/adaptation-mapping/` (LAF 0.1 tree) | **hyphen**: `<work>-mapping.yaml` (e.g. `tolkien-mapping.yaml`) | **6-key** (target: adds `meaning:`) | KEPT (0.1 extension) | `laf-adaptation/kb/adaptation-mapping/tolkien-mapping.yaml` |
| Template | hyphen: `work-mapping-template.yaml` | 5-key | — | `laf-adaptation/templates/work-mapping-template.yaml` |

This "dual-form promotion" is authoritatively specified in **`docs/native-prep/design/package-schemas.md §4.1`** (`package-schemas.md:190-201`): on greenlight, `/kb-management` writes BOTH forms —
- `kb/adaptation-mapping/<slug>-mapping.yaml` (0.1, **hyphen**) → 6-key, `meaning:` **kept**, `_confidence` diagnostics kept.
- `config/concept_mapping/templates/<slug>_mapping.yaml` (root, **underscore**) → 5-key, `meaning:` **STRIPPED**, `_confidence` dropped, so it validates byte-identically against the shipped `tolkien_mapping.yaml` shape.

**The `meaning:` 6th key (0.1-only)** is defined in `package-schemas.md:160-166` as a dual/effective-confidence block:
```yaml
meaning:
  value: "<work-level meaning>"
  text_confidence: PROBABLE
  context_confidence: PROBABLE
  confidence: PROBABLE            # = min(text, context)
```

**Authoring takeaways:**
- The prep phase's `30-mapping.yaml` (the derived work-mapping) is the **6-key** form and lives at `work/prep/<slug>/30-mapping.yaml`; on promotion it forks into the hyphen-6-key and underscore-5-key targets above.
- Do NOT add `meaning:` or `_confidence` to the ROOT underscore copy — it is the frozen 5-key schema (`package-schemas.md:197,201`, R14: "Root gains no meaning concept and no new machinery").
- "ROOT" = the pre-0.1 `config/concept_mapping/` tree (underscore, 5-key); "0.1" = the `laf-adaptation/kb/adaptation-mapping/` tree (hyphen, 6-key target).

### 5.3 Mapping body style (from tolkien-mapping.yaml)

- Leading `#`-comment header naming the work (`tolkien-mapping.yaml:1-2`).
- `characters:` and `key_scenes:` use **inline-flow-map** tier rows: `tier_1: {name: "...", archetype: "...", ...}` (`tolkien-mapping.yaml:15,66`).
- `concepts:` tier values are plain strings (`tolkien-mapping.yaml:44-45`).
- `master_translation_table:` is a list of inline-flow-maps `{original, tier_1, principle}` (`tolkien-mapping.yaml:78-81`).
- The template (`work-mapping-template.yaml`) uses the **expanded** block form with `[Placeholder]` tokens — copy it and fill, per its own header comment (`work-mapping-template.yaml:1-2`).

---
