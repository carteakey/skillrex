---
name: email-management
description: "Comprehensive email management: CLI control with Himalaya, specialized auditing, and automated workflows for inbox organization, security, and cleanup."
---

# Email Management

A complete toolkit for managing email accounts, from manual CLI operations to automated high-density auditing and inbox organization.

## 1. CLI Management (Himalaya)
Use Himalaya for direct, terminal-based control of your email accounts via IMAP/SMTP.
- **Core Operations:** List, read, write, reply, forward, search, and organize emails.
- **Advanced Features:** Message composition via MML, multiple account management, and structured JSON output for automation.
- **Reference:** Detailed CLI usage and configuration guides are in `references/himalaya/`.

## 2. Specialized Auditing
Use this for high-density, categorized extraction of specific entities across multiple accounts.
- **Use Cases:** Finding all domains, identifying all subscriptions, or auditing account statuses (Active/Expired).
- **Preferred Output:** Extreme conciseness; direct lists of entities and their statuses.
- **Reference:** Formatting standards are in `references/email_auditing_format.md`.

## 3. Automated Workflows
Automate repetitive email tasks to maintain a zero-inbox or highly organized state.
- **Newsletter Cleanup:** Move newsletters to dedicated folders using targeted search.
- **Security/OTP Archival:** Identify and archive security alerts and one-time passwords after they expire.
- **Smart Inbox Organization:** Rules-based categorization (e.g., Finance, Updates, Career).
- **Temporal Archival:** Time-based cleanup of old emails (e.g., OTPs older than 24h).
- **Automation Reference:** Detailed logic and templates are in `references/automation/`.

## Pitfalls
- **Non-interactive environments:** Always use the `-y` flag with `himalaya` when running from agents or scripts to avoid hanging on prompts.
- **Gmail IMAP:** When deleting, you may need to move messages to `[Gmail]/Trash` instead of using direct `delete` commands.
- **Search Syntax:** Wrap multi-word search terms in quotes to ensure correct parsing.
- **Automation Parsing:** Always use robust JSON parsing (e.g., `json_parse`) to handle potential log noise in `himalaya`'s stdout.
