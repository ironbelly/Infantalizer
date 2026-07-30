# Research 04: MDTM Template Rules + Stage-0/Gate-Integration → Task-Phase Mapping

**Status: Complete**
**Topic:** GLOBAL MDTM template rules + how spec Stage-0 → §5/§6 gate integration and prep-cordinator "8 stages" renumber map into task-file phases.
**Track goal:** Implement `/laf:prep` v-next Stage 0 chapter materialization per merged-requirements.md.

---

## Step 1: GLOBAL MDTM Complex Template — Rules (in progress)

Template path: `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1516 lines total; PART 1 = building instructions, read completely).

### 1a. Required frontmatter keys (template lines 1-61)
Frontmatter is a fixed YAML block (L1-61). Keys required / notable for THIS task:
- `id` (L2) — `TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS`; here `TASK-RF-prep-chapter-materialize-20260709-004725`.
- `title`, `description`, `version`, `status` (L7 — start `🟡 To Do`; F5 sets `🟠 Doing`→`🟢 Done`).
- `type` (L9) — docs/prompt authoring → `📚 Documentation` (template default L9).
- `priority` (L11), `created_date`/`updated_date` (L12-13), `assigned_to` (L14).
- `coordinator: orchestrator` (L17), `parent_task` (L19), `depends_on` (L20-22).
- `spec_path` (L23) — "driving spec/PRD/TDD path; populated by task-builder (A.2)" → set to the merged-requirements.md spec path.
- `reflect_pre` block (L24-31) — PRE reflect-gate sign-off (verdict/coverage_pct/depth/tcs/run_id/report/reviewed_at); populated by task-builder at A.10.7.
- `reflect_post` (L32) — POST reflect verdict recorded after the final-phase reflect subagent runs.
- `related_docs` (L33-39), `tags` (L42-46), `task_type: static` (L60) — THIS task is fixed content → `static`.

### 1b. Required sections / structure (Section D + PART 2)
- **D3 CRITICAL RULE (L286-289):** NO checklist items before Phase 1. Order = Frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (first executable). Context-review + prior-stage-input reads live IN Phase 1 (Steps 1.2-1.4), never as pre-Phase items.
- **D1 Workflow Compliance Declaration (L255-262)** — informational only, no checkboxes. [WORKFLOW-DEPENDENT — A1 L89-100. Here the "workflow" surrogate = the merged-requirements.md spec.]
- **D2 Cross-Stage Integration Requirements (L264-284)** — informational only; actual read/verify items go in Phase 1 Step 1.4.
- **Post-Completion Actions** section (C4 L242-247, I13 L616-621) — final items only: post-completion validation (I17), then frontmatter update (status/completion_date/updated_date) + Execution Log entry. Do NOT create a "Task Completion and Handoff Protocol" section.
- **## Task Log / Notes** at bottom with `### Phase N Findings` subsections (referenced by every item's error clause, J1 L850-854).
- FORBIDDEN as standalone sections (C1-C3): "Outputs & Deliverables", "Success Criteria", "Verification Checklist" — all embedded into items.

### 1c. B2 self-contained item pattern (Section B, L159-213) — the 6 elements
Every checklist item = ONE full paragraph (B3 L167-170) reading as a standalone prompt. B2 (L159-166) mandates 6 elements:
1. **Context Reference with WHY** — which file(s) to read and why that context is needed for this action.
2. **Action with WHY** — what to do and why.
3. **Output Specification** — exact output file name, location, content, template to follow.
4. **Integrated Verification** — an "ensuring…" clause; NO fabrication/hallucination, 100% derived from cited source files, document negative evidence on failure. (Verification embedded, NOT a separate item — C3 L236-240, I12 L609-614.)
5. **Evidence on Failure Only** — log to `### Phase N Findings` in Task Log ONLY on blocker/error; success evidenced by the output file (B7.4 L210).
6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- B5 FORBIDDEN (L181-201): standalone "read context" items (no output), missing context ref, multi-line/bulleted items, separate verification items, over-granular items (e.g. "create directory" alone), REMINDER blocks between items (E4 L388-389 — worker sees only batch items).
- Canonical correct example: B4 (L172-179).

### 1d. A3 granular breakdown rule (L108-112)
- Break EVERY workflow phase into atomic, verifiable checklist items.
- Individual checklist item for EVERY file, component, or iteration.
- NO high-level or bulk operations — everything granular, exact file paths, specific requirements, measurable outcomes.
- Reinforced by A4 (pre-enumerate all → one item each → consolidate) and I2 (extreme granularity, L522-527).

### 1e. QA-gate encoding rules
- **M3 Lens-Based QA Sequence (L1059-1096)** — MANDATORY replacement for M1 (M1 deprecated, L1034-1045). 8 steps, EACH an explicit `- [ ]` item (L1096): (1) L6 aggregation, (2) structural rf-qa lens agents PARALLEL `fix_authorization:false`, (3) content rf-qa-qualitative lens agents PARALLEL, (4) domain lens agents if any, (5) findings consolidation → `${TASK_DIR}qa/qa-consolidated-findings.md`, (6) ONE fix agent `fix_authorization:true`, (7) ≥2 verification agents PARALLEL, (8) L5 conditional proceed / cycle. Steps 2+3 may share one parallel batch.
- **M4 Source-Fidelity Gate (L1098-1121; requirement I21 L759-788):** runs AFTER M3. Reads BOTH source inputs AND output; checks semantic coverage, detail preservation, cross-source contradiction, phantom coverage, operational/compliance completeness. Min 2 fidelity agents (I21 L784). MANDATORY for doc-from-source tasks (I21 L762-771). NOT required for pure mechanical transforms / config-only (I21 L773-775). **This task authors framework docs FROM the merged-requirements spec → M4 applies (source = spec).**
- **I19 agent-count floors (L699-741):** Final/assembled-output QA absolute minimum = **6 agents** (3 rf-qa structural + 3 rf-qa-qualitative content) for <500-line output; scales 8/10/12 by size (L706-711). Intermediate gates min **5 agents** (L731-737). FLOORS. 8 standard lenses L715-726. Adversarial framing required on every lens agent (L729).
- **I15 phase-gate enforcement (L635-651):** any task with 2+ execution phases MUST have ≥1 phase-gate QA checkpoint between primary execution and a dependent phase; gates <6 (final) / <5 (intermediate) agents are REJECTED at validation (L638). Every QA step its own `- [ ]` item (L651 — "No QA is implicit. No QA lives only in prose").
- **I20 Serialized Fix Authorization (L745-757):** any gate with 3+ agents on same file → report(all, fix_auth:false) → consolidate → ONE fix agent(fix_auth:true) → ≥2 verify → cycle. Parallel fix authorization PROHIBITED.
- **I17 Post-Completion Validation (L675-686):** before status→Done: (1) all `[ ]`→`[x]`, (2) all output files exist (Glob), (3) blockers have resolution notes, (4) if code modified → tests pass, (5) MANDATORY final lens-based QA per M3 on primary output, (6) M4 fidelity gate when source docs consumed.
- **I22 QA intensity (L793-841):** lite = 3 final / 2 intermediate; standard = 7 final / 3 intermediate; full = per-I19 floors. Serialized fix (I20) applies at ALL levels (L838). Default map: Quick/Lightweight→lite, Standard→standard, Deep/Heavyweight→full (L806-809).
- **I18 Testing (L688-697):** required ONLY if task creates/modifies SOURCE CODE (not docs/config). Uses L3 pattern. → **N/A here (no code); ADR-006 forbids a new test script.**

### 1f. Handoff / phase patterns (Section L, L901-1027)
L1 Discovery, L2 Build-from-Discovery, L3 Test/Execute, L4 Review/QA, L5 Conditional-Action, L6 Aggregation. Handoff files persist at `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/` (L909-921). Use template-02 (not 01) whenever items pass info via artifacts (L923-926).

---

## Step 2: Spec §4 + §10 + prep-cordinator "8 stages" + prep SKILL §5/§6 (verbatim state)

### 2a. Spec §4 — Stage 0 sub-steps + the STAGE 0..6 sequence (merged-requirements.md L67-99)
Stage 0 (Source Materialization) is inserted **before the current §3 two-track analysis**, owned by `prep-cordinator` (NATIVE, `laf_sha256=—`, body edits boundary-clean). Sub-steps (L72-84):
- **0.1 Inventory** — list raw inputs (sizes/exts/hashes); identify candidate sets; run `/source-fidelity` source-access declaration and **ABORT-on-NO-ACCESS FIRST** (unchanged discipline).
- **0.2 Detect mode** — §3 precedence → `input_mode` + `mode_confidence`.
- **0.3 Boundary/plan** — dispatch NEW NATIVE skill `chapter-materialize` (executed **inline in the coordinator's context**) → chapter plan: candidate boundaries, titles, order, per-boundary confidence, normalization events, omitted-matter dispositions. **No writes yet.**
- **0.4 Commit (gated)** — materialize **CERTAIN** chapters immediately as new `source/<slug>/ch-<NN>.txt`; retain raw under `source/<slug>/.raw/`; write `chapter-manifest.yaml`. Any **PROBABLE/UNCERTAIN/collision/mode-ambiguity** item → `ambiguous_split`, its `ch-NN.txt` write **deferred** to greenlight.
- **0.5 → gate** — deferred items injected into the existing **§5 question gate**; greenlight **cannot reach CONFIRMED** while any is unresolved; on confirm, coordinator commits deferred writes + sets `chapter-manifest.review.status: CONFIRMED`.

**Spec's STAGE 0..6 sequence table (L86-95) — the SPEC's remap of the prep SKILL §-sequence** (NOT the agent's stage numbers):
```
STAGE 0  materialize chapters + chapter-manifest.yaml            [NEW]
STAGE 1  §2 challenge taxonomy → 10-challenges.yaml              (unchanged)
STAGE 2  §3 two-track work-level analysis → 00/20               (unchanged; reads materialized set)
STAGE 3  §4 mapping → 30                                         (unchanged)
STAGE 4  §5 question gate  ← also receives Stage-0 ambiguous_splits   (EXTENDED)
STAGE 5  §6 greenlight     ← ratifies manifest; commits deferred writes (EXTENDED)
STAGE 6  §7 handoff / §8 traceability                            (unchanged)
```
Separation of concerns (L97-99): `chapter-materialize` owns boundary detection + normalization; `analyst` keeps its single-`source_path`, tier-invariant, ABORT-on-NO-ACCESS contract UNTOUCHED (it analyzes an already-materialized set; it does NOT detect boundaries).

### 2b. Spec §10 — Gate Integration (L223-232)
- **No new gate, no new HALT machinery.** Stage-0 `ambiguous_splits` + `needs_human_review` items fold into the existing §5 coverage-constrained question block (each ambiguous split = a `human_judgment_dimension: true`-equivalent input). Each allows `[skip] → DEFAULTED` in `70-traceability.md`.
- **Deferred-write safety invariant:** no `ch-NN.txt` for a PROBABLE/UNCERTAIN boundary is committed before the human resolves it. CERTAIN chapters commit immediately; the rest commit on greenlight-confirm.
- **Greenlight checklist +1 line:** *"chapter manifest ratified: count N; all UNCERTAIN boundaries and high-risk normalization losses resolved."* Greenlight CONFIRMED ⇒ manifest `review.status: CONFIRMED`.

### 2c. prep-cordinator.md "8 stages" block (agent body, verbatim numbering — L20, L44-98)
The agent body advertises an **8-stage pipeline** ("Owns the 8-stage prep pipeline", L20; "Load the `laf-adaptation:prep` skill and execute its 8-section procedure", L25). The "## The 8 stages" block (L44-62) is a fenced list numbered **STAGE 1 … STAGE 8**, each mapped to a prep SKILL §:
| Agent STAGE | Body label (L47-61) | Maps to prep SKILL § |
|---|---|---|
| STAGE 1 | RESEARCH (a require source_path; b /source-fidelity Phase-0 work-level NO-ACCESS→ABORT; c web-researcher→00) | §3 context track + source-access |
| STAGE 2 | ROADMAP (read 00 + §2 taxonomy skeleton → task list) | §2 |
| STAGE 3 | ANALYZE + CLASSIFY (analyst granularity=work →20; apply §2 taxonomy →10) | §3 text track + §2 |
| STAGE 4 | MAPPING (§4 → 30-mapping.yaml) | §4 |
| **STAGE 5** | **Q-GATE** (emit "## Questions for the user"; HALT; resume on reply) — **HALT gate #1** | §5 |
| STAGE 6 | PACKAGE (write 40 + 70; fold answers into 10/20/30) | §6/§7/§8 partial |
| **STAGE 7** | **GREENLIGHT** (write 50; HALT; on CONFIRM dual-form transform + promotion writes; PENDING→CONFIRMED) — **HALT gate #2** | §6 |
| STAGE 8 | HANDOFF (write 60-handoff-prompt.md; literal `/laf:rewrite --work <slug>`) | §7 |
Followed by "### Stage notes" (L64-98) with per-STAGE bullets that reference **"Stage 1 (a/b)", "Stage 1 (c) / Stage 3", "Stage 3 (+CLASSIFY)", "Stage 4", "Stage 5", "Stage 7", "Stage 7 (operator clarity)", "Stage 8"** by number. **These body references are the consistency hazard** — renumbering the header block without updating the notes breaks them.

**CRITICAL FINDING — three distinct numbering systems are in play:**
1. **prep-cordinator agent body:** STAGE **1..8** (Q-gate=STAGE 5, greenlight=STAGE 7). ← the numbers the builder physically edits.
2. **prep SKILL.md:** §**1..§8** (question-gate=§5, greenlight=§6). ← unchanged section labels.
3. **spec §4 table:** STAGE **0..6** (a re-map of the prep SKILL §-sequence, NOT the agent's stage numbers; its "STAGE 4 §5 question gate / STAGE 5 §6 greenlight" columns confirm it is indexing the SKILL §-sequence).
The spec's STAGE 0..6 table is a **conceptual pipeline view**, not an instruction to renumber the agent's 8-stage block to 0..6. Conflating the two is the trap the builder must avoid.

### 2d. prep SKILL.md §5 / §6 (verbatim — L76-108)
- **§5 Question-gate coverage rule (L76-85):** after §3-§4, emit `## Questions for the user` and HALT. MUST ask about every challenge whose governing rule has `human_judgment_dimension: true`; MUST NOT ask about deterministic rules (violence-level, death-euphemism). Each question allows `[skip] → DEFAULTED` in `70-traceability.md`. Gate = prompt block + halt (interrupt semantics; no runtime). **Spec §10 folds Stage-0 `ambiguous_splits` into THIS block** (each = a `human_judgment_dimension: true`-equivalent input).
- **§6 Greenlight (L87-108):** write `50-greenlight.md` (checklist: source-access declared, mapping confidence ceiling acknowledged, tier set confirmed, key decisions ratified); emit confirmation request; HALT until confirmed. On confirm: coordinator performs §3 dual-form transform + registers kb copy via `/kb-management`; status PENDING→CONFIRMED. **Spec §10 adds ONE checklist line** (manifest ratified) + on confirm commits the deferred `ch-NN.txt` writes and sets `chapter-manifest.review.status: CONFIRMED`.

---

## Step 3: RESOLVED authoring decision (research-notes gap #2) — Stage-0 numbering in prep-cordinator

**Two candidate approaches** (research-notes.md L61):
- **(A) New numbered STAGE 0** — insert a `STAGE 0 MATERIALIZE` before `STAGE 1 RESEARCH`, keeping the existing STAGE 1..8 labels intact. Pipeline becomes **0..8** (a 9-entry list; the "8 stages" prose becomes "9 stages").
- **(B) Sub-phase of STAGE 1 RESEARCH** — describe materialization as a Stage-1 sub-step (e.g. STAGE 1(0) or a new "Stage 1 (materialize)" bullet before the current 1(a)), leaving the STAGE 1..8 numbers and the "8 stages" prose unchanged.

### RECOMMENDATION: **Approach A — a new numbered STAGE 0 (prepended; the pipeline becomes STAGE 0..8, i.e. 9 stages).**

**Rationale (evidence-based):**
1. **Fidelity to the spec's own framing.** Spec §4 (L69) says Stage 0 is "**inserted before** the current §3 two-track analysis" and the spec table (L88) names it `STAGE 0 [NEW]` as a peer of the other stages, not a sub-bullet of research. The spec repeatedly calls it "**Stage 0**" (§1 L17, §4 header L67, §10 L226-229). Modeling it as a first-class numbered stage is the highest-fidelity rendering; burying it as a Stage-1 sub-bullet would understate a stage the spec treats as a peer with its own 0.1-0.5 sub-steps, its own HALT interaction (0.5→§5), and its own write-ownership rows.
2. **Preserves both HALT-gate references with a MECHANICAL, non-renumbering edit.** The two HALT gates are the load-bearing consistency risk (agent body L57=STAGE 5 Q-GATE, L57-60=STAGE 7 GREENLIGHT; "### Stage notes" reference "Stage 5" L80 and "Stage 7" L83, L91). **Prepending a STAGE 0 and keeping STAGE 1..8 unchanged means the Q-gate stays STAGE 5 and greenlight stays STAGE 7 — zero downstream renumber, zero body-reference breakage.** Approach A does NOT shift any existing number. (Contrast: renumbering to 0..7 — collapsing STAGE 8 or re-indexing — WOULD break every "Stage 5"/"Stage 7" note reference; that variant is rejected.)
3. **Separation of concerns is cleaner as a distinct stage.** Spec §4 L97-99 insists `chapter-materialize` (boundary detection) and `analyst` (STAGE 3 ANALYZE) stay separate contracts. A distinct STAGE 0 makes the boundary between "materialize the set" and "analyze the materialized set" structurally visible; folding materialization into STAGE 1 RESEARCH muddies it (RESEARCH is the web-context + source-access stage, a different concern).
4. **The `/source-fidelity` source-access declaration is a natural STAGE 0 opener** (spec §4 0.1 L73: "run the `/source-fidelity` source-access declaration and ABORT-on-NO-ACCESS first"). Today that ABORT lives in STAGE 1(b) (agent L48, L66-68). Moving materialization to STAGE 0 means the source-access/ABORT check most naturally leads STAGE 0 (0.1), and STAGE 1(b)'s work-level `/source-fidelity` Phase-0 stays as-is for the analysis track. The builder must ensure the STAGE 0 0.1 access-declaration and the STAGE 1(b) work-level Phase-0 are described as **the same discipline applied at two points** (materialization-input access, then analysis access), not a contradiction — a one-line reconciliation note in the Stage-0 paragraph handles this.

**Consistency contract the builder MUST honor when applying Approach A:**
- Change the two "8 stages"/"8-section procedure" prose mentions (agent L20 "the 8-stage prep pipeline", L22, L25 "8-section procedure" — note L25 refers to the **SKILL's** §-count which is still 8, so **leave L25 as "8-section procedure"**; only the **agent stage count** L20/L22 becomes 9). Verify each mention's referent before editing (skill §-count = 8, unchanged; agent stage-count = 9).
- Insert `STAGE 0 MATERIALIZE …` as the first entry of the fenced "## The N stages" block (agent L46-62), keeping STAGE 1..8 lines byte-identical.
- Add a `### Stage notes` bullet for **Stage 0** (mirroring the 0.1-0.5 sub-steps, the inline `chapter-materialize` dispatch, the deferred-write invariant, and the 0.5→Stage-5 gate hook) WITHOUT renumbering any existing "Stage N" note.
- In the STAGE 5 Q-GATE note (agent L80-82) add the spec §10 fold ("also receives Stage-0 `ambiguous_splits`") — this EXTENDS the existing STAGE 5, it does not renumber it.
- In the STAGE 7 GREENLIGHT note (agent L83-97) add: the +1 greenlight checklist line, the deferred `ch-NN.txt` commit-on-confirm, and `chapter-manifest.review.status: CONFIRMED` — EXTENDS STAGE 7, no renumber.
- Add the additive `skills:` line `- laf-adaptation:chapter-materialize` to frontmatter (agent L5-11) — additive only, boundary-clean per CLAUDE.md §2.

**Cross-artifact numbering note for the builder:** the prep SKILL.md keeps its §1..§8 labels UNCHANGED (spec §11 L241 only adds a "§1 Stage-0 note + pointer"). The spec's STAGE 0..6 table is a conceptual view and is NOT transcribed into either the agent or the skill as literal renumbering. Net: agent = STAGE 0..8 (9 stages); skill = §1..§8 (unchanged); spec table = 0..6 (conceptual only). Document this three-way mapping in the task so the builder edits each artifact in its own numbering system.

---

## Step 4: Recommended task PHASE breakdown for THIS task

Template 02 (Complex) is correct (research-notes.md L84). The task is **docs/prompt/YAML authoring FROM the merged-requirements spec** — no source code, no runtime. Below is the recommended phase map with per-phase QA-gate placement (I15) and parallelizability. (Files/edit-loci are owned by researchers 01/02/03; this section only sequences them into phases and maps the gates.)

### Phase 1 — Context load + prior-stage inputs (D3 / Phase-1 only; informational + read/verify items)
Per D3 (L286-289) the FIRST executable phase. Steps 1.2-1.4 embed the reads: the merged-requirements spec (§4/§5/§6/§10/§11/§12 loci), the MDTM template rules (this file), the boundary contract (`laf-adaptation/CLAUDE.md` §1-§2), the path-contract, VENDOR.md row format, and `check_boundary.py` classify()/Rule-E/Rule-F mechanics. These are B2 self-contained "read X to extract Y, then write a consolidated context/inventory file at phase-outputs/discovery/…" items (L1/L2 pattern), NOT standalone reads (B5). **This phase is where the three-way numbering map (Step 3) and the 8-file BOM get materialized as a discovery artifact the later authoring items consume.**

### Phase 2 — Author the NEW `chapter-materialize` skill (independent authoring core)
Per A3, one B2 item per file:
- P2.1 `laf-adaptation/skills/chapter-materialize/SKILL.md` (split/normalize/adopt procedure; §6 multi-signal layers, §7 failure-mode table, §8 normalization, confidence rule).
- P2.2 `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml` (declarative signal ruleset).
- P2.3 mirror both to `.claude/skills/chapter-materialize/` (lockstep, spec §11 L249) — **depends on P2.1+P2.2** (sequential after them).
- **Parallelism:** P2.1 and P2.2 are INDEPENDENT of each other → parallelizable (F2a parallel-spawn exception, L447). P2.3 is sequential (reads P2.1/P2.2 outputs).

### Phase 3 — Wire the skill into agent / skill / command (integration edits)
- P3.1 prep-cordinator.md: additive `skills:` line + STAGE 0 block + Stage-0 note + STAGE 5/STAGE 7 extensions (Step 3 contract) → mirror to `.claude/agents/prep-cordinator.md`.
- P3.2 prep SKILL.md §1 Stage-0 note + `chapter-materialize` pointer (§1..§8 labels unchanged) → mirror to `.claude/skills/prep/SKILL.md`.
- P3.3 `.claude/commands/laf/prep.md`: add `--source-mode auto|folder|file|adopt`; note `--source` may resolve to dir/file/adopt-set (delegates to prep-cordinator; does NOT restate pipeline). [command is already the `.claude/` mirror surface per research-notes L22.]
- **Parallelism:** P3.1, P3.2, P3.3 edit THREE DIFFERENT files with no data dependency between them → parallelizable. Each depends on Phase 2 existing (the skill it references must be authored first) → **Phase 3 is sequential AFTER Phase 2**, but its items are mutually parallel.

### Phase 4 — Path-contract / source docs / VENDOR manifest (contract + provenance edits)
- P4.1 path-contract.md: §4 explanatory note (manifest NOT in read-set; **§4 read-set byte-unchanged**), §5 +3 write-ownership rows, NEW §6 "Source-side chapter manifest" (spec §12 L251-263) → mirror to `.claude/` if the prep mirror carries `resources/` (open question gap #1 — researcher 01 resolves).
- P4.2 `laf-adaptation/source/README.md`: +manifest + `.raw/` subsection.
- P4.3 `laf-adaptation/VENDOR.md`: +1 NATIVE row `| skills/chapter-materialize/** | NATIVE | — | — |` (U+2014 em dash; NATIVE `/**` glob row, NOT per-file) placed in the NATIVE group.
- **Parallelism:** P4.1, P4.2, P4.3 edit three different files, no interdependency → parallelizable. Phase 4 depends on Phase 2 (VENDOR row + path-contract reference the new skill dir) → sequential after Phase 2; can run in parallel with Phase 3 in principle, but recommend **serial Phase 3 → Phase 4** to keep the phase-gate QA boundaries clean (I15 wants a clean primary-execution→dependent-phase seam).

### Phase 5 — VALIDATION (boundary + invariants; NOT a test phase)
Per research-notes L86-87, TESTING_REQUIREMENTS = **NONE** (ADR-006 forbids new test scripts; I18 testing gate does NOT apply — no source code modified). The AC6 `check_boundary.py` run is a **VALIDATION item** (L3-shaped execute item capturing exit code), not a unit test:
- P5.1 (L3 execute) run `uv run python scripts/check_boundary.py` **from cwd `laf-adaptation/`** and capture exit code → `phase-outputs/test-results/`; PASS criterion = **exit 0** (Mode V green). [exact cmd/cwd = researcher 02.]
- P5.2 (L4 review) verify `rewrite_phase_reads` (path-contract §4) is byte-unchanged; no 9th numbered package file exists; no second script added; `check_boundary.py` byte-unchanged; `.claude/` mirror parity; AC1-AC7 walkthrough.
- P5.3 (L5 conditional) IF exit≠0 or any invariant fails → fix plan; ELSE proceed.
- **Parallelism:** P5.1 must precede P5.2/P5.3 (they read its result) → sequential within phase.

### Phase 6 — FINAL QA gate + POST reflect + Post-Completion (I15/I17)
**QA_GATE_REQUIREMENTS = FINAL_ONLY** (research-notes L86): a single final-document M3 lens-based QA gate over the assembled output (all edited/new bodies + manifest schema authored), min **6 agents** (3 rf-qa structural + 3 rf-qa-qualitative content per I19 <500-line floor L708). Because the outputs are derived FROM the merged-requirements spec, **M4 source-fidelity gate applies** (I21 L771 "any task where the orchestrator reads source documents to produce output"; source = merged-requirements.md, min 2 fidelity agents L784) — recommend a domain lens on **boundary-contract compliance + AC1-AC7 coverage**. Serialized fix (I20). Then POST reflect subagent (`reflect_post_mode: skill`, research-notes L88) → record `reflect_post`. Then Post-Completion Actions (I17): confirm all `[ ]`→`[x]`, all outputs exist via Glob, blockers resolved, then frontmatter status→`🟢 Done` + completion_date + Execution Log entry.

### Independence / parallelism summary
| Phase | Depends on | Internal items parallel? |
|---|---|---|
| P1 context/inventory | — | reads parallel; consolidation last |
| P2 author skill | P1 | P2.1 ∥ P2.2 (independent); P2.3 mirror sequential |
| P3 wire agent/skill/cmd | P2 | P3.1 ∥ P3.2 ∥ P3.3 (three files, no dep) |
| P4 contract/source/VENDOR | P2 | P4.1 ∥ P4.2 ∥ P4.3 (three files, no dep) |
| P5 validation | P2,P3,P4 | sequential (result-chained) |
| P6 final QA + reflect + done | P5 | M3 lens agents ∥; fix serialized (I20) |

**Gate placement (I15):** exactly one phase-gate is required between the primary authoring phases and the validation/completion phase. Given FINAL_ONLY, place the mandatory M3+M4 gate at **Phase 6** (post-completion, per I17.5/I17.6), covering the full assembled output. No intermediate per-phase gates (avoids the double-QA overkill the research-notes flag for doc authoring). qa_intensity: the task is **Deep** tier → default `full` (I22 L809), but since it is doc/prompt authoring with a small assembled surface, **standard (7 final-gate agents)** is a defensible reduction; recommend **full-floor 6+ agents** to honor the boundary-contract criticality (the release-blockers §14 are safety-grade). Builder picks; both satisfy the ≥6 floor.

---

## Step 4a: Concrete recommendations (for the builder / task-builder skill)
- **MDTM template:** `02` (Complex), GLOBAL path `/config/.claude/templates/workflow/02_mdtm_template_complex_task.md` (project has NO local copy — research-notes L39-40).
- **QA_GATE_REQUIREMENTS = FINAL_ONLY**; final M3 gate min **6 agents** (3 rf-qa + 3 rf-qa-qualitative) + **M4 fidelity gate** (source = merged-requirements.md, min 2 agents) + a domain lens on boundary-contract/AC coverage. Serialized fix (I20). Every gate step an explicit `- [ ]` item (I15 L651).
- **TESTING_REQUIREMENTS = NONE.** No source code is modified (I18 N/A); ADR-006 forbids a new test script. The `check_boundary.py` run is a VALIDATION (L3) item, not a unit test.
- **POST_REFLECT_GATE = ENABLED**, `reflect_post_mode: skill`; SPEC_PATH (frontmatter `spec_path`) = `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md`.
- **`task_type: static`**, `type: 📚 Documentation`.
- **Stage-0 numbering:** Approach **A** (new numbered STAGE 0; agent pipeline → STAGE 0..8 / 9 stages; Q-gate stays STAGE 5, greenlight stays STAGE 7; prep SKILL §1..§8 unchanged; spec's STAGE 0..6 table is conceptual only).

---

**Status: Complete**
