---
description: Onboard a new literary work — research, analyze, and derive its adaptation prep package.
argument-hint: "<novel title>" [--source <path-or-url>]
---

# /laf:prep

Delegate the entire run to the `prep-cordinator` agent (opus). Pass the positional `"<title>"` and, if
present, `--source <path>`.

The `prep-cordinator` owns the 8-stage procedure and the two HALT gates (question gate, greenlight). Do not
restate the pipeline here — it lives in `laf-adaptation/skills/prep/SKILL.md`. The output package path layout
is fixed by `laf-adaptation/skills/prep/resources/path-contract.md`.

If `--source` is omitted, the FIRST thing the coordinator does is elicit the source path as a **required
input** — the novel text is mandatory; there is no memory-based work-level analysis.

`--source` accepts a **local path**. A URL, if supplied, is fetched to a local file first; the
`source_path` the coordinator then runs `/source-fidelity` against is the resolved local path. (The
`argument-hint` `<path-or-url>` is kept verbatim per `prep-agent-schemas.md §5.1`.)
