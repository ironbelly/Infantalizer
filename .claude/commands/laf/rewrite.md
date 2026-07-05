---
description: Begin the chapter rewrite phase for a work already prepped by /laf:prep.
argument-hint: --work <work-slug>
---

# /laf:rewrite

Read the prep package for `--work <slug>` by **hardcoded path** — no other arguments. Per
`laf-adaptation/skills/prep/resources/path-contract.md` §4 (`rewrite_phase_reads`), read exactly:

1. `work/prep/<slug>/30-mapping.yaml`      (the derived mapping, incl. top-level `meaning:`)
2. `work/prep/<slug>/40-prep-brief.md`     (decisions, cross-tier spine, answered questions)
3. `work/prep/<slug>/10-challenges.yaml`   (challenge taxonomy + per-tier strategy)

Then hand control to the `muse` agent for chapter 1 of the existing per-chapter 11-step workflow, with the
instruction: **"The prep package is your only context; do not ask the user to restate anything already
decided in it."** `muse` reads the mapping's inline per-entry confidence and top-level `meaning:` as data —
no `muse` edit, no new skill.

**Multi-chapter scope.** This command begins **chapter 1**; the existing per-chapter 11-step workflow
continues for chapters 2..N (each chapter re-reads the same prep package — `30-mapping.yaml`,
`40-prep-brief.md`, `10-challenges.yaml` — by the hardcoded `rewrite_phase_reads` paths).

**Guard.** Confirm `work/prep/<slug>/50-greenlight.md` shows `status: CONFIRMED` before handing to `muse`. A
`PENDING` (un-greenlit) package is not ready for rewrite — surface that and stop.
