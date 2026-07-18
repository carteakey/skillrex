---
name: vault-76-organization
description: Summarize and organize a local Markdown notes vault by pulling latest changes, reviewing recent notes, extracting tasks, and producing a concise executive digest.
---

# Vault-76 Organization

Create a concise operational digest from `~/repos/vault-76` or another configured Markdown vault. This skill is for reporting and triage by default; do not move, rewrite, or delete notes unless the user explicitly asks.

## Workflow

1. Open the vault directory and inspect git status.
2. Pull latest changes only when the user permits network/git writes or the scheduler is configured to do so.
3. Identify Markdown files changed in the review window, historically the last 24 hours for scheduled runs.
4. Read the relevant changed notes.
5. Produce:
   - an executive summary paragraph of 3-5 sentences
   - 3-5 noteworthy notes with one-sentence impact summaries
   - actionable tasks found from `- [ ]`, `TODO:`, `Task:`, or equivalent markers
   - any blocked or ambiguous items that need user review
6. If no meaningful changes or tasks exist, say that directly and keep the report brief.

## Historical Schedule

The old automation ran weekly on Saturday at 09:00. Its prompt said "daily", but the recorded cron expression was `0 9 * * 6`; treat the cron expression as the source of truth.

## Safety

- Do not restructure notes during a scheduled digest.
- Do not create commits unless the user asks.
- Preserve note wording unless explicitly asked to rewrite or reorganize.
