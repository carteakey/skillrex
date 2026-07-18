# Eventbrite Browser Scraping Fallback

When Firecrawl and `web_extract` fail or are unavailable, Eventbrite can be scraped via the browser toolchain.

## URL
`https://www.eventbrite.ca/d/canada--toronto/events--this-weekend/`

(Note: `.ca` works in browser; the skill's Firecrawl URL uses `.com` — both resolve to the same content.)

## Procedure

1. **Navigate**: `browser_navigate(url)` — loads the filtered "This Weekend" page
2. **Scroll**: `browser_scroll('down')` — ensures event cards are rendered in the DOM
3. **Extract**: `browser_console(expression=...)` with JS:
   ```javascript
   Array.from(document.querySelectorAll(
     '[data-testid="event-card"],.event-card,.eds-event-card,.event-listing'
   )).slice(0, 20).map(el => el.innerText).join('\n---\n')
   ```
4. **Parse**: Output is semi-structured text blocks. Key fields per event:
   - Urgency badge: "Sales end soon", "Going fast", "Almost full"
   - Event name (appears twice per card — desktop + mobile view)
   - Date/time: "Tomorrow at 10:00 AM", "Sunday at 12:00 PM"
   - Venue: "Toronto · Venue Name" (split on `·`)
   - Price: "From $37.00", "From $0.00" (= free)
   - Organizer + follower count

## Key Notes

- Each event card renders **twice** in the DOM (responsive layout). Dedup by event name.
- The page has left-sidebar filters (Category, Date, Neighborhood, Price, Format, Language, Currency). The "This weekend" radio is pre-selected.
- For more events, scroll further before extracting, or increment the `.slice()` range.
- This is a **fallback** — Firecrawl (`/v1/scrape`) is preferred when available for structured markdown parsing.
- Google search (`google.com/search?q=...`) also triggers bot detection — don't use as an intermediary.
