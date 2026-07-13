# Temporal Archival — Full Reference

Workflow for time-based email archival or cleanup (e.g., archiving OTPs/Security alerts older than 24h) using Python and the `himalaya` CLI.

## Temporal Logic

Compare email dates against the current time using timezone-aware objects.

```python
import datetime

def is_older_than(date_str, days=1):
    try:
        # Standardize for fromisoformat
        iso_str = date_str.replace(" ", "T", 1)
        if "+" not in iso_str and "Z" not in iso_str:
            iso_str += "Z"
        email_date = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - email_date) > datetime.timedelta(days=days)
    except:
        return False
```

### Alternative: Regex-based Date Parsing
For more robust handling of varying date formats:
```python
import re, datetime

def is_older_than(date_str, days=1):
    match = re.search(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})", date_str)
    if match:
        dt = datetime.datetime.fromisoformat(f"{match.group(1)}T{match.group(2)}")
        dt = dt.replace(tzinfo=datetime.timezone.utc)
        return (datetime.datetime.now(datetime.timezone.utc) - dt) > datetime.timedelta(days=days)
    return False
```

## Workflow
1. Fetch emails in pages (40-50 per page).
2. Filter by age using `is_older_than()`.
3. Chunk IDs for bulk moves (50 at a time).
4. Provide fallback for individual moves if bulk move fails.

## Pitfalls
- **NoneType String Errors**: `himalaya` JSON fields like `name` or `addr` can be `null`. Use `str(val or "")` or f-strings: `f"{name or ''} {addr or ''}"`.
- **Stdout Truncation**: `execute_code` has a 50KB stdout cap. Stick to page sizes of 40-50.
- **Log Noise**: `himalaya` often emits WARN or INFO logs. Always use `json_parse()` instead of `json.loads()`.
- **Folder Delimiters**: Use the correct delimiter for the IMAP server (usually `/`).
- **Timezone Awareness**: Always use `datetime.timezone.utc` when comparing with `now()`.

## Refined Security Filtering Pattern
```python
def is_security_email(subject, sender):
    subj = (subject or "").lower()
    sndr = (sender or "").lower()

    # 1. EXCLUSIONS (False Positives)
    if any(k in subj for k in ['re:', 'fwd:', 'renewal', 'payout', 'booking', 'itinerary', 'statement']):
        return False

    # 2. STRICT INCLUSIONS (OTP/Alerts)
    security_keywords = [
        'verification code', 'one time password', '(otp)', 'security alert', 'new login',
        'magic sign in code', 'validate your account', 'password reset', 'verify your identity',
        'unusual sign-in activity', 'login code', 'apple account was used to sign in',
        'new device logged in', 'action required: new login'
    ]
    return any(kw in subj for kw in security_keywords) or ('mcafee' in sndr and 'alert' in subj)
```
