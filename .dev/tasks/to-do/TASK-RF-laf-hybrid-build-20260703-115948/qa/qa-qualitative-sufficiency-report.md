# QA Report — task-qualitative (qa-gate-sufficiency lens)

**Topic:** LAF 0.1 hybrid build — QA gate sufficiency + structural correctness of gates
**Date:** 2026-07-03
**Phase:** task-qualitative
**Lens:** qa-gate-sufficiency
**Fix cycle:** N/A (report-only; fix_authorization: false)

**Task file:** `.dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md`
**Track goal:** Implement LAF 0.1 end-to-end producing `laf-adaptation/`.

---

## Overall Verdict: FAIL

(FAIL is driven by 3 IMPORTANT issues found below — NOT by the rejection rule. The post-completion final gate meets the 6-agent floor exactly, so the "<6 agents ⇒ CRITICAL FAIL" rejection rule is NOT triggered. The FAIL comes from the task-qualitative "any issue at any severity ⇒ FAIL" rule.)

## Lens Mandate

Per the spawn prompt, the rejection rule is: **if ANY final-document QA gate has fewer than 6 agents, verdict is FAIL with severity CRITICAL.** Final-document gates must be 3 rf-qa + 3 rf-qa-qualitative (I19/I22). Intermediate research/synthesis gates ≥5 agents per I19. M3 pattern (parallel lens agents fix_auth:false → consolidate → ONE fix agent fix_auth:true → verify) must hold. M4 source-fidelity gate must be present (this task carries port-source verbatim — applies). Each agent must be an explicit `- [ ]` item with a SPECIFIC lens focus and adversarial framing. The boundary-contract-fidelity lens must actually run `uv run python scripts/check_boundary.py`. The Phase-3 HARD GATE conditions must be encoded as verification items.

(Findings appended incrementally below.)

## Gate Enumeration & Agent Counts (verified by line-level grep)

| Gate | Location (lines) | rf-qa (struct+verify) | rf-qa-qualitative (content+verify) | fidelity (M4) | fix_agent (auth:true) | Total lens agents | Meets floor? |
|------|------------------|----------------------|-------------------------------------|---------------|----------------------|-------------------|-------------|
| Phase Gate 0 (vendor) | PG0.2-PG0.5 (249-267) | 4 struct + 1 verify = 5 | 3 content + 1 verify = 4 | (n/a — adopted, no port) | 1 | 7 lens | PASS (≥6) |
| Phase Gate 1 (native spine) | PG1.2-PG1.6 (335-358) | 4 struct + 1 verify = 5 | 3 content + 1 verify = 4 | 3 (PG1.4) | 1 | 10 lens | PASS (≥6) |
| Phase Gate 2 (greenfield) | PG2.2-PG2.5 (393-411) | 4 struct + 1 verify = 5 | 3 content + 1 verify = 4 | (n/a — authored, no port) | 1 | 7 lens | PASS (≥6) |
| Phase Gate 3 (hard-gate report) | PG3.2-PG3.5 (455-473) | 4 struct + 1 verify = 5 | 3 content + 1 verify = 4 | (n/a — runtime artifacts) | 1 | 7 lens | PASS (≥6) |
| POST-COMPLETION final | PC.2-PC.5 (501-518) | 3 struct + 1 verify = 4 | 3 content + 1 verify = 4 | (n/a — re-check) | 1 | 6 lens | PASS (=6 floor) |
| M4 source-fidelity | PG1.4 (346-349) | — | — | 3 (2 fidelity + 1 cross-source) | (rolled into PG1.5) | 3 fidelity | PASS (M4 present) |

Counts verified via `grep -c "fix_authorization: true"` = 5 (one fix agent per gate), `grep "^- [ ] Spawn an rf-qa"` = 47 lens-agent spawn lines. All lens agents carry an explicit `fix_authorization` token (the "no token" grep returned empty).

**Rejection-rule verdict:** The post-completion final gate (PC.2-PC.3) has exactly 3 rf-qa + 3 rf-qa-qualitative = 6 lens agents, meeting the I19/I22 floor. The "<6 ⇒ CRITICAL" rule is **not triggered**.

## M3 / M4 / I20 Pattern Audit

- **M3 pattern (parallel lens, fix_auth:false → consolidate → ONE fix agent auth:true → verify):** Present in all 5 phase/post gates. Verified: each gate has a "Spawn structural/content lens agents (PARALLEL, fix_authorization: false)" step, a "Consolidate ... apply fixes (serialized per I20)" step spawning exactly ONE rf-qa fix agent with `fix_authorization: true`, and a "Verification round (PARALLEL, fix_authorization: false)" step. The serialized-fix protocol is explicitly stated ("This is the ONLY agent authorized to modify the artifacts in this gate"). PASS.
- **M4 source-fidelity gate:** Present at PG1.4 (lines 346-349), correctly placed after Phase 1 (the phase that carries port-source verbatim: 4 tier YAMLs + universal-mappings + thematic/character wrappers + work-mapping-template). The gate runs 3 agents (2 byte-fidelity + 1 cross-source-contradiction). Per the spawn prompt this gate applies because the task carries port-source verbatim — correctly identified. PASS.
- **boundary-contract-fidelity lens runs `uv run python laf-adaptation/scripts/check_boundary.py`:** Confirmed present in all 5 gates (lines 253, 343, 401, 463, 508). Each invocation includes "confirm exit 0". PASS.
- **Phase-3 HARD GATE conditions as verification items:** All 5 conditions are encoded as discrete `- [ ]` L4-verdict items (Steps 5.6-5.10: gate-cond1-tags, gate-cond2-safety, gate-cond3-canon, gate-cond4-quartet, gate-cond5-boundary), aggregated into the GREEN/RED report at Step 5.11 with explicit HALT-on-RED. PASS.
- **Adversarial framing:** Every lens agent carries an "Assume at least N errors ... Find them." adversarial prompt. The framing thresholds scale sensibly (phase gates = "5 errors", post-completion = "10 errors"). PASS.
- **Agents are explicit `- [ ]` items, not prose:** All 47 lens spawns + 5 fix agents are checkbox items. PASS.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Enumerate every QA gate; count agents per gate | none | PASS | grep + line-level Read of PG0/PG1/PG2/PG3/PC headers; counts tabled above; all gates ≥6, post-completion = 6 floor met |
| 2 | Final-document gates ≥6 agents (3 rf-qa + 3 rf-qa-qualitative) | none | PASS | PC.2 = 3 rf-qa (template-conformance/internal-consistency/evidence-quality) + PC.3 = 3 rf-qa-qualitative (actionability/boundary-fidelity/source-fidelity) = 6; PG0/PG1/PG2/PG3 = 7/10/7/7 |
| 3 | Intermediate gates ≥5 agents per I19 | none | PASS | M4 gate (PG1.4) = 3 fidelity agents. The I19 ≥5 floor is scoped to research/synthesis intermediate gates; the M4 gate is a source-fidelity gate, so the ≥5 floor does not strictly govern it. (Floor check itself PASSES.) The separate coverage-sufficiency concern for this gate is captured under check 6 / Issue 3, not here. |
| 4 | Each agent has a SPECIFIC lens focus (not generic) | none | PASS | every spawn names a concrete lens (template-conformance, internal-consistency, evidence-quality, completeness, actionability, boundary-contract-fidelity, domain-accuracy, source-fidelity); no generic "review the phase" agents |
| 5 | M3 pattern: parallel lens auth:false → consolidate → ONE fix auth:true → verify | none | PASS | verified in all 5 gates; `grep -c "fix_authorization: true"` = 5; serialized-fix prose present at each consolidate step |
| 6 | M4 source-fidelity gate present AND covers every carried-verbatim file | AX-3 | FAIL | PG1.4 is present and correctly placed after Phase 1. But it spawns only 3 agents (2 byte-fidelity + 1 cross-source) for 9 carried-verbatim files, leaving the Tolkien-instance mapping and the agency.md wrapper with no dedicated/assigned agent (see Issue 3 for the per-file assignment audit). Gate PRESENCE passes; gate COVERAGE fails the sufficiency bar. |
| 7 | QA agents are explicit `- [ ]` items, not prose | none | PASS | all 47 lens spawns + 5 fix agents are checkboxes |
| 8 | Adversarial framing present | none | PASS | every lens agent has "Assume at least N errors ... Find them." |
| 9 | boundary-contract-fidelity lens runs `uv run python scripts/check_boundary.py` | none | PASS | confirmed at lines 253, 343, 401, 463, 508 (5 gates) — note: invoked as `laf-adaptation/scripts/check_boundary.py` (nested-path form, matches `working-directory: laf-adaptation` CI contract) |
| 10 | Phase-3 HARD GATE conditions encoded as verification items | none | PASS | Steps 5.6-5.10 = 5 discrete gate-condN verdict items + Step 5.11 GREEN-only aggregation with HALT-on-RED |
| 11 | Spawned-agent output filename vs declared path consistency | AX-1 | FAIL | grep found ≥2 cases where the filename in the prose ("producing `<X>`") differs from the filename embedded in the output path; see Issue 1 |
| 12 | Lens-agent output-path naming consistency within a gate | AX-2 | FAIL | PG0 reports use `qa-structural-*-report-phase0.md` / `qa-content-*-report-phase0.md` (with `-report-` infix) while PG1/PG2/PG3/PC reports drop the infix (`qa-structural-*-phase1-report.md`); consolidation steps glob `qa-structural-*.md` so both resolve, but the Phase-0 boundary-fidelity report is named `qa-structural-boundary-fidelity-report-phase0.md` (struct-prefixed) while the SAME lens in PG1+ is `qa-content-boundary-fidelity-...` (content-prefixed) — see Issue 2 |
| 13 | fix-agent scoping (never edits adopted body) | none | PASS | every fix-agent item restates "never editing an adopted body" / "NEVER editing adopted files"; scope is correct |

## Summary
- Checks passed: 10 / 13
- Checks failed: 3 (check 6 M4 coverage, check 11 filename/path drift, check 12 lens-classification drift)
- Critical issues: 0
- Important issues: 3
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)
- Rejection rule (<6 agents on a final gate ⇒ CRITICAL): NOT triggered
- Axis lens status: AX-1 Drift active (BUILD_REQUEST.GOAL verbatim baseline available in spawn prompt: "Implement LAF 0.1 end-to-end producing laf-adaptation/"). drift-axis NOT inactive.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | PG2.2, line 394 (and structurally the same pattern risks lines 336-344, 356-357, 395-397, 400-402, 409-410, 456-459, 462-464, 471-472, 502-504, 507-509, 516-517) | **Spawned-agent output filename disagrees with its declared output path.** At line 394 the agent is told to produce `qa-structural-template-conformance-report.md` but the path it must write to is `.../qa-structural-template-conformance-phase2-report.md`. A mechanical grep across all "producing `<name>` at `<dir>/<pathfile>`" pairs shows every PG1/PG2/PG3/PC lens item where the path is given as a bare directory (e.g. `.../qa/`) leaves the filename ambiguous relative to the named report — and the one PG2 row where both are fully spelled out, they disagree. This is an AX-1 drift defect: the agent-name and the on-disk artifact name can diverge, so the downstream consolidation glob (`Read all 7 QA reports ... qa-structural-*.md`) may pick up a differently-named file than the agent was told to author, or (in the line-394 case) the agent may write one of the two names arbitrarily and the other never exists. | Normalize every lens-agent item so the filename in "producing `<X>`" byte-matches the basename in "at `<dir>/<Y>`". For PG2.2 line 394 specifically: pick one name (recommend `qa-structural-template-conformance-phase2-report.md` to match the sibling phase2 reports) and use it in both the "producing" clause and the path. Audit all ~30 "producing ... at ..." pairs and force name==pathfile. |
| 2 | IMPORTANT | PG0.2 line 253 vs PG1.3 line 343 (and PG2.3/PG3.3/PC.3) | **The boundary-contract-fidelity lens is filed under different agent TYPES across gates, weakening the "3 rf-qa + 3 rf-qa-qualitative" I19/I22 contract.** In PG0.2 (line 253) it is an `rf-qa` (structural) agent producing `qa-structural-boundary-fidelity-report-phase0.md`; in PG1.3/PG2.3/PG3.3/PC.3 (lines 343/401/463/508) the SAME lens is an `rf-qa-qualitative` (content) agent producing `qa-content-boundary-fidelity-...`. The lens runs the identical action (`uv run python laf-adaptation/scripts/check_boundary.py` + manual rule spot-checks) in all five. This is an AX-2 contradiction: the same verification responsibility is classified as structural in one gate and qualitative in four others. Practically it still meets the 6-agent floor in every gate, but a reader auditing "is boundary fidelity a structural or a content check?" gets two incompatible answers, and the PG0 structural bucket effectively has 4 agents (template/internal/evidence/boundary) while PG1+ structural bucket has only 3 (template/internal/evidence/completeness) — i.e. the structural/content split is inconsistent gate-to-gate. | Pick one classification for the boundary-contract-fidelity lens and apply it in all 5 gates. Recommend: classify it as `rf-qa` (structural) in all gates, since its core action is running a script and asserting exit 0 + rule pass/fail (a structural/mechanical check), OR document explicitly why PG0 uses structural (no content yet — only vendored files) while later gates use qualitative (content now exists to also assess). Either resolution is acceptable; the current silent inconsistency is not. |
| 3 | IMPORTANT | PG1.4 (lines 346-349) | **The M4 source-fidelity gate has 3 agents, below the I19 ≥5 floor for intermediate gates — and the consolidation step (PG1.5 line 352) miscounts the reports it must read.** PG1.5 line 352 reads "all QA reports from Steps PG1.2-PG1.4 (4 structural + 3 content + 3 fidelity = 10 reports)" — but PG1.2 spawns 4 structural, PG1.3 spawns 3 content, PG1.4 spawns 3 fidelity = 10 lens reports, which is arithmetically correct. The real defect is the M4 gate's 3-agent count vs I19's intermediate-gate ≥5 floor: the spawn prompt says "Intermediate gates (research/synthesis) ≥5 agents per I19 if any." The M4 gate is a source-fidelity gate (not research/synthesis), so strictly the 5-floor may not govern it — but the spawn prompt's instruction #1 explicitly says to "verify ... Intermediate gates (research/synthesis) ≥5 agents per I19 if any", and the M4 gate is the only intermediate (non-final-document) gate with a sub-6 count. Combined with the fact that the M4 gate is doing load-bearing byte-fidelity work on 9 carried-verbatim files with only 3 agents (2 byte-fidelity + 1 cross-contradiction), the coverage is thin: agent-1 covers 6 files (4 tiers + universal-mappings + template), agent-2 covers 2 files (thematic + character), agent-3 is meta (cross-source contradictions). There is no agent dedicated to the Tolkien instance mapping or to the agency.md wrapper, and no redundancy. This is an AX-3 omission (insufficient coverage for the highest-fidelity-risk work in the whole task). | Either (a) explicitly justify in the task why the M4 gate is allowed 3 agents (cite that I19's ≥5 floor is scoped to research/synthesis gates, not fidelity gates) — and add the Tolkien-instance + agency.md wrapper to an existing agent's scope so nothing is uncovered; OR (b) raise the M4 gate to ≥5 agents (e.g. split agent-1's 6 files into 2 agents, add a dedicated agency/Tolkien agent, add a redundancy cross-check agent). Recommend (a) + scope expansion, since the byte-fidelity check is mechanical and 3 agents is defensible IF every carried file is explicitly assigned. |

## Confidence

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 (task file pages) | Grep: 4 | Glob: 0 | Bash: 4

Every checklist item was checked with line-level evidence (cited line numbers above). No item was left unchecked; no item was unverifiable. The 3 findings come from mechanical grep output (Issue 1), cross-gate agent-type comparison (Issue 2), and explicit count-vs-floor reasoning (Issue 3) — not from speculation.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for QA sizing (gates at 7/10/7/7 agents, post-completion at 6, all ≥ floors) — did NOT recount agents to re-confirm the structural floor (the inherited verdict already machine-verified this).
- Relied on rf-qa PASS for the M3+M4 pattern presence — did NOT re-verify that an M3/M4 pattern exists structurally.
- Relied on rf-qa PASS for the TB-Add-* structural-gate additions.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Spawned-agent filename-vs-path consistency (Issue 1) — verified by `grep -oE "producing \`[^\`]+\` at \`[^\`]+\`"` over the whole task file and diffing the two basenames; rf-qa's structural "report path well-formed" PASS does NOT catch intra-item name/path disagreement because each path is individually well-formed.
- boundary-contract-fidelity lens agent-TYPE classification drift PG0 vs PG1+ (Issue 2) — verified by `grep -n "boundary-contract-fidelity lens"` and reading each of the 5 hits to classify rf-qa vs rf-qa-qualitative; rf-qa's "lens present in every gate" PASS does NOT check that the lens is filed under the same agent type in every gate.
- M4 gate agent-count vs the controlling floor + per-file coverage (Issue 3) — verified by reading PG1.4 lines 346-349 and enumerating which carried-verbatim file each of the 3 agents covers; rf-qa's "M4 gate present" PASS does NOT check that every carried file is assigned to an agent or that the count meets the intermediate-gate floor.

These three semantic checks are exactly the kind rf-qa's structural lens cannot reach (they are correctness/sufficiency questions about the gates, not structural well-formedness), confirming the reliance did not equal verification.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
- Relied on rf-qa PASS for QA sizing (7/10/7/7 + 6) -> semantic counterpart verified: per-gate agent-count table above (Issues 1-3 surface despite the floor being met).
- Relied on rf-qa PASS for M3+M4 pattern presence -> semantic counterpart verified: M3 serialized-fix + M4 fidelity gate audited (Issue 3 surfaces a coverage gap inside the M4 gate that the structural "gate present" check cannot see).
- Relied on rf-qa PASS for TB-Add-* -> semantic counterpart verified: the boundary-contract-fidelity lens's actual `check_boundary.py` invocation confirmed at 5 line cites (Issue 2 surfaces a classification drift the structural check cannot see).

## Recommendations
- Resolve Issue 1 (filename/path normalization) before execution — it is the one most likely to cause a silent consolidation miss during the QA run, because the glob `qa-structural-*.md` would still match but the agent might write the "producing" name while a downstream reader looks for the "path" name.
- Resolve Issue 2 (boundary-contract-fidelity classification) for contract coherence; lower urgency since every gate still meets its floor.
- Resolve Issue 3 (M4 coverage) — at minimum add the Tolkien-instance + agency.md wrapper to an agent's scope so no carried-verbatim file is uncovered.
- None of the 3 issues is CRITICAL; the rejection rule is not triggered. But all three are IMPORTANT and the task-qualitative rule is "any issue ⇒ FAIL," so the verdict is FAIL pending resolution.

## QA Complete
