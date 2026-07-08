# Remediation Specification — PR #1 (LAF 0.1 CWS Hybrid Integration, Path C)

**Type:** Architecture (security/hardening of the boundary-contract enforcement layer)
**Format:** Spec
**Source review:** `.dev/reviews/pr-1-20260704125705/REVIEW.md`
**Target branch:** `feature/laf-0.1-cws-hybrid`
**Authored:** 2026-07-04 (Phase A — spec only; do NOT execute fixes in this phase)
**Phase B consumer:** task-builder (produces an MDTM task file from this spec)

---

## 0. Purpose & Scope

This spec converts the actionable findings of the PR-1 review into a concrete, build-ready remediation plan. It covers the **2 HIGH** trust-root findings (H1, H2) and the **5 MEDIUM** enforcement-hardening findings (M1–M5). The **3 LOW** (L1–L3) and **1 NIT** are documented as deferred follow-ups (Appendix C) — out of scope for this remediation cycle unless explicitly pulled in.

**What this spec does NOT dispute** (per review §"What this review does NOT dispute"): the vendored corpus is byte-faithful, Rules A–F are correctly implemented for the accidental-drift case, and the framework's functional behavior is sound. All findings target the *enforcement's robustness against a hostile or malformed manifest*, not framework correctness.

**The unifying theme (review §"Architectural / Cross-Cutting Observations"):** the contract's strongest guarantees (Rules B/C, upstream equality) run only under `--init` or an explicit `--upstream` run — never in CI. CI's trust root is the PR-controlled `VENDOR.md` manifest, not the pinned upstream. H1 + M1 + M3 are facets of this single gap; H2 is a coverage gap in the same CI mode.

**Single executable in scope:** `laf-adaptation/scripts/check_boundary.py` (459 lines, pure stdlib). Plus the CI workflow `.github/workflows/boundary.yml` (28 lines) and one doc `laf-adaptation/VENDOR.md`.

---

## 1. Design Goals (in priority order)

1. **G1 — Make the trust root the pinned upstream, not the PR-controlled manifest.** (H1, M3) A committer who edits an adopted body AND updates its manifest `laf_sha256` in the same commit must NOT pass CI green.
2. **G2 — Close the adopted-skill-`resources/**` coverage gap in CI mode.** (H2) A deleted manifest row or an untracked resource file under an adopted skill must fail the gate.
3. **G3 — Harden the parser against malformed/hostile manifest input.** (M2, M4) Path traversal, malformed rows, duplicate paths, and bad hashes must fail loud, not silently drop a row (which would silently un-protect its file).
4. **G4 — Constrain the patched-class leeway to the one file entitled to it.** (M1) `ADOPTED-PATCHED` ⇒ `path == agents/writer.md`.
5. **G5 — Make the prefix-rewrite code path tested, not theoretical.** (M5) Rule B's `sha256(prefix_rewrite(upstream)) == laf_sha256` must have a positive test.
6. **G6 — Preserve all existing happy-path behavior.** No regression to Rules A/D/E/F on the current corpus; `--init` and `--report` modes unchanged in contract; pure-stdlib constraint (ADR-006) preserved; `--report` still always exits 0.

**Non-goal:** Rewriting the checker into a runtime or adding a CLI surface. ADR-006 (prompt + YAML-config, one validation script) is inviolable.

---

## 2. Architecture: Two Hardened Modes

The remediation distinguishes two enforcement modes and makes the contract honest about each:

### 2.1 Mode V (Verify, CI) — the gate that runs on every PR/push

**Current behavior:** `verify()` with `upstream_dir=None`. Prints "Rules B and C skipped." Trust root = `VENDOR.md`.

**Remediated behavior:** Mode V remains manifest-anchored BUT gains two new defenses that do not require an upstream checkout:

- **(a) `upstream_sha256` becomes a CI-checked field, not a no-op.** Today `upstream_sha256` is read into each `Row` but never consulted in verify mode. After remediation, verify mode asserts **`sha256(prefix_rewrite(body_on_disk)) == r.upstream_sha256`** for every ADOPTED-CLEAN row — using the `upstream_sha256` already pinned in the manifest. This re-anchors adopted-file integrity to the *upstream-derived* hash rather than the self-referential `laf_sha256`. See §4.1 for the exact semantics and the writer.md/ADOPTED-PATCHED carve-out.
- **(b) Manifest self-consistency (G3).** Parser-level hardening (M2/M4) ensures the manifest itself is well-formed before any rule runs.

**Why this closes H1 without an upstream checkout:** A malicious commit that edits `agents/editor.md` and updates only its `laf_sha256` row now FAILS, because the editor body no longer matches the pinned `upstream_sha256` (which the commit did not also forge — and if it did, that's a much louder, review-visible change to a field documented as upstream-derived). The "editor never modified" invariant (VENDOR.md:11) is enforced against the upstream-derived hash, breaking the self-referential loop. This is the review's recommended "at minimum" path: "have verify mode assert `upstream_sha256` against a committed/pinned baseline it doesn't let the PR rewrite." It is weaker than a full upstream checkout (Option B below) but has zero CI cost and no new dependencies.

### 2.2 Mode U (Verify with `--upstream`) — the strong / upstream-anchored gate

**Current behavior:** `verify(upstream_dir)` runs Rules B/C against whatever tree `--upstream` points at, with no check that the tree is at `upstream_sha`.

**Remediated behavior (M3):** Mode U asserts the `--upstream` checkout's HEAD equals `VENDOR.md`'s pinned `upstream_sha` before trusting any upstream blob. A stale/wrong checkout fails loud rather than producing false-green B/C.

**Optional stronger CI (review H1 "or"):** The spec RECOMMENDS (but does not REQUIRE) that CI optionally run Mode U by checking out the upstream at `upstream_sha` and invoking `--upstream`. This is the absolute guarantee. It is staged as **Option B** in §8 so a task-builder can scope it as a separate, optional task. Mode V's `upstream_sha256` assertion (§2.1a) is the REQUIRED floor; Mode U in CI is the RECOMMENDED ceiling.

---

## 3. Inventory of Changes

| ID | Finding | File(s) | Nature | Priority |
|----|---------|---------|--------|----------|
| **CH-1** | H1 | `check_boundary.py` (verify), `VENDOR.md` (doc) | New Rule A′ in verify mode: assert disk body against pinned `upstream_sha256` | P0 |
| **CH-2** | H2 | `check_boundary.py` (Rule F) | Extend Rule F coverage to adopted skills' `resources/**` | P0 |
| **CH-3** | M1 | `check_boundary.py` (verify, Rule C) | Assert `ADOPTED-PATCHED ⇒ path == agents/writer.md` | P1 |
| **CH-4** | M2 | `check_boundary.py` (parse_manifest) | Reject path-traversal / absolute manifest paths | P1 |
| **CH-5** | M3 | `check_boundary.py` (verify, Mode U) | Assert `--upstream` checkout HEAD == pinned `upstream_sha` | P1 |
| **CH-6** | M4 | `check_boundary.py` (parse_manifest) | Fail loud on malformed/duplicate/bad-hash rows | P1 |
| **CH-7** | M5 | `check_boundary.py` (--init) **or** test fixture | Exercise Rule B's prefix-rewrite path with a positive test | P1 |
| **CH-8** | (cross) | `.github/workflows/boundary.yml` | Doc comment update; OPTIONAL Option B (Mode U in CI) + L2 pinning | P2 |

All changes are inside `laf-adaptation/` except CH-8 (repo-root workflow). No new files outside `laf-adaptation/scripts/` and the workflow. A test fixture directory (CH-7) is the only permitted addition.

---

## 4. Detailed Change Specifications

### 4.1 CH-1 — Verify-mode Rule A′: anchor adopted-file integrity to `upstream_sha256` (H1)

**Problem (H1):** In `verify()` lines 326–335, Rule A checks only `sha256(file) == r.laf_sha256`, where `laf_sha256` is manifest-supplied and PR-editable. `upstream_sha256` (also manifest-supplied) is loaded into `Row.upstream_sha256` (line 166) but **never read in verify mode**. A commit that edits an adopted body AND rewrites its `laf_sha256` row passes A, skips B/C, and satisfies D/E/F.

**Spec — new Rule A′ (verify mode, runs whenever `upstream_dir is None` OR always):**

For each adopted row, after the existing Rule A check, ALSO assert:

```
ADOPTED-CLEAN:   sha256_text(prefix_rewrite(read_text(REPO/r.path))) == r.upstream_sha256
ADOPTED-PATCHED: sha256_text(prefix_rewrite(body_of(read_text(REPO/r.path)))) == r.upstream_sha256
```

Notes for the implementer:
- **For ADOPTED-CLEAN**, the on-disk file should equal `prefix_rewrite(upstream_blob)`. Since the vendored file IS the prefix-rewritten upstream, hashing the prefix-rewrite of the disk file is a no-op for already-rewritten files (the disk file contains `laf-adaptation:` already, so `prefix_rewrite` is idempotent here) — but applying `prefix_rewrite` keeps the assertion faithful to what `upstream_sha256` actually pins (the upstream blob's raw bytes). **Decision point (see §6 Q1):** the implementer must confirm whether `upstream_sha256` in VENDOR.md is the hash of the RAW upstream blob or the PREFIX-REWRITTEN blob. Spot-check: for `agents/brainstormer.md`, `upstream_sha256=aa736c5d…` ≠ `laf_sha256=5c827eff…`, so they differ — meaning the disk file (prefix-rewritten) does NOT hash to `upstream_sha256`. Therefore `upstream_sha256` is almost certainly the **raw upstream** hash, and the assertion must compare `sha256(prefix_rewrite(disk))` against `r.upstream_sha256` **only if** raw==rewritten upstream — which is NOT generally true. **This is the single most important detail to resolve before coding (§6 Q1).** The correct, safe formulation that matches existing `--init` behavior (line 249: `up_sha = sha256_text(up_raw)` — the RAW upstream bytes) is: `upstream_sha256` pins the **raw upstream blob**, so verify-mode Rule A′ for ADOPTED-CLEAN cannot be computed without the upstream blob UNLESS we also store/derive it. Resolution options are enumerated in §6 Q1; the task-builder must pick one.
- **For ADOPTED-PATCHED (writer.md only):** compare the prefix-rewritten BODY (frontmatter stripped) against `upstream_sha256`. writer.md's `upstream_sha256` (line 33: `373e605b…`) — same raw-vs-rewritten question applies.
- **Skip rows whose `upstream_sha256 == NO_HASH`** (NATIVE/BUILD-NEW never have one; an adopted row with `NO_HASH` upstream hash is itself a violation — emit an error: "adopted row missing upstream_sha256").

**Why this is sound:** Once `upstream_sha256` is genuinely checked (not just stored), the self-referential loop is broken: a committer must forge the upstream-derived hash to hide a body edit, and that field is documented (VENDOR.md header) as upstream-derived — a far more review-visible change than rewriting `laf_sha256`.

**Doc update (CH-1 doc part):** `VENDOR.md` header comment and `CLAUDE.md` §2 must state that verify mode now enforces `upstream_sha256` against the on-disk adopted bodies, and clarify whether CI is an accidental-drift gate, a malicious-drift gate, or both (depending on §6 Q1 resolution + whether Option B is adopted). Align the "absolute guarantee" language flagged in the review.

**Acceptance criteria:**
- A test that mutates an adopted body AND updates only its `laf_sha256` row → **FAIL** (exit 1) under remediated verify.
- A test that mutates an adopted body and updates BOTH hashes to be self-consistent but wrong-vs-upstream → behaviour per §6 Q1 resolution (the whole point is to make this FAIL or be loudly detectable).
- The current clean corpus → **PASS** (no false positives).

---

### 4.2 CH-2 — Extend Rule F to adopted skills' `resources/**` (H2)

**Problem (H2):** Rule F (line 400–403) iterates `disk_agents() + disk_skill_skillmds()` only — i.e. `agents/*.md` and `skills/**/SKILL.md`. Adopted skill resources (e.g. `skills/story-review/resources/prose-critique/*.md`) are protected only by Rule A per-row. Deleting a resource's manifest row, or dropping a new untracked file into an adopted skill's `resources/` tree, is invisible to every CI-mode rule.

**Spec:** Add a Rule F sub-check — for every skill dir that contains at least one ADOPTED manifest row (i.e. is an adopted skill), enumerate `disk_skill_files(skill_dir)` and assert each file is `manifest_covers(rows, rel)`. Concretely, add to the Rule F loop:

```
adopted_skill_dirs = {
    r.path.split("/")[1] for r in rows
    if r.path.startswith("skills/") and r.is_adopted
}
for skdir in disk_skill_dirs():
    if skdir.name in adopted_skill_dirs:
        for rel in disk_skill_files(skdir):
            if not manifest_covers(rows, rel):
                errors.append(f"{rel}: adopted-skill file not in VENDOR.md manifest")
```

Notes:
- This makes the manifest's `resources/**` superset (per CLAUDE.md "Why VENDOR.md has more rows (64) than the Rule-F glob set (31)") **enforced**, not merely descriptive.
- An untracked new file in an adopted skill's `resources/` now fails — which aligns with CLAUDE.md's guidance ("Prefer adding a NATIVE skill over dropping a file inside an adopted skill dir"). If a committer legitimately adds a NATIVE resource, they must either add a NATIVE manifest row (extending the glob model) or — per current design preference — add a standalone NATIVE skill. The spec does NOT change that preference; it only makes the violation visible.
- NATIVE/BUILD-NEW skill dirs (glob rows `skills/<name>/**`) are already covered by `manifest_covers` via the glob; this sub-check targets only adopted skill dirs.

**Acceptance criteria:**
- Delete a `resources/**` row from VENDOR.md for an adopted skill → **FAIL** with "adopted-skill file not in VENDOR.md manifest."
- Drop a new untracked `.md` into `skills/story-review/resources/` → **FAIL**.
- Current corpus (all 64 rows intact, no stray files) → **PASS**.

---

### 4.3 CH-3 — Constrain ADOPTED-PATCHED to `agents/writer.md` (M1)

**Problem (M1):** Line 352 trusts the manifest's `cls`. Any row hand-classed `ADOPTED-PATCHED` gets additive-frontmatter leeway. The "only writer.md is patched" invariant is enforced at `--init` (line 204) but not in verify.

**Spec:** In `verify()`, before/within the Rule C loop, add:

```
for r in rows:
    if r.cls == "ADOPTED-PATCHED" and r.path != "agents/writer.md":
        errors.append(f"{r.path}: ADOPTED-PATCHED is reserved for agents/writer.md only")
```

Place this check OUTSIDE the `if upstream_dir:` block so it runs in BOTH Mode V and Mode U (it does not need the upstream tree).

**Acceptance criteria:**
- A manifest row classing any path other than `agents/writer.md` as `ADOPTED-PATCHED` → **FAIL** in both modes.
- `agents/writer.md` as `ADOPTED-PATCHED` → unchanged behavior.

---

### 4.4 CH-4 — Reject path-traversal / absolute manifest paths (M2)

**Problem (M2):** Lines 161/250 — `path = cells[0]` is used unsanitized as `REPO / rel`. A row with `../../etc/passwd` or `/etc/passwd` resolves outside the tree; the script reads/hashes it.

**Spec:** Add a validation helper and call it for every parsed row:

```
def _safe_repo_path(rel: str) -> Path:
    p = (REPO / rel).resolve()
    if not p.is_relative_to(REPO):
        raise ManifestError(f"{rel!r}: manifest path escapes laf-adaptation/ tree")
    return p
```

- `Path.is_relative_to` is stdlib (Python 3.9+); confirm the project's min-Python via `pyproject.toml` (§6 Q2). If <3.9, use `p == REPO or REPO in p.parents`.
- Replace `REPO / r.path` reads in Rules A/B/C and `do_init` with `_safe_repo_path(r.path)`.
- An absolute path (`Path(rel).is_absolute()`) or any `..` escape → `ManifestError` collected as a verify error (fail loud), NOT a silent skip.

**Acceptance criteria:**
- Manifest row `| ../../etc/passwd | ADOPTED-CLEAN | … | … |` → **FAIL** with "path escapes tree."
- Manifest row with absolute path → **FAIL.**
- All current rows (relative, in-tree) → **PASS.**

---

### 4.5 CH-5 — Validate `--upstream` against pinned `upstream_sha` (M3)

**Problem (M3):** Line 338 — Mode U dereferences `upstream_dir` with no check that the checkout is at `VENDOR.md`'s `upstream_sha`. A stale checkout silently false-greens B/C.

**Spec:** When `upstream_dir` is provided, BEFORE running Rules B/C, read the checkout's HEAD and assert it equals the manifest's pinned `upstream_sha`:

```
import subprocess  # stdlib; only used in Mode U
head = subprocess.run(["git", "-C", str(Path(upstream_dir).resolve()), "rev-parse", "HEAD"],
                      capture_output=True, text=True, check=True).stdout.strip()
if head != pinned_upstream_sha:
    errors.append(f"--upstream checkout HEAD {head[:12]} != pinned upstream_sha "
                  f"{pinned_upstream_sha[:12]} (re-checkout at the pinned SHA)")
```

- `pinned_upstream_sha` is parsed from the VENDOR.md header (`upstream_sha:` line). Add a small header parser (the manifest currently only parses the table; the header `upstream_sha:` field is unread). Reuse for CH-5 and expose for future use.
- If `git` is unavailable or the dir is not a git repo (e.g. a tarball checkout), fall back to accepting an explicit `--upstream-sha <sha>` CLI flag and comparing; if neither is available, **fail loud** (do NOT silently trust the tree). Add `--upstream-sha` to argparse.
- This check runs only in Mode U (no cost in Mode V / CI).

**Acceptance criteria:**
- Mode U against a checkout at the wrong SHA → **FAIL** with the HEAD-mismatch message.
- Mode U against a checkout at the pinned SHA → unchanged (Rules B/C run).
- Mode V (no `--upstream`) → unchanged (CH-5 does not execute).

---

### 4.6 CH-6 — Fail loud on malformed / duplicate / bad-hash rows (M4)

**Problem (M4):** `parse_manifest` (lines 158–164) silently `continue`s past rows with `< 4` cells or unrecognized classes; cells split on `|` with no escaping; duplicates not detected. A silently-dropped row un-protects its file.

**Spec — restructure `parse_manifest` to collect errors:**

```
def parse_manifest(text) -> tuple[list[Row], list[str]]:
    rows, errors = [], []
    seen_paths = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 4:
            errors.append(f"manifest line {lineno}: expected 4 cells, got {len(cells)}: {s!r}")
            continue
        path, cls = cells[0], cells[1]
        if path.lower() == "path" or set(path) <= set("-: "):  # header / separator
            continue
        if cls.upper() not in CLASSES:
            errors.append(f"manifest line {lineno}: unknown class {cls!r}")
            continue
        # duplicate-path detection
        if path in seen_paths:
            errors.append(f"manifest line {lineno}: duplicate path {path!r} (first at line {seen_paths[path]})")
            continue
        seen_paths[path] = lineno
        # hash-format validation for adopted rows
        up, laf = _norm_hash(cells[2]), _norm_hash(cells[3])
        if cls.upper() in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
            if not _is_hex64(up) or not _is_hex64(laf):
                errors.append(f"manifest line {lineno}: {path!r} adopted row needs 64-hex hashes")
                continue
        else:  # NATIVE / BUILD-NEW
            if up != NO_HASH or laf != NO_HASH:
                errors.append(f"manifest line {lineno}: {path!r} {cls} row must have {NO_HASH} hashes")
                continue
        rows.append(Row(path, cls.upper(), up, laf))
    return rows, errors
```

Where:
- `CLASSES = {"ADOPTED-CLEAN","ADOPTED-PATCHED","NATIVE","BUILD-NEW"}`.
- `_is_hex64(c)` = `len(c)==64 and all(ch in "0123456789abcdef" for ch in c.lower())`.
- The `|`-in-cell problem: a literal `|` inside a path/hash is genuinely ambiguous in this 4-column pipe format. The spec does NOT introduce escaping (would change the manifest format); instead, the strict `len(cells) != 4` check above turns a `|`-shifted row into a loud failure (it will produce ≠4 cells), which satisfies M4's "fail loudly" intent. Document this in VENDOR.md: paths/hashes must not contain `|`.

**Caller changes:** Every `parse_manifest(read_text(VENDOR.md))` call site (`verify`, `do_init`, `do_report`) must handle the `(rows, errors)` tuple. In `verify` and `do_init`, manifest errors → boundary-contract FAIL (exit 1). In `do_report`, manifest errors → printed as warnings but `--report` STILL exits 0 (preserve L1/contract).

**Acceptance criteria:**
- A row with 3 or 5 cells → **FAIL** (not silently skipped).
- A duplicate path → **FAIL.**
- An adopted row with a 63-char or non-hex hash → **FAIL.**
- A NATIVE row with a real hash → **FAIL** (must be `—`).
- Current well-formed 64-row manifest → **PASS** (zero new errors).

---

### 4.7 CH-7 — Exercise Rule B's prefix-rewrite path (M5)

**Problem (M5):** `do_init` records `laf_sha256 = sha256(on-disk file)` but applies no `prefix_rewrite` (lines 259–264); it trusts the vendorer did it by hand. Every ADOPTED-CLEAN skill row shows `upstream_sha256 == laf_sha256` (the rewrite was a no-op for those files — they contain no `creative-writing-skills:` literal), so Rule B's `sha256(prefix_rewrite(upstream)) == laf_sha256` branch has no positive test. A future prefix-bearing file could be mis-vendored silently.

**Spec — two equally valid resolutions; task-builder picks ONE (§6 Q3):**

- **Option M5-A (test fixture, RECOMMENDED):** Add a self-contained test that constructs a fake upstream blob containing the literal `creative-writing-skills:`, runs `prefix_rewrite`, and asserts the Rule-B equality holds. This proves the rewrite machinery without touching `do_init`. Lowest risk.
- **Option M5-B (make `--init` perform the rewrite):** Have `do_init` actually apply `prefix_rewrite` when computing `laf_sha256` for adopted files, so the recorded hash reflects the transform. Higher risk: changes `--init` semantics and would invalidate every existing `laf_sha256` row that was hand-vendored. NOT recommended unless paired with a full re-vendor.

**Test location:** Create `laf-adaptation/scripts/test_check_boundary.py` (stdlib `unittest`, runnable via `uv run python scripts/test_check_boundary.py`). This is the one permitted new file. The test suite should ALSO cover CH-1 through CH-6 acceptance criteria (§5).

**Acceptance criteria:**
- A unit test with a `creative-writing-skills:`-bearing upstream blob → Rule-B equality holds after `prefix_rewrite`; FAILS if rewrite is skipped. This is the positive test M5 demands.

---

### 4.8 CH-8 — CI workflow + doc alignment (cross-cutting, P2)

**Spec — REQUIRED (doc only):** Update the `boundary.yml` header comment (lines 3–7) and `CLAUDE.md` §2 to accurately describe which rules run in CI Mode V after CH-1 (now including the `upstream_sha256` assertion), so the comment no longer understates the gate.

**Spec — RECOMMENDED (Option B, review H1 "or"):** Strengthen CI to Mode U by adding a step that checks out the upstream at the pinned SHA and runs `--upstream`:

```yaml
- name: Checkout upstream at pinned SHA
  run: git clone https://github.com/haowjy/creative-writing-skills /tmp/cws
       && git -C /tmp/cws checkout 3338495f0fabf778720effdda9386ab56d4ebf6e
- name: Boundary contract (verify, upstream-anchored)
  working-directory: laf-adaptation
  run: uv run python scripts/check_boundary.py --upstream /tmp/cws --upstream-sha 3338495f0fabf778720effdda9386ab56d4ebf6e
```

(Read the SHA from VENDOR.md rather than hardcoding — the task-builder may script a small extraction, or accept duplication with a comment.)

**Spec — OPTIONAL (L2, deferred but cheap if pulled in):** SHA-pin `actions/checkout@v4` and `astral-sh/setup-uv@v7`, and add `permissions: { contents: read }`. Documented in Appendix C; include only if the task-builder is explicitly authorized to absorb L2.

**Acceptance criteria:**
- REQUIRED: CI comment + CLAUDE.md §2 accurately describe the post-CH-1 gate.
- If Option B adopted: CI run log shows Rules B/C executed against the pinned-SHA checkout; CH-5 passes (HEAD matches pin).

---

## 5. Test Plan (Phase B task must include)

A new `laf-adaptation/scripts/test_check_boundary.py` (stdlib `unittest`) covering each acceptance criterion. Run via `uv run python scripts/test_check_boundary.py`. Required cases:

| Test | Finding | Asserts |
|------|---------|---------|
| `test_clean_corpus_passes` | — | Current VENDOR.md + tree → verify exit 0 (no regressions) |
| `test_adopted_body_edit_plus_laf_hash_rewrite_fails` | H1/CH-1 | Mutate body + rewrite `laf_sha256` only → exit 1 |
| `test_adopted_resource_row_deleted_fails` | H2/CH-2 | Delete a `resources/**` row → exit 1 |
| `test_untracked_adopted_resource_fails` | H2/CH-2 | Drop new file in adopted skill `resources/` → exit 1 |
| `test_patched_class_off_writer_fails` | M1/CH-3 | Non-writer `ADOPTED-PATCHED` row → exit 1 (both modes) |
| `test_path_traversal_rejected` | M2/CH-4 | `../../etc/x` row → exit 1 |
| `test_absolute_path_rejected` | M2/CH-4 | `/etc/x` row → exit 1 |
| `test_upstream_wrong_sha_fails` | M3/CH-5 | Mode U, checkout at wrong SHA → exit 1 |
| `test_malformed_row_fails` | M4/CH-6 | 3-cell / 5-cell row → exit 1 |
| `test_duplicate_path_fails` | M4/CH-6 | Duplicate path → exit 1 |
| `test_bad_hash_fails` | M4/CH-6 | 63-char / non-hex adopted hash → exit 1 |
| `test_native_with_hash_fails` | M4/CH-6 | NATIVE row with real hash → exit 1 |
| `test_prefix_rewrite_positive` | M5/CH-7 | `creative-writing-skills:` blob → Rule-B equality holds |
| `test_report_exits_0_on_malformed` | L1-touch | `--report` with malformed manifest → exit 0 (warnings printed) |

Tests must build a temp `REPO` tree (refactor permitting) or monkeypatch `REPO`/`VENDOR_MD` to a tmp fixture so they don't mutate the real tree. If refactoring `REPO` to be injectable is too invasive, run tests against a copied fixture dir under `tempfile`.

---

## 6. Open Questions for Phase B (task-builder MUST resolve before/while coding)

> These are the decisions a task-builder cannot infer from the review alone. Each is gated on a quick verification step.

- **Q1 (BLOCKER for CH-1):** Is `upstream_sha256` in VENDOR.md the hash of the RAW upstream blob or the PREFIX-REWRITTEN blob? Evidence: `--init` line 249 does `up_sha = sha256_text(up_raw)` (raw), and `agents/brainstormer.md` has `upstream_sha256=aa736c5d…` ≠ `laf_sha256=5c827eff…` (they differ, consistent with raw-vs-rewritten). **Verify by:** computing `sha256(prefix_rewrite(raw_upstream_brainstormer))` against the manifest's `upstream_sha256`. The answer determines CH-1's exact assertion formula. If `upstream_sha256` is the RAW hash (likely), then verify-mode Rule A′ must compare `sha256(prefix_rewrite(disk))` against a *stored* value — and since the disk file is already rewritten, `sha256(disk) == sha256(prefix_rewrite(raw_upstream))` only holds when raw upstream lacks the prefix literal. The clean resolution: **store BOTH `upstream_sha256_raw` (existing) AND assert against it by computing `sha256(prefix_rewrite(raw))` requires the upstream blob — which Mode V doesn't have.** Therefore the most robust CH-1 design is: add a third manifest column or use `--upstream` in CI (Option B). **The task-builder must choose between (a) adding a `laf_sha256_expected` baseline the PR cannot forge, (b) running Mode U in CI, or (c) accepting the review's "document it as accidental-drift gate" minimum.** This is the crux of H1 and must be settled with the maintainer.
- **Q2:** Project minimum Python version? (`Path.is_relative_to` needs 3.9+.) Check `pyproject.toml` / `.python-version`. Determines CH-4 helper implementation.
- **Q3:** CH-7 Option M5-A (test fixture) vs M5-B (rewrite in `--init`)? Recommend M5-A.
- **Q4:** Is Option B (Mode U in CI, CH-8) in scope for this cycle, or follow-up? Recommend: implement CH-1 floor now, file Option B as follow-up — UNLESS the maintainer wants the absolute guarantee immediately.

---

## 7. Sequencing & Dependencies (for the task-builder)

```
CH-6 (parser hardening)  ──┐
                           ├──► CH-1 (Rule A′) ──► CH-8 (doc/CI)
CH-4 (path safety)        ──┤        │
                           │        ▼
CH-3 (writer-only patch) ──┤   CH-7 (tests for ALL)
                           │
CH-2 (Rule F resources)  ──┤
                           │
CH-5 (upstream-sha, Mode U) ┘
```

- **CH-6 first:** parser hardening changes `parse_manifest`'s return signature (now `(rows, errors)`); every other change consumes parsed rows, so land it first.
- **CH-4, CH-3, CH-2, CH-5** are independent of each other; can be parallelized after CH-6.
- **CH-1** depends on the §6 Q1 resolution; lands after the parser.
- **CH-7** (tests) is developed alongside each change and is the gate for "done."
- **CH-8** lands last (documents the final behavior).

Recommended task granularity for MDTM: one task per CH-* (8 tasks), plus a final integration/verification task that runs the full test suite + a manual `uv run python scripts/check_boundary.py` on the real tree confirming exit 0.

---

## 8. Out of Scope / Deferred (Appendix C reference)

- **L1** (read_text / --report crash robustness) — touched only minimally by CH-6's `--report` exit-0 guarantee; full try/except wrapping deferred.
- **L2** (unpinned actions, no permissions block) — deferred unless CH-8 Option B is adopted and the maintainer absorbs it.
- **L3** (set-based frontmatter diff drops duplicate removals; unterminated-frontmatter edge) — deferred; functional impact is narrow.
- **NIT** (hardcoded NATIVE/BUILD-NEW name lists) — deferred; documented as known coupling.

These remain valid follow-ups; they are excluded only to keep this remediation cycle focused on the H1/H2/M1–M5 set the review prioritized.

---

## 9. Definition of Done (Phase B must verify ALL)

1. All 8 CH-* changes implemented per §4.
2. `laf-adaptation/scripts/test_check_boundary.py` exists and all §5 cases pass via `uv run python scripts/test_check_boundary.py`.
3. `uv run python scripts/check_boundary.py` (verify, Mode V) on the real tree → **exit 0** (no regression on the clean corpus).
4. `uv run python scripts/check_boundary.py --report` → **exit 0** (contract preserved).
5. §6 Q1–Q4 resolved and the chosen resolution recorded in the MDTM task.
6. `VENDOR.md` header + `CLAUDE.md` §2 + `boundary.yml` comment updated to match the remediated behavior (no absolute-guarantee language the gate doesn't actually deliver).
7. Pure-stdlib constraint preserved (ADR-006); no new runtime deps.

---

*End of remediation spec. Phase B (task-builder) consumes this directly; Phase A produced this document only and executed no fixes.*
