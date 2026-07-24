---
name: did-openai-cook-my-drive
description: Checks if the user is affected by the OpenAI Codex CLI SSD wear bug (TRACE logging to SQLite). Diagnoses the local database size, version, and guides the user on checking SSD write wear stats on Linux, macOS, and Windows.
---

# did-openai-cook-my-drive

This skill helps the agent audit the local workstation or connected machines for the **OpenAI Codex CLI SSD wear bug**. It checks the size of Codex logs, checks the installed version of Codex, and provides instructions to query SSD lifetime write endurance.

## 1. Quick Diagnostic Run
The skill includes a pre-packaged Bash script that automates the audit on Linux and macOS:

```bash
# Run the diagnostic script
/home/kchauhan/.agents/skills/did_openai_cook_my_drive/scripts/check_drive.sh
```

## 2. Platform-Specific Manual Audit & Remediation

### Linux
1. **Check Log Size:**
   ```bash
   ls -lh ~/.codex/logs_2.sqlite*
   ```
2. **Check Version:**
   ```bash
   codex --version
   ```
   *Versions before 0.142.x are fully vulnerable.*
3. **Query SSD Endurance:**
   Identify your NVMe SSD name (e.g. `/dev/nvme0` or `/dev/nvme1`) and run:
   ```bash
   sudo smartctl -A /dev/nvme0
   ```
   Look at the `Data Units Written` line.
4. **Remediation:**
   * Update immediately:
     ```bash
     npm install -g @openai/codex@latest
     # or
     codex update
     ```
   * Stopgap (Redirect to RAM):
     ```bash
     mkdir -p "/dev/shm/codex-$(id -u)" && chmod 700 "/dev/shm/codex-$(id -u)"
     rm -f ~/.codex/logs_2.sqlite ~/.codex/logs_2.sqlite-wal ~/.codex/logs_2.sqlite-shm
     ln -s "/dev/shm/codex-$(id -u)/logs_2.sqlite" ~/.codex/logs_2.sqlite
     ```

### macOS
1. **Check Log Size:** Same as Linux (`~/.codex/logs_2.sqlite`).
2. **Check Version:** `codex --version`.
3. **Query SSD Endurance:**
   Install `smartmontools` via Homebrew:
   ```bash
   brew install smartmontools
   sudo smartctl -A /dev/disk0
   ```
4. **Remediation:**
   * **Do NOT use `/tmp` symlinking.** On macOS, `/tmp` is not a RAM disk and sits on your physical SSD.
   * Update Codex cask or package:
     ```bash
     brew upgrade --cask codex
     ```

### Windows
1. **Check Log Size:** Check `%USERPROFILE%\.codex\logs_2.sqlite`.
2. **Query SSD Endurance:**
   * Download and run **CrystalDiskInfo**.
   * Read **Total Host Writes** or **Total NVMe Host Writes**.
3. **Remediation:**
   * Update Codex:
     ```cmd
     npm install -g @openai/codex@latest
     ```
