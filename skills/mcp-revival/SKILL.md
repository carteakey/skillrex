---
name: mcp-revival
description: Diagnose and restore unavailable or partially failing local MCP servers across Codex, Gemini/Antigravity, OpenClaw, Docker, HTTP, stdio, and OAuth transports. Use when MCP tools disappear, initialization fails, a server is omitted as not ready, a port or endpoint is wrong, OAuth refresh is rejected, a local bridge needs relinking, or a configuration repair needs protocol-level verification.
---

# MCP Revival

Repair MCP availability from the transport outward. Treat “the process is running” as insufficient: an MCP is revived only after its client configuration, transport handshake, capability discovery, and one safe read-only operation work.

## Workflow

### 1. Establish scope and preserve state

- Identify the affected client(s), server name(s), and first failing operation.
- Read the repository README, relevant project notes, and any existing MCP setup skill before editing.
- Snapshot or inspect current config and logs without printing bearer tokens, API tokens, cookies, OAuth codes, phone numbers, or message contents.
- Preserve unrelated user edits. Do not kill every matching process, delete session databases, or rotate credentials as a first step.

### 2. Classify the failure

Check the client registry and recent logs, then classify each server as one or more of:

- **Configuration** — wrong command, runtime, working directory, URL, path, header, or transport.
- **Reachability** — service down, host port collision, Docker mapping mismatch, or a host listener answering instead of the intended container.
- **Protocol** — initialize succeeds but `tools/list`, a resource, or a safe read-only call fails; preserve the MCP session ID for streamable HTTP.
- **Authentication** — OAuth `invalid_grant`, expired bearer/API credential, or a linked-device session invalidated by the upstream service.
- **Stale runtime** — files and credentials are fixed on disk, but the client has cached the old server snapshot.
- **Build/runtime** — local stdio server cannot start because dependencies, architecture, or the configured executable is wrong.

Do not treat an `auth_status=unsupported` label on a local stdio server as a transport failure by itself; confirm it with an initialize probe.

### 3. Verify the source of truth

For each server, find the actual runnable source:

- Docker Compose service and host/container port mapping.
- Local stdio command, absolute executable, arguments, environment, and working directory.
- Hosted or local HTTP endpoint, expected path (`/mcp` versus legacy `/sse`), and required authorization header.
- OAuth-capable server and the client that owns its credential store.

Use the existing cross-client configuration workflow when changing registries. If the server is meant to work in multiple clients, update every in-scope registry and its secret-safe reference/backup together; do not leave one client pointing at the old port or transport.

### 4. Repair reachability and configuration

- Validate JSON/TOML and Compose configuration before restarting anything.
- For Docker-backed HTTP MCPs, run `docker compose config --quiet`, `docker compose ps`, and `docker compose port`. Check both `lsof` for the host port and container logs. A healthy container does not prove the host endpoint reaches it.
- If another process owns the intended host port, identify it first. Prefer changing only the host-side port (keep the container port stable), then update all client configs and documentation.
- For local stdio MCPs, verify the executable and dependency environment, then run the project’s build/test command when source changes or missing artifacts are suspected.
- Preserve secret injection patterns. Never copy a real token into a tracked backup or a skill.

### 5. Reauthorize only the affected OAuth client

When logs show a rejected refresh grant or the client reports unauthorized OAuth credentials:

1. Run the owning client’s supported login command (for Codex, `codex mcp login <server>`).
2. Complete the approval flow in the existing signed-in browser session when possible.
3. Wait for the command to report success; do not copy authorization codes or tokens into chat, shell history, or config files.
4. Remember that Codex, OpenClaw, and other clients may keep separate OAuth stores. A successful login in one client does not prove another client is authorized.

If browser login needs an account or verification step that is unavailable, leave the server registered, report the exact user action required, and continue verifying unrelated servers.

### 6. Verify the MCP protocol

For streamable HTTP, send a JSON-RPC `initialize` request with `Accept: application/json, text/event-stream`; capture the returned `Mcp-Session-Id`; then send `notifications/initialized` and `tools/list` with that session ID. For legacy SSE, follow the server’s documented event/message flow instead of assuming `/mcp` works.

For stdio, launch the configured command with a bounded timeout, send `initialize`, and confirm a valid JSON-RPC response containing `serverInfo` and protocol capabilities. Prefer a client-native probe when available.

After discovery, perform one harmless read-only call (for example, list metadata or count records). Initialization alone is not completion.

### 7. Refresh client state

- Reload the client’s MCP runtime/cache after config changes (for example, `openclaw mcp reload` for OpenClaw).
- Start a new Codex task or restart the Codex app when the current task still reports an old “not ready” snapshot after the on-disk config and OAuth store are fixed.
- Re-run the client’s list/status/doctor command and a bounded probe for every repaired server.

### 8. Handle linked-device bridges

For a WhatsApp-like bridge, distinguish MCP discovery from upstream account state:

- A successful MCP probe only proves the wrapper starts; it does not prove the linked device is authenticated.
- If the upstream service logs out the device, keep the bridge running, generate a fresh QR, and ask the user to scan it in the upstream app’s linked-device screen.
- Verify the bridge’s authenticated/connected log, local REST health endpoint, and one read-only MCP operation. Keep session databases; do not delete them to force a login.
- If a REST health endpoint fails on a nullable database field, fix the source scan/model handling rather than masking it with a destructive database reset.

## Verification checklist

Report each server with a concrete result:

- config parses and points at the intended command/URL;
- service/listener is reachable;
- MCP `initialize` succeeds;
- `tools/list` (or equivalent capability discovery) succeeds;
- one safe read-only call succeeds;
- OAuth/linked-device state is authorized, or the exact user step remains;
- client runtime was reloaded or a restart/new task is required.

Use bounded commands and redact sensitive output. Record material repairs in the repository’s required session log, including files/systems touched, decisions, and follow-ups.

## Safety boundaries

- Start read-only. Ask before destructive, bulk, or credential-rotating actions unless the user explicitly requested them.
- Do not expose secrets from config, environment, keychain, browser, or logs.
- Do not send messages, edit financial/document data, or perform non-read-only MCP calls merely to test availability.
- Do not broaden a port or process cleanup beyond the identified server. Preserve unrelated services and user work.
