---
name: system-performance
description: Performs system load, memory, swap, and thermal diagnostics on macOS and Linux hosts, identifies resource hogs (including ANECompilerService/CoreML loops), and outputs a formatted markdown performance report. Trigger this skill whenever the user asks about system slowness, diagnostic reports, or system monitoring.
---

# System Performance Diagnostic Skill

Use this skill to diagnose and troubleshoot system sluggishness, high CPU load, memory pressure, and thermal throttling across the local machine and all reachable remote hosts (e.g., `kpc`, `pi`, `fx505`, `m1`) defined in SSH configurations.

## 📋 Step-by-Step Diagnostic Protocol

### Step 1: Discover Target Hosts
1. Check the local host operating system.
2. Read `~/.ssh/config` and `~/.ssh/config.local` to parse available host aliases (such as `kpc`, `pi`, `fx505`, `m1`, etc.).
3. Test SSH connectivity to each host.
   * **Note:** For systems experiencing severe swap pressure (thrashing), the SSH daemon may be slow to fork. Increase connection timeout to `-o ConnectTimeout=15` (instead of 3) to prevent banner exchange timeouts. Avoid disk-heavy commands (e.g. `find ~`) on thrashing hosts to prevent exacerbating OOM loops.

---

### Step 2: Run Diagnostic Commands
For the local machine and each reachable remote host, execute the appropriate commands based on its operating system:

#### For macOS:
* **System Diagnostics:**
  ```bash
  sysctl hw.ncpu && uptime && pmset -g sysload && pmset -g therm && echo "--- Memory Swap ---" && sysctl vm.swapusage
  ```
* **Top CPU Processes (sorted by CPU):**
  ```bash
  ps -Ao pid,%cpu,%mem,comm -r | head -n 11
  ```
* **Top Memory Processes (sorted by memory):**
  ```bash
  ps -Ao pid,%cpu,%mem,comm -m | head -n 11
  ```
* **Apple Neural Engine / `ANECompilerService` Diagnostics (if high CPU / ML compilation detected):**
  * Check if `ANECompilerService` is active and check accumulated CPU time:
    ```bash
    ps aux | grep -i ANECompilerService | grep -v grep
    ```
  * Trace the underlying XPC caller daemon (`aned`) and client app via system log:
    ```bash
    /usr/bin/log show --last 15m --style syslog | grep -i ANECompilerService
    ```
  * *Note:* `ANECompilerService` is a root-owned XPC daemon. Terminating stuck compilations over SSH requires pseudo-tty sudo:
    ```bash
    ssh -t <host> "sudo kill -9 <PID>"
    ```

#### For Linux / Raspberry Pi:
* **System Diagnostics:**
  ```bash
  nproc && uptime && echo "--- Memory Usage ---" && free -h && echo "--- Swap Usage ---" && cat /proc/swaps
  ```
* **Top CPU Processes (sorted by CPU):**
  ```bash
  ps -Ao pid,%cpu,%mem,comm --sort=-%cpu | head -n 11
  ```
* **Top Memory Processes (sorted by memory):**
  ```bash
  ps -Ao pid,%cpu,%mem,comm --sort=-%mem | head -n 11
  ```

#### For Docker / OrbStack Hosts (Container Swap Usage):
If a host runs Docker/OrbStack, host-level swap stats can be inflated by guest VM caching. You can extract individual container swap allocations using cgroups v2 inside the VM:
1. Run a temporary container to extract raw swap bytes per container ID:
   ```bash
   docker run --rm -v /sys/fs/cgroup:/cgroup:ro alpine sh -c 'for d in /cgroup/docker/*; do if [ -d "$d" ]; then echo "$(basename $d) $(cat $d/memory.swap.current 2>/dev/null || echo 0)"; fi; done'
   ```
2. Correlate container IDs with human-readable names:
   ```bash
   docker ps -a --no-trunc --format '{{.ID}} {{.Names}}'
   ```

---

### Step 3: Triage the Metrics
Compare the collected metrics for each host against the following thresholds:

1. **Load Average:** Compare the 1-minute load average to the number of CPU cores. Alerts are triggered if load exceeds the physical core count.
2. **Thermal Throttling (macOS only):** Check if `thermal level = Bad` or `combined level = Bad`.
3. **Memory & Swap Pressure:** Check if active swap usage exceeds 1 GB (or 50% capacity).
4. **Resource Hogs:** Identify the top CPU-consuming and memory-consuming processes.
5. **Stuck Neural Engine Compilation (`ANECompilerService`):** Check if `ANECompilerService` has accumulated excessive CPU time (e.g. >30 minutes at ~100% CPU) due to orphan model compilation tasks from exited client apps.

---

### Step 4: Write and Update the Report Artifact
Always create or update a structured markdown file named `system_performance_report.md` in the current conversation directory:
`<appDataDir>/brain/<conversation-id>/system_performance_report.md`

#### Report Structure:
1. **Title:** `# Multi-Host System Performance Report`
2. **Comparison Table:** A master summary table comparing all hosts: Hostname, CPU Cores, Load Average, Thermal Status, Swap Status, and Reachability.
3. **Host Deep Dives:** For each reachable machine, present its top CPU/Memory processes, container-level swap breakdowns (if applicable), and any active alerts.
4. **Actionable Recommendations:** Provide a consolidated, numbered list of fixes organized by host (e.g., stopping specific containers/apps, restarting services, or physical cooling).

---

### Step 5: Report to the User
* Provide a brief, high-level summary of the overall status (which hosts are healthy, and which ones have issues).
* Provide a clickable link to the generated report: `[system_performance_report.md](file:///absolute/path/to/report)`.
* Offer to perform mitigations on any of the remote or local hosts (e.g., stopping services, restarting VMs, or rebooting).
