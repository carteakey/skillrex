---
name: did-openai-cook-my-drive
description: Checks if the user is affected by the OpenAI Codex CLI SSD wear bug (TRACE logging to SQLite). Diagnoses the local database size, version, and guides the user on checking SSD write wear stats on Linux, macOS, and Windows.
---

# did-openai-cook-my-drive

This skill helps the agent audit the local workstation or connected machines for the **OpenAI Codex CLI SSD wear bug**. It checks the size of Codex logs, checks the installed version of Codex, and provides instructions to query SSD lifetime write endurance.

## 1. Quick Diagnostic Run
The skill includes a pre-packaged Bash script that automates the audit on Linux and macOS:

```bash
# Local run
./scripts/check_drive.sh

# Remote run over SSH (e.g. M1 Mac or Linux server)
ssh user@remote-host 'bash -s' < ./scripts/check_drive.sh
```

## 2. Key Technical Learnings & Platform Guidance

### macOS
1. **Log Location:** `~/.codex/logs_2.sqlite*`
2. **Path Considerations:**
   * Homebrew binaries on Apple Silicon reside at `/opt/homebrew/bin/brew` and `/opt/homebrew/bin/smartctl`.
   * `smartctl` on Apple Silicon macOS does not require `sudo` to read `/dev/disk0` SMART attributes.
3. **Hardware NVMe Wear Verification:**
   * Run: `/opt/homebrew/bin/smartctl -a /dev/disk0`
   * Key lines to inspect:
     - `Percentage Used`: Physical NAND wear indicator (0% = brand new, 100% = rated TBW reached).
     - `Data Units Written`: Total lifetime bytes written to flash (multiply by 512,000 bytes per unit, e.g., `175,042,208` units = ~89.6 TB).
     - `SMART overall-health self-assessment test result`: Should read `PASSED`.
4. **Remediation Note:**
   * **Do NOT use `/tmp` symlinking on macOS.** On APFS, `/tmp` and `$TMPDIR` sit directly on the physical SSD volume, not in a RAM disk. The only proper fix is updating `codex-cli` (`npm install -g @openai/codex@latest` or `brew upgrade`).

### Linux
1. **Log Location:** `~/.codex/logs_2.sqlite*`
2. **SSD Endurance:**
   * Run: `sudo smartctl -A /dev/nvme0n1`
   * For unprivileged status, inspect `/proc/diskstats` or `/sys/class/block/nvme0n1/stat` to monitor sector read/write rates.
3. **Stopgap (RAM Redirect):**
   ```bash
   mkdir -p "/dev/shm/codex-$(id -u)" && chmod 700 "/dev/shm/codex-$(id -u)"
   rm -f ~/.codex/logs_2.sqlite*
   ln -s "/dev/shm/codex-$(id -u)/logs_2.sqlite" ~/.codex/logs_2.sqlite
   ```

### Long-Term Monitoring (Scrutiny)
For self-hosted homelabs with multiple nodes (workstations, Mac servers, Linux media hosts), deploy **Scrutiny** (WebUI + `scrutiny-collector`) to track SMART attribute trends and alert on write endurance anomalies before drive failure occurs.

---

## References
* OpenAI Codex SSD Wear Issue: [openai/codex#28224](https://github.com/openai/codex/issues/28224)
* Scrutiny SMART Dashboard: [AnalogJ/scrutiny](https://github.com/AnalogJ/scrutiny)

