# Scheduled Event Monitoring Jobs

Historical recurring event-monitoring jobs from the old automation state.

## Meetup Event Discovery

- Schedule: `0 9 * * *`
- Location: Toronto, ON.
- Interests: healthcare, nursing transition, tech, networking, entrepreneurship.
- Source: `https://www.meetup.com/find/?location=ca--on--Toronto&source=EVENTS`
- Reporting: return exactly `[SILENT]` if no new events are found.

## Workflow

1. Open the Meetup discovery URL with browser automation or an HTTP-capable extraction script.
2. Search for relevant terms.
3. Extract event title, date, time, venue, and URL.
4. Compare against previously reported event URLs or IDs.
5. Report only new or high-value matches.
6. Keep reports short and actionable.
