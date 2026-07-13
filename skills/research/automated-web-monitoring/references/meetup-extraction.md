# Meetup.com Event Extraction Pattern

When scraping Meetup.com, use `browser_console` to extract structured data to avoid parsing messy HTML/text snapshots.

## JavaScript Extraction Pattern

Use this pattern in `browser_console(expression=...)`:

```javascript
Array.from(document.querySelectorAll('main a[href*="/events/"]')).map(a => ({
  title: a.innerText.split('\n')[0],
  time: a.innerText.split('\n')[1],
  url: a.href
}))
```

## Verification
After extraction, verify the results by checking if the URLs and titles match the expected structure.
