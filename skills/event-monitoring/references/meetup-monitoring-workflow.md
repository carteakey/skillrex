# Meetup Monitoring Workflow

This document outlines the specific implementation used to monitor Meetup.com events for a user's career transition interests.

## 1. Extraction Pattern (JavaScript)
To extract structured data efficiently, use `browser_console` with the following pattern:

```javascript
Array.from(document.querySelectorAll('a[href*="/events/"]')).map(a => {
  const title = a.querySelector('h3')?.innerText || a.innerText;
  const url = a.href.split('?')[0]; // Remove query params
  const timeText = a.querySelector('time')?.innerText || "";
  const hostText = a.innerText.split('by ')[1] || "";
  return { title, url, timeText, hostText };
}).filter(e => e.title && e.url);
```

## 2. Deduplication Strategy (Python)
To prevent duplicate reporting due to URL variations (like trailing slashes), use `execute_code` to normalize URLs and compare against a set of IDs from previous sessions.

```python
# 1. Normalize previously reported URLs
previously_reported_normalized = {url.rstrip("/") for url in previously_reported_urls}

# 2. Extract IDs from current events for even more robust matching
truly_new = []
for url, event in all_current_events.items():
    # Extract event ID from URL (e.g., .../events/314665929/)
    parts = url.rstrip("/").split("/")
    event_id = parts[-1] if parts else ""
    
    if event_id and event_id not in previously_reported_ids:
        truly_new.append(event)
```

## 3. Session History Retrieval
Always use `session_search(query="...", limit=X)` to find the most recent successful report before starting the new scan.
