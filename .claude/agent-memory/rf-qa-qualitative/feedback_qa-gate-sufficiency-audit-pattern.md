---
name: qa-gate-sufficiency-audit-pattern
description: How to audit a Rigorflow task file's QA gates for sufficiency (not just structure) — the checks rf-qa's structural PASS cannot reach
metadata:
  type: feedback
---

When auditing a Rigorflow task file's QA gates under the `qa-gate-sufficiency` lens, rf-qa's structural verdict ("gates present, agent counts ≥ floors, M3+M4 patterns present") is necessary but NOT sufficient. The semantic checks rf-qa cannot reach are:

1. **Filename vs path drift** — grep `producing \`<X>\` at \`<dir>/<Y>\`` pairs and diff the two basenames. rf-qa checks each path is well-formed but cannot catch intra-item name/path disagreement (e.g. line 394: `qa-structural-template-conformance-report.md` produced at `.../qa-structural-template-conformance-phase2-report.md`). Glob-based consolidation `qa-structural-*.md` masks this until an agent writes one name and a downstream reader looks for the other.

2. **Lens agent-type drift across gates** — the same lens can be filed as `rf-qa` (structural) in one gate and `rf-qa-qualitative` (content) in another. rf-qa checks "lens present in every gate" but not "lens filed under the same agent type in every gate." Example from LAF 0.1 task: boundary-contract-fidelity lens was `rf-qa` in PG0, `rf-qa-qualitative` in PG1/2/3/PC.

3. **Per-file coverage inside a gate** — an M4 source-fidelity gate can be "present and correctly placed" structurally yet leave specific carried-verbatim files with no assigned agent. Enumerate the files each agent claims and intersect against the full carried set; uncovered files (e.g. the Tolkien-instance mapping, the agency.md wrapper) are an AX-3 omission even though the gate structurally exists.

**Why:** These three defect classes are the gap between "structurally well-formed QA gates" and "QA gates that will actually catch the right errors at execution time." A structural PASS with any of these latent still produces silent consolidation misses or uncovered fidelity surface during the run.

**How to apply:** Run the three grep/read patterns above on every Rigorflow task file's QA-gate section before declaring the gates sufficient. They are cheap (3 greps + line-level reads of the gate headers) and catch defects the floor-count check cannot.
