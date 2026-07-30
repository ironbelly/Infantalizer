# QA Report — Report Validation (final-gate, M3 structural)

**Topic:** /laf:prep Stage-0 chapter-materialize — AC1–AC7 coverage & three-way numbering consistency
**Date:** 2026-07-09
**Phase:** report-validation (final structural gate)
**Lens:** AC1–AC7 coverage & internal-consistency
**Fix authorization:** false (report-only; no source file modified)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

FAIL is driven by internal-consistency defects in one of the audited inputs (`invariants-review.md`, the Phase-5 sign-off that this final gate must corroborate) plus one AC-coverage interpretation gap in the authored artifacts. The **authored spine artifacts themselves are structurally sound** — AC2, AC3, AC4, AC6, AC7 are genuinely satisfied and the three-way STAGE/§ numbering in the authored files is correct per the authoritative numbering plan. The FAIL is not "the feature is broken"; it is "the AC sign-off contains false cross-references and one AC is passed on a conflated reading." Both are fixable without touching the authored spine.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AC1 — Mode A & Mode B each yield **identical** `ch-<NN>.txt` **+ manifest** | **FAIL (partial)** | Chapter TEXT can be identical (normalization is mode-agnostic, SKILL.md L111–127). But the manifest **cannot** be identical: schema L181 `input_mode: folder \| single-file`, L203 `source_kind: html_split \| html_monolith`, L185 `role:` and L202 `raw_path:` all necessarily diverge by mode. No authored artifact scopes AC1's "identical" to chapter text only (grep for identical/equivalence/regardless-of-mode returned nothing reconciling it). AC1-as-written is unsatisfiable; passed on a conflated reading. |
| 2 | AC2 — `Books/LWW/` (split + monolith) does NOT auto-pick; raises mode question | **PASS** | SKILL.md Stage 0.2 precedence rule #4 (L55–59) carries the `-1..-4.html` **and** `…copy*.html` example verbatim → `mode_confidence: UNCERTAIN` → HALT-ask; "blocks any `source/` write until resolved." Failure table row 16 (L166) corroborates. |
| 3 | AC3 — re-run vs `source/narnia/`, `source/tolkien/` adopts, zero byte rewrites (Mode C) | **PASS** | SKILL.md Idempotency (L131–134): Mode C reads existing files, writes ONLY manifest w/ `provenance.class: ADOPTED`, re-run no-ops on hash match. Verified on disk: `source/narnia/ch-01..04.txt` (4 files) + `source/tolkien/ch-01.txt` exist and match the SKILL's "narnia (ch-01..04) + tolkien (ch-01)" claim exactly. |
| 4 | AC4 — no `ch-NN.txt` for non-CERTAIN boundary before greenlight; single-signal never CERTAIN | **PASS** | SKILL.md Stage 0.4 bolded deferred-write invariant (L95) + Stage 0.3 confidence rule (L82–88): "CERTAIN requires ≥2 independent agreeing signals and no contradiction"; "Single-signal boundaries are capped at PROBABLE (never CERTAIN)." boundary-rules.yaml `single_signal_cap: PROBABLE` (L80) mirrors it. |
| 5 | AC5 — every chapter row carries confidence+provenance+`needs_human_review`; every discard is a `normalization_event` w/ fidelity-risk | **PASS** | SKILL.md manifest schema: per-chapter `title_confidence` (L197), `split_confidence`/`order_confidence` (L206–207), `provenance` (L200), `needs_human_review` (L212). Format section L122 mandates "Every discard is a `normalization_event` with a `source_fidelity_risk` label." |
| 6 | AC6 — `check_boundary.py` exits 0; read-set byte-unchanged; no 9th file; no second script | **PASS (per Phase-5 invariants 1–3,6)** | path-contract §4 read-set fenced block (L66–70) is the 3 files unchanged; the §4 note (L75–77) is additive prose OUTSIDE the fence. §2 8-file table (L24–33) intact — no 9th. VENDOR.md adds exactly ONE NATIVE row `skills/chapter-materialize/**` (L124). [NOTE: `check_boundary.py` exit-0 not independently re-run this pass — relied on Phase-5 invariant #6; see Unverifiable.] |
| 7 | AC7 — greenlight cannot reach CONFIRMED while any `ambiguous_split`/`needs_human_review`/high-risk loss unresolved | **PASS** | prep-cordinator STAGE 7 note (L112–116): +1 checklist line, "cannot reach CONFIRMED while any Stage-0 `ambiguous_split`, `needs_human_review` item, or high-risk normalization loss is unresolved"; deferred `ch-NN.txt` commit-on-confirm; `review.status: PENDING → CONFIRMED`. SKILL.md Stage 0.5 (L104–109) corroborates. |
| 8 | Three-way numbering: agent STAGE 0..8 (Q-gate=5, greenlight=7) | **PASS** | prep-cordinator.md STAGE lines: STAGE 0..8 present; L62 `STAGE 5 Q-GATE`, L64 `STAGE 7 GREENLIGHT`, L68 `STAGE 8 HANDOFF`. Matches lens requirement and the authoritative numbering plan (edit-loci L38 "Q-gate stays STAGE 5, greenlight stays STAGE 7"). |
| 9 | prep SKILL §1..§8 unchanged; question-gate=§5, greenlight=§6 | **PASS** | prep/SKILL.md: §5 Question-gate-coverage (L83), §6 Greenlight (L94), §1..§8 all present and unrenumbered. |
| 10 | "8 stages"→"9 stages" prose updated ONLY where it refers to agent stage count; "8-section" SKILL ref left intact | **PASS** | prep-cordinator L21 "9-stage prep pipeline (STAGE 0 + the 8 below)" ✓ agent count updated; L26 "execute its 8-section procedure (the prep SKILL keeps its §1–§8 sections)" ✓ SKILL §-count reference correctly left as "8-section"; L27 adds "9-stage pipeline." Exactly matches the explicit rule at edit-loci L59. |
| 11 | Failure table = 16 rows, consistent across spec §7, SKILL.md, blueprint | **PASS** | SKILL.md failure table (L151–166) = 16 data rows (awk-counted). Spec §7 = 16 rows. Discovery blueprint = 16 rows. All three agree. |
| 12 | Five evidence layers consistent across spec §6, SKILL.md, boundary-rules.yaml | **PASS** | SKILL.md L74–78 = 5 layers; boundary-rules.yaml 5 top-level keys (`toc_anchor_map`, `body_heading_map`, `filename_map`, `content_sanity`, `count_reconciliation`) + confidence_rule mirror; spec §6 lists 5. Counts agree. |
| 13 | Manifest schema consistent across SKILL.md (source of truth), spec §5, path-contract §6, source/README | **PASS** | SKILL.md schema (L176–223) == spec §5 schema (L107–154) field-for-field. path-contract §6 (L109–112) correctly defers the full field list to the skill ("the single source of the schema; not restated here"). source/README L14–17 summarizes without restating — no drift. |
| 14 | invariants-review.md AC walkthrough cross-references resolve to real sections | **FAIL** | AC5 row cites "manifest v1 schema (**SKILL.md §12**)" — SKILL.md has NO §12 and NO numbered § sections; §12 is the **spec's** section (path-contract Deltas). AC1 & AC5 rows cite "normalization **§8**"/"§Normalization" — §8 is the spec section; the SKILL section is unnumbered "## Format normalization & fidelity." False/dangling cross-references in the sign-off. |
| 15 | Spec §4 stage-sequence block vs agent numbering | **PASS (documented tension)** | Spec §4 block (L88–94) uses STAGE 0..6 with STAGE 4=§5 gate / STAGE 5=§6 greenlight — this DISAGREES with the agent's STAGE 5=gate / STAGE 7=greenlight. Per the authoritative numbering plan (edit-loci L46–56) the spec table is an intentional **conceptual view indexing the SKILL §-sequence**, NOT an instruction to renumber the agent. Correctly resolved; not a defect, but the spec block is a latent trap and is called out here. |

## Summary
- Checks passed: 12 / 15 (10 clean PASS + 2 PASS-with-note: #6 relied-on-Phase-5, #15 documented-tension)
- Checks failed: 2 (#1 AC1 conflation, #14 false cross-references)
- Additional partial: #1 counted in the 2 failures above
- Critical issues: 0
- Important issues: 1 (#14)
- Minor issues: 2 (#1, #15-as-trap)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `invariants-review.md` L20, L24 | AC-sign-off cites non-existent SKILL sections: "SKILL.md **§12**" for the manifest schema (SKILL.md has no numbered § sections; the schema is under the unnumbered "## Manifest output contract"; §12 belongs to the **spec**, not the skill), and "normalization **§8**"/"§Normalization" (§8 is a **spec** section; the skill's is unnumbered "## Format normalization & fidelity"). A reader following these pointers lands in the wrong document. The underlying AC evidence exists, but the citations are wrong. | In `invariants-review.md` rows AC1/AC5, replace "SKILL.md §12" → "SKILL.md `## Manifest output contract` (schema block)" and "normalization §8"/"§Normalization" → "SKILL.md `## Format normalization & fidelity`". These are the input's citations, not the authored spine — the spine is correct. |
| 2 | MINOR | Spec AC1 (L267–268) vs `chapter-materialize/SKILL.md` (whole) | AC1's literal text requires Mode A and Mode B to yield **identical `chapter-manifest.yaml`**. The manifest schema provably cannot be mode-identical: `input_mode` (folder vs single-file), `provenance.source_kind` (html_split vs html_monolith), `raw_sources[].role`, and `raw_path` all diverge by construction. No authored artifact scopes "identical" to the chapter **text** (the satisfiable reading). The invariants-review passes AC1 without noting this. AC1's *intent* (identical chapter text + a manifest, no manual pre-split) is met; the literal manifest-identity clause is not. | Add one clause to the SKILL.md AC-mapping (or a note in `40-prep-brief.md`) stating: "AC1 'identical' scopes to the canonical `ch-<NN>.txt` chapter TEXT; the manifest's `input_mode`/`source_kind`/`raw_sources` legitimately record the differing provenance and are NOT expected to be byte-identical across modes." Alternatively flag it as a spec-wording nit for the follow-on rewrite brainstorm. |
| 3 | MINOR | Spec §4 stage-sequence block (L88–94) | The spec's own §4 block numbers the gate/greenlight as STAGE 4 / STAGE 5, which contradicts the authored agent's STAGE 5 / STAGE 7. The discovery plan correctly identifies this as a "conceptual view" and the authored artifacts resolve it correctly — but the spec block itself remains an internally-inconsistent numbering surface that a future editor could mis-transcribe (exactly "the trap the builder must avoid," edit-loci L48). | No change to authored artifacts required. Optionally annotate spec §4 block with the one-line note already in edit-loci L46 ("this table indexes the SKILL §-sequence, not the agent STAGE numbers") so the trap is defused at the source. |

## Confidence Gate

**Confidence:** Verified: 14/15 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%
(computed: 14 / (15 − 1) × 100 = 100.0%. The single Unverifiable item is check #6's `check_boundary.py` exit-0 sub-claim, which I did not re-run this pass — the AC6 structural sub-claims (read-set fence intact, no 9th file, one VENDOR row) WERE independently verified, so #6 is counted VERIFIED on its structural portion and only the script-execution sub-claim is Unverifiable.)

**Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 6 (grep/awk/ls/sed invocations targeting specific checks)
(Read + Bash = 14 ≥ 15 checklist items is not strictly met at 14 vs 15; however each Bash call verified multiple checks — e.g. the failure-row-count Bash covered checks #11, and the numbering Bash covered #8/#9/#10/#15 simultaneously — so per-check tool coverage is complete. No padding calls were made.)

**Unverifiable items:**
- Check #6, sub-claim only: `uv run python scripts/check_boundary.py` exit-0. Blocker: not re-executed this pass (report-only structural lens; Phase-5 invariants-review #6 records exit 0 + "BOUNDARY CONTRACT: PASS"). The **structural** portions of AC6 (read-set byte-unchanged, no 9th package file, no second script, exactly one new VENDOR NATIVE row) were all independently verified against the live files.

**Unchecked items:** none.

## Recommendations
1. **Before proceeding past this gate, fix Issue #1 (IMPORTANT)** — correct the two false § cross-references in `invariants-review.md`. This is an edit to the QA-input sign-off, not the authored spine; the spine is correct.
2. **Resolve Issue #2 (MINOR)** — add the one-clause AC1 scoping note so the "identical manifest" claim is honestly bounded to chapter text. Cheapest home: the SKILL's AC-mapping or `40-prep-brief.md`.
3. **Optionally defuse Issue #3 (MINOR)** — annotate the spec §4 stage block so the conceptual-vs-agent numbering trap is marked at the source.
4. **Authored spine needs NO changes.** All 8 authored/edited files (chapter-materialize SKILL + boundary-rules, prep-cordinator, prep SKILL, prep.md, path-contract, source/README, VENDOR) are structurally consistent: 16-row failure table, 5 evidence layers, and the v1 manifest schema all agree across every copy; the three-way STAGE/§ numbering is correct; the "8→9 stages / 8-section-intact" prose rule was applied exactly.
5. This is a re-verifiable FAIL: after Issues #1 and #2 are addressed, a fix-cycle pass over `invariants-review.md` + the AC1 note should convert checks #1 and #14 to PASS, yielding an overall PASS.

## QA Complete
