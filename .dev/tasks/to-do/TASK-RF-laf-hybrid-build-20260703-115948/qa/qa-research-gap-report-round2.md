# QA Research Gap Report — Round 2 (Gap-Fill Closure Verification)

**Lens:** GAP-DETECTION — re-verification round (adversarial stance)
**QA Mode:** research-gate | fix_authorization: false
**Scope:** Verify closure ONLY of the 6 gaps from round 1 (G1, G2, G3, G4, G5, G8).
Subsystems 01–06 (already-passing) were NOT re-audited.
**Gap-fill under test:** `research/07-gap-fill.md`
**Ground-truth:** `.dev/releases/current/0.1/design/` specs + repo-root `config/`, `prompts/`, `.github/`, `LICENSE`, and the vendored `creative-writing-skills/` subtree.

---

## Method

1. Read the round-1 gap report + the gap-fill file (`07-gap-fill.md`).
2. For each of the 6 gaps, verified the fill supplies **authorable, evidence-cited** content — not a hand-wave.
3. Independently spot-checked the gap-fill's own citations against on-disk ground truth (not trusting the fill's self-report).

**Ground-truth checks actually run this round (independent of the fill's claims):**

| Check | Result | Confirms |
|---|---|---|
| `ls .github/` (repo root) | exists, EMPTY, no `workflows/` | G3 "must create `.github/workflows/`" ✓ |
| `head LICENSE` (repo root) | `MIT License / Copyright (c) 2026 Ryan` | G2 repo-root=MIT ✓ |
| `ls creative-writing-skills/NOTICE` | absent | G2 "upstream ships no NOTICE" ✓ |
| `cat creative-writing-skills/CLAUDE.md` | `@AGENTS.md` (10 B) | G1 adopted pattern = thin pointer ✓ |
| `head creative-writing-skills/LICENSE` | Apache License 2.0 (11357 B) | G2 upstream=Apache-2.0 ✓ |
| `ls creative-writing-skills/.github/workflows/` | `ci.yml`, `release.yml` | G3 adopted CI shape exists ✓ |
| Read `prompts/transformation/tier_1_transform.md` (74 lines) | full content | G4 digest grounded ✓ |
| Read `prompts/transformation/tier_3_transform.md` (64 lines) | full content | G4 digest grounded ✓ |
| grep `config/age_profiles/tier_5_young_adult.yaml` | `adaptation_philosophy`:71, `supplementary_approach`:82, `core_principle`:72, `narrative_complexity`:35, `agency_externalization`:54 | G4 ya.md source keys ✓ |
| `ls config/age_profiles/` | tier_{1,2,3,5} only, NO tier_4 | G5/KC-6 ✓ |
| `ls docs/design_decisions/00{1,3}` | 001 (1108 B), 003 (1576 B) exist | G5 source files ✓ |
| grep top-level keys `templates/work_mapping_template.yaml` | 5 keys (l.4,11,39,47,57) | G8/KC-7 ✓ |
| boundary-contract.md l.48, 97, 145-147, 171-181 | all match fill's cites | G1/G2/G3 anchors ✓ |
| DESIGN.md l.105, 293, 70, 52 | all match fill's cites | G1/G8 anchors ✓ |
| skill-specs.md l.80-83, 276-282 | match fill's cites | G4/G5 anchors ✓ |
| boundary-contract.md manifest rows l.58-81 | 11 adopted agents + 12 adopted skills + 2 NATIVE + 2 BUILD-NEW agents + 3 NATIVE + 1 BUILD-NEW skills | G8/KC-1..5 ✓ |

Every spot-checked citation in the gap-fill resolved correctly. **No fabricated cites found.**

---

## Gap-by-gap closure verdict

### G1 — CLAUDE.md content (IMPORTANT) → **CLOSED**

The fill supplies a **complete authorable outline** (07-gap-fill.md:42-88) covering all three
DESIGN.md:105-mandated parts:
- **Adopted pattern** — resolved with evidence: upstream `CLAUDE.md` is a 10-byte `@AGENTS.md`
  pointer (independently confirmed: `cat` returns exactly `@AGENTS.md`). The fill correctly
  concludes LAF adopts the *thin-entry-point pattern*, not the file, and authors native content
  (LAF has no AGENTS.md, Mars layer cut). This is a genuine resolution, not a hand-wave.
- **LAF conventions section** — concrete: frontmatter dialect (Claude-lowered, no Mars keys),
  tier axis first-class, the 6 constraints, UV rule, flat-tree distribution. Cites DESIGN §2.1, §5.
- **Boundary-contract note** — present (VENDOR.md + check_boundary.py pointer + ADOPTED-PATCHED
  writer.md caveat).
- **Boundary note verified:** the claim that CLAUDE.md is outside the rule-F glob is TRUE — BC:145-147
  globs only `agents/*.md` + `skills/**/SKILL.md`. Confirmed independently.

Provenance ("NATIVE-authored, adapted-from-ADOPTED-pattern", no manifest hash row) is coherent and
matches the glob fact. A builder can drop the outline into a B2 paragraph verbatim. **Genuinely closed.**

### G2 — NOTICE R1/R5 contradiction (IMPORTANT) → **CLOSED**

The R1-vs-R5 contradiction is **explicitly resolved** (07-gap-fill.md:98): R5 wins — NOTICE **IS**
a required committed Phase-0 file. Two independent justifications, both verified:
1. **Spec already commits to it** — BC:48 literally reads `attribution retained per NOTICE`
   (confirmed verbatim). A manifest that references a file "per NOTICE" presupposes the file. Sound.
2. **License facts** — independently confirmed: vendored CWS ships `LICENSE` (Apache-2.0, 11357 B)
   but **NO NOTICE** (`ls` returns nothing). So LAF authors the NOTICE to carry attribution upstream
   didn't package. Correct.

**Placement justified against real on-disk license facts** (the round-1 ask): repo-root `LICENSE` =
MIT © 2026 Ryan (confirmed), vendored subtree = Apache-2.0. Fill places NOTICE at
`laf-adaptation/NOTICE` (with the vendored subset), NOT repo root, precisely to avoid muddling the
repo's MIT license with an Apache-2.0 NOTICE. This is a correct, evidence-grounded placement
decision — exactly what round 1 demanded.

An **authorable skeleton** is supplied (07-gap-fill.md:112-137), plus a well-reasoned companion
deliverable (`LICENSE-CWS` for Apache-2.0 §4(a) copy-of-license), and execution-time unknowns
(upstream_sha, holder name) are flagged non-blocking. **Genuinely closed.**

### G3 — .githooks/pre-commit + CI (IMPORTANT) → **CLOSED**

- **Phase conflict resolved** (07-gap-fill.md:154): Phase 0, not Phase 4. Justification is sound —
  `check_boundary.py` is authored in Phase 0 (DESIGN:293 confirmed), wrappers only invoke it, and
  deferring enforcement leaves the tree unguarded during Phases 1-3 (the exact window native edits
  land). A counter-consideration (why not Phase 2) is raised and dismissed with a valid reason
  (`--init` rewrites the manifest each phase; verify only checks listed files). Adversarially, this
  is the *right* kind of reasoning — it engages the objection rather than ignoring it.
- **`.github/` existence VERIFIED** (round-1 ask): fill states repo-root `.github/` exists but is
  EMPTY, no `workflows/`, must be created. **Independently confirmed** — `ls .github/` shows an empty
  dir, `ls .github/workflows/` fails. Accurate.
- **Authorable content supplied:** `.githooks/pre-commit` bash wrapper (07-gap-fill.md:168-188) and
  `.github/workflows/boundary.yml` (l.194-215), both invoking `uv run python scripts/check_boundary.py`
  (satisfies BC:181 UV rule — confirmed). Adopted-pattern grounding is real: CWS `.githooks/pre-commit`
  exists and AGENTS.md documents the opt-in `git config core.hooksPath .githooks` + `--no-verify`
  bypass verbatim (both confirmed on disk). CWS `.github/workflows/{ci,release}.yml` confirmed present.
- The no-`--upstream`-in-CI claim is grounded in BC:97 (`check_boundary.py` verify default = CI +
  pre-commit gate — confirmed) and correctly flagged for execution-time confirmation.

Nested-dir `cd`/`working-directory` caveat is flagged as an execution-time detail. **Genuinely closed.**

### G4 — children.md source digest (IMPORTANT) → **CLOSED**

This was the round-1 gap requiring the researcher to **actually open** the transform prompts. **They
did.** I independently read both files and cross-checked the digest table (07-gap-fill.md:234-246):

| Digest claim | Fill cite | Ground-truth (verified) |
|---|---|---|
| Prosocial centering "helping, sharing, kindness" | tier_1:9 | tier_1_transform.md:9 exact ✓ |
| Externalize agency; "Sauron was evil"→"Grumpy King" | tier_1:13-19 | l.13-19 exact table ✓ |
| Violence→cooperation (Battle→Big Tidy-Up) | tier_1:21-28 | l.21-28 exact ✓ |
| Death→journey/rest (died→"new adventure") | tier_1:30-37 | l.30-37 exact ✓ |
| Positive resolution; permitted/forbidden emotions | tier_1:46-50 | l.46-50 exact ✓ |
| Safe home preserved | tier_1:67 | l.67 exact ✓ |
| Vocab/sentence ceilings (12 words, 800-word ch.) | tier_1:52-58 | l.52-58 exact ✓ |
| Worked example (orcs→noisy grumbles) | tier_1:71-73 | l.71-73 exact ✓ |
| T3 weight-not-gore; hope; forbidden gore/torture | tier_3:28-29,47-48 | l.28-29, 47-48 exact ✓ |
| T3 death direct; Denethor before/after | tier_3:31-32,59-63 | l.31-32, 59-63 exact ✓ |
| T3 shift "protect→scaffold complexity" | tier_3:14 | l.14 exact ✓ |

The digest is a concrete, faithful, line-cited craft-dimension extraction — not a pointer to raw
files. This directly answers round-1 G4's core complaint. **ya.md source keys CONFIRMED to exist**
in tier_5 yaml: independently grepped `adaptation_philosophy` (l.71), `supplementary_approach`
(l.82), `core_principle` (l.72). Line numbers match the fill's claims exactly. **Genuinely closed.**

### G5 — tier_N.md commentary count (MINOR) → **CLOSED**

Recommended count + justification supplied (07-gap-fill.md:265): **5 files** (tier_1/2/3/4/5.md),
justified by skill-specs.md:80's literal range "tier_1.md … tier_5.md" (confirmed on disk — the
spec's own enumeration spans through tier_5). The commentary-≠-stored-profile distinction is correct
(no tier_4.yaml on disk — confirmed; a *commentary* file breaks no rule). A 4-file fallback is
documented as weaker with reasons. Guard against re-introducing a de-facto tier_4 profile is called
out. Source files (design_decisions 001/003) confirmed to exist. **Genuinely closed** (recommendation
+ evidence-backed justification, which is all a MINOR gap requires).

### G8 — numeric Key-Constraints (MINOR) → **CLOSED**

Consolidated reconciled constraint list (KC-1..KC-7, 07-gap-fill.md:284-296) with cites. Spot-verified:
- **KC-1/5 (15 agents / 23 adopted files):** boundary-contract manifest rows l.58-81 confirmed —
  11 adopted agents (10 CLEAN + writer PATCHED) + 12 adopted skills + 2 NATIVE + 2 BUILD-NEW agents +
  3 NATIVE + 1 BUILD-NEW skills. Decomposition is exact. ✓
- **KC-6 (no tier_4.yaml):** `config/age_profiles/` = tier_{1,2,3,5} only. Confirmed. ✓
- **KC-7 (work-mapping 5 keys):** `templates/work_mapping_template.yaml` top-level keys at
  l.4,11,39,47,57 = 5. Confirmed exact. ✓
- **"13 adopted" caveat:** DESIGN:70 confirmed to read "13 adopted agents/skills"; it genuinely does
  NOT decompose to 11+12=23. The fill honestly flags it as loose/stale and defers to the manifest per
  DESIGN §6 — an appropriate resolution (surfaced as Open-Question, not silently picked). ✓
- **"6 agents" Phase-0:** DESIGN:293 confirmed reads "6 adopted review/orch agents"; fill correctly
  reconciles it as the active subset while all 11 vendor in Phase 0. Sound. ✓

**Genuinely closed.**

---

## Adversarial residual notes (non-blocking; do NOT reopen gaps)

These are honesty checks, not reopened gaps — none rises to IMPORTANT/MINOR closure failure:

1. **KC-2 dormant-agent count (5) is the fill's own synthesis.** DESIGN:82 + l.110-111 mark dormant
   agents but I did not line-verify all five names this round. The fill cites them; low risk. Builder
   should sanity-check the dormant list against DESIGN §1.1 at author time. Not a closure defect.
2. **NOTICE/CLAUDE.md/hooks are all correctly self-flagged as OUTSIDE the rule-F glob** — this means
   they are un-enforced by check_boundary.py. The fill states this plainly (good), so the builder
   won't expect gate coverage. This is a documented property, not a gap.
3. **Execution-time unknowns** (upstream_sha, LICENSE-CWS naming, nested-dir `working-directory`,
   verify-mode-without-`--upstream`) are explicitly enumerated (07-gap-fill.md:313-318) and correctly
   marked non-blocking. Appropriate hand-off hygiene.

None of these blocks task-building or reopens a round-1 gap.

---

## Closure summary

| Gap | Severity | Round-1 status | Round-2 verdict | Evidence independently confirmed? |
|---|---|---|---|---|
| G1 CLAUDE.md content | IMPORTANT | open | **CLOSED** | Yes (CLAUDE.md=`@AGENTS.md`, glob, DESIGN:105) |
| G2 NOTICE contradiction | IMPORTANT | open | **CLOSED** | Yes (MIT root, Apache upstream, no NOTICE, BC:48) |
| G3 hooks + CI | IMPORTANT | open | **CLOSED** | Yes (.github empty, CWS pattern, BC:171-181/97) |
| G4 children.md digest | IMPORTANT | open | **CLOSED** | Yes (both transform prompts read; every cite exact) |
| G5 tier_N.md count | MINOR | open | **CLOSED** | Yes (skill-specs:80 range, no tier_4 profile) |
| G8 numeric constraints | MINOR | open | **CLOSED** | Yes (manifest rows, work-mapping 5 keys, DESIGN:70/293) |

All 6 gaps are genuinely closed with authorable, evidence-cited content. The gap-fill researcher
**actually opened the previously-unread sources** (tier_1/tier_3 transform prompts) and produced a
concrete line-cited digest; **resolved both inter-researcher/spec conflicts** (NOTICE R1/R5,
hooks phase) with justified single answers grounded in real on-disk license/CI facts; and **verified
`.github/` state** directly. Every citation I spot-checked resolved correctly against ground truth —
no fabrication, no hand-waving.

---

VERDICT: PASS
