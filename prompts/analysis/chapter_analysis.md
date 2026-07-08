# Chapter Analysis Prompt
## Source Analysis with v2.0 Anti-Hallucination Protocol

## Phase 0: Source Declaration

```
SOURCE ACCESS LEVEL: [Select one]
□ FULL ACCESS - Complete text available
□ PARTIAL ACCESS - Excerpts or summaries
□ MEMORY-BASED - Working from recall
□ NO ACCESS - Cannot proceed

⚠️ If MEMORY-BASED: All output requires UNCERTAIN tags
❌ If NO ACCESS: ABORT
```

## Phase 1: Essential Verification

| Field | Value | Confidence |
|-------|-------|------------|
| Work Title | | |
| Chapter Number | | |
| Chapter Title | | |

**Opening Sentence:** `"[quote]"` Confidence: [CERTAIN/PROBABLE/UNCERTAIN]

**Closing Sentence:** `"[quote]"` Confidence: [CERTAIN/PROBABLE/UNCERTAIN]

## Phase 2: Dual-Pass Documentation

### PASS ONE: Structure and Events

**Major Characters:**
| Character | Role | Confidence |
|-----------|------|------------|

**Sequential Events (5-10):**
| # | Event | Confidence |
|---|-------|------------|

### PASS TWO: Summary

**Chapter Summary (100-150 words):**
Confidence: [CERTAIN/PROBABLE/UNCERTAIN]

## Phase 3: Transformation Flags

| Category | Instances | Severity |
|----------|-----------|----------|
| Violence | | |
| Death | | |
| Emotional | | |
| Abstract | | |

## Phase 4: Consistency Check

- [ ] Characters appear logically
- [ ] Timeline makes sense
- [ ] Locations possible

## Output Format

```yaml
metadata:
  chapter: "[number] - [title]"
  source_access: "[FULL/PARTIAL/MEMORY]"
  confidence: "[HIGH/MEDIUM/LOW]"

transformation_flags:
  violence_transform: [true/false]
  death_transform: [true/false]
  agency_externalization: [true/false]

uncertainties:
  - "[List UNCERTAIN elements]"
```

## Confidence Tags

| Tag | Definition |
|-----|------------|
| **CERTAIN** | Directly quoted from text |
| **PROBABLE** | Multiple observations support |
| **UNCERTAIN** | Inferred or reconstructed |

**Principle:** Transparent uncertainty > false certainty
