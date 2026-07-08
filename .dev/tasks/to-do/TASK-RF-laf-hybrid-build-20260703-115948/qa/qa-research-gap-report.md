# QA Research Gap Report — LAF 0.1 Hybrid Build

**Lens:** GAP-DETECTION (adversarial stance)
**QA Mode:** research-gate | fix_authorization: false
**Track goal:** Implement LAF 0.1 end-to-end (Phases 0-4) producing laf-adaptation/
**Assigned files:** research/01 through research/06
**Ground-truth specs:** .dev/releases/current/0.1/design/ (7 specs)

---

## Method

1. Read scope map (research-notes.md) + all 7 design specs.
2. Read all 6 research files.
3. For each buildable area in the specs, verify research coverage sufficient to author task items.
4. Rate gaps: CRITICAL (blocks builder) / IMPORTANT (reduces quality) / MINOR (nice-to-fix).

---

## Coverage matrix — buildable area → research coverage

| Buildable area | Spec anchor | Covered by | Sufficient to author? |
|---|---|---|---|
| 15 agents (11 adopted / 2 native / 2 build-new) | DESIGN §1.1, §2 | R1 §A, R2 (native), R3 (build-new) | YES |
| 16 skill dirs + resources | DESIGN §2, skill-specs | R1 §B, R2, R3 | YES |
| Native agent bodies (analyst, safety-verifier) | agent-schemas §2 | R2 F1-F2 (verbatim frontmatter + hard blocks) | YES |
| Native skill bodies (tiers, rules, source-fidelity) | skill-specs §1-3 | R2 F3-F5 (verbatim bodies) | YES |
| writer.md patch (ADOPTED-PATCHED) | agent-schemas §3 | R2 F6, R1 A11 | YES |
| reader-sim persona-as-data | agent-schemas §4 | R2 F7 (persona payload documented, no edit) | YES |
| chronicler / tier-coordinator | agent-schemas §5, tier-coordinator.md | R3 F1-F2 (algorithms + invariants verbatim) | YES |
| /adaptation-safety + rubric | skill-specs §4, safety-rubric.md | R3 F3, F6 (6 sections verbatim) | YES |
| Genre resources children.md / ya.md | skill-specs §4.1 | R3 F4-F5 (dimensions + sourcing) | PARTIAL — see G4 |
| kb/tiers + adaptation-mapping port | kb-formats §2-3 | R4 (9-file carry table, on-disk verified) | YES |
| per-tier canon graft G1 formats | kb-formats §4 | R4 §4 (all 5 file formats) | YES |
| Tier-4 interpolation (never stored) | kb-formats §2.4 | R4 §1.4 + R2 F3 ("DO NOT create tier_4.yaml") | YES |
| check_boundary.py (A-F, modes, helpers) | boundary-contract §3 | R5 §3 (full verbatim pseudocode) | YES |
| VENDOR.md manifest | boundary-contract §2 | R5 §2 (verbatim skeleton) | YES |
| Upstream CWS acquisition | user decision #1 | R5 §5 (7-step procedure) | YES |
| 11-step workflow + safety loop + fan-out | DESIGN §3 | R6 §1-3 | YES |
| Phase-3 hard gate (5 conditions) | DESIGN §7 | R6 §5 (L3/L4/L6 encoding) | YES |
| Proof-chapter provisioning | DESIGN §7 | R6 §4 (3 options + copyright flag) | YES |
| Phase-4 upstream-sync docs | boundary-contract §5 | R5 §7 (6-step verbatim) | YES |
| CLAUDE.md authoring | DESIGN §2 line 105 | R1 D9 (flagged, provenance nuance) | PARTIAL — see G1 |
| NOTICE (Apache-2.0) | boundary-contract §2 line 48 | R1 open item #6, R5 §5.1 step 5 | PARTIAL — see G2 |
| .githooks/pre-commit + CI wiring | boundary-contract §4 | R1 P4.2, R5 §6 | PARTIAL — see G3 |
| source/ work/ kb/ scaffolding | DESIGN §2 | R1 §C-D (scaffold rows) | YES |

---

## Findings

### G1 — CLAUDE.md authoring content is unspecified (IMPORTANT)

DESIGN.md §2 line 105 lists `laf-adaptation/CLAUDE.md` as "ADOPTED pattern + LAF conventions
section + boundary-contract note" — a build deliverable. R1 D9 (research 01, lines 227, 230)
correctly *inventories* it as a target file and flags the provenance nuance (adopted-pattern vs
authored, outside the check_boundary.py rule-F glob). **But no researcher extracted or specified
what CLAUDE.md must CONTAIN.** There is no source `CLAUDE.md` in the upstream cited, and no spec
section defines its three parts:
- the "ADOPTED pattern" — where does it come from (CWS root CLAUDE.md at the pinned SHA)?
- the "LAF conventions section" — what conventions (frontmatter dialect, tier-axis, boundary rule)?
- the "boundary-contract note" — presumably a pointer to VENDOR.md + check_boundary.py.

A task builder can author a checklist ITEM ("author CLAUDE.md") but has no content contract to
put in the B2 self-contained paragraph beyond the one-line DESIGN description. This is authorable
but under-specified — the builder will have to synthesize content. **Severity: IMPORTANT** — it
does not block the build (the file is not gate-checked), but the item will be vague relative to
every other file, which all have verbatim or line-cited content. Recommend the task explicitly
scope CLAUDE.md content (or defer it as a documented stub) rather than leave it to executor
improvisation.

### G2 — NOTICE file: no researcher owns it; conflicting placement (IMPORTANT)

boundary-contract.md line 48 states `license: Apache-2.0 (upstream) — attribution retained per
NOTICE` and DESIGN.md line 106 says "(Apache-2.0 attribution)". This implies a `NOTICE` file at
the tree root. Coverage:
- R1 (research 01, line 231) explicitly flags it: "A `NOTICE` file for Apache-2.0 attribution is
  implied but NOT explicitly placed in the tree... **Unverified — needs decision** whether
  attribution lives in `VENDOR.md`... or a separate `NOTICE` file." (open item #6).
- R5 (research 05, §5.1 step 5 + §8 Phase 0) says "Retain **Apache-2.0 attribution in a `NOTICE`
  file**" and lists "write `NOTICE` (Apache-2.0)" as a Phase-0 deliverable.

**The gap: the two researchers DISAGREE and neither resolves it.** R1 treats NOTICE as an open
decision (maybe just a VENDOR.md line); R5 treats it as a committed Phase-0 file deliverable. A
task builder reading both gets a contradiction: is NOTICE a real file to author in Phase 0, or a
line in VENDOR.md? The Apache-2.0 license *requires* a NOTICE file be propagated if the upstream
ships one — so this is a real compliance concern, not cosmetic. **Severity: IMPORTANT.** The task
builder needs a single resolved answer. Recommend: Phase 0 authors a root `NOTICE` file
(Apache-2.0 attribution to haowjy/creative-writing-skills) AND the VENDOR.md `license:` line
points to it — and the task should note NOTICE is outside the check_boundary.py glob (like
CLAUDE.md).

### G3 — .githooks/pre-commit + CI wiring left as "optional / needs decision" (IMPORTANT)

boundary-contract.md §4 (lines 173-181) names TWO concrete enforcement points as **blocking**:
- `.githooks/pre-commit` (opt-in per clone) → `check_boundary.py`
- CI (PR gate) → `check_boundary.py`

Coverage:
- R1 (research 01) P4.2 lists ".githooks/pre-commit wiring — **needs decision**" and open item #7
  marks it "optional infra, needs decision."
- R5 (research 05) §6 documents the enforcement table verbatim and §6 closing says
  ".githooks/pre-commit (opt-in hook wrapper) and a CI workflow step — both simply invoke the
  UV-wrapped command. These are lightweight wrappers, not additional scripts."

**The gap: no researcher produced the actual authorable content** for either wrapper, and R1
places it in Phase 4 as optional while the spec lists it as a standing enforcement point (not a
phase deliverable). Two problems for the builder:
1. **Phase placement is wrong/ambiguous.** The pre-commit hook and CI wiring logically belong in
   Phase 0 (once check_boundary.py exists), not Phase 4. R1 buried it at P4.2 as optional; R5
   lists it under "Deliverables the script depends on (Phase-0 artifacts)". This is an
   inter-researcher placement conflict.
2. **No content.** Neither the `.githooks/pre-commit` script body nor the CI workflow YAML is
   drafted. Both are trivial (a one-line UV invocation) but a B2 self-contained item needs the
   exact content + path.

**Severity: IMPORTANT.** The boundary contract's entire value proposition is enforcement; leaving
the enforcement wiring as "optional, needs decision" undercuts the #1 residual-risk mitigation
(DESIGN §6). Recommend: resolve to Phase 0, author both wrappers with the UV-wrapped command,
and note the pre-commit hook is opt-in (`git config core.hooksPath .githooks`).

### G4 — children.md / ya.md sourcing is named but content is thin (IMPORTANT)

skill-specs §4.1 says children.md is "Sourced from the tier-1/tier-3 transform prompts and tier
profiles" and ya.md from "the tier-5 profile's `adaptation_philosophy` + `supplementary_approach`".
R3 (research 03) FILES 4-5 lists the content *dimensions* (prosocial centering, episodic
structure, etc.) and points at the sourcing files. **However:**

- The tier-1/tier-3 transform prompts (`prompts/transformation/tier_1_transform.md`,
  `tier_3_transform.md`) — the named source for children.md — were **NOT read or extracted by any
  researcher.** R4's 9-file carry table (research 04 §0) does not include them (they are not
  verbatim YAML carries). R3 names them as the source but did not open them. **Verified they exist**
  (`prompts/transformation/tier_1_transform.md` 2129 B, `tier_3_transform.md` 2040 B). So the
  builder is told "source children.md from these two files" but has no extract of their content and
  no line cites — unlike every other native artifact which has verbatim content.
- ya.md's source fields (`adaptation_philosophy`, `supplementary_approach` in tier_5.yaml) ARE
  within R4's carried tier_5.yaml, so ya.md is better anchored than children.md.

Unlike the safety RUBRIC (which R3 carried verbatim from safety_check.md), the genre resources are
**authored craft prose**, not verbatim carries — so some synthesis is expected. But the builder
still needs the transform-prompt content in hand to author children.md faithfully. **Severity:
IMPORTANT** (not critical — the sourcing files are named and exist, so the executor can read them
at build time; but the research did not pre-digest them, so the task item will point at raw
sources rather than a distilled content contract). Recommend the task item for children.md
explicitly reference `prompts/transformation/tier_1_transform.md` + `tier_3_transform.md` +
`kb/tiers/tier_1..3.yaml` as read-inputs in its B2 context clause.

### G5 — adaptation-tiers commentary file count unresolved + source not extracted (MINOR)

DESIGN.md line 122 says `adaptation-tiers` carries "resources/tier_N.md commentary" (plural).
R1 (research 01, B13r + note line 104) flags the exact count as "content decision owned by R2".
R2 (research 02, FILE 3) decides "5 files" (tier_1.md..tier_5.md) sourced from
`docs/design_decisions/001-five-tier-system.md` and `003-agency-externalization.md`. Verified
both design-decision files exist (001: 1108 B, 003: 1576 B). Two small gaps:
1. R2 says 5 commentary files (tier_1..tier_5), but there is no tier_4 profile — a tier_4.md
   commentary is arguably odd (T4 is interpolated). The 5-vs-4 commentary decision is not
   reconciled against the "no tier_4 stored" rule. Minor, but the builder should decide whether
   tier_4.md commentary exists (it can — commentary is not a stored profile — but it's unstated).
2. The two design-decision source files were named but not extracted/quoted (like G4). They are
   tiny (< 1.6 KB each) and exist, so the executor reads them at build time. Severity: MINOR.

### G6 — Integration points: adequately covered (NO GAP)

Checked the three cross-subsystem seams the QA brief called out:
- safety-verifier FAIL to writer step 3. Covered: R6 §2 (loop is CWS's, trigger is native),
  R3 §4.1 workflow-branch pseudocode (next: revise returns to workflow step 3), R6 explicitly
  flags "verify the FAIL edge exists even if the proof chapter passes first try" (research 06
  line 63) — a genuine integration-test insight. Sufficient.
- tier-coordinator RECONCILED gates chronicler. Covered: R3 §5 + tier-coordinator.md §5
  (reconcile()==RECONCILED then for tier: chronicler(...)), R3 run-gate section. Sufficient.
- analyst tier-invariant, shared_analysis fans to per-tier pipelines. Covered: R6 §3, R3
  Check A (unsourced yields CONFLICT). Sufficient.
No gap. The seams are documented with pseudocode and cited.

### G7 — Test/verification coverage: adequately covered (NO GAP)

- check_boundary.py verification (run --init, --report, verify, exit 0): covered by
  R5 §3.1 modes + research-notes TESTING_REQUIREMENTS + R6 gate condition 5.
- Phase-3 5-condition gate as integration test: covered by R6 §5 (each condition to L4 verdict
  item, L6 aggregation, HALT on any FAIL).
- proof-chapter provisioning decision: covered by R6 §4 (3 ranked options, copyright flag,
  reconciliation of "real Tolkien chapter" spec phrasing vs licensing).
No gap.

### G8 — Cross-spec numeric discrepancies surfaced but not builder-resolved (MINOR)

R1 §E documents three real discrepancies (11 vs 15 agents; "13 adopted" reconciles to no clean
count; Phase-0 "6 agents" vs 11 in manifest) and R4 §5.2 flags the "Four vs 5 top-level keys" in
work-mapping. All are correctly flagged and given a build-to recommendation (build 15 agents,
build to the boundary-contract manifest, build to 5 keys). These are handled well; noting them
only because several end with "confirm with design owner" — the task builder should carry these as
explicit Key-Constraints/Open-Questions rather than silently pick a side. Severity: MINOR.

### G9 — Tier-3 safety ADVISORY consistency (NO GAP, noted)

safety-verifier runs the rubric in ADVISORY at T3 (agent-schemas §2.2). children.md covers T1-3
craft (R3 FILE 4). The rubric word-lists are T1/T2 only (safety-rubric §1). Internally consistent
(T3 rubric is advisory/report-only, reusing T1-2 sections). No missing artifact. Confirmed not a gap.

---

## Summary of gaps

| ID | Area | Severity |
|---|---|---|
| G1 | CLAUDE.md authoring content unspecified | IMPORTANT |
| G2 | NOTICE file — inter-researcher contradiction, unresolved placement | IMPORTANT |
| G3 | .githooks/pre-commit + CI wiring left optional; wrong phase; no content | IMPORTANT |
| G4 | children.md source (tier_1/3 transform prompts) not pre-digested | IMPORTANT |
| G5 | adaptation-tiers tier_4.md commentary count unreconciled | MINOR |
| G8 | Numeric discrepancies flagged but need explicit builder carry | MINOR |
| G6/G7/G9 | Integration points, test coverage, T3 advisory | NO GAP |

No CRITICAL gaps found. Every buildable AREA in the 7 specs has research coverage; the
IMPORTANT items are the small infra/attribution/doc deliverables (CLAUDE.md, NOTICE, git-hooks,
genre-resource sourcing) that the specs mention only in passing and that no single researcher
fully owned. None blocks the task builder from producing a working task file, but all four reduce
task-item quality (vague B2 paragraphs, unresolved contradictions the executor must guess at).

## Verdict rationale

The six research files provide dense, line-cited, largely-verbatim coverage of every major
subsystem: agents, skills, kb layers, boundary contract, workflow, and proof gate. The adversarial
sweep found NO missing buildable subsystem and NO broken integration seam. The gaps are confined to
four peripheral deliverables the specs under-specify (CLAUDE.md content, NOTICE file, enforcement
wiring, genre-resource source digestion) plus two hand-off-hygiene items. Because the affected
deliverables are real (spec-named) and two involve an unresolved inter-researcher contradiction
(NOTICE) and a spec-vs-research phase conflict (git-hooks), the aggregate crosses the threshold
from "clean pass" to "pass with required fixes."

VERDICT: FAIL

Rated issues (must address before task-build):
- IMPORTANT G1 — Scope CLAUDE.md content (3 parts) or document as an explicit stub.
- IMPORTANT G2 — Resolve NOTICE: author a root NOTICE file in Phase 0 + point VENDOR.md at it;
  note it's outside the check_boundary.py glob.
- IMPORTANT G3 — Move .githooks/pre-commit + CI wiring to Phase 0, author both wrappers with the
  UV-wrapped check_boundary.py invocation; mark pre-commit opt-in.
- IMPORTANT G4 — For children.md, cite prompts/transformation/tier_1_transform.md +
  tier_3_transform.md + kb/tiers/tier_1..3.yaml as read-inputs in the task item.
- MINOR G5 — Decide tier_4.md commentary presence; cite design_decisions 001/003 as read-inputs.
- MINOR G8 — Carry the R1/R4 numeric discrepancies as explicit Key-Constraints in the task file.

Note on FAIL severity: all six issues are IMPORTANT/MINOR and independently fixable with small
additions; none requires re-research of a subsystem. A task builder could proceed and patch these
inline, but per the adversarial gate they are logged as required fixes rather than silently waived.

