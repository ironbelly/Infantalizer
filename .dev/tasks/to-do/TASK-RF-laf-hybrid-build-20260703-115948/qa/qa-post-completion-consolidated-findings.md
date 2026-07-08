# Post-Completion (Final Assembled-Output) — Consolidated QA Findings (Step PC.4)

**Compiled:** 2026-07-04 | **Sources:** 6 post-completion lens reports

## Lens verdict rollup
| Lens | Verdict | Issues |
|------|---------|--------|
| template-conformance | PASS | 0 |
| internal-consistency | FAIL | 7 (3 IMPORTANT, 4 MINOR) |
| evidence-quality | PASS | 0 |
| actionability | FAIL | 10 (4 IMPORTANT, 6 MINOR) |
| boundary-contract-fidelity | PASS | 0 |
| source-fidelity | PASS | 0 |

**The tree's STRUCTURE, byte-fidelity, and boundary contract are perfect** (4 lenses clean incl. the FINAL
boundary assertion and the full 9-file carried-verbatim corpus). All findings are **documentation-accuracy**
in the shipped docs (CLAUDE.md, UPSTREAM-SYNC.md) + 2 native bodies + 1 report — the root cause is that
CLAUDE.md/UPSTREAM-SYNC.md were authored in Phase 0/annotated forward-looking, and are now STALE because
**0.1 is DONE** and the complete 15-agent/16-skill tree exists.

## Fix plan (deduplicated into groups G1–G8). Targets: CLAUDE.md, UPSTREAM-SYNC.md, agents/analyst.md, skills/adaptation-safety/SKILL.md, phase-3-hard-gate-report.md. NO adopted/carried-verbatim file.

### G1 [IMPORTANT] Aspirational Phase-0 tense is now stale (0.1 DONE) — the map contradicts the territory
(actionability #1 source/ present-but-doc-says-absent, #3 tree counts stale, #5 UPSTREAM-SYNC "Phase 4" hedge; internal-consistency F-2)
- `laf-adaptation/CLAUDE.md`: rewrite the §1 present-state note (the "Phase-0 present-state — counts are target totals" paragraph) and the §4 "Where things live" tree so they describe the **COMPLETED** tree: all 15 agents + 16 skills present now. Remove the "+2 NATIVE +2 BUILD-NEW authored in Phases 1–2" forward annotations, the "source/ — created when the first work is adapted" and "templates/ — authored in Phase 1" hedges (both exist now), and any "target totals" framing. Keep a one-line "(built across Phases 0–2)" footnote if useful, but the live counts must be current.
- `laf-adaptation/CLAUDE.md` §2: drop the "(authored in Phase 4; present in the completed tree)" hedge on the UPSTREAM-SYNC.md reference → just "see UPSTREAM-SYNC.md".
- `laf-adaptation/UPSTREAM-SYNC.md`: drop any "authored in Phase 4 / not at Phase 0" self-description.

### G2 [IMPORTANT/MINOR] Classification completeness in the non-manifested note
(actionability #2 new-file-in-adopted-resources, #4 adopted-count clarity; internal-consistency F-1)
- `laf-adaptation/CLAUDE.md` non-manifested note: ADD a rule — "A new file authored inside an ADOPTED skill's `resources/` tree is a NATIVE addition: it must NOT collide with an upstream filename (Rule E) and is not hash-pinned; but prefer adding a NATIVE skill rather than a file inside an adopted skill dir (boundary contract)."
- Clarify the adopted-agent count: "11 adopted-provenance agents (10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED = writer.md)".
- Add one clarifying line that the VENDOR.md manifest has MORE rows (64) than the Rule-F glob set (31 = agents/*.md + skills/**/SKILL.md) because adopted skill `resources/**` are also hashed (for Rule A/B), which is broader than Rule-F's coverage requirement.

### G3 [IMPORTANT/MINOR] Cross-tree design-pack citations are not resolvable from the shipped tree
(actionability #7 DESIGN/boundary-contract not shipped, #9 ADR-006; internal-consistency F-3 inconsistent disclaimer, F-5 verdict-contract cited 3 ways)
- `laf-adaptation/CLAUDE.md`: add ONE consolidated note (e.g. at the end of §1 or in a short "References" line) stating: design-pack citations in this tree (`DESIGN.md`, `boundary-contract.md`, `kb-formats.md`, `safety-rubric.md`, `skill-specs.md`, `agent-schemas.md`, `tier-coordinator.md`, ADR-006) are **build-time provenance** living under `.dev/releases/current/0.1/design/`, NOT required for day-to-day contribution — the shipped docs are self-sufficient. This makes the many `§`-references consistent (they are all provenance, not runtime dependencies).

### G4 [IMPORTANT/MINOR] UPSTREAM-SYNC.md Step 1 + Step 6 not self-contained/executable
(actionability #6 11-step workflow unrunnable from docs, #8 Step 1 no command)
- `laf-adaptation/UPSTREAM-SYNC.md` Step 1: add the concrete command `git clone https://github.com/haowjy/creative-writing-skills <checkout>` (or `git fetch`) and note `<checkout>` is the `--upstream DIR` for Steps 2/5.
- Step 6: make self-contained — instead of only "re-run the Phase-3 hard gate (the 11-step workflow)", give the concrete re-run (`uv run python scripts/check_boundary.py`) AND inline the 5 gate conditions that must re-pass (v2.0 tags · safety PASS · per-tier canon · quartet ran · boundary green), and briefly name the 11-step workflow order (analyst→muse→writer→critic→editor→writer→continuity-checker→safety-verifier→reader-sim→tier-coordinator→chronicler) so Step 6 is runnable from the doc alone.

### G5 [IMPORTANT] adaptation-safety `next` pseudocode reads contradictory standalone
(internal-consistency F-4)
- `laf-adaptation/skills/adaptation-safety/SKILL.md`: on the aggregation pseudocode line `next = "revise" if overall == FAIL else "promote"`, append an inline pointer comment (e.g. `# see "Operational reading of next" below — revise ONLY when mode==blocking AND result==FAIL`) so the line does not read as contradicting the deterministic note when read in isolation. Do NOT delete the carried formula.

### G6 [IMPORTANT] CLAUDE.md overstates which agents take `active_tier`
(internal-consistency F-6)
- `laf-adaptation/CLAUDE.md` §3 tier-axis bullet: correct it — `active_tier` is an explicit input for **safety-verifier** and **chronicler**; **tier-coordinator** fans across a `tiers` set (subset of {1,2,3,5}); **writer** is ADOPTED-PATCHED and receives the tier via its scene brief + `/adaptation-rules` (not a declared frontmatter param); **analyst** is tier-invariant (no active_tier). Keep the T4-interpolated-never-stored line.

### G7 [MINOR] analyst status enum under-declared
(internal-consistency F-7)
- `laf-adaptation/agents/analyst.md` output-contract: note `status ∈ {OK, ABORTED}` — OK is the normal completion path (the hard-behavior block only shows the ABORTED branch); the runtime analysis emits `status: OK`.

### G8 [MINOR] hard-gate report RED-path only covers 2 of 5 conditions
(actionability #10)
- `.dev/tasks/.../phase-outputs/reports/phase-3-hard-gate-report.md` failure-paths paragraph: add one-line remediations for cond-1 (→ re-run analyst / restore ABORT-on-NO-ACCESS discipline; missing v2.0 tags), cond-3 (→ re-dispatch chronicler per-tier write), cond-4 (→ re-dispatch the missing quartet agent) so all 5 conditions have a concrete RED route.

## After edits
Run `uv run python laf-adaptation/scripts/check_boundary.py` — MUST stay exit 0 (none of these touch adopted
files, the manifest table, or Rule-F-scanned paths). Confirm no PASS→FAIL on the 4 lenses that passed.

## Constraints
NEVER edit an adopted file, the VENDOR.md manifest table, or any carried-verbatim kb/tiers / adaptation-mapping /
templates / adaptation-rules-resource YAML payload. Editable: CLAUDE.md, UPSTREAM-SYNC.md, agents/analyst.md,
skills/adaptation-safety/SKILL.md (prose only, outside fenced payloads), and the hard-gate report.
