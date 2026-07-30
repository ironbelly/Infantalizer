# M4 Source-Fidelity Report — agent 1 (spec §1–§8)

**Date:** 2026-07-09 · fix_authorization: false (read-only) · **Overall Verdict: PASS**

Every requirement in §1–§8 has faithful, semantically-complete representation in the assembled output. No missing coverage; no phantom/fabricated coverage.

| Spec | Requirement | Result | Output evidence |
|------|-------------|--------|-----------------|
| §1 | Stage 0 Mode A/B/C → canonical ch-<NN>.txt + confidence-tagged manifest; no new command/script/runtime; frozen read-set; ambiguity→gate; no non-CERTAIN pre-confirm write | PASS | SKILL.md principle/non-runtime + gated commit; path-contract §4 note; prep-cordinator STAGE 0 |
| §2 G1-G5 | one-run materialize; first-class manifest w/ provenance; preserve 8-file pkg + 3-file read-set + one script; route non-CERTAIN; adopt narnia/tolkien zero re-split | PASS | SKILL.md adopt/sidecar/sole-script; prep SKILL §1 note (8 files unchanged) |
| §2 N1-N4 | no per-chapter fidelity in prep; no new command/2nd script; no 4th read/9th file; analyst not splitter | PASS | SKILL.md "analyst is NOT the splitter"; command adds only a flag |
| §3 | `--source` dir/file/adopt/URL; `--source-mode` NEW default auto; argument-hint | PASS | command file; prep-cordinator Inputs source_mode |
| §3 precedence | adopt>folder>file>ambiguity HALT incl. split+monolith both-present HALT; PROBABLE/UNCERTAIN blocks write | PASS | SKILL.md Stage 0.2 rules 1-4 + both-present negative guard |
| §4 0.1-0.5 | inventory+ABORT-on-NO-ACCESS; detect mode; plan NO writes; gated commit; route to §5; CONFIRMED on greenlight | PASS | SKILL.md Stage 0.1-0.5; prep-cordinator STAGE 0 + notes |
| §5 manifest schema | every field | PASS | SKILL.md manifest block — `diff` vs spec §5 **byte-identical** |
| §6 five evidence layers | TOC / body-heading / filename natural-sort / content-sanity / count-reconciliation | PASS | SKILL.md 5-layer table; boundary-rules.yaml 5 keys |
| §6 confidence rule | CERTAIN ≥2 signals + no contradiction; single-signal→PROBABLE; UNCERTAIN triggers | PASS | SKILL.md verbatim rule; boundary-rules.yaml mirror (SKILL authoritative) |
| §7 16 failure rows | all 16 | PASS | SKILL.md failure table — `diff` vs spec §7 **16 rows byte-identical** |
| §8 normalization | HTML/PDF handling; UTF-8; no reword/reflow; `.raw/` retention; normalization_event + source_fidelity_risk; high-risk-loss blocks greenlight | PASS | SKILL.md normalization section; source/README `.raw/` |

**Confidence:** 10/10 verified, 100%. **Issues:** 0 missing, 0 phantom.

Benign notes (not findings): boundary-rules.yaml char thresholds (500/1500/120000) are a faithful operationalization of §6.4's abstract "non-empty body / plausible length" (not a spec contradiction); AC1 "identical" scope clarification (chapter TEXT identical, manifest provenance mode-specific) is a correct non-contradicting refinement (defer confirm to the §13 agent).
