# Phase 2 QA — Consolidated Findings (Serialized Fix input)

Gate: 5 PASS (template-conformance, internal-consistency, evidence+completeness, domain-accuracy) + 1 FAIL (actionability).
All findings are IN-SCOPE (both files were authored this phase). Fix ALL in-place. Do NOT change verbatim-frozen content (the 16-row failure table, the `chapter-manifest.yaml` v1 schema block, the confidence-rule/deferred-write bolded sentences) — those passed byte-identical and must stay byte-identical.

Files:
- A = `laf-adaptation/skills/chapter-materialize/SKILL.md`
- B = `laf-adaptation/skills/chapter-materialize/resources/boundary-rules.yaml`

## IMPORTANT (executability — actionability lens)

**I-1 (F1): Mode-C "exists and validates" is undefined.** In A's Stage 0.2, "adopt" fires when a `source/<slug>/ch-*.txt` set "exists and validates" — but "validates" has no testable meaning. FIX: add a one-line testable definition, e.g. "validates = every file matches the canonical `ch-<NN>.txt` name (zero-padded, contiguous ordinals from 01, no gaps), each is non-empty, and `order == numeric id`." Adopt only when validation passes; otherwise fall through to folder/ambiguity.

**I-2 (F2): "non-canonical per-chapter files" predicate not surfaced.** In A's Stage 0.2 Mode A trigger ("≥2 non-canonical per-chapter files"), define "non-canonical" in the body: "non-canonical = a per-chapter file whose name does NOT already match the canonical `source/<slug>/ch-<NN>.txt` form (i.e. it needs materialization, not adoption)." (This distinguishes Mode A input from an already-adopted Mode C set.)

**I-3 (F3): CERTAIN rule's "AND no contradiction" clause not operationalized.** Keep the bolded sentence VERBATIM, but add an adjacent (non-bolded) operationalization line in the same §: "A *contradiction* = two independent signals disagree on the same fact — different boundary offsets for the same chapter, different chapter counts (TOC vs body-heading vs filename), or different titles/ordinals. Any contradiction caps the affected boundary at UNCERTAIN regardless of signal count." Do NOT alter the bolded sentence itself.

**I-4 (F5): PDF extraction names no mechanism under the no-runtime (ADR-006) invariant.** A's normalization section says "PDF → extract the text stream" but no script/runtime may exist, and `Books/LWW/` contains a real `.pdf`. FIX: state the mechanism explicitly — "PDF text is obtained by the model reading the PDF directly (the executing model's native PDF-read capability); NO extraction script is added (ADR-006). PDF sources are inherently lower-fidelity: extraction garble (broken words, ligatures, repeated page headers) caps the affected boundaries at UNCERTAIN and blocks greenlight until a human accepts the result or supplies a cleaner source (per the PDF failure-mode row)."

## MINOR

**M-1 (F4, also flagged by internal-consistency + domain lenses): dangling `§B6` anchor.** B (`boundary-rules.yaml`) confidence_rule comment points the authoritative copy at "SKILL.md §B6", which does not exist. FIX: change the reference to the real heading — "the authoritative copy lives in SKILL.md `### Confidence rule (load-bearing)`".

**M-2 (F6): hash-identical monolith tie-break not deterministic.** A's Stage 0.1 / §10 "pick one canonical" among hash-identical duplicate monoliths lacks a deterministic rule. FIX: add "when duplicates are byte-identical (same sha256), pick the canonical by the shortest filename, tie-broken by lexicographic order (so the un-suffixed base name wins over `... copy N`); the rest are `role: ignored_duplicate`." (Matches the `ignore_globs` intent.)

**M-3 (F7): Stage 0.1 role assignment ordered before 0.3 evidence.** FIX: add a half-sentence that `raw_sources[].role` in 0.1 is a PROVISIONAL classification finalized after the 0.3 evidence pass (front_matter vs chapter_file can flip once headings are mapped).

**M-4 (domain O2): base monolith without a `copy` token escapes `ignore_globs`.** In B, `ignore_globs` catches `*copy*` duplicates but not a same-content base monolith named without "copy" (e.g. `...Lewis.html`). FIX: add a comment on `ignore_globs` clarifying it is a HINT only and that byte-identical duplicates are resolved by the sha256 tie-break (M-2), NOT by glob alone — so the base monolith is de-duplicated by hash even though it lacks a `copy` token. (Do not try to glob-match the base; the hash rule is authoritative.)

## DO-NOT-TOUCH (passed byte-identical — must remain so)
- The 16-row failure-modes table (A §11) — byte-identical to blueprint §C.
- The `chapter-manifest.yaml` v1 schema fenced block (A §12) — byte-identical to blueprint §D, every field.
- The bolded confidence rule sentence and the bolded deferred-write invariant sentence — verbatim.
- Frontmatter (name + description only).
