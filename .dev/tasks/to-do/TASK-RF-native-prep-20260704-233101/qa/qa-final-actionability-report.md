# QA Report — FINAL Actionability / Operator-Clarity Lens (Phase 6)

**Topic:** Operator actionability of `/laf:prep`, `/laf:rewrite`, and the `ADDING_NEW_WORKS.md` automated-alternative pointer paragraph.
**Date:** 2026-07-05
**Phase:** doc-qualitative (actionability lens, FINAL consolidated gate)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY)

---

## Overall Verdict: FAIL

The four built artifacts (`prep.md`, `rewrite.md`, `prep-cordinator.md`, `prep/SKILL.md`) are mutually
consistent and internally cross-reference the path contract correctly. The pointer paragraph in
`ADDING_NEW_WORKS.md` accurately reflects what the built commands do at the headline level
(slug-based onboarding, dual-form promotion, `/laf:rewrite --work <slug>` follow-on, native phase as the
automated alternative). Those properties PASS.

But "operator actionability" is a stricter bar than "internal consistency," and at that bar the set
FAILS. An operator reading only these surfaces cannot complete a single end-to-end run without guessing
at five separate decision points. Each is documented below with the specific gap and the concrete fix.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `/laf:prep` argument surface is unambiguous | FAIL | `.claude/commands/laf/prep.md:3` declares `argument-hint: "<novel title>" [--source <path-or-url>]` but line 9 says "if present, `--source <path>`" — the body silently narrows the advertised URL form to a path-only form. An operator who copies the argument hint and passes a URL cannot tell from the command file whether the URL is honored. |
| 2 | Slug derivation is specified enough for the operator to predict it | FAIL | `path-contract.md:15` says `<work-slug>` is "the lowercase slug derived from the title (e.g. `tolkien`)". `prep-cordinator.md:36` says "lowercase; the `work/prep/<work-slug>/` key". Neither states the actual algorithm (whitespace→hyphen? punctuation stripping? title-case collapse? disambiguation on collision?). The operator must then use the *derived* slug verbatim as `--work <slug>` for `/laf:rewrite`, but cannot predict what to type until the run completes. |
| 3 | `/laf:rewrite` greenlight gate has a defined operator action | PASS (with caveat) | `rewrite.md:20-21` and `path-contract.md:65` both state the CONFIRMED/PENDING guard and "surface that and stop." Caveat (not a fail): the command does not tell the operator *how* to flip PENDING→CONFIRMED — that action lives in `prep/SKILL.md §6` ("Emit a confirmation request; HALT until confirmed"). Acceptable for a delegated command but the operator of `/laf:rewrite` reading only `rewrite.md` sees a gate with no remediation path. |
| 4 | `/laf:rewrite` scope beyond chapter 1 is stated | FAIL | `rewrite.md:15` says "hand control to the `muse` agent for chapter 1 of the existing per-chapter 11-step workflow." Nothing in `rewrite.md`, `prep/SKILL.md`, or `path-contract.md` states what happens for chapters 2..N — does the operator re-invoke `/laf:rewrite` per chapter? Does `muse` loop? The command's name ("Begin the chapter rewrite phase") implies a phase; the body implements exactly chapter 1. An operator cannot tell from the command how to drive a multi-chapter rewrite. |
| 5 | Pointer paragraph accurately describes the built `/laf:prep` invocation | PASS | `ADDING_NEW_WORKS.md:14` quotes `/laf:prep "<novel title>" --source <path-or-url>` which matches `prep.md:3` verbatim. Slug-based onboarding, dual-form promotion (0.1 6-key keeps `meaning:` / root 5-key strips it), and `/laf:rewrite --work <slug>` follow-on all match `prep/SKILL.md §6` and `path-contract.md §3-§4`. |
| 6 | Pointer presents native phase as automated alternative without contradicting manual flow | PASS | `ADDING_NEW_WORKS.md:13` "The steps below are the **manual** work-mapping flow" + line 21 "the manual flow below remains useful for understanding, patching, or hand-curating" frames native as alternative, not replacement. Manual step 6 validates against the same 5-key schema the root promotion target uses; no contradiction. |
| 7 | Pointer paragraph is sufficient for an operator to know what to do next | FAIL | The pointer tells the operator to *run* `/laf:prep` and that the package lands at `work/prep/<slug>/`, but it does not tell the operator (a) that the run will HALT twice awaiting their input (question gate + greenlight), (b) that a `--source` value will be demanded as a required input if omitted, or (c) that the operator must perform the greenlight confirm to flip `50-greenlight.md` to `status: CONFIRMED` before `/laf:rewrite` will proceed. An operator who runs `/laf:prep "My Book"` and waits will hit two unexpected HALTs and an unexpected gate failure on the follow-on `/laf:rewrite`. |
| 8 | `/laf:prep` entry behavior is fully specified | PASS | `prep.md:8-16` delegates cleanly to `prep-cordinator`, states the source path is required, and routes to the path contract for layout. The HALT gates and abort-on-NO-ACCESS are restated in `prep-cordinator.md` Stage 1/5/7. |
| 9 | `/laf:rewrite` entry behavior is fully specified | PASS | `rewrite.md:8-13` hardcodes the 3-file read-set by reference to `path-contract.md §4`, confirmed identical in `path-contract.md:60-62`. No ambiguity about what `muse` consumes. |
| 10 | Pointer-paragraph link target resolves | PASS | `ADDING_NEW_WORKS.md:24` relative link `../../laf-adaptation/skills/prep/resources/path-contract.md` resolves to existing file (verified on disk). The two manual-flow example links (`tolkien_mapping.yaml`, `narnia_mapping.yaml`) also resolve. |
| 11 | Cross-command consistency (`<path>` vs `<path-or-url>`) | FAIL | Same root defect as check #1, scored separately because it is also a cross-artifact contradiction between `prep.md` line 3 (`<path-or-url>`) and `prep.md` line 9 (`--source <path>`), and between `prep.md` line 3 (`<path-or-url>`) and `prep-cordinator.md:35` (`--source <path>`). Per Critical Rule #6, contradictions are always IMPORTANT or CRITICAL — never minor. |
| 12 | `/laf:rewrite` argument-hint matches body | PASS | `rewrite.md:3` `argument-hint: --work <work-slug>` matches body line 8 `--work <slug>`. Acceptable: `<work-slug>` and `<slug>` are obviously the same token; this is not the same class of defect as check #1 (where one form admits URLs and the other does not). |

## Summary
- Checks passed: 7 / 12
- Checks failed: 5 (#1, #2, #4, #7, #11)
- Critical issues: 0
- Important issues: 5
- Minor issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY)
- Axis lens status: doc-qualitative phase — Axis column omitted (task-qualitative-only).

## Confidence
- Verified: 12 / 12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 6 | Grep: 3 | Bash: 3 | Glob: 0
- Every checklist row has a file:line citation. No UNCHECKED items.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `.claude/commands/laf/prep.md:3` vs `:9` | argument-hint advertises `<path-or-url>` but body line 9 narrows to `--source <path>`. Operator cannot tell whether URLs are honored. | Pick one form and apply it in both the argument-hint and the body. If URLs are supported (the hint implies they are), state so in the body. If not, change the hint to `<path>`. The chosen form must also match `prep-cordinator.md:35`. |
| 2 | IMPORTANT | `laf-adaptation/skills/prep/resources/path-contract.md:15`; `laf-adaptation/agents/prep-cordinator.md:36` | Slug-derivation algorithm is unstated. Operator cannot predict the `--work <slug>` value they will need for `/laf:rewrite` until the run completes, and cannot pre-create the directory. | Add a one-line algorithm to `path-contract.md §1`, e.g. "`<work-slug>` = lowercase of the title with whitespace collapsed to a single hyphen and all non-`[a-z0-9-]` stripped; on collision with an existing `work/prep/<slug>/`, append `-2`, `-3`, …". Have `prep-cordinator.md:36` reference it. |
| 3 | IMPORTANT | `.claude/commands/laf/rewrite.md:15` | Command body covers chapter 1 only; nothing states how the operator drives chapters 2..N. Command name ("Begin the chapter rewrite phase") implies phase-level scope. | Add one line to `rewrite.md`: "For chapters 2..N, re-invoke `/laf:rewrite --work <slug>` (or state that `muse` loops — pick the truth)." |
| 4 | IMPORTANT | `docs/guides/ADDING_NEW_WORKS.md:13-24` | Pointer paragraph does not warn the operator about the two HALTs (question gate, greenlight) or the required-input elicitation when `--source` is omitted. Operator will hit unexpected interrupts and an unexpected gate failure on the `/laf:rewrite` follow-on. | Add one sentence to the pointer: "Expect two HALTs (a coverage-constrained question gate and a greenlight confirm) and note that `/laf:rewrite` will refuse a `PENDING` package — confirm greenlight first." |
| 5 | IMPORTANT | `.claude/commands/laf/prep.md:3` ↔ `:9` ↔ `laf-adaptation/agents/prep-cordinator.md:35` | Three-way `<path-or-url>` vs `<path>` inconsistency (cross-artifact contradiction, same root as #1; flagged separately per Critical Rule #6 because contradictions are always ≥ IMPORTANT). | Resolve to a single form across all three locations as in #1. Resolving #1 will resolve #5 if the same edit touches all three sites. |

## Actions Taken
None. REPORT-ONLY (`fix_authorization: false`). No files modified.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on prior structural-QA PASS for cross-reference integrity of path-contract §-citations.
- Relied on prior structural-QA PASS for existence of all six files in the read set.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Argument-hint vs body consistency in `prep.md` — verified by Read of `.claude/commands/laf/prep.md:3,9` and Grep across all three sites; surfaced the `<path-or-url>` ↔ `<path>` contradiction the structural pass does not test.
- Slug-derivation algorithm presence — verified by Grep for "slug" across all four artifacts; confirmed only the "lowercase from title (e.g. tolkien)" example exists, with no algorithm statement anywhere.
- Multi-chapter rewrite scope — verified by Grep for "chapter" / "muse" / "11-step" across `rewrite.md`, `prep/SKILL.md`, `path-contract.md`; confirmed chapter-2+ handling is undocumented.
- Pointer-paragraph accuracy and link resolution — verified by Read of `ADDING_NEW_WORKS.md:13-24` and Bash `ls` of the cited link targets.

## Recommendations

Resolve all 5 IMPORTANT findings before the FINAL gate can PASS. The set is small and the fixes are
single-line edits in 4 files (`prep.md`, `prep-cordinator.md`, `path-contract.md`, `rewrite.md`,
`ADDING_NEW_WORKS.md`):

1. Pick one `--source` form and apply it consistently across `prep.md` line 3 + line 9 and
   `prep-cordinator.md:35`. (Resolves findings #1 and #5 together.)
2. Add the slug-derivation algorithm to `path-contract.md §1` and reference it from
   `prep-cordinator.md:36`. (Resolves #2.)
3. State the chapter-2..N driver in `rewrite.md`. (Resolves #3.)
4. Add the two-HALT / greenlight-confirm warning to the `ADDING_NEW_WORKS.md` pointer. (Resolves #4.)

After these edits, re-run this actionability lens. None of the four fixes are scope-creative — each
restates information already present elsewhere in the prep subsystem (the HALTs are in `prep/SKILL.md`,
the greenlight gate is in `path-contract.md §4`, the slug is the package key) but currently invisible to
an operator who reads only the command file or the pointer paragraph.

## QA Complete
