# QA Report — Domain-Accuracy Lens (Phase 3 outputs vs DESIGN.md §3)

**Topic:** LAF 0.1 hybrid build — Phase 3 compose-and-prove
**Date:** 2026-07-04
**Phase:** doc-qualitative (domain-accuracy overlay)
**Fix authorization:** FALSE — report only
**Verdict:** PENDING

---

## Scope

Adversarial domain-accuracy audit of Phase-3 outputs against DESIGN.md §3 (11-step workflow + provenance).
Assume >=5 domain-accuracy errors exist. Zero-trust every provenance attribution, every tier rendering, every fan-out claim.

CHECKS:
1. 11-step provenance tally correct in run summary
2. Tier-differentiated framing REAL (T1 max-transformed / T5 near-source / T3 in-between)
3. Parallel-fan-out topology correct (analyst once shared, tier-coordinator fans T1/3/5)

---

## Overall Verdict: FAIL

5 domain-accuracy issues found (1 CRITICAL, 3 IMPORTANT, 1 MINOR). The three headline CHECKS
(provenance tally, tier-differentiation, fan-out topology) are each substantially correct at the
run-summary level, but adversarial artifact-vs-claim cross-checking surfaced defects the summaries
paper over: an internally-contradictory source analysis, an UNCERTAIN death hardened to CERTAIN at T3,
a fan-out that claims "steps 3-9 per tier" but only ran the quartet + revision loop for T1, and a T5
"near-verbatim" draft that silently diverges from its declared source.

---

## CHECK 1 — 11-step provenance tally

**Result: PASS (with one SPEC-internal ambiguity noted, not a run-summary defect).**

Canonical tally (per CHECK 1 + DESIGN §3 data-flow labels), cross-checked against
`phase3-t1-run-summary.md` per-step Provenance column:

| Step | Agent | Canonical | Run-summary label | Match |
|------|-------|-----------|-------------------|-------|
| 1 | analyst | NATIVE | NATIVE | ✓ |
| 2 | muse | ADOPTED | ADOPTED | ✓ |
| 3 | writer | ADOPTED (+native skill) | ADOPTED + /adaptation-rules | ✓ |
| 4 | critic | ADOPTED | ADOPTED (quartet) | ✓ |
| 5 | editor | ADOPTED | ADOPTED (quartet, never folded) | ✓ |
| 6 | writer revision | ADOPTED | ADOPTED | ✓ |
| 7 | continuity-checker | ADOPTED | ADOPTED (quartet) | ✓ |
| 8 | safety-verifier | NATIVE | NATIVE | ✓ |
| 9 | reader-sim | ADOPTED | ADOPTED (quartet) | ✓ |
| 10 | tier-coordinator | BUILD-NEW | BUILD-NEW | ✓ |
| 11 | chronicler | BUILD-NEW | BUILD-NEW | ✓ |

Every provenance attribution matches the canonical tally. analyst + safety-verifier = NATIVE ✓;
critic/editor/reader-sim/continuity-checker + muse + writer = ADOPTED ✓; tier-coordinator + chronicler
= BUILD-NEW ✓. No folded agent, no wrong provenance in the tally itself.

**Noted (SPEC-internal, not a Phase-3 output defect):** DESIGN §3's ASCII data-flow draws the "review
quartet (constraint #4)" box around steps 4/5/6/7 — i.e. it visually includes *writer-revision* (step 6)
and *excludes* reader-sim (step 9) from the quartet box, whereas DESIGN §1.2's review-lineup table (and
CHECK 1) define the quartet as critic/editor/reader-sim/continuity-checker. The run summary correctly
follows the §1.2 / CHECK-1 definition. This is a DESIGN.md drafting inconsistency, not a run-summary
error — flagged for spec cleanup, not gating this review.

---

## CHECK 2 — Tier-differentiated framing is REAL

**Result: PASS for differentiation; but two fidelity defects inside the tier renderings.**

Differentiation is genuine and non-collapsed. No two tiers are indistinguishable:

| Element | T1 (max transform) | T3 (transition) | T5 (near-source) |
|---------|--------------------|-----------------| -----------------|
| Sauron | "The Grumpy King" (no sunshine) | "Sauron", cold will, true menace | "Sauron", as source |
| Théoden's fall | "grew very tired and sat right down" (rest-not-death) | "Théoden died" (direct) | "he fell" (source ambiguity preserved) |
| Nazgûl | "Grumpy Riders", shy shadow, smiles | "the Nazgûl … cry drained courage" | "the Nazgûl … cry unmanned brave men" |
| Denethor | "Sad Leader", windows reopened | "given way … despair" | "something had already broken" |
| deaths | deferred (rest) | disclosed ("died", grief) | preserved ("would not rise") |

T1 is maximally transformed (Grumpy King / Big Tidy-Up / rest-not-death), T5 is near-source (Sauron,
"he fell", deaths preserved), T3 sits between (Sauron menace, "died" direct). Confirmed distinct. See
ISSUE-2 and ISSUE-5 for the fidelity defects that ride inside this otherwise-real differentiation.

---

## CHECK 3 — Parallel-fan-out topology

**Result: PARTIAL — analyst-once is TRUE; but the "steps 3-9 per tier" claim is overstated (ISSUE-3).**

TRUE parts, artifact-verified:
- **analyst ran once (shared):** the three promoted `analysis.yaml` (tier-1/3/5) are byte-identical
  copies of the single `work/analysis/ch-01.yaml`; the shared analysis carries no `active_tier` and
  defers death-handling to the tier (correctly tier-invariant). ✓
- **tier-coordinator fanned T1/3/5:** `ch-01-cross-tier.md` reconciles all three, status RECONCILED,
  conflicts []. ✓
- **chronicler ran per tier:** all three tier dirs hold the full canon set (adapted/analysis/canon-delta
  /continuity/decisions). My first `find | head` was truncated and hid tier-3/tier-5 — re-enumeration
  confirms all three tiers' canon exists on disk. No folded tier. ✓
- **no shared-canon name leak:** grep confirms "Grumpy King"/"Grumpy Rider"/"Sad Leader"/"Tidy" appear
  ONLY under `kb/adaptations/tolkien/tier-1/`; shared `kb/canon/` + `kb/timeline/` hold source names
  only (Inv.3 holds). ✓

OVERSTATED part — see ISSUE-3: the fan-out summary claims each tier "ran steps 3-9 independently," but
only T1 has quartet critique reports and a v2 revision on disk.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `work/analysis/ch-01.yaml` L34 vs L39 | **Self-contradictory source analysis on the king's death.** `transformation_flags.death: {instances: 2}` counts the king's death as a hard flagged death-instance, but `uncertainties` L39 explicitly says "Whether the fallen king dies or is only unhorsed is **not made explicit** … treat it per the active tier." The same artifact both asserts and disclaims the king's death certainty. Under the v2.0 source-fidelity protocol an UNCERTAIN fact must not be silently counted as a CERTAIN death instance. This is the shared truth every tier reads, so the defect propagates. | Reconcile: either downgrade the king's death out of `death.instances` (count only the soldiers' "would not rise" as the CERTAIN death), or promote the uncertainty note; the two lines must agree. The soldiers' death is CERTAIN; the king's is UNCERTAIN — the flag count must reflect that split. |
| 2 | IMPORTANT | `tier-3/continuity.md`, `drafts/ch-01-t3-v1.md` L7 | **T3 hardens an UNCERTAIN source fact to CERTAIN.** The shared analysis marks the king's death UNCERTAIN (L39), yet T3 asserts "Théoden **died**" as a flat durable canon fact in continuity.md and the draft. T5 correctly preserves the ambiguity ("he fell"); T3 over-asserts. This is exactly the v2.0 discipline the NATIVE spine exists to enforce, violated in a promoted per-tier canon. | T3 death-handling should render the fall as direct-but-not-invented (e.g. "was struck down and did not rise" tracks the source) OR the analyst must first resolve the king's death to CERTAIN with evidence. Do not manufacture a CERTAIN "died" from an UNCERTAIN source. |
| 3 | IMPORTANT | `phase3-fanout-summary.md` L8-9; `phase3-fanout-raw.txt` L3-6 | **Fan-out claims "steps 3-9 per tier" but T3/T5 skipped the quartet + revision loop.** The summary states each tier "ran steps 3-9 independently." On disk, ONLY T1 has quartet critique reports (critic/editor/continuity/reader-sim) and a v2 revision draft. T3 and T5 have zero critique reports and no v2 — only a v1 adapted draft (writer step 3) → safety (step 8) → chronicler. Steps 4/5/6/7/9 produced no T3/T5 artifacts. The claim reads as if all three tiers got the full pipeline; only T1 did. This is the "undifferentiated execution rendering" the audit was told to hunt: the fan-out folds T3/T5 down to writer→safety→chronicler while claiming steps 3-9. | Correct the fan-out summary to state accurately which steps each tier ran (T1 = full 3-9 + revision loop; T3/T5 = step 3 + step 8 + chronicler, quartet not re-run per tier), OR actually run the quartet + revision per tier if the gate requires "all four quartet agents ran" per tier. As written the summary overstates coverage. |
| 4 | IMPORTANT | `source/tolkien/ch-01.txt` L14 | **Source fixture is contaminated with a T1-transformed name.** The declared read-only source-of-truth says "Grumpy Riders — the Nazgûl, they were named". "Grumpy Riders" is a Tier-1 transformation label (it appears as the T1 rendering of the Nazgûl in `tier_1` canon), not source prose. A pristine Tolkien-style source should say "the Nazgûl" / "the Ringwraiths". This contaminates the tier-invariant baseline that every tier and the analyst trace to. | Clean the source fixture L14 to source-register naming ("the Nazgûl" / "the dread riders"); re-run analyst so the shared analysis traces to an uncontaminated baseline. Note this is the root cause of ISSUE-5. |
| 5 | MINOR | `drafts/ch-01-t5-v1.md` L19 vs `source/tolkien/ch-01.txt` L14 | **T5 "near-verbatim" draft silently diverges from its declared source.** T5 policy header says "The source is rendered near-verbatim." But the source L14 reads "Grumpy Riders — the Nazgûl, they were named"; the T5 draft L19 reads "the Nazgûl" — T5 silently dropped the "Grumpy Riders" phrase. The correction is *better* prose (see ISSUE-4), but it is an undisclosed deviation from a "preserve author intent / near-verbatim" tier. A near-source tier should either preserve verbatim or footnote the deviation. | Once ISSUE-4 cleans the source, T5 should render verbatim from it. If T5 corrects a source artifact, that is a substantive transform and must be disclosed (T5's own comment block reserves changes to "genuine access barriers", which this is not). |

---

## Self-Audit

**(a) Reliance list — structural PASS items skipped for structural re-check:**
- Relied on prior structural QA for section numbering, file-existence, boundary-contract (check_boundary)
  green, and template conformance of the run summaries. This lens is domain-accuracy only.

**(b) Independent semantic checks (tool-verified):**
- Provenance tally — Read `phase3-t1-run-summary.md` per-step column, cross-checked each against DESIGN.md
  §3 data-flow labels and CHECK-1 canonical tally (11/11 match). Tool: Read.
- analyst-once — Bash `head -6` on all three promoted `analysis.yaml` proved byte-identical shared
  analysis + grep confirmed no `active_tier` in shared analysis. Tool: Bash/grep.
- No folded tier / no canon leak — `find kb/adaptations -type f` enumerated all 3 tiers' full canon sets;
  grep proved "Grumpy King" absent from shared canon/timeline. Tool: Bash/find/grep.
- Tier differentiation — Read all three `adapted.md` + all three continuity.md; built the element×tier
  matrix directly from prose. Tool: Read.
- Death-certainty contradiction (ISSUE-1/2) — Read `work/analysis/ch-01.yaml` L34 vs L39 and traced the
  UNCERTAIN flag into T3's "died". Tool: Read.
- Quartet-per-tier coverage (ISSUE-3) — `ls work/critique-reports/` + `ls work/drafts/` proved only T1
  has quartet reports + v2. Tool: Bash/ls.
- Source contamination + T5 divergence (ISSUE-4/5) — grep "grumpy rider|nazg" across source + T5 draft.
  Tool: Bash/grep.

**Confidence:** Verified: 3/3 CHECKS fully artifact-cross-checked | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 9 | Grep/Bash: 5 | Glob(find): included in Bash

No web research was performed (all verification was local-file-bound); Tavily precedence not triggered.

## QA Complete
