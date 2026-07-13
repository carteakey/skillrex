# Cron Job Reporting Protocol

When running as a scheduled cron job, strict adherence to delivery instructions is required to prevent unnecessary notifications.

## Delivery Rules

1.  **No Self-Delivery**: Do NOT use `send_message` or attempt to deliver the output yourself. The system handles delivery of the final response.
2.  **Silent Mode**: If there are no new findings, respond with exactly `[SILENT]` and nothing else.
    - Correct: `[SILENT]`
    - Incorrect: `[SILENT] No new events found.`
3.  **Final Response**: The primary content must be in the final response itself.

## Prompt Context
Always check the prompt for specific `[IMPORTANT]` or `[SYSTEM]` instructions regarding:
- Delivery method.
- Silent response requirements.
- Formatting constraints.
