# QA Report — Content Qualitative Review (operational-correctness lens)

**Topic:** LAF prep Stage-0 chapter-materialize — M3 content final gate
**Date:** 2026-07-09
**Phase:** doc-qualitative (final-gate, operational-correctness lens)
**Fix cycle:** N/A
**fix_authorization:** false (report-only; no source file modified)

---

## Overall Verdict: FAIL

The assembled Stage-0 materialization procedure is internally *documented* as safe, but read as an
operator would **execute** it, the mode-detect precedence guesses on exactly the input it names as its
motivating ambiguity case, the `--source-mode` override is severed mid-pipeline, the pipeline is
ordered so the `--source`-omitted path is unrunnable, and the incompleteness gate that should catch a
partial split is unreachable in the very mode it guards. Six operational-correctness defects, two
CRITICAL.

---

## Items Reviewed

| # | Check (operator lens) | Result | Evidence |
|---|-----------------------|--------|----------|
| 1 | Mode-detect precedence is unambiguous AND ambiguity branch HALTs rather than guesses | **FAIL** | SKILL.md:43-59 "pick the first that holds"; rule 2 `folder` has no negative guard; real `Books/LWW/` (verified: 4 split `-1..-4.html` + 5 byte-identical monoliths sha `8d2cf…` + PDF) makes rule 2 hold → returns `folder` before rule 4 ambiguity is reached. Command prep.md:27 promises HALT; skill guarantees no-HALT for the named case. |
| 2 | Deferred-write invariant prevents committing a non-CERTAIN `ch-NN.txt` before greenlight | **PASS (scoped)** | SKILL.md:91-102 invariant holds *at boundary-confidence granularity* — non-CERTAIN boundaries deferred to §5. But see item 6: scoped to boundary confidence, does not cover work-completeness. |
| 3 | Stage 0.5 routes deferred items into EXISTING §5 gate, no new HALT machinery; greenlight blocked while unresolved | **PASS** | SKILL.md:104-109 + prep-cordinator.md:99-103,112-116 + prep/SKILL.md:21-26: `ambiguous_splits` fold into §5; "no new gate"; STAGE 7 checklist blocks CONFIRMED. Consistent across all three files. |
| 4 | `chapter-materialize` dispatch is inline in coordinator context; analyst NOT repurposed as splitter | **PASS** | SKILL.md:18-22 (analyst "not repurposed"; inline procedure); prep-cordinator.md:73-74 ("executed in this coordinator's own context, not a forked agent"); STAGE 3 (prep-cordinator.md:92-95) dispatches analyst separately with "do NOT fork a new analyzer." |
| 5 | `--source-mode` flag + broadened `--source` semantics operable end-to-end | **FAIL** | Flag declared in command (prep.md:3,26) and honored in SKILL (SKILL.md:58), but prep-cordinator (the delegate that dispatches the skill) has NO ingestion: Inputs table (prep-cordinator.md:34-38) lists only title/source_path/work_slug; no `source_mode` row, no forwarding in STAGE 0. Flag severed mid-pipeline. URL `--source` (prep.md:18) has no stage performing the fetch-to-local step. |
| 6 | (derived) Incompleteness / count-reconciliation gate protects a partial folder split | **FAIL** | SKILL.md "Split set incomplete" (line 161) block lives only in the failure table, unwired to Stage 0.3→0.4 flow or the confidence rule. boundary-rules.yaml:70-73 `all_present_counts_must_agree` is satisfied by 4==4 (body_heading==filename) in a Mode-A scan with no TOC/monolith in the candidate set; the true count 17 (verified in base monolith) never surfaces. 4 CERTAIN chapters commit immediately (SKILL.md:97). |
| 7 | STAGE 0 / STAGE 1 ordering is executable (source_path resolved before Stage-0 mode-detect) | **FAIL** | prep-cordinator.md:49-54: STAGE 0 runs source-access + mode-detect FIRST, but `source_path` elicitation (when `--source` omitted) is STAGE 1(a), ordered after STAGE 0. Data dependency runs backward; Stage-0 note (79-81) reconciles the *two source-fidelity declarations* but not the elicitation ordering. |
| 8 | Mode C adopt vs manifest schema `.raw/`/`raw_path` consistency | **FAIL (IMPORTANT)** | SKILL.md:131-134 adopt "write/refresh ONLY chapter-manifest.yaml," existing `.txt` untouched, no raw source exists; schema (SKILL.md:183-187, 200-202) makes `raw_sources[].path` "retained at .raw/" and per-chapter `provenance.raw_path: .raw/...html` structurally present; path-contract §5 lists `.raw/*` as a Stage-0 write. Undefined what `raw_path` holds for an ADOPTED chapter (verified narnia adopt set: ch-01..04, no HTML/.raw present). |

## Summary
- Checks passed: 3 / 8
- Checks failed: 5
- Critical issues: 2 (findings F1, F2)
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 6

Every check was verified against actual source files (SKILL.md, prep-cordinator.md, prep.md,
path-contract.md, prep/SKILL.md, boundary-rules.yaml) and the real filesystem state (`Books/LWW/`
directory listing, sha256 byte-identity of the 5 monoliths, chapter-heading counts in split files vs
base monolith, `source/narnia|tolkien` adopt sets). Tool-call count (11) exceeds checklist item count
(8): each Bash call performed multiple concrete verifications (dir listing, sha256, heading grep,
glob-match test, precedence re-read, flag trace).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | CRITICAL | SKILL.md:43-59 (Stage 0.2 precedence) | Precedence says "evaluate top-to-bottom and pick the first that holds." Rule 2 (`folder`) matches any "directory of ≥2 non-canonical per-chapter files" with NO negative guard for a co-present dominating monolith. For the canonical `Books/LWW/` case (4 split `-1..-4.html` + monolith, both verified present), rule 2 fires and returns `folder` BEFORE rule 4 (ambiguity → HALT) is ever evaluated. The skill guesses `folder` on the exact input it names as its ambiguity exemplar, silently materializing 4 of 17 chapters. Command prep.md:27 promises "on ambiguity `auto` raises a mode question rather than guessing" — the skill contradicts that promise. | Add a negative guard to rule 2: `folder` fires only when NO dominating monolith / competing candidate set is co-present; otherwise fall through to rule 4. OR restructure so the ambiguity test (rule 4) is evaluated BEFORE `folder`/`file` when >1 candidate set exists. The "first that holds" ordering must not let `folder` pre-empt the ambiguity HALT. |
| F2 | CRITICAL | prep-cordinator.md:34-38, 49-54 (Inputs + STAGE 0) | `--source-mode` operator override is declared in the command (prep.md:3,26) and honored inside the SKILL (SKILL.md:58), but the prep-cordinator — the agent `/laf:prep` delegates the ENTIRE run to and that dispatches chapter-materialize inline — never ingests or forwards it. Inputs table has no `source_mode` row; STAGE 0 never mentions receiving the override. The flag is operable at both ends and severed in the middle: an operator's `--source-mode folder` cannot reach the detection logic. The "operable end-to-end" claim is false. | Add a `source_mode` (from `--source-mode`, default `auto`) row to the prep-cordinator Inputs table and forward it into the STAGE 0 inline chapter-materialize dispatch so SKILL.md:58's "operator override is honored here" has a value to honor. |
| F3 | CRITICAL | prep-cordinator.md:49-54 (STAGE 0 vs STAGE 1 ordering) | STAGE 0 (mode-detect + source-access declaration) runs FIRST and requires a resolved `source_path`, but `source_path` elicitation for the `--source`-omitted path is STAGE 1(a), ordered AFTER STAGE 0. The pipeline is unrunnable when `--source` is omitted: Stage 0 executes against an unresolved path before Stage 1a elicits it. The Stage-0 note (79-81) explicitly reconciles the two *source-fidelity declarations* but says nothing about the elicitation ordering. | Add a Stage-0 precondition: if `--source` is omitted, elicit the required `source_path` BEFORE STAGE 0 mode-detect (move the elicitation ahead of STAGE 0, or add an explicit "Stage 0 preconditions: source_path resolved (elicit first if --source omitted)" note). Downgradable to IMPORTANT if the team asserts elicitation always precedes STAGE 0 by convention — but as written the numbered order contradicts that. |
| F4 | IMPORTANT | SKILL.md:80-89 (confidence rule) + 91-102 (Stage 0.4) + 161 (failure table) + boundary-rules.yaml:70-73 | The "Split set incomplete" block ("block Mode A unless operator confirms partial scope") exists only as a failure-table row, unwired to the Stage 0.3→0.4 flow or the load-bearing confidence rule. In a Mode-A folder scan of a partial split (verified: `Books/LWW/-1..-4.html` = 4 files, each with clean isolated `CHAPTER I..IV` headings), body-heading count (4) and filename count (4) agree → each boundary earns 2 agreeing signals → CERTAIN → Stage 0.4 materializes immediately. The true count (17) lives in the monolith TOC, which is not in the Mode-A candidate set, so `all_present_counts_must_agree` is trivially satisfied and never raises `ambiguous_split`. The deferred-write invariant does NOT protect this case because the chapters are genuinely boundary-CERTAIN; the hazard is a work-completeness property the invariant never checks. | Wire count-reconciliation as a hard precondition on Stage 0.4 commit: before committing any Mode-A CERTAIN chapter, require the folder's expected total (from any available TOC/monolith heading count, or an explicit operator `partial-scope` confirmation) to match the materialized count; otherwise raise `ambiguous_split` and defer. Make "Split set incomplete" a blocking gate step, not a table note. |
| F5 | IMPORTANT | SKILL.md:131-134 (Mode C adopt) vs 183-187, 200-202 (manifest schema) + path-contract.md §5 | Mode C adopt reads existing `ch-*.txt` untouched and writes ONLY the manifest — there is no raw HTML/PDF source, so no `.raw/` content and no per-chapter `raw_path`. But the v1 manifest schema makes `raw_sources[].path` ("retained at source/<slug>/.raw/") and per-chapter `provenance.raw_path: .raw/...html` structurally present, and path-contract §5 lists `source/<slug>/.raw/*` as a Stage-0 write. For an ADOPTED chapter (verified: `source/narnia/ch-01..04` with no `.raw/`) the schema fields have no defined value. An operator cannot tell what `raw_path` / `raw_sources` should contain for an adopt run. | State explicitly in the adopt section and the schema that under `provenance.class: ADOPTED`, `raw_path` is null/omitted and `.raw/` is not written (adopt is a zero-raw path); make `raw_sources`/`raw_path` conditional on `class: MATERIALIZED`. Reconcile path-contract §5's unconditional `.raw/*` Stage-0-write row with the adopt zero-write reality. |
| F6 | IMPORTANT | prep.md:18-20 (URL semantics) vs prep-cordinator.md STAGE 0/1, SKILL.md:28 | The command states "A URL, if supplied, is fetched to a local file first; the `source_path` the coordinator then runs `/source-fidelity` against is the resolved local path" — but no stage in the coordinator or skill performs that fetch-to-local step. STAGE 0.1 (SKILL.md:28) assumes `--source` resolves to local paths ("list every raw input the --source argument resolves to"). The coordinator has `WebFetch` but no stage invokes it for URL materialization. The broadened `--source` semantics are not operable for the URL case. | Add an explicit pre-STAGE-0 step (in the coordinator) that, when `--source` is a URL, fetches it to a local file and rebinds `source_path` to the local path before mode-detect. Or, if URL support is out of scope for this milestone, remove the URL claim from prep.md:18-20 so the command does not promise an unimplemented path. |

## Actions Taken
None — `fix_authorization: false`. All findings are report-only. No source file was modified.

## Recommendations
- Resolve F1 and F2 before this gate can pass — they are the load-bearing failures: F1 makes the skill
  guess (not HALT) on its own motivating example, silently truncating a 17-chapter book to 4; F2 makes
  the advertised operator escape hatch (`--source-mode`) inert, so the operator cannot even override the
  wrong guess from F1. The two compound: an operator hitting `Books/LWW/` gets a silent wrong result AND
  no working override.
- F3 blocks the `--source`-omitted operator path entirely; fix the stage ordering.
- F4 is the correctness backstop for F1 — even if precedence were fixed, any genuine partial-folder
  input needs the incompleteness gate wired into the commit precondition, not left as a table note.
- F5 and F6 are contract/consistency gaps that will confuse an operator mid-run; resolve or scope-cut.
- No web research was required for this review (all verification was local-file / filesystem bound);
  therefore no Tavily-vs-fallback tool-engagement line applies.

## Self-Audit (mandatory)
1. **How many factual claims verified against source?** All 8 checklist items were verified against
   actual source files and live filesystem state — 0 relied-upon, 0 assumed. Specific verifications:
   precedence wording (SKILL.md:43-59), flag declaration/honoring/ingestion trace across 3 files, stage
   ordering (prep-cordinator.md:49-54), byte-identity of 5 monoliths via sha256, chapter-heading counts
   (4 in splits vs 17 in monolith) via grep, adopt-set existence (narnia ch-01..04, tolkien ch-01),
   dedup tie-break tested against real filenames, `* copy*.html` glob-match tested.
2. **What specific files were read?** `SKILL.md` (chapter-materialize), `prep-cordinator.md`,
   `.claude/commands/laf/prep.md`, `prep/SKILL.md`, `prep/resources/path-contract.md`,
   `chapter-materialize/resources/boundary-rules.yaml`; plus filesystem: `Books/LWW/` listing + hashes +
   heading counts, `laf-adaptation/source/` tree.
3. **Why should the user trust the checking was thorough?** This review did NOT find 0 issues — it found
   6, two CRITICAL, each with a file:line citation and, for the CRITICAL ones, a reproduction traced
   against the real `Books/LWW/` input the skill itself names. The precedence defect was proven by
   walking the "first that holds" rule against a verified directory listing; the flag defect by tracing
   the flag through all three files and finding the middle link absent; the truncation hazard by
   confirming 4 split files (CHAPTER I–IV) vs 17 monolith headings on disk.
4. **Web research / Tavily?** No web research was performed; all checks were local. No fallback occurred.

## QA Complete
