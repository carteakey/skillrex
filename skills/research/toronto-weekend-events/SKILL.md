---
name: toronto-weekend-events
description: Aggregate Toronto events from multiple sources (blogTO, Eventbrite, Meetup, r/toronto, Narcity) into a categorized digest. Covers weekend events, career/professional Meetup monitoring, and delta-based change detection. Designed for cron delivery.
---

# Toronto Weekend Events Digest

Scrape, deduplicate, and curate weekend events/activities in Toronto from multiple sources into a categorized Telegram-friendly digest.

## Historical Schedule

The old automation ran daily at 19:00 and delivered to Telegram. Recreate scheduling outside this skill using cron, systemd timers, GitHub Actions, or the active agent's scheduler. If total event quality is too low, return exactly `[SILENT]`.

## Source Priority & Access Methods

### 🥇 Primary — blogTO (most structured, reliable)

**Two-step: RSS for URL → Firecrawl for content**
1. **RSS Feed** to find the article URL:
   - URL: `https://www.blogto.com/rss/articles.xml`
   - Filter: items where `<title>` contains "things to do" (case-insensitive)
   - Extract the `<link>` URL — this is the weekly radar article
   - ⚠️ The RSS `<description>` field does NOT contain clean structured event data — it has messy HTML with formatting artifacts. **You MUST scrape the full article via Firecrawl.**

2. **Firecrawl scrape** the article URL (`/v1/scrape` with `formats: ["markdown"]`, `onlyMainContent: true`):
   - Returns clean markdown with structured event blocks
   - **Category headers**: `- ##### Category Name` (e.g., `- ##### Art events`, `- ##### Comedy`, `- ##### Concerts`, `- ##### Sport events`, `- ##### Free events you don't want to miss`)
   - ⚠️ Skip `- #### Live your best life with blogTO's Top Events newsletter` — this is a promo, not a category
   - **Event pattern** (each event spans ~60-80 lines with many empty lines):
     - Line A: `- [Event Name](https://www.blogto.com/events/...)` ← initial link
     - ~5-10 empty lines
     - Date: `April 23` or `February 19 - April 30`
     - ~5-10 empty lines + `Add to my Events`
     - Line B: `[Event Name](same url)` ← repeated link
     - Description text (1-2 sentences)
     - ~5-8 empty lines
     - Location: `Scotiabank Arena`, `OCAD University`, etc.
     - ~5 empty lines + `Add to my Events`
   - **Phase-based parsing** (see Implementation Notes below): `date → repeat_link → desc → location`
   - Scan range: up to **80 lines** forward per event block (not 40!)

**Events Calendar (browser — for day-specific picks, optional)**
- URL: `https://www.blogto.com/events/`
- Click on Friday/Saturday/Sunday dates to get day-by-day listings

### 🥈 Secondary — To Do Canada (Firecrawl — reliable with correct parsing)

- URL: `https://www.todocanada.ca/things-to-do-in-toronto-this-weekend/`
- Access: **Firecrawl scrape** (`/v1/scrape` with `formats: ["markdown"]`, `onlyMainContent: true`)
- ⚠️ **Key parsing pattern** — events follow this exact format:
 - Category headers: `## **I. Live Music**`, `## **II. Theatre**`, etc. — match with `re.match(r'^#{1,3}\s+\*?\*?(?:[IVX]+\.?\s+)?(.+?)(?:\*\*)?\s*$', line)`
 - Event items: `- [Event Name](url) on Day, Month XX | HH:MM PM @ Venue` — single-line format!
 - Regex: `re.match(r'^-\s+\[(.+?)\]\([^)]+\)\s+on\s+(.+?)\s*\|\s*(.+?)\s*@\s*(.+)', line)`
 - This yields **~17 events per run** reliably (concerts, theatre, sports, festivals)
 - Sections I-IV have concrete events; Section V ("Things to do") is evergreen links — skip it
- Also has monthly overview: `https://www.todocanada.ca/toronto-april-events-festivals/`

### 🥈 Secondary — Eventbrite

- URL: `https://www.eventbrite.com/d/canada--toronto/events--this-weekend/` (note: `.com` not `.ca` for initial URL, but links in content use `.ca`)
- Access: **Firecrawl scrape** (direct scrape, NOT search — `/v1/search` returns URLs only with no markdown content)
- ⚠️ **Key parsing pattern** — Firecrawl markdown has a specific structure:
 - Skip `![image]` lines: `- [![...primary image](url)]` — these are image thumbnails, NOT events
 - Real event lines: `[**EVENT NAME**](https://www.eventbrite.ca/e/...)` — match with strict regex `re.match(r'^\[?\*\*(.+?)\*\*\]?\(https://www\.eventbrite\.ca/e/', line)`
 - Also try plain format: `[Event Name](https://www.eventbrite.ca/e/...)` as fallback
 - Date on next non-empty line: `Friday at 10:30 PM` or `Sun, Apr 26, 7:00 PM`
 - Venue pattern: `Toronto · Venue Name` — split on ` · ` and take last part
 - Price line (`From CA$`/`Free`) = past event info, stop scanning
 - Events appear **twice** in the page (promoted + organic) — dedup handles this
 - **Clean escaped pipes**: Eventbrite markdown has `\\|` in names — strip with `re.sub(r'\s*\\\\?\|.*$', '', name)`
- Yields **~6 events per run** with dates and venues
- Good for smaller/indie events not covered by blogTO/To Do Canada

### 🥈 Secondary — r/toronto — Community Picks (✅ CONFIRMED WORKING)

**Reddit RSS endpoint works reliably.** The following DO NOT work:
- `reddit.com/r/toronto/search.json` — blocked (403/429)
- `old.reddit.com` — blocked
- `curl` with any User-Agent on HTML — blocked
- DuckDuckGo search for Reddit URLs — CAPTCHA
- **Firecrawl `/v1/scrape` on reddit.com** — explicitly blocked ("We do not support this site")

**✅ This DOES work — Reddit RSS search:**
```
curl -s -L -H "User-Agent: Mozilla/5.0 (compatible; TorontoDigest/1.0)" \
 "https://www.reddit.com/r/toronto/search.rss?q=things+to+do+in+toronto+week&restrict_sr=on&sort=new&t=week&limit=3"
```
- Returns Atom XML with `<entry>` elements containing title, link, author, and HTML content
- Parse with `xml.etree.ElementTree` using namespace `{'atom': 'http://www.w3.org/2005/Atom'}`
- **Important**: The auto-mod weekly thread title format is `"Things to do in Toronto - Week of [Date], [Year]"` — NOT "What are you doing this weekend"
- Search queries to try (in order): `things+to+do+in+toronto+week`, `what+are+you+doing+this+weekend+toronto`
- The thread itself is a stub — the value is in the **comments** where users post events. The RSS entry gives you the thread URL to check.
- **Do NOT use Firecrawl for Reddit** — use the RSS endpoint directly via `curl`

### 🥉 Tertiary — Narcity
- ⚠️ **Narcity's "things to do this weekend" URL (`/toronto/things-to-do-this-weekend`) is a 404**. The old article format at `/toronto/things-to-do/` may also be unreliable.
- Try searching Narcity homepage for weekend-specific articles instead
- Less structured than blogTO — more listicle style
- Often has seasonal roundups and "bucket list" content

### 🥉 Tertiary — Toronto.ca Events (browser-accessible, good for city festivals)
- URL: `https://www.toronto.ca/explore-enjoy/festivals-events/`
- Access: **Browser navigation** (Firecrawl may also work; browser is confirmed reliable)
- Best for **city-run signature events** — Indigenous Peoples Month, Pride Month, Indigenous Arts Festival, Summerlicious, Canada Day, Doors Open, Nuit Blanche, Cavalcade of Lights, etc.
- Also has a **Festivals & Events Calendar** at `https://www.toronto.ca/explore-enjoy/festivals-events/festivals-events-calendar/`
- Not for day-by-day event listings — use for anchoring "ongoing city events" in the digest

### Skip These
- Instagram/TikTok tags — unreliable to scrape
- Firecrawl on Reddit — explicitly blocked by Firecrawl ("We do not support this site"). Use RSS endpoint instead.
- **ToDo Canada via browser** — Cloudflare bot detection blocks automated browser access (returns "Performing security verification" challenge page). Only Firecrawl works for this source.

## Deduplication Strategy

1. Normalize event names: lowercase, strip punctuation but **preserve spaces**, trim whitespace, keep 50 chars
2. Key regex: `re.sub(r'[^a-z0-9 ]', '', name.lower()).strip()[:50]` — preserves word boundaries for better matching
3. Compare across sources — same event from blogTO + Eventbrite = merge, keep richer description
4. Tag each event with its source(s): `[blogTO]`, `[Eventbrite]`, `[r/toronto]`
5. For delta detection: compare against previous run's event list (store in session or file)

## Output Format (Telegram)

```
🗓️ Toronto Weekend Digest — [Month Day-Day]

🔥 Top Picks
• Event Name — Date, Venue [source] [Free!]

🎨 Art & Culture
• ...

🎵 Music
• ...

😂 Comedy
• ...

🍔 Food & Drink
• ...

🌳 Free & Outdoors
• ...

💬 Community Picks (r/toronto)
• ...

📚 Full listings: [blogTO](url) | [Eventbrite](url) | [Now Toronto](url)
```

### Categories
- **🔥 Top Picks**: 2-3 most notable/popular events across all categories
- **🎨 Art & Culture**: Galleries, exhibitions, theater, film
- **🎵 Music**: Concerts, DJ sets, open mics
- **😂 Comedy**: Stand-up, improv, comedy shows
- **🍔 Food & Drink**: Food festivals, pop-ups, tastings
- **🌳 Free & Outdoors**: Parks, walks, free community events
- **💬 Community Picks**: Recommendations from r/toronto thread (if available)

## Implementation Notes

- **blogTO is the backbone** — RSS finds the article URL, Firecrawl extracts structured markdown. This two-step is critical; RSS alone is insufficient.
- **Phase-based blogTO parsing** (most important implementation detail):
 - When parsing Firecrawl markdown for blogTO events, use a state machine with phases: `date → repeat_link → desc → location`
 - Each event block spans **up to 80 lines** (lots of empty lines between sections). Scan forward 80 lines, not 40.
 - Skip "Add to my Events" lines and empty lines in the scan
 - Category headers use format `- ##### Category Name` — but skip `#### Live your best life...` (newsletter promo)
 - Event links match: `^-\s+\[(.+?)\]\((https://www\.blogto\.com/events/[^)]+)\)`
 - The same event link appears twice in the markdown (once as list item, once as standalone link) — use the second occurrence to delineate where the description starts
 - **"Add to my Events"** is the reliable delimiter between sections — after seeing it, the next non-empty content is the next section (repeat link, or next event)
- **To Do Canada** — with correct regex (`on ... | ... @ Venue`), reliably yields **~17 events** per run. Key: events are single-line format, not multi-line like blogTO.
- **Eventbrite** — use direct Firecrawl `/v1/scrape` (NOT `/v1/search` which returns URLs only). Watch for `![image]` artifacts and escaped `\\|` in names. Events appear twice in page (promoted + organic). When Firecrawl is unavailable, fall back to browser scraping (see `references/eventbrite-browser-scraping.md`).
- Browser-based sources (blogTO calendar, Narcity) should be scraped **after** Firecrawl sources to fill gaps
- Keep the total digest under ~4000 chars for Telegram readability
- Prioritize events happening Fri-Sun; if run Mon-Thu, focus on the upcoming weekend
- If an event appears in multiple sources, prefer blogTO's description (usually more detailed)

## Cron Job Details

- **Script**: `~/.agent/scripts/toronto-weekend-digest.py` (referenced as `toronto-weekend-digest.py` in cron config)
- **Job ID**: `7d667ab16d75`
- **Schedule**: `0 19 * * *` (7:00 PM ET daily)
- **Delivery**: Telegram (origin)
- **Silent-if-no-results**: If total_events is 0 or only 1-2 low-quality events, respond `[SILENT]`
- **First run**: Always delivers full digest regardless

## Pitfalls

- **Reddit access**: Use ONLY the RSS search endpoint (`search.rss?q=...&restrict_sr=on`). JSON API, HTML scraping, and Firecrawl are ALL blocked. The RSS endpoint is the one reliable method.
- **Firecrawl blocks Reddit**: `POST /v1/scrape` with any `reddit.com` URL returns `{"success": false, "error": "We do not support this site"}`. This is an explicit Firecrawl policy, not a transient error.
- **blogTO RSS description is NOT sufficient**: The RSS `<description>` field has messy HTML with formatting artifacts — you CANNOT reliably parse events from it. You MUST Firecrawl-scrape the full article URL found in the RSS `<link>`.
- **To Do Canada event format**: Events are single-line `- [Name](url) on Day, Month XX | HH:MM PM @ Venue`. The `on ... | ... @` pattern is the key to reliable parsing — don't try to parse multi-line blocks like blogTO.
- **blogTO location field is often empty**: Some events (especially Comedy events) don't have a venue listed in the article — the location field will be empty. This is a data quality issue, not a parsing bug.
- **Date parsing**: blogTO uses formats like "April 23" or "February 19 - April 30". To Do Canada uses "Thursday, April 23, 08:00 PM". Eventbrite uses "Friday at 10:30 PM" or "Sun, Apr 26, 7:00 PM". Parse carefully per source.
- **Eventbrite image artifacts**: Firecrawl markdown from Eventbrite contains `[![Event Name primary image](img_url)]` lines — these are NOT event links. Filter them by checking for `![` prefix. The real event link is `[**EVENT NAME**](eventbrite.ca/e/...)` on the next non-empty line.
- **Eventbrite escaped pipes**: Names contain `\\|` (escaped pipe) in Firecrawl output — clean with `re.sub(r'\s*\\\\?\\|.*$', '', name)` before using.
- **Eventbrite duplicate blocks**: Each event appears ~2x in the page (promoted section + organic listing). Dedup normalization handles this.
- **Eventbrite browser fallback**: When Firecrawl/web_extract fail, Eventbrite is browser-scrapeable at `.ca` URL (`https://www.eventbrite.ca/d/canada--toronto/events--this-weekend/`). Use `browser_console` JS extraction:
  ```javascript
  Array.from(document.querySelectorAll('[data-testid="event-card"],.event-card,.eds-event-card,.event-listing')).slice(0,20).map(el => el.innerText).join('\n---\n')
  ```
  - Output is semi-structured text with event name, date/time, venue (`Toronto · Venue Name`), and price
  - The `.ca` domain works in browser (skill's Firecrawl URL uses `.com` — both resolve to the same content)
  - Scroll down first (`browser_scroll('down')`) to load event cards into the DOM before extracting
  - Each event card appears twice in the DOM (desktop + mobile views) — dedup by event name
- **Dedup normalization**: Use `re.sub(r'[^a-z0-9 ]', '', name.lower()).strip()[:50]` — **preserving spaces** is critical for matching cross-source variants like "Dave: The Boy Who Played the Harp Tour 2026" (blogTO) vs "DAVE – The Boy Who Played the Harp Tour" (To Do Canada).
- **ToDo Canada Cloudflare block**: Browser access to `todocanada.ca` triggers Cloudflare bot detection ("Performing security verification" page). Only `web_extract`/Firecrawl can reliably access it — if the Firecrawl key is configured. Browser-based scraping of this source will fail.
- **Narcity weekend URL is dead**: The URL `https://www.narcity.com/toronto/things-to-do-this-weekend/` returns a 404. Search the Narcity homepage for weekend articles instead of using a direct URL.
- **Web search rate limits**: The `web_search` tool can hit 429 (Too Many Requests) during peak usage. When this happens, fall back to direct browser navigation to event source sites (Eventbrite, toronto.ca, blogTO) and extract data via `browser_console` JS.
- **`web_extract`/Firecrawl are unreliable**: Both `web_extract` and Firecrawl `/v1/scrape` can fail intermittently (429, connection errors, or bot detection). The Eventbrite browser fallback (`references/eventbrite-browser-scraping.md`) is the most reliable path when these tools are down.
- **Google Search bot detection**: Direct `browser_navigate` to `google.com/search?q=...` triggers Google's CAPTCHA/bot detection ("unusual traffic" page). Do NOT use Google as an intermediary to find event pages — navigate directly to known event source URLs instead.
- **Fallback chain when primary tools fail**: If `web_search` → 429 AND `web_extract`/Firecrawl → error, use this order:
  1. **Eventbrite browser** — navigate to `.ca` URL, scroll, JS extract (most reliable fallback)
  2. **toronto.ca browser** — city-run signature events (good for anchoring ongoing festivals)
  3. **Reddit RSS** — `curl` to `search.rss?q=things+to+do+in+toronto+week` (always works, no browser needed)
  4. **BlogTO RSS + browser** — navigate to blogTO events calendar if Firecrawl is down
  5. **Skip** ToDo Canada (Cloudflare), Narcity (404), and Google (bot detection) in fallback mode

## Meetup Career Event Monitoring

For career-focused event discovery on Meetup.com in Toronto (e.g., Healthcare/Nursing, Tech/Networking, Entrepreneurship):

### Search Strategy
Run **3–5 searches**, mixing combined keywords with category browsing:

**Combined keyword searches (faster — fewer page loads):**
1. **`Nursing+Healthcare`** — Combines both terms; filters out more noise than running them separately. Still yields wellness/meditation events but also surfaces health-coaching and boundary-building events.
2. **`Tech+Networking+Entrepreneurship`** — Best single search for the tech/startup ecosystem. Yields Startup Valley, founder mixers, business networking.
3. **`Nursing+Transition+Career`** — Best for career-change-specific events (career pathway workshops, tech-career-transition webinars, Le Wagon events). ⭐ HIGH VALUE for career transition focus.

**Single-keyword fallback (if combined searches miss something):**
4. **`Healthcare`** — Still best for HealthTech, pharma networking, AI+Health crossover events.
5. **`Startup`** — Fallback if `Entrepreneurship` yields social-entrepreneurship category with zero events.

**Category browse (bypasses keyword search entirely — finds events keyword searches miss):**
6. **Technology category** — URL: `https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS&category=technology`
   - Surfaces Google Developer Group, Azure/AWS community, Java User Group, and other platform-specific events that don't always match "Tech Networking" keywords
   - ⚠️ Cookie consent dialog blocks content on category pages — dismiss it first by clicking the "Close" button on the popup

### URL Construction
Direct URL navigation is fastest (avoids cookie dialog + typing):
- Base: `https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS`
- With combined keywords: `https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS&keywords=Tech+Networking+Entrepreneurship` (use `+` to join terms)
- With single keyword: `https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS&keywords=Healthcare`
- Category filter: `https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS&category=technology` (or `career-and-business`, `support-and-coaching`)
  - ⚠️ Category pages trigger a cookie consent dialog — must dismiss before data extraction
  - Available category slugs: `technology`, `career-and-business`, `support-and-coaching`, `science-and-education`
- ⚠️ The `location` parameter uses slug format `ca--on--Toronto` (double dashes), NOT plain text like `Toronto`
- If you use `browser_type` in the search box instead, Meetup shows autocomplete suggestions (e.g., "Nursing", "Nursing Student") — click the suggestion button to trigger the search
- The `dateRange` parameter is NOT reliably supported — filter by date using the UI buttons after landing

### Data Extraction
Use `browser_console` with JS extraction (NOT `browser_snapshot` — the accessibility tree lumps all event card text together). The simplest working approach:

**Quick extraction (recommended — dedup by event ID):**
```javascript
const eventLinks = document.querySelectorAll('a[href*="/events/"]');
const results = [];
const seen = new Set();
eventLinks.forEach(link => {
  const href = link.href;
  const text = link.textContent.trim().replace(/\s+/g, ' ');
  const match = href.match(/\/events\/(\d+)/);
  if (match && !seen.has(match[1])) {
    seen.add(match[1]);
    results.push({ url: href, text: text.substring(0, 250) });
  }
});
JSON.stringify(results, null, 2);
```

**Detailed extraction (per-field, use if quick isn't enough):**
```javascript
const cards = document.querySelectorAll('a[href*="/events/"]');
const results = [];
const seenIds = new Set();
cards.forEach(card => {
  const href = card.href;
  const idMatch = href.match(/\/events\/(\d+)/);
  if (!idMatch || seenIds.has(idMatch[1])) return;
  seenIds.add(idMatch[1]);
  const heading = card.querySelector('h3, h2, [class*="heading"]');
  const title = heading ? heading.textContent.trim() : '';
  const timeEl = card.querySelector('time');
  const dateTime = timeEl ? timeEl.textContent.trim() : '';
  const fullText = card.textContent;
  const byMatch = fullText.match(/by\s+(.+?)(?:\d+ attendees|icon|$)/);
  const organizer = byMatch ? byMatch[1].trim() : '';
  const isOnline = fullText.includes('Online');
  const attendeeMatch = fullText.match(/(\d+)\s+attendees/);
  const attendees = attendeeMatch ? attendeeMatch[1] : '';
  // Strip tracking params for clean URL
  const cleanUrl = href.replace(/[?&](recId|recSource|searchId|eventOrigin)=[^&]*/g, '').replace(/\?$/, '');
  results.push({ title, dateTime, organizer, online: isOnline, attendees, eventId: idMatch[1], url: cleanUrl });
});
JSON.stringify(results, null, 2);
```

**Key extraction tips:**
- Meetup renders each event card TWICE on the page (visible card + offscreen duplicate). Dedup by event ID (the `\d+` in `/events/\d+`) to avoid double-counting.
- The `text` field from quick extraction includes title, date, organizer, venue, and attendees all concatenated — parse with regex in post-processing.
- Tracking params (`recId`, `searchId`, `recSource`, `eventOrigin`) make URLs unique per card instance — strip before comparing or storing.

### Delta Deduplication
- Use `session_search(query="Meetup Toronto events")` to find previous cron run summaries
- Compare **event IDs** (last path segment of the URL, e.g. `314110401`) against previously reported IDs
- Strip Meetup tracking params (`recId`, `searchId`, `recSource`) before comparing
- Only report events not seen in previous runs

### Career Categorization
- 🏥 **Healthcare & Nursing-Related**
- 💻 **Tech & Networking**
- 🚀 **Entrepreneurship & Startup**
- Include a **"Top Picks"** section highlighting events that bridge career transitions (e.g., HealthTech, AI in Healthcare)

### Career Exploration & Program Research

For career transition research beyond event monitoring:
- **Program discovery**: Focus on accelerated, second-entry, or bridge programs for career changers
- **Admissions contact**: Locate "Academic Advising" or "Admissions Recruitment" pages; request transcript reviews with specific program track
- **Inquiry template**: Subject: "Inquiry regarding [Program Type] prerequisites - [Your Name]"
- **Experience building**: Identify volunteer/support organizations in target field
- See `references/career-transition-programs.md` for Ontario-specific second-entry BScN programs, inquiry templates, and healthcare support organizations

**Pitfalls:**
- Do not assume a previous degree covers all prerequisites — always verify with admissions
- Always ask about "Second-Entry" or "Accelerated" programs rather than standard 4-year programs
- Professional keyword searches on event platforms often return social/wellness results — pivot to industry proxies
- Keep a running list of all admissions correspondence and transcript evaluations

### Notable Recurring Toronto Event Groups
- Toronto AI, Machine Learning and Computer Vision Meetup
- QueerTech Toronto
- Canadian Networking
- Startup Networking & Founder Ecosystem | Toronto
- Toronto Analytics.Club: Data & AI Community
- AWS User Group Toronto
- DevOps Toronto
- TechTO / TechTO Fintech
- Google Developer Group - Toronto (Google Cloud Labs events, 35-49 attendees)
- Metro Toronto Azure Community (Microsoft Build summaries, 51+ attendees)
- Toronto Java Users Group (Java+AI agent events, waitlist fills fast)
- Le Wagon Toronto - Learn Tech & AI Skills (career transition workshops, online)
- Recruiter POV (LinkedIn & resume clinics from tech recruiters, online)
- The Hip Haus - Young Professionals Networking (22+ attendees per event)
- WE CAN Network! (general networking, ⭐4.8)
- Toronto Ecom Network (ecommerce founder mixers)
- LeaderSHIFT (import/export and business model workshops, ⭐4.9)
- Employment Readiness Workshop (career pathway exploration, limited seats)
- Toronto - Exploring Health, Wealth & AI (confidence & boundary building, online)

### Pitfalls (Meetup-Specific)
- **"Nursing" keyword is unreliable**: Returns language exchanges, wellness workshops, meditation, social mixers. After 7+ cron runs, it has NEVER returned a professional nursing event. Use "Healthcare" as primary search term for professional events.
- **"Entrepreneurship" search often fails**: Meetup redirects to "Social Entrepreneurship" category with zero events. Use direct URL with `keywords=Entrepreneurship` instead of relying on category filters. Also try "Startup" as fallback.
- **Cookie consent dialog**: Dismiss the popup on first visit per session. It blocks the page content from rendering fully. Click the "Close" button.
- **URL tracking params**: Meetup appends `recId`, `recSource`, `searchId`, `eventOrigin`. Strip for dedup — these make the same event URL appear different across card instances.
- **Duplicate event cards on page**: Each event renders ~2x in the DOM (visible + offscreen). Always dedup by event ID (`/events/{id}/`), not by full URL.
- **Recurring events**: Some show "Every Mon" or "Every two weeks on Tue" — note recurrence pattern. These tend to be low-quality (meditation, language exchange) — filter accordingly.
- **`browser_vision` not always available**: Non-multimodal models fail with vision. Always use `browser_console` JS extraction.
- **`browser_snapshot` too coarse**: Accessibility tree merges all event card content into long text blocks. Use JS `querySelectorAll('a[href*="/events/"]')` instead.
- **No Nursing-to-Tech niche exists**: After 7+ monitoring runs, no Toronto Meetup group specifically targets the nursing→tech career transition. The best proxy events are: (1) Visual AI in Healthcare meetups, (2) Cross-sector AI roundtables, (3) General tech networking events where healthtech can be discussed.
- **CANCELLED events linger**: Meetup doesn't remove cancelled events from search results — they appear with "[CANCELLED]" in the title. Filter these out during post-processing.
