---
name: tpl-map-pass-monitor
description: Monitor Toronto Public Library MAP/ePass availability for configured attractions and report only when target passes are available; use for TPL MAP pass checks, heartbeat checks, and silent-if-no-results scheduled runs.
---

# TPL MAP Pass Monitor

Monitor the Toronto Public Library MAP/ePass portal for target attractions and report available passes. Keep this skill credential-free: read the library card and PIN from the runtime environment or the user's secret manager.

## Inputs

- `TPL_LIBRARY_CARD` - library card number.
- `TPL_PIN` - library PIN.
- `TPL_MAP_URL` - default `https://epass-ca.quipugroup.net/?clientID=16&libraryID=1`.
- `TPL_TARGETS` - comma-separated attraction names. Historical targets: Aquarium, Toronto Zoo, Canadian Stage, Tafelmusik.

## Workflow

1. Confirm credentials are available from environment or an approved secret source. Never echo the card number or PIN in logs or reports.
2. Open the TPL MAP URL with browser automation or a script.
3. Log in with the card and PIN.
4. Search or scan pass inventory for each configured target.
5. Normalize attraction names before matching. Treat case, punctuation, and venue suffix differences as non-meaningful.
6. If no target passes are available, return exactly `[SILENT]`.
7. If passes are available, report:
   - attraction name
   - available date/time or pass window
   - booking URL or next action
   - any limits or expiry shown on the portal

## Heartbeat Mode

Use heartbeat mode only to confirm the monitor is alive. Do not include credentials. A heartbeat should state that the monitor ran, whether login worked, and whether the pass scan completed.

## Scheduling

Historical schedules from the old automation state:

- Pass monitor: every 5 minutes, paused on 2026-04-05.
- Heartbeat: hourly, paused on 2026-04-05.

Recreate scheduling outside this skill using cron, systemd timers, GitHub Actions, or the active agent's scheduler.

## Safety

- Do not commit TPL credentials.
- Do not send recurring "nothing found" messages.
- Ask before booking, reserving, or changing account state.
