# T1 Reflection Card — PRE reflect gate (UC-1)

**Reviewer frame:** executor-disjoint (no executor model class in reviewer pool)
**Mode:** pre (spec-coverage / spec-literal-correctness audit of tasklist vs DESIGN.md)
**Calibration target:** blind (this card graded by confidence-calibrator without formation context)

## Dimension 1 — Citation grounding (spec refs in tasklist)

Every build step in the tasklist cites a verifiable spec section with line numbers. Sampled:
- Step 2.2 → boundary-contract.md §3 (lines 92-167): rules A-F pseudocode
- Step 3.8 → agent-schemas.md §2.1 (lines 42-77): analyst frontmatter + ABORT block
- Step 4.2 → tier-coordinator.md §1-§6 (FULL): reconcile checks A/B/C
- Step 5.3 → DESIGN.md §3 (lines 158-209): 11-step workflow

The tasklist's `related_docs` frontmatter block (lines 26-39) maps every companion spec to its load-bearing role. The References section (lines 110-116) re-cites the same with section-level granularity. Citation density is exceptionally high — each of the 58 Steps opens with a "Read X.md §Y (lines A-B)" directive.

**Grounding assessment:** STRONG. No uncited build action; no fabricated spec references. The "Read before write" pattern is enforced per-step.

## Dimension 2 — Coverage completeness

See coverage-matrix.md. All 16 parsed requirements (§7 Phase gates + §5 constraints + §1.1 inventory + §3 11-step + §4 invariants) and all 29 inferred requirements map to ≥1 tasklist step. coverage_pct_union = 1.00.

**Completeness assessment:** COMPLETE. No unmapped spec requirements.

## Dimension 3 — Deviation-classification clarity (PRE mode: spec-literal-correctness)

PRE mode classifies tasklist-vs-spec divergences. Findings:

### Finding F1 — §7 Phase 0 agent count shorthand ("6") vs §1.1 inventory (11 adopted agents)
- **Spec anchor:** DESIGN.md §7 Phase 0 says "Copy 6 adopted review/orch agents"; §1.1 (lines 56-67) inventory lists 11 adopted agents (muse, critic, editor, reader-sim, continuity-checker, brainstormer, outliner, character-sim, style-creator, web-researcher, writer).
- **Tasklist stance:** Phase 2 Step 2.3 correctly targets 11 agents (lists all 11 explicitly). The tasklist resolves the §7 shorthand by deferring to §1.1 (the authoritative inventory) — this is the correct resolution since §7 "6" refers only to the review/orch subset, while the full adopted set per §1.1 + §2 distribution tree is 11.
- **Classification:** NOT a defect. The tasklist is more correct than a literal §7 reading. **No action.**

### Finding F2 — §5 constraint #1 lists "analyst" among active_tier recipients, but analyst is tier-invariant by design
- **Spec anchor:** DESIGN.md §5 #1 (line 268) says "active_tier is an explicit input parameter in analyst, writer, safety-verifier, tier-coordinator, chronicler". But §3.2 (lines 228-229) + agent-schemas §2.1 + Step 3.8 confirm analyst runs ONCE per chapter (tier-invariant source truth) and does NOT take active_tier.
- **Tasklist stance:** Step 3.8 correctly declares analyst inputs as source_path/work/chapter with NO active_tier, and explicitly notes "NO active_tier, analysis is tier-invariant". This is a deliberate, spec-internal tension (§5 #1 vs §3.2) that the tasklist resolves correctly per §3.2 (the data-flow authority).
- **Classification:** NOT a defect — tasklist resolves a spec-internal contradiction correctly. **Documented as design nuance in coverage matrix CON-1. No action**, but worth flagging to spec author as a §5 wording imprecision (analyst should not be listed in the active_tier recipient set).

### Finding F3 — work-mapping-template key count: spec §3.2 prose "four" vs file's 5 keys
- **Spec anchor:** kb-formats.md §3.2 (per Step 3.17 + PG1.4 cross-source-contradiction agent) says "four" top-level keys, but the actual template file + spec enumeration both yield 5 (work_metadata, characters, concepts, key_scenes, master_translation_table).
- **Tasklist stance:** Step 3.17 explicitly notes "5 top-level keys (NOT 4 — spec §3.2 prose 'four' is a typo; the file + spec enumeration both give 5)". PG1.4 includes a cross-source-contradiction agent that flags this as a spec typo (not a tasklist error).
- **Classification:** NOT a defect — tasklist correctly identifies and survives a spec typo. **No action.**

### Finding F4 — T4 interpolation never stored (no tier_4.yaml)
- **Spec anchor:** kb-formats.md §2.4 + DESIGN.md §3.2 (T4 interpolated at runtime).
- **Tasklist stance:** Step 3.14 explicitly says "Do NOT create a tier_4.yaml — T4 is interpolated at runtime, never stored." Step 3.2 creates tier_4.md as commentary (derivation rationale), NOT a stored profile. PG1.2 completeness lens checks "NO tier_4.yaml exists".
- **Classification:** NOT a defect. Correctly handled. **No action.**

### Finding F5 — schema drift preserved (T1-T3 conflict_to_cooperation/death_euphemism vs T5 conflict_handling/death_handling)
- **Spec anchor:** kb-formats.md §2.2 (schema drift deliberate, absorbed by key-tolerant lookups).
- **Tasklist stance:** Steps 3.11-3.14 port YAMLs byte-faithful preserving drift; Step 3.3 puts the key-tolerant lookup note in the skill body; PG1.4 fidelity gate verifies drift preserved (NOT flagged as error).
- **Classification:** NOT a defect. Correctly handled. **No action.**

### Finding F6 — proof-chapter provisioning: copyrighted Tolkien vs public-domain stand-in
- **Spec anchor:** DESIGN.md §7 Phase 3 says "one Tolkien chapter"; §6 residual risk says "real Tolkien chapter".
- **Tasklist stance:** Step 5.1 supports PATH A (operator-supplied Tolkien under their access rights — PREFERRED, not committed) OR PATH B (public-domain stand-in — committable fallback). Explicitly: "DO NOT commit copyrighted Tolkien prose". This is a necessary legal-provenance refinement of the spec's "Tolkien chapter" language.
- **Classification:** NECESSARY DEVIATION (forced by external legal constraint, documented inline with rationale per §10.2). The tasklist is more legally sound than a literal spec reading. **No action** — correctly carried as an Open Question (line 590).

## Dimension 4 — Risk surface coverage

The tasklist covers every residual risk in DESIGN.md §6:
- Boundary drift → check_boundary.py + VENDOR.md (Phase 0)
- Hybrid half-done → Phase 3 HARD GATE (5 conditions)
- Two-provenance cognitive load → VENDOR.md provenance declarations + CLAUDE.md
- Upstream-sync → Phase 4 UPSTREAM-SYNC.md
- Latent divergent-canon → per-tier continuity + (work,tier,chapter) key (Phase 2 + Phase 3 gate cond3)

Additional risk surfaces the tasklist adds beyond the spec:
- **POST reflect gate (Step PC.6):** runs `superclaude reflect run --depth deep --fix --promote` as a penultimate gate. This is a process-level addition (not in DESIGN.md) that hardens the "0.1 done" definition. Correctly gated (exit 0 only proceeds; exit 10/11/2 FAIL).
- **Per-phase QA gates (PG0-PG3) + post-completion gate (PC.1-PC.5):** 5 lens-based QA gates (template-conformance, internal-consistency, evidence-quality, completeness, actionability, boundary-fidelity, source-fidelity, domain-accuracy) per phase. These are process additions not in DESIGN.md but consistent with the spec's gate discipline (§7 defines phase gates; the QA gates operationalize them).
- **Fix-cycle discipline (max 3 cycles per I16/I20):** bounded retry on every gate. Reasonable.

**Risk assessment:** COMPREHENSIVE. The tasklist adds process hardening (reflect gate, lens QA) without diverging from spec intent.

## Dimension 5 — Recommendation actionability

Every checklist item follows the "Read X → do Y → verify Z → log blocker if fail" pattern. Each item names:
- The exact file path to read (spec section + lines)
- The exact file path to create
- The verification (check_boundary.py exit 0, byte-comparison, gate verdict)
- The blocker log location on failure

This is exceptionally actionable — an executor can follow each item without interpretation.

## T1 verdict (pre-calibration)

- **Status:** success (no defects; 6 findings all classified as NOT-a-defect or NECESSARY)
- **Coverage:** 1.00 (parsed + union)
- **Confidence (self-reported):** 0.94
  - Citation grounding: 0.96
  - Coverage completeness: 1.00
  - Deviation-classification clarity: 0.92 (two spec-internal tensions F2/F3 resolved correctly but worth surfacing)
  - Risk surface coverage: 0.90 (POST reflect gate + QA gates are process additions; verifying they don't over-constrain is a T2 question)
  - Recommendation actionability: 0.95
- **Escalation recommendation:** ESCALATE to T2 (per §5.1 --depth deep forces T2 regardless; and the tasklist's scale — 151 items, 6 phases, multi-spec — warrants heterogeneous review)

## Notable strengths (for T2 calibration)
1. Per-step "Read spec §X (lines Y-Z)" directive — eliminates ambiguity.
2. Provenance-class grouping (ADOPTED-CLEAN vs ADOPTED-PATCHED vs NATIVE vs BUILD-NEW) consistent with §1.1.
3. Every phase ends with a boundary gate re-run (Phase 0/1/2/3 + final) — constraint #6 enforced continuously, not just at end.
4. The 5 HARD-GATE conditions (Step 5.6-5.10) map 1:1 to DESIGN.md §7 Phase 3 gate.
5. Open Questions section (lines 585-594) honestly carries execution-time decisions as risks, not as task items.

## Notable concerns to debate at T2
1. **F2 (analyst active_tier):** spec §5 #1 wording imprecision — should the tasklist flag this to the spec author, or silently resolve per §3.2? (Currently silently resolves.)
2. **Process-add scope:** the 5 lens-QA gates per phase + post-completion gate add substantial ceremony. Is this proportionate to a "0.1" release, or over-engineered? (T2 should debate cost/benefit.)
3. **Step PC.6 POST reflect gate:** the tasklist invokes `superclaude reflect run --depth deep --fix --promote` — the `--fix` and `--promote` flags auto-mutate. Is auto-promotion appropriate for a 0.1 release gate, or should it be `--no-promote` with manual promotion? (T2 should debate.)
4. **Step 1.2 first-commit dependency:** the POST reflect gate's audit base resolves from `start_commit:`. Step 1.2 makes the first commit + repins. This is correct handling of zero-commit territory, but it couples the tasklist to git-state preconditions not in DESIGN.md.
