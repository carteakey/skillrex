# Pricing Strategy & Comps Analysis

How to calculate optimal, fast-turnaround listing prices using local market comparables.

---

## 1. Comps Discovery Workflow

### Using the `facebook-marketplace` MCP
If available, invoke `search_listings`:
- `query`: Exact brand and model (e.g., `M1 MacBook Air 8GB`, `Sony WH-1000XM4`).
- `latitude` / `longitude`: Coordinates of the seller's area.
- `radius_km`: 25–40 km (the typical radius a local buyer will travel).
- `min_price`: Set a sensible minimum (e.g., $30) to filter out $1 or "Free" spam listings.

### Web Search Fallback
If the MCP tool is unavailable or hits rate limits:
- Search Google for: `site:facebook.com/marketplace "[city]" "[item name]"` or Kijiji / Craigslist listings.
- Check eBay "Sold Items" (refurbished/pre-owned) and subtract 10–15% to adjust for platform fees and shipping.

---

## 2. Filtering Noise from Raw Comps

Discard outliers before computing prices:
1. **Ignore spam prices**: $1, $1,234, or $99,999 placeholders.
2. **Ignore "For Parts / Not Working"**: Unless the user's item is also non-functional.
3. **Ignore "Willing to Ship" drop-shippers**: Filter for local, verified peer-to-peer sellers.
4. **Account for condition gaps**: A sealed, brand-new unit commands 20–30% more than a good-condition used unit.

---

## 3. The 10–20% Fast-Sale Formula

Marketplace buyers are deal-hunters. An item priced at average market value can sit for weeks with tire-kickers. Pricing **10% to 20% below active median** creates urgency and attracts immediate, serious buyers.

```text
1. Active Median Price (Comparable Condition) = $[M]
2. Fair Market Value (FMV) = $[M]
3. Fast-Sale Price (15% below FMV) = $[M * 0.85], rounded to nearest $5 or $10
```

### Psychological Rounding Rules
- **Under $100**: Round to the nearest $5 (e.g., $35, $45, $65, $85).
- **$100 to $500**: Round to the nearest $10 or $20 (e.g., $140, $180, $220, $350).
- **Over $500**: Round to the nearest $25 or $50 (e.g., $550, $675, $850).
- Avoid odd prices like $187, $93, or $312 — they look like automated dealer or pawnshop algorithms.

---

## 4. Presenting the Strategy to the Seller

Always provide two clear listing options:

| Strategy | List Price | Stated Terms | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **Option A: Fast Sale (Recommended)** | 15–20% below median | *"Priced to sell quickly. Price is firm."* | Sells within 24–72 hours; filters out hagglers. |
| **Option B: Haggle Buffer** | At or 5% below median | Open to reasonable offers | Buyer negotiates down to your target floor. |

---

## 5. Quick Depreciation Reference (Rule of Thumb)

When active comps are scarce, use standard secondary market depreciation from current retail:
- **Current Gen Apple / Flagship Tech**: 75–85% of retail if Like New.
- **Previous Gen Tech / Consoles**: 50–65% of original retail.
- **Older Tech (3+ years)**: 30–45% of original retail.
- **Solid Wood / Brand Furniture (e.g. West Elm, Article)**: 40–50% of retail.
- **IKEA / Flat-Pack Furniture**: 25–40% of retail (assembly value rarely carries over).
