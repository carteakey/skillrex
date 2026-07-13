# Scheduled Email Jobs

Historical email cron jobs from the old automation state. These jobs are folded into the `email-management` skill instead of separate skills.

## Newsletter Cleanup

- Schedule: `0 10 * * 6`
- Scope: `personal` and `primary` Himalaya accounts.
- Action: move newsletter senders to the newsletters folder.
- Silent behavior: report only moved counts or errors.

Use domains from the newsletter cleanup reference and update them as senders change.

## OTP/Security Cleanup

- Schedule: `0 11 * * 6`
- Scope: `INBOX` on configured accounts.
- Action: move expired OTP, login-code, and security-alert mail older than 24 hours to `Admin/Security Logs`.
- Safety: leave messages in place when date parsing fails.

## Smart Inbox Organizer

- Schedule: `0 12 * * 6`
- Scope: `INBOX` on configured accounts.
- Action: categorize mail into folders such as `Finance/Banking`, `Finance/Orders`, `Updates/Newsletters`, `Updates/Promotions`, and `Career/Job Search`.
- Safety: do not move security/OTP messages during general organization.
- Silent behavior: return exactly `[SILENT]` if nothing moved.

## Runtime Requirements

- `himalaya` installed and configured.
- Folder names should be verified before moving messages.
- Use non-interactive flags such as `-y` where Himalaya may prompt.
