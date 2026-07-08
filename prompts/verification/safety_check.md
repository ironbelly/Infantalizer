# Safety Verification Prompt
## Post-Generation Check for Tier 1-2 Adaptations

## Purpose

Verify adapted content meets safety requirements for young children (ages 3-8).

**Run on ALL Tier 1 and Tier 2 outputs before delivery.**

## Section 1: Forbidden Content Scan

**TIER 1 FORBIDDEN:**
```
kill, killed, slay, slew, murder, wound, blood, gore, 
stab, attack, fight, sword, weapon, die, died, dead, death
```

**TIER 2 FORBIDDEN:**
```
kill, killed, murder, slay, slew, blood, gore, torture, 
stab, die, died (can use "passed away", "lost")
```

| Word Found | Location | PASS/FAIL |
|------------|----------|-----------|

## Section 2: Agency Externalization Check

Negative outcomes = external states or accidents, NEVER innate character qualities.

| Character/Event | Cause Given | External? | PASS/FAIL |
|-----------------|-------------|-----------|-----------|

**Violations:** "He was evil" ❌ | "Driven by greed" ❌ | "She betrayed them" ❌

## Section 3: Emotional Safety

**Permitted:**
- Tier 1: happy, sad, scared, grumpy, tired, excited, brave, kind
- Tier 2: + worried, lonely, embarrassed, proud, frustrated

| Negative Emotion | Resolved? | How? |
|------------------|-----------|------|

**Chapter Ending:**
- [ ] Positive emotional state
- [ ] Sense of safety
- [ ] Problem resolved

## Section 4: Safe Home Schema

- [ ] Home presented as safe haven
- [ ] If threatened, restored
- [ ] No permanent destruction
- [ ] Family relationships positive

## Section 5: Nightmare Prevention

- [ ] Monsters are grumpy/silly, not terrifying
- [ ] Darkness is temporary and fixable
- [ ] Fear is manageable

## Section 6: Linguistic Compliance

**Tier 1:** Max 12 words per sentence

| Sentence | Word Count | PASS/FAIL |
|----------|------------|-----------|

- [ ] No passive voice
- [ ] No complex clauses
- [ ] Kindergarten vocabulary

## Verification Summary

| Section | Result |
|---------|--------|
| Forbidden Content | PASS / FAIL |
| Agency Externalization | PASS / FAIL |
| Emotional Safety | PASS / FAIL |
| Safe Home Schema | PASS / FAIL |
| Nightmare Prevention | PASS / FAIL |
| Linguistic Compliance | PASS / FAIL |

**Final:** [ ] APPROVED  [ ] REVISION REQUIRED

## Automatic Failures

**Tier 1:** Death language, violence, "evil", unresolved fear, internal motivation
**Tier 2:** Graphic violence, "kill/murder/slay", prolonged hopelessness
