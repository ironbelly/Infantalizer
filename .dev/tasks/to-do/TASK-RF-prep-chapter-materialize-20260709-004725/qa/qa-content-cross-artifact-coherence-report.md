# QA Report — Final Gate (M3 content) · Cross-Artifact Coherence & Non-Restatement

**Topic:** TASK-RF-prep-chapter-materialize-20260709-004725 — Stage-0 chapter-materialize wiring
**Date:** 2026-07-09
**Phase:** task-qualitative (final-gate; lens = cross-artifact coherence & non-restatement)
**Fix cycle:** N/A
**fix_authorization:** false (report-only; no source file modified)

---

## Overall Verdict: FAIL

Adversarial stance held: I assumed ≥5 cross-artifact coherence errors existed and hunted for them.
I found **6 findings** (1 CRITICAL, 3 IMPORTANT, 2 MINOR). The reference chain mostly resolves and
the non-restatement discipline is largely honored, but there are genuine contradictions and one
broken cross-artifact reference.

---

## Reference chain traced (SKILL.md → prep-cordinator STAGE 0 → prep SKILL §1 → command --source-mode → path-contract §6 → source/README → VENDOR row)

| Hop | From | To | Resolves? | Evidence |
|-----|------|-----|-----------|----------|
| 1 | chapter-materialize SKILL.md | boundary-rules.yaml (5 layers + confidence mirror) | YES | `resources/boundary-rules.yaml` exists (4379 B); 5 layer keys + `confidence_rule` present |
| 2 | prep-cordinator STAGE 0 | chapter-materialize skill (inline dispatch) | YES | agent L12 `skills:` line + L46-84 STAGE 0 block; skill frontmatter `name: chapter-materialize` |
| 3 | prep SKILL §1 Stage-0 note | chapter-materialize + manifest sidecar | YES | prep SKILL L21-26; points at `laf-adaptation:chapter-materialize` |
| 4 | command `--source-mode` | prep SKILL §1 + chapter-materialize | YES | prep.md L22-29; arg-hint L3 |
| 5 | command `input_mode` mapping | manifest schema `input_mode` enum | **NO** | See Finding #1 (CRITICAL) |
| 6 | path-contract §6 | chapter-materialize schema | YES | path-contract L100-117; defers full field list to skill |
| 7 | path-contract §5 write-ownership | STAGE 0 writes | YES | rows L84-86 (`ch-<NN>.txt`, `chapter-manifest.yaml`, `.raw/*`) |
| 8 | source/README materialization | manifest + `.raw/` | YES | README L9-22 |
| 9 | VENDOR row | skills/chapter-materialize/** NATIVE | YES | VENDOR.md L124 `skills/chapter-materialize/** | NATIVE | — | —` |

Symlink verified live: `.claude/skills/chapter-materialize -> ../../laf-adaptation/skills/chapter-materialize`
(matches the `.claude/skills/prep` pattern the discovery artifact claimed).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Full chain reference resolution (9 hops) | FAIL | Hop 5 broken — `input_mode` enum mismatch (Finding #1) |
| 2 | No skill/command/agent restates a literal package/read-set path | FAIL | prep SKILL §1 restates the 8-file "`00`–`70`" set; §7 restates the 3-file read-set (Finding #4, MINOR) — but agent + command are clean |
| 3 | Manifest "sidecar, NOT rewrite_phase_reads member" consistent across SKILL / path-contract §4 note / §6 | PASS | skill L170-171; path-contract §4 note L75-77; §6 L113-115 — all three assert identical claim |
| 4 | STAGE 5 / STAGE 7 extensions reference Stage-0 deferred writes coherently | PASS-with-caveat | agent L99-103 (STAGE 5 receives `ambiguous_splits`), L112-116 (STAGE 7 commits deferred `ch-NN.txt`) — coherent; but manifest `review.status` flip is contradictory across artifacts (Finding #2) |
| 5 | Additive `skills:` line + `--source-mode` flag consistent between agent frontmatter and command | PASS | agent L12 `- laf-adaptation:chapter-materialize`; command arg-hint L3 + body L26-29 |
| 6 | STAGE-0 stage-count prose ("9 stages") consistent with "8-section" SKILL referent | PASS | agent L21/L26/L46 — "9-stage pipeline (STAGE 0 + the 8 below)" vs "8-section procedure"; referents distinct and correctly kept (per the discovery numbering contract) |
| 7 | Mode-C adopt claim vs actual filesystem (narnia ch-01..04, tolkien ch-01) | PASS | `source/narnia/ch-01..04.txt` + `source/tolkien/ch-01.txt` exist; contiguous from 01 |
| 8 | chapter_count vs mode-ambiguity example internal consistency | FAIL | Finding #3 (IMPORTANT) — schema example `chapter_count: 17` |

---

## Summary
- Checks passed: 5 / 8
- Checks failed: 3
- Critical issues: 1
- Issues fixed in-place: 0 (report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `.claude/commands/laf/prep.md` L28-29 ↔ `chapter-materialize/SKILL.md` L182 | **`input_mode` enum contradiction (AX-2).** The command states the flag values "map to the manifest `input_mode`: folder→`folder`, file→`single-file`, adopt→`adopt-existing`." The manifest schema in the skill declares `input_mode: folder | single-file | adopt-existing` — consistent there. BUT the prep-cordinator STAGE 0 note (agent L75) and Stage 0.2 skill output (`input_mode` + `mode_confidence`, skill L61) describe modes as **`adopt / folder / file`**, and the command's own arg-hint is `--source-mode auto\|folder\|file\|adopt`. The value the operator types (`file`) is NOT the value written to the manifest (`single-file`), and the value `adopt` becomes `adopt-existing`. This 3-way naming (`file`→`single-file`, `adopt`→`adopt-existing`) is documented in exactly ONE place (command L28-29) and is silently assumed everywhere else. A downstream consumer reading the manifest `input_mode: single-file` cannot round-trip it to the `--source-mode file` flag without that single buried mapping line. This is a live cross-artifact coherence gap: the flag vocabulary and the manifest vocabulary are two different closed sets joined by one un-cross-referenced sentence. | Add the flag↔manifest `input_mode` mapping to the manifest output contract section of `chapter-materialize/SKILL.md` (co-locate it with the schema that defines the enum), and have the command's L28-29 mapping reference it rather than being the sole definition. At minimum, make the skill's `input_mode` enum comment cite the `--source-mode` flag values so the two closed sets are visibly reconciled in the schema itself. |
| 2 | IMPORTANT | `chapter-materialize/SKILL.md` L173 ↔ agent `prep-cordinator.md` L116 ↔ L67 | **`review.status` flip contradiction (AX-2).** The skill says: manifest is written with `review.status: PENDING`; "`prep-cordinator` flips it to `CONFIRMED` on greenlight" (L173) and Stage 0.5 "sets `chapter-manifest.review.status: CONFIRMED`" (L108). The agent STAGE 7 ratification note (L116) says on CONFIRM the coordinator "sets `chapter-manifest.review.status: PENDING → CONFIRMED`" — consistent. BUT the agent STAGE 7 fenced pipeline step (L64-67) describes the greenlight CONFIRM as setting "**status PENDING → CONFIRMED**" for the **greenlight/50-greenlight.md** status (path-contract §2 L31, `50-greenlight.md status: PENDING → CONFIRMED`), and the chapter-manifest flip is a *separate* status on a *separate* file. The two `PENDING → CONFIRMED` flips (greenlight-file status vs chapter-manifest `review.status`) are textually identical and co-located in STAGE 7, creating a real ambiguity about which file's status is being set at L67. A reader cannot tell whether the single L67 "status PENDING → CONFIRMED" covers the manifest or only the greenlight file. | In the agent STAGE 7 fenced step (L64-67), disambiguate: state that the CONFIRM sets `50-greenlight.md status: PENDING → CONFIRMED` AND (per the ratification note) the separate `chapter-manifest.review.status: PENDING → CONFIRMED`. Do not leave the two identically-worded flips to be inferred from adjacency. |
| 3 | IMPORTANT | `chapter-materialize/SKILL.md` L192 (schema) ↔ L161 (failure table) ↔ actual `source/narnia` | **`chapter_count: 17` example is internally self-contradicting for the shipped work (AX-2).** The manifest schema example hardcodes `work: narnia`, `slug: narnia`, `chapter_count: 17`, and lists chapters keyed to LWW ("Lucy Looks into a Wardrobe"). LWW actually has **17 chapters** in full — so 17 is correct for the *complete* novel. BUT the shipped `source/narnia/` set is `ch-01..04` (4 files), which the skill itself (L133) and source/README (L21-22) describe as the adopted set. The schema example therefore depicts a `chapter_count: 17` narnia manifest that does not correspond to any state this repo can produce from its committed narnia source (4 chapters), while simultaneously the failure-table row L161 uses "`-1..-4` but TOC says 17" as the canonical Split-set-incomplete example — i.e. the exact 4-vs-17 gap that the schema example glosses over as a clean 17. The schema example and the failure-mode example describe the same work (narnia/LWW) with contradictory chapter states without noting that the committed set is the *partial* (4-chapter) case. | Either annotate the schema example that `chapter_count: 17` is the *full-novel* illustration (not the committed 4-chapter adopt set), or switch the illustrative `chapter_count` to a value consistent with the committed source so the schema, the failure-table example, and `source/narnia/` tell one coherent story. |
| 4 | MINOR | `prep/SKILL.md` L19 and L119-121 | **Non-restatement discipline: skill restates literal path-contract content (AX-1 drift risk).** §1 opens "never restate a path literally in this skill" (L17-18) then immediately restates the package contents as "the 8 fixed-name files `00`–`70`" (L19); §7 restates the read-set as "`[30-mapping, 40-prep-brief, 10-challenges]`" (L119-121). These duplicate the authoritative path-contract §2 (8-file table) and §4 (3-file read-set). The agent body and command correctly avoid this ("never restate a path here" — agent L30). The skill's own rule is violated by the skill itself. This is drift-prone: if path-contract §2/§4 change, these mirror statements silently diverge. Note: the discovery artifact (edit-loci L22) explicitly required "keep the '8 fixed-name files 00-70' statement at line 19 intact (spec N3 forbids a 9th package file)" — so this restatement is *intentional and spec-mandated*, hence MINOR not IMPORTANT. But the §1 self-contradiction ("never restate a path" + restating the file set) should carry a note that the count is an invariant-assertion, not a path definition. | Add a half-sentence in prep SKILL §1 clarifying that naming the "8 fixed-name `00`–`70`" set is an invariant assertion (the manifest is not a 9th file), NOT a path restatement — the authoritative names/paths remain in path-contract §2. Resolves the surface self-contradiction with L17-18. |
| 5 | MINOR | `boundary-rules.yaml` L65 vs L66 | **Content-sanity floor internal inconsistency (AX-2, within-file — flagged as it feeds the cross-artifact confidence contract).** `content_sanity.min_body_chars: 500` (the non-empty/front-matter floor) vs `plausible_length_range.min_chars: 1500`. A chapter of 500–1499 chars passes the "non-empty body" floor (skill Layer 4: "non-empty body, a plausible length") but fails the plausible-length floor — the skill's Layer 4 prose ("has a non-empty body, a plausible length") collapses two different thresholds the YAML separates. Not itself a cross-artifact break, but the skill's Layer-4 confidence contract (which feeds CERTAIN/PROBABLE tagging consumed downstream) is underspecified about which floor gates the confidence drop. | Clarify in the skill Layer-4 row (L77) or boundary-rules comment which floor triggers a confidence downgrade vs which triggers front/back-matter reclassification, so the 500 vs 1500 gap is intentional and consumer-legible. |
| 6 | MINOR | `chapter-materialize/SKILL.md` L134-141 duplicate-pick vs `boundary-rules.yaml` L51-54 | **Duplicate-monolith tie-break wording (AX-1, low risk).** Skill L138-141: canonical pick = "shortest filename, tie-broken by lexicographic order (so the un-suffixed base name wins over `... copy N`)." boundary-rules L51-54 says `ignore_globs` is a HINT only and the "base monolith named WITHOUT a 'copy' token ... will NOT glob-match"; the sha256 tie-break is authoritative. These are consistent in intent, but the skill says "shortest filename" as the *primary* key while the YAML frames the base-name-wins as an sha256-tie-break consequence. Both reach the same result for the LWW case; the two descriptions of the *ordering key* differ (shortest-filename-then-lexicographic vs hash-dedup-then-base-name). | Align the two descriptions on a single stated ordering key (recommend: "byte-identical (same sha256) → pick shortest filename, lexicographic tie-break"), and have boundary-rules reference the skill as authoritative (it already says "SKILL.md wins on any drift" for the confidence rule — extend that note to the dedup rule). |

---

## Non-restatement audit (per instruction: "verify NO skill/command/agent body restates a literal package or read-set path")

| Artifact | Restates a literal package/read-set path? | Verdict |
|----------|-------------------------------------------|---------|
| `prep-cordinator.md` (agent) | No — explicitly "never restate a path here" (L29-30); Stage-0 note L82-84 defers to path contract | CLEAN |
| `.claude/commands/laf/prep.md` | No — "output package path layout is fixed by ... path-contract.md" (L12-13) | CLEAN |
| `.claude/commands/laf/rewrite.md` | Restates the 3-file read-set (L11-13) — but this is the read-set *consumer*, and it cites path-contract §4 as authority (L9) | ACCEPTABLE (cites authority) |
| `prep/SKILL.md` | YES — "8 fixed-name files `00`–`70`" (L19) + read-set list (L119-121) | Finding #4 (MINOR; spec-mandated invariant assertion) |
| `path-contract.md` | It IS the source of truth | N/A |

The core non-restatement contract (agent + command must not restate paths) **holds**. The skill's
restatements are invariant assertions the discovery artifact explicitly mandated, hence downgraded to MINOR.

---

## Manifest "sidecar / NOT a rewrite_phase_reads member" three-way consistency (PASS)

Verified identical claim in all three required locations:
- `chapter-materialize/SKILL.md` L170-171: *"`chapter-manifest.yaml` is a `source/` sidecar — NOT a numbered package file, NOT a `rewrite_phase_reads` member."*
- `path-contract.md` §4 note L75-77: *"the Stage-0 `source/<slug>/chapter-manifest.yaml` is a `source/` sidecar, deliberately NOT in `rewrite_phase_reads` ... read-set stays exactly the three files above (no 4th entry)."*
- `path-contract.md` §6 L113-115: *"not a package file ... not a `rewrite_phase_reads` member."*
- Corroborated by `prep/SKILL.md` §1 note L24-25 and `source/README.md` L16-17.

The 3-file read-set (`30-mapping`, `40-prep-brief`, `10-challenges`) is byte-consistent across
path-contract §4, prep SKILL §7, and rewrite.md — no 4th entry leaked in. **This is the highest-risk
invariant and it is fully coherent.**

---

## STAGE 5 / STAGE 7 deferred-write coherence (PASS)

- STAGE 5 (agent L99-103): the Q-gate "**also receives the Stage-0 `ambiguous_splits`**" — matches
  skill Stage 0.5 (L104-109: deferred items "injected into the existing §5 question gate").
- STAGE 7 (agent L112-116): on CONFIRM "commits the **deferred** `ch-NN.txt` writes for the now-resolved
  boundaries" — matches skill Stage 0.5 (L107-108: "the `prep-cordinator` (not this skill) commits the
  deferred writes"). Ownership (skill plans/defers; coordinator commits) is coherent across both artifacts.

The deferred-write invariant chain is coherent; the only STAGE 7 defect is the identical-wording
`PENDING → CONFIRMED` ambiguity (Finding #2).

---

## Self-Audit

**(a) Reliance list — rf-qa structural PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was provided in the spawn prompt. I therefore fell back to
  standalone behavior and re-verified structural facts myself (symlink existence, VENDOR row presence,
  file existence). Nothing was relied-upon-without-verification.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Enum reconciliation (Finding #1):** Read command L28-29 AND skill schema L182 AND skill Stage 0.2
  L41-61 — compared the `--source-mode` flag closed set `{auto,folder,file,adopt}` against the manifest
  `input_mode` closed set `{folder,single-file,adopt-existing}`; found the `file`→`single-file` /
  `adopt`→`adopt-existing` mapping exists in exactly one un-cross-referenced sentence.
- **Sidecar invariant three-way (PASS):** grep-free manual read of skill L170, path-contract L75-77 +
  L113-115 — confirmed byte-consistent claim.
- **Filesystem-vs-doc adopt claim:** `ls source/narnia` (ch-01..04) + `ls source/tolkien` (ch-01) vs
  skill L133 + README L21-22 — confirmed the adopt claim, then found the schema `chapter_count: 17`
  vs 4-file reality tension (Finding #3).

**Confidence:** Verified: 8/8 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 8 | Grep: 1 (multi-pattern) | Glob: 0 | Bash: 2

Tool-call count (11 Read/Grep/Bash invocations across 8 files) ≥ 8 checklist items — engagement floor met.

**Tool-engagement summary (web research):** No external/web lookup was required for this review — the
lens is entirely local-file-bound (cross-artifact coherence within the repo). Tavily was therefore not
invoked; no fallback occurred.

---

## Recommendations
1. Resolve Finding #1 (CRITICAL) before this output ships: the `--source-mode` ↔ manifest `input_mode`
   vocabulary bridge must be defined at the schema, not buried in one command sentence.
2. Disambiguate the two identical `PENDING → CONFIRMED` flips in agent STAGE 7 (Finding #2).
3. Reconcile the narnia `chapter_count: 17` schema example with the committed 4-chapter source (Finding #3).
4. MINOR findings #4–#6 are drift-prevention improvements; address in the same pass since all touch the
   same three files.

Per the qualitative-QA no-leniency rule, ALL findings (including MINOR) must be resolved before this
output passes the final gate.

## QA Complete
