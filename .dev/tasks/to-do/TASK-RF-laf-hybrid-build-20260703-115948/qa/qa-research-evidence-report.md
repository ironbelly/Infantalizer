# QA Research — Evidence-Quality Report

**Lens:** evidence-quality (research-gate)
**Stance:** adversarial / zero-trust
**fix_authorization:** false
**Date:** 2026-07-03
**Reviewer scope:** 01-file-inventory-target-tree.md, 02-native-agents-skills.md, 03-buildnew-agents-safety.md, 04-kb-layers-portsource.md, 05-boundary-contract-script.md, 06-proof-gate-workflow-template.md

**Ground truth:** `.dev/releases/current/0.1/design/` (DESIGN.md, agent-schemas.md, skill-specs.md, kb-formats.md, boundary-contract.md, safety-rubric.md, tier-coordinator.md) + LAF port-sources at `config/`, `prompts/`, `templates/`.

**Method:** Every research file read in full. Directed spot-checks (R2/R3 frontmatter vs agent-schemas.md; R4 tier key-drift vs actual YAML; R5 rules A–F vs boundary-contract.md §3.2; R6 MDTM path existence; R1 manifest reconciliation vs boundary-contract.md §2). Findings appended incrementally below.

---

## Findings

### Spot-check coverage (all directed checks + broad sampling)

Verified references by opening the ground-truth source, not trusting the research prose. Coverage well exceeds the 20% floor: ~40+ distinct citations resolved across all 7 spec files + 6 port-source YAMLs + filesystem-absence claims.

| # | Claim checked | Research file | Ground truth | Result |
|---|---|---|---|---|
| SC-1 | tier_1 uses `conflict_to_cooperation`(66)/`death_euphemism`(73); tier_5 uses `conflict_handling`(58)/`death_handling`(61) | R4 §1.3 | tier_1_preschool.yaml L66/L73; tier_5_young_adult.yaml L58/L61 | **EXACT MATCH** ✓ |
| SC-2 | tier_2 `conflict_to_cooperation`(60)/`death_euphemism`(68); tier_3 (66)/(69) | R4 §1.3 | grep confirmed L60/68, L66/69 | **EXACT MATCH** ✓ |
| SC-3 | analyst frontmatter verbatim (agent-schemas.md:50-61) | R2 FILE 1 | agent-schemas.md:50-61 | **VERBATIM** ✓ |
| SC-4 | safety-verifier frontmatter (agent-schemas.md:87-97), inputs incl. active_tier (99-100), tier-gate (102-107) | R2 FILE 2 | agent-schemas.md:87-107 | **VERBATIM** ✓ |
| SC-5 | writer vendored form incl. duplicated `creative-writing-craft` line (agent-schemas.md:157-172) | R2 FILE 6 | agent-schemas.md:141-172 (upstream dup at 143-144 preserved) | **VERBATIM** ✓ |
| SC-6 | chronicler frontmatter `model: sonnet`, NO Bash (agent-schemas.md:222-233) | R3 FILE 1 | agent-schemas.md:222-233 (tools: Read,Write,Glob,Grep) | **VERBATIM** ✓ |
| SC-7 | tier-coordinator frontmatter `model: opus`, HAS Bash (agent-schemas.md:264-275) | R3 FILE 2 | agent-schemas.md:264-275 (tools incl. Bash) | **VERBATIM** ✓ |
| SC-8 | check_boundary.py rules A–F (boundary-contract.md §3.2) | R5 §3.2 | boundary-contract.md:108-151 | **VERBATIM** ✓ |
| SC-9 | VENDOR.md format, 5 header fields, G3 invariants (boundary-contract.md §2) | R5 §2 | boundary-contract.md:42-88 | **VERBATIM** ✓ |
| SC-10 | body_of / frontmatter_line_diff, order-insensitive skills: (boundary-contract.md:162-167) | R5 §3.4 | boundary-contract.md:162-167 | **VERBATIM** ✓ |
| SC-11 | MDTM template resolved pipx path exists | R6 §0 | `/config/.local/share/pipx/.../02_mdtm_template_complex_task.md` (120364 bytes, present) | **RESOLVES** ✓ |
| SC-12 | `.claude/templates/` does NOT exist | R6 §0 | `ls` → No such file or directory | **CONFIRMED** ✓ |
| SC-13 | no `source/` dir, no `ch-*.txt` fixtures | R6 §4 | `ls`/`find` → absent | **CONFIRMED** ✓ |
| SC-14 | "13 adopted agents/skills copied unchanged" (DESIGN.md:70) | R1 §E | DESIGN.md:70 verbatim | **CONFIRMED** ✓ |
| SC-15 | "(11 agents, 16 skills)" header + 15-file tree (DESIGN.md:52, 106-116) | R1 §A/§E | DESIGN.md:52, ASCII 55-67, tree 106-116 | **CONFIRMED** ✓ |
| SC-16 | Phase-0 "6 adopted review/orch agents + 12 adopted skills" (DESIGN.md:293) | R1 §E.3 | DESIGN.md:293 verbatim | **CONFIRMED** ✓ |
| SC-17 | "deliberately small (13)" (DESIGN.md:283) | R1 §E | DESIGN.md:283 verbatim | **CONFIRMED** ✓ |
| SC-18 | boundary manifest = 11 adopted agent rows + "all 12 adopted skills" (boundary-contract.md:60-73) | R1 §E.1 | boundary-contract.md:60-73 | **CONFIRMED** ✓ |
| SC-19 | tier-coordinator Inputs/Outputs, fan-out §2, reconcile A/B/C §3, report §4 | R3 FILE 2 | tier-coordinator.md:19-147 | **VERBATIM** ✓ |
| SC-20 | safety rubric 6 sections + word-lists + auto-fails + aggregation + verdict §4 | R3 FILE 6 | safety-rubric.md:19-130 | **VERBATIM** ✓ |
| SC-21 | universal_mappings 9 concepts at exact lines + tier_4_5 `[preserve]` collapse | R4 §2.1 | universal_mappings.yaml L4/10/16/22/28/34/40/46/52; preserve at 8/14/20/26/32/38/44/50/56 | **EXACT MATCH** ✓ |
| SC-22 | tolkien_mapping has 5 top-level keys, not "Four" as prose claims | R4 §2.2 / §5.2 | tolkien_mapping.yaml L4/13/43/64/77 = 5 keys; kb-formats.md:147 literally says "Four" | **CONTRADICTION CONFIRMED** ✓ |
| SC-23 | 5 Phase-3 gate conditions (DESIGN.md:296) | R6 §5 | DESIGN.md:296 verbatim (v2.0 tags·safety PASS·per-tier canon·all four quartet·check_boundary green) | **VERBATIM** ✓ |
| SC-24 | "real Tolkien chapter" phrasing (DESIGN.md:282, 296) | R6 §4 | DESIGN.md:282, :296 | **CONFIRMED** ✓ |
| SC-25 | agent-schemas.md §2.2 verdict is abbreviated vs safety-rubric.md §4 full form | R3 note | agent-schemas.md:112-119 (short) vs safety-rubric.md:96-115 (full) | **CONFIRMED — genuine variance, correctly flagged** ✓ |

### Per-file evidence-quality assessment

**R1 — 01-file-inventory-target-tree.md — PASS.**
Every provenance-class assignment cites `DESIGN.md`/`boundary-contract.md`/`agent-schemas.md` file:line. The three numeric discrepancies (#1 "11 agents"=adopted-only; #2 "13"=imprecise prose; #3 Phase-0 "6"=core-active-only) are each grounded in verified cites and resolved to the machine-checked manifest as authoritative — the correct call, since Rule F (boundary-contract.md:147) fails on any unmanaged `agents/*.md`, forcing all 11 adopted agents to be vendored. Unverifiable items (adopted `resources/**` per-file list, tier-commentary count, NOTICE file, `.githooks/pre-commit`) are explicitly flagged **Unverified / needs-decision** rather than asserted. No unsupported claims found.

**R2 — 02-native-agents-skills.md — PASS.**
All frontmatter blocks (analyst, safety-verifier, writer) reproduce agent-schemas.md verbatim including the deliberately-preserved duplicate `creative-writing-craft` line. Correctly distinguishes analyst (no `active_tier`) from safety-verifier (receives `active_tier`) — confirmed at agent-schemas.md:63-64 vs 99-100. The story-memory prefix-rewrite note is accurate. Skill-spec cites (adaptation-tiers, adaptation-rules, source-fidelity bodies) are internally consistent with the quoted line ranges; the 5-phase source-fidelity protocol and §3.2 YAML schema are presented as contracts with correct provenance boundaries (R4 owns YAML payload, R2 owns wrapper).

**R3 — 03-buildnew-agents-safety.md — PASS.**
chronicler/tier-coordinator frontmatter verbatim; the sonnet/no-Bash vs opus/has-Bash distinction is real and verified. The full reconcile() A/B/C algorithm and the safety rubric (word-lists, auto-failures, aggregation pseudocode, verdict YAML, branch logic) are verbatim from tier-coordinator.md and safety-rubric.md. R3 proactively surfaces the abbreviated-vs-full verdict variance (agent-schemas.md §2.2 vs safety-rubric.md §4) and correctly designates the §4 form authoritative — a genuine, verified spec nuance, not a fabrication. Ownership boundaries (R4 owns kb formats, R2 owns safety-verifier agent) are stated accurately.

**R4 — 04-kb-layers-portsource.md — PASS (strongest evidence discipline).**
Every port-source claim is grounded in an on-disk read with exact line cites, all of which resolved. The conflict/death key-drift is `[SPEC-CONFIRMED]` with all four tier files' exact lines verified. The "Four vs Five top-level keys" issue is correctly labeled `[SPEC-CONTRADICTED — minor]`: kb-formats.md:147 does literally say "Four" while its own enumeration and the actual file give 5 — R4 caught a real internal spec inconsistency and gave sound builder guidance. Non-uniform bucket fields, tier_4_5 `[preserve]` collapse, and no-tier_4-source are all independently verified. Flag taxonomy ([SPEC-CONFIRMED]/[SPEC-CONTRADICTED]) is applied correctly and honestly.

**R5 — 05-boundary-contract-script.md — PASS.**
The entire rules A–F pseudocode, VENDOR.md format skeleton, 3 modes, helper definitions, prefix-rewrite semantics, and 6-step upstream-sync protocol are verbatim from boundary-contract.md. Execution-time unknowns (exact `upstream_sha`, `vendored_on`, checkout dir path, CI-verify upstream-access model) are explicitly flagged as needs-decision, not invented. The upstream-repo URL (`github.com/haowjy/creative-writing-skills`) matches boundary-contract.md:45 verbatim; R5 labels the WebSearch existence-confirmation as external ("HIGH reliability") while correctly deferring all hashes/SHAs to the spec as source of truth — appropriate epistemic hygiene. The §3.3 note that verify-mode upstream access is spec-underspecified is a correct reading.

**R6 — 06-proof-gate-workflow-template.md — PASS.**
The 11-step workflow table, safety loop, fan-out, and 5 gate conditions all cite DESIGN.md line ranges consistent with DESIGN.md:296 (gate conditions verbatim). The three absence claims — MDTM template not at `.claude/templates/`, no `source/`, no `ch-*.txt` — are all filesystem-verified true, and the resolved pipx template path exists (120 KB). The Tolkien-copyright reconciliation (label work as Tolkien, seed mapping from tolkien_mapping.yaml, provision prose externally/PD) is a well-reasoned, correctly-flagged constraint honoring DESIGN.md:282/296 phrasing without asserting a fabricated fixture. MDTM PART-1 rule cites (A3/A4/B2/C/E2/E3/L1-L6/M3) are into the resolved template file and internally consistent.

### Cross-cutting observations (non-blocking)

- **OBS-1 (MINOR):** R2 (line 19) summarizes adaptation-tiers as carrying "`resources/tier_1..5.md`" and "5 rationale resources," while R1 §B.2 correctly flags the exact commentary-file count as an R2 content decision (`DESIGN.md:122` says only "resources/tier_N.md commentary"). R2's "5 files" is a reasonable inference (one per tier 1/2/3/4/5) but is presented slightly more definitively than the spec strictly licenses. R2 does cite skill-specs.md:80-83 as the sourcing basis. Not a fabrication; a mild over-precision. Builder should treat the tier-commentary count as R2-decided per R1's flag.
- **OBS-2 (MINOR):** R5's VENDOR.md manifest is explicitly a FORMAT skeleton with representative rows ("...all 12 adopted skills"), and R5 correctly defers the authoritative row list to R1 (R5 line 119). R1 in turn treats the 11 fully-enumerated agent rows as authoritative. The two files are consistent; no double-source-of-truth conflict. Noted only to confirm the seam was checked.
- **OBS-3 (informational):** Multiple researchers independently flag the same open decisions (NOTICE file, `.githooks/pre-commit`, exact upstream SHA, verify-mode upstream access). These are consistently labeled needs-decision across R1/R5 — good triangulation, no contradiction.

### Adversarial null-result statement

I actively searched for: (a) frontmatter blocks quoted as "verbatim" that diverge from the spec — none found; (b) line cites that fail to resolve — none found among 25 directed checks; (c) assertions stated as fact that the spec does not support — none found (R4's two spec-contradiction flags are correct catches of the *spec's* internal inconsistency, not research errors); (d) missing/mis-applied `[UNVERIFIED]`/`[SPEC-CONTRADICTED]` tags — flagging discipline is consistent and correct. The only findings are two MINOR over-precision notes (OBS-1) and confirmatory seam checks (OBS-2/3). No CRITICAL or IMPORTANT evidence-quality defect exists.

---

## VERDICT: PASS

Evidence quality across all six assigned research files is high. Every directed spot-check (R2/R3 frontmatter vs agent-schemas.md; R4 tier key-drift vs actual YAML; R5 rules A–F vs boundary-contract.md §3.2; R6 MDTM path existence; R1 manifest reconciliation vs boundary-contract.md §2) passed against ground truth. Claims are consistently backed by resolvable spec `file:line` cites or on-disk port-source content; unverifiable items and genuine spec contradictions are correctly and honestly flagged rather than papered over.

**Severity-rated issues:** None at CRITICAL or IMPORTANT. Two MINOR items only:
- **MINOR (OBS-1):** R2's "5 tier-commentary resources" is a mild over-precision vs the spec's non-committal "resources/tier_N.md commentary"; builder should honor R1's flag that the count is an R2 content decision.
- **MINOR (OBS-2):** VENDOR.md manifest row-list ownership is split R5(format)/R1(rows) by design; confirmed consistent, noted for builder awareness.

Neither MINOR item blocks the builder or reduces the fidelity of the extracted specs. The research package is evidence-sound and ready for task-building.
