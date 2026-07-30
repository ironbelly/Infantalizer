# CLAUDE.md — laf-adaptation

Guidance for AI agents (and humans) working in the `laf-adaptation/` tree.

> **Provenance of this file:** Structure adopted from the upstream CWS `CLAUDE.md`/`AGENTS.md`
> convention (a thin entry-point pointing at a conventions doc); content authored for LAF
> (Mars/Meridian layer removed). Upstream's `CLAUDE.md` is literally `@AGENTS.md`; LAF has **no
> AGENTS.md** (the Mars source layer is cut), so LAF's conventions live inline here. This file is
> NATIVE-authored and is **not** hash-pinned (it is outside the `check_boundary.py` Rule-F glob, which
> only covers `agents/*.md` and `skills/**/SKILL.md`).

LAF 0.1 is a **prompt + YAML-config framework — NOT software** (ADR-006). There is exactly **one**
script, `scripts/check_boundary.py`, and it is a *validation tool*, not a runtime. Do not add other
scripts or a CLI.

---

## 1. Provenance Model — every file is ADOPTED, NATIVE, or BUILD-NEW

| Class | What it is | Editing rule |
|-------|-----------|--------------|
| **ADOPTED** | CWS files vendored verbatim (patch-clean) from upstream `cw/`. The domain-agnostic review / orchestration / kb machinery. | **Never edit an adopted body.** The only permitted vendor-time transform is the uniform prefix rewrite `creative-writing-skills:` → `laf-adaptation:`. See `VENDOR.md` for the pinned manifest. |
| **ADOPTED-PATCHED** | Exactly one file: `agents/writer.md`. Adopted body, plus **one** additive `skills:` frontmatter line. | Frontmatter-additive only (`- laf-adaptation:<skill>`); body text-normalized (LF) identical to upstream. |
| **NATIVE** | LAF-authored files carrying the domain-specific adaptation spine: tier axis, source-fidelity, transformation rules. `agents/analyst.md`, `agents/safety-verifier.md`; skills `adaptation-tiers`, `adaptation-rules`, `source-fidelity`. | Author freely; not hash-pinned; must not collide with an upstream file name (Rule E). |
| **BUILD-NEW** | Greenfield in *both* systems: tier-aware canon extraction and cross-tier reconciliation. `agents/chronicler.md`, `agents/tier-coordinator.md`; skill `adaptation-safety`. | Author freely; not hash-pinned; must not collide with an upstream file name (Rule E). |

**If you think you must edit an adopted file: STOP. Add a skill instead** and attach it via the agent's
`skills:` frontmatter. That is the whole point of the boundary contract (below).

**Present-state (0.1 DONE — the complete tree exists now).** All counts below are **live**, not targets.
The tree holds **15 agent files** (11 adopted-provenance = 10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED
`writer.md`; 2 NATIVE = `analyst`, `safety-verifier`; 2 BUILD-NEW = `chronicler`, `tier-coordinator`)
and **16 skill dirs** (12 ADOPTED; 3 NATIVE = `adaptation-tiers`, `adaptation-rules`, `source-fidelity`;
1 BUILD-NEW = `adaptation-safety`). The NATIVE and BUILD-NEW files named in the table above are all
present. (Built across Phases 0–2; 0.1 is DONE.)

The authoritative per-file classification + hashes live in [`VENDOR.md`](VENDOR.md).

**Non-manifested files (outside the Rule-F hash-pin glob).** The `check_boundary.py` Rule-F glob only
hash-pins `agents/*.md` and `skills/**/SKILL.md`. Everything else is intentionally *not* manifested, and
is classified as follows:

- `scripts/` — **NATIVE** tooling. Exactly one script (`check_boundary.py`) per ADR-006; not a runtime.
- `kb/tiers/` + `kb/adaptation-mapping/` — **NATIVE** carried-verbatim YAML (text-normalized (LF)
  faithful copies of LAF's `config/`).
- `kb/adaptations/<work>/tier-<N>/` — **NATIVE** graft G1.
- `kb/` adopted layers (`canon/`, `characters/`, `world/`, `timeline/`, `styles/`, `vocab.md`, `issues/`)
  — **ADOPTED** scaffold (runtime-populated).
- `templates/` — **NATIVE** (carried verbatim).
- `source/` — **BUILD-NEW**.
- `NOTICE` / `LICENSE-CWS` — Apache-2.0 **attribution**.
- `CLAUDE.md` / `VENDOR.md` / `UPSTREAM-SYNC.md` — **NATIVE** docs.

These are intentionally outside the Rule-F hash-pin glob: only adopted `agents/*.md` and
`skills/**/SKILL.md` bodies are hash-pinned, because those are the patch-clean, upstream-syncable subset.

**Adopted-provenance count (11 = 10 ADOPTED-CLEAN + 1 ADOPTED-PATCHED).** Of the 15 agents, **11 are
adopted-provenance**: 10 are ADOPTED-CLEAN (vendored text-normalized (LF) identical after the prefix rewrite) and exactly
**1 is ADOPTED-PATCHED (`agents/writer.md`)** — adopted body plus one additive `skills:` frontmatter line.
The remaining 4 are 2 NATIVE + 2 BUILD-NEW.

**New files inside an ADOPTED skill's `resources/` tree.** A file authored inside an adopted skill's
`resources/` subtree is a **NATIVE addition**: it must NOT collide with an upstream filename (Rule E) and
is not hash-pinned. **Prefer adding a NATIVE skill** over dropping a file inside an adopted skill dir — a
standalone NATIVE skill keeps the adopted skill's tree patch-clean and honors the boundary contract; a
new file inside an adopted dir muddies the upstream-sync boundary even though it is technically permitted.

**Why VENDOR.md has more rows (68) than the Rule-F glob set (31).** The Rule-F *coverage* requirement is
the 31-file glob (`agents/*.md` + `skills/**/SKILL.md`). The VENDOR.md manifest is broader: it also hashes
adopted skill `resources/**` files (needed for Rules A/B upstream-diff integrity), so the manifest carries
**more rows than Rule-F's coverage set**. Rule F asserts every managed file is *manifested*; it does not
cap the manifest at the glob — hashing `resources/**` is a superset that strengthens (never weakens) the
integrity check.

**Design-pack references are build-time provenance, not runtime dependencies.** Citations throughout this
tree to `DESIGN.md`, `boundary-contract.md`, `kb-formats.md`, `safety-rubric.md`, `skill-specs.md`,
`agent-schemas.md`, `tier-coordinator.md`, and `ADR-006` point at the **build-time design pack** that
lives under `.dev/releases/current/0.1/design/` — the record of *where each contract was designed*. They
are **provenance pointers, not files you need to resolve to contribute**: the shipped `laf-adaptation/`
tree is self-sufficient (every runtime contract is restated in the in-tree agent/skill bodies). If a `§`
reference is unreachable from the shipped tree, that is expected — read the in-tree skill/agent body,
which is the single source of truth at execution time.

---

## 2. Boundary Contract (constraint #6 — the load-bearing rule)

**NATIVE knowledge enters ADOPTED agents ONLY via `skills:` frontmatter — never by editing an adopted
agent's body.** This is what keeps the adopted subset patch-clean and upstream-syncable (a 3-way merge
against upstream stays a clean fast-forward as long as adopted bodies never drift — see
[`UPSTREAM-SYNC.md`](UPSTREAM-SYNC.md)).

- The **one** demonstration of the contract is `agents/writer.md` (ADOPTED-PATCHED): it gets a single
  additive line `- laf-adaptation:adaptation-rules` and nothing else. Its body is text-normalized (LF)
  identical to upstream; even upstream quirks (e.g. its duplicate `creative-writing-craft` skill line) are preserved
  verbatim, not "fixed".
- **Enforcement:** `uv run python scripts/check_boundary.py` (verify mode, "Mode V"). It exits non-zero
  on any violation of:
  - **A** — every adopted file matches its recorded `laf_sha256` (catches any accidental edit).
  - **A′** (CH-1) — every ADOPTED-CLEAN body re-derives, via the inverse prefix rewrite
    (`laf-adaptation:` → `creative-writing-skills:`), to its pinned `upstream_sha256`. This re-anchors
    adopted-file integrity to the **upstream-derived** hash rather than the self-referential
    `laf_sha256`: a commit that edits an adopted body AND rewrites only its `laf_sha256` row now FAILS
    (the body no longer matches the pinned `upstream_sha256`). Forging `upstream_sha256` is a loud,
    review-visible change to a field documented as upstream-derived. Mode V is therefore a
    **single-field `laf_sha256`-forgery gate**. It does **NOT** catch a **two-field forgery**
    (rewriting BOTH `laf_sha256` AND `upstream_sha256` to be self-consistent) — that bypasses Mode V
    by construction and is caught only by Mode U (Rules B/C against a pinned-SHA upstream checkout)
    plus branch protection + mandatory human review of any `upstream_sha256` diff. See `VENDOR.md`
    "Hash semantics" for the full honest statement of what Mode V does and does not close.
  - **C′** (CH-3) — `ADOPTED-PATCHED` is reserved for `agents/writer.md` only.
  - **D** — G3 quartet intact (`critic`/`editor`/`reader-sim`/`continuity-checker` ADOPTED-CLEAN) and
    `editor.md` never folded.
  - **E** — no NATIVE/BUILD-NEW name collides with an upstream file.
  - **F / F′** (CH-2) — every `agents/*.md` and `skills/**/SKILL.md` is manifested, AND every file
    under an adopted skill's `resources/**` is manifested.
  - Parser hardening (CH-6) + path safety (CH-4): malformed / duplicate / bad-hash rows and
    path-traversal / absolute manifest paths FAIL loud.
  In **Mode U** (`--upstream <checkout>`), Rules B/C additionally run a full upstream diff, and CH-5
  asserts the checkout `HEAD` == VENDOR.md's pinned `upstream_sha`. Mode U is the absolute guarantee;
  it is not (yet) run in CI — see `.github/workflows/boundary.yml` and `VENDOR.md`. The pre-commit hook
  (`.githooks/pre-commit`, opt-in) and CI both run Mode V.
- **Enabling the opt-in hook:** `git config core.hooksPath laf-adaptation/.githooks` (run once, from the
  git repo root). To bypass the hook for a single commit: `git commit --no-verify`.
- **CI location:** the CI workflow lives at the **git repo root** as `.github/workflows/boundary.yml`
  (NOT under `laf-adaptation/` — `laf-adaptation/` is a subdirectory of the repo). The workflow runs the
  boundary check with `working-directory: laf-adaptation`.

---

## 3. LAF Conventions

- **Frontmatter dialect: Claude-native (cw-lowered), NOT Mars.** All agent/skill frontmatter uses the
  Claude Code dialect. Agents: `name`, `description`, `model` (∈ {opus, sonnet, haiku, inherit} — never a
  Mars alias), `skills` (fully-qualified `laf-adaptation:<skill>`), `tools`. Skills: `name` + `description`
  only. **Never** introduce Mars keys — `type`, `model-invocable`, `effort`, `model-policies`, `sandbox`,
  `subagents`. Adopted agents are vendored from CWS `cw/agents/` (already Claude-lowered), never from the
  Mars `agents/` source.
- **The tier axis is first-class, but agents consume the tier differently.** `active_tier` is an
  explicit declared input for **`safety-verifier`** and **`chronicler`**. **`tier-coordinator`** does not
  take a single `active_tier` — it fans across a **`tiers` set** (a subset of {1,2,3,5}) to reconcile
  renderings. **`writer`** is ADOPTED-PATCHED, so it takes no LAF frontmatter tier param; it receives the
  operative tier via its **scene brief + `/adaptation-rules`**, not a declared parameter. **`analyst` is
  tier-invariant — it takes NO `active_tier`** (it produces one shared, tier-neutral source analysis that
  every tier's transform reads). Tier profiles live in `kb/tiers/` (`tier_1/2/3/5.yaml`). **Tier 4 is
  interpolated at request time (T3 floor, T5 ceiling, conservative midpoint;
  `agency_externalization = FORBIDDEN`) — never stored as a file.**
- **Carried-verbatim = zero rework.** Port-source YAMLs (`kb/tiers/*.yaml`, `kb/adaptation-mapping/*`,
  the transformation-rule resources) are text-normalized (LF) faithful copies of LAF's `config/` — including deliberate
  schema drift (T1-T3 `conflict_to_cooperation`/`death_euphemism` vs T5 `conflict_handling`/
  `death_handling`). Normalization belongs in the *reader* skills (key-tolerant `.get(a) or .get(b)`),
  never in the vendored file.
- **UV-only for Python.** Always invoke the script as `uv run python scripts/check_boundary.py`. Never
  `python -m`, bare `pip`, or `python script.py`.
- **One flat tree.** Claude Code reads `laf-adaptation/` directly. CWS's Mars/plugin packaging
  (`mars.toml`, the `cw/` mirror, sync scripts) is cut.

### The 6 constraints (where each is mechanized — DESIGN §5)

1. **Tier axis first-class** — `active_tier` explicit param; `kb/tiers/` a native kb layer, never dissolved into persona/genre.
2. **Uncertainty discipline** — `analyst` Phase-0 ABORT-on-NO-ACCESS; `/source-fidelity` mandates CERTAIN/PROBABLE/UNCERTAIN tags before any transform.
3. **safety_check** — `safety-verifier` agent + `/adaptation-safety` rubric; the verdict contract blocks kb promotion on FAIL.
4. **Quartet (4 distinct) + 5th** — critic/editor/reader-sim/continuity-checker vendored as 4 distinct adopted files; `safety-verifier` is a distinct 5th native reviewer, never merged. G3 invariant: `editor.md` present & unmodified, asserted by `check_boundary.py`.
5. **work/ vs kb/ split** — adopted `kb-management` lifecycle; `chronicler` writes to `kb/` **only on muse-accept**; native subdirs (`work/analysis`, `work/safety-reports`) live under `work/`.
6. **skill-vs-agent (boundary contract)** — `check_boundary.py` proves adopted bodies match `VENDOR.md` hashes; native knowledge enters only via `skills:` frontmatter.

---

## 4. Where things live

```
laf-adaptation/
├── CLAUDE.md            # this file (NATIVE; not hash-pinned)
├── VENDOR.md            # BOUNDARY CONTRACT: pinned upstream SHA + per-file manifest
├── NOTICE               # Apache-2.0 attribution for the vendored CWS subset
├── LICENSE-CWS          # full Apache-2.0 text accompanying the vendored files
├── UPSTREAM-SYNC.md     # the 6-step upstream-sync procedure
├── agents/              # 15 agent files: 11 adopted-provenance (writer.md ADOPTED-PATCHED) + 2 NATIVE (analyst, safety-verifier) + 2 BUILD-NEW (chronicler, tier-coordinator)
├── skills/              # 16 skill dirs: 12 ADOPTED + 3 NATIVE (adaptation-tiers, adaptation-rules, source-fidelity) + 1 BUILD-NEW (adaptation-safety)
├── kb/
│   ├── canon/ characters/ world/ timeline/ styles/ vocab.md issues/   # ADOPTED layers (runtime-populated)
│   ├── tiers/                     # NATIVE: tier_1/2/3/5.yaml (T4 interpolated, never stored)
│   ├── adaptation-mapping/        # NATIVE: universal-mappings.yaml + <work>-mapping.yaml (cascade)
│   └── adaptations/<work>/tier-<N>/   # NATIVE graft G1: per-tier canon, keyed (work, tier, chapter)
├── source/              # BUILD-NEW: the work being adapted (read-only reference)
├── work/                # ADOPTED lifecycle: analysis/ (NATIVE) drafts/ critique-reports/ safety-reports/ (NATIVE)
├── templates/           # work-mapping-template.yaml (NATIVE, carried verbatim)
├── scripts/             # check_boundary.py — the ONLY script (boundary-contract enforcement)
└── .githooks/pre-commit # opt-in enforcement wrapper
```
