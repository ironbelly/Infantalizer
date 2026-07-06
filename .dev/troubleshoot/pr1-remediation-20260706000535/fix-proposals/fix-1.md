# Fix Proposal 1 — H1: manifest_covers class-aware + glob restriction + regression test

## Problem
`manifest_covers` (`check_boundary.py:296`) treats any `/**` row as covering any matching path with **no class check**. Rule A only hash-checks adopted rows; Rule D protects only the quartet. A manifest edit replacing an exact `agents/foo.md | ADOPTED-CLEAN | <h> | <h>` row with `agents/** | NATIVE | — | —` would: (a) satisfy Rule F coverage via the glob, (b) no longer hash-check `foo.md`, (c) not trip Rule D. The parser only *emits* `/**` for NATIVE/BUILD-NEW skills (line 407) but **does not reject** `agents/**` or adopted-path globs. No regression test covers this.

## Proposed change (3 parts, all in `laf-adaptation/`)

### Part A — parse-time glob restriction
In `parse_manifest`, after the class-specific hash validation block (currently lines 266-273), add: if `path.endswith("/**")` (a glob row) AND `cls` is not in `{NATIVE, BUILD-NEW}`, FAIL loud with `"glob rows are reserved for NATIVE/BUILD-NEW skills"`. Additionally, restrict the glob *shape*: a glob row must match `skills/<name>/**` (i.e. start with `skills/` and end with `/**`); reject `agents/**`, root-level `**`, etc.

```python
# After line 274, before rows.append — actually integrate into the validation:
if path.endswith("/**"):
    if cls.upper() in ("ADOPTED-CLEAN", "ADOPTED-PATCHED"):
        errors.append(f"manifest line {lineno}: glob row {path!r} cannot be ADOPTED (adopted files need exact hash rows)")
        continue
    if not path.startswith("skills/"):
        errors.append(f"manifest line {lineno}: glob row {path!r} must be under skills/ (only 'skills/<name>/**' is allowed)")
        continue
```

### Part B — class-aware manifest_covers
Make `manifest_covers` require that a path is covered either by an exact row OR by a glob row whose class is NATIVE/BUILD-NEW (it already only gets those after Part A, but make the predicate self-defending):

```python
def manifest_covers(rows, rel: str) -> bool:
    for r in rows:
        if r.path == rel:
            return True
        if r.is_glob and rel.startswith(r.path[:-2]) and not r.is_adopted:
            return True
    return False
```

### Part C — regression test
Add a `GlobSafetyTests(BoundaryTestBase)` class to `test_check_boundary.py` with ≥2 tests:
1. `test_agents_glob_rejected`: inject `| agents/** | NATIVE | — | — |` → assert `verify() != 0` and error mentions glob/skills.
2. `test_adopted_glob_rejected`: inject `| agents/writer.md/** | ADOPTED-CLEAN | <64hex> | <64hex> |` → assert fail.
3. `test_broad_glob_does_not_cover_adopted`: build a tree where an adopted agent is "covered" only by a (rejected) glob — assert the parser catches it before coverage even runs.

## Evidence
- `check_boundary.py:296-302` (`manifest_covers`, class-agnostic)
- `check_boundary.py:177-178` (`is_glob` = `endswith("/**")`)
- `check_boundary.py:407` (only NATIVE/BUILD-NEW emit `/**`, but no parse-time gate)
- `check_boundary.py:499-507` (Rule A iterates `is_adopted` only)
- `check_boundary.py:603-608` (Rule D = quartet only)

## Risks
- **Low.** Part A only rejects shapes that are already never legitimately produced by `--init`. The shipped VENDOR.md has no `agents/**` rows, so this is purely additive hardening.
- Part B's `not r.is_adopted` is belt-and-suspenders; Part A is the real gate.
- Must re-run `verify()` after the change to confirm the live manifest still passes (it will — no glob rows exist for adopted paths today).

## Test plan
1. `uv run python scripts/test_check_boundary.py` → all 25 existing + 3 new tests pass.
2. `uv run python scripts/check_boundary.py` → still exits 0 (PASS) on the live tree.
