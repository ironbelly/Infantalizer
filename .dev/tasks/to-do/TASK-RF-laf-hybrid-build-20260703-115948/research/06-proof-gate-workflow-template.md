# Research: Phase-3 Proof Gate + 11-Step Workflow + MDTM Template
**Topic type:** Data Flow Tracer + Template & Examples
**Scope:** 11-step workflow, safety loop, fan-out, Phase-3 hard gate, proof-chapter, MDTM Template 02 rules
**Status:** Complete
**Date:** 2026-07-03

**Summary:** Documented (1) the full 11-step per-chapter workflow with per-step provenance/READS/WRITES (§1), (2) the safety revision loop — CWS loop + native safety-verifier FAIL trigger, no adopted file edited (§2), (3) multi-tier fan-out — analyst once/chapter, tier-coordinator fans steps 3-9 across T1/T3/T5, parallel default / sequential G2 fallback (§3), (4) proof-chapter provisioning — NO source chapter exists; recommended external execution-time input (primary) or public-domain stand-in (committable fallback), with an explicit Tolkien-copyright flag; only `tolkien_mapping.yaml` (a mapping config, not prose) exists (§4), (5) the Phase-3 HARD GATE deliverable + its 5 conditions encoded as L3/L4/L5/L6 verification items (§5), and (6) the MDTM Template 02 PART 1 rules (A3, A4, B2, C, E2/E3 anti-orphaning, L1-L6 handoffs, M3 gates) with line cites (§6). KEY FLAGS: the MDTM template is NOT at `.claude/templates/...` — resolved to the pipx path `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/templates/workflow/02_mdtm_template_complex_task.md`; no prior TASK-* examples exist; no `source/`/chapter fixtures exist.
---

## 0. Resolved paths & key corrections (read first)

- **DESIGN.md actual path:** `.dev/releases/current/0.1/design/DESIGN.md` (relative to repo root `/config/workspace/Infantalizer`). Confirmed present (23,691 bytes). Cited below as `DESIGN.md:<line>`.
- **MDTM Template 02 — PATH CORRECTION:** The brief's path `.claude/templates/workflow/02_mdtm_template_complex_task.md` **does not exist** (no `.claude/templates/` dir in this repo; the repo's only `templates/` dir holds `work_mapping_template.yaml`). The real, resolved template lives in the installed SuperClaude package:
  - **Canonical:** `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/templates/workflow/02_mdtm_template_complex_task.md`
  - (identical copies under `.../_src/superclaude/templates/workflow/` and many `/config/.cache/uv/archive-v0/*/`)
  - **Builder action:** set frontmatter `template_schema_doc` to the canonical pipx path, OR reference the source-of-truth `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` convention from global CLAUDE.md. Flag that the literal `.claude/...` path is stale.
- **Prior TASK-* examples in `.dev/tasks/to-do/`:** NONE except this task's own folder (`TASK-RF-laf-hybrid-build-20260703-115948/`). No other `TASK-*` example folders exist to copy from. (Peer research files 01-05 from R1-R5 are present in this folder's `research/` subdir.)
- **Tolkien source chapter text:** NO `source/<work>/ch-NN.txt` or any `*.txt` chapter fixture exists anywhere in the repo. The only Tolkien artifact is a **mapping config** (not chapter prose): `config/concept_mapping/templates/tolkien_mapping.yaml` (LotR character/concept/scene tier translations). See §4 for provisioning.

---

## 1. The 11-Step Per-Chapter Workflow (DESIGN.md §3, `DESIGN.md:158-209`)

Source unit: `source/<work>/ch-<NN>.txt` (read-only reference, `DESIGN.md:164`). Steps labeled by provenance `[NATIVE / ADOPTED / BUILD-NEW]`.

| # | Step / Agent | Provenance | READS | WRITES |
|---|---|---|---|---|
| 1 | `analyst` | **NATIVE** | source chapter, `/source-fidelity` | `work/analysis/ch-<NN>.yaml` (CERTAIN/PROBABLE/UNCERTAIN tags) `DESIGN.md:167-171` |
| — | *Phase-0 ABORT gate* (inside analyst) | NATIVE | SOURCE ACCESS status | HALT if `SOURCE ACCESS = NO ACCESS` (constraint #2) `DESIGN.md:170` |
| 2 | `muse` | **ADOPTED** | `work/analysis`, `kb/tiers/tier_N`, `kb/adaptation-mapping` | scene brief (in-session; **NOT persisted to kb**) `DESIGN.md:173-175` |
| 3 | `writer` | **ADOPTED + NATIVE skill** | brief, `/adaptation-rules` (adaptation mode), `kb/tiers/tier_N` | `work/drafts/ch-<NN>-t<N>-v1.md` `DESIGN.md:177-180` |
| 4 | `critic ×N` | **ADOPTED** | draft (parallel focus areas; adaptation-quality) | `work/critique-reports/` `DESIGN.md:183` |
| 5 | `editor` | **ADOPTED** | draft | editorial memo (priority order) — **never folded (G3)** `DESIGN.md:184` |
| 6 | `writer` revision | **ADOPTED** | critique + editorial memo | `work/drafts/ch-<NN>-t<N>-v2.md` `DESIGN.md:185` |
| 7 | `continuity-checker` | **ADOPTED** | revised draft, `kb/adaptations/<work>/tier-N` | canon-contradiction report `DESIGN.md:186` |
| 8 | `safety-verifier` | **NATIVE** | revised draft, `/adaptation-safety`, `kb/tiers/tier_N` | `work/safety-reports/ch-<NN>-t<N>.md` → verdict `{PASS\|FAIL}`. MANDATORY Tier 1-2; runs AFTER continuity (constraint #3) `DESIGN.md:189-192` |
| — | *FAIL branch* | NATIVE trigger | verdict FAIL | → **back to step 3** (revision loop; blocks promotion) `DESIGN.md:193` |
| 9 | `reader-sim` | **ADOPTED** | draft, tier `developmental_basis` persona | felt-experience report (after convergence) `DESIGN.md:196-198` |
| 10 | `tier-coordinator` | **BUILD-NEW** | every `tier-N adapted.md` for this chapter | cross-tier consistency report (parallel default; sequential fallback G2) `DESIGN.md:200-203` |
| 11 | `chronicler` | **BUILD-NEW** | accepted outputs | ON **muse-accept only** (work→kb promotion, constraint #5): `kb/canon/`, `kb/timeline/`, `kb/adaptations/<work>/tier-N/continuity.md` (per-tier, graft G1), `.../chapters/ch-NN/canon-delta.md` `DESIGN.md:205-208` |

**Provenance tally (workflow agents):** NATIVE = analyst(1), safety-verifier(8); ADOPTED = muse(2), writer(3,6), critic(4), editor(5), continuity-checker(7), reader-sim(9); BUILD-NEW = tier-coordinator(10), chronicler(11). Writer(3) is ADOPTED body + NATIVE `/adaptation-rules` skill via `skills:` frontmatter only (constraint #6, `DESIGN.md:48-50`).

**Quartet note (constraint #4 / invariant G3, `DESIGN.md:84-95, 182-187`):** Steps 4-5-7-9 (critic, editor, continuity-checker, reader-sim) are the **four distinct adopted review agents** — none folded. `safety-verifier` (step 8) is the **fifth, native** reviewer, never merged into the quartet.

## 2. The Safety Revision Loop (DESIGN.md §3.1, `DESIGN.md:211-224`)

The loop cycle (`DESIGN.md:213-220`):
```
writer(3) → critic/editor(4-5) → writer revise(6) → continuity(7) → safety-verifier(8)
   ▲                                                                        │
   └───────────────── FAIL (blocks promotion) ──────────────────────────────┘
                                  │ PASS
                                  ▼
                      reader-sim(9) → tier-coordinator(10) → chronicler(11)
```

**Two-provenance decomposition (the key claim, `DESIGN.md:222-224`):**
- The **loop is CWS's** — the writer→critic→writer revision cycle already exists in the adopted machinery.
- The **trigger is LAF's** — a `safety-verifier` FAIL verdict is what re-enters the loop.
- **No adopted file is edited** to wire this: the trigger lives *entirely* in the native `safety-verifier` agent's body. (This is the loop "LAF lacked," constraint #3, `DESIGN.md:211`.)

**Builder implication:** the proof run's integration test must be able to *exercise* the loop (a FAIL that returns to step 3), or at minimum assert the loop wiring exists in `safety-verifier`. A clean PASS on first pass does not prove the FAIL→step-3 edge; encode a verification item that the FAIL branch is present in the agent body even if the proof chapter passes safety on the first attempt.

## 3. Multi-Tier Fan-Out (DESIGN.md §3.2, `DESIGN.md:226-238`)

- `analyst` runs **once per source chapter** — tier-invariant source truth; its output is shared across all tiers (`DESIGN.md:228-233`).
- `tier-coordinator` then **fans the transform across tiers**; each tier runs pipeline **steps 3-9** independently (`DESIGN.md:232-234`).
- Fan-out topology (`DESIGN.md:231-238`):
```
                   ┌──► tier-1 pipeline (steps 3-9) ──┐
analyst ch-NN ─────┼──► tier-3 pipeline (steps 3-9) ──┼──► tier-coordinator ──► chronicler ×tier
(once, shared)     └──► tier-5 pipeline (steps 3-9) ──┘   reconcile source-canon,
                                                           tier-differentiated framing
```
- **DEFAULT: parallel fan-out** (`DESIGN.md:236`).
- **FALLBACK (graft G2): sequential** — for state-heavy works where tier-N canon must settle before tier-N+1 (`DESIGN.md:237`).
- `chronicler` runs **per tier** ("×tier"), writing each tier's `continuity.md` + `canon-delta.md` (graft G1) — see step 11 above.

**Note:** T4 is interpolated (not a distinct profile) — `kb/tiers/` holds tier_1/2/3/5 profiles, "T4 interpolated" (`DESIGN.md:134`). The proof gate uses **T1, T3, T5** (see §5), consistent with the fan-out example.

## 4. Proof-Chapter Provisioning (the hard-gate input)

**Current state (evidence):**
- No `source/` directory exists in the repo. DESIGN.md §2 declares `source/` as a **BUILD-NEW** dir: "the work being adapted (read-only reference)" (`DESIGN.md:126`). It is created at build time, not pre-populated.
- No `*.txt` chapter fixtures exist anywhere (searched repo-wide).
- The only Tolkien asset is `config/concept_mapping/templates/tolkien_mapping.yaml` — a **mapping config** (character/concept/scene → tier translations for LotR), NOT chapter prose. It is usable as `<work>-mapping.yaml` seed data (`DESIGN.md:251`, kb/adaptation-mapping cascade) but does **not** supply the `ch-NN.txt` prose the analyst (step 1) reads.

**LICENSING FLAG (must surface in the task):** J.R.R. Tolkien's *The Lord of the Rings* / *The Hobbit* are **NOT public domain** (still under copyright in most jurisdictions; US expiry not until well after 2026). The task **must not** bundle verbatim Tolkien prose as a committed fixture. The Phase-0 ABORT gate (`DESIGN.md:170`, constraint #2) explicitly HALTs when `SOURCE ACCESS = NO ACCESS`, so the framework is designed to treat source prose as an external/provisioned input, not a shipped artifact.

**Recommended provisioning (lightest correct approach — ranked):**
1. **PREFERRED — execution-time input (self-contained framework, external chapter):** Task creates the empty `source/<work>/` dir + a `source/README.md` documenting the expected `ch-NN.txt` contract (encoding, one chapter per file). The proof-run item instructs the executor to place a **short single chapter of the actual work under adaptation** at `source/<work>/ch-01.txt` at execution time (the human operator supplies it under their own access rights). This honors user decision #1 ("Phase 0 acquires upstream CWS first" + self-contained-where-reasonable) without committing copyrighted text. The 11-step run is then driven against that file.
2. **ALTERNATIVE — public-domain stand-in for the mechanism proof:** Use a short **public-domain** narrative excerpt (e.g., a Grimm/Andersen fairy-tale chapter, or a Tolkien-adjacent public-domain source such as the Kalevala / Norse Eddas / Beowulf which influenced Tolkien) as `source/<work>/ch-01.txt` purely to prove the *pipeline mechanics* (all 11 steps run, tags emitted, safety PASS, per-tier canon written). The gate tests **integration wiring**, not Tolkien-specific fidelity, so a PD stand-in fully satisfies the 5 gate conditions. This keeps the task fully self-contained and committable.
   - `tolkien_mapping.yaml` can still seed `kb/adaptation-mapping/<work>-mapping.yaml` to exercise the mapping cascade if the LotR work label is used, but the *prose* source stays PD or externally supplied.
3. **NOT RECOMMENDED:** committing real Tolkien chapter text as a fixture — copyright risk; avoid.

**DESIGN.md phrasing to honor:** §7 Phase-3 deliverable says "one **Tolkien** chapter" (`DESIGN.md:296`) and §6 says "a real Tolkien chapter" (`DESIGN.md:282`). Reconcile by: label the `<work>` as the Tolkien work and seed the mapping from `tolkien_mapping.yaml`, while the **prose file itself** is provisioned per option 1 (external, execution-time) — real Tolkien text supplied by the operator under their own rights — with option 2 available as a committable fallback proof. **Flag this reconciliation explicitly in the task's Open Questions / Key Constraints.**

## 5. Phase-3 HARD GATE (DESIGN.md §7, `DESIGN.md:296`; risk framing `DESIGN.md:282`)

**Phase label:** "3. Compose & prove (HARD GATE)".

**Deliverable (the integration test, `DESIGN.md:296`):**
1. Run the **full 11-step workflow on ONE Tolkien chapter at Tier 1**.
2. Then run the **same chapter at Tiers 1/3/5 through `tier-coordinator`**.

**The 5 GATE conditions (verbatim from `DESIGN.md:296`, separated by `·`):**
1. **v2.0 tags present** — analyst output (`work/analysis/ch-NN.yaml`) carries CERTAIN/PROBABLE/UNCERTAIN tags (v2.0 Pragmatic Verification Protocol via `/source-fidelity`).
2. **safety PASS** — `safety-verifier` verdict = PASS (mandatory Tier 1-2; `work/safety-reports/ch-NN-tN.md`).
3. **per-tier canon written** — `kb/adaptations/<work>/tier-N/continuity.md` (+ `chapters/ch-NN/canon-delta.md`) exists for each tier run (chronicler on muse-accept, graft G1).
4. **all four quartet agents ran** — critic, editor, continuity-checker, reader-sim each executed (constraint #4 / G3; safety-verifier is the distinct 5th).
5. **`check_boundary.py` green** — boundary contract passes: adopted agent bodies byte-identical to `VENDOR.md` manifest hashes (constraint #6; see R5's boundary-script research).

**Encode each as an explicit verification checklist item (per MDTM I15 / M3 — see §6).** Suggested integration-test structure using L-series patterns:
- **L3 (Test/Execute):** run the T1 full 11-step pipeline; capture per-step outputs + a run-summary.
- **L3 (Test/Execute):** run the same chapter at T1/T3/T5 through `tier-coordinator`; capture cross-tier report.
- **L4 (Review/QA) ×5:** one verdict item per gate condition (1-5 above), each producing PASS/FAIL against concrete artifact paths.
- **L6 (Aggregation):** consolidate the 5 condition verdicts into a single **Phase-3 gate report**; gate is GREEN only if all 5 = PASS. If any FAIL → HALT (this is the "hard gate": 0.1 is not "done" until all 5 pass, `DESIGN.md:308`).

## 6. MDTM Template 02 — PART 1 Rules the Builder MUST Obey

**Resolved template path:** `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/templates/workflow/02_mdtm_template_complex_task.md`. PART 1 (build instructions) = lines 64-1131; PART 2 (the task-file template to copy) = lines 1139-end. Line cites below are into this file (`02:<line>`).

### 6.1 Section A — Workflow integration & granularity
- **A1 (`02:89-100`) Workflow-doc availability:** check for a governing workflow doc first. For THIS task the governing "workflow" is **DESIGN.md §3 + §7**, so all `[WORKFLOW-DEPENDENT]` sections apply — treat DESIGN.md phases 0-4 as the governing workflow, map every phase/gate to task elements.
- **A2 (`02:102-106`) Deep integration:** extract EVERY requirement/phase/step/quality-standard from DESIGN.md; map each to a task element; include ALL its verification criteria (i.e., the 5 gate conditions) in the task's verification section.
- **A3 (`02:108-112`) COMPLETE GRANULAR BREAKDOWN:** break EVERY phase into atomic, verifiable checklist items; **create an individual checklist item for EVERY file / component / iteration**; NO high-level/bulk operations; include exact file paths + measurable outcomes. → For LAF this means: one item per adopted-agent copy, one per native skill authored, one per build-new agent, one per kb layer file, etc. (cross-ref R1 file inventory).
- **A4 (`02:114-133`) ITERATIVE PROCESS STRUCTURE:** for any multi-item process: (X.1) pre-enumerate ALL items in an initial step → (X.2) one checklist item per specific item → (X.3) a consolidation step ONLY after all items complete. Use for: enumerating the 13 adopted files to vendor, the per-tier proof runs (T1/T3/T5), the 5 gate conditions.
- **A5 (`02:135-139`) Cross-stage integration:** every phase must explicitly name inputs from prior phases (exact paths) and validate against prior-stage findings. → Phase 1 reads Phase 0's `VENDOR.md`; Phase 3 reads Phases 0-2 outputs.
- **A6 (`02:141-145`) Workflow-compliance enforcement:** reference specific DESIGN.md sections throughout; copy quality standards (the 5 gate conditions) directly.

### 6.2 Section B — Self-contained checklist items (CRITICAL)
- **B1 (`02:151-157`) Why:** batch execution across session rollovers means context from batch 1 is GONE by batch 3+. Standalone "read context" items are USELESS.
- **B2 (`02:159-165`) EVERY item = a complete self-contained prompt with 6 elements:**
  1. **Context Reference with WHY** — which file(s) to read and why.
  2. **Action with WHY** — what to do and why.
  3. **Output Specification** — exact output file path/name, content, template to follow.
  4. **Integrated Verification** — an "ensuring…" clause; derive ALL content from referenced source files, 100% accuracy, no fabrication, document negative evidence on failure.
  5. **Evidence on Failure Only** — log to task notes ONLY if blocked/errored (success is evidenced by the output file).
  6. **Explicit Completion Gate** — "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete."
- **B3 (`02:167-170`) Format:** ONE full paragraph per item (not bullets/multi-line), verbose, executable independently.
- **B4 (`02:172-179`) Correct example** = action + verification integrated; do NOT create separate verification items.
- **B5 (`02:181-200`) FORBIDDEN:** standalone "read context" items; missing context reference; multi-line/bulleted items; separate verification/confirmation items; overly-granular items ("create directory" alone — combine with the file that needs it); separate REMINDER blocks between items.
- **B7 (`02:206-213`) Key principles:** each item is a complete independent prompt; context + verification embedded IN the action; output files = evidence; log only on FAIL; one verbose paragraph; QA process (I15-I16) handles verification between batches.

### 6.3 Section C — Embed, don't sectionize (`02:216-247`)
- **C1** outputs/deliverables embedded in the item that creates them (no "Outputs" section). **C2** success criteria embedded as the "ensuring…" clause (no "Success Criteria" section). **C3** verification embedded in action items (no separate "Verification Checklist" section). **C4 (`02:242-247`) TASK COMPLETION** handled only by the **Post-Completion Actions** section (frontmatter status/completion_date update + Execution Log entry); post-completion validation items (I17) handle output verification.

### 6.4 Section E — Checklist structure & phase-dependency ordering (`02:291-383`)
- **E1 (`02:295-309`):** every actionable item is a flat `- [ ]` checkbox; **NO nested checkboxes**; **NO parent checkboxes summarizing children**; each is ONE atomic verifiable action; use bold `**Step X.Y:**` headers for grouping (never checkboxes on step headers); items in exact completion order.
- **E2 (`02:311-365`) Anti-orphaning / ordering (the load-bearing rule):** **summary/parent checkboxes MUST come AFTER all their component items**; NEVER a parent before its children; components completed BEFORE summaries; use descriptive headers not parent checkboxes. Work flows TOP→BOTTOM only.
- **E3 (`02:367-383`) Sequential order:** checkboxes in exact completion order; never require marking items above current position; each phase completes ALL its checkboxes before the next; FORBIDDEN: "see below", "return to phase", any backward movement.
- **Phase-dependency ordering (implication for LAF):** because Phase 3 consumes Phases 0-2 outputs and Phase 4 documents the synced tree, encode phases in strict `0 → 1 → 2 → 3 → 4` order; the **completion / gate items land in the FINAL phase / Post-Completion** (anti-orphaning: the Phase-3 gate-report aggregation and the frontmatter-completion item are LAST, never earlier). No forward references.

### 6.5 Section L — Intra-task handoff patterns (complex/subagent tasks) (`02:904-1026`)
Handoff files persist on disk under `.dev/tasks/TASK-NAME/phase-outputs/{discovery,test-results,reviews,plans,reports}/` across all batches (`02:909-921`). Use when later items depend on earlier items' outputs (else use Template 01).

| Pattern | When | Key rule | Cite |
|---|---|---|---|
| **L1 Discovery** | explore codebase/env/data → structured findings | the discovery FILE is the deliverable; later items read it by path | `02:928-938` |
| **L2 Build-from-Discovery** | create output using a prior discovery file | reference BOTH the discovery file path AND the source file path | `02:940-950` |
| **L3 Test/Execute** | run command/script/test suite | capture BOTH raw output AND a structured summary | `02:952-962` |
| **L4 Review/QA** | assess a prior output vs source/spec | produce a structured PASS/FAIL verdict with specific findings (never "looks good") | `02:964-974` |
| **L5 Conditional-Action** | behavior depends on a prior result | MUST handle BOTH branches (success AND failure); always create the output file | `02:976-988` |
| **L6 Aggregation** | consolidate many outputs → one report | use Glob to discover files dynamically (don't hardcode); typically final item of a phase | `02:990-1000` |
| **L7 selection guide** | — | table + common phase structures (Discovery→Build→Review; Build→Test→Fix; Full Lifecycle w/ QA gates) | `02:1002-1026` |

**Direct mapping to LAF Phase-3 proof (see §5):** the 11-step run = **L3**; each of the 5 gate conditions = **L4**; branch on FAIL (loop/HALT) = **L5**; the consolidated Phase-3 gate report = **L6**. Vendoring enumeration in Phase 0 = **L1**; building native/greenfield files from specs = **L2**.

### 6.6 Section M — Phase-gate QA (`02:1028-1120`, applies at phase boundaries)
- **M3 Lens-Based QA (mandatory; M1 deprecated, `02:1034-1096`):** at each phase gate spawn parallel structural (rf-qa) + content (rf-qa-qualitative) lens agents (`fix_authorization: false`), consolidate findings (Step 5), ONE fix agent with `fix_authorization: true` (Step 6), parallel verification round (Step 7), conditional proceed w/ max cycles (Step 8). **EVERY step = an explicit `- [ ]` item; do NOT collapse (`02:1096`).**
- **M2 applicability (`02:1047-1057`):** this LAF build is a **code-modifying / integration task** → gates after implementation phases, M3 lens-based (min 6 agents per I19). If any files derive from spec docs (DESIGN.md companion specs), a **fidelity gate (M4, `02:1098+`)** also applies.

### 6.7 Frontmatter field for the builder (`02:1-61`)
- **`template_schema_doc` (`02:47`)** — set to the resolved template path (§0). Other builder-populated fields: `id` (`TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS`), `spec_path` (→ `.dev/releases/current/0.1/design/DESIGN.md`), `depends_on`, `related_docs` (the 6 companion specs), `type` (🧩 Integration or ✨ Feature), `parent_task`. **D3 (`02:286-289`): NO checklist items before Phase 1** — frontmatter → Workflow Compliance (informational) → Prerequisites (informational) → Phase 1 (first executable items).

---

## 7. Summary for the task-builder (actionable)

1. **Workflow (§1):** encode the 11 steps as the per-chapter pipeline; each step's agent, provenance, READS, WRITES are in the §1 table with DESIGN.md line cites. Writer(3) gains adaptation mode via `skills:` frontmatter only.
2. **Safety loop (§2):** loop is CWS's, trigger is native `safety-verifier` FAIL→step-3; no adopted file edited. Verify the FAIL edge exists even if the proof chapter passes first try.
3. **Fan-out (§3):** analyst once/chapter (tier-invariant); tier-coordinator fans steps 3-9 across T1/T3/T5; parallel default, sequential G2 fallback; chronicler per tier.
4. **Phase-3 hard gate (§5):** deliverable = full 11-step T1 run + same chapter T1/3/5 via tier-coordinator. Encode the **5 conditions** (v2.0 tags · safety PASS · per-tier canon · all 4 quartet ran · check_boundary.py green) as explicit L4 verdict items + an L6 gate-report aggregation; GREEN requires all 5 PASS, else HALT (definition of "0.1 done").
5. **Proof chapter (§4):** none exists. Recommend option 1 (external, execution-time `source/<work>/ch-01.txt`) as primary, option 2 (public-domain stand-in) as committable fallback. Seed mapping from `config/concept_mapping/templates/tolkien_mapping.yaml`. **Flag the Tolkien copyright constraint — do NOT commit real Tolkien prose.**
6. **MDTM rules (§6):** obey A3 (granular per-file items), A4 (enumerate→per-item→consolidate), B2 (6-element self-contained paragraph items), C (embed outputs/verification), E2/E3 (parent/summary AFTER children; strict top→bottom; no forward refs; completion items in final phase), L1-L6 handoff patterns for the discovery/build/test/review/conditional/aggregate items, M3 lens-based QA at phase gates. Set `template_schema_doc` to the resolved pipx path (§0). No checklist items before Phase 1 (D3).

**Path resolution flags for the builder:** (a) MDTM template is NOT at `.claude/templates/...` — use the resolved pipx path; (b) no prior TASK-* examples exist to copy; (c) no `source/` or chapter fixtures exist — must be provisioned per §4.
