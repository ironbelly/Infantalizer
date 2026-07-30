# QA Report — Task ↔ Research/Spec Alignment (Cross-Validation)

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-07-09
**Task file:** `TASK-RF-prep-chapter-materialize-20260709-004725.md`
**Driving spec:** `.dev/brainstorms/20260709T001338Z-prep-chapter-ingestion/merged-requirements.md`
**Adversarial stance:** Assume the builder dropped or misrepresented research findings. Target ≥3 alignment gaps.

**Cross-validation goal:** Every significant research/spec finding has a corresponding checklist item, and no item fabricates actions not grounded in research.

---

## Inputs Read (full, no skimming)

- Task file: `TASK-RF-prep-chapter-materialize-20260709-004725.md` (422 lines, all 7 phases + checklist)
- Spec: `merged-requirements.md` (§1-§15, incl. §11 BOM, §13 AC1-AC7)
- Research 01 (file inventory + edit loci, 8 BOM files)
- Research 02 (boundary contract, VENDOR row, AC6, check_boundary mechanics)
- Research 03 (skill authoring: manifest v1 schema, 16-row failure table, confidence rule, precedence)
- Research 04 (MDTM template + Approach A numbering + gate mapping)
- Ground-truth spot checks against `path-contract.md`, `VENDOR.md`, `laf-adaptation/scripts/`

---

## CHECK 1 — Spec §11 BOM (8 files) → corresponding edit/create item

| # | Spec §11 BOM file | Change per spec | Task item(s) | Verdict |
|---|---|---|---|---|
| 1 | `skills/chapter-materialize/SKILL.md` | NEW NATIVE — split/normalize/adopt procedure | **Step 2.1** (author) | COVERED |
| 2 | `skills/chapter-materialize/resources/boundary-rules.yaml` | NEW NATIVE — declarative ruleset | **Step 2.2** (author) | COVERED |
| 3 | `agents/prep-cordinator.md` | +1 `skills:` line + Stage-0 procedure | **Step 3.1** (5 sub-edits a–f) | COVERED |
| 4 | `skills/prep/SKILL.md` | +Stage-0 note §1 + pointer | **Step 3.2** (edits a,b) | COVERED |
| 5 | `skills/prep/resources/path-contract.md` | +§5 rows + §6 subsection; §4 read-set UNCHANGED | **Step 4.1** (edits a,b,c) | COVERED |
| 6 | `source/README.md` | +manifest + `.raw/` subsection | **Step 4.2** | COVERED |
| 7 | `.claude/commands/laf/prep.md` | +`--source-mode`; broadened `--source` | **Step 3.3** (edits a,b) | COVERED |
| 8 | `VENDOR.md` | +1 NATIVE row (Rule F) | **Step 4.3** | COVERED |

Plus the spec's implied 9th artifact — the `.claude/skills/chapter-materialize` **symlink** (mirror
convention, research 01 §0) — is covered by **Step 2.3**. **All 8 BOM files + the symlink map 1:1 to
task items. No BOM file dropped.** VERDICT: PASS.

---

## CHECK 2 — Acceptance criteria AC1–AC7 → item or verification criterion

| AC | Requirement (spec §13) | Where reflected in task | Verdict |
|----|----|----|----|
| AC1 | Mode A + Mode B yield identical canonical set + manifest, no manual pre-split | Step 2.1 §5 mode-detect + §7 commit; verified Step 5.2(6) AC walkthrough; M4 Step 6.7 (spec §1-§8) | COVERED |
| AC2 | `Books/LWW/` (split+monolith) does NOT auto-pick → mode question | Step 2.1 §5 ambiguity→HALT branch (verbatim `Books/LWW/` example); Step 6.3 operational-correctness lens explicitly checks the HALT-not-guess branch | COVERED |
| AC3 | Re-run narnia/tolkien adopts, zero byte rewrites (Mode C) | Step 2.1 §10 "Mode C adopt zero re-split"; Step 5.2(5) no adopted body touched | COVERED |
| AC4 | No non-CERTAIN `ch-NN.txt` before greenlight; single-signal never CERTAIN | Step 2.1 §6 confidence rule (single-signal capped PROBABLE) + §7 deferred-write invariant; Step 6.3 confidence-rule lens | COVERED |
| AC5 | Every chapter row: confidence+provenance+needs_human_review; every discard a normalization_event w/ fidelity risk | Step 2.1 §12 manifest schema + §9 normalization; Step 6.2 manifest-schema lens verifies every field | COVERED |
| AC6 | `check_boundary.py` exits 0; read-set byte-unchanged; no 9th file; no second script | Steps 5.1 (run), 5.2 (invariants 1–5), 7.2 (final re-check) | COVERED |
| AC7 | Greenlight cannot CONFIRM while any ambiguous_split/needs_review/high-risk loss unresolved | Step 2.1 §8 route-to-gate + Step 3.1(f) STAGE 7 checklist line; Step 6.3 operational lens | COVERED |

**All 7 ACs are reflected in build items AND independently checked by the Phase 5 invariants walkthrough
(Step 5.2 item 6) and the Phase 6 QA lenses.** VERDICT: PASS.

---

## CHECK 3 — Load-bearing research artifacts → the authoring item (Step 2.1)

| Artifact | Source | Reflected in Step 2.1? | Verdict |
|----|----|----|----|
| Manifest v1 schema (every field) | research 03 §D / spec §5 | §12 "END on the VERBATIM `chapter-manifest.yaml` v1 schema fenced block … every field from the blueprint" | COVERED |
| 16-row failure table (verbatim) | research 03 §C / spec §7 | §11 "carrying the VERBATIM 16-row table … do NOT paraphrase"; Step 6.2 lens asserts "EXACTLY 16 rows" | COVERED |
| Confidence rule (CERTAIN ≥2 signals) | research 03 §B6 / spec §6 | §6 "state VERBATIM and bolded **'CERTAIN requires ≥2 independent agreeing signals and no contradiction.'**" | COVERED |
| Auto-detect precedence (adopt>folder>file>HALT) | research 03 §B5 / spec §3 | §5 "carrying the auto-detect precedence VERBATIM as an ordered list" | COVERED |
| Five evidence layers | research 03 §B6 / spec §6 | §6 `### The five evidence layers` ordered table | COVERED |
| Deferred-write safety invariant | research 03 §B7 / spec §10 | §7 bolded invariant | COVERED |

**Every high-value research finding for the schema/table/rule/precedence is explicitly instructed into
Step 2.1 with verbatim/byte-exact language.** VERDICT: PASS.

---

## CHECK 4 — FABRICATION CHECK (adversarial: item referencing files/patterns NOT in research/spec)

Cross-referenced every file path, script, and edit target named in the task against the research + spec.

| Potential fabrication | Present in task? | Grounded? | Verdict |
|----|----|----|----|
| Editing `check_boundary.py` | Referenced **22×** but ONLY as "byte-unchanged / ZERO edits / do NOT touch" + one VALIDATION run (Steps 5.1, 7.2) | research 02 Q1 mandates zero edits; run is the AC6 validation, not an edit | NO FABRICATION |
| A 9th numbered package file | Explicitly FORBIDDEN throughout; manifest declared a `source/` sidecar | spec N3, research 01 §3 | NO FABRICATION |
| A second script / test runtime | Explicitly FORBIDDEN (ADR-006); no `create script` item exists | spec §2 N2, research 04 §1e (TESTING=NONE) | NO FABRICATION |
| A second VENDOR row for `boundary-rules.yaml` | Explicitly forbidden — one `/**` glob row covers both files | research 02 Q2 | NO FABRICATION |
| A copy-based `.claude` mirror step | Explicitly forbidden — symlink only (`readlink`, not `diff -r`) | research 01 §0 (mirror = symlink) | NO FABRICATION |
| Any invented manifest field / failure row | Task instructs VERBATIM reproduction only, with field-count/row-count assertions | research 03 §C/§D | NO FABRICATION |
| Editing an ADOPTED body | Explicitly forbidden; Step 5.2(5) asserts only NATIVE/new files touched | spec §11, research 01 summary | NO FABRICATION |

**No task item fabricates an action absent from research/spec. The task is notably disciplined: nearly
every "do NOT" mirrors a specific research finding.** VERDICT: PASS.

---

## CHECK 5 — Research-identified edge cases → verification criteria

| Edge case | AC | Reflected in task verification? | Verdict |
|----|----|----|----|
| Books/LWW mode ambiguity (split+monolith) | AC2 | Step 2.1 §5 verbatim example; Step 6.3 operational lens checks HALT-not-guess | COVERED |
| Mode C zero-resplit adopt | AC3 | Step 2.1 §10; Step 5.2(5) | COVERED |
| Deferred-write invariant | AC4/AC7 | Step 2.1 §7 bolded; Step 6.3 confidence + operational lenses | COVERED |
| Byte-unchanged read-set | AC6 | Step 5.2(1) grep-assert + git-diff double check; Step 4.1(a) note-after-L73 preserves block | COVERED |
| Per-chapter normalization_event fidelity | AC5 | Step 2.1 §9 + §12 schema; Step 6.2 manifest-schema lens; Step 6.3 confidence lens | COVERED |

VERDICT: PASS.

---

## CHECK 6 — Spec §15 deferred seams recorded as OUT-OF-SCOPE (not build items)

Spec §15 defers two seams: (1) whether `/laf:rewrite` reads `chapter-manifest.yaml` (a potential 4th
`rewrite_phase_reads` entry); (2) per-chapter analysis granularity in the rewrite phase.

Task file §"OUT-OF-SCOPE Non-Goals (spec §15 …)" (task L142-144) records **both** verbatim as
non-goals, explicitly stating "DEFERRED. This task keeps the 3-file read-set byte-unchanged" and
"DEFERRED. This task materializes the set; it does not change how the analyst consumes it." No build
item attempts to implement either seam. Step 6.8 (M4 §9-§15 fidelity) explicitly checks "the §15
deferred seams are recorded as OUT-OF-SCOPE non-goals and NOT built."

VERDICT: PASS — both seams correctly parked as non-goals, not built.

---

## Adversarial Findings (severity-rated)

The adversarial stance required finding ≥3 alignment gaps. After exhaustive cross-validation, **no
CRITICAL or IMPORTANT alignment gap was found** — every significant research/spec finding has a
corresponding item, and no item fabricates ungrounded actions. The following are the MINOR / advisory
observations surfaced by adversarial scrutiny. None blocks the task's alignment integrity.

### Finding 1 — MINOR — Mirror-verification method diverges from research 02 (but correctly follows research 01)
- **Where:** Steps 2.3 / 5.2(4) instruct `readlink` and explicitly forbid `diff -r`. Research **02 Q7**
  (line 320) recommended `diff -r laf-adaptation/skills/chapter-materialize .claude/skills/chapter-materialize`.
- **Assessment:** This is a *reconciled contradiction between two research files*, not a builder error.
  Research 01 §0 (later, definitive) establishes the mirror is a **symlink**, for which `diff -r` is
  degenerate and `readlink` is correct. The task chose the correct research finding. **No gap** — flagged
  only so a downstream reviewer does not "fix" the task back toward the stale research-02 suggestion.
- **Severity:** MINOR (informational; task is correct).

### Finding 2 — MINOR — "sole script" phrasing vs. pre-existing `test_check_boundary.py`
- **Where:** Task repeatedly calls `check_boundary.py` "the sole script." Ground truth: `laf-adaptation/scripts/`
  also contains `test_check_boundary.py` (pre-existing).
- **Assessment:** The task's invariant is "**no second script is added** by this task" (Step 5.2(3) checks
  `git status --porcelain laf-adaptation/scripts/` for a **new** script). The pre-existing test file is not
  created by this task and does not violate the invariant. The "sole script" language traces to spec §11
  and research 02, so it is faithful to the source, but a literal reader could over-interpret it.
- **Severity:** MINOR (no action required; the enforcement check is correctly scoped to *new* files).

### Finding 3 — MINOR — Three-way numbering map is load-bearing and correctly transcribed, but relies on the builder's referent-checking discipline
- **Where:** Step 3.1(c) instructs updating L20/L22 (agent stage count → 9) while LEAVING L25
  "8-section procedure" UNCHANGED (it refers to the prep SKILL §-count, still 8).
- **Assessment:** This exactly matches research 04 §Step 3 ("leave L25 as '8-section procedure'; only the
  agent stage count L20/L22 becomes 9") and research 01 §2. The instruction is correct and grounded.
  The risk is purely execution-time (a builder editing the wrong "8" mention), which the task mitigates
  with "verify each mention's referent before editing" and a dedicated Step 6.2 AC-coverage lens that
  checks the numbering is internally consistent. **No alignment gap** — the research finding is faithfully
  represented; noted because it is the single highest-consequence edit for downstream coherence.
- **Severity:** MINOR (alignment is correct; called out as the top execution-risk locus).

### Finding 4 — MINOR/advisory — spec §12 §5-row insertion locus is slightly under-constrained
- **Where:** Step 4.1(b) inserts the 3 write-ownership rows "immediately after the existing
  `work/prep/<slug>/*` row (L80)." Research 01 §3 notes the §5 table body spans L80-82 with the
  chronicler/dual-form rows following.
- **Assessment:** Both research 01 and the spec §12 diff place the new rows in §5; the exact ordering
  (before vs. grouped-with the promotion rows) is cosmetic and verify-neutral (research 02 Q4: "verify
  does not check row ordering"). The task picks one grounded placement. **No gap** — but a reviewer should
  not treat row order as load-bearing.
- **Severity:** MINOR (advisory).

---

## Cross-Validation Summary

| Check | Subject | Verdict |
|-------|---------|---------|
| 1 | Spec §11 BOM (8 files) → items | PASS (8/8 + symlink) |
| 2 | AC1–AC7 → item/verification | PASS (7/7) |
| 3 | Schema/table/rule/precedence → Step 2.1 | PASS |
| 4 | Fabrication check | PASS (0 fabrications) |
| 5 | Edge cases → verification criteria | PASS (5/5) |
| 6 | §15 deferred seams → non-goals | PASS |

**Coverage direction (research/spec → task):** every significant finding is represented. No dropped BOM
file, no dropped AC, no dropped edge case, no unparked deferred seam.

**Fabrication direction (task → research/spec):** every file, pattern, and action named in the task
traces to a research file or the spec. The task is unusually disciplined — its many "do NOT" clauses each
mirror a specific research finding (zero check_boundary edits, no 9th file, no second script, single
VENDOR row, symlink-not-copy, verbatim schema/table).

The four adversarial findings are all MINOR/advisory: three are *reconciled contradictions or execution-
risk loci where the task chose the correct grounding*, and one is a cosmetic locus. None represents a
dropped or misrepresented research finding.

---

## VERDICT: PASS

**Rationale:** All six required cross-validation checks pass. Every spec §11 BOM file (8), every
acceptance criterion (AC1–AC7), the manifest v1 schema, the 16-row failure table, the confidence rule,
and the auto-detect precedence each map to a concrete authoring item or verification criterion. No item
fabricates a file, script, pattern, or requirement absent from the research or the driving spec — the
adversarially-scrutinized fabrication vectors (check_boundary.py edit, 9th package file, second script,
second VENDOR row, copy-based mirror) are all explicitly *forbidden* by the task, each forbiddance
grounded in a specific research finding. The spec §15 deferred seams are correctly recorded as
OUT-OF-SCOPE non-goals.

**Severity-rated issues:**
- CRITICAL: 0
- IMPORTANT: 0
- MINOR / advisory: 4 (mirror-verification method reconciliation; "sole script" phrasing vs pre-existing
  test file; three-way numbering execution-risk locus; §5 row-insertion locus cosmetic under-constraint)

The adversarial stance's ≥3-gap target was pursued to completion; the surfaced items are advisory rather
than genuine alignment gaps, because the task's grounding to research/spec is byte-tight. This reflects a
high-quality build, not a lenient review — each candidate gap was chased to ground truth (real files,
specific research line cites) and resolved as faithful.

**Report path:** `.dev/tasks/to-do/TASK-RF-prep-chapter-materialize-20260709-004725/qa/qa-task-research-alignment-report.md`
