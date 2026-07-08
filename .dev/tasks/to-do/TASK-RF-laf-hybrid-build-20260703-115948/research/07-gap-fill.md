# Research: Gap-Fill — Peripheral Spec-Named Deliverables
**Topic type:** Gap-Fill
**Scope:** CLAUDE.md, NOTICE, .githooks/CI, children.md source, tier_N.md count, numeric Key-Constraints
**Status:** Complete
**Date:** 2026-07-03
---

## Evidence base (files opened for this gap-fill)

| File | What it grounds |
|---|---|
| `.dev/releases/current/0.1/design/DESIGN.md` §1-2, §5, §7 | G1, G3 phase placement, G8 |
| `.dev/releases/current/0.1/design/boundary-contract.md` §2 (l.48), §4 (l.171-181) | G2, G3 |
| `.dev/releases/current/0.1/design/skill-specs.md` §1, §4.1 | G4, G5 |
| `.dev/releases/current/0.1/creative-writing-skills/CLAUDE.md` | G1 — adopted CLAUDE.md pattern (`@AGENTS.md`) |
| `.dev/releases/current/0.1/creative-writing-skills/AGENTS.md` | G1, G3 — adopted conventions + `.githooks` pattern |
| `.dev/releases/current/0.1/creative-writing-skills/LICENSE` | G2 — upstream is Apache-2.0 (full text present, NO NOTICE) |
| `.dev/releases/current/0.1/creative-writing-skills/.githooks/pre-commit` | G3 — adopted opt-in hook pattern |
| `.dev/releases/current/0.1/creative-writing-skills/.github/workflows/ci.yml` | G3 — adopted CI shape |
| `prompts/transformation/tier_1_transform.md`, `tier_3_transform.md` | G4 — children.md source (READ verbatim) |
| `config/age_profiles/tier_1_preschool.yaml`, `tier_3_middle_elementary.yaml`, `tier_5_young_adult.yaml` | G4 — vocab/sentence ceilings, safe-home, nightmare-prevention, ya keys |
| `docs/design_decisions/{001-five-tier-system.md,003-agency-externalization.md}` (existence + skill-specs cite) | G5 |

**Repo-root facts verified this session (2026-07-03):**
- `.github/` EXISTS at repo root but is EMPTY — **no `.github/workflows/`** (G3: must be created).
- Repo-root `LICENSE` is **MIT** ("Copyright (c) 2026 Ryan"). The *vendored upstream* CWS is **Apache-2.0** — two different licenses; the adopted subtree must retain its own attribution (G2).
- **No `NOTICE`** file exists in the vendored CWS tree (only `LICENSE` = Apache-2.0 full text). LAF must author the NOTICE (G2).
- The vendored `creative-writing-skills/CLAUDE.md` is a 10-byte pointer: literally `@AGENTS.md` (G1).

---

## G1 (IMPORTANT) — CLAUDE.md content for `laf-adaptation/`

**Spec anchor:** DESIGN.md:105 lists `laf-adaptation/CLAUDE.md` = "ADOPTED pattern + LAF conventions section + boundary-contract note". DESIGN §1 (l.38-51, provenance classes + constraint #6), §2.1 (l.147-154, Claude-lowered dialect), §5 (l.264-273, the 6 constraints).

**Resolved provenance:** `CLAUDE.md` is **NATIVE-authored, adapted-from-ADOPTED-pattern** (not ADOPTED-CLEAN). It is NOT hash-pinned and is OUTSIDE the `check_boundary.py` rule-F glob (rule F globs only `agents/*.md` + `skills/**/SKILL.md` — boundary-contract.md:147), so it needs no manifest row. Mark it `NATIVE` in VENDOR.md's prose (not the hashed manifest) for provenance clarity.

**The "ADOPTED pattern" resolved (evidence).** The upstream CWS root `CLAUDE.md` is a **one-line pointer**: `@AGENTS.md` (creative-writing-skills/CLAUDE.md, 10 bytes). The real guidance lives in `AGENTS.md`. So the adopted *pattern* is: "CLAUDE.md is a thin entry point that references a fuller conventions doc; keep repo guidance in one canonical place." LAF adopts this **pattern**, not the file — LAF's CLAUDE.md carries its own content (LAF has no `AGENTS.md` and its conventions differ: Mars is cut). Provenance line to state in the file: *"Structure adopted from upstream CWS CLAUDE.md/AGENTS.md convention; content authored for LAF (Mars/Meridian layer removed)."*

**Authorable outline for `laf-adaptation/CLAUDE.md`:**

```markdown
# CLAUDE.md — LAF Adaptation Framework

Guidance for AI agents working in this repository. LAF 0.1 is a **prompt + YAML-config
framework** (ADR-006 — no Python/CLI runtime; the one script, check_boundary.py, is a
validation tool only). Structure adopted from the upstream CWS CLAUDE.md/AGENTS.md
convention; content is LAF-native (the Mars/Meridian packaging layer is cut).

## Provenance model (READ FIRST)
Every file under agents/ and skills/ is exactly one of three classes:
- **ADOPTED** — vendored from CWS verbatim (patch-clean, prefix-rewritten). NEVER edit an
  adopted file's body. See VENDOR.md for the per-file manifest and hashes.
- **NATIVE** — LAF-authored adaptation spine (tiers, rules, source-fidelity, safety).
- **BUILD-NEW** — greenfield in both systems (chronicler, tier-coordinator, adaptation-safety).

## The boundary contract (constraint #6 — load-bearing)
Native knowledge enters an ADOPTED agent ONLY as a loadable skill via `skills:` frontmatter —
NEVER by editing the adopted agent's body. This is what keeps the adopted subset upstream-syncable.
- Manifest + hashes: `VENDOR.md`
- Enforcement: `uv run python scripts/check_boundary.py` (run before every commit; see .githooks/)
- If you think you must edit an adopted file: STOP. Add a skill instead, or record it as ADOPTED-PATCHED
  (only writer.md is permitted, additive `- laf-adaptation:<skill>` frontmatter line only).

## LAF conventions
- **Frontmatter dialect:** Claude-native / cw-lowered — `name` + `description` only (skills),
  Claude agent keys (agents). NO Mars keys (`type`, `model-invocable`, `effort`, `model-policies`,
  `sandbox`, `subagents`). Adopted files are vendored from CWS `cw/` (already Claude-lowered),
  not from Mars `agents/`. (DESIGN §2.1)
- **Tier axis is first-class (constraint #1):** the active tier is ALWAYS an explicit `active_tier`
  parameter — never inferred from genre or persona. Five tiers (1,2,3,5 stored; **Tier 4 is
  interpolated at request time, never stored as a file**). Profiles: `kb/tiers/tier_<N>.yaml`.
- **The 6 constraints** (DESIGN §5): (1) tier axis first-class; (2) uncertainty discipline —
  CERTAIN/PROBABLE/UNCERTAIN tags + ABORT-on-NO-ACCESS; (3) safety_check gate (FAIL blocks
  promotion); (4) review quartet stays 4 distinct agents + safety-verifier is a distinct 5th;
  (5) work/ vs kb/ split (promotion only on muse-accept); (6) skill-vs-agent boundary contract.
- **UV only:** never `python -m` / bare `pip`. The pre-commit + CI invocation is
  `uv run python scripts/check_boundary.py`.
- **Distribution is one flat tree** — Mars packaging (mars.toml, cw/ mirror, sync_cw_skills.py) is cut.

## Where things live
- agents/ — 11 adopted + 2 native + 2 build-new = 15 agent files
- skills/ — 12 adopted + 3 native + 1 build-new = 16 skill dirs
- kb/tiers/, kb/adaptation-mapping/, kb/adaptations/<work>/ — native kb layers
- work/ — lifecycle (drafts, analysis, safety-reports); promoted to kb/ only on muse-accept
- scripts/check_boundary.py — the ONLY script; boundary-contract enforcement
- VENDOR.md — the boundary manifest; NOTICE — Apache-2.0 attribution for the adopted subset
```

**Builder note:** This is authored prose (no verbatim upstream source for the body — the upstream file is just `@AGENTS.md`). The B2 self-contained paragraph for the CLAUDE.md item should carry the three required parts and cite DESIGN.md:105, §2.1, §5. Placement: **Phase 0** (it documents the vendored tree the moment it exists) or early **Phase 1**; recommend Phase 0 alongside VENDOR.md/NOTICE so the conventions doc lands with the vendored subset it governs.

---

## G2 (IMPORTANT) — NOTICE file (R1/R5 contradiction RESOLVED)

**Spec anchor:** boundary-contract.md:48 — `license: Apache-2.0 (upstream) — attribution retained per NOTICE`. DESIGN.md:106 — VENDOR.md line "(Apache-2.0 attribution)".

**RESOLUTION: a `NOTICE` file IS required and IS a committed Phase-0 file.** R5 is correct; R1's "maybe just a VENDOR.md line" is superseded. Two independent reasons:

1. **The spec already commits to it.** boundary-contract.md:48 literally says attribution is "retained **per NOTICE**" — the manifest references a NOTICE file by name. A file cannot be referenced "per NOTICE" and simultaneously not exist. The decision is already made in the spec; the researchers just didn't reconcile it.
2. **Apache-2.0 §4(d) requires it.** The Apache License 2.0 requires that if the distributed Work "includes a NOTICE text file," the redistribution must retain attribution notices. Even where upstream ships none, retaining upstream copyright/attribution when redistributing Apache-2.0 material is the compliant and conventional practice. **Evidence:** the vendored upstream CWS ships `LICENSE` (full Apache-2.0 text, 11357 bytes) but **NO NOTICE file** (verified — `ls NOTICE` in the vendored tree returns nothing). So LAF **authors** the NOTICE to carry the upstream attribution that upstream did not package separately.

**Placement decision — `laf-adaptation/NOTICE` (tree root of the adopted distribution), NOT repo root.** Justification:
- The repo root `LICENSE` is **MIT** (© 2026 Ryan) — LAF's own license. Putting an Apache-2.0 NOTICE at repo root would muddle the repo's own MIT licensing.
- The Apache-2.0 obligation attaches to the **vendored subset**, which lives entirely under `laf-adaptation/`. Co-locating `NOTICE` with `VENDOR.md` and `LICENSE`-equivalent inside `laf-adaptation/` keeps the attribution with the material it covers and matches DESIGN.md:106 (VENDOR.md sits at `laf-adaptation/` root).
- Recommendation: also vendor the upstream **Apache-2.0 `LICENSE`** file into `laf-adaptation/LICENSE` (or `laf-adaptation/LICENSE-CWS`) so the full license text travels with the NOTICE, as Apache-2.0 §4(a) requires distributing a copy of the License. The task should carry this as a companion Phase-0 deliverable.

**Provenance:** `NOTICE` is `NATIVE`-authored (LAF writes it) but its *content* is upstream attribution. Like CLAUDE.md, it is OUTSIDE the `check_boundary.py` rule-F glob (globs only `agents/*.md` + `skills/**/SKILL.md`; boundary-contract.md:147) — no manifest hash row; note it in VENDOR.md prose.

**Authorable `laf-adaptation/NOTICE` skeleton:**

```
LAF Adaptation Framework (laf-adaptation)
=========================================

This distribution contains files vendored, unmodified (apart from a uniform,
deterministic namespace prefix rewrite "creative-writing-skills:" -> "laf-adaptation:"),
from the following upstream project:

    creative-writing-skills
    Upstream repository: https://github.com/haowjy/creative-writing-skills
    Vendored at commit:  <full 40-char upstream_sha — see VENDOR.md>
    Vendored on:         2026-07-03

The vendored files are licensed under the Apache License, Version 2.0.
A copy of the Apache License 2.0 accompanies these files (see LICENSE / LICENSE-CWS
in this directory) and is also available at:

    http://www.apache.org/licenses/LICENSE-2.0

Copyright and attribution for the vendored (ADOPTED) files remain with the
upstream creative-writing-skills authors. See VENDOR.md for the per-file
provenance manifest (which files are ADOPTED vs NATIVE vs BUILD-NEW).

Files marked NATIVE or BUILD-NEW in VENDOR.md are authored by the LAF project
and are NOT covered by this upstream attribution.
```

**Open, execution-time decisions (mark for builder):**
- The exact `upstream_sha` and any upstream copyright-holder name/year are filled in at Phase-0 vendor time (`check_boundary.py --init` records the SHA; the holder name comes from the upstream repo's own NOTICE/README if present — upstream ships none, so attribution is "the creative-writing-skills authors" unless a named holder is found). **Requires execution-time confirmation.**
- Whether to name the vendored license copy `LICENSE` vs `LICENSE-CWS` (avoid collision with any future `laf-adaptation/LICENSE`) — recommend `LICENSE-CWS` for clarity.

**VENDOR.md linkage:** keep line 48 as-is (`attribution retained per NOTICE`); the NOTICE now exists to satisfy that reference.

---

## G3 (IMPORTANT) — `.githooks/pre-commit` + CI wiring (phase conflict RESOLVED)

**Spec anchor:** boundary-contract.md §4 (l.171-181). The enforcement table names TWO blocking points, both running `check_boundary.py`:
- l.175 — `Pre-commit hook (.githooks/pre-commit, opt-in per clone)` → blocking (blocks the commit)
- l.176 — `CI (PR gate)` → blocking (fails the PR)
- l.181 — "Per project rules, LAF uses UV: the pre-commit and CI invocations are `uv run python scripts/check_boundary.py`."

**PHASE PLACEMENT — RESOLVED to Phase 0.** R1 (Phase 4, "optional") is wrong; R5 (Phase 0) is correct. Reasoning:
- The script (`check_boundary.py`) is authored in **Phase 0** (DESIGN.md:293 — Phase 0 runs `check_boundary.py --init`). The wrappers are trivial one-liners that only *invoke* that script; there is no dependency reason to defer them.
- The hook + CI are the *enforcement* of constraint #6 and the #1 residual-risk mitigation (DESIGN §6). Deferring them to Phase 4 leaves the tree unguarded during Phases 1-3, exactly when native/build-new files are being added and an accidental adopted-file edit is most likely. The value proposition is enforcement-from-the-start.
- **Counter-consideration (why not Phase 2):** one could argue the hook should wait until the full tree exists (after greenfield) so rule F ("every agents/*.md + skills/**/SKILL.md is in the manifest") doesn't false-fail on a partial tree. But `--init` re-writes the manifest each phase, and the verify gate only checks files *listed* in the manifest — so a partial tree checks clean as long as the manifest matches what's present. Phase 0 placement is safe. **Recommendation: author both wrappers in Phase 0**, immediately after `check_boundary.py` and `check_boundary.py --init` succeed. (If the builder prefers a conservative split: author the CI workflow in Phase 0 but only *activate* branch protection after Phase 2 — optional, not required.)

**Adopted-pattern evidence.** The upstream CWS already ships this exact pattern (verified):
- `creative-writing-skills/.githooks/pre-commit` — a bash script, `set -uo pipefail`, runs checks, `exit 1` on failure, documents opt-in `git config core.hooksPath .githooks` and `--no-verify` bypass (l.7-8). LAF adapts the *shape*, swapping CWS's cw-sync/plugin checks for the single `check_boundary.py` call.
- `creative-writing-skills/.github/workflows/ci.yml` — `on: [push, pull_request]` to main, `astral-sh/setup-uv@v7`, then validation steps. LAF adapts the shape to one `uv run python scripts/check_boundary.py` step.
- `AGENTS.md` documents the pattern verbatim: *".githooks/pre-commit ... committed but not auto-installed — enable it once per clone: `git config core.hooksPath .githooks`. It blocks the commit on failure; bypass a single commit with `git commit --no-verify`."*

**Repo-root CI fact (verified):** `.github/` exists at repo root but is **EMPTY** — there is **no `.github/workflows/` directory**. The task must **create** `.github/workflows/` and the workflow file. (Do not assume the CWS `.github/` is reused; that lives only inside the vendored subtree.)

**Authorable content — `laf-adaptation/.githooks/pre-commit`:**

```bash
#!/usr/bin/env bash
# Pre-commit hook for laf-adaptation.
# Enforces the boundary contract (constraint #6): proves every ADOPTED file is
# byte-identical to its VENDOR.md manifest hash before allowing a commit.
#
# Enable once per clone:  git config core.hooksPath .githooks
# Bypass a single commit: git commit --no-verify

set -uo pipefail

echo "pre-commit: boundary contract (check_boundary.py)..."
if ! uv run python scripts/check_boundary.py; then
  echo >&2
  echo "pre-commit: boundary check failed. An ADOPTED file was modified, or the" >&2
  echo "manifest is out of date. Fix it, or bypass with 'git commit --no-verify'." >&2
  exit 1
fi

echo "pre-commit: ok."
```

Notes: opt-in (committed, not auto-installed); mark executable (`chmod +x`). If `laf-adaptation/` is a subdirectory of the repo (not the git root), the hook must `cd` to the `laf-adaptation/` dir first, or the `scripts/check_boundary.py` path must be repo-relative — **execution-time detail** depending on whether `laf-adaptation/` == git root. Recommend the hook `cd "$(git rev-parse --show-toplevel)/laf-adaptation"` if nested; otherwise run as-is.

**Authorable content — `.github/workflows/boundary.yml` (create `.github/workflows/` first):**

```yaml
name: Boundary Contract

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check-boundary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v7

      - name: Verify adopted-file boundary contract
        run: uv run python scripts/check_boundary.py
        # working-directory: laf-adaptation   # uncomment if laf-adaptation/ is not the repo root
```

Notes:
- `check_boundary.py` verify mode needs NO `--upstream` checkout (rule B/C recompute against upstream only in `--init`; verify mode A/D/E/F work on the vendored tree + manifest alone — boundary-contract.md:97, §3.2). So CI needs no upstream clone. **Confirm** at execution time that verify mode truly runs without `--upstream` (spec l.97 shows bare `check_boundary.py` as the CI/pre-commit gate, so yes).
- Pin `astral-sh/setup-uv` to the same major the CWS CI used (`@v7`) for consistency; the builder may bump to latest at execution time.
- `working-directory:` is the CI analogue of the hook's `cd` concern — set only if `laf-adaptation/` is nested below the git root.

**Builder placement summary:** Phase 0 deliverables += `laf-adaptation/.githooks/pre-commit` (opt-in, executable) and `.github/workflows/boundary.yml` (new dir). Both are B2-authorable with the exact content above; both invoke `uv run python scripts/check_boundary.py` (satisfying boundary-contract.md:181 UV rule).

---

## G4 (IMPORTANT) — `children.md` source digest (transform prompts + tier profiles READ)

**Spec anchor:** skill-specs.md:276-278 — `resources/children.md` for Tiers 1-3: "prosocial centering, episodic structure, positive resolution, safe-home schema, nightmare-prevention framing, vocabulary/sentence ceilings. Sourced from the tier-1/tier-3 transform prompts and tier profiles."

**Files READ (previously un-opened by any researcher):** `prompts/transformation/tier_1_transform.md` (74 lines), `prompts/transformation/tier_3_transform.md` (64 lines), plus `config/age_profiles/tier_1_preschool.yaml`, `tier_3_middle_elementary.yaml`.

**Digested craft dimensions children.md must carry (each with concrete source content + cite):**

| Dimension (skill-specs term) | Concrete content pulled from source | Cite |
|---|---|---|
| **Prosocial centering** | "Models helping, sharing, kindness." Heroic acts = helping, sharing, comforting, persevering, being kind (T1); adds defending_others, sacrifice (T3). | tier_1_transform.md:9, config tier_1:84-86, tier_3:78-80 |
| **Externalize negative agency** (T1-2 mandatory → T3 optional) | "Badness is always a STATE or ACCIDENT, never innate." Table: "Sauron was evil" → "The Grumpy King was grumpy because his land had no sunshine"; "Gollum attacked" → "The silly creature wanted to play a game". T3: villain motivation "can be internal". | tier_1_transform.md:13-19, config tier_1:62-64, tier_3:63-64,74-76 |
| **Violence → cooperation** (T1) / **weight not gore** (T3) | T1: Battle→Big Tidy-Up, War→Helping Adventure, Attack→making a mess, Enemy army→Noisy messy helpers. T3: "Show stakes and consequences without graphic detail"; battle summarized, injury implied; forbidden graphic_gore/torture/prolonged_suffering. | tier_1_transform.md:21-28, tier_3_transform.md:28-29,47-48, config tier_3:24-28 |
| **Death handling** (euphemism → direct-but-gentle) | T1: died→"went on a new adventure", killed→"needed to rest", dead→"resting" (mandatory journey_or_sleep). T3: "Name death directly. Focus on meaning." can_say: died/death/killed. | tier_1_transform.md:30-37, config tier_1:73-78, tier_3_transform.md:31-32, config tier_3:69-72 |
| **Positive / emotional resolution** | T1: "Every negative emotion resolves positively by chapter end." Permitted: happy/sad/scared/grumpy/tired/excited/brave/kind. Forbidden: despair/trauma/grief/rage. T3: "Hope even in dark content"; "Suffering has purpose"; forbidden "Despair without hope". | tier_1_transform.md:46-50, config tier_1:30-31, tier_3_transform.md:40-51 |
| **Episodic structure** | T1 chapter_structure: `episodic: true`, `requires_positive_resolution: true`, max 800 words. T3: `episodic: false`, permits cliffhangers/subplots/delayed_resolution (so children.md must note the T1-2→T3 shift OUT of strictly-episodic). | config tier_1:56-59, tier_3:56-59 |
| **Safe-home schema** | T1 safety: `safe_home_schema: {requirement: mandatory, if_violated: must_be_restored}`. T1 safety checklist item: "Safe home preserved". | config tier_1:88-91, tier_1_transform.md:67 |
| **Nightmare-prevention framing** | T1 safety: `nightmare_prevention: {monsters: "reframe as grumpy/silly creatures", darkness: "temporary, fixed with sunshine"}`. | config tier_1:92-94 |
| **Vocabulary ceiling** | T1: grade K, max_syllables 2, forbidden [kill,die,dead,evil,wound,blood,weapon]. T2 (interp): between. T3: grade 3-5, can_introduce [grief,betray,sacrifice,honor,destiny]. | config tier_1:46-49, tier_1_transform.md:52-58, tier_3:48-50 |
| **Sentence / chapter ceiling** | T1: max 12 words/sentence, max 1 clause, no passive voice, max 800-word chapter. T3: max 20 words/sentence, max 3 clauses, max 2500-word chapter. | config tier_1:51-57, tier_1_transform.md:52-57, tier_3:52-57 |
| **Worked before/after examples** | T1: "The orcs attacked. Many soldiers fell. Éowyn slew the Witch-king." → "The noisy grumbles made a big mess at the city walls. Many helpers got very tired. Brave Éowyn helped everyone stay safe." T3 Denethor example (tier_3_transform.md:59-63) shows the same scene at T1 vs T3. | tier_1_transform.md:71-73, tier_3_transform.md:59-63 |

**children.md authoring guidance:** it is *authored craft prose* (not a verbatim carry) that synthesizes the above into "how to write children's fiction well across T1-3," organized by the transition arc (T1-2 = protect from complexity → T3 = scaffold complexity; tier_3_transform.md:14). The rubric (safety-rubric.md) *gates*; children.md *informs the writer*. **B2 read-inputs the task item must name:** `prompts/transformation/tier_1_transform.md`, `prompts/transformation/tier_3_transform.md`, `config/age_profiles/tier_1_preschool.yaml`, `config/age_profiles/tier_3_middle_elementary.yaml` (and tier_2 for interpolation of the T1→T3 midpoint).

**ya.md source confirmation (lighter check — DONE).** skill-specs.md:280-282 says ya.md is sourced from "the tier-5 profile's `adaptation_philosophy` + `supplementary_approach`." **CONFIRMED both keys exist** in `config/age_profiles/tier_5_young_adult.yaml`:
- `adaptation_philosophy:` (line 71) — `core_principle: "Adaptation means accessibility, not sanitization."`, plus `when_to_intervene` (archaic language, historical context, obscure cultural references — l.73-76) and `when_not_to_intervene` (difficult themes, moral complexity, character deaths — l.77-80). This maps **exactly** to skill-specs.md:280-281's "when-to-intervene vs when-not-to-intervene" and "meaning-not-sanitization."
- `supplementary_approach:` (line 82) — `recommended:` character guide, timeline, context notes, discussion questions (l.83-87).
- Also present and usable: `narrative_complexity: {unreliable_narrator: true, irony: "full_range"}` (l.38-39) — matches skill-specs.md:281 "unreliable narrator and full irony range permitted." `agency_externalization: {mode: forbidden, reason: "Patronizing; undermines character complexity"}` (l.54-56).

So ya.md is **well-anchored** (its source keys verified present); children.md is the one needing the pre-digest above, now supplied.

---

## G5 (MINOR) — `adaptation-tiers/resources/tier_N.md` commentary count

**Spec anchor:** DESIGN.md:122 — `adaptation-tiers/ (SKILL.md + resources/tier_N.md commentary)`. skill-specs.md §1 (l.80-83) — "`resources/tier_1.md` … `tier_5.md`: design commentary carried from `docs/design_decisions/001-five-tier-system.md` and `003-agency-externalization.md`."

**Tension:** skill-specs.md:80 explicitly names the range `tier_1.md … tier_5.md` (implying **5** commentary files), but there are only **4 stored tier profiles** (`config/age_profiles/tier_{1,2,3,5}_*.yaml` — verified; no `tier_4`), because **Tier 4 is interpolated, never stored** (skill-specs.md:43,73-77; kb-formats §2.4).

**RECOMMENDATION: author 5 commentary files — `tier_1.md, tier_2.md, tier_3.md, tier_4.md, tier_5.md`.** Justification:
1. **skill-specs.md:80 literally writes the range "tier_1.md … tier_5.md"** — the spec's own enumeration includes tier_4.md. This is the strongest ground-truth signal.
2. **Commentary ≠ stored profile.** The "no tier_4.yaml" rule (constraint against a *stored data profile*) does not forbid a *commentary* file. In fact tier_4 is the one tier that most *needs* commentary, because it is the interpolation rule — `tier_4.md` is the natural home to explain "how T4 is derived (T3 floor, T5 ceiling, midpoint rounding toward conservative; agency_externalization inherits T4_5=FORBIDDEN)" (skill-specs.md:73-77). Omitting tier_4.md would leave the single most-confusing tier undocumented.
3. The SKILL.md body itself has a `## Interpolation (Tier 4)` section (skill-specs.md:73-77); `resources/tier_4.md` extends that with the design rationale, consistent with how tier_1.md/tier_3.md extend their SKILL.md rows.

**So: 5 files.** Content sourcing is uniform: `tier_{1,2,3,5}.md` carry the developmental/threshold rationale from `docs/design_decisions/001-five-tier-system.md` + `003-agency-externalization.md` (both verified to exist: 001 ≈1108 B, 003 ≈1576 B). `tier_4.md` carries the interpolation-derivation rationale (sourced from the SKILL.md §Interpolation contract + the T3/T5 profiles it interpolates between). **Guard against the anti-pattern:** tier_4.md must NOT define a stored profile or numeric constant set as if it were canonical — it explains the *derivation*, referencing T3 as floor and T5 as ceiling. Add this as an explicit note in the task item so the executor does not accidentally re-introduce a de-facto tier_4 profile.

**Read-inputs the task item must name:** `docs/design_decisions/001-five-tier-system.md`, `docs/design_decisions/003-agency-externalization.md`, plus (for tier_4.md) the SKILL.md §Interpolation block and `config/age_profiles/tier_3_middle_elementary.yaml` + `tier_5_young_adult.yaml`.

**If the builder prefers minimal surface:** a defensible alternative is 4 files (tier_1/2/3/5.md, mirroring the 4 stored profiles) with the T4 interpolation rationale folded into the SKILL.md §Interpolation section only. This is *acceptable* but weaker — it contradicts skill-specs.md:80's explicit "tier_5.md" range that includes tier_4.md, and it buries the hardest tier's rationale. **Primary recommendation stands at 5.**

---

## G8 (MINOR) — reconciled numeric facts as explicit task Key-Constraints

Compile the reconciled counts so the builder carries them as **Key-Constraints** and they are not re-litigated during execution. Each is verified against the specs (and, where noted, against on-disk files this session).

**Consolidated Key-Constraints (author verbatim into the task file):**

| # | Constraint | Evidence / reconciliation |
|---|---|---|
| KC-1 | **Build 15 agent files total:** 11 ADOPTED + 2 NATIVE + 2 BUILD-NEW. | DESIGN.md §1.1 diagram l.55-67; VENDOR.md manifest lists 11 adopted agent rows (boundary-contract.md:60-70) + analyst/safety-verifier (NATIVE l.74-75) + chronicler/tier-coordinator (BUILD-NEW l.76-77). |
| KC-2 | **11 ADOPTED agents**, of which **5 are dormant on the core adapt path:** brainstormer, outliner, character-sim, style-creator, web-researcher. The other 6 are active: muse, critic, editor, reader-sim, continuity-checker, writer. | DESIGN.md:82 ("web-researcher retained but dormant"), l.110-111 (brainstormer/outliner/character-sim/style-creator/web-researcher marked "dormant"); active set from §3 workflow + §1.2 quartet. |
| KC-3 | **12 ADOPTED skills.** | DESIGN.md §1.1 skill box (l.62-66) enumerates 12: writing-principles, creative-writing-craft, creative-writing-modes, story-review, story-memory, kb-management, shared-dao, llm-writing, writing-staffing, intent-modeling, grill-with-docs, creative-research. Phase 0 (l.293) confirms "12 adopted skills". |
| KC-4 | **16 skill directories total:** 12 ADOPTED + 3 NATIVE (/adaptation-tiers, /adaptation-rules, /source-fidelity) + 1 BUILD-NEW (/adaptation-safety). | DESIGN.md §1.1 header "16 skills" (l.52); native set §1.1 (l.62-63) + l.78 ("4 native skills + 1 build-new… + 2 genre resources"). NOTE the DESIGN prose says "4 native skills" counting /adaptation-safety among them loosely; the provenance-precise split is **3 NATIVE + 1 BUILD-NEW** (VENDOR.md l.78-81 marks adaptation-safety BUILD-NEW). |
| KC-5 | **23 ADOPTED files vendored in Phase 0** = 11 adopted agents + 12 adopted skills. | Sum of KC-1 (adopted agents) + KC-3 (adopted skills). This is the count the VENDOR.md manifest hash-rows must cover (plus each adopted skill's `resources/**`, hashed recursively — boundary-contract.md:87-88). |
| KC-6 | **NO `tier_4.yaml` (or any stored Tier-4 profile).** Tier 4 is interpolated at request time (T3 floor, T5 ceiling, conservative midpoint; agency_externalization = FORBIDDEN via T4_5 bucket). Only tier_{1,2,3,5}.yaml are stored. | skill-specs.md:43, 73-77; kb-formats §2.4; on-disk verified: `config/age_profiles/` has only tier_{1,2,3,5}_*.yaml (no tier_4). A `resources/tier_4.md` *commentary* file is still authored (see G5) — that is NOT a stored profile. |
| KC-7 | **`<work>-mapping.yaml` has 5 top-level keys, not 4** (spec §3.2 prose says "4"; the template has 5). Keys: `work_metadata, characters, concepts, key_scenes, master_translation_table`. | On-disk verified this session: `templates/work_mapping_template.yaml` top-level keys at lines 4,11,39,47,57 = 5 keys. Treat any "4 keys" phrasing as a prose typo; **build to 5**. |

**Provenance-count caveat (surface for builder as a note, not a blocker):** DESIGN.md:70 says "**13 adopted agents/skills** are copied unchanged." This "13" does **not** cleanly decompose against the 11-agent / 12-skill split (11+12=23, not 13). The "13" appears to be a stale/loose figure (possibly an early agents-only-subset count). **Resolution: ignore the "13"; build to KC-1..KC-5 (11 adopted agents, 12 adopted skills, 23 adopted files).** Carry this as an Open-Question note only if the design owner is available; otherwise the manifest counts (boundary-contract.md §2) are authoritative per DESIGN §6 ("build to the boundary-contract manifest").

**Phase-0 "6 agents" reconciliation:** DESIGN.md:293 (Phase 0) says "Copy **6 adopted review/orch agents**". This is the *active* subset (KC-2's 6 active adopted agents), not the full 11 — the 5 dormant agents are also vendored in Phase 0 (they appear in the VENDOR.md manifest and must be hash-pinned). **Resolution: Phase 0 vendors all 11 adopted agents** (manifest requires it); the "6" refers only to the actively-wired review/orchestration set. Build to 11.

---

## Summary — all 6 gaps closed

| Gap | Severity | Resolution | New Phase-0 deliverables / key decision |
|---|---|---|---|
| **G1** | IMPORTANT | Authorable `laf-adaptation/CLAUDE.md` outline supplied (provenance model + boundary note + LAF conventions + 6 constraints). Adopted "pattern" = upstream CLAUDE.md is a `@AGENTS.md` pointer; LAF adopts the *thin-entry-point pattern*, authors native content. Outside check_boundary.py glob. | `laf-adaptation/CLAUDE.md` (Phase 0) |
| **G2** | IMPORTANT | R1/R5 contradiction RESOLVED → **NOTICE IS a required committed Phase-0 file** at `laf-adaptation/NOTICE` (not repo root — repo root is MIT; upstream is Apache-2.0). Upstream ships LICENSE but NO NOTICE, so LAF authors it. Skeleton supplied. Companion: vendor upstream Apache-2.0 license as `laf-adaptation/LICENSE-CWS`. | `laf-adaptation/NOTICE` + `LICENSE-CWS` (Phase 0) |
| **G3** | IMPORTANT | Phase conflict RESOLVED → **hook + CI go in Phase 0** (script exists there; enforcement must guard Phases 1-3). Authorable `.githooks/pre-commit` (opt-in, `uv run python scripts/check_boundary.py`) + `.github/workflows/boundary.yml` supplied. Verified: repo-root `.github/` exists but EMPTY (no workflows/ — must create). | `laf-adaptation/.githooks/pre-commit` + `.github/workflows/boundary.yml` (Phase 0) |
| **G4** | IMPORTANT | Read tier_1/tier_3 transform prompts + tier_1/3/5 profiles (never opened before). 11-dimension digest table for `children.md` with concrete content + line cites. ya.md source keys (`adaptation_philosophy`, `supplementary_approach`) CONFIRMED present in tier_5 yaml. | children.md read-inputs pinned; ya.md anchored |
| **G5** | MINOR | RECOMMEND **5 commentary files** (tier_1/2/3/4/5.md) — spec range says "tier_1.md … tier_5.md"; tier_4.md documents interpolation (must NOT be a stored profile). 4-file fallback noted but weaker. | tier_4.md commentary count decided |
| **G8** | MINOR | 7 reconciled Key-Constraints (KC-1..KC-7): 15 agents (11 adopted incl 5 dormant), 12 adopted skills, 16 skills total, 23 adopted files, NO tier_4.yaml, work-mapping = 5 keys (on-disk verified). "13" and "6 agents" phrasings reconciled as loose/subset figures. | Key-Constraints block for task file |

**Net new Phase-0 file deliverables surfaced by this gap-fill:** `laf-adaptation/CLAUDE.md`, `laf-adaptation/NOTICE`, `laf-adaptation/LICENSE-CWS` (companion), `laf-adaptation/.githooks/pre-commit`, `.github/workflows/boundary.yml`. All are B2-authorable with the content in this file.

**Items requiring execution-time decisions (explicitly flagged, non-blocking):**
1. Exact `upstream_sha` + upstream copyright-holder name in NOTICE (filled at `--init` vendor time).
2. `LICENSE` vs `LICENSE-CWS` filename for the vendored Apache-2.0 copy (recommend LICENSE-CWS).
3. Whether the hook/CI need a `cd`/`working-directory: laf-adaptation` (depends on whether `laf-adaptation/` == git root).
4. Confirm `check_boundary.py` verify mode runs without `--upstream` in CI (spec l.97 indicates yes).
5. tier_N.md commentary count: 5 (recommended) vs 4 (fallback).

**Verification note:** all cites in this file are grounded in files read this session (spec `file:line` + on-disk port-source content). On-disk facts verified 2026-07-03: `.github/` empty; repo LICENSE=MIT; vendored CWS has LICENSE(Apache-2.0)+no NOTICE+`.githooks/pre-commit`+`.github/workflows/{ci,release}.yml`; `config/age_profiles/` = tier_{1,2,3,5} only; `templates/work_mapping_template.yaml` = 5 top-level keys.
