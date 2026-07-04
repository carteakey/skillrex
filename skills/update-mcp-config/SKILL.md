---
name: update-mcp-config
description: Update MCP server configuration consistently across Codex, Antigravity CLI, Antigravity/Gemini shared config, Docker Compose, Antigravity tool caches, and secret-safe backup notes. Use when adding, changing, testing, or documenting local MCP servers across multiple AI tools.
---

# Update MCP Config

Use this skill when a local MCP server should be available from more than one tool, especially Codex and Antigravity.

## Core Workflow

1. Identify the runnable server source of truth:
   - Docker Compose service, long-running local process, stdio command, or hosted HTTP endpoint.
   - Prefer Docker Compose for local HTTP MCP servers that should survive restarts.
2. Update Codex:
   - Config file: `/Users/kchauhan/.codex/config.toml`
   - HTTP MCP shape:
     ```toml
     [mcp_servers.name]
     url = "http://localhost:PORT/mcp"
     ```
   - Stdio MCP shape:
     ```toml
     [mcp_servers.name]
     command = "/path/to/command"
     args = ["arg1", "arg2"]
     ```
3. Update Antigravity CLI:
   - Config file: `/Users/kchauhan/.gemini/antigravity-cli/mcp_config.json`
   - HTTP MCP shape:
     ```json
     {
       "mcpServers": {
         "name": {
           "url": "http://localhost:PORT/mcp"
         }
       }
     }
     ```
   - Permission file: `/Users/kchauhan/.gemini/antigravity-cli/settings.json`
   - Add `"mcp(name/*)"` under `permissions.allow` when the tool should be callable without repeated permission prompts.
4. Update shared Gemini/Antigravity config when relevant:
   - Config file: `/Users/kchauhan/.gemini/config/mcp_config.json`
   - Existing local pattern uses:
     ```json
     {
       "mcpServers": {
         "name": {
           "serverUrl": "http://localhost:PORT/mcp"
         }
       }
     }
     ```
5. Refresh Antigravity tool cache when the server can be discovered:
   - CLI cache: `/Users/kchauhan/.gemini/antigravity-cli/mcp/<server>/`
   - App cache: `/Users/kchauhan/.gemini/antigravity/mcp/<server>/`
   - Write one JSON descriptor per tool using the existing cache shape:
     ```json
     {"name":"tool_name","description":"...","parameters":{...}}
     ```
   - Only refresh caches after a successful MCP `tools/list`.
6. Save a secret-safe backup/reference in the appropriate personal repo:
   - Life-related MCP skills and notes belong in `/Users/kchauhan/repos/lifedex`.
   - Store reconstruction snippets and instructions, not raw API tokens or bearer secrets.

## Testing

Do not stop at "container is up." Test the MCP protocol.

Minimum checks:

```bash
docker compose -f /path/to/docker-compose.yml config --quiet
docker compose -f /path/to/docker-compose.yml ps <service>
/Applications/Codex.app/Contents/Resources/codex mcp list
```

For HTTP MCP endpoints, perform:

1. `initialize`
2. `notifications/initialized`
3. `tools/list`
4. One safe read-only `tools/call` if the server exposes a harmless read tool.

For Paperless-like streamable HTTP servers, use `Accept: application/json, text/event-stream` and preserve the `Mcp-Session-Id` header from `initialize`.

If discovery works but a tool call fails, treat the setup as not finished. Check container logs, architecture mismatches, auth, endpoint path, and server transport assumptions.

## Safety

- Never copy raw API tokens, bearer tokens, passwords, private keys, or identity data into repo backups.
- Prefer placeholders such as `<paperless-api-token>` in tracked files.
- Preserve existing unrelated config entries and user edits.
- Validate JSON/TOML after edits.
- If an image is amd64-only on Apple Silicon and a real tool call crashes under emulation, build or choose a native arm64 image and document why.

## Useful Local Paths

- Codex config: `/Users/kchauhan/.codex/config.toml`
- Antigravity CLI MCP config: `/Users/kchauhan/.gemini/antigravity-cli/mcp_config.json`
- Antigravity CLI settings: `/Users/kchauhan/.gemini/antigravity-cli/settings.json`
- Shared Gemini MCP config: `/Users/kchauhan/.gemini/config/mcp_config.json`
- Antigravity CLI MCP cache: `/Users/kchauhan/.gemini/antigravity-cli/mcp`
- Antigravity app MCP cache: `/Users/kchauhan/.gemini/antigravity/mcp`
- Life MCP references: `/Users/kchauhan/repos/lifedex/reference`
- Life MCP skills: `/Users/kchauhan/repos/lifedex/skills`
