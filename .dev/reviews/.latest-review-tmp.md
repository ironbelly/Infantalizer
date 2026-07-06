# Code Review: PR #1 — LAF 0.1 (CWS Hybrid Integration, Path C)

**Target:** [PR #1](https://github.com/ironbelly/Infantalizer/pull/1) · **Base ↔ Head:** `main` ↔ `feature/laf-0.1-cws-hybrid`
**Reviewer:** `/sc:auggie-review` (depth=deep — Auggie prism-b pass + independent `auggie-reviewer` cross-check, both grounded)
**Generated:** 2026-07-04
**Stats:** 100 files / 9,867 lines. Only **1 executable file** (`laf-adaptation/scripts/check_boundary.py`); the rest are prose/config — the review is scoped to the code + CI + boundary-contract architecture. **11 findings + 1 nit, 0 dropped during grounding** (every finding cites real code).

---

## Summary

The build is well-structured and the boundary-contract *machinery* is correct for its happy path (both review passes independently confirmed rules A–F execute as documented and the vendored corpus is byte-faithful). **The one substantive theme — flagged HIGH by both passes independently — is a trust-model gap: in the mode CI actually runs (`check_boundary.py` with no `--upstream`), the enforcement's trust root is the PR-controlled `VENDOR.md` manifest, not the pinned upstream.** `upstream_sha256` is never read in verify mode; Rules B/C are skipped; Rule A/D/E/F all consult manifest-supplied values. So a single commit that edits an adopted body **and** updates its manifest hash passes CI green — the documented absolute guarantees ("`editor.md` is NEVER modified") are delivered only conditionally. Recommendation: **block-worthy for the security-gate framing, but not a functional blocker** — the framework works; the enforcement should be hardened before it's relied on as a security boundary against a malicious committer (vs. the accidental-drift case it already handles well).

## Findings

### 🟠 High (should fix before relying on this as a security gate)

#### H1. CI trusts the PR-controlled manifest — an adopted file + its hash can be edited together and pass CI
- **File:** `.github/workflows/boundary.yml:27` (+ `laf-adaptation/scripts/check_boundary.py:334,371`)
- **Category:** security / architecture · **Source:** both passes (independently)
- **Why this matters:** CI runs `uv run python scripts/check_boundary.py` with **no `--upstream`**, so `verify()` prints "Rules B and C skipped" and `upstream_sha256` is never read. Rule A only checks `sha256(file) == r.laf_sha256`, where `laf_sha256` comes from the same `VENDOR.md` the commit can edit. A commit that modifies `agents/editor.md` and updates its `laf_sha256` row passes A (self-consistent), skips B/C, and satisfies D/E/F (which also read the manifest's `cls`/paths). The invariant "editor never folded/modified" (VENDOR.md:11, CLAUDE.md §4) is enforced only transitively through a self-referential hash.
- **Recommendation:** In CI, check out the upstream at the pinned `upstream_sha` and run with `--upstream <checkout>` so Rules B/C anchor to upstream; **or** have verify mode assert `upstream_sha256` against a committed/pinned baseline it doesn't let the PR rewrite. At minimum, document that CI-verify is an accidental-drift gate, not a malicious-drift gate, and rely on branch protection + human review for the latter.

#### H2. Adopted skill `resources/**` are not integrity-covered in verify-without-upstream
- **File:** `laf-adaptation/scripts/check_boundary.py:194,196,401` (Rule F + `disk_skill_skillmds`)
- **Category:** architecture · **Source:** both passes
- **Why this matters:** Rule F's coverage set is `disk_agents() + disk_skill_skillmds()` — only `agents/*.md` and `skills/**/SKILL.md`. Adopted skill resources (e.g. `skills/story-review/resources/prose-critique/*.md`) are protected *only* by their per-file manifest rows via Rule A. Delete a resource's row (or drop a new file into an adopted skill's `resources/` tree — which CLAUDE.md itself calls a "NATIVE addition") and it is invisible to every rule in the CI mode. A whole class of adopted-subtree drift goes undetected.
- **Recommendation:** Extend Rule F to require every file under an adopted skill's `resources/**` be manifested (or hash the adopted skill dirs as a tree), so a deleted row or an untracked resource file fails the gate.

### 🟡 Medium (fix in this PR if cheap, else file a follow-up)

#### M1. Rule C is not constrained to the single allowed patched file `agents/writer.md`
- **File:** `laf-adaptation/scripts/check_boundary.py:352` — `if r.cls != "ADOPTED-PATCHED": continue`
- **Why:** Verify trusts the manifest's `cls`. Any row hand-classed `ADOPTED-PATCHED` gets the additive-frontmatter leeway (body must match, but `- laf-adaptation:` frontmatter lines may be added). The "only `writer.md` is patched" invariant is enforced at `--init` (line 204) but not in verify.
- **Recommendation:** Assert `ADOPTED-PATCHED ⟹ path == "agents/writer.md"` in `verify()`; any other patched row is a violation.

#### M2. Manifest paths are used unsanitized (path traversal / absolute paths)
- **File:** `laf-adaptation/scripts/check_boundary.py:161,250` — `path, cls = cells[0], cells[1]` → `read_text(REPO / rel)`
- **Why:** A manifest row with `../../etc/...` or an absolute path resolves outside the tree; the script reads/hashes it. The manifest is repo-controlled, but a security-boundary parser should reject escapes.
- **Recommendation:** Reject manifest paths that are absolute or resolve outside `REPO` (`(REPO / rel).resolve().is_relative_to(REPO)`).

#### M3. `--upstream` is not validated against the pinned `upstream_sha`
- **File:** `laf-adaptation/scripts/check_boundary.py:338` (Rule B/C dereference `upstream_dir`)
- **Why:** The script trusts whatever tree `--upstream` points at; it never asserts the checkout is at `VENDOR.md`'s `upstream_sha`. A stale/wrong upstream checkout silently produces false-green B/C.
- **Recommendation:** Read `upstream_sha` from the manifest header and assert the `--upstream` checkout's HEAD matches (or accept `--upstream-sha` and compare).

#### M4. Malformed / `|`-containing / duplicate manifest rows are silently tolerated
- **File:** `laf-adaptation/scripts/check_boundary.py:158-164` (`parse_manifest`)
- **Why:** Rows with `< 4` cells or an unrecognized class are silently skipped; cells are split on `|` with no escaping, so a `|` inside a cell shifts columns and misassigns class/hash. In a security-relevant parser, silent tolerance lets a row be dropped (its file then unchecked by A).
- **Recommendation:** Fail loudly on unparseable rows, duplicate paths, and malformed hashes rather than `continue`.

#### M5. `--init` never performs the prefix rewrite it "models"; Rule B is untested by the current corpus
- **File:** `laf-adaptation/scripts/check_boundary.py:259-264` (`do_init` skill loop)
- **Why:** `do_init` records `laf_sha256 = sha256(on-disk file)` but applies no `prefix_rewrite`; it trusts the vendorer did it by hand. Every ADOPTED-CLEAN skill row in VENDOR.md shows `upstream_sha256 == laf_sha256` (the rewrite was a no-op for those files), so Rule B's `sha256(prefix_rewrite(upstream)) == laf_sha256` path has no positive test — a future prefix-bearing file could be mis-vendored without notice.
- **Recommendation:** Either have `--init` perform the rewrite itself, or add a fixture test with a `creative-writing-skills:`-bearing file to exercise Rule B.

### 🟢 Low (nice-to-have / hardening)

#### L1. `read_text` / `--report` crash on malformed input instead of a clean contract-fail
- **File:** `laf-adaptation/scripts/check_boundary.py:65-66,419` — no `try/except`, no `errors=` on decode.
- **Why:** A non-UTF-8 byte in an adopted file, or a file removed between enumeration and read, raises an uncaught traceback; `--report` (documented "always exit 0") also crashes on a malformed manifest read, violating its own contract.
- **Recommendation:** Wrap reads; convert to a boundary-contract error; guarantee `--report` exits 0.

#### L2. CI uses unpinned third-party actions and no explicit least-privilege permissions
- **File:** `.github/workflows/boundary.yml:20,23` — `actions/checkout@v4`, `astral-sh/setup-uv@v7` (tags, not SHAs); no `permissions:` block.
- **Why:** For a security gate, a moved tag is a supply-chain vector, and the default `GITHUB_TOKEN` is broad.
- **Recommendation:** SHA-pin the actions; add `permissions: { contents: read }`.

#### L3. Set-based `frontmatter_line_diff` drops duplicate-line removals
- **File:** `laf-adaptation/scripts/check_boundary.py:100-108` (+ the unterminated-frontmatter edge at `88`)
- **Why:** Frontmatter is diffed as a set, so removing one of two identical lines is invisible — weaker than the "byte-identical, additive-only, duplicate preserved" intent. Separately, an unterminated frontmatter folds the whole file into `body`, so Rule C's additive checks never run.
- **Recommendation:** Use an ordered/multiset comparison for the additive check; treat malformed frontmatter as an error, not "no frontmatter."

### 💬 Nit

- **`check_boundary.py:200-219`** — NATIVE/BUILD-NEW classification depends on hardcoded name lists (`NATIVE_AGENTS`, `BUILD_NEW_AGENTS`, …) and defaults unknown non-upstream files to NATIVE. Functionally fine and already documented, but it couples the checker to the framework's file roster; a stray new agent silently classes NATIVE. Consider deriving from a small declared provenance file, or at least warning on the default-NATIVE path.

## Architectural / Cross-Cutting Observations

- **The trust root is the manifest, not the pinned upstream (ties H1/M1/M3).** The contract's strongest guarantees (B/C, upstream equality) run only under `--init` or an explicit `--upstream` run — never in CI. This is a deliberate design trade-off (the `boundary.yml` comment says A/D/E/F "work on the manifest alone"), but the docs elsewhere state the guarantees as absolute. Align the docs with the enforced (conditional) guarantee, or strengthen CI to the absolute one.
- **What this review does NOT dispute:** the vendored corpus is byte-faithful, rules A–F are correctly implemented for the accidental-drift case, and the framework's functional behavior (the Phase-3 hard-gate proof) is sound. The findings are about the *enforcement's robustness against a hostile manifest*, not about whether the framework works.

## Audit

- Auggie chunks: 1 (deep, prism-b, `--wait-for-indexing`, exit 0) + 1 independent `auggie-reviewer` Claude-side cross-check.
- Findings dropped during grounding: **0** (all 11 + nit cite real, verified `file:line`).
- Convergence: both passes independently found H1 and H2 — highest confidence.
