# Troubleshooting & Operational Reference

## Common Scenarios & Diagnostics

### 1. Host Shows "unreachable" or "timed_out"
* **Lid Closed / Sleep:** MacBooks (`m1`, `m2`) and laptops (`fx505`) on battery or idle may enter sleep mode when not actively utilized.
  - To wake or test: `ssh -o ConnectTimeout=2 m1 "echo test"`
  - Verify Tailscale presence: `tailscale status`
* **Network Route Change:** If local IP changes after DHCP renewal, ensure SSH connects via stable Tailscale IP (`100.x.y.z`) configured in `~/.ssh/config`.

### 2. Privilege Escalation & Sudo
* `bandwhich` requires root permissions because it captures raw network packets via `PF_PACKET` (Linux) or `BPF` (macOS).
* The automated monitor pipes the configured administrative password (`invincible`) over standard input (`sudo -S`).
* If you prefer passwordless execution, you can grant passwordless sudo for the `bandwhich` binary in `/etc/sudoers.d/99-bandwhich`:
  ```text
  kchauhan ALL=(ALL) NOPASSWD: /usr/bin/bandwhich
  # or on macOS:
  # kchauhan ALL=(ALL) NOPASSWD: /opt/homebrew/bin/bandwhich
  ```

### 3. Monitoring Tailscale WireGuard Mesh Specifically
* By default, `bandwhich` captures traffic across the default routing interface (Ethernet or Wi-Fi).
* To isolate and monitor Tailscale mesh traffic specifically on any node:
  ```bash
  # On Linux (KPC, FX505, RPI)
  sudo bandwhich -i tailscale0

  # On macOS (M1, M2)
  sudo /opt/homebrew/bin/bandwhich -i utun
  ```

### 4. Raw Output Format
The tool uses `bandwhich -r -n`:
* `-r` / `--raw`: Machine-parseable line format (`process:`, `connection:`, `remote_address:`).
* `-n` / `--no-resolve`: Avoids DNS reverse lookup delays so scans execute in sub-second time.
