# QA Research Depth Report — LAF 0.1 Hybrid Build

**Lens:** research-depth
**Stance:** Adversarial — assume research is superficial until proven otherwise.
**Track goal:** Implement LAF 0.1 end-to-end (Phases 0-4) producing `laf-adaptation/`.
**Assigned files:** research/01 through research/06.
**Ground-truth:** `.dev/releases/current/0.1/design/` (7 specs).
**Test:** Can a task builder author per-file checklist items WITHOUT re-reading source specs?

---

## Method

Reading all 6 research files and all 7 design specs. For each depth-checklist item,
comparing research authorable-content against ground-truth spec content to detect
surface-level file inventories masquerading as deep research.

Concrete test targets: `analyst.md`, `check_boundary.py`, `kb/tiers/tier_1.yaml` carry,
`/adaptation-safety` SKILL.md.

---

## Findings (incremental)

### Depth Checklist Item 1 — HOW, not just WHAT (authorable content)

**R2 (native agents/skills): PASS — deep.** Verified against ground-truth:
- `analyst.md` frontmatter in R2 (02:53-64) is **byte-identical** to agent-schemas.md:50-61,
  including the `# rewritten to laf-adaptation:story-memory at vendor time` comment. Phase-0 ABORT
  hard-block (R2 FILE 1) matches agent-schemas.md:71-77 verbatim. Inputs (source_path/work/chapter,
  NOT active_tier) match agent-schemas.md:63-64.
- `safety-verifier.md` frontmatter, tier-gate (T1-2 full/T3 advisory/T4-5 SKIP N/A), verdict-block,
  Write-only constraint all match agent-schemas.md:87-122 verbatim.
- SKILL.md bodies for adaptation-tiers (4-section body incl. Interpolation), adaptation-rules (Applying
  a rule + Cascade), source-fidelity (5-phase protocol + §3.2 output schema) are **byte-verbatim** to
  skill-specs.md:49-78, 104-126, 182-243. The §3.2 output YAML schema is reproduced in full.
- `writer.md` patch: R2 gives upstream baseline (with the preserved duplicate `creative-writing-craft`
  line), the vendored form, both-hash rule, and Rule-C mechanics — all match agent-schemas.md:136-178.
- **A builder can author analyst.md / safety-verifier.md / all 3 native SKILL.md files without
  re-opening any spec.** Frontmatter is verbatim, body outlines are verbatim, output schemas present.

**R3 (build-new agents/safety): PASS — deep.** Verified against safety-rubric.md + agent-schemas.md:
- chronicler/tier-coordinator frontmatter verbatim (agent-schemas.md:222-233, 264-275); model + Bash
  distinction (chronicler NO Bash, tier-coordinator HAS Bash) correctly captured.
- The FULL safety rubric is reproduced: 6 sections with verbatim word-lists (Tier-1/Tier-2 forbidden
  tokens exactly match safety-rubric.md:24-27), permitted-emotions lists, auto-failures (T1/T2),
  aggregation pseudocode (safety-rubric.md:76-87 verbatim), machine-parseable verdict YAML block
  (safety-rubric.md:96-115 verbatim), and workflow branch logic (safety-rubric.md:119-127 verbatim).
- tier-coordinator reconcile() Checks A/B/C with pseudocode from tier-coordinator.md (not re-read here
  but internally consistent and cited line-by-line).
- **A builder can author /adaptation-safety SKILL.md verbatim from R3 without re-reading the rubric.**

### Depth Checklist Item 1 (cont.) — R5 check_boundary.py algorithm

**R5: PASS — deep.** Cross-checked against boundary-contract.md byte-for-byte:
- Rules A-F pseudocode in R5 §3.2 is a **verbatim reproduction** of boundary-contract.md:108-151.
- 3 modes (verify/--init/--report), exit codes, `--upstream <dir>` requirement match §3.1 exactly.
- Helper defs `body_of()` and `frontmatter_line_diff()` (incl. order-insensitivity on `skills:`) match
  boundary-contract.md:162-167. R5 correctly connects order-insensitivity to the writer.md duplicate
  `creative-writing-craft` line.
- VENDOR.md format (5 header fields, 3-line invariants, 4-column manifest, recursive resource hashing)
  matches §2 verbatim. Prefix-rewrite determinism + writer 2-hash rule captured.
- 6-step upstream-sync protocol matches §5 verbatim.
- **A builder can author scripts/check_boundary.py from R5 without re-reading boundary-contract.md.**
  The one genuine gap (verify-mode upstream access) is explicitly flagged as needs-decision, not glossed.

### Depth Checklist Item 1 (cont.) — R4 carry mapping + kb schemas

**R4: PASS — exceptionally deep.** R4 went beyond the spec and **read the actual port-source YAML files
on-disk**, verifying claims rather than restating spec prose:
- 9-row port-source→target carry table with exact line counts (716 lines total), rename pattern
  (`_`→`-`, suffix drop), verbatim-copy mode. One item per file.
- kb/tiers schema: per-file top-level key presence table (T1/T2/T3/T5) verified on-disk, matching
  kb-formats.md:83-88.
- **Schema drift independently confirmed** (`conflict_to_cooperation`/`death_euphemism` vs
  `conflict_handling`/`death_handling`) with exact line cites per file, plus the reader-side
  `.get(a) or .get(b)` key-tolerance resolution.
- Cascade resolution (5-level, most-specific-wins) with the master_translation_table NEVER-a-source
  invariant. Tier-4 no-file / interpolated. graft-G1 file formats (continuity/decisions/canon-delta.md)
  with I-1/I-2/I-3 invariants from kb-formats.md §4.
- Caught a real **[SPEC-CONTRADICTED]** discrepancy ("Four" vs 5 top-level keys) and resolved it.

### Depth Checklist Item 2 — End-to-end data flows

**PASS.** R6 traces the full 11-step workflow with per-step provenance/READS/WRITES (matching DESIGN §3),
the safety FAIL→step-3 loop (CWS loop / native trigger decomposition), the analyst-once + tier fan-out
across T1/T3/T5, and the RECONCILED→chronicler gate. R3+R4 corroborate the RECONCILED gate and the
per-tier chronicler write. Data flows are traced, not merely named.

### Depth Checklist Item 3 — Edge cases / failure modes

**PASS.** Documented across the set:
- analyst NO-ACCESS → `status: ABORTED` HALT (R2 FILE 1, R6 step-1 gate).
- safety T4-5 SKIP → verdict N/A; auto-failures dominate section rollups (R3 aggregation).
- tier-coordinator CONFLICT branch → caller re-dispatches offending tier before chronicler (R3 FILE 2).
- sequential-fallback G2 trigger (state-heavy markers parallel_plotlines/unreliable_narrator/
  nested_timeline OR author override) (R3, R6 §3).
- schema-drift key-tolerance (R4 §1.3).
- Rule C body-byte-change FAIL; Rule E name-collision; verify-mode upstream access flagged (R5).
- Proof-chapter provisioning: Tolkien-copyright FLAG + PD-standin fallback + external-input primary (R6 §4).

### Depth Checklist Item 4 — Replicable patterns

**PASS.** Claude-lowered closed key-set (name/description/model/skills/tools; Mars keys forbidden) —
R2 dialect contract matches agent-schemas.md:22-36. Prefix-rewrite determinism, ADOPTED-PATCHED 2-hash
rule, verbatim-carry zero-rework all specified with enough precision to replicate.

### Depth Checklist Item 5 — Per-file authorability test (4 representative targets)

1. **analyst.md** — R2 FILE 1 supplies verbatim frontmatter + Phase-0 ABORT block + inputs + output
   contract + builder checklist. **Authorable without re-reading. PASS.**
2. **check_boundary.py** — R5 §3.1-3.4 supplies modes, full A-F algorithm, helper defs, exit semantics.
   **Authorable without re-reading. PASS.**
3. **kb/tiers/tier_1.yaml carry** — R4 CARRY-01 supplies source path, line count (94), rename target,
   verbatim-copy-no-normalize instruction, drift-preservation rule. **Authorable. PASS.**
4. **/adaptation-safety SKILL.md** — R3 FILE 3 + FILE 6 supply verbatim frontmatter + the full 6-section
   rubric body + auto-failures + verdict contract. **Authorable without re-reading. PASS.**

### Cross-file integrity & minor observations (non-blocking)

- **Ownership boundaries are clean.** R1 owns inventory/manifest rows; R2 native content; R3 build-new
  content; R4 kb data/formats; R5 boundary script; R6 workflow/MDTM. No content duplication that would
  cause conflicting task items; handoffs are explicitly labeled ([R2]/[R3]/[R4] tags in R1 §F checklist).
- **Verdict-block variant discrepancy** (abbreviated agent-schemas.md §2.2 vs authoritative
  safety-rubric.md §4) is caught by BOTH R2 and R3, which agree the §4 full form is authoritative. Good
  adversarial cross-checking — not a gap.
- **Discrepancy handling is a strength, not hand-waving.** R1's three numeric discrepancies (11-vs-15
  agents, "13 adopted", 6-vs-11 Phase-0) are each traced to a specific denominator and resolved to a
  concrete build target ("build 15 agents", "build to manifest", "vendor all 11"). These are real spec
  imprecisions surfaced with build-actionable resolutions.
- **Open decisions are correctly externalized, not invented:** upstream_sha, NOTICE-file placement,
  .githooks opt-in, verify-mode upstream access, tier-commentary file count, proof-chapter provisioning.
  None of these block authorability of the file being built; each is a genuine execution-time choice.
- **Minor:** R6 correctly flags the MDTM template path in the brief (`.claude/templates/...`) is stale
  and resolves the real pipx path. This is a builder-blocking correction that was caught — good depth.

---

## VERDICT: PASS

The research is **genuinely deep**, not a surface-level file inventory. Every representative target file
(analyst.md, safety-verifier.md, the 3 native SKILL.md files, check_boundary.py, the 9 kb carries,
/adaptation-safety, chronicler, tier-coordinator) is authorable from research alone — verbatim
frontmatter, verbatim body outlines, full output schemas, full algorithms, and hard-behavior blocks are
present. Spot-checks against 5 of the 7 ground-truth specs (boundary-contract.md, agent-schemas.md,
skill-specs.md, safety-rubric.md, and R4's on-disk port-source verification) confirmed **byte-level
fidelity** with zero fabrication detected.

Depth checklist: all 5 items PASS.
- (1) HOW-not-WHAT: authorable content present for native (R2), build-new (R3), script (R5), kb (R4). ✓
- (2) End-to-end data flows traced (R6 11-step, safety loop, fan-out, RECONCILED gate). ✓
- (3) Edge cases / failure modes documented (ABORT, SKIP N/A, CONFLICT, G2, key-tolerance, Rule C/E). ✓
- (4) Patterns replicable (closed key-set, prefix determinism, 2-hash, verbatim-carry). ✓
- (5) 3-4 representative files authorable without re-reading specs — verified 4/4. ✓

**Adversarial stance discharged:** I assumed superficiality and attempted to disprove depth by comparing
research claims against ground-truth line-by-line. The research survived: it does not merely list file
names — it reproduces the authorable payload and even independently re-verifies on-disk data (R4). The
one class of genuine gaps (execution-time unknowns) is explicitly flagged rather than silently omitted,
which is the correct behavior for a Deep-tier research pack.

No FAIL-severity issues. No blocking gaps to per-file task authorability.

**Report file:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/qa/qa-research-depth-report.md`
