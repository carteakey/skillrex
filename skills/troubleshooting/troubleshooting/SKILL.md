---
name: troubleshooting
description: Diagnose and fix common infrastructure, tooling, and runtime issues in the AI agent environment. Covers Playwright browser executable errors, dependency version mismatches, PATH problems, and other recurring troubleshooting patterns.
---

# Troubleshooting Hub

Umbrella skill for diagnosing and fixing common issues in the AI agent environment. Each subsection covers a specific class of problem with step-by-step resolution.

## General Troubleshooting Principles

1. **Read the error message carefully** — most errors contain the exact path, version, or flag that's wrong.
2. **Check versions and paths** — version mismatches (binary expects X, system has Y) are the most common root cause.
3. **Don't fight the package manager** — if a tool expects a specific version, symlink or shim rather than downgrading.
4. **Verify the fix** — always re-run the failing command after applying a fix.
5. **Check environment consistency** — cron jobs, background processes, and subagents may have different PATH/env than the main session.

## Playwright Browser Executable Errors

When `browser_navigate` or other `browser_*` tools fail with:
```
browserType.launch: Executable doesn't exist at /home/.../.cache/ms-playwright/chromium_headless_shell-<OLD_VERSION>/chrome-headless-shell-linux64/chrome-headless-shell
```

This means the browser tool expects a specific Playwright binary version, but the installed version differs.

### Resolution

**Do NOT try to downgrade Playwright.** Install the latest version and symlink:

1. **Install latest Playwright browsers:**
   ```bash
   npx playwright install chromium
   ```
   Use `pty: true` and `timeout: 300` (downloads hundreds of MBs).

2. **Check which version was actually installed:**
   ```bash
   ls -l ~/.cache/ms-playwright/
   ```
   Look for the newer version directory (e.g., `chromium_headless_shell-1217`).

3. **Create symlinks to the expected path:**
   For `chromium_headless_shell`:
   ```bash
   mkdir -p ~/.cache/ms-playwright/chromium_headless_shell-<OLD_VERSION>/chrome-headless-shell-linux64/
   ln -s ~/.cache/ms-playwright/chromium_headless_shell-<NEW_VERSION>/chrome-headless-shell-linux64/chrome-headless-shell ~/.cache/ms-playwright/chromium_headless_shell-<OLD_VERSION>/chrome-headless-shell-linux64/chrome-headless-shell
   ```
   For standard `chromium` (if required):
   ```bash
   mkdir -p ~/.cache/ms-playwright/chromium-<OLD_VERSION>/chrome-linux/
   ln -s ~/.cache/ms-playwright/chromium-<NEW_VERSION>/chrome-linux/chrome ~/.cache/ms-playwright/chromium-<OLD_VERSION>/chrome-linux/chrome
   ```

4. **Verify:** Retry `browser_navigate` — it should now work via the symlink.

## Adding New Troubleshooting Sections

When a new recurring issue is diagnosed:
1. Add a new `##` subsection with a descriptive name
2. Include the error symptom, root cause, and resolution steps
3. Move session-specific details to `references/<topic>.md`
