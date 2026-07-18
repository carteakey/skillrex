---
name: deal-finder
description: Scrapes and summarizes the top deals from rfd.davegallant.ca.
---

# Deal Finder Skill

This skill automates the process of checking `rfd.davegallant.ca` for the latest and hottest deals, categorizing them for easy reading.

## Trigger Conditions
- User asks to "check deals", "find deals", or "check rfd.davegallant.ca".
- User mentions "rfd".

## Procedure

1. **Navigate to the Site:**
   Use `browser_navigate` to go to `https://rfd.davegallant.ca`.

2. **Capture Page Content:**
   Use `browser_snapshot` to get the current list of deals.

3. **Parse and Categorize:**
   Analyze the snapshot to extract:
   - **Deal Title:** The text within the link.
   - **Category:** Group items into logical buckets like:
     - 🔥 **Hot Deals & Freebies** (Free items, highly discounted)
     - 💰 **Great Savings** (General discounts)
     - 🍔 **Food & Dining** (Restaurants, groceries)
     - 📱 **Tech & Electronics** (Gadgets, mobile plans, internet)
     - 🛍️ **Retail & Lifestyle** (Clothing, home goods)
   - **Key Details:** Any mentioned prices, expiry dates, or specific brands.

4. **Format Output:**
   Present the results in a clean, structured Markdown format with emojis for readability.

## Pitfalls
- **Bot Detection:** The site may implement aggressive bot detection. If navigation fails or returns an error, notify the user.
- **Dynamic Content:** If the page appears empty, try a `browser_scroll` or a slight delay before taking the snapshot.
- **Truncated Snapshots:** If the list is extremely long, ensure all relevant categories are captured by reviewing the snapshot carefully.

## Verification
- Ensure the summary includes a mix of categories and clearly highlights "Free" items.
- Verify that links (if extracted) are presented or mentioned as available.