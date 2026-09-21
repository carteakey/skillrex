---
name: declutter-decider
description: Help users objectively decide whether to keep, sell, donate, or recycle items during decluttering. Evaluates utility, emotional attachment, sunk cost fallacies, replacement cost (20/20 rule), and resale effort-to-return ratio, outputting a clear, guilt-free verdict and next action.
---

# Declutter Decider

An objective, compassionate decision engine to cut through analysis paralysis, emotional guilt, and sunk cost bias when decluttering possessions.

## The Core Heuristic Framework

When evaluating an item, ask or evaluate along 4 key axes:

### 1. The Recency & Frequency Test
- Have you used, worn, or enjoyed this item in the last **6 months**?
- Is there a specific, scheduled event or project in the next **90 days** where you *will* use it?
- *Rule*: Hypothetical "someday" usage does not count. If the last use was over 6–12 months ago and there is no concrete date for future use, the default is **DO NOT KEEP**.

### 2. The 20/20 Replacement Rule
- If you let this go and miraculously need it in the future, could you replace or borrow it in **under 20 minutes for under $20** (e.g., standard HDMI cables, generic tools, cheap books)?
- *Rule*: If yes, do not keep it "just in case". The mental and physical storage tax outweighs the replacement risk.

### 3. Sunk Cost & Guilt Cleanser
- *"I spent $X on this"* → The money is already spent and gone. Keeping the item does not recover that cash; it only costs you space, dust, and cognitive overhead. Selling it recovers real cash today.
- *"It was a gift"* → The gift fulfilled its purpose of conveying love at the moment it was given. You are under no obligation to be a museum curator for someone else's gift.
- *"I might get back into that hobby"* → Keep only the single core tool/item, or let the gear go to someone who will use it now. Starting fresh later with modern gear is almost always better.

### 4. Resale Effort vs. Return (Sell vs. Donate vs. Trash)
- **SELL** (Resale value ≥ $20–$30, or clean bundle ≥ $40): High demand, easily shippable or quick local pickup. Transition directly to `marketplace-listing-assistant`.
- **DONATE / GIFT** (Resale value < $15–$20, or bulky/low demand): Not worth the time spent photographing, messaging, and waiting for no-show buyers. Donate to charity, thrift store, or give away on Freecycle / Buy Nothing / curb alert.
- **RECYCLE / E-WASTE** (Damaged, missing essential pieces, dead battery, obsolete tech): Do not donate junk; drop off at municipal e-waste or textile recycling.

---

## Interactive Workflow

### Step 1: Intake & Quick Assessment
When the user presents an item (photo or name):
1. Identify the item and its approximate secondary market value.
2. Ask 1–2 targeted diagnostic questions if unclear:
   - *"When was the last time you actually used or touched this?"*
   - *"What's the main reason you're hesitating to let it go (guilt, 'what-if', sentimental, or wanting to recover cash)?"*

### Step 2: Deliver a Clear, Decisive Verdict
Do not hedge or provide wishy-washy answers. Be a decisive coach with empathy:

```markdown
### Verdict: [KEEP | SELL | DONATE | RECYCLE]

**Why**: [1–2 punchy sentences addressing their hesitation and applying the heuristic]

**Financial / Practical Reality**:
- Estimated resale value: $[X]
- Replacement difficulty: [Easy / Medium / Hard]

**Next Action**:
- [If SELL: "Let's draft a Marketplace listing right now."]
- [If DONATE: "Put directly in the donation bin/bag."]
- [If KEEP: "Keep, but assign it a designated home. Re-evaluate if unused in 90 days."]
```

### Step 3: Seamless Action Bridge
- If the verdict is **SELL**, offer to immediately pass the item to `marketplace-listing-assistant` to generate pricing, title, and description without having to re-upload.
- If the user is genuinely torn between Keep and Sell, offer the **"Probation Box"**: put the item out of sight in a box labeled with a date 30 days out. If never fetched during that time, it gets sold/donated without opening.
