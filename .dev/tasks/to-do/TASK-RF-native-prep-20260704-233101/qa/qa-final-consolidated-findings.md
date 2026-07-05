# Final Consolidated Findings (Phase 6 — final gate)

**Overall consolidated verdict: FAIL** (issues reported by the internal-consistency, actionability, and domain-accuracy lenses).

Source reports (under `.dev/tasks/to-do/TASK-RF-native-prep-20260704-233101/qa/`):
- `qa-final-template-conformance-report.md` — PASS, 0 defects (25/25).
- `qa-final-internal-consistency-report.md` — **FAIL**, 4 CRITICAL + 1 IMPORTANT + 2 MINOR.
- `qa-final-evidence-boundary-report.md` — PASS (boundary green, NATIVE=8, all outputs source-traced); 5 doc-level non-blocking notes (D1–D5).
- `qa-final-actionability-report.md` — **FAIL**, 5 IMPORTANT.
- `qa-final-domain-accuracy-report.md` — **FAIL**, 1 CRITICAL + 3 IMPORTANT.
- `qa-final-crossref-chain-report.md` — PASS (all 4 chains intact); 3 MINOR non-blocking observations.

## Deduplicated findings (classification + resolution)

### FF1 — source-fidelity output schema omits meaning/compound_scene; analyst wording incorrectly calls source-fidelity "ADOPTED-CLEAN" — CRITICAL (internal-consistency #2/#5, domain-accuracy #1)
- **Classification: GENUINE defect — and the P1 MF1 fix rationale was factually wrong.** VERIFIED: `laf-adaptation/VENDOR.md:115` classifies `skills/source-fidelity/**` as **NATIVE** (not ADOPTED-CLEAN); `laf-adaptation/CLAUDE.md` §1/§4 confirm source-fidelity is NATIVE and freely editable. The P1 MF1 fix wording claimed source-fidelity is "ADOPTED-CLEAN" and "cannot be extended per constraint #6" — that is incorrect. Because source-fidelity IS NATIVE and freely editable, the clean fix (the one the P1 meaning-flow agent strongly preferred as "option (a)") is to extend source-fidelity's output schema to include the `meaning`/`compound_scene`/`compound_scenes` fields — making it the genuine single source of truth. This also resolves domain-accuracy #1's concern that the analyst emits `meaning:` with no in-skill definition home: source-fidelity (which the analyst DOES load) will define the field.
- **Resolution:** (a) Extend `laf-adaptation/skills/source-fidelity/SKILL.md` Output schema (between `transformation_flags` and `uncertainties`) to include `meaning:`, `compound_scene:`, `compound_scenes:` with the same shapes the analyst emits (grounded in `/thematic-fidelity` as the concept source). (b) Correct `analyst.md` Output contract wording: source-fidelity IS the single source of truth (now including these fields); remove the incorrect "ADOPTED-CLEAN cannot be extended" rationale.

### FF2 — Stage-7/§6/path-contract §5 "promote via /kb-management" headline contradicts the operator-clarity note — IMPORTANT (evidence-boundary D3, domain-accuracy #2)
- **Classification: GENUINE readability contradiction (residual from the P0 F2/F4 fix — the operator-clarity note was added but the original misleading headline was left).** The headline says kb-management promotes/writes; the note says it does NOT perform the transform. Reader-skim hazard.
- **Resolution:** Tighten the headlines in `prep-cordinator.md` Stage 7, `prep/SKILL.md` §6, and `path-contract.md` §3/§5 so they are consistent with the operator-clarity note: the COORDINATOR performs the dual-form transform (path-contract §3 is the rule); `/kb-management` provides the kb-lifecycle write. Remove/soften the misleading "promote via /kb-management" / "kb-management writes the targets" phrasing in the headlines (the operator-clarity note already states the correct mechanism).

### FF3 — `<path-or-url>` vs `<path>` perceived contradiction — IMPORTANT (actionability #1/#5)
- **Classification: NOT a defect in the frontmatter — design-verbatim.** `prep-agent-schemas.md` §5.1 specifies `argument-hint: "<novel title>" [--source <path-or-url>]` verbatim. The frontmatter MUST stay verbatim per the design pack. The body's `source_path` is the resolved local path. Minor body clarity can be added.
- **Resolution:** Leave the `argument-hint` verbatim (design authority). Add a one-line clarification in `prep.md` body that `--source` accepts a local path (a URL, if given, is fetched to a local file first). No frontmatter change.

### FF4 — slug algorithm unstated — IMPORTANT (actionability #2)
- **Classification: GENUINE small doc gap.** `path-contract.md` §1 only says "lowercase from title (e.g. tolkien)". An operator can't predict the `--work <slug>` token.
- **Resolution:** Add a one-line slug rule to `path-contract.md` §1 (lowercase; spaces/punctuation → hyphens; drop leading articles; e.g. "The Lord of the Rings" → "tolkien" is a work-name slug, conventionally the recognizable short name lowercased).

### FF5 — multi-chapter scope undocumented in /laf:rewrite — IMPORTANT (actionability #3)
- **Classification: GENUINE small doc gap.** `rewrite.md` says "chapter 1 of the per-chapter workflow" but doesn't state how chapters 2..N proceed.
- **Resolution:** Add a one-line note to `rewrite.md` that the command begins chapter 1 and the existing per-chapter workflow continues for subsequent chapters (each chapter re-reads the same prep package).

### FF6 — ADDING_NEW_WORKS.md pointer omits the HALTs / greenlight gate — IMPORTANT (actionability #4)
- **Classification: GENUINE small doc gap.** The pointer doesn't warn about the question-gate HALT, the greenlight confirm HALT, or that `/laf:rewrite` refuses a PENDING package.
- **Resolution:** Add a brief note to the pointer paragraph about the two HALTs (question gate, greenlight) and that `/laf:rewrite` requires a CONFIRMED greenlight.

### FF7 — tier-coordinator Check D `<work>-mapping.yaml` path ambiguity — IMPORTANT (domain-accuracy #4, crossref-chain O-3)
- **Classification: GENUINE minor wording clarity.** "Read the top-level `meaning:` from `<work>-mapping.yaml`" could be read as the underscore (root, meaning-stripped) copy. The meaning only lives in the 6-key kb hyphen copy.
- **Resolution:** Tighten the Check D wording in `tier-coordinator.md` to specify the 6-key kb copy (`kb/adaptation-mapping/<slug>-mapping.yaml`) carries the work-level `meaning:`.

## NOT defects (design-faithful — re-raised but correctly NOT changed)

- **tier-coordinator in prep-cordinator `tools:`** (internal-consistency #3, domain-accuracy #3): VERBATIM from `prep-agent-schemas.md` §1 frontmatter. Removing it would deviate from the design pack. (Already classified design-faithful at P0.)
- **analyst/tier-coordinator not loading `thematic-fidelity`** (internal-consistency #1/#4/#6, domain-accuracy #1): design-faithful — `prep-agent-schemas.md` §4.2 mandates "no new skill line"; meaning is read as data; the `(R10; /thematic-fidelity)` citations are build-time provenance per CLAUDE.md §1. With FF1, the `meaning:` field is now defined in source-fidelity (which both agents load), fully resolving the "no in-skill definition home" concern WITHOUT adding a skill line. The crossref-chain lens independently confirmed Check D's chain is intact.
- **`prep-cordinator` spelling** (internal-consistency #7): INTENTIONAL per `prep-agent-schemas.md` §1 ("Name spelling `prep-cordinator` is intentional"). NOT a defect.
- **`<path-or-url>` argument-hint** (FF3): design-verbatim per §5.1; only the body gets a clarification.
- **evidence-boundary D1** (`compound_scene_eligible` vs `compound_scene` terminology): carried faithfully from the design pack's own internal inconsistency; not introduced by this build.
- **evidence-boundary D2/D5, crossref-chain O-1/O-2**: documentation-level observations outside this build's scope (VENDOR.md comment wording, upstream muse skill references, etc.).

## Fix scope for the serialized fix agent (I20 — single agent)

Apply FF1–FF7 to the NATIVE/command/docs outputs:
- FF1: `laf-adaptation/skills/source-fidelity/SKILL.md` (extend Output schema) + `laf-adaptation/agents/analyst.md` (correct Output contract wording).
- FF2: `laf-adaptation/agents/prep-cordinator.md` Stage 7, `laf-adaptation/skills/prep/SKILL.md` §6, `laf-adaptation/skills/prep/resources/path-contract.md` §3/§5 (headline/wording coherence with the operator-clarity note).
- FF3: `.claude/commands/laf/prep.md` body one-line clarification (NO frontmatter change).
- FF4: `laf-adaptation/skills/prep/resources/path-contract.md` §1 slug rule.
- FF5: `.claude/commands/laf/rewrite.md` multi-chapter note.
- FF6: `docs/guides/ADDING_NEW_WORKS.md` pointer HALT/greenlight note.
- FF7: `laf-adaptation/agents/tier-coordinator.md` Check D `<work>-mapping.yaml` wording.

MUST NOT: change any frontmatter dialect, add/remove skill lines (design §4.2 mandates no new skill line for tier-coordinator; analyst skills list unchanged), edit adopted files, change VENDOR rows, alter the `prep-cordinator` spelling, or change the `argument-hint` (design-verbatim). After the edit, re-run `uv run python laf-adaptation/scripts/check_boundary.py` (final line begins `BOUNDARY CONTRACT: PASS`) and `git diff --stat` on writer.md/muse.md (empty).
