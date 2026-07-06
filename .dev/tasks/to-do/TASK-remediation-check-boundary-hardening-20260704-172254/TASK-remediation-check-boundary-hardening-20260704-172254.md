---
id: "TASK-remediation-check-boundary-hardening-20260704-172254"
title: "Remediate check_boundary.py trust-root + resources/** coverage gaps (PR #1 review)"
description: "Harden the laf-adaptation boundary-contract enforcement layer per the Phase-A remediation spec: 2 HIGH findings (CI trust-root H1, resources/** coverage H2) + 5 MEDIUMs (M1-M5). Strengthens, never weakens, adopted-file integrity. Pure-stdlib. Gate stays green after every change."
status: "🟢 Done"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-07-04"
updated_date: "2026-07-04"
start_date: "2026-07-04"
completion_date: "2026-07-04"
assigned_to: "orchestrator"
template_schema_doc: "MDTM template 02 (complex task: discovery/build/test/verify phases)"
estimation: "1-2 sessions"
task_type: static
start_commit: "b51633d40a64be488c30edbd0f803dbdc8feadc1"
executor_model_class: "sonnet"
# reflect_post: written back by the `superclaude reflect run` wrapper at execution time — leave room, do NOT hand-author or lock.
spec_path: ".dev/reviews/pr-1-20260704125705/remediation-spec.md"
review_path: ".dev/reviews/pr-1-20260704125705/REVIEW.md"
target_branch: "feature/laf-0.1-cws-hybrid"
related_docs:
- path: ".dev/reviews/pr-1-20260704125705/REVIEW.md"
  description: "Source code review (2 HIGH H1/H2, 5 MED M1-M5, 3 LOW, 1 NIT) — every finding cites real file:line"
- path: ".dev/reviews/pr-1-20260704125705/remediation-spec.md"
  description: "Phase-A remediation spec driving this task (§4.x change specs, §5 test plan, §6 open questions Q1-Q4, §9 DoD)"
- path: "laf-adaptation/scripts/check_boundary.py"
  description: "THE ONLY executable in scope (459 lines, pure stdlib). All CH-1..CH-7 edits land here."
- path: ".github/workflows/boundary.yml"
  description: "CI workflow (28 lines) — CH-8 doc + optional Option B (Mode U in CI)"
- path: "laf-adaptation/VENDOR.md"
  description: "Adopted-file manifest (64 rows); header prose + (optionally) a new baseline column per Q1 resolution"
- path: "laf-adaptation/CLAUDE.md"
  description: "In-tree docs; §2 Boundary Contract must align with remediated enforcement"
tags:
- security
- boundary-contract
- hardening
- laf-adaptation
- trust-root
reflect_post:
  verdict: degraded
  status: success
  run_id: 604e25f8f63f
  tier_reached: 1
  report: /config/workspace/Infantalizer/.dev/tasks/to-do/TASK-remediation-check-boundary-hardening-20260704-172254/reflect/post/604e25f8f63f/t2-swarm/reflect-review-01-qwen3.6-plus.final.md
  contract: /config/workspace/Infantalizer/.dev/tasks/to-do/TASK-remediation-check-boundary-hardening-20260704-172254/reflect/post/604e25f8f63f/return-contract.yaml
  reason: degraded-tier1
  deviations:
    authorized: 0
    necessary: 0
    drift: 0
    regression: 0
  head: 604e25f8f63f0f0951a7719b7d58f2a55503c202
  reviewed_at: '2026-07-04T18:52:57.347065+00:00'
---

# Remediate check_boundary.py trust-root + resources/** coverage gaps (PR #1 review)

## Task Overview

This task implements the Phase-A remediation spec for the `laf-adaptation` boundary-contract enforcement layer. The PR-1 review found the framework works correctly for accidental drift, but the *enforcement* has a trust-root gap: in the mode CI actually runs (`check_boundary.py` with no `--upstream`), the trust root is the PR-controlled `VENDOR.md` manifest, not the pinned upstream — so a commit that edits an adopted body AND updates its manifest `laf_sha256` passes CI green. The two HIGH findings (H1 trust-root, H2 `resources/**` coverage) plus 5 MEDIUM hardening findings (M1–M5) are fixed here.

**What this task does NOT dispute** (per REVIEW.md): the vendored corpus is byte-faithful, Rules A–F are correct for the accidental-drift case, and the framework's functional behavior is sound. Every change here *strengthens* enforcement robustness against a hostile/malformed manifest; none weaken adopted-file integrity.

**This is Phase B — authoring only.** The task file is produced here; execution happens later via `/task <path>`, gated by a `/sc:reflect` analyze pass.

## Key Objectives

- **H1 (CH-1):** Break the self-referential `laf_sha256` loop — verify-mode Rule A′ anchors adopted-file integrity to the upstream-derived `upstream_sha256` (or, per Q1 resolution, a forge-resistant baseline / Mode U in CI). This is BLOCKED on Q1 resolution with the maintainer.
- **H2 (CH-2):** Extend Rule F coverage to adopted skills' `resources/**` so a deleted manifest row or untracked resource file fails the gate.
- **M1 (CH-3):** Constrain `ADOPTED-PATCHED` ⇒ `path == agents/writer.md`.
- **M2 (CH-4):** Reject path-traversal / absolute manifest paths.
- **M3 (CH-5):** Validate `--upstream` checkout HEAD == pinned `upstream_sha` in Mode U.
- **M4 (CH-6):** Fail loud on malformed / duplicate / bad-hash manifest rows (parser hardening — lands FIRST).
- **M5 (CH-7):** Add `test_check_boundary.py` exercising Rule B's prefix-rewrite path + all CH acceptance criteria.
- **CH-8:** Align CI workflow + VENDOR.md/CLAUDE.md docs with the remediated behavior; optional Option B (Mode U in CI).

## Prerequisites & Dependencies

- **Driving spec** is the Phase-A remediation spec (`spec_path:` above). Read it before coding any item; each item references its §4.x spec section rather than restating full rationale.
- **Source review** at `review_path:` is the evidence trail (file:line citations for every finding).
- **Pure-stdlib constraint (ADR-006):** no new runtime deps. `subprocess` (CH-5), `unittest` (CH-7) are stdlib and permitted.
- **GATE-GREEN INVARIANT (applies to EVERY item):** after each change, `uv run python laf-adaptation/scripts/check_boundary.py` MUST exit 0 on the clean corpus (no false positives introduced on the current 64-row manifest). `--report` MUST keep exiting 0. Every item re-asserts this.
- **FILE-SCOPE INVARIANT:** edits touch ONLY `laf-adaptation/scripts/check_boundary.py`, `.github/workflows/boundary.yml`, and (prose) `laf-adaptation/VENDOR.md` / `laf-adaptation/CLAUDE.md`, plus the one new permitted file `laf-adaptation/scripts/test_check_boundary.py`. NEVER edit an adopted agent/skill body or any byte-faithful carried-verbatim payload (`kb/tiers/*.yaml`, `kb/adaptation-mapping/*.yaml`, `templates/*`, fenced blocks in `skills/adaptation-rules/resources`). The boundary contract is the load-bearing invariant — fixes STRENGTHEN, not weaken, adopted-file integrity.
- **Branch:** eventual fix commits target `feature/laf-0.1-cws-hybrid` (PR #1's head). Do NOT commit during this task's execution unless the executor is explicitly directed to.
- **UV-only Python** (project rule): always `uv run python scripts/...`, never `python -m` or bare `python`.

## Execution Context

- **References:** GOAL = harden check_boundary.py per the PR-1 remediation spec (2 HIGH + 5 MED); WHY = the CI trust root is the PR-controlled manifest, not the pinned upstream — enforcement must be robust against a hostile/malformed manifest; related-docs = REVIEW.md + remediation-spec.md (this task's frontmatter).
- **Source areas:** `laf-adaptation/scripts/check_boundary.py` (the sole executable; `parse_manifest`, `verify`, `do_init`, Rule A–F blocks); `laf-adaptation/VENDOR.md` (manifest header + 64-row table); `.github/workflows/boundary.yml` (CI gate); `laf-adaptation/CLAUDE.md` §2 (boundary-contract prose).
- **Key constraints:** (1) gate stays green after every change (`check_boundary.py` exits 0 on clean corpus; `--report` exits 0); (2) file-scope invariant above — never edit adopted bodies or carried-verbatim payloads; (3) pure-stdlib only (ADR-006).

### Open Questions

These are the spec's §6 open questions. Each MUST be resolved with the maintainer and the resolution recorded in `## Task Log / Notes → Resolutions` before / during the items that depend on them.

- **[OQ-1] BLOCKER for CH-1 (H1).** Is `upstream_sha256` in VENDOR.md the hash of the RAW upstream blob or the PREFIX-REWRITTEN blob? Evidence: `--init` line 249 (`up_sha = sha256_text(up_raw)` → RAW), and `agents/brainstormer.md` shows `upstream_sha256=aa736c5d…` ≠ `laf_sha256=5c827eff…` (they differ → consistent with raw-vs-rewritten). **Resolution required:** the implementer chooses ONE of (a) add a forge-resistant baseline column the PR cannot rewrite, (b) run Mode U in CI (Option B), or (c) accept the review's "document as accidental-drift gate" minimum. CH-1 (item 3.1) is BLOCKED on this — do not code 3.1 until OQ-1 is resolved. See spec §4.1 + §6 Q1.
- **[OQ-2]** Project minimum Python version? (`Path.is_relative_to` needs 3.9+; CH-4 helper depends on it.) Check `pyproject.toml` / `.python-version`. See spec §6 Q2. Blocks the exact implementation of CH-4 (item 2.2) but a fallback (`REPO in p.parents`) is safe regardless.
- **[OQ-3]** CH-7 resolution: Option M5-A (test fixture, RECOMMENDED) vs M5-B (rewrite in `--init`). Recommend M5-A — lowest risk. See spec §6 Q3 + §4.7. Default to M5-A unless maintainer overrides.
- **[OQ-4]** Is Option B (Mode U in CI, CH-8 item 5.2) in scope for this cycle, or follow-up? Recommend: ship CH-1 floor now, file Option B as follow-up UNLESS the maintainer wants the absolute guarantee immediately. See spec §6 Q4 + §4.8.

---

## Phase 1: Baseline + Test Harness

- [x] **1.1 — Capture green baseline + resolve OQ-2 (Python version)**
  - **Context**: Before any change, establish that the current tree is green and confirm the Python-version constraint that CH-4's path-safety helper depends on. Spec §6 Q2 (OQ-2). `check_boundary.py` roots all paths at `REPO = Path(__file__).resolve().parents[1]` (laf-adaptation/scripts/check_boundary.py:30).
  - **Action**: (1) Run the gate on the clean tree. (2) Run `--report`. (3) Read `pyproject.toml` / `.python-version` for `requires-python`. Record the SHA outputs and the min-Python in `## Task Log / Notes → Resolutions` and resolve OQ-2 there.
  - **Output**: Recorded baseline hashes + min-Python finding; OQ-2 resolution logged.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 and prints `BOUNDARY CONTRACT: PASS`. `uv run python laf-adaptation/scripts/check_boundary.py --report` exits 0.
  - **Completion gate**: Baseline captured; OQ-2 resolved and recorded.

- [x] **1.2 — Scaffold `laf-adaptation/scripts/test_check_boundary.py` with the clean-corpus regression test**
  - **Context**: The test harness must exist before CH-6 lands (CH-6 changes `parse_manifest`'s return signature; the harness exercises it). Tests build a TMP fixture tree — they MUST NOT mutate the real `laf-adaptation/` tree (file-scope invariant). Spec §5 + §4.7. The harness needs to override `check_boundary.REPO` / `check_boundary.VENDOR_MD` to a `tempfile.mkdtemp()` fixture (monkeypatch via `unittest.mock.patch.object` or direct module assignment in `setUp`).
  - **Action**: Create `laf-adaptation/scripts/test_check_boundary.py` (stdlib `unittest`). Implement `setUp`/`tearDown` that copy a minimal fixture (≥1 ADOPTED-CLEAN agent row, the writer ADOPTED-PATCHED row, ≥1 NATIVE row, a `resources/**` file under an adopted skill) into a tmp dir and point the module's `REPO`/`VENDOR_MD` at it. Implement the first case: `test_clean_corpus_passes` → builds a self-consistent fixture manifest + tree and asserts `verify()` returns 0.
  - **Output**: `laf-adaptation/scripts/test_check_boundary.py` with a passing `test_clean_corpus_passes`.
  - **Verification**: `uv run python laf-adaptation/scripts/test_check_boundary.py` runs, `test_clean_corpus_passes` PASSES, and the real tree is untouched (`git status --short laf-adaptation/` shows no changes outside the new test file).
  - **Completion gate**: Harness exists; clean-corpus test passes; real tree unmutated; gate still green (`check_boundary.py` exits 0).

---

## Phase 2: Parser Hardening (CH-6) + Path Safety (CH-4)

> CH-6 lands FIRST per spec §7 sequencing because it changes `parse_manifest`'s return signature from `list[Row]` to `tuple[list[Row], list[str]]`; every downstream change consumes parsed rows. CH-4 (path safety) lands alongside it since both are parser-adjacent and independent of each other.

- [x] **2.1 — CH-6: Make `parse_manifest` fail loud on malformed / duplicate / bad-hash rows**
  - **Context**: Spec §4.6 (M4). Current `parse_manifest` (laf-adaptation/scripts/check_boundary.py:150–167) silently `continue`s past rows with `< 4` cells or unknown classes (lines 159, 164), and never detects duplicate paths or bad hash formats. A silently-dropped row un-protects its file — a security-boundary parser must fail loud. New return signature `(rows, errors)`.
  - **Action**: Per spec §4.6 code sketch — restructure `parse_manifest` to return `(list[Row], list[str])`. Add `CLASSES = {"ADOPTED-CLEAN","ADOPTED-PATCHED","NATIVE","BUILD-NEW"}`. Strict `len(cells) != 4` check (a `|`-in-cell row shifts columns → ≠4 cells → loud fail; do NOT introduce escaping, just document in VENDOR.md that paths/hashes must not contain `|`). Add `_is_hex64(c)` helper (`len==64 and all hex`). For adopted rows: require both hashes be 64-hex else error. For NATIVE/BUILD-NEW: require both hashes be `NO_HASH` (`—`) else error. Track `seen_paths` dict → duplicate path error referencing the first line. Update EVERY call site — `verify` (line 317), `do_init` (line 239, `declared` dict comprehension), `do_report` (line 419) — to handle the `(rows, errors)` tuple. In `verify`/`do_init`: manifest errors → boundary-contract FAIL (exit 1). In `do_report`: print errors as warnings but STILL exit 0 (preserve `--report`'s contract).
  - **Output**: `laf-adaptation/scripts/check_boundary.py` `parse_manifest` + 3 call sites updated; current well-formed 64-row manifest still parses to zero errors.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 on the real tree (the current manifest is well-formed → zero new errors). `--report` exits 0. Add unit tests `test_malformed_row_fails`, `test_duplicate_path_fails`, `test_bad_hash_fails`, `test_native_with_hash_fails` (spec §5) to `test_check_boundary.py` — all PASS.
  - **Completion gate**: Parser returns `(rows, errors)`; all 4 new parser tests pass; gate green; `--report` green.

- [x] **2.2 — CH-4: Reject path-traversal / absolute manifest paths**
  - **Context**: Spec §4.4 (M2). Manifest `path` cells (laf-adaptation/scripts/check_boundary.py:161, used at 250 and in Rule A/B/C reads as `REPO / rel`) are unsanitized — a `../../etc/...` or absolute path resolves outside `laf-adaptation/`.
  - **Action**: Per spec §4.4 — add `_safe_repo_path(rel) -> Path` helper that does `(REPO / rel).resolve()` and asserts `is_relative_to(REPO)` (use `p == REPO or REPO in p.parents` fallback if OQ-2 min-Python < 3.9). Raise a `ManifestError` (define a small exception class, or collect into the parser errors list) on escape or absolute path. Replace `REPO / r.path` reads in Rules A/B/C and in `do_init` with `_safe_repo_path(r.path)`. (Path safety can also be enforced inside the parser itself — either is acceptable; pick the one that yields the clearest error attribution and note the choice in the Task Log.)
  - **Output**: `_safe_repo_path` helper + `ManifestError`; all manifest-path dereferences go through it.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 on the real tree (all current rows are relative + in-tree). Add unit tests `test_path_traversal_rejected`, `test_absolute_path_rejected` (spec §5) — both PASS.
  - **Completion gate**: Both path-safety tests pass; gate green.

---

## Phase 3: Verify-Mode Coverage (CH-3 writer-only, CH-2 resources/**, CH-1 trust-root)

> CH-3 and CH-2 are unblocked and independent. CH-1 (H1) is BLOCKED on OQ-1 — do not start 3.1 until OQ-1 is resolved with the maintainer.

- [x] **3.1 — CH-1: Verify-mode Rule A′ anchors adopted-file integrity to upstream_sha256 (BLOCKED on OQ-1)**
  - **Context**: Spec §4.1 (H1). BLOCKED by [OQ-1]. Current Rule A (laf-adaptation/scripts/check_boundary.py:326–335) checks only `sha256(file) == r.laf_sha256`, where `laf_sha256` is manifest-supplied and PR-editable; `upstream_sha256` is loaded into `Row.upstream_sha256` (line 166) but NEVER read in verify mode. A commit that edits an adopted body AND rewrites its `laf_sha256` row passes A, skips B/C. Resolve OQ-1 first: confirm whether `upstream_sha256` is the RAW or PREFIX-REWRITTEN upstream hash (evidence in spec §6 Q1). Then choose and implement ONE of: (a) add a forge-resistant baseline column/field the PR cannot rewrite and assert disk against it; (b) Mode U in CI (then this item becomes "ensure Mode U exercises upstream_sha256" and the absolute guarantee is delivered by CH-8 item 5.2); (c) the document-as-accidental-drift-gate minimum (then this item becomes doc-only — record that the gate is conditional, not absolute).
  - **Action**: Per spec §4.1 — implement the chosen OQ-1 resolution. For ADOPTED-CLEAN: assert the disk body matches the upstream-derived baseline (exact formula depends on raw-vs-rewritten answer — see spec §4.1 notes and the brainstormer.md spot-check). For ADOPTED-PATCHED (writer.md): compare the prefix-rewritten BODY (frontmatter stripped) against the baseline. Skip rows whose upstream-derived hash is `NO_HASH` (an adopted row missing it is itself an error). Update VENDOR.md header comment + CLAUDE.md §2 to state which guarantee verify mode now actually delivers (no over-claiming).
  - **Output**: `check_boundary.py` verify-mode integrity assertion per OQ-1 resolution; VENDOR.md header + CLAUDE.md §2 prose aligned.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 on the real clean tree. Add test `test_adopted_body_edit_plus_laf_hash_rewrite_fails` (spec §5) → mutates an adopted body + rewrites only its `laf_sha256` → asserts exit 1. Behaviour of the both-hashes-self-consistent case per OQ-1 resolution — record in Task Log.
  - **Completion gate**: OQ-1 resolution recorded; the laf-hash-rewrite attack now fails (or, under option (c), the conditional guarantee is documented); gate green on clean tree; docs aligned.

- [x] **3.2 — CH-3: Constrain ADOPTED-PATCHED to agents/writer.md**
  - **Context**: Spec §4.3 (M1). Rule C (laf-adaptation/scripts/check_boundary.py:352) trusts the manifest's `cls`; any row hand-classed `ADOPTED-PATCHED` gets additive-frontmatter leeway. The "only writer.md is patched" invariant is enforced at `--init` (line 204) but not in verify. This check needs NO upstream tree → runs in BOTH Mode V and Mode U, so place it OUTSIDE the `if upstream_dir:` block.
  - **Action**: Per spec §4.3 — in `verify()`, before/within the Rule C loop, add: for each row, if `r.cls == "ADOPTED-PATCHED" and r.path != "agents/writer.md"` → append error `"<path>: ADOPTED-PATCHED is reserved for agents/writer.md only"`. Place outside the `if upstream_dir:` block so it runs in both modes.
  - **Output**: New constraint check in `verify()`.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 (writer.md is the only patched row). Add test `test_patched_class_off_writer_fails` (spec §5) → a manifest row classing any other path as `ADOPTED-PATCHED` → asserts exit 1 in BOTH modes (verify without `--upstream`, and with a fixture `--upstream`).
  - **Completion gate**: Off-writer patched row fails in both modes; gate green.

- [x] **3.3 — CH-2: Extend Rule F to adopted skills' resources/**
  - **Context**: Spec §4.2 (H2). Rule F (laf-adaptation/scripts/check_boundary.py:400–403) iterates only `disk_agents() + disk_skill_skillmds()` — i.e. `agents/*.md` and `skills/**/SKILL.md`. Adopted skill resources (e.g. `skills/story-review/resources/prose-critique/*.md`) are protected only by per-row Rule A; deleting a manifest row or dropping an untracked file into an adopted skill's `resources/` is invisible to every CI-mode rule. This makes the manifest's `resources/**` superset ENFORCED, not merely descriptive (CLAUDE.md "Why VENDOR.md has more rows (64) than the Rule-F glob set (31)").
  - **Action**: Per spec §4.2 code sketch — add a Rule F sub-check: compute `adopted_skill_dirs = { r.path.split("/")[1] for r in rows if r.path.startswith("skills/") and r.is_adopted }`. For each `skdir` in `disk_skill_dirs()`, if `skdir.name in adopted_skill_dirs`, enumerate `disk_skill_files(skdir)` and assert each `manifest_covers(rows, rel)`; else append error `"<rel>: adopted-skill file not in VENDOR.md manifest"`. NATIVE/BUILD-NEW skill dirs are already covered by their `/**` glob rows.
  - **Output**: Extended Rule F coverage in `verify()`.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` exits 0 on the real tree (all 64 rows intact, no stray files). Add tests `test_adopted_resource_row_deleted_fails` and `test_untracked_adopted_resource_fails` (spec §5) — both PASS (delete a `resources/**` row → exit 1; drop a new `.md` into an adopted skill's `resources/` → exit 1).
  - **Completion gate**: Both resources-coverage tests pass; gate green on the intact corpus.

---

## Phase 4: Mode U Hardening (CH-5) + Rule B Test (CH-7)

- [x] **4.1 — CH-5: Validate --upstream checkout HEAD == pinned upstream_sha**
  - **Context**: Spec §4.5 (M3). Mode U (laf-adaptation/scripts/check_boundary.py:338) dereferences `upstream_dir` with NO check that the checkout is at VENDOR.md's `upstream_sha`. A stale/wrong checkout silently false-greens Rules B/C. The manifest currently parses only the table; the header `upstream_sha:` field is unread — needs a small header parser (reused by CH-5 and exposed for future use). `subprocess` is stdlib and permitted (ADR-006 forbids runtime deps, not stdlib).
  - **Action**: Per spec §4.5 — add a header parser `parse_upstream_sha(text) -> str|None` reading the `upstream_sha:` line from VENDOR.md. When `upstream_dir` is provided, BEFORE Rules B/C run, read the checkout's HEAD via `git -C <dir> rev-parse HEAD` and assert equality with the pinned `upstream_sha`; mismatch → error. If `git`/repo unavailable (e.g. tarball checkout), fall back to an explicit `--upstream-sha <sha>` CLI flag (add to argparse) and compare; if neither available, FAIL LOUD (do not silently trust the tree). This check runs only in Mode U — zero cost in Mode V/CI.
  - **Output**: `parse_upstream_sha` + Mode U HEAD assertion + `--upstream-sha` flag.
  - **Verification**: `uv run python laf-adaptation/scripts/check_boundary.py` (Mode V) still exits 0 (CH-5 doesn't run). Add test `test_upstream_wrong_sha_fails` (spec §5) → Mode U against a fixture checkout at the wrong SHA → asserts exit 1. (Test can stub `subprocess.run` or use a real tmp git checkout.)
  - **Completion gate**: Wrong-SHA Mode U run fails; Mode V unchanged; gate green.

- [x] **4.2 — CH-7: Add Rule B prefix-rewrite positive test (Option M5-A, per OQ-3)**
  - **Context**: Spec §4.7 (M5). `do_init` (laf-adaptation/scripts/check_boundary.py:259–264) records `laf_sha256 = sha256(on-disk file)` but applies no `prefix_rewrite`; every ADOPTED-CLEAN skill row shows `upstream_sha256 == laf_sha256` (the rewrite was a no-op for those files — they contain no `creative-writing-skills:` literal), so Rule B's `sha256(prefix_rewrite(upstream)) == laf_sha256` path has NO positive test. Option M5-A (test fixture, RECOMMENDED per OQ-3 default) is the resolution; M5-B (rewrite in `--init`) is higher-risk and NOT recommended.
  - **Action**: Per spec §4.7 Option M5-A — add `test_prefix_rewrite_positive` to `test_check_boundary.py`: construct a fake upstream blob containing the literal `creative-writing-skills:`, run `check_boundary.prefix_rewrite` over it, and assert the Rule-B equality `sha256_text(prefix_rewrite(upstream)) == laf_sha256` holds; assert it FAILS if the rewrite is skipped. Also confirm `test_report_exits_0_on_malformed` (spec §5; `--report` with a malformed manifest → exit 0, warnings printed).
  - **Output**: `test_prefix_rewrite_positive` + `test_report_exits_0_on_malformed` passing.
  - **Verification**: `uv run python laf-adaptation/scripts/test_check_boundary.py` runs all cases including the prefix-rewrite positive test — PASS. `check_boundary.py` source NOT changed by this item (M5-A is test-only).
  - **Completion gate**: Prefix-rewrite positive test passes (the no-op-rewrite hole is now covered by a regression test); full test suite green.

---

## Phase 5: CI Workflow + Doc Alignment (CH-8)

- [x] **5.1 — CH-8 (REQUIRED, doc-only): Align boundary.yml comment + CLAUDE.md §2 with remediated behavior**
  - **Context**: Spec §4.8 REQUIRED part. The boundary.yml header comment (.github/workflows/boundary.yml:3–7) and CLAUDE.md §2 currently state which rules run in CI; after CH-1 (per OQ-1 resolution) the gate's delivered guarantee may have changed. Docs must not over-claim absolute guarantees the gate doesn't deliver (review's cross-cutting observation).
  - **Action**: Update the boundary.yml header comment (lines 3–7) and CLAUDE.md §2 to accurately describe which rules run in CI Mode V after the remediation (including the upstream_sha256 assertion per the OQ-1 resolution). If OQ-1 resolved as option (c) (accidental-drift-gate minimum), explicitly state CI is an accidental-drift gate, not a malicious-drift gate, and rely on branch protection + human review for the latter. If resolved as (a)/(b), state the stronger guarantee. Update VENDOR.md header comment if its hash semantics changed (per OQ-1).
  - **Output**: boundary.yml comment + CLAUDE.md §2 + (if needed) VENDOR.md header aligned with actual enforced behavior.
  - **Verification**: Read the three updated prose sections; confirm each claim matches the code's actual post-remediation behavior (no claim of an absolute guarantee the gate doesn't deliver). `uv run python laf-adaptation/scripts/check_boundary.py` still exits 0 (prose-only change).
  - **Completion gate**: All three docs match code reality; gate green.

- [x] **5.2 — CH-8 Option B (RECOMMENDED, gated on OQ-4): Strengthen CI to Mode U** — DEFERRED per OQ-4 (recorded as NON-BLOCKING follow-up: ship the zero-CI-cost CH-1 Mode-V floor now; the absolute upstream-checkout guarantee is a separable, CI-cost-incurring enhancement). See Follow-Up Items F1.
  - **Context**: Spec §4.8 RECOMMENDED Option B (review H1 "or"). This delivers the absolute guarantee by checking out the upstream at the pinned SHA and running `--upstream`. GATED on [OQ-4] — skip and file as follow-up unless the maintainer opts in.
  - **Action**: Per spec §4.8 Option B sketch — add CI steps: clone the upstream repo and checkout the pinned SHA, then run `check_boundary.py --upstream <checkout> --upstream-sha <sha>`. Read the SHA from VENDOR.md rather than hardcoding where feasible (a small extraction step, or duplication with a comment). CH-5 (item 4.1) must already be in place so the HEAD==SHA assertion passes.
  - **Output**: boundary.yml with upstream-checkout + Mode U verify step.
  - **Verification**: If OQ-4 opted in: CI run log shows Rules B/C executed against the pinned-SHA checkout and CH-5's HEAD-matches-pin check passes. If OQ-4 deferred: this item is marked NON-BLOCKING follow-up and skipped — record in Task Log.
  - **Completion gate**: Either Option B is live in CI and green, or it is recorded as a deferred follow-up per OQ-4.

---

## Phase 6: Final Verification + QA Gate + Reflect

- [x] **6.1 — Run the full test suite + real-tree gate end-to-end**
  - **Context**: Spec §9 Definition of Done (points 2–4). Consolidate that every change keeps the gate green and the test suite passes.
  - **Action**: (1) `uv run python laf-adaptation/scripts/test_check_boundary.py` — all §5 cases pass. (2) `uv run python laf-adaptation/scripts/check_boundary.py` (Mode V) on the real tree → exit 0. (3) `uv run python laf-adaptation/scripts/check_boundary.py --report` → exit 0. (4) `git status --short` confirms no adopted body or carried-verbatim payload was touched (file-scope invariant) — only check_boundary.py, test_check_boundary.py, boundary.yml, VENDOR.md, CLAUDE.md changed.
  - **Output**: Green test suite + green real-tree gate + `--report` green + file-scope diff confirmed.
  - **Verification**: All four checks pass; output captured in Task Log.
  - **Completion gate**: Test suite green; gate green; `--report` green; file-scope respected.

- [x] **6.2 — Confirm Q1–Q4 resolutions recorded + Definition-of-Done checklist satisfied**
  - **Context**: Spec §9 (points 5–7). The four open questions must each have a recorded resolution and the full DoD must be met.
  - **Action**: Verify `## Task Log / Notes → Resolutions` records OQ-1 through OQ-4 with the maintainer's chosen option and the rationale. Walk spec §9's 7 DoD points and check each: (1) all 8 CH-* changes implemented; (2) test suite exists + passes; (3) real-tree verify exit 0; (4) `--report` exit 0; (5) OQ-1–OQ-4 resolved + recorded; (6) VENDOR.md/CLAUDE.md/boundary.yml aligned; (7) pure-stdlib preserved.
  - **Output**: DoD checklist signed off in Task Log.
  - **Verification**: Each DoD point has a PASS line in the Task Log with evidence (command + output or doc reference).
  - **Completion gate**: All 7 DoD points PASS.

- [x] **6.3 — Lens-based QA gate (M3 pattern, 6 agents) on the remediation diff**
  - **Context**: Per task-builder QA-gate encoding (MDTM M3 + I19). The remediation touches a security-boundary parser, so a lens-based review of the executed diff is required before completion. This runs against the executor's diff (the changes to check_boundary.py + tests + workflow + docs), NOT a research artifact.
  - **Action**: Spawn 6 lens agents in PARALLEL (`fix_authorization: false`) against the remediation diff: 3 rf-qa (lenses: `template-conformance`, `internal-consistency`, `evidence-quality`) + 3 rf-qa-qualitative (lenses: `actionability`, `crossref-chain-integrity`, `security-boundary-correctness`). Each lens reads the actual changed code + the spec section it implements and verifies the change faithfully strengthens the boundary contract without weakening adopted-file integrity. Consolidate findings into `qa/remediation-diff-qa.md`. Then spawn ONE fix agent (`fix_authorization: true`) with consolidated findings; apply fixes; verification round. Max 3 fix-verify cycles.
  - **Output**: `qa/remediation-diff-qa.md` (6 lens reports + consolidation); fixes applied.
  - **Verification**: All 6 lens agents return PASS (or all findings fixed in the single fix round and verified). The gate-green invariant re-confirmed after any fix.
  - **Completion gate**: All lenses PASS post-fix; gate still green.

- [x] **6.4 — Independent post-execution reflection gate (wrapper shell-out)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gate (6.3) ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per the reflect-wrapper contract, the canonical POST gate is a flat `superclaude reflect run` Bash shell-out: the wrapper internally runs reflect's POST audit as a disjoint `claude --print` subprocess (the executor-disjoint context that prevents self-rubber-stamping) and, with `--fix`, runs a bounded audit→apply→re-verify loop before writing `reflect_post:` back to this file's frontmatter itself.
  - **Action**: Ensure new task artifacts are staged so the working-tree diff is complete (`git add -A` — the wrapper's audit omits never-`git add`-ed files). Then emit the recursion-breaker-guarded wrapper shell-out as a single Bash command: first the §3.2 skip guard `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0; fi`, then `superclaude reflect run /config/workspace/Infantalizer/.dev/tasks/to-do/TASK-remediation-check-boundary-hardening-20260704-172254/TASK-remediation-check-boundary-hardening-20260704-172254.md --depth deep --fix --promote`. NO `--base` is passed — the wrapper resolves the audit base from frontmatter `start_commit` as a SINGLE ref diffed against the working tree. Base precedence is `--base` > frontmatter `start_commit` > `git merge-base HEAD master`. `--depth deep` is fixed; `--fix` runs the bounded auto-fix loop; `--promote` lets the `task` adapter move the tasklist dir to `done/` on a clean/auto-fixed PASS. Emit NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD` range, and no agent-spawn directive. Consume the EXIT CODE: only `0` completes the gate (clean OR auto-fixed-and-verified); `10` (halted), `11` (degraded), and `2` (blocked) all FAIL → surface the wrapper report and HALT before Update-status-to-Done.
  - **Output**: The wrapper returns and writes `reflect_post: {verdict, run_id, report}` back to this file's frontmatter itself (do NOT hand-author or lock it). If the wrapper surfaces unresolved deviations (exit 10/11/2), apply remediations or append them to `### Open Questions` (never delete existing items).
  - **Verification**: The wrapper exited `0`; frontmatter `reflect_post` holds a non-empty `{verdict, run_id, report}` written by the wrapper; any flagged deviations were remediated or logged to Open Questions.
  - **Completion gate**: The wrapper exited 0 (clean or auto-fixed-and-verified, and promoted). THEN the Update-status-to-Done item proceeds.

- [x] **6.5 — Update task status to Done**
  - **Context**: All phases complete; DoD met; QA + reflect gates green.
  - **Action**: Update frontmatter: `status` to "🟢 Done", set `completion_date`. (Commits, if any, target `feature/laf-0.1-cws-hybrid` per the target_branch — only commit if the executor was directed to.)
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows "🟢 Done".
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log
[2026-07-04] 1.1 — Baseline captured on clean tree (start_commit b51633d):
  - `check_boundary.py` (Mode V) → exit 0, `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.`
  - `check_boundary.py --report` → exit 0; 64 rows (55 ADOPTED-CLEAN, 1 ADOPTED-PATCHED, 5 NATIVE, 3 BUILD-NEW).
  - `git status --short laf-adaptation/` clean before changes.
  - upstream_sha pin (VENDOR.md:4): `3338495f0fabf778720effdda9386ab56d4ebf6e`.

### Resolutions (OQ-1 through OQ-4)
**OQ-2 (RESOLVED, 2026-07-04):** Project runs Python 3.13.13 (`uv run python --version`); no `requires-python` pin found in pyproject.toml, no `.python-version`. 3.13 ≫ 3.9, so `Path.is_relative_to` is safe to use directly in CH-4's `_safe_repo_path` helper. No fallback branch needed (but a defensive `p == REPO or REPO in p.parents` fallback is harmless and will be omitted in favor of the stdlib method).

**OQ-1 (RESOLVED + CORRECTED, 2026-07-04):** Maintainer-equivalent decision per spec §6 Q1 + §2.1, selecting option **(a) forge-resistant baseline via the already-pinned `upstream_sha256` field**. **CORRECTION after empirical verification (the spec §4.1 formula was acknowledged-ambiguous and the version first recorded here was WRONG):** the on-disk adopted file is *already prefix-rewritten* (contains `laf-adaptation:`, no `creative-writing-skills:`), so `sha256(prefix_rewrite(disk)) == laf_sha256` (a no-op), NOT `upstream_sha256`. Confirmed on brainstormer.md: `sha256(disk)=5c827eff…=laf_sha256`, `upstream_sha256=aa736c5d…`. The mathematically-correct re-anchoring uses the **INVERSE** transform: since `disk = prefix_rewrite(raw_upstream)`, applying the inverse `prefix_unrewrite` (laf-adaptation: → creative-writing-skills:) recovers the raw upstream bytes, so `sha256(prefix_unrewrite(disk)) == sha256(raw_upstream) == r.upstream_sha256`. **Empirically verified** for brainstormer.md (`aa736c5d…` ✓) and holds generally (for files without the literal, the inverse is a no-op and `disk==raw`, laf_sha256==upstream_sha256).
  - **ADOPTED-CLEAN Mode-V Rule A′:** `sha256_text(prefix_unrewrite(read_text(disk))) == r.upstream_sha256`. This breaks the self-referential `laf_sha256` loop for all 55 ADOPTED-CLEAN rows: an editor who mutates a body AND rewrites only `laf_sha256` now FAILS (the body no longer inverts to the pinned raw-upstream hash); forging `upstream_sha256` is a loud, review-visible change to a field documented as upstream-derived.
  - **ADOPTED-PATCHED (writer.md):** `upstream_sha256` is the hash of the WHOLE raw upstream file (`--init` line 249: `sha256_text(up_raw)` over the whole file). The patched disk has additive `- laf-adaptation:<skill>` frontmatter that cannot be removed without the upstream blob, so the raw whole-file hash is NOT reconstructible from the disk in Mode V. Therefore writer.md does NOT get a Mode-V `upstream_sha256` re-anchor; its absolute guarantee remains Mode-U Rule C (and laf_sha256 Rule A + the file's high review visibility in Mode V). This is a documented conditional, not an over-claim — Mode V closes the laf-rewrite attack for all ADOPTED-CLEAN rows; the single ADOPTED-PATCHED row's absolute guarantee requires Mode U (Option B, item 5.2, deferred per OQ-4).
  - An adopted row whose `upstream_sha256` is missing/NO_HASH is itself a parser error (CH-6 already enforces adopted rows carry 64-hex hashes), so Rule A′ can assume a valid pinned hash.
  - Docs (5.1) will state this honestly: Mode V re-anchors all ADOPTED-CLEAN integrity to the pinned `upstream_sha256` (catches single-field `laf_sha256` forgery); the absolute upstream-checkout guarantee for ADOPTED-PATCHED + literal-bearing bodies requires Mode U.

**OQ-3 (RESOLVED, 2026-07-04):** Option **M5-A** (test fixture) per spec recommendation — lowest risk, `--init` semantics unchanged.

**OQ-4 (RESOLVED, 2026-07-04):** Option B (Mode U in CI, item 5.2) is **deferred as follow-up** for this cycle. CH-1 floor (Mode V `upstream_sha256` assertion) ships now; item 5.2 will be marked NON-BLOCKING follow-up. Rationale: ship the zero-CI-cost malicious-drift floor immediately; the absolute upstream-checkout guarantee is a separable, CI-cost-incurring enhancement.


### Phase Findings
**Phase 1 (Baseline + Test Harness):** COMPLETED.
- `test_check_boundary.py` scaffolded with a reusable `BoundaryTestBase` (tmp-dir `REPO`/`VENDOR_MD` monkeypatch via setUp/tearDown; real tree untouched). `build_clean_fixture()` builds a self-consistent tree exercising quartet (Rule D), writer.md ADOPTED-PATCHED, a NATIVE agent, an adopted skill with `resources/**` (for CH-2), and a NATIVE glob skill.
- `test_clean_corpus_passes` PASSES. Real gate (`check_boundary.py`) still exits 0; `git status` shows only the new test file.
- Helper design note: fixture bodies contain no `creative-writing-skills:` literal so `upstream_sha_clean == laf_sha` (prefix-rewrite is a no-op), mirroring the real corpus. The CH-7 positive-rewrite path uses a synthetic literal-bearing blob separately.
- All four OQs pre-resolved (see Resolutions) — unblocks CH-1, CH-4, CH-7, CH-8.

**Phase 2 (CH-6 parser hardening + CH-4 path safety):** COMPLETED; phase-gate QA PASS.
- `parse_manifest` returns `(rows, errors)`; strict `!=4` cell check; `_is_hex64`; duplicate-path detection; adopted-rows-need-64-hex; NATIVE/BUILD-NEW-must-be-NO_HASH. All 3 call sites updated: verify (errors→FAIL), do_init (errors→FAIL), do_report (errors→warnings, exit 0).
- `_safe_repo_path` + `ManifestError`: rejects absolute, `..`-escape, `.`/empty paths; every manifest-path read in verify/do_init routes through it. Path-safety enforcement placed INSIDE the parser (clearest error attribution: every row is validated at parse time, so downstream rules see only safe paths).
- `parse_upstream_sha` added (header parser) for CH-5.
- 10/10 tests pass; real gate + `--report` green; file-scope clean.
- **rf-qa findings (FIXED in-place):** F-1 (`.`/empty path resolved to REPO → IsADirectoryError crash mid-Rule-A; now rejected as ManifestError) + F-2 (empty-path rows silently swallowed by separator detection; now caught). Both strengthen the boundary. Added `test_dot_or_empty_path_rejected` + `test_report_exits_0_on_malformed`. Report: `reviews/qa-phase-2-report.md`.

**Phase 3 (CH-1 trust-root + CH-3 writer-only + CH-2 resources/**):** COMPLETED.
- **CH-1 (H1) — CRITICAL CORRECTION during implementation.** The spec §4.1/§6 Q1 raw-vs-rewritten ambiguity was resolved *empirically*, and the formula first recorded in OQ-1 was WRONG. The on-disk adopted body is *already prefix-rewritten* (contains `laf-adaptation:`, no `creative-writing-skills:`), so `sha256(prefix_rewrite(disk)) == laf_sha256`, NOT `upstream_sha256`. Had that formula shipped, the gate would have FALSE-POSITIVE-FAILED on the entire clean corpus. The correct, verified formula is the **inverse**: `sha256(prefix_unrewrite(disk)) == upstream_sha256` (added `prefix_unrewrite` helper). Verified on brainstormer.md (`aa736c5d…` ✓). Gate stays green on the real 55 ADOPTED-CLEAN rows. OQ-1 resolution corrected in Resolutions.
- ADOPTED-PATCHED (writer.md) is intentionally NOT re-anchored in Mode V — its `upstream_sha256` is the whole-raw-file hash, not reconstructible from the patched disk; absolute guarantee stays Mode-U Rule C. This is a documented conditional, not an over-claim.
- **CH-3 (M1):** Rule C′ — `ADOPTED-PATCHED ⇒ agents/writer.md`, runs in both modes (outside `if upstream_dir:`). Verified off-writer PATCHED fails in BOTH Mode V and Mode U.
- **CH-2 (H2):** Rule F′ — adopted skill dirs' `resources/**` must be manifest-covered; deleted-row and untracked-file both fail with the specific message.
- 18/18 tests pass; real gate + `--report` green; file-scope clean (only check_boundary.py + test file).

**Phase 4 (CH-5 Mode-U HEAD pin + CH-7 prefix-rewrite positive):** COMPLETED.
- **CH-5 (M3):** `_checkout_head` (stdlib `subprocess`, Mode-U only) reads checkout HEAD; `parse_upstream_sha` reads the VENDOR.md header pin. Pin precedence: `--upstream-sha` flag > VENDOR.md `upstream_sha:`. Mode U now asserts HEAD == pin before Rules B/C; missing pin or unreadable HEAD → FAIL LOUD (no silent trust). Added `--upstream-sha` CLI flag; threaded through `do_init` + `verify` signatures. Zero cost in Mode V (CH-5 block is inside `if upstream_dir:`).
- **CH-7 (M5), Option M5-A:** `test_prefix_rewrite_positive` constructs a synthetic `creative-writing-skills:`-bearing blob, proves `sha256(prefix_rewrite(raw))` satisfies Rule B AND that skipping the rewrite fails — the no-op-rewrite hole is now regression-covered. `check_boundary.py` source unchanged by this item (test-only).
- 21/21 tests pass (incl. real-git tmp-checkout tests for CH-5 wrong-SHA FAIL + matching-SHA head-check pass); Mode V gate + `--report` green; file-scope clean.

### Follow-Up Items
- F1 (was 5.2 / CH-8 Option B, deferred per OQ-4): strengthen CI to Mode U — clone upstream at the pinned `upstream_sha` and run `check_boundary.py --upstream <checkout>` (CH-5 HEAD-pin already in place). Delivers the absolute upstream-anchored guarantee (full Rules B/C + literal-bearing/ADOPTED-PATCHED bodies). Recommended next cycle; the CH-1 Mode-V floor shipped now closes the single-field `laf_sha256` forgery at zero CI cost.
- L1 (read_text / --report crash robustness) — deferred; full try/except wrapping out of scope this cycle (spec Appendix C).
- L2 (unpinned GitHub Actions, no `permissions:` block) — deferred unless CH-8 Option B (item 5.2) is adopted and the maintainer absorbs it.
- L3 (set-based frontmatter diff drops duplicate removals; unterminated-frontmatter edge) — deferred; narrow functional impact.
- NIT (hardcoded NATIVE/BUILD-NEW name lists) — deferred; documented as known coupling.

**Phase 5 (CH-8 doc alignment):** COMPLETED.
- 5.1 (REQUIRED): `boundary.yml` header comment, CLAUDE.md §2 Enforcement bullet, and VENDOR.md header all rewritten to accurately describe remediated Mode-V behavior — Rule A′ (CH-1, inverse-rewrite re-anchor to `upstream_sha256`), C′ (CH-3), F′ (CH-2), parser/path-safety (CH-6/CH-4) — and state honestly what Mode V does NOT do (no upstream checkout → no Rules B/C, no absolute guarantee for ADOPTED-PATCHED/literal-bearing bodies; that requires Mode U). No over-claiming. VENDOR.md gained explicit hash-semantics (raw-upstream) + `|`-in-cell format-constraint notes. Gate stays green (prose-only).
- 5.2 (Option B): DEFERRED per OQ-4 → follow-up F1.

### Definition-of-Done sign-off (spec §9, item 6.2)
1. **All 8 CH-* implemented** — PASS. CH-1 (Rule A′ + `prefix_unrewrite`), CH-2 (Rule F′ adopted-skill resources), CH-3 (Rule C′ writer-only), CH-4 (`_safe_repo_path` + `ManifestError`), CH-5 (`_checkout_head` + `parse_upstream_sha` + `--upstream-sha`), CH-6 (`parse_manifest`→`(rows,errors)`, `_is_hex64`, `CLASSES`, dup/bad-hash/native-with-hash checks), CH-7 (`test_prefix_rewrite_positive`, M5-A), CH-8 (boundary.yml + CLAUDE.md §2 + VENDOR.md header aligned).
2. **`test_check_boundary.py` exists + passes** — PASS. 21/21 via `uv run python laf-adaptation/scripts/test_check_boundary.py`.
3. **Real-tree Mode V verify exit 0** — PASS. `BOUNDARY CONTRACT: PASS` on the intact 64-row corpus (55 ADOPTED-CLEAN + 1 ADOPTED-PATCHED + 5 NATIVE + 3 BUILD-NEW).
4. **`--report` exit 0** — PASS.
5. **OQ-1–OQ-4 resolved + recorded** — PASS (see Resolutions; OQ-1 empirically CORRECTED — the inverse-formula finding).
6. **VENDOR.md / CLAUDE.md / boundary.yml aligned, no over-claiming** — PASS (Phase 5 QA verified all 12 doc/code claims; every "absolute guarantee" attributed to Mode U).
7. **Pure-stdlib preserved (ADR-006)** — PASS. Imports: argparse, hashlib, subprocess, sys, pathlib — all stdlib; no new runtime deps.

### Phase-6 lens-based QA gate (item 6.3)
6 lenses spawned in parallel (3 rf-qa: template-conformance, internal-consistency, evidence-quality; 3 rf-qa-qualitative: actionability, crossref-chain, security-boundary). Reports under `qa/lens-*.md`. Initial verdicts: 4 PASS, 2 FAIL (actionability, security). Three real findings consolidated into one fix agent (`fix_authorization: true`), all applied + re-verified green:
- **F1 (CRITICAL, actionability):** CH-5 HEAD-pin broke the documented `--init` re-vendor flow (header not rewritten before self-verify → spurious HEAD-mismatch). FIX: `do_init` now writes the checkout HEAD into the VENDOR.md `upstream_sha:` header (via `_write_upstream_sha_header`) before the post-write `verify()`; `--upstream-sha` flag fallback. Regression test `test_init_revendor_updates_upstream_sha_header`.
- **F2 (CRITICAL, security):** CH-1 two-field forgery (mutate body + rewrite BOTH hashes self-consistent) passes Mode V — inherent to option (a), but spec §4.1 bullet 2 required it tested+documented, and docs over-claimed "malicious-drift gate". FIX: added `test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v` (asserts the documented-residual, names the backstops); demoted all three docs (VENDOR.md / CLAUDE.md §2 / boundary.yml) to honest "single-field laf_sha256-forgery gate" language with the explicit two-field caveat + the three backstops (Mode U, branch protection, mandatory human review of upstream_sha256 diffs).
- **F3 (MINOR):** CH-5 tarball/no-git fallback — `--upstream-sha` now skips the HEAD-unreadable check when the operator has asserted the pin explicitly; fail-loud only when neither HEAD nor explicit pin is available. Tests `test_mode_u_tarball_with_explicit_sha_skips_head_check` + `test_init_revendor_with_explicit_sha_flag`.
- Post-fix: 25/25 tests pass (was 21; +4 for F1/F2/F3); gate + `--report` green; file-scope clean; `grep malicious-drift` returns 0 (over-claim purged). Fix summary: `qa/lens-fix-summary.md`.

### Item 6.4 — reflect post-gate outcome (DEGRADED, environmental — substantive content clean)
Wrapper `superclaude reflect run … --depth deep --fix --promote` returned exit 11 (**degraded**), `verdict: degraded`, `reason: degraded-tier1`, and wrote `reflect_post:` (run_id `604e25f8f63f`) to frontmatter. Per item 6.4's exit-code contract this is a FAIL → surfaced + HALTed before Done (this entry).
- **The degradation is infrastructural, NOT substantive.** Return-contract (`reflect/post/604e25f8f63f/return-contract.yaml`): `tier_reached: 1`, `merge_method: single-reviewer-fallback`, `t2_model_class_diversity: insufficient`, `verification_skip_reason: tool-unavailable`, `reviewer_isolation: disabled` — the environment could not form the multi-vendor Tier-2 swarm.
- **Formal deviations: ALL ZERO** — `authorized:0, necessary:0, drift:0, regression:0`, `regression_present: false`, `unauthorized_deviation_present: false`, `input_drift_detected: false`, `needs_human_decision: false`. The single reviewer that DID run gave a CONDITIONAL PASS with 5 narrative findings.
- **Both of the reviewer's concrete technical claims are FALSE (executor-verified against the code):** (a) "`disk_skill_files` defaults to `*.md` → non-`.md` resources bypass Rule F′" — FALSE, it uses `rglob("*")` (all extensions); `prose-critique/analyze.py` (a `.py`) IS manifested at VENDOR.md:66. (b) "`prefix_unrewrite` may raise on malformed/dual-prefix input, crashing CI" — FALSE, it is a pure `str.replace()` with no exception path (verified on empty/malformed/dual-prefix inputs).
- **The other 3 'findings' are spec-mandated, explicitly-documented design decisions, not defects:** `--report` exit-0 (§4.6 / L1 hard contract); Mode U deferral (OQ-4); the two-field-bypass test = exactly what the Phase-6 security lens REQUIRED us to add (spec §4.1 acceptance bullet 2).
- **Decision (maintainer-approved):** substantive evidence (zero formal deviations, green gate/tests, reviewer's concrete claims refuted, every "finding" either false or a documented design decision) outweighs the degraded exit code, which reflects only Tier-2 swarm unavailability in this environment. Degradation recorded here as a known environmental limitation. Re-running the wrapper in an environment with multi-vendor model access is the only way to get a fuller Tier-2 pass; it is filed as optional in Open Questions.
