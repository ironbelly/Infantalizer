# Phase Gate 3 — Consolidated QA Findings (Step PG3.4)

**Compiled:** 2026-07-04 | **Sources:** 7 lens reports

## Lens verdict rollup
| Lens | Verdict | Issues |
|------|---------|--------|
| template-conformance | PASS | 0 (3 MINOR) |
| internal-consistency | FAIL | 6 (3 IMPORTANT, 3 MINOR) |
| evidence-quality | PASS | 4 (1 IMPORTANT, 3 MINOR) |
| completeness | PASS | 2 (MINOR) |
| actionability | FAIL | 5 (3 IMPORTANT, 2 MINOR) |
| boundary-contract-fidelity | PASS | 0 |
| domain-accuracy | FAIL | 5 (1 CRITICAL, 3 IMPORTANT, 1 MINOR) |

**Core gate conditions remain genuinely GREEN** (boundary exit 0, invariants hold, runs happened, provenance
correct). The findings are accuracy/consistency defects in the proof-run artifacts + honesty of the reports.

## Fix procedure (ORDERED — apply top to bottom; edits are cross-dependent)

### D1 [CRITICAL/IMPORTANT] Source fixture leaked a T1 label + ambiguous king death
`laf-adaptation/source/tolkien/ch-01.txt` — the SOURCE must use source framing (no tier-1 labels) and make
the king's death explicit so the analyst can tag it and T3's "died" is faithful.
- Replace: `and one of the Grumpy Riders — the Nazgûl, they were named, and their cry unmanned brave men — struck the king from his horse, and he fell.`
- With: `and one of the Nazgûl — dark riders whose cry unmanned brave men — struck the king from his horse. Théoden fell, and did not rise again.`

### D2 [CRITICAL] analysis.yaml self-contradiction on the king's death
`laf-adaptation/work/analysis/ch-01.yaml`:
- In `events` seq 5, change the event text to reflect the now-explicit death: `A Nazgûl strikes the king from his horse; Théoden falls and does not rise again.`
- In `uncertainties`, DELETE the line: `"Whether the fallen king dies or is only unhorsed is not made explicit in the closing text (he 'fell'); downstream death-handling should treat it per the active tier."` (the source now makes it explicit; keep only the title-inference uncertainty).
- Then re-copy this file over the 3 promoted copies: `kb/adaptations/tolkien/tier-{1,3,5}/chapters/ch-01/analysis.yaml`.

### D3 [IMPORTANT] T5 near-source draft must match the corrected source
`laf-adaptation/work/drafts/ch-01-t5-v1.md` (T5 = preserve author intent):
- Replace: `one of the\nNazgûl — their cry unmanned brave men — struck the king from his horse, and he fell.` (the sentence spanning the Nazgûl strike)
- With source-faithful text: `one of the\nNazgûl — dark riders whose cry unmanned brave men — struck the king from his horse. Théoden fell, and did not rise again.`
- Then re-copy: `cp work/drafts/ch-01-t5-v1.md kb/adaptations/tolkien/tier-5/chapters/ch-01/adapted.md`.
(T3 already says "Théoden died" — now faithful; T1 correctly renders the death as "grew very tired and sat right down". No change to T1/T3 drafts needed beyond confirming consistency.)

### D4 [IMPORTANT] Quotation drift — the T1 Théoden rendering quoted 3 ways
Align all three to the ACTUAL v2 draft text `grew very tired and sat right down`:
- `laf-adaptation/work/analysis/ch-01-cross-tier.md`: in the traceability table, change the T1 cell for "Théoden's fall" from `"grew very tired and sat down to rest"` to `"grew very tired and sat right down"`.
- `phase-outputs/reports/phase-3-hard-gate-report.md` (in the task dir): change `"grew tired and rested" (T1)` to `"grew very tired and sat right down" (T1)`.
- `phase-outputs/test-results/phase3-fanout-summary.md`: same alignment where the T1 rendering is quoted.

### D5 [IMPORTANT] Fan-out summary overstates T3/T5 pipeline
`phase-outputs/test-results/phase3-fanout-summary.md`: the full review quartet ran ONCE at T1 (per the
gate's quartet condition scope); T3/T5 ran writer(transform) + safety(advisory/N-A) + were reconciled by
tier-coordinator + promoted by chronicler. Reword any claim that "each tier ran steps 3-9 independently"
to state this accurately (T1 ran the full 11-step pipeline incl. the quartet; T3/T5 ran the
transform+safety+reconcile+chronicle path; the fan-out proves tier-differentiation + reconciliation).
Mirror the correction in `phase3-fanout-raw.txt` if it makes the same claim.

### D6 [IMPORTANT evidence] Stale "FAIL" line in the T1 raw capture
`phase-outputs/test-results/phase3-t1-run-raw.txt` contains `FAIL: transformed name leaked to shared canon`
— a false positive from grepping an explanatory comment that was later reworded. Regenerate the capture by
re-running the Inv.3 check now (the shared canon is clean): overwrite the file's Inv.3 line so it reads
`PASS: no transformed name in shared kb/canon/tolkien/ch-01.md`. (Verify first with
`grep -rli "grumpy king" laf-adaptation/kb/canon/ laf-adaptation/kb/timeline/` → must be empty.)

### D7 [MINOR] Wording overreach + traceability
- `phase-outputs/reviews/gate-cond3-canon.md` and the run summaries: change "'Grumpy King' appears **only**
  under `kb/adaptations/tolkien/tier-1/`" to "...only under the per-tier tier-1 canon and the work-mapping
  config `kb/adaptation-mapping/tolkien-mapping.yaml`, never in shared `kb/canon/`/`kb/timeline/`".
- `phase-outputs/reviews/gate-cond5-boundary.md`: record the concrete `--upstream` checkout path
  (`.dev/releases/current/0.1/creative-writing-skills`, SHA 3338495f0fabf778720effdda9386ab56d4ebf6e) and
  note that plain verify mode skips Rules B/C (they hold under `--upstream`, which was run and also exit 0).

### D8 [IMPORTANT actionability] Reports not self-contained on failure paths
Add a brief failure-path note to `phase-outputs/reports/phase-3-hard-gate-report.md`: state what a RED
verdict entails (HALT, name the failing condition + remediation) and that a tier-coordinator CONFLICT
(non-empty `conflicts:`) would list `{type, tier, element}` and block chronicler until the offending tier's
writer is re-dispatched, and that a safety FAIL would populate `verdict.evidence` with `{section, location}`
revision targets. (One short paragraph; the happy path here is conflicts:[]/evidence:[]/GREEN.)

## After all edits
1. Re-copy the two affected adapted.md (T5) + promoted analysis.yaml (×3).
2. Regenerate the T1 raw capture's Inv.3 line (D6).
3. Run `uv run python laf-adaptation/scripts/check_boundary.py` — MUST stay exit 0 (none of these touch
   adopted files, the manifest, or Rule-F-scanned paths).
4. Confirm the hard-gate remains GREEN (the 5 conditions are unaffected: the fixes improve accuracy, they do
   not change any PASS→FAIL).

## Constraints
NEVER edit an adopted file or the VENDOR.md manifest table or any carried-verbatim kb/tiers, adaptation-mapping,
or resource YAML payload. The source fixture, proof-run drafts/analysis/canon, and the phase-outputs reports
are the only editable targets.
