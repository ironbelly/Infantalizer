# R5 — Design Pack Cross-Validation (DESIGN↔CODE Fidelity)

**Task:** TASK-RF-native-prep-20260704-233101
**Topic:** Verify the design pack's concrete claims against live code.
**Method:** For each concrete/checkable claim in the 6 design docs, tag `[CODE-VERIFIED]` (with confirming file:line), `[CODE-CONTRADICTED]` (state what code shows), or `[UNVERIFIED]`.
**Scope:** DESIGN↔CODE fidelity ONLY. Evidence = file:line for every verdict.

Status: Complete

**Bottom line:** All 6 design docs cross-validated against live code. **Every concrete, checkable claim is CODE-VERIFIED. Zero contradictions found.** The design pack is a faithful build spec — the builder can trust its VENDOR line refs, path splits, edit anchors, schema keys, and boundary mechanics verbatim.

---

## A. VENDOR.md line-reference claims

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| VENDOR.md line 111 = `agents/analyst.md \| NATIVE \| — \| —` | DESIGN.md §1.1 (L78); prep-agent-schemas §3 (L106); boundary-verification row 8 | **[CODE-VERIFIED]** | `laf-adaptation/VENDOR.md:111` exact: `\| agents/analyst.md \| NATIVE \| — \| — \|` |
| VENDOR.md line 113 = `skills/adaptation-rules/** \| NATIVE` | DESIGN.md §6 C3 (L293); boundary-verification row 7 (L32) | **[CODE-VERIFIED]** | `laf-adaptation/VENDOR.md:113` exact: `\| skills/adaptation-rules/** \| NATIVE \| — \| — \|` |
| VENDOR.md line 117 = `agents/tier-coordinator.md \| BUILD-NEW` | DESIGN.md §1.1 (L78); prep-agent-schemas §4 (L171) | **[CODE-VERIFIED]** | `laf-adaptation/VENDOR.md:117` exact: `\| agents/tier-coordinator.md \| BUILD-NEW \| — \| — \|` |
| VENDOR.md line 60 = muse ADOPTED-CLEAN | prep-agent-schemas §implied; DESIGN.md §1.1 (L74) "muse is ADOPTED-CLEAN" | **[CODE-VERIFIED]** | `laf-adaptation/VENDOR.md:60`: `\| agents/muse.md \| ADOPTED-CLEAN \| c8819ec8… \| 18cafdc2… \|` |
| VENDOR.md line 65 = writer ADOPTED-PATCHED | DESIGN.md §1.1 (L75); boundary-verification row 10 (L35) | **[CODE-VERIFIED]** | `laf-adaptation/VENDOR.md:65`: `\| agents/writer.md \| ADOPTED-PATCHED \| 373e605b… \| c1b3e12f… \|` |

## B. check_boundary.py mechanics claims

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| `classify()` assigns NATIVE to new agents not in BUILD_NEW set | DESIGN.md §5 (L267); boundary-verification §2 (L65-70) | **[CODE-VERIFIED]** | `check_boundary.py:336-339` — `if parts[0]=="agents": if name in BUILD_NEW_AGENTS: return "BUILD-NEW"; return "NATIVE"`. `prep-cordinator.md` ∉ `BUILD_NEW_AGENTS {chronicler.md, tier-coordinator.md}` (L45) ⇒ NATIVE |
| `classify()` assigns NATIVE to new skill dirs not in BUILD_NEW_SKILLS | boundary-verification §2 (L67-69) | **[CODE-VERIFIED]** | `check_boundary.py:340-344` — `if parts[0]=="skills"…: if sk in BUILD_NEW_SKILLS: return "BUILD-NEW"; return "NATIVE"`. `prep`,`thematic-fidelity` ∉ `BUILD_NEW_SKILLS {adaptation-safety}` (L47) ⇒ NATIVE |
| `--init` regenerates rows from disk (`disk_agents()` + `disk_skill_dirs()`) only | DESIGN.md §5 (L263); boundary-verification §2 (L55) | **[CODE-VERIFIED]** | `check_boundary.py:378` (`for rel in disk_agents()`), `:389` (`for skdir in disk_skill_dirs()`); `disk_agents()`:306-308 globs `agents/*.md`; `disk_skill_dirs()`:311-313 iterates `skills/` dirs |
| New non-adopted skill dir → one `skills/<name>/** \| NATIVE \| — \| —` glob row | boundary-verification §2 (L67-69) | **[CODE-VERIFIED]** | `check_boundary.py:405-407` — `else:` (not adopted) branch: `rows.append((f"{skill_rel}/**", cls, NO_HASH, NO_HASH))` |
| ADOPTED-PATCHED reserved for writer.md (Rule C′) | DESIGN.md §1.1 (L75); boundary-verification Rule C′ (L87) | **[CODE-VERIFIED]** | `check_boundary.py:534-536` (Rule C′): `if r.cls=="ADOPTED-PATCHED" and r.path!="agents/writer.md": errors.append(…reserved for agents/writer.md only)`. Also `classify()`:330-331 assigns ADOPTED-PATCHED only to `agents/writer.md` |
| Muse cannot receive a skill line without violating C′ | DESIGN.md §1.1 (L74-75); boundary-verification row 11 (L36) | **[CODE-VERIFIED]** | Adding a `skills:` line to muse.md (ADOPTED-CLEAN) would change its body → Rule A `laf_sha256` mismatch (`:506`) AND Rule A′ upstream_sha256 mismatch (`:526-530`). To reclassify as ADOPTED-PATCHED would trip C′ (`:535`). Both gates confirm the claim |
| Editing a NATIVE/BUILD-NEW NO_HASH body does not alter its manifest row | DESIGN.md §5 (L275-276); prep-agent-schemas §3 (L106-107), §4 (L171-172) | **[CODE-VERIFIED]** | NATIVE/BUILD-NEW rows carry `— / —` (parser enforces: `:270-273`); Rules A/A′ only hash `is_adopted` rows (`:499-500`, `:520-521`). Body content of NATIVE files is never hashed → edit is boundary-safe |

## C. Root-mapping 5-key schema claim

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| Root mapping schema is exactly 5 keys: `work_metadata, characters, concepts, key_scenes, master_translation_table` | DESIGN.md §6 C2 (L292); path-contract §3 (L59-60); prep-skill-specs §4 (L72) | **[CODE-VERIFIED]** | `config/concept_mapping/templates/tolkien_mapping.yaml` — top-level keys at L4 (`work_metadata`), L13 (`characters`), L43 (`concepts`), L64 (`key_scenes`), L77 (`master_translation_table`). Exactly 5, no `meaning:` |
| ADDING_NEW_WORKS.md step 6 asserts the same 5 keys | DESIGN.md §6 C2 (L292); prep-skill-specs §4 (L72) | **[CODE-VERIFIED]** | `docs/guides/ADDING_NEW_WORKS.md:104` "## Step 6: Validate the YAML"; L111 comment: `# → ['characters', 'concepts', 'key_scenes', 'master_translation_table', 'work_metadata']` (5 keys, sorted) |

## D. Path-split claims (underscore root / hyphen 0.1-kb)

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| Root templates use underscore `<work>_mapping.yaml` | DESIGN.md §2 path-fidelity note (L132-135); path-contract §3 (L53-54) | **[CODE-VERIFIED]** | `config/concept_mapping/templates/` contains `narnia_mapping.yaml`, `tolkien_mapping.yaml` (underscore) — `ls` confirmed |
| 0.1 kb uses hyphen `<work>-mapping.yaml` | DESIGN.md §2 (L132-135); path-contract §3 (L51-52) | **[CODE-VERIFIED]** | `laf-adaptation/kb/adaptation-mapping/` contains `tolkien-mapping.yaml`, `universal-mappings.yaml` (hyphen) — `ls` confirmed |

## E. analyst.md edit-anchor claims

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| analyst.md is NATIVE, model opus, not hash-pinned | prep-agent-schemas §3 (L106) | **[CODE-VERIFIED]** | `laf-adaptation/agents/analyst.md:2` `name: analyst`, `:4` `model: opus`; VENDOR.md:111 NATIVE `—/—` (not pinned) |
| Has `## Inputs (passed by the caller)` section (granularity/out_path inserts) | prep-agent-schemas §3.1 (L113) | **[CODE-VERIFIED]** | `analyst.md:18` `## Inputs (passed by the caller)`; L19-21 list `source_path`, `work`, `chapter` — the exact anchor lines the diff extends |
| Has `## Output contract` with `transformation_flags` + `uncertainties` (meaning/compound_scene insert there) | prep-agent-schemas §3.2 (L124-143) | **[CODE-VERIFIED]** | `analyst.md:51` `## Output contract`; L54 lists `…transformation_flags, uncertainties` in the v2.0 schema — the exact keys the diff inserts `meaning`/`compound_scene` between |
| Has `## Hard behavior` section with Phase-0 block (body-note inserts after) | prep-agent-schemas §3.3 (L152-160) | **[CODE-VERIFIED]** | `analyst.md:33` `## Hard behavior (in this agent body, not delegated to a skill)`; L34-39 Phase-0 block; L37 `IF NO-ACCESS: emit status: ABORTED…HALT` — the ABORT gate the note must not relax |
| analyst currently hardcodes chapter granularity `work/analysis/ch-<NN>.yaml` | DESIGN.md §6 D-analyst-work-mode (L298); prep-agent-schemas §3.1 (L120) | **[CODE-VERIFIED]** | `analyst.md:52` `Write \`work/analysis/ch-<NN>.yaml\``; L14 "run **once per source chapter**"; L37 emits to `work/analysis/ch-NN.yaml` — chapter granularity is the current default |

## F. tier-coordinator.md edit-anchor claims

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| Has Checks A/B/C (Check D inserts after C) | prep-agent-schemas §4.1 (L176-177) | **[CODE-VERIFIED]** | `tier-coordinator.md:59` `### Check A — Source-fidelity consistency`; `:70` `### Check B — No downward disclosure leak`; `:82` `### Check C — Framing monotonicity`. Check D inserts after C's block (ends ~L93) |
| Has a `## Checks` report block with A/B/C lines (Check D `+ - D meaning-preserved` line inserts) | prep-agent-schemas §4.2 (L199-205) | **[CODE-VERIFIED]** | `tier-coordinator.md:145` `## Checks`; L146 `- A source-fidelity: PASS…`; L147 `- B disclosure-leak: PASS…`; L148 `- C monotonicity: PASS…` — exact anchor for the additive `- D meaning-preserved:` line |
| Conflicts ride existing `RECONCILED \| CONFLICT` gate; no new control flow | prep-agent-schemas §4.2 (L207-209) | **[CODE-VERIFIED]** | `tier-coordinator.md:35` `status: RECONCILED \| CONFLICT`; L36 `conflicts: [ ... ]`; Checks A/B/C append `conflicts += {type:…}` (L66-67, L78-79, L88-89) — Check D's `meaning_diff` rides the same list |
| tier-coordinator already loads adaptation-tiers/source-fidelity/kb-management (no new skill line for Check D) | prep-agent-schemas §4.2 (L209-211) | **[CODE-VERIFIED]** | `tier-coordinator.md:5-8` `skills:` = `adaptation-tiers`, `source-fidelity`, `kb-management` — all three present; Check D reads meaning as data, needs no new line |

## G. web-researcher.md claim

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| web-researcher is model sonnet, ADOPTED, tools Read/WebSearch/WebFetch | DESIGN.md §1.2 (L86); prep-skill-specs §3 (L63) | **[CODE-VERIFIED]** | `laf-adaptation/agents/web-researcher.md:4` `model: sonnet`; `:7` `tools: Read, WebSearch, WebFetch`; VENDOR.md:64 `agents/web-researcher.md \| ADOPTED-CLEAN` |

## H. prep-cordinator frontmatter skills-existence claims (prep-agent-schemas §1)

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| `source-fidelity` skill EXISTS | prep-agent-schemas §1 (L32) | **[CODE-VERIFIED]** | dir `laf-adaptation/skills/source-fidelity/` present (`ls` confirmed) |
| `adaptation-tiers` skill EXISTS | prep-agent-schemas §1 (L33) | **[CODE-VERIFIED]** | dir `laf-adaptation/skills/adaptation-tiers/` present |
| `adaptation-rules` skill EXISTS | prep-agent-schemas §1 (L34) | **[CODE-VERIFIED]** | dir `laf-adaptation/skills/adaptation-rules/` present; VENDOR.md:113 NATIVE |
| `kb-management` skill EXISTS | prep-agent-schemas §1 (L35) | **[CODE-VERIFIED]** | dir `laf-adaptation/skills/kb-management/` present; VENDOR.md:81 ADOPTED-CLEAN |
| `prep` skill is NEW (to be created by this task) | prep-agent-schemas §1 (L36); prep-skill-specs §1 | **[CODE-VERIFIED]** (correctly absent) | `laf-adaptation/skills/prep/` MISSING — expected; this task creates it. Not a contradiction |
| `thematic-fidelity` skill is NEW (to be created by this task) | prep-agent-schemas §1 (L37); prep-skill-specs §2 | **[CODE-VERIFIED]** (correctly absent) | `laf-adaptation/skills/thematic-fidelity/` MISSING — expected; this task creates it. Not a contradiction |

> **Note for builder:** 2 of the 6 skills in the `prep-cordinator` frontmatter (`prep`, `thematic-fidelity`) do not yet exist. This is BY DESIGN — they are the two NATIVE skills this task creates (DESIGN.md §1.1, prep-skill-specs.md §1-2). Their absence is the expected pre-build state, NOT a design/code contradiction.

## I. Supplementary boundary claims (bonus verifications)

| Claim | Design location | Verdict | Evidence (file:line) |
|---|---|---|---|
| Commands live at `.claude/commands/laf/`, outside `laf-adaptation/`, NOT VENDOR-manifested | DESIGN.md §5 (L277), §6 C1 (L291); boundary-verification rows 1-2 | **[CODE-VERIFIED]** | `check_boundary.py` REPO = `parents[1]` = `laf-adaptation/` (`:31`); manifest paths must be under REPO (`_safe_repo_path`:215-216 rejects escapes). `.claude/commands/laf/` is outside REPO ⇒ cannot be manifested — consistent with claim |
| Rule E: prep-cordinator/prep/thematic-fidelity do not collide with upstream names | boundary-verification Rule E (L89) | **[UNVERIFIED]** | Cannot confirm absence in upstream CWS without an `--upstream` checkout (Mode U). Rule E code exists (`:610-621`); the *claim* that CWS has no prep phase is plausible but not code-checkable from this tree alone. Non-blocking (Mode V does not run Rule E's upstream arm) |
| `skills/adaptation-rules/**` glob covers exemplars (no new VENDOR row needed) | DESIGN.md §5 (L272-274); boundary-verification row 7 (L32) | **[CODE-VERIFIED]** | `manifest_covers()`:296-302 — glob row `skills/adaptation-rules/**` (VENDOR.md:113) covers any `skills/adaptation-rules/…` path via `rel.startswith(r.path[:-2])`. Exemplars under `skills/adaptation-rules/resources/exemplars/` are covered |
| C4: skill dir is `laf-adaptation/skills/adaptation-rules/` (spec's `adaptation-rules/resources/` path was wrong) | DESIGN.md §6 C4 (L294) | **[CODE-VERIFIED]** | All skills live under `laf-adaptation/skills/` (`ls` shows `skills/adaptation-rules`); no top-level `laf-adaptation/adaptation-rules/`. Design's corrected path matches code |

---

## Contradictions found

**NONE.** Every concrete, checkable claim in the design pack is CODE-VERIFIED against the live tree.

One item is **[UNVERIFIED]** (not contradicted): boundary-verification Rule E's claim that `prep-cordinator`/`prep`/`thematic-fidelity` have no upstream-name collision cannot be confirmed without an `--upstream` CWS checkout (Mode U). This is non-blocking for Mode V (the CI/pre-commit gate) — Rule E's upstream-collision arm only runs under `--upstream` (`check_boundary.py:614-621`). The builder should still run Mode U at P3 if a pinned-SHA checkout is available, per boundary-verification §3.

**Builder guidance:** No design claim is contradicted, so no task item needs to be dropped or reworded on fidelity grounds. All VENDOR line refs (60/65/111/113/117), the classify()/--init boundary mechanics, the 5-key root schema, the underscore/hyphen path split, and all analyst.md + tier-coordinator.md edit anchors are exact and safe to build against verbatim.

