# A.10 Structural Validation — Consolidated Findings

Both lenses returned **VERDICT: PASS** with MINOR-only findings. No CRITICAL/IMPORTANT. The task file is
structurally sound. The following MINOR fixes are authorized for a single serialized fix pass (I20).

## Items Reviewed (PASS/FAIL passthrough for A.10.5 inheritance)

| Lens | Verdict | Blocking issues |
|---|---|---|
| b2-self-containment | PASS | none |
| phase-structure | PASS | none |
| TB-Add-1 (placeholders) | PASS | none |
| TB-Add-4 (DAG deps) | PASS | none |
| TB-Add-6 (verify-prefix) | PASS | none |
| TB-Add-7 (Exec-Context source-areas reappear) | PASS | none |
| TB-Add-8 (per-item evidence binding) | PASS | none |
| Frontmatter (spec_path/start_commit/executor_model_class/reflect_*) | PASS | none |
| Phase ordering vs DESIGN §7 P0→P4 | PASS | none |
| Boundary + empty-diff gates | PASS | none |
| POST reflect wrapper (flat, penultimate, guarded, exit-0) | PASS | none |
| QA gate floors (P0=5, P1=5, final=6) + serialized fix | PASS | none |

## Authorized MINOR fixes

1. **F1 — Step 4.1 command well-formedness check (≈line 303):** the runnable check greps only
   `^description:` but the verification prose also claims to confirm `argument-hint`. Add
   `grep -c '^argument-hint:' .claude/commands/laf/prep.md .claude/commands/laf/rewrite.md` (expect 1 each)
   to the runnable check so the assertion matches the prose.
2. **F2 — Steps 2.8 & 2.9 (≈lines 219, 223):** tighten the frontmatter assertion from qualitative
   ("carries the `argument-hint`") to quantitative — require "exactly one `description:` line AND exactly
   one `argument-hint:` line", parallel to the existing `description` wording.
3. **F3 — Overview phase-count wording (≈line 73 / Overview):** the prose says "five phases" but there are
   six `### Phase N:` headers (a Setup phase + P0–P4). Reword to "**five DESIGN.md §7 phases (P0–P4)** plus
   a Phase 1 setup phase (six `### Phase` sections total)" so the count is unambiguous.
4. **F4 — Line ≈71 "can be followed verbatim":** soften to "…can be followed verbatim **except the two
   documented staleness corrections below (Narnia→Tolkien; runtime-vs-build-time promotion)**" to remove the
   tension with the very next paragraph.

## NOT fixed (defensible as-is; recorded for the audit trail)

- **Step 2.11 asserts literal `NATIVE == 8`** rather than `baseline+3`. Baseline NATIVE=5 is verified live
  (research/06) and captured at Step 1.3; `8` is the correct expected value. Leave as-is (concrete assertion
  is stronger than an indirect reference).
- **Phase 4 (P2) uses a single-agent verification, not a ≥5 M3 gate.** P2 is a *static well-formedness
  check* (`ls` + `grep`), not a lens-based QA gate over a produced document, so the M3/I19 floor does not
  apply. Correctly scoped.
- **Six long single-artifact items (>250 words).** Each is atomic (one file), not a batch/split violation.

## Fixes Applied

Serialized fix pass (I20), `fix_authorization: true`. All 4 authorized MINOR fixes applied in-place;
NOT-fixed items left untouched. Landing lines re-read and confirmed post-edit.

- **F1 — Step 4.1 command well-formedness check (task file line 303):** Added a parallel
  `grep -c '^argument-hint:' .claude/commands/laf/prep.md .claude/commands/laf/rewrite.md` (expect 1 each)
  to the runnable check, and extended the verdict/assertion prose to require exactly one `argument-hint:`
  line each — the runnable check now matches the prose.
- **F2 — Steps 2.8 & 2.9 (task file lines 219 & 223):** Tightened the qualitative
  "carries exactly one `description:` line and the `argument-hint`" to the quantitative
  "carries exactly one `description:` line AND exactly one `argument-hint:` line" in both command-authoring items.
- **F3 — Task Overview phase-count wording (task file line 73):** Reworded to "five DESIGN.md §7 phases
  (P0–P4) plus a Phase 1 setup phase — six `### Phase` sections total", keeping the P0–P4 mapping intact.
- **F4 — "can be followed verbatim" sentence (task file line 71):** Appended
  "— except the two documented staleness corrections below (Narnia→Tolkien; runtime-vs-build-time promotion)"
  so it no longer contradicts the following staleness-correction paragraph.

NOT touched (defensible as-is, per instruction): Step 2.11 literal `NATIVE == 8`; Phase 4 (P2) single-agent
static well-formedness verification.

VERDICT: PASS
