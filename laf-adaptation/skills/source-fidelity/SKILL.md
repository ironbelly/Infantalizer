---
name: source-fidelity
description: |
  The v2.0 anti-hallucination protocol for source analysis. Mandates CERTAIN/PROBABLE/UNCERTAIN
  confidence tags on every extracted fact, a source-access declaration with ABORT-on-NO-ACCESS, and a
  dual-pass documentation procedure. Load before any source transform. Transparent uncertainty > false
  certainty.
---

# Source Fidelity — v2.0 Pragmatic Verification Protocol

Principle: **Transparent uncertainty > false certainty.** Every fact you extract carries a confidence tag.

## Confidence tags
| Tag | Meaning |
|-----|---------|
| CERTAIN   | Directly quoted from text |
| PROBABLE  | Multiple observations support |
| UNCERTAIN | Inferred or reconstructed |

## Phase 0 — Source Declaration
Declare SOURCE ACCESS LEVEL (exactly one):
  FULL ACCESS · PARTIAL ACCESS · MEMORY-BASED · NO ACCESS
- MEMORY-BASED ⇒ every output item MUST be tagged UNCERTAIN.
- NO ACCESS   ⇒ ABORT. Do not produce analysis.        ← constraint #2 hard gate

### Observable-test decision rule (how to pick the access level)
The four levels above are declared by an **observable test** on the passed `source_path`, not by feel:

| Level | Observable test |
|-------|-----------------|
| FULL ACCESS  | `source_path` was passed, the file **exists, is readable, and is non-empty** (readable end-to-end). |
| PARTIAL ACCESS | The file **exists but is truncated or partially unreadable** (readable but incomplete — e.g. only part of the chapter is present). Tag facts drawn from missing regions UNCERTAIN. |
| NO ACCESS    | The file is **missing or empty** (path does not resolve, or resolves to a zero-length/unreadable file) ⇒ **ABORT** (emit `status: ABORTED`). |
| MEMORY-BASED | The caller passed **no source file at all**, or explicitly flagged the request as reconstruction/from-memory ⇒ every output fact tagged UNCERTAIN. |

Evaluate top-to-bottom and pick the **first** level whose test holds. This is the operational reading of
the declaration rule above; it does not relax the ABORT gate — missing/empty still aborts.

## Phase 1 — Essential Verification
Title, chapter number, chapter title (each: value + confidence). Opening & closing sentence + confidence.

## Phase 2 — Dual-Pass Documentation
PASS ONE (structure/events): major characters (role + confidence); 5-10 sequential events (+ confidence).
PASS TWO (summary): 100-150 word summary with overall confidence.

## Phase 3 — Transformation Flags
Flag categories present: violence, death, emotional intensity, abstraction — each with instances + severity.

## Phase 4 — Consistency Check
Characters logical · timeline coherent · locations consistent.

## Output schema — `work/analysis/ch-<NN>.yaml`

The `analyst` agent emits this (carried from `chapter_analysis.md`'s YAML output block, extended with the
`status` field for the ABORT gate). The analyst and this skill agree on this exact contract:

```yaml
status: OK | ABORTED            # ABORTED ⇒ NO-ACCESS; downstream halts
metadata:
  work: <work>
  chapter: <NN>
  source_access: FULL | PARTIAL | MEMORY-BASED | NO-ACCESS
  confidence: CERTAIN | PROBABLE | UNCERTAIN     # overall
essentials:
  title:   {value: "...", confidence: CERTAIN}
  chapter_title: {value: "...", confidence: PROBABLE}
  opening_sentence: {value: "...", confidence: CERTAIN}
  closing_sentence: {value: "...", confidence: CERTAIN}
characters:
  - {name: "...", role: "...", confidence: CERTAIN}
events:
  - {seq: 1, event: "...", confidence: CERTAIN}
summary: {text: "...", confidence: PROBABLE}
transformation_flags:
  violence:  {instances: N, severity: low|med|high}
  death:     {instances: N, severity: low|med|high}
  emotional: {instances: N, severity: low|med|high}
  abstract:  {instances: N, severity: low|med|high}
uncertainties:
  - "list of items the analyst could not verify"
```

## Overall confidence derivation
The `metadata.confidence` field (and Phase 2's "overall confidence") is **not** a fresh judgment — it is
**derived as the lowest/worst-case tag present across the essentials**. Order the tags CERTAIN > PROBABLE >
UNCERTAIN and take the **minimum**: if any essential fact is UNCERTAIN, overall = UNCERTAIN; else if any is
PROBABLE, overall = PROBABLE; only when **all** essentials are CERTAIN is overall = CERTAIN. This makes the
overall tag mechanical and conservative — one uncertain essential drags the whole analysis's confidence
down, by design.

Note on citations: any cross-tree `§`-style reference in this skill (e.g. to `skill-specs.md` or
`chapter_analysis.md`) is **build-time design-pack provenance**, not a runtime dependency. The in-tree
skill body is **self-sufficient**: everything needed to run the protocol is present here.

## Tag propagation
These CERTAIN/PROBABLE/UNCERTAIN tags flow downstream through the **adopted** `story-memory`
fact-extraction carrier (native tag, adopted carrier) — with **no edit to `story-memory`**; the tags are
just data in the facts it extracts. The boundary contract is preserved: the native uncertainty discipline
rides on the adopted carrier without modifying it.
