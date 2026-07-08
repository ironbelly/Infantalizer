# QA Report — BOUNDARY-CONTRACT-FIDELITY (Phase-0 LAF)

**Topic:** laf-adaptation/ boundary-contract enforcement gate (adopted CWS subset fidelity)
**Date:** 2026-07-03
**Phase:** doc-qualitative (adapted: structural boundary-contract fidelity / zero-trust gate audit)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Lens:** BOUNDARY-CONTRACT-FIDELITY — the ACTUAL enforcement gate, run + independently spot-checked

---

## Overall Verdict: PASS

Adversarial stance assumed >=5 latent violations (adopted body byte-change, missing manifest row, writer body edit, folded editor). **None found.** The boundary gate is real, its logic is sound (script read in full, not trusted blind), and every rule was independently reconfirmed by recomputing sha256 hashes outside the script. Zero violations.

---

## Step 1 — Run the enforcement gate (both modes)

| Mode | Command | Exit code | Output |
|------|---------|-----------|--------|
| default (A, D, E, F) | `uv run python laf-adaptation/scripts/check_boundary.py` | **0** | `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` (with NOTE that B/C skipped w/o --upstream) |
| full A-F (+B/C) | `...check_boundary.py --upstream .../creative-writing-skills` | **0** | `BOUNDARY CONTRACT: PASS — all rules (A-F) satisfied.` |

Both exit 0. The script was READ in full (459 lines) before trusting it — zero-trust on the gate itself. Script logic is genuinely rigorous (see Script-integrity audit below).


---

## Script-integrity audit (zero-trust on the gate itself)

The script (`check_boundary.py`, 459 lines) was READ IN FULL before trusting its exit code, because an adversary could weaken the checker rather than the data. The logic is genuinely rigorous:

- **Rule A** (L327-335): every adopted file's on-disk sha256 must equal recorded `laf_sha256`. Catches ANY edit.
- **Rule B** (L338-348): each ADOPTED-CLEAN `laf_sha256` must equal `sha256(prefix_rewrite(upstream_blob))`. `prefix_rewrite` is RECOMPUTED from the live upstream file, never read from a stored diff (L69-73).
- **Rule C** (L351-369): writer.md body must be byte-identical to `body_of(prefix_rewrite(upstream))`; frontmatter diff must be additive-only and every added line must start with `- laf-adaptation:`. Order-insensitive set semantics correctly preserve the duplicate craft line.
- **Rule D/G3** (L376-380): quartet {critic,editor,reader-sim,continuity-checker} must each be present AND classed ADOPTED-CLEAN — editor cannot be folded.
- **Rule E** (L383-398): no NATIVE/BUILD-NEW row may shadow an upstream file name.
- **Rule F** (L401-403): every `agents/*.md` and `skills/**/SKILL.md` on disk must be manifest-covered.

No weakening, no short-circuit, no hard-coded PASS, no swallowed exception was found in the checker. The `prefix_rewrite` recompute-not-trust design is exactly what a fidelity gate should do.

---

## Independent verification (NOT the script — recomputed by hand)

An independent Python pass (own manifest parser, own sha256, own prefix rewrite — no import of `check_boundary`) was run over the entire manifest:

- **Rule A independently:** all **56** manifest rows — disk sha256 == recorded `laf_sha256`. PASS.
- **Rule B independently:** all **55** ADOPTED-CLEAN rows — `sha256(prefix_rewrite(upstream_raw))` == recorded `laf_sha256`. PASS. Additionally re-derived: `sha256(upstream_raw)` == recorded `upstream_sha256` for all 55 (a chain the script itself does NOT verify — extra zero-trust layer). PASS.

### Spot-check 2a — ADOPTED-CLEAN `agents/muse.md` (recomputed hashes)

| Quantity | sha256 |
|----------|--------|
| `sha256(prefix_rewrite(upstream cw/agents/muse.md))` | `18cafdc251a528f0186d2d74135ae94cad0d05d37d2bf8f399a134969409af8f` |
| vendored `laf-adaptation/agents/muse.md` | `18cafdc251a528f0186d2d74135ae94cad0d05d37d2bf8f399a134969409af8f` |
| manifest `laf_sha256` | `18cafdc251a528f0186d2d74135ae94cad0d05d37d2bf8f399a134969409af8f` |

All three IDENTICAL (Rule B holds). The prefix rewrite genuinely fired: upstream had 16 `creative-writing-skills:` occurrences; vendored file has 16 `laf-adaptation:` occurrences, 0 residual `creative-writing-skills:`.

### Spot-check 2b — ADOPTED-PATCHED `agents/writer.md` (body + frontmatter diff)

- **Body:** byte-identical to `body_of(prefix_rewrite(upstream cw/agents/writer.md))`. PASS (no writer body edit).
- **Frontmatter ADDED:** exactly `['  - laf-adaptation:adaptation-rules']` — one line, the authorized additive skill.
- **Frontmatter REMOVED:** `[]` — nothing removed (additive-only holds).
- **Duplicate `creative-writing-craft` line:** upstream carries it twice; vendored file preserves it twice verbatim (not "fixed"). PASS.

### Spot-check 2c — quartet {critic, editor, reader-sim, continuity-checker}

| Agent | On disk | Manifest class |
|-------|---------|----------------|
| critic.md | yes (1680 B) | ADOPTED-CLEAN |
| editor.md | yes (1935 B) | ADOPTED-CLEAN |
| reader-sim.md | yes (340 B) | ADOPTED-CLEAN |
| continuity-checker.md | yes (1549 B) | ADOPTED-CLEAN |

**editor NOT folded:** `diff <(prefix_rewrite(upstream editor.md)) laf editor.md` → IDENTICAL. editor.md is a standalone ADOPTED-CLEAN file, not merged/folded into any other agent. G3 invariant holds.

### Break-it attempt 3 — search adopted agent BODIES for injected native content

Regex `adaptation|active_tier|tier|safety-verifier|source-fidelity|chronicler|tier-coordinator|analyst` (case-insensitive) run against the BODY (post-second-`---`) of all 11 adopted agents: **0 hits.** All `laf-adaptation:` grep matches in the raw files are frontmatter `skills:` entries (legitimate prefix-rewrite output). The only native-skill reference anywhere is `writer.md` frontmatter line `- laf-adaptation:adaptation-rules` — the single authorized ADOPTED-PATCHED addition. No native tier/adaptation content leaked into any adopted body.

---

## Phase-0 scope observation (NOT a violation)

The disk tree contains ONLY the adopted subset: 11 adopted agents (writer.md = ADOPTED-PATCHED) and 12 adopted skill dirs. The 4 NATIVE/BUILD-NEW agents (analyst, safety-verifier, chronicler, tier-coordinator) and 4 NATIVE/BUILD-NEW skills (adaptation-tiers, adaptation-rules, source-fidelity, adaptation-safety) that CLAUDE.md's target-state prose describes are **not yet on disk** — consistent with "Phase-0 LAF." Correspondingly, VENDOR.md's manifest has **zero** NATIVE/BUILD-NEW rows.

This is internally consistent and NOT a Rule-F gap: Rule F only requires files PRESENT ON DISK to be manifest-covered, and Rule E's collision check has nothing to collide. writer.md references `adaptation-rules` which does not exist on disk yet — a forward reference to a future-phase skill, not a boundary-contract violation (the gate does not require referenced skills to exist). Flagged here for the orchestrator's awareness of build phase, not as a defect of the boundary gate under review.

---

## Self-Audit

**(a) Reliance list — items where the script's PASS was accepted for structure:**
- Relied on the script's exit-0 for Rules D (quartet present/classed), E (no collision), F (manifest coverage) as the structural baseline — then independently reconfirmed D by disk+manifest-class spot-check (2c), E by noting zero NATIVE/BUILD-NEW rows on disk, F by enumerating disk agents/SKILL.mds against the 56 parsed rows.

**(b) Independent semantic checks (>=1 required) — where the script PASS was insufficient and own tool work was required:**
- **Rule A/B recomputed outside the script:** own sha256 + own prefix rewrite over all 56 rows (disk==laf_sha256) and all 55 ADOPTED-CLEAN rows (rewrite(upstream)==laf_sha256) — evidence: independent Python pass, no `check_boundary` import. Also verified the raw-upstream→recorded-`upstream_sha256` chain, which the script does NOT check.
- **muse.md tri-hash equality** recomputed by hand (2a) — the script trusts the manifest; I recomputed `prefix_rewrite(upstream)` sha256 fresh and confirmed == vendored == manifest.
- **writer.md body byte-diff** recomputed by hand (2b) — split frontmatter/body independently, confirmed body byte-identical and exactly one additive frontmatter line.
- **editor-fold `diff`** run directly (2c) — proved editor.md == prefix_rewrite(upstream editor.md), no fold.
- **native-content body grep** (break-it 3) — regex over post-`---` bodies of all 11 adopted agents, 0 hits.
- **Script-integrity read** — read all 459 lines of the checker to confirm no weakened/hard-coded PASS.

---

## Confidence
- Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Checks: (1) run default gate, (2) run full A-F gate, (2a) muse hash, (2b) writer body/fm, (2c) quartet+editor-fold, (3) native-content grep, plus (A) independent Rule A recompute, (B) independent Rule B recompute, (S) script-integrity read.

## Tool engagement
- Read: 3 (check_boundary.py, VENDOR.md, CLAUDE.md via system context) | Grep: (via Bash grep) 2 | Glob: (via Bash ls/find) 4 | Bash: 8

---

## Issues Found
None. No CRITICAL, IMPORTANT, or MINOR boundary-contract violations. The Phase-0 scope observation above is informational (build-phase awareness), not a gate defect.

## QA Complete
