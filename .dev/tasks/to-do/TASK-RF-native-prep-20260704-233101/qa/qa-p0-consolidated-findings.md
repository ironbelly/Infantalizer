# P0 Consolidated Findings (Phase Gate P0)

**Overall consolidated verdict: FAIL** (issues reported by ≥1 lens of any severity).

Source reports (all under `.dev/tasks/to-do/TASK-RF-native-prep-20260704-233101/qa/`):
- `qa-p0-template-conformance-report.md` — PASS, 0 findings.
- `qa-p0-completeness-report.md` — PASS, 0 findings.
- `qa-p0-design-fidelity-report.md` — PASS, 3 MINOR (all authorized divergences: sparser exemplar provenance, narnia→tolkien example swap, genericized writing-principles reference).
- `qa-p0-boundary-safety-report.md` — PASS on all 6 boundary criteria; 1 Medium (CLAUDE.md doc-drift: still says "15 agents / 16 skills"; CLAUDE.md is outside the Rule-F hash-pin glob so the boundary stays green — documentation, not a boundary violation).
- `qa-p0-operational-coherence-report.md` — **FAIL**, 2 CRITICAL + 3 IMPORTANT + 1 MINOR.

## Deduplicated findings (with classification + resolution)

### F1 — Stage 3 dispatches analyst `granularity: work`; analyst has no such branch — CRITICAL (operational-coherence)
- **Classification: PHASE-ORDERING — NOT a P0-build defect.** The analyst work-mode branch is authored in the immediately-next phase (Phase 3 / Step 3.1, the P1 analyst diff from `prep-agent-schemas.md` §3). DESIGN.md §7 deliberately sequences P0 skeleton → P1 body edits; the prep-cordinator's forward-reference is BY DESIGN. The branch lands BEFORE P3 exercises it (Step 5.2 asserts "the analyst diff from P1 must have produced these").
- **Resolution:** Tracked — verified at the Phase Gate P1 QA (PG1) that the analyst branch actually lands. No P0 file edit.

### F2 — Stage 7 promotion delegates to `/kb-management` (adopted), which has no dual-form awareness — CRITICAL (operational-coherence)
- **Classification: GENUINE P0-scope clarity gap (the single actionable item).** The design pack authoritatively names `/kb-management` as the promotion invocation (prep-agent-schemas.md §1 STAGE 7; path-contract.md §3; prep-skill-specs.md §6). But as written, "promote via /kb-management" can be read as delegating the 6-key↔5-key transform to kb-management's own body, which lacks the rule. The legitimate fix (faithful to the design mechanism — still `/kb-management`-invoked, still dual-form): make explicit in prep-cordinator Stage 7 and prep SKILL.md §6 that the COORDINATOR owns the transform — reading `resources/path-contract.md` §3 as the rule source (the two targets, the meaning-strip, the _confidence-strip, the hyphen-vs-underscore naming) — and invokes `/kb-management` for the kb-lifecycle write using its own `Write` tool. The path-contract resource already fully specifies the transform; the clarity edit just names the operator unambiguously.
- **Resolution:** Apply scoped clarity edit to `prep-cordinator.md` Stage 7 + `prep/SKILL.md` §6 (P0 NATIVE files). Re-run boundary check.

### F3 — Analyst does not load `thematic-fidelity`, so cannot emit `meaning:` — IMPORTANT (operational-coherence)
- **Classification: CROSS-PHASE — resolved by P1.** The `meaning:` field is added to the analyst's output contract in the P1 analyst diff (Step 3.1 / prep-agent-schemas.md §3.2). Whether the analyst also needs `thematic-fidelity` in its `skills:` list (it is NATIVE, frontmatter freely editable) is a P1 concern. The P1 QA gate (PG1) verifies the meaning field lands coherently.
- **Resolution:** Tracked — addressed in Phase 3 (P1). No P0 file edit.

### F4 — Path-contract §5 names `/kb-management` as the dual-form writer but no NATIVE artifact performs the transform — IMPORTANT (operational-coherence)
- **Classification: Same root cause as F2; resolved by the F2 clarity edit.** The path-contract resource (a P0 file) is the right place to name the actual operator. The §3 runtime-greenlight-ownership note already states these are runtime outputs; the clarity edit adds that the coordinator (loading this contract) owns the transform.
- **Resolution:** Apply scoped clarity edit to `prep/resources/path-contract.md` §5. Re-run boundary check.

### F5 — Tier-key vocabulary mismatch: prep SKILL.md "{1,2,3,5}" vs template "{tier_1, tier_2, tier_3, tier_4_5}" — IMPORTANT/MINOR (operational-coherence)
- **Classification: NOT a defect — documented carried-verbatim drift.** `{1,2,3,5}` is the canonical LAF tier set (laf-adaptation/CLAUDE.md §3: "subset of {1,2,3,5}", "Tier 4 is interpolated, never stored"). The template's `tier_4_5` key is carried-verbatim prior art; the framework handles such drift via key-tolerant readers (CLAUDE.md §3: "key-tolerant `.get(a) or .get(b)`"). The QA agent itself notes the existing `tolkien-mapping.yaml` uses `tier_1`/`tier_3`, confirming the template vocabulary is prior art, not a contract the prep pipeline must match at build time. The P3 runtime mapping uses the design's tier set.
- **Resolution:** No action — documented carried-verbatim drift handled by key-tolerant readers.

### F6 — `tier-coordinator` listed in prep-cordinator `tools:` but never dispatched — MINOR (operational-coherence)
- **Classification: NOT a defect — verbatim from the design authority.** `prep-agent-schemas.md` §1 frontmatter specifies `tools: > Agent(web-researcher, analyst, tier-coordinator), ...`. The QA agent itself calls this "permissive over-listing, not a defect." Removing it would DEVIATE from the design pack.
- **Resolution:** No action — design-faithful. (If the design later drops it, that's a design change, not a P0 build correction.)

### F7 (from boundary-safety) — CLAUDE.md doc-drift ("15 agents / 16 skills") — Medium
- **Classification: Documentation drift outside the boundary hash-pin glob.** CLAUDE.md is NATIVE and not hash-pinned; the boundary stays green. The counts (now 16 agents / 18 skills) are a documentation accuracy issue for future contributors, not a P0 deliverable defect. Updating CLAUDE.md counts is outside this task's checklist scope (no checklist item touches CLAUDE.md body content).
- **Resolution:** Logged as a Follow-Up Item (not blocking; CLAUDE.md is not a task deliverable).

### F8 (from design-fidelity) — 3 MINOR authorized divergences
- Sparser exemplar provenance, narnia→tolkien example swap, genericized writing-principles reference — all explicitly authorized by the design pack (research confirmed narnia→tolkien is the documented staleness correction).
- **Resolution:** No action — authorized.

## Fix scope for the serialized fix agent (I20 — single agent)

Apply ONLY the F2/F4 clarity edit:
1. `laf-adaptation/agents/prep-cordinator.md` Stage 7 — make explicit the coordinator owns the dual-form transform (path-contract §3 as rule) and invokes `/kb-management` for the kb-lifecycle write.
2. `laf-adaptation/skills/prep/SKILL.md` §6 — same clarification.
3. `laf-adaptation/skills/prep/resources/path-contract.md` §5 — name the coordinator (loading this contract) as the transform operator.

MUST NOT touch: the analyst branch (F1/F3 — P1's job), the tier-coordinator tools entry (F6 — design-faithful), the tier vocabulary (F5 — documented drift), CLAUDE.md (F7 — out of scope). After the edit, re-run `uv run python laf-adaptation/scripts/check_boundary.py` and confirm the final line begins `BOUNDARY CONTRACT: PASS`.
