---
name: automated-web-monitoring
description: Automated web monitoring and periodic data extraction.
---

# Automated Web Monitoring

Automated web monitoring is used to periodically check websites for specific updates, events, or data points relevant to a user's interests.

## Workflow

1.  **Discovery & History**: Use `session_search` to identify previous reports and avoid duplicate notifications.
2.  **Navigation**: Use `browser_navigate` to reach the target site.
3.  **Interaction**: Use `browser_type` and `browser_press` to perform searches or apply filters.
4.  **Structured Extraction**: Use `browser_console` to execute JavaScript and extract data in a structured format (e.g., JSON) rather than relying on text snapshots. This is more robust against UI changes.
5.  **Deduplication**: Compare current findings against `session_search` results.
6.  **Reporting**:
    - Report new items clearly.
    - If no new items are found, respond exactly with `[SILENT]` to suppress delivery.
    - For cron jobs, strictly follow the specific delivery and silent instructions provided in the prompt.

## Pitfalls
- **Bot Detection**: Web scraping via browser can trigger bot detection. If blocked, consider using a residential proxy or different search patterns.
- **UI Changes**: Web elements change. Always use `browser_console` to verify selectors if extraction fails.
- **Truncation**: Long lists of events may be truncated by the model's output limit. If a response is truncated, use a continuation prompt.

## References
- [[meetup-extraction|Meetup.com Event Extraction Pattern]]
- [[cron-reporting|Cron Job Reporting Protocol]]
