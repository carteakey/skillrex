---
name: whatsapp-bridge
description: Operate and troubleshoot Kartikey's local WhatsApp MCP bridge. Use when Codex needs to query WhatsApp messages, unread chats, contacts, media, YouTube links, send messages/files/audio, verify the bridge/MCP server health, refresh WhatsApp history, interpret phone sync notifications, or repair the local whatsapp-mcp setup under /Users/kchauhan/services/whatsapp-mcp.
---

# WhatsApp Bridge

## Core Context

- Service repo: `/Users/kchauhan/services/whatsapp-mcp`
- Bridge repo: `/Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge`
- MCP server repo: `/Users/kchauhan/services/whatsapp-mcp/whatsapp-mcp-server`
- Message DB: `/Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge/store/messages.db`
- Session DB: `/Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge/store/whatsapp.db`
- Bridge API: `http://127.0.0.1:8080/api`
- Long-running bridge: `screen -S whatsapp-bridge`

Prefer MCP WhatsApp tools when they are available. Use shell/API checks when the MCP tools return empty results unexpectedly or when debugging bridge health.

## Quick Health Check

Run these from anywhere:

```bash
screen -ls
lsof -iTCP:8080 -sTCP:LISTEN -n -P
curl -sS http://127.0.0.1:8080/api/chats
sqlite3 /Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge/store/messages.db \
  'SELECT "chats", count(*) FROM chats UNION ALL SELECT "messages", count(*) FROM messages;'
```

Expected:

- `screen -ls` shows `whatsapp-bridge`.
- `lsof` shows `whatsapp-bridge` listening on `127.0.0.1:8080`.
- `/api/chats` returns JSON with `"success":true`.
- The DB has nonzero chat/message counts once synced.

If MCP unread/search calls return `[]`, first determine whether the DB is genuinely empty or the bridge/MCP layer is stale.

## Common MCP Tasks

Use the WhatsApp MCP tools directly when exposed:

- `get_unread_messages(limit=...)` for unread chat summaries.
- `list_messages(query="youtube.com" | "youtu.be" | "youtube", include_context=true)` for link searches.
- `list_chats(limit=..., include_last_message=true, sort_by="last_active")` to confirm message visibility.
- `download_media(message_id, chat_jid)` for local media retrieval.
- `send_message`, `send_file`, and `send_audio_message` only when the user explicitly asks to send something.

When searching YouTube links, query at least:

- `youtube.com`
- `youtu.be`
- `youtube`

If no matches appear, say that the currently synced store has no matches; do not imply WhatsApp itself has no older matches.

## Refreshing Data

The bridge exposes a local history refresh endpoint:

```bash
curl -sS -X POST http://127.0.0.1:8080/api/history-sync \
  -H 'Content-Type: application/json' \
  -d '{"max_chats":1,"messages_per_chat":10}'
```

Use low-noise refreshes first:

- Prefer `chat_jid` when the user knows the target chat.
- Otherwise start with `max_chats: 1` and `messages_per_chat: 10`.
- Avoid repeated broad refreshes unless the user accepts phone notifications.

Supported JSON:

```json
{
  "chat_jid": "optional-chat-jid",
  "max_chats": 25,
  "messages_per_chat": 50
}
```

The MCP server code includes a `refresh_data(chat_jid=None, max_chats=25, messages_per_chat=50)` wrapper. If the current Codex session does not expose it as `mcp__whatsapp.refresh_data`, use the HTTP endpoint or Python wrapper directly:

```bash
cd /Users/kchauhan/services/whatsapp-mcp/whatsapp-mcp-server
uv run python - <<'PY'
import whatsapp
print(whatsapp.refresh_data(max_chats=1, messages_per_chat=10))
PY
```

Phone notifications like `Syncing...`, `Tap to resume`, `Syncing stopped`, or `Finished syncing` are normal for on-demand linked-device history sync. Explain that the phone is responding to the bridge; it does not mean a chat message was sent to another person.

## Restarting the Bridge

To restart cleanly:

```bash
screen -S whatsapp-bridge -X quit 2>/dev/null || true
lsof -tiTCP:8080 -sTCP:LISTEN | xargs -r kill
cd /Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge
go build -o whatsapp-bridge .
screen -dmS whatsapp-bridge /bin/bash -lc 'cd /Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge && ./whatsapp-bridge'
sleep 6
lsof -iTCP:8080 -sTCP:LISTEN -n -P
```

Use `screen -r whatsapp-bridge` to watch logs. Detach with `Ctrl-a d`.

## Known Failure Modes

### Empty DB or stale schema

If `/api/chats` fails with `no such column: unread_count` or MCP returns nothing while the bridge is running, inspect schema/counts:

```bash
sqlite3 /Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge/store/messages.db '.schema chats'
sqlite3 /Users/kchauhan/services/whatsapp-mcp/whatsapp-bridge/store/messages.db '.schema messages'
```

The bridge should migrate old DBs to include:

- `chats.unread_count`
- `messages.is_read`

If this regresses, repair code in `whatsapp-bridge/main.go` rather than relying only on one-off `ALTER TABLE` commands.

### History sync panic

Do not call `BuildHistorySyncRequest(nil, ...)`. The current `whatsmeow` version expects a `types.MessageInfo` anchor. The bridge should request history before the oldest locally stored message per chat and send it with `SendPeerMessage`.

### Duplicate MCP servers

If behavior is weird, check for duplicate Python MCP server pairs:

```bash
ps aux | rg -i 'whatsapp-mcp-server|whatsapp-bridge'
```

Duplicate MCP servers can point at stale state. Do not kill processes blindly if a user task is mid-flight; explain what you found first.

## Safety

- Never send WhatsApp messages/files/audio unless the user explicitly requests the send.
- Do not delete `whatsapp.db`; it holds the linked-device session and may require QR reauth.
- Do not delete `messages.db` unless the user explicitly wants a full resync and accepts the tradeoff.
- Treat phone numbers, JIDs, chat names, and message contents as private. Summarize only what is needed for the user’s request.
