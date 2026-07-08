# Phase Gate 2 — Consolidated QA Findings (Step PG2.4)

**Compiled:** 2026-07-03 | **Sources:** 7 lens reports (4 structural + 3 content)

## Lens verdict rollup

| Lens | Verdict | Blocking issues |
|------|---------|-----------------|
| template-conformance | PASS | 0 |
| internal-consistency | FAIL | 5 (3 IMPORTANT, 2 MINOR) |
| evidence-quality | FAIL | 2 (1 IMPORTANT, 1 MINOR) |
| completeness | PASS | 0 |
| actionability | FAIL | 6 (2 CRITICAL, 3 IMPORTANT, 1 MINOR) + 1 cross-cutting |
| boundary-contract-fidelity | PASS | 0 (1 MINOR wording note) |
| domain-accuracy | PASS | 0 |

**Boundary gate GREEN** (`check_boundary.py` exit 0, A–F). Genuine build defects are narrow; most
actionability findings are design-level abstractions the specs themselves carry (like Phase-1 F7).

## GENUINE BUILD DEFECTS — fix (corrective/additive to native prose only)

| ID | Sev | File | Issue | Fix |
|----|-----|------|-------|-----|
| D1 | IMPORTANT | `skills/adaptation-safety/resources/children.md` | The Denethor Tier-3 example is presented inside quote marks as a verbatim carry but drops sentences and stitches with `…` — a paraphrase masquerading as a verbatim quote (evidence-quality F1). | Replace the abbreviated stitched quote with the FULL verbatim T3 Denethor passage from `prompts/transformation/tier_3_transform.md`, OR clearly relabel it as an "excerpt (abridged)" so it does not read as verbatim. Prefer full verbatim. |
| D2 | MINOR | `skills/adaptation-safety/resources/children.md` | The Denethor example is attributed to "the transform prompts" (plural); both the T1 and T3 halves live in `tier_3_transform.md`'s worked example (the T1 prompt's worked example is Éowyn) (evidence-quality F2). | Correct the attribution to `prompts/transformation/tier_3_transform.md` (its T1→T3 worked example). |
| D3 | IMPORTANT | `agents/chronicler.md` | Write-targets omit the on-accept promotion of `chapters/ch-<NN>/analysis.yaml` that kb-formats §4 assigns ("copy of work/analysis/ch-NN.yaml, promoted on accept"); the promotion is unowned (internal-consistency Check 1). | Add to chronicler's write targets: on accept, promote `analysis.yaml` (copy of `work/analysis/ch-<NN>.yaml`) into `kb/adaptations/<work>/tier-<N>/chapters/ch-<NN>/`. Note `adapted.md` is provided as the `adapted_path` INPUT (already at that path from the tier pipeline). |
| D4 | IMPORTANT | `skills/adaptation-safety/SKILL.md` (aggregation `next` line) | The carried aggregation formula `next = revise if overall==FAIL else promote` computes `next=revise` for a T3-advisory FAIL, diverging from `safety-verifier.md`'s deterministic F6 rule (advisory always promotes). The two files disagree (internal-consistency Check 3 / actionability F-6). | Align the SKILL's `next` with the F6 rule (additive note): `next = revise` ONLY when `mode==blocking AND result==FAIL`; for `mode==advisory` (T3) and `mode==skipped` (T4-5), `next = promote` (report-only). Keep the carried formula but annotate it so the two files agree. |

## EXECUTABILITY GAPS — resolve with spec-consistent operational-reading notes (additive; same pattern as Phase-1 F7)

| ID | Sev | File | Gap | Operational-reading note to add |
|----|-----|------|-----|----------------------------------|
| E1 | CRITICAL(design) | `agents/tier-coordinator.md` | Check B (`disclosures`/`permitted_at`) and Check C (`maturity()`) reference abstract concepts the spec §3 defines only ordinally (actionability F-3/F-4). Carried verbatim from tier-coordinator.md §3 — a design abstraction, not a carry defect. | Add an "Operational reading" note (keeping the spec pseudocode intact): ground `maturity()` in concrete tier-profile fields — the element's governing `mode:` on the ladder (`mandatory`<`optional`<`preserve`) plus `kb/tiers/tier_<N>.yaml` `thresholds.violence.level` and `thresholds.moral_ambiguity.level`; ground `permitted_at(disclosure, tier)` in the tier's `transformation_rules.death_handling`/`conflict_*` strategy (e.g. T1 `death` deferred via `journey_or_sleep` ⇒ a death disclosure is NOT permitted at T1). |
| E2 | IMPORTANT(design) | `agents/chronicler.md` | Invariants 1 & 3 not shown as mechanically checkable — no stated write-format carries the `(work,tier,chapter)` key; `continuity.md` path has no chapter coordinate (actionability F-1/F-2). | Add a note on how the key is materialized: `work`+`tier` are encoded in the directory path (`kb/adaptations/<work>/tier-<N>/`); `chapter` is encoded in the per-chapter path (`chapters/ch-<NN>/`) and stamped on each appended `continuity.md`/`decisions.md` entry (continuity.md is per-tier RUNNING state across chapters by design, so the chapter lives on the entry, not the dir). Inv.3 name-check: before writing to shared `kb/canon/`, confirm the fact uses the source name from `analysis.yaml`, not a tier-transformed name. |
| E3 | MINOR(design) | `agents/tier-coordinator.md` / CLAUDE.md | The numbered 11-step workflow that agents branch on ("step 3/10/11") is defined in DESIGN.md §3 (build-time), not in-tree (actionability cross-cutting). | Add a one-line pointer in tier-coordinator/chronicler (or note in CLAUDE.md) that the step numbers reference the per-chapter 11-step workflow (analyst→muse→writer→critic→editor→writer→continuity-checker→safety-verifier→reader-sim→tier-coordinator→chronicler), proven end-to-end by the Phase-3 hard gate. |

## Notes / no-fix

- boundary-fidelity MINOR: chronicler is roster-documented upstream (README/docs) but unshipped as a `cw/`
  file — "vapor in both systems" is a task/design wording nuance, not a built-artifact defect. Rule E
  (filename collision vs `cw/`) holds. NO built-artifact fix.
- E1/E2/E3 are design-level; the operational-reading notes make them executable WITHOUT contradicting or
  rewriting the spec-carried text. Do NOT touch any carried-verbatim YAML payload.

## Fix scope + constraints for the PG2.4 fix agent

Edit ONLY these BUILD-NEW native bodies: `agents/chronicler.md`, `agents/tier-coordinator.md`,
`skills/adaptation-safety/SKILL.md`, `skills/adaptation-safety/resources/children.md`. (E3 may add a line
to CLAUDE.md.) NEVER edit an adopted file, a NATIVE Phase-1 file unless needed, or any carried-verbatim
YAML payload / kb file / template. After fixes, re-run `check_boundary.py` — must stay exit 0.
