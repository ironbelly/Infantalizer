# P1 Consolidated Findings (Phase Gate P1)

**Overall consolidated verdict: FAIL** (issues reported by the meaning-flow lens of any severity).

Source reports (all under `.dev/tasks/to-do/TASK-RF-native-prep-20260704-233101/qa/`):
- `qa-p1-additive-anchor-report.md` — PASS, 0 findings (14/14 checks; purely additive, anchors correct, frontmatter byte-identical).
- `qa-p1-abort-boundary-report.md` — PASS, 0 blocking (15/15 hard-gate checks; ABORT intact, no new skill line, no new control flow, boundary green, adopted diff empty; 1 MINOR non-blocking forward-reference note).
- `qa-p1-design-fidelity-report.md` — PASS, 0 blocking (5 MINOR advisory observations, all sanctioned re-anchoring/packaging choices; all required insertions byte-faithful to prep-agent-schemas.md §3/§4).
- `qa-p1-schema-consistency-report.md` — PASS, 0 findings (analyst `meaning:` single-confidence form correct; `out_path` default preserved; Check D consistent).
- `qa-p1-meaning-flow-report.md` — **FAIL**, 4 CRITICAL + 2 IMPORTANT.

## Deduplicated findings (classification + resolution)

### MF1 — source-fidelity output schema omits meaning/compound_scene; analyst's "single source of truth" claim overstates — CRITICAL (meaning-flow #1)
- **Classification: GENUINE P1-scope wording fix (option b).** `source-fidelity` is ADOPTED-CLEAN (hash-pinned) — the boundary contract (CLAUDE.md §2) FORBIDS editing its body, so option (a) "extend source-fidelity's schema" is impermissible. The legitimate fix is in `analyst.md` (NATIVE, P1 scope): reword the Output contract so source-fidelity is authoritative for the BASE v2.0 schema while the R10/R11 additive fields (`meaning`, `compound_scene`, `compound_scenes`) are defined in the analyst's own additive block. This removes the contradiction without touching the adopted skill.
- **Resolution:** Apply wording fix to `analyst.md` Output contract section.

### MF2 — analyst Output contract internal inconsistency (base enumeration omits additive fields) — IMPORTANT (meaning-flow #3)
- **Classification: GENUINE P1-scope clarity fix.** The base field enumeration and the additive block read as slightly contradictory. Fold `meaning`/`compound_scene`/`compound_scenes` into the enumeration so the Output contract is self-consistent.
- **Resolution:** Apply wording fix to `analyst.md` Output contract section (same edit pass as MF1).

### MF3 — tier-coordinator cites /thematic-fidelity for Check D but doesn't load it; "no new skill line" asserted not demonstrated — CRITICAL/IMPORTANT (meaning-flow #2, #5)
- **Classification: NOT a defect — design-faithful.** The design pack (`prep-agent-schemas.md` §4.2) EXPLICITLY mandates: "The tier-coordinator already loads /adaptation-tiers, /source-fidelity, /kb-management; Check D reads meaning as data from the mapping/analysis, so **no new skill line is required (keeps the frontmatter diff empty)**." Adding `thematic-fidelity` to tier-coordinator's skills would DEVIATE from the design pack. Check D's body is operationally self-sufficient: it inlines `preserves_meaning()` as an ordinal judgment WITH a worked example ("Grumpy King" preserves "external corrupting force") — that IS the operational definition; "reads meaning as data" requires only the field value + the inlined judgment. The `(R10; /thematic-fidelity)` citation is build-time provenance per CLAUDE.md §1 ("Design-pack references are build-time provenance, not runtime dependencies"), not a runtime skill dependency.
- **Resolution:** No action — design-faithful. The design pack is the authority; the P1 diff implements §4.2 verbatim (the design-fidelity lens confirmed byte-faithfulness).

### MF4 — work-mapping-template.yaml missing top-level `meaning:` — CRITICAL (meaning-flow #6)
- **Classification: NOT a defect — misread of architecture.** The template is the frozen 5-key BASE form. R14 (package-schemas.md): "Root gains no meaning concept and no new machinery." `meaning:` is the 6-key 0.1 RUNTIME extension that the prep-cordinator ADDS to `30-mapping.yaml` at derivation time (prep-agent-schemas.md §3.2, prep SKILL.md §4). The template is deliberately meaning-less; the promoted root copy (`<slug>_mapping.yaml`) strips `meaning:` to validate against this frozen 5-key shape (path-contract §3). Adding `meaning:` to the template would CONTRADICT R14 and break the dual-form promotion contract. The finding conflates the frozen template with the runtime mapping.
- **Resolution:** No action — the template is correctly the frozen 5-key base form by design (R14).

### MF5 — thematic-fidelity SKILL.md "muse reads as data" claim has hidden /laf:rewrite precondition — CRITICAL (meaning-flow #4)
- **Classification: Legitimate minor clarity note, but concerns a P0 file (out of P1 strict scope).** The claim is CORRECT and the `/laf:rewrite` command (P0) surfaces `meaning:` to muse. The hidden-precondition observation is valid as documentation. thematic-fidelity/SKILL.md is a P0 file; editing it during the P1 gate crosses the phase boundary. The same meaning-flow chain is exercised and verified at P3 runtime (where `/laf:rewrite` actually runs). The `/laf:rewrite` entry point is the documented rewrite-phase entry per the design pack (path-contract §4, prep-agent-schemas.md §5.2).
- **Resolution:** Logged as a Follow-Up Item (optional one-sentence clarity note for a future pass); not a P1-blocking defect. The functional chain is sound.

### MF6 (from abort-boundary) — analyst/tier-coordinator cite /thematic-fidelity without loading it — MINOR non-blocking
- Same root theme as MF3/MF5. The abort-boundary lens itself flagged this as the *correct* boundary outcome (no new skill line) and PASS overall.
- **Resolution:** No action — covered by MF3/MF5 classification.

## Fix scope for the serialized fix agent (I20 — single agent)

Apply ONLY the MF1 + MF2 wording fixes in `laf-adaptation/agents/analyst.md` (Output contract section):
- Reword so source-fidelity is authoritative for the BASE v2.0 schema; the `meaning`/`compound_scene`/`compound_scenes` additive fields are defined in the analyst's additive block (cannot extend adopted source-fidelity per boundary contract).
- Fold the additive fields into a self-consistent Output contract presentation.

MUST NOT touch:
- `laf-adaptation/skills/source-fidelity/SKILL.md` (ADOPTED-CLEAN — boundary-forbidden).
- `laf-adaptation/agents/tier-coordinator.md` skills list (design pack §4.2 mandates NO new skill line; Check D is design-faithful).
- `laf-adaptation/templates/work-mapping-template.yaml` (frozen 5-key base form per R14).
- `laf-adaptation/skills/thematic-fidelity/SKILL.md` (P0 file — out of P1 scope; MF5 is a documented Follow-Up).
- Any adopted file. Any VENDOR row.

After the edit, re-run `uv run python laf-adaptation/scripts/check_boundary.py` (final line must begin `BOUNDARY CONTRACT: PASS`) and `git diff --stat -- laf-adaptation/agents/writer.md laf-adaptation/agents/muse.md` (must be empty).
