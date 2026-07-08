# Tier-2 Independent Audit — TASK-remediation-check-boundary-hardening-20260704-172254

**Verdict: FAIL — material unresolved deviations; downstream adversarial scoring warranted.**

The task self-reports Phases 1–5 + 6.1–6.3 complete with 25/25 tests green, but the artifact contains several evidence gaps, one acknowledged-but-unmitigated H1 residual, and an unfinished independent gate (6.4). Findings below.

---

## F-1 [HIGH] — H1 "trust-root" only partially closed; absolute guarantee silently deferred

**Evidence (target text):**
- "Resolutions → OQ-1": *"writer.md does NOT get a Mode-V `upstream_sha256` re-anchor; its absolute guarantee remains Mode-U Rule C ... a documented conditional, not an over-claim."*
- "Phase 4 Follow-Up Items → F1": *"strengthen CI to Mode U ... Delivers the absolute upstream-anchored guarantee. Recommended next cycle."*
- "Phase 6.3 lens-fix F2": *"CH-1 two-field forgery (mutate body + rewrite BOTH hashes self-consistent) passes Mode V — inherent to option (a)"* — only mitigated by demoting doc language.

**Drift / unresolved decision:**
The H1 finding in the source review was "the CI trust root is the PR-controlled manifest". After remediation:
- For ADOPTED-CLEAN: single-field `laf_sha256` forgery is now caught ✓
- For ADOPTED-CLEAN: two-field (`laf_sha256` + `upstream_sha256`) forgery **still passes** ✗
- For ADOPTED-PATCHED (`agents/writer.md`): **not re-anchored at all** in Mode V ✗
- Absolute guarantee for either: deferred to Mode U / F1 ✗

The remediation ships a *weaker* guarantee than H1 demanded, and the "absolute" guarantee is moved to a deferred follow-up. This is a legitimate engineering trade-off, but it should have surfaced as an explicit re-scope of H1 → M-level partial, not a "PASS" DoD line.

**Concrete demand for scorer:** verify that `VENDOR.md` header, `CLAUDE.md` §2, and `boundary.yml` header **do not** contain the phrase "malicious-drift gate" anywhere, and that the two-field-forgery residual is called out in **all three** docs (not just one).

**Suspect-source file:** `laf-adaptation/scripts/check_boundary.py` (Rule A′ block), `laf-adaptation/VENDOR.md` (header prose), `laf-adaptation/CLAUDE.md` §2, `.github/workflows/boundary.yml:3-7`.

---

## F-2 [HIGH] — Empirical claim underlying CH-1's correctness is asserted, not reproducible from artifact

**Evidence (target text):**
- "Resolutions → OQ-1": *"The mathematically-correct re-anchoring uses the **INVERSE** transform ... Empirically verified for brainstormer.md (`aa736c5d…` ✓) and holds generally (for files without the literal, the inverse is a no-op and `disk==raw`, laf_sha256==upstream_sha256)."*
- "Phase 3 Findings": *"The spec §4.1/§6 Q1 raw-vs-rewritten ambiguity was resolved *empirically*, and the formula first recorded in OQ-1 was WRONG."*

**Missing verification:**
1. Only **one** file (brainstormer.md) is cited with a hash prefix. No table of `sha256(prefix_unrewrite(disk))` vs `r.upstream_sha256` for all 55 ADOPTED-CLEAN rows. The claim "holds generally" is unverified for any file other than brainstormer.md.
2. The premise `disk == prefix_rewrite(raw_upstream)` requires that prefix-rewrite was the **only** transformation between upstream and disk. If any ADOPTED-CLEAN row also received trailing-newline normalization, line-ending changes, or BOM stripping, the inverse won't recover raw bytes. No evidence rules this out across the 55-row corpus.
3. The "CORRECTION" narrative (spec formula was WRONG, fixed empirically) is a known smell: it suggests the implementer ran the code, saw failures, and reverse-engineered a formula that passes — without independently confirming the transformation contract.

**Concrete demand for scorer:** require a side-channel artifact (e.g. `qa/inverse-rewrite-verification.csv`) showing `path, upstream_sha256, sha256(prefix_unrewrite(disk))` for all 55 ADOPTED-CLEAN rows. If absent, treat CH-1 as unverified.

**Suspect-source file:** `laf-adaptation/scripts/check_boundary.py` (`prefix_unrewrite` helper + Rule A′ comparison site).

---

## F-3 [MED] — Status / completion-state drift

**Evidence:**
- Frontmatter: `status: "🟠 Doing"`
- Phase checkboxes: 1.1–6.3 all `[x]`; 6.4 and 6.5 `[ ]`
- "Definition-of-Done sign-off": all 7 points marked PASS
- 6.4 explicitly requires `superclaude reflect run` exit 0 before 6.5

**Drift:** The task self-certifies DoD satisfied while the canonical independent gate (6.4) is explicitly incomplete and `reflect_post:` is absent from the frontmatter (the target's own frontmatter lacks the field entirely, despite the inline directive "leave room, do NOT hand-author or lock"). DoD point 5 ("OQ-1–OQ-4 resolved + recorded") is marked PASS — but OQ-1's resolution is "ship a weaker Mode-V floor and defer the absolute guarantee to F1", which is a **re-scope**, not a resolution of the original question ("is upstream_sha256 raw or rewritten?").

**Suspect-source file:** the task file itself; downstream scorer should treat any `🟢 Done` transition attempted without a populated `reflect_post:` as a hard block.

---

## F-4 [MED] — F1 fix introduces a new write path to VENDOR.md not in original CH scope

**Evidence (target text, Phase 6.3):**
- *"FIX: `do_init` now writes the checkout HEAD into the VENDOR.md `upstream_sha:` header (via `_write_upstream_sha_header`) before the post-write `verify()`"*

**Regression risk:** `do_init` is the re-vendor entry point. Adding a header-rewrite step means `--init` now mutates a file the same invocation then verifies. Failure modes not addressed in the artifact:
1. What if the existing header has a different format (e.g., `upstream_sha :` with a space, or `Upstream-SHA:`)? `_write_upstream_sha_header` parsing robustness is unspecified.
2. What if `--init` is run without `--upstream`? Does it still attempt to write the header? The artifact doesn't say.
3. What if `--upstream-sha` is provided but the checkout HEAD is unavailable — does `do_init` write the flag value, or skip? F3's "explicit pin skips HEAD-unreadable check" is in `verify`, not `do_init`.

**Missing verification:** No test named for "header rewrite preserves the rest of VENDOR.md" or "header rewrite is idempotent". The named test `test_init_revendor_updates_upstream_sha_header` only confirms the field is written, not that surrounding prose is preserved byte-for-byte.

**Suspect-source file:** `laf-adaptation/scripts/check_boundary.py` (`do_init`, `_write_upstream_sha_header`), `laf-adaptation/VENDOR.md` (header region).

---

## F-5 [MED] — `prefix_unrewrite` helper introduced post-spec; surface area not bounded

**Evidence:** Phase 3 Findings mention *"added `prefix_unrewrite` helper"* without specifying:
- The exact string-replacement contract (is it `laf-adaptation:` → `creative-writing-skills:` only, or all laf-adaptation references?)
- Whether it operates on bytes or text (encoding-sensitive for hash equality)
- Whether it's symmetric with `prefix_rewrite` (composition `prefix_unrewrite(prefix_rewrite(x)) == x` is the load-bearing invariant for CH-1; not asserted as a unit test)

**Drift:** This helper is the linchpin of the entire H1 remediation and was added during implementation rather than specified. The Phase-6.3 lens gate was run on the diff and supposedly caught other issues — but did it specifically assert `prefix_unrewrite ∘ prefix_rewrite == identity`? The artifact doesn't list such a test.

**Concrete demand for scorer:** look for `test_prefix_rewrite_round_trip` or equivalent in `test_check_boundary.py`. If missing, the inverse-correctness of CH-1 is unverified beyond the single brainstormer.md data point.

**Suspect-source file:** `laf-adaptation/scripts/check_boundary.py` (`prefix_rewrite`, `prefix_unrewrite`).

---

## F-6 [MED] — Subprocess use in CH-5 lacks injection-surface analysis

**Evidence (target text, Phase 4):**
- *"`_checkout_head` (stdlib `subprocess`, Mode-U only) reads checkout HEAD"*
- *"Pin precedence: `--upstream-sha` flag > VENDOR.md `upstream_sha:`"*

**Missing verification:** No mention of:
1. Whether `subprocess.run` is called with `shell=False` (should be) and a controlled arg list (`['git', '-C', dir, 'rev-parse', 'HEAD']`).
2. Whether `dir` (`--upstream` value) is sanitized — since CH-4 enforces path-safety for *manifest* paths but `--upstream` is a CLI arg, not a manifest cell.
3. Timeout/capture semantics for the git invocation.
4. Error handling for missing `git` binary (the F3 "tarball fallback" handles missing repo, but missing executable is a separate code path).

**Suspect-source file:** `laf-adaptation/scripts/check_boundary.py` (`_checkout_head`).

---

## F-7 [MED] — L2 (unp