---
name: event-monitoring
description: Automate the discovery and reporting of new items from web sources with robust deduplication.
---
# Event Monitoring
Automate the discovery and reporting of new items (events, news, updates) from web sources, ensuring deduplication against previous reports.

## Trigger
When the user requests a recurring check for new items on a website (e.g., "Monitor Meetup for X", "Track new Reddit posts for Y").

## Workflow
1. **Establish Baseline**: Use `session_search` to find the most recent report and extract the list of already-reported unique identifiers (IDs or normalized URLs).
2. **Data Extraction**:
    - Navigate to the target URL using `browser_navigate`.
    - Use `browser_console` to execute JavaScript for high-fidelity, structured data extraction. This is faster and more accurate than vision for large lists.
3. **Deduplication**:
    - Use `execute_code` to compare the new list against the baseline.
    - **Crucial**: Always normalize identifiers (e.g., `url.rstrip("/")`) or extract unique database IDs from the URL to prevent duplicates caused by trailing slashes or query parameters.
4. **Reporting**:
    - Categorize findings.
    - Highlight "High Value" or "Actionable" items.
    - If no new items are found, use `[SILENT]` to suppress delivery.

## Pitfalls
- **URL Mismatch**: Do not rely on exact string matching for URLs; normalize them first.
- **Vision Latency**: Avoid using `browser_vision` for structured lists; use `browser_console` for efficiency.
- **Silent Failure**: If no new items are found, ensure the response is exactly `[SILENT]` to prevent unnecessary notifications.

## References
- `references/meetup-monitoring-workflow.md`
- `references/scheduled-jobs.md`
