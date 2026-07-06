# QA Report — Task Integrity (Phase-Structure Lens)

**Topic:** LAF 0.1 (CWS Hybrid, Path C) end-to-end implementation
**Date:** 2026-07-03
**Phase:** task-integrity
**Fix cycle:** N/A
**Lens:** phase-structure
**Template:** 02 (complex)

---

## Overall Verdict: FAIL

Two CRITICAL structural defects (reflect skip-guard form; phase-outputs path missing the `to-do/` segment across 99 items), plus one IMPORTANT and two MINOR findings. The phase *ordering*, *dependencies*, *heading level*, and *counts* are sound; the failures are in the reflect gate construction and the intra-task handoff path.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete & well-formed | PASS | Read lines 1-69: `id`, `title`, `status`, `created_date`, `updated_date`, `type`, `template_schema_doc`, `task_type`, `spec_path`, `start_commit`, `related_docs` (7 entries), `tags` all present and non-empty. `start_commit: "no-commits-yet..."` documents the no-commits baseline. |
| 2 | Mandatory template-02 sections present | PASS | Read lines 73-159: Task Overview, Key Objectives, Prerequisites & Dependencies (Parent Task, Previous Stage Outputs), Execution Context (References, Source Areas, Key Constraints, Handoff File Convention, Frontmatter Update Protocol), Detailed Task Instructions, Post-Completion Actions, Task Log / Notes — all present. |
| 3 | Phase dependencies logical, no cycles/missing | PASS | grep of `### Phase` + `### Phase Gate` headers (lines 161-475): linear chain Phase 1 → Phase 2 → Gate 0 → Phase 3 → Gate 1 → Phase 4 → Gate 2 → Phase 5 → Gate 3 → Phase 6 → Post-Completion. Each build phase is followed by its gate; gates read only preceding-phase outputs. No backward references found. |
| 4 | Phase ordering (vendor→native→greenfield→proof gate→sync) | PASS | Headers confirm: taskfile "Phase 2" = build Phase 0 Vendor; "Phase 3" = build Phase 1 Native; "Phase 4" = build Phase 2 Greenfield; "Phase 5" = build Phase 3 Hard Gate; "Phase 6" = build Phase 4 Upstream-Sync. Matches DESIGN.md §7 progression. |
| 5 | Task-completion items inside final phase (anti-orphaning) | PASS | Read lines 488-525: Post-Completion Actions contains output-Glob verification, final boundary-script re-run, full post-completion lens-based QA (PC.1-PC.5), the POST reflect gate (PC.6), Task Summary, and the status→Done update gated on reflect PASS + final QA PASS + hard-gate GREEN. |
| 6 | Task Log section present at bottom | PASS | grep line 527: `## Task Log / Notes 📋` with Task Summary, Execution Log, per-phase Findings sections (Phase 2-6), Phase Gate Findings, Open Questions, Follow-Up, Deviations. |
| 7 | Estimated item count reasonable | PASS | `grep -c '^- \[ \]'` = 150 checklist items for a 5-build-phase + 4-gate + post-completion task. Proportional to scope. |
| 8 | Open Questions / gaps documented | PASS | Read lines 582-591: 6 Open Questions carried as risks (upstream SHA, proof-chapter provisioning, LICENSE filename, hook/CI working-dir, verify-mode upstream access, tier_N.md count). None silently dropped. |
| 9 | QA gates follow M3 (lens sequence) + M4 (fidelity) | PASS | Per-gate agent counts: Gate 0 = 4 structural + 3 content (7); Gate 1 = 4+3+3 fidelity (10, includes M4); Gate 2 = 4+3 (7); Gate 3 = 4+3 (7); Post-Completion = 3+3 (6). All ≥ intermediate floor (5) and final floor (6) per I19. Serialized fix (I20) + verification rounds present in every gate. |
| 10 | TB-Add-1: placeholder scan (no TBD/TODO/FIXME; no title-only items) | PASS | `grep -nE 'TBD\|TODO\|FIXME'` over the file = 0 hits. Every `- [ ]` item has full Context+Action+Output+Verification+Completion-gate body (B2 6-field). |
| 11 | TB-Add-3: clarification adjacency (blocked items reference OQ index) | PASS (N/A-ish) | No checklist item is hard-blocked on an Open Question at build time — the 6 OQs are execution-time decisions whose resolution is embedded in the relevant item's Action (e.g. Step 2.1 embeds the SHA-pinning OQ, Step 5.1 embeds the proof-chapter OQ). No orphaned blocked items. |
| 12 | TB-Add-4: circular dependency detection (DAG) | PASS | Cross-referenced item reads/writes: discovery (2.1) → build (2.3/2.4 read inventory) → manifest (2.12/2.13) → verify (2.14) → gate. Within-phase ordering is read-after-write. No item references a later item that references it back. Acyclic. |
| 13 | TB-Add-5: granularity / XL splitting | MINOR | `awk` longest checklist item = 3016 chars (Step 2.2, author check_boundary.py). Several items in the 1500-2800 range (2.1, 3.7, 5.3, 5.4). Each is scoped to ONE deliverable file/output, so they are atomic by deliverable — but Step 2.2 packs ~15 internal requirements (6 functions, 3 CLI modes, rules A-F, helpers) into one item, which is at the upper bound of the atomicity rule. Borderline; flagged MINOR. |
| 14 | TB-Add-6: Verification/Acceptance format consistency | PASS | All items terminate with the uniform `... Once done, mark this item as complete.` completion gate. Verification is embedded as the `ensuring...` clause in every item (no separate `- ✅` / `- [x]` Acceptance form used — consistent single-form compliance with B2). |
| 15 | TB-Add-7: Execution Context source areas reappear in items; no file:line in the block | PASS (format variance) | Read lines 119-124: `### Source Areas` lists 4 areas (design spec dir, port-source configs, upstream checkout, laf-adaptation tree). All 4 reappear in item Context fields (e.g. Step 2.1 cites upstream checkout; Steps 3.4-3.17 cite port-source configs). Block contains directory-level refs only, no `path.py:NN`. NOTE: uses heading form `### Source Areas` rather than the `**Source areas:**` bold-line form the check names — content compliant, format variance only (MINOR, folded here). |
| 16 | TB-Add-8: per-item Context evidence binding (file:line or evidence-absence) | PASS | Spot-checked Steps 2.1, 2.2, 3.1, 3.8, 4.2, 5.3 — all cite explicit `(lines N-M)` ranges against the design specs (e.g. `boundary-contract.md §3 (lines 92-167)`, `skill-specs.md §1 (lines 33-83)`). Strong file:line compliance. |
| 17 | Phase heading level vs template | PASS | Template 02 (read lines 1233, 1291, 1339) uses `## Detailed Task Instructions` then `### Phase 1`, `### Phase 2`. Task file uses identical convention (lines 159, 161, 171). NOT a violation — matches template exactly. |
| 18 | Build-phase ↔ taskfile-phase double-mapping clarity | PASS | Task Overview line 77 states the mapping in prose ("Phase 0 (Vendor)", "Phase 1 (Native Spine)", ...). Every phase header makes it explicit: `### Phase 2: Phase 0 — Vendor`, `### Phase 3: Phase 1 — Native Spine`, etc. Not confusing. |
| 19 | Count math (15 agents / 16 skills / 23 adopted) | PASS | Read line 133: 11 adopted + 2 native + 2 build-new = 15 agents ✓; 12 adopted + 3 native + 1 build-new = 16 skills ✓; 11 agents + 12 skills = 23 adopted ✓. Internally consistent and consistent with Step 2.3 (11 agent items) + Step 2.4 (12 skill items). |
| 20 | Reflect gate skip-guard form (Critical Rule 20) | **FAIL — CRITICAL** | Read line 521: the skip guard is `if [ -n "$SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" ]` — the **`-n "$VAR"` quoted-string form**. The spec mandates `[ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]` (env-var-equals-"1") and explicitly prohibits the `-n` form. Byte-for-byte wrong. |
| 21 | Reflect gate: flat wrapper, consumes exit code, no `--reflect`/range/agent-spawn | PARTIAL → IMPORTANT | Line 521 correctly uses `superclaude reflect run <TASK_FILE> --depth deep --fix --promote` (flat shell-out, not `--reflect`/`<base>..HEAD`/agent-spawn — good). BUT exit-code handling deviates: spec says "only 0 proceeds; 10/11/2 FAIL"; the item treats exit 2 as "proceed to the status-update item (non-blocking)". Exit 2 should FAIL per the verification spec. |
| 22 | phase-outputs / qa handoff path consistency | **FAIL — CRITICAL** | Task physically lives at `.dev/tasks/to-do/TASK-RF-.../` (verified). The reflect command (line 521) correctly uses the `to-do/` path. But 99 checklist items + the Handoff File Convention (line 138) reference `.dev/tasks/TASK-RF-.../phase-outputs/` and `.dev/tasks/TASK-RF-.../qa/` **WITHOUT the `to-do/` segment** (grep: 99 items use no-`to-do` path; 0 items use the `to-do/` path for phase-outputs). Artifacts would be written to / read from a directory tree detached from the task's lifecycle home. |

## Summary
- Checks passed: 18 / 22
- Checks failed: 4 (2 CRITICAL, 1 IMPORTANT via partial, 1 MINOR)
- Critical issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Confidence
**Verified:** 22/22 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

Every checklist item was checked with direct tool evidence (Read of frontmatter/sections, grep of headers/items/placeholders/paths/reflect-guard, awk line-length, filesystem path-existence checks against the task's real location).

## Tool engagement
Read: 4 | Grep (via Bash): 6 | Glob (via Bash find/ls): 3 | Bash: 5
tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 (no external lookup required — all verification was local source-truth).

---

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | Line 521, Step PC.6 (POST reflect gate) | Skip-guard uses the prohibited `-n "$VAR"` form: `if [ -n "$SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" ]`. Critical Rule 20 mandates the env-var-equals-"1" form `[ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]` and explicitly forbids the `-n` form. | Replace the guard with: `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect wrapper already active — skipping nested invoke"; else superclaude reflect run ".dev/tasks/to-do/TASK-RF-laf-hybrid-build-20260703-115948/TASK-RF-laf-hybrid-build-20260703-115948.md" --depth deep --fix --promote; fi`. Verify byte-for-byte against the spec. |
| 2 | CRITICAL | Lines 138 + ~99 items (Steps 2.1, 2.2, 2.13, 2.14, PG0.1-PG0.5, PG1.x, PG2.x, PG3.x, PC.x — every phase-outputs/qa reference) | Handoff paths are `.dev/tasks/TASK-RF-laf-hybrid-build-20260703-115948/phase-outputs/...` and `.../qa/...`, MISSING the `to-do/` status-folder segment. The task's physical home is `.dev/tasks/to-do/TASK-RF-.../` (the reflect command on line 521 gets this right). The 99 items + the Handoff File Convention on line 138 disagree with the reflect gate on the root path, and the artifacts would be detached from the task's lifecycle (stranded when the task moves to-do → in-progress → done). | Either (a) replace all 99 hardcoded `.dev/tasks/TASK-RF-.../(phase-outputs|qa)` paths with `.dev/tasks/to-do/TASK-RF-.../(phase-outputs|qa)` to match the task's real home and the reflect-gate path, OR (b) parameterize as `${TASK_DIR}phase-outputs/` / `${TASK_DIR}qa/` so the path follows the task across status folders. The Handoff File Convention block (line 138) must be corrected in lockstep since it is the source the items were derived from. |
| 3 | IMPORTANT | Line 521, Step PC.6 (exit-code handling) | Item treats reflect exit 2 (infrastructure error) as "proceed to status-update (non-blocking)". The verification spec states "only 0 proceeds; 10/11/2 FAIL" — exit 2 must FAIL, not proceed. | Either halt on exit 2 (treat as FAIL like 10/11) OR, if the operational intent is that infra errors genuinely shouldn't block, document the deviation explicitly in the Open Questions section and reconcile with the spec. As written it silently contradicts the gate contract. |
| 4 | MINOR | Step 2.2 (line 179, 3016 chars); also Steps 2.1, 3.7, 5.3, 5.4 (>2000 chars) | Item atomicity borderline: Step 2.2 authors an entire Python script (manifest parser + prefix_rewrite + verify + --init + --report + sha256 + rules A-F + 2 helpers) in one ~3000-char item. Each is scoped to a single deliverable file so it is not a multi-file violation, but it is at the upper bound of "could someone execute this item without scrolling?". | Consider splitting Step 2.2 into (a) skeleton + manifest parser + prefix_rewrite, (b) verify() rules A-F, (c) --init/--report modes — three sequential items each under ~1200 chars. Not blocking; the item IS self-contained. |
| 5 | MINOR | Line 119, Execution Context | `### Source Areas` uses heading form; TB-Add-7 names the `**Source areas:**` bold-line form. Content is present and every source area reappears in item Context fields, so this is format variance only — not a structural gap. | Optional: align to `**Source areas:**` bold-line form for strict TB-Add-7 conformance. No functional impact. |

## Recommendations (before the task may be marked ready)
1. **Fix Issue 1 (reflect skip-guard) — mandatory.** This is an explicitly-flagged Critical Rule 20 violation; the task cannot pass task-integrity with the `-n` form in place.
2. **Fix Issue 2 (handoff paths) — mandatory.** Pick (a) literal `to-do/` correction or (b) `${TASK_DIR}` parameterization and apply uniformly across the 99 items + the Handoff File Convention block + the `qa/` output paths. Until fixed, the phase-outputs and QA reports will not co-locate with the task file.
3. **Resolve Issue 3 (exit-2 handling)** to match the gate contract, or document the deviation in Open Questions.
4. Issues 4-5 are non-blocking polish.

## QA Complete
