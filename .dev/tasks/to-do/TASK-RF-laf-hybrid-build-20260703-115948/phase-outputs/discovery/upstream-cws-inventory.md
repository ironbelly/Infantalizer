# Upstream CWS Vendoring Inventory — Phase 0 Discovery (L1 deliverable)

**Generated:** 2026-07-03 (Step 2.1)

## Upstream acquisition parameters (feed VENDOR.md + the `--upstream <dir>` flag)

- **upstream_repo:** `https://github.com/haowjy/creative-writing-skills` (confirmed via `git remote -v` on the checkout — `origin` = `https://github.com/haowjy/creative-writing-skills.git`)
- **upstream_sha (pinned):** `3338495f0fabf778720effdda9386ab56d4ebf6e`
- **checkout-dir (the `--upstream <dir>` value):** `.dev/releases/current/0.1/creative-writing-skills` (repo-relative; absolute `/config/workspace/Infantalizer/.dev/releases/current/0.1/creative-writing-skills`)
- **vendored_on:** 2026-07-03
- **license:** Apache-2.0 (upstream) — attribution retained per NOTICE
- **prefix_rewrite:** `"creative-writing-skills:" -> "laf-adaptation:"` (uniform, deterministic)

### Acquisition note (why no fresh network clone)

A pre-existing, working-tree-clean checkout of the exact upstream repo was already present at `.dev/releases/current/0.1/creative-writing-skills`, pinned at SHA `3338495f0fabf778720effdda9386ab56d4ebf6e`. It is a nested git repo (its `origin` remote is the target repo), sits **outside** the future `laf-adaptation/` tree (so Rule F's `glob("agents/*.md") + glob("skills/**/SKILL.md")` — rooted at `laf-adaptation/` — never scans it), and was added to `.gitignore` in Step 1.2 so it is never committed. It is therefore used directly as the `--upstream <dir>` source, satisfying the Step 2.1 requirement (clone + pin) without a network round-trip. All adopted files are vendored from its **`cw/`** subtree (Claude-lowered dialect), **never** from `agents/` (Mars source).

## Summary counts (the manifest MUST hash all of these)

| Metric | Count |
|--------|-------|
| Adopted agents (`cw/agents/*.md`) | **11** |
| Adopted skill directories (`cw/skills/<name>/`) | **12** |
| Adopted skill-tree files (SKILL.md + every `resources/**`) | **45** (12 SKILL.md + 33 resource files) |
| **Total adopted files hashed** (11 agents + 45 skill-tree files) | **56** |
| Provenance classes present | ADOPTED-CLEAN (10 agents + all 12 skills), ADOPTED-PATCHED (`writer.md` only) |

> **"23 adopted files"** in the task overview = 11 agents + 12 skill *dirs* (top-level adopted units). Recursively, that expands to **56** hashed files because each adopted skill carries its full `resources/**` subtree, all recursively hashed so a body edit to any resource is caught (boundary-contract.md §2 lines 87-88).

> **Non-adopted skills present in the checkout (EXCLUDED — do NOT vendor):** the checkout's `cw/skills/` ships 18 dirs; only the 12 named below are adopted. The 6 excluded are `character-sim`, `creative-writing-muse`, `interactive-artifact`, `project-setup`, `reader-sim`, `story-planning` (not in the reconciled 12-ADOPTED set per constraint #8). `character-sim`/`reader-sim` exist as *agents* in the adopted set, but their same-named *skill* dirs are NOT adopted.

## Adopted agents (11) — vendored per-file from `cw/agents/<name>.md`

Each gets the uniform prefix rewrite `creative-writing-skills:` → `laf-adaptation:` on its `skills:` frontmatter list; body byte-identical. `writer.md` (11th) additionally gets ONE appended line `- laf-adaptation:adaptation-rules` (ADOPTED-PATCHED, two distinct hashes). Quartet members {critic, editor, reader-sim, continuity-checker} MUST be present + ADOPTED-CLEAN (Rule D).

| Target Path | Upstream Path | Provenance Class |
|-------------|---------------|------------------|
| `agents/muse.md` | `cw/agents/muse.md` | ADOPTED-CLEAN |
| `agents/critic.md` | `cw/agents/critic.md` | ADOPTED-CLEAN (quartet) |
| `agents/editor.md` | `cw/agents/editor.md` | ADOPTED-CLEAN (quartet; NEVER folded/modified) |
| `agents/reader-sim.md` | `cw/agents/reader-sim.md` | ADOPTED-CLEAN (quartet) |
| `agents/continuity-checker.md` | `cw/agents/continuity-checker.md` | ADOPTED-CLEAN (quartet) |
| `agents/brainstormer.md` | `cw/agents/brainstormer.md` | ADOPTED-CLEAN (dormant) |
| `agents/outliner.md` | `cw/agents/outliner.md` | ADOPTED-CLEAN (dormant) |
| `agents/character-sim.md` | `cw/agents/character-sim.md` | ADOPTED-CLEAN (dormant) |
| `agents/style-creator.md` | `cw/agents/style-creator.md` | ADOPTED-CLEAN (dormant) |
| `agents/web-researcher.md` | `cw/agents/web-researcher.md` | ADOPTED-CLEAN (dormant; CWS 11th agent) |
| `agents/writer.md` | `cw/agents/writer.md` | **ADOPTED-PATCHED** (+1 additive `- laf-adaptation:adaptation-rules`) |

## Adopted skills (12 dirs, 45 files) — vendored per-skill from `cw/skills/<name>/`

Each skill = SKILL.md + full `resources/**` subtree, ALL prefix-rewritten (`creative-writing-skills:` → `laf-adaptation:`) and ALL ADOPTED-CLEAN (byte-identical to upstream-after-rewrite). Every file listed below is recursively hashed by `--init` (Rule A/B). Target paths drop the `cw/` prefix (`cw/skills/X` → `skills/X`).

| Target Path | Upstream Path | Provenance Class |
|-------------|---------------|------------------|
| `skills/writing-principles/SKILL.md` | `cw/skills/writing-principles/SKILL.md` | ADOPTED-CLEAN |
| `skills/writing-principles/resources/citations.md` | `cw/skills/writing-principles/resources/citations.md` | ADOPTED-CLEAN |
| `skills/writing-principles/resources/failure-modes.md` | `cw/skills/writing-principles/resources/failure-modes.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/SKILL.md` | `cw/skills/creative-writing-craft/SKILL.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/prose-writing.md` | `cw/skills/creative-writing-craft/resources/prose-writing.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/scene-construction.md` | `cw/skills/creative-writing-craft/resources/scene-construction.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/style-analysis.md` | `cw/skills/creative-writing-craft/resources/style-analysis.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/genre/fantasy.md` | `cw/skills/creative-writing-craft/resources/genre/fantasy.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/genre/horror.md` | `cw/skills/creative-writing-craft/resources/genre/horror.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/genre/litfic.md` | `cw/skills/creative-writing-craft/resources/genre/litfic.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/genre/mystery.md` | `cw/skills/creative-writing-craft/resources/genre/mystery.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/genre/romance.md` | `cw/skills/creative-writing-craft/resources/genre/romance.md` | ADOPTED-CLEAN |
| `skills/creative-writing-craft/resources/genre/thriller.md` | `cw/skills/creative-writing-craft/resources/genre/thriller.md` | ADOPTED-CLEAN |
| `skills/creative-writing-modes/SKILL.md` | `cw/skills/creative-writing-modes/SKILL.md` | ADOPTED-CLEAN |
| `skills/creative-writing-modes/resources/prose-modes.md` | `cw/skills/creative-writing-modes/resources/prose-modes.md` | ADOPTED-CLEAN |
| `skills/story-review/SKILL.md` | `cw/skills/story-review/SKILL.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/copyedit.md` | `cw/skills/story-review/resources/copyedit.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/developmental-edit.md` | `cw/skills/story-review/resources/developmental-edit.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/editorial-review.md` | `cw/skills/story-review/resources/editorial-review.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/line-edit.md` | `cw/skills/story-review/resources/line-edit.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/proofreading.md` | `cw/skills/story-review/resources/proofreading.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/reader-sim-signal.md` | `cw/skills/story-review/resources/reader-sim-signal.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique.md` | `cw/skills/story-review/resources/prose-critique.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/analyze.py` | `cw/skills/story-review/resources/prose-critique/analyze.py` | ADOPTED-CLEAN (upstream resource, not a LAF script) |
| `skills/story-review/resources/prose-critique/antipatterns.md` | `cw/skills/story-review/resources/prose-critique/antipatterns.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/baseline.md` | `cw/skills/story-review/resources/prose-critique/baseline.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/character.md` | `cw/skills/story-review/resources/prose-critique/character.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/continuity.md` | `cw/skills/story-review/resources/prose-critique/continuity.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/prose.md` | `cw/skills/story-review/resources/prose-critique/prose.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/structure.md` | `cw/skills/story-review/resources/prose-critique/structure.md` | ADOPTED-CLEAN |
| `skills/story-review/resources/prose-critique/voice.md` | `cw/skills/story-review/resources/prose-critique/voice.md` | ADOPTED-CLEAN |
| `skills/story-memory/SKILL.md` | `cw/skills/story-memory/SKILL.md` | ADOPTED-CLEAN |
| `skills/story-memory/resources/fact-extraction.md` | `cw/skills/story-memory/resources/fact-extraction.md` | ADOPTED-CLEAN |
| `skills/story-memory/resources/story-context.md` | `cw/skills/story-memory/resources/story-context.md` | ADOPTED-CLEAN |
| `skills/story-memory/resources/story-reference-writing.md` | `cw/skills/story-memory/resources/story-reference-writing.md` | ADOPTED-CLEAN |
| `skills/story-memory/resources/story-reference-writing/reference-modes.md` | `cw/skills/story-memory/resources/story-reference-writing/reference-modes.md` | ADOPTED-CLEAN |
| `skills/story-memory/resources/writing-artifacts.md` | `cw/skills/story-memory/resources/writing-artifacts.md` | ADOPTED-CLEAN |
| `skills/story-memory/resources/writing-issues.md` | `cw/skills/story-memory/resources/writing-issues.md` | ADOPTED-CLEAN |
| `skills/kb-management/SKILL.md` | `cw/skills/kb-management/SKILL.md` | ADOPTED-CLEAN (SKILL.md only, no resources) |
| `skills/shared-dao/SKILL.md` | `cw/skills/shared-dao/SKILL.md` | ADOPTED-CLEAN (SKILL.md only) |
| `skills/llm-writing/SKILL.md` | `cw/skills/llm-writing/SKILL.md` | ADOPTED-CLEAN (SKILL.md only) |
| `skills/writing-staffing/SKILL.md` | `cw/skills/writing-staffing/SKILL.md` | ADOPTED-CLEAN (SKILL.md only) |
| `skills/intent-modeling/SKILL.md` | `cw/skills/intent-modeling/SKILL.md` | ADOPTED-CLEAN (SKILL.md only) |
| `skills/grill-with-docs/SKILL.md` | `cw/skills/grill-with-docs/SKILL.md` | ADOPTED-CLEAN (SKILL.md only) |
| `skills/creative-research/SKILL.md` | `cw/skills/creative-research/SKILL.md` | ADOPTED-CLEAN (SKILL.md only) |

### Per-skill file counts (verification)

| Skill | SKILL.md | Resource files | Total |
|-------|----------|----------------|-------|
| writing-principles | 1 | 2 | 3 |
| creative-writing-craft | 1 | 9 | 10 |
| creative-writing-modes | 1 | 1 | 2 |
| story-review | 1 | 15 | 16 |
| story-memory | 1 | 6 | 7 |
| kb-management | 1 | 0 | 1 |
| shared-dao | 1 | 0 | 1 |
| llm-writing | 1 | 0 | 1 |
| writing-staffing | 1 | 0 | 1 |
| intent-modeling | 1 | 0 | 1 |
| grill-with-docs | 1 | 0 | 1 |
| creative-research | 1 | 0 | 1 |
| **TOTAL** | **12** | **33** | **45** |

## Vendoring transform rules (applied per file at Steps 2.3–2.4)

1. **All adopted files:** copy from `cw/` verbatim, apply prefix rewrite `creative-writing-skills:` → `laf-adaptation:` (typically only in SKILL.md/agent `skills:` frontmatter lists; resource `.md`/`.py` bodies usually have no such token but are still passed through the deterministic rewrite so any occurrence is normalized). Body bytes otherwise unchanged.
2. **`writer.md` only:** after the prefix rewrite, append exactly one line `- laf-adaptation:adaptation-rules` to the `skills:` list. Preserve upstream quirks verbatim (e.g. any duplicate `creative-writing-craft` line — do NOT "fix").
3. **Never** introduce Mars keys (`type`, `model-invocable`, `effort`, `model-policies`, `sandbox`, `subagents`) — the `cw/` dialect already excludes them.

