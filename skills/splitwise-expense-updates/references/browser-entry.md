# Splitwise Web Entry

Use this only after the core workflow has verified the source facts, target group, payer, and cent-exact shares.

## Entry sequence

1. Invoke the available browser-control skill and use a browser with the user's signed-in Splitwise session. If no session is signed in, open `https://secure.splitwise.com/login`, hand off login to the user when credentials or MFA are required, and resume only after they confirm it is ready.
2. Navigate visibly to the target group or friendship. Read the current activity and search likely duplicates before opening the form.
3. Click **Add an expense**. Inspect a fresh DOM snapshot and locate controls by their visible labels; do not hard-code coordinates or selectors across sessions.
4. Enter the verified description and total. Select every participant involved in the expense.
5. Use the sentence **Paid by [person] and split [method]** to choose the payer and split:
   - Keep **equally** only when cent allocation is acceptable and verified.
   - Use exact amounts for deterministic odd-cent allocation.
   - Use percentage or shares only when the user requested that representation and the resulting cents are verified.
6. Click the date field to set the transaction date. For a recurrence, also set weekly, fortnightly, monthly, or yearly and state that it continues indefinitely unless stopped. Configure an email reminder only when the user requests it.
7. Add category, notes, or receipt only when requested or source-backed. A receipt upload transmits a personal file and must follow the browser skill's upload and sensitive-data rules.
8. Re-read the visible form summary: group, participants, description, total, currency, payer, owed amounts, date, and recurrence. Ask for action-time confirmation when required by the browser policy, then click the final save control once.
9. Verify success from the saved expense or activity feed and the updated balance. Record any web-visible expense identifier when available; otherwise report that the browser UI did not expose one.

## Daily-limit handling

- Track successful creations during the current local day separately from attempted or failed submissions.
- Stop immediately when Splitwise displays its daily-limit warning. Do not retry through another interface or account to evade it.
- Keep unsubmitted expenses in a manual-entry table with an explicit future batch and `pending—daily limit` status.
- The official support material confirms that free accounts can add more expenses after the daily limit resets, but does not specify a universal numeric cap or reset hour. Use a user-observed cap only as a conservative local default and let the live UI override it.
- A friend may add an expense and mark another person as payer, but use that route only when the user explicitly asks that person to do so; never contact or impersonate them automatically.

## Recurring expenses

- In the web form, click the date field to open date and repeat settings.
- Recurrences post near the hour of original creation and continue until stopped.
- Editing the latest occurrence's amount changes future recurrences, not past ones.
- On web, open the latest occurrence and use **Cancel future recurrences** to stop it. Treat cancellation as a destructive cloud change and obtain the required confirmation.

## Fallback output

If login, browser control, or the quota blocks entry, return the core manual table plus `Batch` and `Status`. State the exact blocker and preserve the verified expense facts for a later browser pass.

## Authoritative references

- Splitwise Support: `https://kb.splitwise.com/balances-and-expenses/what-are-different-ways-i-can-split-an-expense`
- Splitwise Support: `https://kb.splitwise.com/balances-and-expenses/how-can-i-manage-recurring-expenses`
- Splitwise Support: `https://feedback.splitwise.com/knowledgebase/articles/2010350-why-am-i-seeing-an-expense-limit`
