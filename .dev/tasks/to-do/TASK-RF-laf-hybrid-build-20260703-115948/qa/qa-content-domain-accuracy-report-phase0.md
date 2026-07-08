# QA Report — Domain-Accuracy Lens (Phase-0 Vendored Tree vs Design Intent)

**Topic:** LAF 0.1 Phase-0 vendored tree vs DESIGN.md §1.1 / §2
**Date:** 2026-07-03
**Phase:** doc-qualitative (DOMAIN-ACCURACY lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE (report only)
**Spec:** `.dev/releases/current/0.1/design/DESIGN.md` (§2 distribution layout; §1.1 component inventory)
**Tree:** `laf-adaptation/`

---

## Overall Verdict: PASS

The Phase-0 vendored tree is domain-accurate against DESIGN.md §1.1 and §2. The agent census
(11 ADOPTED), skill census (12 ADOPTED), and phase-boundary discipline (all NATIVE + BUILD-NEW
artifacts correctly absent) match the spec exactly, verified file-by-file against disk. Zero
errors of any severity.

The adversarial mandate assumed ≥5 domain-accuracy errors (wrong agent count, missing
web-researcher, wrongly-vendored chronicler, wrong distribution layout). I ran each down with
zero-trust tool evidence. **None materialized** — the tree is correct. See the census tables and
the "Adversarial hypotheses — all refuted" section for the evidence trail.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Distribution layout (agents/ skills/ kb/ work/ scripts/ + root files) | PASS | `ls -la laf-adaptation/`: agents/, skills/, kb/, work/, scripts/ all present; root files VENDOR.md, NOTICE, LICENSE-CWS, CLAUDE.md all present. Matches DESIGN.md §2. |
| 2 | 11 adopted agents = exactly the §1.1-named set; web-researcher vendored | PASS | `ls agents/*.md \| wc -l` = 11; set-difference check found no strays and no missing. web-researcher.md present (Read: valid frontmatter, CWS 11th agent, `model: sonnet`, `/creative-research`). |
| 3 | chronicler / tier-coordinator / analyst / safety-verifier NOT yet present | PASS | Per-file existence probe: all four report `absent`. Correct — chronicler + tier-coordinator are Phase-2 BUILD-NEW; analyst + safety-verifier are Phase-1 NATIVE. |
| 4 | 12 adopted skills present; native/build-new skills NOT present | PASS | `ls -d skills/*/ \| wc -l` = 12; intended-12 all `OK`, no unexpected dirs. adaptation-tiers/-rules/source-fidelity/adaptation-safety all `absent` (Phase 1/2). |

---

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (report-only)

---

## Agent Census vs Spec (DESIGN.md §1.1)

**Disk — `agents/` (11 files, ADOPTED):**

| # | Agent | On disk | Spec provenance (§1.1) | Verdict |
|---|-------|---------|------------------------|---------|
| 1 | muse | ✔ | ADOPTED | ✔ |
| 2 | critic | ✔ | ADOPTED (quartet) | ✔ |
| 3 | editor | ✔ | ADOPTED (quartet, never folded G3) | ✔ |
| 4 | reader-sim | ✔ | ADOPTED (quartet) | ✔ |
| 5 | continuity-checker | ✔ | ADOPTED (quartet) | ✔ |
| 6 | brainstormer | ✔ | ADOPTED (dormant on core path) | ✔ |
| 7 | outliner | ✔ | ADOPTED (dormant) | ✔ |
| 8 | character-sim | ✔ | ADOPTED (dormant) | ✔ |
| 9 | style-creator | ✔ | ADOPTED (dormant) | ✔ |
| 10 | web-researcher | ✔ | ADOPTED — **CWS 11th agent, retained/dormant** (§1.1 provenance note) | ✔ |
| 11 | writer | ✔ | ADOPTED-PATCHED (adaptation mode via `skills:` frontmatter) | ✔ |

**Correctly ABSENT (not Phase-0 scope):**

| Agent | Provenance | Phase | On disk | Verdict |
|-------|-----------|-------|---------|---------|
| analyst | NATIVE | 1 | absent | ✔ correct |
| safety-verifier | NATIVE | 1 | absent | ✔ correct |
| chronicler | BUILD-NEW ("unshipped vapor in both systems", §1.1 note) | 2 | absent | ✔ correct |
| tier-coordinator | BUILD-NEW | 2 | absent | ✔ correct |

Agent count = 11, exactly matching the ADOPTED column of §1.1. Zero strays, zero missing.

---

## Skill Census vs Spec (DESIGN.md §1.1 / §2)

**Disk — `skills/` (12 dirs, ADOPTED):**

writing-principles · creative-writing-craft · creative-writing-modes · story-review ·
story-memory · kb-management · shared-dao · llm-writing · writing-staffing · intent-modeling ·
grill-with-docs · creative-research

All 12 intended skills present (`OK`); zero unexpected dirs.

**Correctly ABSENT (not Phase-0 scope):**

| Skill | Provenance | Phase | On disk | Verdict |
|-------|-----------|-------|---------|---------|
| adaptation-tiers | NATIVE | 1 | absent | ✔ correct |
| adaptation-rules | NATIVE | 1 | absent | ✔ correct |
| source-fidelity | NATIVE | 1 | absent | ✔ correct |
| adaptation-safety | BUILD-NEW | 2 | absent | ✔ correct |

---

## Adversarial Hypotheses — All Refuted

The spawn seeded five specific error hypotheses. Each was tested against disk and refuted:

1. **"A wrong agent count"** — REFUTED. `agents/*.md` = 11, matching §1.1 ADOPTED column exactly.
2. **"A missing web-researcher"** — REFUTED. `agents/web-researcher.md` present; Read confirms it
   is the real CWS 11th agent (valid Claude-lowered frontmatter, `/creative-research` skill,
   WebSearch/WebFetch tools). VENDOR.md line 27 manifests it as ADOPTED-CLEAN.
3. **"A wrongly-vendored chronicler"** — REFUTED. `agents/chronicler.md` does NOT exist. Consistent
   with §1.1 provenance note ("unshipped vapor in both `cw/agents/` and `agents/`") and Phase-2
   scope. It is correctly absent, not wrongly vendored.
4. **"A wrong distribution layout"** — REFUTED. §2 top-level dirs agents/ skills/ kb/ work/
   scripts/ and root files VENDOR.md/NOTICE/LICENSE-CWS/CLAUDE.md all present and correctly placed.
5. **(Implied) native/build-new leakage into Phase 0** — REFUTED. All 4 native/build-new agents
   and all 4 native/build-new skills are absent, respecting the Phase-0 → Phase-1/2 gate.

---

## Non-Error Observations (documented for honest record — NOT findings)

These are spec-vs-tree observations that are **correct by phase-scoping**, surfaced so the audit
trail is complete and a later reviewer does not mistake them for gaps:

- **`source/` and `templates/` absent at root.** DESIGN.md §2 shows both in the *full* target
  tree. `source/` is BUILD-NEW (the work being adapted) and `templates/work-mapping-template.yaml`
  is NATIVE (carried in Phase 1). Both are correctly out-of-scope for Phase-0 vendoring. Not an
  error; these are populated in later phases.
- **`kb/tiers/`, `kb/adaptation-mapping/`, `kb/adaptations/` absent.** These are NATIVE kb layers
  (Phase 1). The ADOPTED base layers (`kb/canon/ characters/ world/ timeline/ styles/ vocab.md
  issues/`) ARE present, exactly matching the ADOPTED portion of §2. Correct.
- **`work/analysis/` and `work/safety-reports/` absent; `work/drafts/` + `work/critique-reports/`
  present.** The two absent subdirs are NATIVE (Phase 1). The two present are ADOPTED lifecycle.
  Correct phase split per §2 / constraint #5.
- **CLAUDE.md line 66 / 67 self-describe the tree as "15 agent files / 16 skill dirs".** These
  counts describe the *final* built state (11 ADOPTED + 2 NATIVE + 2 BUILD-NEW agents = 15; 12 + 3
  + 1 skills = 16), NOT the Phase-0 vendored state. This is a forward-looking doc convention, not a
  count error against the current tree. Consistent with §1.1's "11 agents, 16 skills" framing.
- **`writer.md` preserves the upstream duplicate `creative-writing-craft` skill line** (lines 7–8)
  plus the single additive `- laf-adaptation:adaptation-rules` (line 12). This is the intended
  ADOPTED-PATCHED behavior per CLAUDE.md §2 ("even upstream quirks … preserved verbatim, not
  fixed"). Correct, not a defect.

---

## Self-Audit

**How many factual claims independently verified against source/disk:** All 4 checks + both
census tables were verified with direct tool evidence (no reliance on the tree's own assertions).
Specifically: 11-agent count (ls + wc + set-difference), 12-skill count (ls + wc +
set-difference), 4 absent agents (per-file existence probe), 4 absent skills (per-file existence
probe), web-researcher authenticity (Read of frontmatter + VENDOR.md manifest line), writer
ADOPTED-PATCHED shape (Read), distribution layout (ls -la root + kb/ + work/ + scripts/).

**Specific files read:** DESIGN.md (full), CLAUDE.md (full, via system context), VENDOR.md
(full manifest), agents/web-researcher.md, agents/reader-sim.md, agents/character-sim.md,
agents/writer.md. Plus directory listings of laf-adaptation/, agents/, skills/, kb/, work/,
scripts/.

**Why trust a 0-error verdict:** The adversarial stance was applied — I did not accept the tree at
face value. Each of the 5 seeded error hypotheses was independently probed against disk and
refuted with cited evidence (see "Adversarial Hypotheses — All Refuted"). The census was checked
bidirectionally: every spec-named artifact confirmed present, AND a set-difference scan confirmed
no unexpected strays exist. Phase-boundary correctness was verified by proving the 8 Phase-1/2
artifacts are absent, not merely by confirming the Phase-0 set is present. A single-direction check
("are the 11 there?") would have missed a stray; the bidirectional check did not.

**Web research:** None performed. All checks were local-file-bound (tree vs spec). Tavily-first
policy not triggered.

**Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 4 (ls/wc/set-difference/existence-probe
composites). Total tool calls (9) ≥ checks (4). Not suspect.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

---

## Recommendations

- Proceed. Phase-0 vendored tree is domain-accurate against DESIGN.md §1.1 and §2. Green light for
  Phase-1 native-spine authoring.
- (Advisory, out-of-lens) The `check_boundary.py --init` hash-verification gate (DESIGN.md Phase-0
  gate) is a separate structural check; this DOMAIN-ACCURACY lens confirms the *census and layout*
  are correct but does not re-run the SHA-256 manifest verification — that belongs to the
  structural rf-qa pass.

## QA Complete
