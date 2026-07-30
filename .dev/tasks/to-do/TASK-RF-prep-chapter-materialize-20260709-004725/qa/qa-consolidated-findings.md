# M3 Final-Gate — Consolidated Findings (Serialized Fix input)

7 lens agents: 3 PASS (manifest-schema-fidelity, confidence-rule-integrity, boundary-contract-domain) + 4 FAIL. Consolidated verdict: **FAIL**. Dedup'd findings below, most-severe first. Fix ALL non-"won't-fix" items.

## GUARDRAILS — DO NOT TOUCH (all passed byte-identical; keep byte-identical)
- The `chapter-manifest.yaml` v1 schema fenced block (SKILL.md) — byte-identical to blueprint. For F5, add a PROSE clarification in the adopt section; do NOT edit the schema block.
- The 16-row failure-mode table — byte-identical, exactly 16 rows.
- The two bolded sentences (confidence rule + deferred-write invariant) — verbatim.
- SKILL.md frontmatter (name+description only).
- path-contract §4 read-set fenced block + §2 8-file table — byte-unchanged. check_boundary.py — byte-unchanged. VENDOR single row + U+2014. prep-cordinator STAGE 1..8 lines — byte-stable (STAGE 0 prepend only).

## CRITICAL

**C-1 (operational F1 / cross-artifact overlap): Mode-detect precedence picks `folder` for the split+monolith case instead of HALTing — VIOLATES AC2 / release-blocker #1.** SKILL.md Stage 0.2 says "evaluate top-to-bottom, first that holds"; rule 2 (`folder`, ≥2 non-canonical per-chapter files) has no guard for a CO-PRESENT dominating monolith, so for `Books/LWW/` (split `-1..-4.html` AND `...copy*.html` monoliths both present) rule 2 fires and returns `folder` before rule 4 (ambiguity → HALT) is reached. Spec §3 requires: a directory containing BOTH split chapter-like files AND a dominating monolith → `mode_confidence: UNCERTAIN` → HALT-ask (do not guess). FIX: add a negative guard to rule 2 — "folder (Mode A) fires ONLY when the directory holds ≥2 non-canonical per-chapter files AND NO co-present dominating monolith; if BOTH a split-set and a monolith are present, fall through to rule 4 (ambiguity → HALT-ask, mode_confidence: UNCERTAIN, block any source/ write)." Make the both-present case explicitly route to HALT. (`--source-mode folder` may still force it, but auto must not guess.)

**C-2 (operational F2 / cross-artifact CRITICAL): `--source-mode` is not forwarded through prep-cordinator.** The command declares `--source-mode` and the SKILL honors it, but prep-cordinator (which `/laf:prep` delegates the whole run to, and which dispatches chapter-materialize inline) has no `source_mode` input and never forwards it — the override is dead in the middle. FIX: (a) add a `source_mode` row to prep-cordinator's `## Inputs` table (`--source-mode <auto|folder|file|adopt>`, optional, default auto); (b) in the STAGE 0 note / fenced entry, state the coordinator passes `source_mode` (and `source_path`) into the inline chapter-materialize dispatch. Also surface the flag↔input_mode mapping (file→single-file, adopt→adopt-existing, folder→folder) in SKILL.md Stage 0.2 (where input_mode is set), not only in the command.

## IMPORTANT

**I-1 (operational F3): STAGE 0 runs before STAGE 1(a) source_path elicitation, but STAGE 0 needs source_path.** FIX: move the "require source_path (elicit as a required input if --source omitted)" obligation to the FRONT of STAGE 0 (STAGE 0 must first ensure source_path is present, then run the /source-fidelity source-access declaration). Update the STAGE 0 note + fenced entry so ordering is runnable; keep STAGE 1(a)'s wording coherent (it can reference that source_path was required at STAGE 0). Do not renumber STAGE 1..8.

**I-2 (operational F4): the "Split set incomplete" gate is unreachable in Mode A.** With only filenames present (4 files, no TOC), count_reconciliation is trivially satisfied and each boundary reads CERTAIN, so a partial split (4 of 17) is silently accepted. Spec failure-table row: "file count < TOC count → block Mode A unless operator confirms partial scope." FIX: in SKILL.md Stage 0.3 (count reconciliation) and boundary-rules.yaml `count_reconciliation`, require that when Mode A has NO corroborating expected-count signal (no TOC, no cross-checkable heading count), chapter-set COMPLETENESS is treated as UNCERTAIN → raise an `ambiguous_split`/gate item ("possible incomplete split; operator confirm partial scope"). Single-source filename count alone cannot certify completeness.

**I-3 (operational F5): Mode C adopt vs `.raw/`/`raw_path`.** Adopt-existing sets have no raw source, but the schema/§5 make `raw_path`/`.raw/` structurally present. FIX (PROSE only, do NOT edit the schema block): in SKILL.md §Idempotency/adopt and/or the manifest-contract note, state that for `provenance.class: ADOPTED` the `raw_path` / `.raw/` fields MAY be absent/null (a manifest-less adopted set has no retained raw), and that adopt writes/refreshes only the manifest (no `.raw/` copy). path-contract §6 `.raw/` retention note can add "(materialized chapters only; adopted sets may have no `.raw/`)".

**I-4 (operational F6): URL `--source` fetch-to-local has no implementing stage.** The command says a URL is fetched to a local file/`.raw/` first, but no stage performs it. FIX: in SKILL.md Stage 0.1 (Inventory), add that when `--source` resolves to a URL, it is fetched to a local file under `source/<slug>/.raw/` FIRST and the local path becomes the working `source_path` (consistent with the command's existing statement); provenance records the original URL.

**I-5 (cross-artifact IMPORTANT): `review.status` flip ambiguity at STAGE 7.** Two textually-identical `PENDING → CONFIRMED` flips co-exist (the `50-greenlight.md` file status and the separate `chapter-manifest.review.status`). FIX: disambiguate in prep-cordinator STAGE 7 — name each explicitly (e.g. "set `50-greenlight.md` status PENDING→CONFIRMED (the greenlight file) AND, separately, set `chapter-manifest.review.status` PENDING→CONFIRMED (the manifest)").

**I-6 (ac-coverage IMPORTANT): invariants-review.md cites non-existent skill sections.** The Phase-5 `invariants-review.md` AC rows cite "SKILL.md §12" / "§8 normalization" — those are the SPEC's section numbers; the chapter-materialize SKILL has UNNUMBERED `##` headings. FIX (sign-off artifact, not the spine): correct the citations in `phase-outputs/reviews/invariants-review.md` to the skill's actual heading names (`## Manifest output contract`, `## Format normalization & fidelity`).

## MINOR

**M-1 (boundary-compliance MINOR): CLAUDE.md edit absent from the QA inventory.** FIX: add a `laf-adaptation/CLAUDE.md` row to `phase-outputs/reports/qa-input-inventory.md` (the count-correction edit; already recorded in the task Deviations log).

**M-2 (ac-coverage MINOR / cross-artifact): AC1 "identical … chapter-manifest" reading.** AC1's "identical" applies to the canonical chapter TEXT set; the manifest legitimately records mode-specific provenance (`input_mode`, `source_kind`) and cannot be byte-identical across Mode A vs B. FIX: add a one-line clarification in SKILL.md (AC-relevant spot, e.g. Stage 0.4 or the manifest-contract note): "the canonical `ch-<NN>.txt` chapter TEXT is identical across Mode A/B; the manifest's mode/provenance fields legitimately differ by input mode."

**M-3 (cross-artifact MINOR): `min_body_chars: 500` vs `plausible_length_range` min 1500 in boundary-rules.yaml.** Reconcile: clarify with a comment that `min_body_chars` is the hard non-empty floor (reject empties) and `plausible_length_range` is the sanity band (below-band → PROBABLE/flag), OR align the numbers so min_body_chars ≤ plausible min. Prefer the clarifying comment.

**M-4 (cross-artifact MINOR): duplicate-monolith tie-break wording divergence** between SKILL.md and boundary-rules.yaml. Make the two consistent (shortest filename → lexicographic; byte-identical resolved by sha256).

## WON'T-FIX (note only)
- chapter_count: 17 schema worked-example vs 4-chapter narnia — the domain-expert lens ruled this an illustrative schema template value (with `|`-enum placeholders), zero boundary implication. Leave as illustrative; optionally the fix agent may add "(illustrative)" but it is non-blocking.
- spec §4's own STAGE 4/5 numbering trap — upstream spec surface, out of scope (the authored artifacts resolve it correctly).
- prep SKILL "never restate a path" then restating the 8-file set — pre-existing; the 8-file statement is a spec-mandated invariant assertion, not a path restatement of the kind the rule forbids.
