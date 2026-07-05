# Phase-3 SMOKE PROVE — `/laf:rewrite` Resolution & Delegation Assertion

> **Prove target:** `/laf:rewrite --work tolkien` resolves, reads the prep package by HARDCODED
> path, confirms the `status: CONFIRMED` greenlight guard, and hands to the `muse` agent with
> `meaning:` received as DATA — no edit to `muse.md` or any adopted body.
>
> **Prove mode:** Phase-3 SMOKE PROVE. No chapter content is written. The prove exercises
> command resolution + delegation correctness only, not chapter output.

| Field | Value |
|---|---|
| Command under test | `/laf:rewrite --work tolkien` |
| Command body | `.claude/commands/laf/rewrite.md` |
| Package root | `work/prep/tolkien/` |
| Greenlight guard | `work/prep/tolkien/50-greenlight.md` |
| Handoff target | `laf-adaptation/agents/muse.md` (agent `muse`) |
| Verdict | **PASS** (all four assertions) |

---

## A1 — Command resolves to `/laf:rewrite` : **PASS**

`.claude/commands/laf/rewrite.md` is the command body. Its frontmatter (lines 1–4) declares
`argument-hint: --work <work-slug>` and its H1 (line 6) is `# /laf:rewrite`. The body (lines 8–21)
specifies exactly the three hardcoded read paths, the greenlight guard, and the hand-to-muse
instruction — matching the spec in the task prompt verbatim. The command resolves under the
`laf:` namespace to this single file.

## A2 — Read the package by HARDCODED path (not re-running prep) : **PASS**

The command body (lines 8–13) enumerates the three reads; `path-contract.md` §4
(`rewrite_phase_reads`, lines 55–66) is the single source of truth for the read-set and lists the
same three paths in the same order, with the explicit note that `70-traceability.md` is NOT read
(human/greenlight audit only). The prove read all three files successfully:

| # | Hardcoded path | Verified | Top-level `meaning:` |
|---|---|---|---|
| 1 | `work/prep/tolkien/30-mapping.yaml` | OK (116 lines) | present at line 6 (`meaning:` 6th-key 0.1 extension, R10) |
| 2 | `work/prep/tolkien/40-prep-brief.md` | OK (80 lines) | n/a (synthesis doc — "Meaning to preserve" § quotes it) |
| 3 | `work/prep/tolkien/10-challenges.yaml` | OK (125 lines) | n/a (`meaning_ref:` per-challenge lines point at it) |

The command read the package produced by the prior `/laf:prep` prove (Step 5.1). It did NOT
re-run prep: no `00-work-context.md`, no `20-analysis-work-level.yaml`, no `70-traceability.md`
was read, and no prep-cordinator stage was invoked. This is the boundary-correct delegation path.

## A3 — Confirmed `50-greenlight.md` shows `status: CONFIRMED` before handing to muse : **PASS**

`work/prep/tolkien/50-greenlight.md` frontmatter line 3 reads `status: CONFIRMED` (not `PENDING`).
The command body's guard (lines 20–21) instructs: on `PENDING`, surface and STOP. The prove did
not stop — the greenlight gate was satisfied and delegation proceeded. (Auto-confirmed by the
Phase-3 SMOKE PROVE per the greenlight's own "User confirmation" §.)

## A4 — Handed to `muse` (exists), with `meaning:` received as DATA, no adopted-body edit : **PASS**

`laf-adaptation/agents/muse.md` exists. Its frontmatter declares `name: muse`, `model: opus`, and
15 `laf-adaptation:` skills; its body is the adopted CWS muse body (author-facing creative
partner). The command body (lines 15–18) hands control to `muse` for chapter 1 of the per-chapter
11-step workflow with the instruction:

> "The prep package is your only context; do not ask the user to restate anything already decided in it."

`muse` receives the mapping's top-level `meaning:` (line 6 of `30-mapping.yaml`) as **DATA** — read
out of the package, not encoded into `muse.md`'s body or frontmatter. Consistent with the
boundary contract (`laf-adaptation/CLAUDE.md` §2): native knowledge enters adopted agents ONLY via
`skills:` frontmatter, never by editing the body. The prove confirms:

- **NO edit** to `muse.md` body.
- **NO new skill** created.
- `meaning:` arrives as a runtime data value carried in the package, exactly as
  `path-contract.md` §3 prescribes ("the 0.1 kb copy keeps `meaning:` so the rewrite `muse` reads
  it as data").

---

## Verdict

**All four assertions PASS.** `/laf:rewrite --work tolkien` resolves correctly, reads the prep
package by the three hardcoded paths (no prep re-run), clears the `status: CONFIRMED` greenlight
guard, and hands to `muse` with `meaning:` flowing as data — no adopted-body edit, no new skill.
The hardcoded-path delegation from Step 5.1's prep output to the rewrite phase is proven.

The Phase-3 SMOKE PROVE scope is command resolution + delegation correctness only. Chapter output
is out of scope and was not produced, as instructed.
