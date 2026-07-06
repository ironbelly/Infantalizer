---
title: "Boundary Contract — VENDOR.md + check_boundary.py"
parent: DESIGN.md
status: draft
---

# Boundary Contract

The boundary contract is the mechanism that keeps constraint #6 alive and mitigates the #1 residual risk
("just tweak an adopted agent"). It has two artifacts:

1. **`VENDOR.md`** — the manifest: upstream commit SHA + a per-file provenance table with hashes.
2. **`scripts/check_boundary.py`** — the gate: proves every adopted file matches its recorded hash, that
   `ADOPTED-PATCHED` files differ from upstream only in the permitted way, and that the quartet is intact
   (invariant G3).

> **Scope note.** This is the **only** script LAF 0.1 ships (ADR-006: prompt framework, not software).
> It is a *validation* tool, not a runtime — it reads files and computes hashes; it never transforms the
> framework. That keeps it inside the ADR-006 boundary.

---

## 1. Provenance classes

Every file under `agents/` and `skills/` carries exactly one class:

| Class | Meaning | `check_boundary.py` rule |
|---|---|---|
| `ADOPTED-CLEAN` | Vendored from CWS, byte-identical to the vendored baseline | `sha256(file) == laf_sha256`, and `laf_sha256 == upstream_sha256_after_prefix_rewrite` |
| `ADOPTED-PATCHED` | Vendored but carries the uniform prefix rewrite **and** a recorded additive frontmatter graft (only `writer.md`) | `sha256(file) == laf_sha256`; diff vs upstream is frontmatter-only + additive (§3.2) |
| `NATIVE` | LAF-authored | not hash-pinned to upstream; must NOT appear in the upstream tree |
| `BUILD-NEW` | Greenfield | not hash-pinned; must NOT appear in the upstream tree |

The **prefix rewrite** (`creative-writing-skills:` → `laf-adaptation:`) is the one uniform vendor-time
transform applied to all adopted files. It is deterministic, so the check recomputes it rather than
trusting a stored diff.

---

## 2. `VENDOR.md` format

```markdown
# VENDOR.md — Adopted-file manifest

upstream_repo: https://github.com/haowjy/creative-writing-skills
upstream_sha:  <full 40-char commit SHA the adopted subset was vendored from>
vendored_on:   2026-07-03
license:       Apache-2.0 (upstream) — attribution retained per NOTICE
prefix_rewrite: "creative-writing-skills:" -> "laf-adaptation:"   # uniform, deterministic

## Invariants (asserted by check_boundary.py)
- G3 quartet-intact: agents/{critic,editor,reader-sim,continuity-checker}.md are ADOPTED-CLEAN and present.
- editor.md is NEVER folded, NEVER modified.
- No NATIVE/BUILD-NEW file name collides with an upstream file name.

## Manifest

| path | class | upstream_sha256 | laf_sha256 |
|------|-------|-----------------|------------|
| agents/muse.md               | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/critic.md             | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/editor.md             | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/reader-sim.md         | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/continuity-checker.md | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/brainstormer.md       | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/outliner.md           | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/character-sim.md      | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/style-creator.md      | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/web-researcher.md     | ADOPTED-CLEAN   | <hash> | <hash> |
| agents/writer.md             | ADOPTED-PATCHED | <hash> | <hash> |
| skills/writing-principles/SKILL.md      | ADOPTED-CLEAN | <hash> | <hash> |
| skills/creative-writing-craft/SKILL.md  | ADOPTED-CLEAN | <hash> | <hash> |
| ... (all 12 adopted skills' SKILL.md + resources/**)           | ...   | ...    | ...    |
| agents/analyst.md            | NATIVE    | — | — |
| agents/safety-verifier.md    | NATIVE    | — | — |
| agents/chronicler.md         | BUILD-NEW | — | — |
| agents/tier-coordinator.md   | BUILD-NEW | — | — |
| skills/adaptation-tiers/**   | NATIVE    | — | — |
| skills/adaptation-rules/**   | NATIVE    | — | — |
| skills/source-fidelity/**    | NATIVE    | — | — |
| skills/adaptation-safety/**  | BUILD-NEW | — | — |
```

- `upstream_sha256` — hash of the file **in the upstream repo at `upstream_sha`** (before prefix rewrite).
- `laf_sha256` — hash of the file **as it lives in `laf-adaptation/`** (after prefix rewrite, and for
  `writer.md`, after the additive graft).
- For adopted skill directories, every file under `resources/` is hashed too (recursively), so a body
  edit to a resource is caught.

---

## 3. `scripts/check_boundary.py` — the gate

### 3.1 Modes

```
check_boundary.py            # verify: default; exit 1 on any violation (CI + pre-commit gate)
check_boundary.py --init     # first vendor: compute laf_sha256 for adopted files, write manifest rows
check_boundary.py --report   # human-readable provenance summary; always exit 0
```

`--init` runs once in Phase 0. It requires a local checkout of the upstream repo at `upstream_sha` (path
via `--upstream <dir>`) to record `upstream_sha256` and prove the prefix rewrite is the only
transformation.

### 3.2 Verify algorithm

```
load VENDOR.md manifest → rows[]
errors = []

# A. Adopted files match their recorded LAF hash (catches ANY edit, body or frontmatter)
for row in rows where class in {ADOPTED-CLEAN, ADOPTED-PATCHED}:
    if sha256(row.path) != row.laf_sha256:
        errors += f"{row.path}: modified since vendoring (laf_sha256 mismatch)"

# B. ADOPTED-CLEAN is exactly upstream-after-prefix-rewrite (no hidden graft)
for row in rows where class == ADOPTED-CLEAN:
    expected = sha256( prefix_rewrite( upstream_blob(row.path) ) )
    if row.laf_sha256 != expected:
        errors += f"{row.path}: ADOPTED-CLEAN but differs from upstream beyond prefix rewrite"

# C. ADOPTED-PATCHED diff is frontmatter-only AND additive
for row in rows where class == ADOPTED-PATCHED:
    up   = prefix_rewrite( upstream_blob(row.path) )   # upstream, prefix-normalized
    cur  = read(row.path)
    if body_of(cur) != body_of(up):                    # body = everything after closing '---'
        errors += f"{row.path}: body changed — adopted agent bodies must be byte-identical"
    added, removed = frontmatter_line_diff(up, cur)
    if removed:
        errors += f"{row.path}: frontmatter lines removed — patch must be additive only"
    if any(not line.strip().startswith('- laf-adaptation:') for line in added):
        errors += f"{row.path}: only additive `- laf-adaptation:<skill>` skill lines are permitted"

# D. Invariant G3 — quartet intact, editor never folded
for name in ["critic","editor","reader-sim","continuity-checker"]:
    p = f"agents/{name}.md"
    if p not in manifest or class(p) != "ADOPTED-CLEAN" or not exists(p):
        errors += f"G3 violation: {p} must exist as ADOPTED-CLEAN (quartet intact)"

# E. No native/build-new file name collides with an upstream file (prevents shadowing an adopted file)
for row in rows where class in {NATIVE, BUILD-NEW}:
    if upstream_has(row.path):
        errors += f"{row.path}: NATIVE/BUILD-NEW shadows an upstream file name"

# F. Every agents/*.md and skills/**/SKILL.md is listed in the manifest (no unmanaged files)
for f in glob("agents/*.md") + glob("skills/**/SKILL.md"):
    if f not in manifest: errors += f"{f}: not in VENDOR.md manifest"

exit(1 if errors else 0); print each error
```

**Key guarantees:**
- **Rule A** catches *any* change to an adopted file (the blunt hash gate).
- **Rule C** is the one that specifically permits `writer.md`'s single additive skill line and *nothing
  else* — body byte-identical, frontmatter additions restricted to `- laf-adaptation:<skill>` lines.
- **Rule D** hard-codes G3: the four quartet agents must be present and clean; `editor` can never be
  folded or edited.
- **Rule E** stops a contributor from "patching" an adopted agent by shadowing it with a native file of
  the same name.

### 3.3 `body_of` / `frontmatter_line_diff` (definitions)

- `body_of(text)` = everything after the second `---` delimiter line (the markdown body). Adopted bodies
  must match byte-for-byte.
- `frontmatter_line_diff(a, b)` = line-level added/removed sets computed on the YAML frontmatter block
  only, after prefix normalization. Order-insensitive for `skills:` list entries.

---

## 4. Enforcement points

| Point | Command | Blocking? |
|---|---|---|
| Pre-commit hook (`.githooks/pre-commit`, opt-in per clone) | `python3 scripts/check_boundary.py` | Yes — blocks the commit |
| CI (PR gate) | `python3 scripts/check_boundary.py` | Yes — fails the PR |
| Phase 0 vendor | `python3 scripts/check_boundary.py --init --upstream <dir>` | Writes manifest |
| Phase 3 hard gate | `check_boundary.py` green is one of the 5 gate conditions ([DESIGN.md §7](DESIGN.md)) | Yes |
| Phase 4 upstream-sync | re-run `--init` after re-pinning `upstream_sha`; diff adopted only | Re-pins manifest |

Per project rules, LAF uses UV: the pre-commit and CI invocations are `uv run python scripts/check_boundary.py`.

---

## 5. Upstream-sync protocol (Phase 4) — how the contract survives updates

```
1. Fetch upstream; pick new target SHA.
2. For each ADOPTED-CLEAN file: 3-way reconcile
     base = upstream@old_sha (prefix-rewritten)
     ours = laf file (== base, by contract)
     theirs = upstream@new_sha (prefix-rewritten)
   Since ours == base, apply theirs cleanly (fast-forward). Conflicts ⇒ manual cherry-pick.
3. For writer.md (ADOPTED-PATCHED): reapply the single additive skill line on top of theirs' body.
4. NEVER touch NATIVE / BUILD-NEW files during sync.
5. Re-run check_boundary.py --init to recompute hashes; update upstream_sha + vendored_on in VENDOR.md.
6. Re-run the Phase 3 hard gate before shipping the synced version.
```

Because adopted files are provably unmodified (ours == base), upstream patches apply without merge pain —
that is the entire payoff of the boundary contract. The moment an adopted file drifts, this fast-forward
degrades to manual cherry-pick, which is exactly the cost the contract is designed to prevent.
