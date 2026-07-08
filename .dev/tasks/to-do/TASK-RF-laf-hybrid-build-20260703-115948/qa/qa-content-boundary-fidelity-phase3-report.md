# QA Report — Content Boundary-Contract-Fidelity (Phase 3 proof run)

**Topic:** LAF hybrid build — Phase-3 proof-run boundary & canon fidelity
**Date:** 2026-07-04
**Phase:** doc-qualitative (BOUNDARY-CONTRACT-FIDELITY lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE — REPORT ONLY
**Stance:** Adversarial / zero-trust. Prior expectation: ≥5 boundary/canon breaches.

---

## Overall Verdict: PENDING

_(Filled in after all four steps complete.)_

---

## Step-by-Step Evidence

### Step 1 — `check_boundary.py` exit codes (adopted-file drift check)

| Invocation | Rules exercised | Output | Exit |
|---|---|---|---|
| `uv run python laf-adaptation/scripts/check_boundary.py` | A (hash-match), D, E, F. B/C skipped (no `--upstream`) | `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` | **0** |
| `... --upstream .dev/releases/current/0.1/creative-writing-skills` | A–F including B/C (upstream-diff) | `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` | **0** |

- Upstream checkout `.dev/releases/current/0.1/creative-writing-skills` confirmed present (contains `agents/`, `AGENTS.md`, `.claude/`, etc.).
- The `--upstream` run activates Rules B and C (upstream byte-diff of adopted files). Both PASS → **no adopted file drifted from the vendored upstream during the Phase-3 proof run.**
- The default run's Rule A (hash-match against recorded manifest) also PASS → adopted-file bytes match the manifest hashes recorded at vendor time.
- **Result: PASS.** Exit 0 on both invocations. No adopted-body drift detected.

### Step 2 — Chronicler invariant (Inv.3: no tier-transformed name in shared canon/timeline)

Target files located under `laf-adaptation/kb/` (not repo-root `kb/` — the whole kb tree lives inside `laf-adaptation/`; instruction paths are relative to that root).

**2a. Transformed names must be ABSENT from shared source-truth layers:**

| File | grep `Grumpy King|Sad Leader|Grumpy Riders|Big Tidy` | Result |
|---|---|---|
| `kb/canon/tolkien/ch-01.md` | 0 matches (grep exit 1) | **ABSENT ✓** |
| `kb/timeline/tolkien.md` | 0 matches (grep exit 1) | **ABSENT ✓** |

Read-through confirms both shared files carry **source names only** (Sauron, Denethor, Théoden, Éowyn, Nazgûl) and both carry an explicit Inv.3 header ("no tier-transformed rendering may appear here"). Not empty, not stubbed, correctly tier-neutral.

**2b. Transformed names must be PRESENT under tier-1 (grep exit 0):**

All four transformed names found under `kb/adaptations/tolkien/tier-1/` across `decisions.md`, `chapters/ch-01/canon-delta.md`, `chapters/ch-01/adapted.md`, and `continuity.md` — e.g. `adapted.md:1 "The Big Tidy-Up at the Grey City"`, `continuity.md:8 "The Grumpy King"`, `continuity.md:16 "The Grumpy Riders"`, `decisions.md:6 "Sad Leader"`. Transformations correctly quarantined to tier-1.

- **Result: PASS.** Chronicler invariant (Inv.3) holds. Transformed names live ONLY in tier-1; shared canon/timeline are source-name-only.

### Step 3 — Cross-tier bleed check

| Scope | grep for tier-1 transformed names | Result |
|---|---|---|
| `kb/adaptations/tolkien/tier-3/continuity.md` | 0 matches (exit 1) | **clean ✓** |
| `kb/adaptations/tolkien/tier-3/` (full subtree) | 0 matches (exit 1) | **clean ✓** |
| `kb/adaptations/tolkien/tier-5/` (full subtree) | 0 matches (exit 1) | **clean ✓** |

Zero-trust positive check (files are genuinely populated, not vacuously clean): read both `tier-3/chapters/ch-01/adapted.md` and `tier-5/chapters/ch-01/adapted.md`. Each is a full, tier-appropriate rendering using **source names** (Sauron, Denethor, Théoden, Éowyn, Nazgûl) — correct, because agency-externalization / name-transformation is a **tier-1 MANDATORY** transform and is **FORBIDDEN at T5** (T5 preserve_original policy verbatim in the file header). T3 is the transition tier with real stakes and deaths intact. No tier-1 lexicon bleeds into T3 or T5.

- **Result: PASS.** No cross-tier bleed. Tiers are genuinely distinct and each correctly scoped.

### Step 4 — No adopted agent/skill body edited during proof run

- `check_boundary.py` **Rule A** (adopted-hash match vs recorded manifest) PASS on both runs → adopted `agents/*.md` + `skills/**/SKILL.md` bodies byte-match the manifest.
- `--upstream` run adds **Rule B** (ADOPTED-CLEAN == upstream-after-prefix-rewrite) and **Rule C** (writer.md diff is frontmatter-only + additive) — both PASS.
- Adopted-file counts match completed-tree target: **15 agent files, 16 skill dirs** present; VENDOR manifest carries hashed rows for the adopted subset.
- **Independent hash spot-check (not trusting the script's self-report):** live `sha256sum agents/editor.md` = `2645f358fdc0f6b011479fa27195ba096c3836d2c6c4e7955bd78c1da82410e3`, **byte-exact** to the `laf_sha256` manifest column. G3 invariant ("editor.md NEVER folded, NEVER modified") independently confirmed.

- **Result: PASS.** No adopted body drift. Rule A/B/C green + independent hash match.

---

## Overall Verdict: **PASS**

All four boundary/canon-fidelity checks pass under adversarial, zero-trust verification. The Phase-3 proof run introduced **zero** boundary or canon breaches:

- No adopted-body drift (exit 0 on both `check_boundary.py` invocations; independent editor.md hash match).
- No transformed-name leak into shared canon/timeline (Inv.3 holds).
- No cross-tier bleed (T3/T5 clean of tier-1 lexicon; each tier genuinely populated and correctly scoped).

**The adversarial prior (≥5 breaches expected) was NOT confirmed by evidence.** Every candidate breach surface named in the spawn brief — adopted-body drift, transformed name leaked to shared canon, cross-tier bleed — was directly tested and found clean. This is reported honestly: the proof run is genuinely clean, not under-inspected.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | **None.** Zero boundary/canon breaches found. | — |

_Note on the one path discrepancy (informational, not a defect): the spawn brief referenced shared files as `kb/canon/tolkien/ch-01.md` and `kb/timeline/tolkien.md`; the actual repo root for the kb tree is `laf-adaptation/kb/...`. The files exist and were verified at the corrected paths. This is a brief-vs-repo path-rooting note, not a content breach._

## Actions Taken

None — `fix_authorization: FALSE` (report only). No files modified.

## Self-Audit

**Factual claims independently verified against source (not relied upon from the script's self-report):**
1. `check_boundary.py` exit codes — ran both invocations myself; observed exit 0 (`echo $?`) directly.
2. Upstream checkout existence — `ls` confirmed `.dev/releases/current/0.1/creative-writing-skills` present.
3. Transformed-name ABSENCE in shared canon/timeline — independent `grep -nE` (exit 1 both files).
4. Transformed-name PRESENCE in tier-1 — independent `grep -rnE` (exit 0, 13 hits enumerated).
5. Cross-tier cleanliness — independent `grep -rnE` over tier-3 and tier-5 subtrees (exit 1 all).
6. Tier files genuinely populated — Read tier-3 + tier-5 `adapted.md` in full (positive check against vacuous-pass).
7. Shared files source-name-only — Read `ch-01.md` + `tolkien.md` in full; confirmed Inv.3 headers.
8. Adopted-body integrity — computed live `sha256sum agents/editor.md`, byte-matched `laf_sha256` manifest column (did NOT merely trust Rule A's PASS).

**Files Read (not just grepped):** `check_boundary.py` (header), `kb/canon/tolkien/ch-01.md`, `kb/timeline/tolkien.md`, `tier-3/chapters/ch-01/adapted.md`, `tier-5/chapters/ch-01/adapted.md`, `laf-adaptation/CLAUDE.md` (provenance model), `VENDOR.md` (manifest rows).

**Why trust a 0-issue verdict here:** the verdict does not rest on the script reporting PASS. Every gate was re-derived with my own tools — I re-grepped the invariants the script does not directly assert (chronicler Inv.3, cross-tier bleed), I read the shared + tier files to rule out vacuous passes (empty/stubbed files would also grep-clean), and I re-hashed an adopted body by hand to confirm Rule A wasn't a false green. The candidate breach surfaces were tested, not assumed absent.

**No web research performed** — this review is entirely local-file-bound (adopted-file hashes, kb canon/tier files). Tavily-first precedence not triggered; nothing to record in a tool-engagement fallback line.

## Confidence Gate

- **Confidence:** Verified: 4/4 steps | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 4 (+CLAUDE.md/VENDOR via reminders) | Grep: 5 grep invocations | Bash: 9 | Glob: 0 (used `find`/`ls` via Bash)
- All 4 steps VERIFIED with cited tool output. No UNCHECKED, no UNVERIFIABLE items.

## QA Complete
