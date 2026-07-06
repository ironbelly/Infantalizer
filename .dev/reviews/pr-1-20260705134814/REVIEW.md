# Code Review: PR #1 — LAF 0.1 — CWS Hybrid Integration (Path C)

**Target**: PR #1 (https://github.com/ironbelly/Infantalizer/pull/1)
**Reviewer**: /sc:auggie-review (depth=quick, focus=correctness,security,anti-patterns,tests,ci,architecture)
**Generated**: 2026-07-05
**Base ↔ Head**: `main` ↔ `feature/laf-0.1-cws-hybrid`
**Head SHA**: `ae1184b`
**Stats**: 272 files, ~23k diff lines. Reviewed the **executable code surface** (the only place real bugs can live): `laf-adaptation/scripts/check_boundary.py` (709 lines, the boundary-contract keystone), `analyze.py` (309 lines), `.github/workflows/boundary.yml`, `.githooks/pre-commit`, and the YAML config schema files. The other ~260 files are markdown prose / static YAML data and were not line-reviewed. **6 findings, 0 dropped during grounding.**

---

## Summary

This is a well-architected PR. The boundary-contract design is unusually rigorous — a vendoring integrity scheme with two trust roots (`laf_sha256` + `upstream_sha256`), prefix-rewrite equivalence proofs, parser hardening, and path-safety. The shipped `check_boundary.py` passes its own 25-test stdlib suite (which I ran — all pass). The framework's self-documentation is honest about what its CI ("Mode V") does and does not guarantee.

**Top 3 risks:**
1. **The 25-test regression suite for the boundary checker is not run in CI** (Medium, cheap fix). A logic regression in the security keystone could merge as long as the live fixture happens to pass.
2. **`manifest_covers` is class-agnostic** — a manifest edit could swap exact adopted-file rows for broad globs and silently drop hash protection (High, the only finding with no corresponding regression test or doc note).
3. **The "byte-identical vendoring" claim is text-normalized**, not byte-accurate (Medium, contract-fidelity nit; internally consistent).

**Recommendation: nits-only → request-changes.** No Critical issues. The High finding (#H1) is a real logic gap worth closing before this becomes load-bearing; the rest are addressable as follow-ups. The widely-documented "Mode V writer.md residual" appears below as a finding only because it was surfaced — it is explicitly an accepted design tradeoff, not a defect.

---

## Findings

### 🟠 High (should fix before merge)

#### H1. `manifest_covers` accepts class-agnostic globs — adopted files can silently lose hash protection
- **File**: `laf-adaptation/scripts/check_boundary.py:296`
- **Category**: security / correctness
- **Source**: auggie (grounded + verified)
- **Evidence**:
  ```python
  def manifest_covers(rows, rel: str) -> bool:
      for r in rows:
          if r.path == rel:
              return True
          if r.is_glob and rel.startswith(r.path[:-2]):  # 'skills/x/**' covers 'skills/x/...'
              return True
      return False
  ```
- **Why this matters**: Rule F/F′ (lines 628-647) uses `manifest_covers` to assert every `agents/*.md`, `skills/**/SKILL.md`, and adopted-skill `resources/**` file is manifested. But the predicate treats *any* `/**` row as covering *any* matching path, with **no class check**. Rule A (lines 499-507) only hash-checks rows where `r.is_adopted`. So a two-step manifest edit — delete the exact `agents/foo.md | ADOPTED-CLEAN | <hash> | <hash>` row, add `agents/** | NATIVE | — | —` — would: (a) still satisfy Rule F coverage via the glob, (b) no longer hash-check `foo.md` under Rule A (no adopted row), (c) not trip Rule D (quartet only). An adopted file's body could then drift with no boundary alarm. The parser (line 407) only ever emits `/**` glob rows for NATIVE/BUILD-NEW skills, but **nothing validates that glob rows are restricted to that shape** — `agents/**` or `skills/<adopted>/**` rows are accepted. Unlike the documented two-field hash forgery, this gap has **no regression test and no doc note** calling it out.
- **Recommendation**: At parse time, restrict `/**` glob rows to NATIVE/BUILD-NEW skill roots of the exact form `skills/<name>/**` (reject `agents/**` and any adopted-path glob). Make `manifest_covers` class-aware so an adopted file is only "covered" by an exact adopted hash row, not by an unrelated glob. Add a regression test asserting a `agents/**` glob row is rejected.

### 🟡 Medium (fix in this PR if cheap, otherwise file followup)

#### M1. CI does not run the boundary checker's regression test suite
- **File**: `.github/workflows/boundary.yml:49`
- **Category**: tests / ci
- **Source**: auggie (grounded + verified — suite confirmed to exist and pass)
- **Evidence**:
  ```yaml
        - name: Set up uv
          uses: astral-sh/setup-uv@v7

        - name: Boundary contract (verify)
          working-directory: laf-adaptation
          run: uv run python scripts/check_boundary.py
  ```
- **Why this matters**: The workflow runs the checker against the live tree only. `laf-adaptation/scripts/test_check_boundary.py` (36 KB, **25 stdlib unittests, all passing** — I ran it) covers parser hardening, Mode-U SHA pinning, prefix rewrite, resource coverage, path traversal, and the trust-root forgery cases. None of it runs in CI. A regression in the checker logic — the security keystone of the whole PR — could merge as long as the current fixture happens to pass `verify`. The trust-root tests in particular (`test_adopted_body_edit_plus_laf_hash_rewrite_fails`, `test_upstream_sha256_rewrite_of_clean_body_fails`) are exactly the assertions you do not want to silently lose.
- **Recommendation**: Add a CI step (under `working-directory: laf-adaptation`) that runs `uv run python scripts/test_check_boundary.py`. If the "exactly one script under `scripts/`" rule (ADR-006) is hard, the test file is already a sibling of the script and doesn't violate the runtime "one tool" rule — it's a test, not a runtime artifact. Running it costs seconds.

#### M2. Hashing is text-normalized, not byte-accurate
- **File**: `laf-adaptation/scripts/check_boundary.py:68` (and `read_text` at `:76`)
- **Category**: correctness / contract-fidelity
- **Source**: auggie (grounded + verified)
- **Evidence**:
  ```python
  def sha256_text(text: str) -> str:
      return sha256_bytes(text.encode("utf-8"))

  def read_text(p: Path) -> str:
      return p.read_text(encoding="utf-8")
  ```
- **Why this matters**: `Path.read_text` opens in text mode with default `newline=None`, which applies universal-newline translation (`\r\n` / `\r` → `\n`) before the bytes are ever hashed. The boundary contract is described elsewhere as "byte-identical vendoring" / "byte-faithful," but the implementation hashes the LF-normalized form. A CRLF and an LF version of the same file produce the same `laf_sha256`. The same text pipeline feeds `prefix_rewrite` and `body_of` comparisons, so the system is **internally consistent** — it just isn't byte-accurate. This is a fidelity nit against the prose, not a functional bug today (all vendored files are LF). It becomes real if upstream ever ships CRLF.
- **Recommendation**: Either (a) hash raw bytes via `read_bytes()` for the manifest hashes and do prefix rewriting on bytes, or (b) soften the docs to "text-normalized (LF) integrity" so the contract and the code agree. (a) is stronger; (b) is cheaper.

#### M3. The writer.md Mode-V gap is a documented residual — but it's worth a one-line pointer in the checker
- **File**: `laf-adaptation/scripts/check_boundary.py:517`
- **Category**: ci / architecture (documented limitation)
- **Source**: auggie-flagged, **downgraded from High after grounding**
- **Evidence**:
  ```python
      # ADOPTED-PATCHED (writer.md) is intentionally excluded: its `upstream_sha256` is
      # the whole-raw-upstream-file hash, not reconstructible from the patched disk
      # without the upstream blob; its absolute guarantee is Mode-U Rule C.
  ```
- **Why this matters**: Auggie flagged this as "Default/CI mode never enforces the ADOPTED-PATCHED writer additive-only contract." On grounding, this is **not a defect** — it is an explicitly documented and tested design decision. The exclusion is acknowledged here at line 517, in the workflow comments (`boundary.yml:27-33`, "ADOPTED-PATCHED ... ABSOLUTE guarantee requires Mode U ... deferred follow-up OQ-4"), in `CLAUDE.md`, in `VENDOR.md` "Hash semantics," and — decisively — in two regression tests: `test_writer_is_not_reanchored_in_mode_v` and `test_adopted_body_edit_plus_both_hashes_forged_PASSES_mode_v` (the latter literally commented `DOCUMENTED-RESIDUAL (F2 / spec §4.1 bullet 2)`). The residual is backstopped by branch protection + mandatory human review of any `upstream_sha256` diff. **Downgraded to Medium** and reframed: the only actionable ask is a `# OQ-4` / `# residual: writer.md` comment near line 578 (the Rule-C skip) so a future reader of just the code sees the pointer to Mode U, not just the inverse-direction comment at 517.
- **Recommendation**: No logic change. Optionally add a one-line comment at the `else:` block (line 598) explicitly naming OQ-4 / writer.md so the Mode-V skip is self-documenting without reading the workflow header.

### 🟢 Low (nice-to-have)

#### L1. Additive-only frontmatter diff collapses duplicate lines
- **File**: `laf-adaptation/scripts/check_boundary.py:118`
- **Category**: correctness (edge case)
- **Source**: auggie (grounded + verified), **downgraded from Medium**
- **Evidence**:
  ```python
      up_fm = {ln.rstrip() for ln in split_frontmatter(up_text)[0] if ln.strip()}
      cur_fm = {ln.rstrip() for ln in split_frontmatter(cur_text)[0] if ln.strip()}
      added = sorted(cur_fm - up_fm)
      removed = sorted(up_fm - cur_fm)
  ```
- **Why this matters**: Set semantics discard multiplicity, so deleting one copy of a duplicated frontmatter line is invisible if another identical copy remains. The docstring (line 121) claims this "correctly handles writer.md's preserved duplicate `creative-writing-craft` line," but the implementation would not detect removal of one of two duplicates under Mode U. This only matters in Mode U (which CI doesn't run) and only for that one duplicated line — narrow edge case.
- **Recommendation**: If Mode U ever ships in CI, switch to a `collections.Counter` multiset for the diff so multiplicity is preserved. Not needed for 0.1.

#### L2. Concept-mapping tier keys drift between `tier_5` and `tier_4_5`
- **File**: `config/concept_mapping/templates/tolkien_mapping.yaml:23` (vs `config/concept_mapping/universal_mappings.yaml:8` and `laf-adaptation/templates/work-mapping-template.yaml:23`)
- **Category**: architecture / schema-consistency
- **Source**: auggie (grounded + verified)
- **Evidence**: `tolkien_mapping.yaml` uses `tier_5:`; `universal_mappings.yaml` and `work-mapping-template.yaml` use `tier_4_5:`.
- **Why this matters**: Two different key conventions for the upper tier across sibling mapping files. `CLAUDE.md` documents this drift as deliberate and mandates reader-side tolerant lookup (`.get(a) or .get(b)`), but there is **no schema-level validation** enforcing that consumers do this — a reader resolving tier-5 in a work-specific override could silently miss it.
- **Recommendation**: Either standardize on one key, or add a one-time consistency check (could live in `check_boundary.py` as a new rule, or a tiny schema validator). Low priority — the contract already says readers must be tolerant.

### 💬 Nits

- `analyze.py` (309 lines) was scanned for `subprocess`, `os.system`, `eval`, `exec`, `yaml.load`, `pickle`, `shell=`, `input` — **none present**. Clean local CLI helper. No action.
- The pre-commit hook (`.githooks/pre-commit`) correctly runs the same Mode-V command as CI and handles the nested-`laf-adaptation/`-under-git-root case. No action.

---

## Architectural / Cross-Cutting Observations

1. **Mode-U (the absolute guarantee) is not in any automated gate.** Both CI and the opt-in pre-commit hook run Mode V only. This is consistent and documented, but means the upstream-anchored Rules B/C and the writer.md additive-body proof are enforced only by human review of `upstream_sha256` diffs. The `upstream_sha256`-diff-as-review-signal design is sound; just be aware the absolute guarantee is a human gate, not a machine one. (`boundary.yml:27-33`, `check_boundary.py:538-601`)

2. **Deliberate tier-YAML schema drift is by design but unsupported by a guard.** T1-T3 use `conflict_to_cooperation` / `death_euphemism`; T5 uses `conflict_handling` / `death_handling`. Documented in `CLAUDE.md` as intentional (reader normalizes), but no validator enforces readers do so. (`kb/tiers/tier_1.yaml`, `kb/tiers/tier_5.yaml`)

3. **The hash-pinning trust model is strong and honestly documented.** Two trust roots, prefix-rewrite inversion to break the self-referential `laf_sha256` loop (Rule A′, CH-1), and explicit "this is what Mode V does NOT catch" prose in the workflow header are exactly the right engineering posture for a vendoring boundary. This is the best part of the PR.

---

## Audit

- **Auggie chunks**: 1 (succeeded, 0 retried, 0 skipped; 218s, exit 0)
- **Findings dropped during grounding**: 0 (all 6 cited real file:line; evidence snippets matched verbatim)
- **Severity remaps**: 2 downgrades — H1(writer gap) High→Medium (documented/tested residual); M2(frontmatter sets) Medium→Low (narrow Mode-U edge case). H1(manifest_covers) confirmed High.
- **Persona cross-check**: disabled (depth=quick)
- **Token cost**: Claude ≈ orchestration only; Auggie ≈ deep pass (offloaded)
- **Test suite run**: `uv run python scripts/test_check_boundary.py` → 25 tests, OK (confirms M1)

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 1 medium: 3 low: 2 nit: 0
dropped: 0
auggie_chunks: 1
-->
