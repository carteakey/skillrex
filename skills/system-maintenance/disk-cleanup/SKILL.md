---
name: disk-cleanup
description: Safely clean up system disk space by clearing trash, browser and development caches, and unused user-level runtime data; use when the user asks to free space or audit disk usage.
---

# System Disk Cleanup Skill

This skill allows the agent to safely clean up system disk space by emptying the trash, clearing large browser and development caches, and removing unused flatpak runtimes.

## Usage

When the user asks to "clean up disk space" or "free up space", the agent should:
1. Run the `scripts/system_cleanup.sh` script to perform user-level cleanup.
2. Advise the user to manually run the following commands if they want to perform system-level cleanup (as they require `sudo` privileges):
   - `sudo flatpak uninstall --unused -y`
   - `sudo pacman -Sc`

## Scripts

- `scripts/system_cleanup.sh`: A safe bash script to clean up `~/.local/share/Trash`, `~/.cache`, and user-level Flatpak runtimes.
