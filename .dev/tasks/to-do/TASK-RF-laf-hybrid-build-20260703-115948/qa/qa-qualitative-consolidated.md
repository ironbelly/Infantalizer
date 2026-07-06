# QA Task-Validation — Qualitative Consolidated Findings (A.10.5)

**Task file:** .dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md
**Round:** 1 (operational-correctness + qa-gate-sufficiency lenses)

---

## Items Reviewed (qualitative)

| Check | Lens | Verdict |
|---|---|---|
| UV-only uniformity (24 invocations, 0 bare-python) | operational | PASS |
| check_boundary.py mode flags correct | operational | PASS |
| Verbatim-carry port-source paths exist on disk | operational | PASS |
| Port-source content claims byte-accurate (agency_externalization, death_handling, 9 concepts, 5 keys, T1-vs-T5 drift) | operational | PASS |
| safety-verifier FAIL→step-3 + tier-coordinator RECONCILED→chronicler gates wired natively | operational | PASS |
| Hook/CI working-directory handling | operational | PASS |
| Proof-chapter honors no-copyrighted-Tolkien | operational | PASS |
| All QA gates meet I19/I22 floors (PG0=7, PG1=10, PG2=7, PG3=7, final=6; M3 + I20 serialized fix) | sufficiency | PASS |
| M4 source-fidelity gate present (PG1.4, 3 agents) | sufficiency | PASS |
| boundary-contract-fidelity lens runs check_boundary.py in all 5 gates | sufficiency | PASS |
| Phase-3 HARD GATE: 5 conditions as discrete items + GREEN-only aggregation + HALT-on-RED | sufficiency | PASS |
| **Q-1: start_commit unresolvable (zero-commit repo) → reflect gate guaranteed exit-2 FAIL** | operational | **CRITICAL FAIL** |
| **Q-2: Filename/path drift — "producing <X>" name vs output basename mismatch (~30 lens items)** | sufficiency | **IMPORTANT FAIL** |
| **Q-3: Lens agent-type drift — boundary-contract-fidelity is rf-qa in PG0 but rf-qa-qualitative in PG1/2/3/PC** | sufficiency | **IMPORTANT FAIL** |
| **Q-4: M4 fidelity gate coverage gap — Tolkien-instance mapping + agency.md wrapper have no assigned agent** | sufficiency | **IMPORTANT FAIL** |

---

## Fixes to apply (single serialized fix agent, I20)

### Q-1 (CRITICAL) — start_commit unresolvable; reflect gate guaranteed to FAIL
**Problem:** The repo has zero commits on `main` (`git log` → "does not have any commits yet"). The task frontmatter carries `start_commit: "no-commits-yet"` — not a resolvable git ref. The POST reflect gate derives its audit base from `start_commit`/merge-base; `superclaude reflect run ... --depth deep --fix --promote` returns `Error: head-unresolved` exit 2. Per PC.6's contract, exit 2 is FAIL → HALT. So the task can NEVER reach `status: 🟢 Done` against its declared starting condition.
**Fix (pick one — recommended is (a)):**
(a) Add an item EARLY in Phase 1 (Preparation and Setup) that: makes the first git commit on `main` (the repo is currently all-untracked first-commit territory), then re-captures `start_commit` as `git rev-parse HEAD` and updates the frontmatter `start_commit:` field to that real SHA via Edit. Document that the reflect wrapper resolves the audit base from frontmatter `start_commit`. This makes the reflect gate resolvable.
(b) ALTERNATIVELY, change the PC.6 reflect invocation to pass an explicit resolvable `--base <ref>` (e.g. `--base <first-commit-sha>` or, if the wrapper supports it, a ref that will exist post-execution). Note: per the contract, `--base` has highest precedence over frontmatter start_commit + merge-base.
Implement (a) as the primary fix (it also unblocks normal git workflow); document the choice in the report.

### Q-2 (IMPORTANT) — Filename/path drift in QA lens items
**Problem:** At line 394 and ~30 lens-spawn items, the agent prompt's "producing `<X>`" name disagrees with the item's `Output:`/output-path basename. Risk: silent consolidation miss during the QA run.
**Fix:** Audit the QA-spawn items in Phase Gate 0/1/2/3 + post-completion. For each, make the "producing <filename>" name in the prompt MATCH the `Output:`/output-path basename exactly (including the `-phase0`/`-phase1` suffixes applied in fix round 1). One pass of name-alignment across all lens-spawn items.

### Q-3 (IMPORTANT) — Lens agent-type drift
**Problem:** The boundary-contract-fidelity lens is spawned as `rf-qa` (structural) in PG0 but as `rf-qa-qualitative` (content) in PG1/2/3/PC. The same verification classified two ways.
**Fix:** Standardize. Pick ONE agent type for the boundary-contract-fidelity lens across ALL gates and apply consistently. Recommended: `rf-qa-qualitative` (it's a content/correctness verification — does the boundary contract actually hold — which suits the qualitative agent; rf-qa is structural). Update the `subagent_type:` in every boundary-contract-fidelity lens-spawn item (PG0, PG1, PG2, PG3, post-completion) to match. Document the choice.

### Q-4 (IMPORTANT) — M4 fidelity gate coverage gap
**Problem:** The 3-agent M4 source-fidelity gate (PG1.4) covers 9 carried-verbatim files but leaves the Tolkien-instance mapping (`tolkien-mapping.yaml` at onboarding) and the `agency.md` skill-resource wrapper with no dedicated/assigned fidelity agent.
**Fix:** Either (a) add the tolkien-mapping.yaml + agency.md to the assignment list of an existing PG1.4 fidelity agent (extend its `assigned_files`), OR (b) add a 4th fidelity agent item to PG1.4 explicitly covering those two files. Recommended: (a) — extend one existing agent's assignment to keep the gate at 3 agents (avoid resizing). Ensure every carried-verbatim file has an assigned fidelity verifier.

---

**Post-fix verification:** (a) frontmatter `start_commit:` is a real 40-char SHA pattern (or the Phase-1 item performs the first commit + repin); (b) the reflect `head-unresolved` condition is addressed; (c) QA lens "producing <X>" names match output basenames; (d) boundary-contract-fidelity lens has ONE consistent agent type across all 5 gates; (e) every carried-verbatim file (incl. tolkien-mapping + agency.md) has an assigned M4 fidelity agent.
