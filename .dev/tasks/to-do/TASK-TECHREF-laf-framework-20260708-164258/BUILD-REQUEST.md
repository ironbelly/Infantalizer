# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-reference
Task Directory: .dev/tasks/to-do/TASK-TECHREF-laf-framework-20260708-164258/
Research Notes: .dev/tasks/to-do/TASK-TECHREF-laf-framework-20260708-164258/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Create a comprehensive Technical Reference document for the LAF (Literary Adaptation Framework) under `laf-adaptation/`, following the project template. The document will be written to docs/laf/LAF-ADAPTATION-FRAMEWORK-TECHNICAL-REFERENCE.md.

WHY: The LAF framework was built across Phases 0–2 (a prompt + YAML-config framework for tier-aware literary adaptation) and has just been exercised end-to-end (narnia ch-01 adapted across Tiers 1/2/3/5, reconciled, and promoted to canon). It needs a canonical, code-verified technical reference so both AI agents and human contributors can understand, run, and extend the two pipelines (prep + rewrite), the tier axis, the kb layer, and the boundary contract without reading every source file. The existing in-tree docs (CLAUDE.md, docs/native-prep/design/*, ADRs) are partly stale (e.g. provenance counts) — this reference documents the ACTUAL current tree.

TASK_ID_PREFIX: TASK-TECHREF

FEATURE_SLUG: laf-framework

TEMPLATE: 02

DOCUMENTATION STALENESS WARNINGS:
One staleness item is already identified during scope discovery and MUST be surfaced (not resolved away):
`laf-adaptation/CLAUDE.md` §1 states "15 agent files" and "16 skill dirs", but the live tree has 16 agents
and 18 skills (the `prep-cordinator` agent and prep-era skills were added after that CLAUDE.md text). Tag
this [CODE-CONTRADICTED] and record it in Tech Debt (Section 14). This is doc drift, NOT a framework defect —
the tech reference documents the actual 16/18 tree. Phase 2 Agent 06 (Doc Analyst) owns confirming exact
current counts and the ADOPTED/NATIVE/BUILD-NEW split. All other Phase 2 agents perform full documentation
cross-validation with CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED tags.
Do NOT create task items that reference architecture marked [CODE-CONTRADICTED] or [UNVERIFIED] as current.

TEMPLATE 02 PATTERN MAPPING FOR THIS SKILL:
- Phase 1 (Preparation): Update task status, confirm scope from research notes, read the template at /config/.claude/templates/documents/technical_reference_template.md, confirm Standard depth tier, confirm task folder + research/synthesis/qa/reviews subfolders exist (already created).
- Phase 2 (Deep Investigation): L1 Discovery — 6 codebase agents investigate the framework and write findings files to research/. Spawn ALL 6 in parallel.
- Phase 3 (Completeness Verification): L4 Review/QA — STANDARD intensity = 3 agents (1 rf-analyst completeness + 1 rf-qa evidence-quality + 1 rf-qa-qualitative research-depth) IN PARALLEL, fix_authorization:false. Consolidate → gap-fill research agents (one per gap) → 2-agent verify. Max 2 cycles. (6 research files, no partitioning needed.)
- Phase 4 (Web Research): L1 Discovery — 1 optional agent (developmental-tiers grounding), gap-driven only.
- Phase 5 (Synthesis + Gate): L2 Build-from-Discovery — 5 synthesis agents read research files and produce template-aligned synth sections. Then STANDARD gate = 3 agents (1 rf-analyst synthesis-accuracy + 1 rf-qa structure + 1 rf-qa-qualitative coherence) IN PARALLEL, fix_authorization:false. Consolidate → 1 rf-qa fix agent → 2-agent verify. Max 2 cycles. >4 synth files → partition the gate.
- Phase 6 (Assembly + Lens QA + Fidelity): L6 Aggregation — rf-assembler consolidates synth files into the final doc. Then Gate 3 lens QA STANDARD = 7 agents (3 rf-qa structural: template-conformance, internal-consistency, evidence-quality; 3 rf-qa-qualitative content: actionability, domain-accuracy, crossref-chain; 1 domain lens rf-qa: code-example-accuracy), all fix_authorization:false → consolidate → 1 fix → 2-agent verify (max 2 cycles). Then Gate 4 source-fidelity STANDARD = 2 rf-qa fidelity agents (semantic-coverage + detail-preservation) reading actual laf-adaptation/ source + full doc → consolidate → 1 fix → 2-agent verify (max 2 cycles).
- Phase 7 (Present to User & Complete Task): ANTI-ORPHANING — task-completion items WITHIN this phase.

QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: PER_PHASE
  Gate 1: Research Completeness (Phase 3) — standard: 1 rf-analyst (completeness) + 1 rf-qa (evidence-quality) + 1 rf-qa-qualitative (research-depth) = 3 agents. Max 2 fix cycles.
  Gate 2: Synthesis Quality (Phase 5) — standard: 1 rf-analyst (accuracy) + 1 rf-qa (structure) + 1 rf-qa-qualitative (coherence) = 3 agents. Max 2 fix cycles.
  Gate 3: Final Document Lens-Based QA (Phase 6, step 6a) — standard: 3 rf-qa structural (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative content (actionability, domain-accuracy, crossref-chain) + 1 domain lens (code-example-accuracy) = 7 agents. Max 2 fix cycles.
  Gate 4: Source-Document Fidelity (Phase 6, step 6c) — standard: 2 rf-qa fidelity agents (semantic-coverage + detail-preservation). Max 2 fix cycles.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION + SOURCE_FIDELITY + NO_DOCS_CLOSE_DEFECT
  TEMPLATE_COMPLIANCE: All sections present or marked N/A with rationale. N/A expected for §6 State Management and §7 Component Inventory (no client-side state / UI components — this is a prompt+YAML framework); §11 Performance is a short note (no runtime), not a measured profile.
  EVIDENCE_TRAIL: Every claim cites file paths (laf-adaptation/...:line), agent/SKILL bodies, or verified sources.
  CROSS_VALIDATION: Doc-sourced claims (from docs/ and CLAUDE.md) carry [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tags.
  SOURCE_FIDELITY: Gate 4 fidelity agents read actual laf-adaptation/ source (agent bodies, SKILL.md files, kb/tiers/*.yaml, check_boundary.py) AND the assembled doc; verify every documented subsystem, agent I/O contract, tier threshold, and boundary rule against source, not just synthesis files.
  NO_DOCS_CLOSE_DEFECT (C8): A [CODE-CONTRADICTED] finding on an in-scope capability (something a spec/ADR names as shipped but that is not actually wired) MUST be recorded as a DEFECT with a linked MDTM remediation task, not re-labeled as a known-gap without a cited scope decision. NOTE: the known CLAUDE.md count drift is a DOC-vs-DOC staleness (stale prose count vs actual tree), NOT an unwired capability — it is correctly Tech-Debt §14, not a C8 defect. Apply C8 only if an agent finds an ADR/spec-declared capability that is genuinely not wired in the framework.

TESTING_REQUIREMENTS: N/A — documentation-only skill, no code produced. (Note: the framework itself HAS a test at laf-adaptation/scripts/test_check_boundary.py — document its existence in §5.6/§13, but this skill writes no tests.)

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-TECHREF-laf-framework-20260708-164258/research-notes.md
Read this file FIRST for full detailed findings: existing files, patterns, the 6 planned investigation assignments with types and output paths, synthesis mapping, N/A section rationale, and the pre-identified staleness item.

TEMPLATE_PATH: /config/.claude/templates/documents/technical_reference_template.md
OUTPUT_PATH: docs/laf/LAF-ADAPTATION-FRAMEWORK-TECHNICAL-REFERENCE.md

SKILL CONTEXT FILE:
/config/.claude/skills/tech-reference/SKILL.md
Read the "Agent Prompt Templates" section for: Codebase Research Agent Prompt, Web Research Agent Prompt, Synthesis Agent Prompt, the rf-analyst / rf-qa / rf-qa-qualitative gate prompts, the Lens-Based QA prompts, the Source-Document Fidelity prompt, and the rf-assembler Assembly prompt. Read "Synthesis Mapping Table", "Content Rules", "Validation Checklist", "Tier Selection", "Output Structure". Embed these in the relevant checklist items per B2 self-contained pattern.

CRITICAL — GRANULARITY REQUIREMENT:
Per MDTM template rules A3 and A4, create individual checklist items for EVERY research agent (6), web research topic (1), synthesis file (5), each QA lens agent, each consolidation step, each fix agent, and each verification agent. Do NOT batch. Each lens agent gets its own item. A Phase 6 QA gate will have ~12-16 items (7 lens agents + consolidation + fix + 2 verify + 2 fidelity + consolidation + fix + 2 verify).

IMPORTANT PATH NOTE FOR TASK FILE:
This project (/config/workspace/Infantalizer) has NO local .claude/templates. The template and MDTM templates live at /config/.claude/templates/... — use ABSOLUTE paths for the template in all embedded agent prompts. The framework under investigation is /config/workspace/Infantalizer/laf-adaptation/. All agents must use absolute paths.

TO BUILD A GOOD TASK FILE, YOU NEED: goal + outputs, source files/context (from research notes), phases/steps (from research notes SUGGESTED_PHASES + the phase mapping above), verification criteria, dependencies. The research notes cover most of this.

ESCALATION:
You are running as a subagent (no team context). Do NOT broadcast TASK_READY, use TaskCreate, or SendMessage. Return the task file path as your final output. Codebase questions → codebase-retrieval / grep. If blocked → create the best task file you can and note gaps in the Task Log.

SKILL PHASES TO ENCODE IN TASK FILE:
Encode Phases 1–7 as sequential B2 self-contained checklist items exactly as described in the TEMPLATE 02 PATTERN MAPPING and QA_GATE_REQUIREMENTS above. Every agent prompt embedded per B2 MUST include its mandatory protocol blocks: Incremental File Writing Protocol (all agents), ADVERSARIAL STANCE (QA/analyst agents), Documentation Staleness Protocol (research agents). Anti-orphaning: task-completion items inside Phase 7.

TASK FILE LOCATION: .dev/tasks/to-do/TASK-TECHREF-laf-framework-20260708-164258/TASK-TECHREF-laf-framework-20260708-164258.md

STEPS:
1. Read the research notes file specified above (MANDATORY).
2. Read the SKILL.md file specified above for agent prompts, synthesis mapping, content rules, validation checklist, tier selection, assembly procedure (MANDATORY).
3. Read the MDTM template: /config/.claude/templates/workflow/02_mdtm_template_complex_task.md (MANDATORY).
4. Follow PART 1 instructions in the template completely (A3 granularity, B2 self-contained items, E1-E4 flat structure).
5. Note any gaps in the Task Log section.
6. Create the task file at .dev/tasks/to-do/TASK-TECHREF-laf-framework-20260708-164258/TASK-TECHREF-laf-framework-20260708-164258.md using PART 2 structure.
7. Return the task file path.
