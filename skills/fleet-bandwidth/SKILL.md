---
name: fleet-bandwidth
description: Monitor real-time network activity, per-process bandwidth utilization, and socket connections across all homelab fleet devices (KPC, FX505, Mac Server M1, MacBook Air M2, and Raspberry Pi) using bandwhich. Use this skill when the user asks to check network activity, diagnose high bandwidth usage, inspect network traffic across machines, or generate a fleet bandwidth report.
---

# Fleet Bandwidth & Network Activity Monitor

Provides automated parallel execution of `bandwhich` across all nodes in the homelab fleet, aggregating real-time per-process network throughput, active sockets, and remote endpoint traffic into a unified report.

## Fleet Devices Covered
* **KPC:** CachyOS desktop workstation (`local` / `100.110.126.24`)
* **FX505:** CachyOS laptop media server / HTPC (`fx505-ts` / `100.81.22.64`)
* **Mac Server (M1):** Apple Silicon M1 Docker host (`m1` / `100.89.197.43` / `192.168.0.56`)
* **Macbook Air (M2):** Apple Silicon M2 developer control plane (`m2` / `100.109.129.110`)
* **Raspberry Pi 4:** Debian Bookworm arm64 network/DNS anchor (`rpi` / `100.81.82.24` / `192.168.0.85`)

Detailed host parameters and IP definitions are maintained in [hosts.json](./references/hosts.json).

## Quick Execution

Execute the standalone CLI command on the workstation:
```bash
fleet-bandwidth [duration_seconds]
```

Or run the script via Python:
```bash
python3 ~/.agents/skills/fleet-bandwidth/scripts/fleet_bandwidth.py [duration_seconds]
```
*(Default sampling duration is 3 seconds).*

## Workflow for the Agent

When activated by a user request to monitor bandwidth or network traffic:
1. **Run the Collector:** Execute `fleet-bandwidth 3` (or call `scripts/fleet_bandwidth.py`).
2. **Review the Summary:** Parse the generated markdown table to identify:
   - The highest-consuming node in the fleet.
   - The top active processes (e.g. downloads, LLM streaming, Plex/Jellyfin streams).
   - Any nodes that timed out or are sleeping.
3. **Deep Dive (if requested):** If a specific host is hogging bandwidth, inspect its active connections or launch targeted monitoring for that node.
4. **Consult Operational Guide:** For permission issues, sleeping laptops, or Tailscale interface isolation, see [Troubleshooting Reference](./references/troubleshooting.md).

## Single Host Diagnostics

To inspect a single device interactively:
```bash
# Workstation (local)
sudo bandwhich

# Remote hosts
ssh m1 "sudo /opt/homebrew/bin/bandwhich"
ssh m2 "sudo /opt/homebrew/bin/bandwhich"
ssh fx505-ts "sudo bandwhich"
ssh rpi "sudo bandwhich"
```
