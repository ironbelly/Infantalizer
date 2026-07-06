# Phase Gate 1 — Consolidated QA + Fidelity Findings (Step PG1.5)

**Compiled:** 2026-07-03 | **Sources:** 10 reports (4 structural + 3 content + 3 M4 fidelity)

## Lens verdict rollup

| Lens | Agent | Verdict | Blocking issues |
|------|-------|---------|-----------------|
| template-conformance | rf-qa | PASS | 0 |
| internal-consistency | rf-qa | PASS | 0 (2 INFO) |
| evidence-quality | rf-qa | PASS | 0 (1 MINOR info) |
| completeness | rf-qa | PASS | 0 |
| **actionability** | rf-qa-qualitative | **FAIL** | **7 (1 CRITICAL, 4 IMPORTANT, 2 MINOR)** |
| boundary-contract-fidelity | rf-qa-qualitative | PASS | 0 |
| domain-accuracy | rf-qa-qualitative | PASS | 0 |
| M4 source-fidelity #1 (kb YAMLs) | rf-qa | PASS | 0 |
| M4 source-fidelity #2 (skill-resource wrappers) | rf-qa | PASS | 0 (tolkien-mapping deferred to PC.3) |
| M4 cross-source-contradiction | rf-qa | PASS | 0 genuine contradictions |

**Boundary gate GREEN** (`check_boundary.py` exit 0, A–F). **All carried-verbatim ports byte-identical**
(9/9 verified: 4 tier YAMLs + universal-mappings + work-mapping-template + thematic/character/agency
wrappers; tolkien-mapping deferred to Phase 3). So the FAIL is **not** a carry defect — the actionability
gaps are design-level under-specifications that the native bodies faithfully reproduced.

## Fix scope + hard constraints for the PG1.5 fix agent

The fixes are **additive actionability clarifications to NATIVE PROSE only**. HARD CONSTRAINTS:
- Do NOT edit any adopted file.
- Do NOT touch the fenced ```yaml payloads inside `resources/thematic.md`/`character.md`/`agency.md`, nor
  any `kb/tiers/*.yaml`, `kb/adaptation-mapping/*.yaml`, or `templates/*.yaml` — these are byte-faithful
  carries the M4 gate verified; editing their payload would REGRESS the fidelity gate.
- Only ADD clarifying notes/subsections to the NATIVE skill/agent bodies (`skills/adaptation-tiers/SKILL.md`,
  `skills/adaptation-rules/SKILL.md`, `skills/source-fidelity/SKILL.md`, `agents/analyst.md`,
  `agents/safety-verifier.md`). Keep the original spec-carried text intact; append clarifications that make
  the rule executable, phrased as the operational reading of the already-present rule (do NOT contradict it).
- After fixes, re-run `check_boundary.py` — it must stay exit 0.

## Findings to apply (F1–F7)

| # | Sev | File (native prose) | Additive fix |
|---|-----|---------------------|--------------|
| F7 | CRITICAL | `skills/adaptation-tiers/SKILL.md` (Interpolation) | ADD a subsection giving the operational reading of "round toward conservative" per threshold TYPE, keeping the existing rule verbatim above it: numeric scalar → arithmetic midpoint, floor-round; enumerated permitted/forbidden lists → T4 = T3's permitted set (the floor); items unique to T5 are EXCLUDED; boolean flags → T4 inherits the T3 value; grade-level / other strings → inherit the T3 (more restrictive) value. `agency_externalization` stays pinned FORBIDDEN (already in the rule). |
| F4 | IMPORTANT | `skills/adaptation-rules/SKILL.md` (Applying a rule, step 2) | ADD a schema-tolerant clarification (mirroring the key-tolerant note already at the "Key-tolerant lookup" section): "read `<category>.tier_<N>.mode` if present; otherwise the category's tier row IS the rule payload — apply its `target`/`strategy`/`translations` directly." Note which categories carry `mode:` (conflict, agency, villain, heroism) vs a direct payload (violence, death at T1-3). |
| F3 | IMPORTANT | `agents/safety-verifier.md` | ADD a precondition note: `/adaptation-safety` is BUILD-NEW, authored in Phase 2 (Step 4.3); it is present in the completed tree and safety-verifier loads it there. (Same forward-reference class as the Phase-0 UPSTREAM-SYNC annotation — honest, not a code change.) |
| F1 | IMPORTANT | `skills/source-fidelity/SKILL.md` (Phase 0) + `agents/analyst.md` | ADD an observable-test decision rule for the access levels (grounded in `prompts/analysis/chapter_analysis.md`'s descriptors): FULL = source_path exists, readable, non-empty; PARTIAL = exists but truncated/partially unreadable; NO-ACCESS = file missing or empty → ABORT; MEMORY-BASED = caller passed no source file / flagged reconstruction → all facts UNCERTAIN. |
| F6 | IMPORTANT | `agents/safety-verifier.md` (verdict/branch) | ADD the deterministic rule next to the branch table: `next = revise` iff (`mode == blocking` AND `result == FAIL`); else `next = promote`. |
| F2 | MINOR | `agents/analyst.md` | Note the in-tree `/source-fidelity` schema is the authoritative single source of truth for the output contract (the `skill-specs.md §3.2` citation is a build-time provenance pointer, not required at runtime). |
| F5 | MINOR | `skills/source-fidelity/SKILL.md` | ADD the overall-confidence derivation: overall = the lowest/worst-case tag present across essentials (CERTAIN > PROBABLE > UNCERTAIN). Note cross-tree `§`-citations are build-time design-pack provenance; the in-tree skill body is self-sufficient. |

## Non-actionable / deferred (no fix)

- fidelity-2: `tolkien-mapping.yaml` byte-check DEFERRED to PC.3 (created in Phase 3 Step 5.2).
- internal-consistency INFO: spec §2.1 shows the pre-rewrite `creative-writing-skills:story-memory` token with an explanatory comment — the shipped analyst correctly resolves to `laf-adaptation:story-memory`. NO fix.
- The carried YAML payloads and kb YAMLs are byte-faithful and MUST stay untouched.
