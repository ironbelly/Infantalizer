# Boundary Facts — chapter-materialize NATIVE skill

Consolidated boundary-contract facts for adding the `chapter-materialize` NATIVE skill.
All facts copied VERBATIM from `research/02-boundary-contract-and-verification.md`. No fabrication.

Source: `.dev/tasks/to-do/TASK-RF-prep-chapter-materialize-20260709-004725/research/02-boundary-contract-and-verification.md`
Repo root: `/config/workspace/Infantalizer`

---

## 1. Exact VENDOR.md row (NATIVE)

Add EXACTLY ONE row into the NATIVE group of VENDOR.md:

```
| skills/chapter-materialize/** | NATIVE | — | — |
```

- **The em-dash character is U+2014 (EM DASH).** `NO_HASH = "—"` at `check_boundary.py:50`. The two
  placeholder hash cells MUST use U+2014 (`—`) — NOT U+2013 en-dash and NOT ASCII hyphen-minus U+002D.
  (The `-` inside a path like `chapter-materialize` is ASCII U+002D; the two hash cells are U+2014.)
  Use the em-dash `—` (U+2014) to match every existing NATIVE/BUILD-NEW row **byte-for-byte**.
- **The `/**` glob covers BOTH `SKILL.md` AND `resources/boundary-rules.yaml` (and every other file
  under `skills/chapter-materialize/`).** The single `skills/chapter-materialize/**` glob row satisfies
  Rule F coverage for `SKILL.md`, and Rule F′ (per-file coverage) skips NATIVE dirs entirely — it only
  iterates ADOPTED skill dirs. So **NO second row** and **no per-file / no `resources/` row** is added.

---

## 2. Zero `check_boundary.py` edits

**check_boundary.py: DO NOT EDIT.** A new NATIVE skill auto-classifies NATIVE.

- `classify()` default is NATIVE. At `check_boundary.py:368` the function returns `"NATIVE"` for any
  non-upstream skill whose name is NOT in `BUILD_NEW_SKILLS` (line 367 returns `"NATIVE"` inside the
  skills branch; line 368 is the final fall-through). `BUILD_NEW_SKILLS = {"adaptation-safety"}` (line 47),
  so `chapter-materialize` (not in that set) → NATIVE.
- **Do NOT touch `NATIVE_SKILLS` / `BUILD_NEW_SKILLS` / `classify()`.** `NATIVE_SKILLS` is NOT an
  allowlist — it is never read in the classification or verify paths. Existing NATIVE manifest rows
  `skills/prep/**` and `skills/thematic-fidelity/**` are NATIVE yet are NOT members of `NATIVE_SKILLS`,
  so a new NATIVE skill does not need to be added to `NATIVE_SKILLS` either.
- In plain verify mode (the AC6 command, no `--init`), classification is not even run — verify reads the
  class straight from the VENDOR.md manifest row. The manifest row is the source of truth.

---

## 3. AC6 verification command + PASS criterion

Exact invocation (working-directory `laf-adaptation`):

```
cd laf-adaptation && uv run python scripts/check_boundary.py
```

Success = **exit code 0** with stdout containing `BOUNDARY CONTRACT: PASS`.

This is Mode V (no `--upstream`), exactly what CI (`.github/workflows/boundary.yml`) and the opt-in
pre-commit hook run. Baseline PASSES today (captured read-only: `BOUNDARY CONTRACT: PASS — all rules
(A-F) satisfied.` / `EXIT_CODE=0`). AC6 must reproduce this same command, exit 0, and PASS line after
all edits.

---

## 4. Grep-assert for the 3 frozen `rewrite_phase_reads` paths

The rewrite phase reads EXACTLY these three files (from `skills/prep/resources/path-contract.md` §4).
Their byte-stability is NOT machine-enforced by `check_boundary.py`; assert it with a grep against the
three VERBATIM paths:

```
work/prep/<slug>/30-mapping.yaml
work/prep/<slug>/40-prep-brief.md
work/prep/<slug>/10-challenges.yaml
```

Grep-assert (order-independent, robust to surrounding edits):

```
f=laf-adaptation/skills/prep/resources/path-contract.md
grep -qF 'work/prep/<slug>/30-mapping.yaml'   "$f" \
  && grep -qF 'work/prep/<slug>/40-prep-brief.md' "$f" \
  && grep -qF 'work/prep/<slug>/10-challenges.yaml' "$f" \
  && echo "read-set OK"
```
