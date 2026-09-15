#!/usr/bin/env python3
"""
fleet_bandwidth.py - Parallel bandwhich monitor across homelab fleet.
Monitors KPC, FX505, Mac Server M1, MacBook Air M2, and Raspberry Pi.
"""

import sys
import time
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

HOSTS = [
    {
        "id": "kpc",
        "name": "KPC (Workstation)",
        "target": "local",
        "platform": "linux",
        "bin": "bandwhich",
    },
    {
        "id": "fx505",
        "name": "FX505 (Laptop)",
        "target": "fx505-ts",
        "platform": "linux",
        "bin": "bandwhich",
    },
    {
        "id": "m1",
        "name": "Mac Server (Apple M1)",
        "target": "m1",
        "platform": "macos",
        "bin": "/opt/homebrew/bin/bandwhich",
    },
    {
        "id": "m2",
        "name": "Macbook Air (Apple M2)",
        "target": "m2",
        "platform": "macos",
        "bin": "/opt/homebrew/bin/bandwhich",
    },
    {
        "id": "rpi",
        "name": "Raspberry Pi 4",
        "target": "rpi",
        "platform": "linux",
        "bin": "/usr/local/bin/bandwhich",
    },
]

def format_rate(bps):
    if bps >= 1024 * 1024:
        return f"{bps / (1024 * 1024):.2f} MB/s"
    elif bps >= 1024:
        return f"{bps / 1024:.1f} KB/s"
    else:
        return f"{bps} B/s"

def build_command(host, duration):
    if host["platform"] == "linux":
        return f"echo invincible | sudo -S timeout --signal=INT {duration} {host['bin']} -r -n 2>/dev/null"
    else:
        # macOS self-terminating wrapper running as root
        py_snippet = (
            f"import subprocess, time, signal; "
            f"p = subprocess.Popen(['{host['bin']}', '-r', '-n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True); "
            f"time.sleep({duration}); "
            f"p.send_signal(signal.SIGINT); "
            f"out, _ = p.communicate(); "
            f"print(out)"
        )
        return f"echo invincible | sudo -S python3 -c \"{py_snippet}\" 2>/dev/null"

def sample_host(host, duration=3):
    cmd_str = build_command(host, duration)
    try:
        if host["target"] == "local":
            res = subprocess.run(
                cmd_str,
                shell=True,
                capture_output=True,
                text=True,
                timeout=duration + 5
            )
            stdout = res.stdout
            status = "online"
        else:
            ssh_cmd = [
                "ssh",
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=3",
                host["target"],
                cmd_str
            ]
            res = subprocess.run(
                ssh_cmd,
                capture_output=True,
                text=True,
                timeout=duration + 5
            )
            stdout = res.stdout
            status = "online" if res.returncode in (0, 124) else "unreachable"
    except subprocess.TimeoutExpired:
        return {
            "host": host["name"],
            "id": host["id"],
            "target": host["target"],
            "status": "timed_out",
            "total_up": 0,
            "total_down": 0,
            "total_bps": 0,
            "processes": [],
            "remotes": [],
        }
    except Exception as e:
        return {
            "host": host["name"],
            "id": host["id"],
            "target": host["target"],
            "status": f"error: {str(e)}",
            "total_up": 0,
            "total_down": 0,
            "total_bps": 0,
            "processes": [],
            "remotes": [],
        }

    processes = {}
    remotes = {}
    
    frames = stdout.split("Refreshing:")
    for frame in frames:
        for line in frame.splitlines():
            line = line.strip()
            # Process match
            m_proc = re.match(r'process:\s+<[^>]+>\s+"([^"]+)"\s+up/down Bps:\s+(\d+)/(\d+)\s+connections:\s+(\d+)', line)
            if m_proc:
                pname = m_proc.group(1)
                up = int(m_proc.group(2))
                down = int(m_proc.group(3))
                conns = int(m_proc.group(4))
                if pname not in processes:
                    processes[pname] = {"up": 0, "down": 0, "conns": 0}
                if (up + down) >= (processes[pname]["up"] + processes[pname]["down"]):
                    processes[pname] = {"up": up, "down": down, "conns": conns}

            # Remote address match
            m_rem = re.match(r'remote_address:\s+<[^>]+>\s+(\S+)\s+up/down Bps:\s+(\d+)/(\d+)\s+connections:\s+(\d+)', line)
            if m_rem:
                raddr = m_rem.group(1)
                up = int(m_rem.group(2))
                down = int(m_rem.group(3))
                conns = int(m_rem.group(4))
                if raddr not in remotes:
                    remotes[raddr] = {"up": 0, "down": 0, "conns": 0}
                if (up + down) >= (remotes[raddr]["up"] + remotes[raddr]["down"]):
                    remotes[raddr] = {"up": up, "down": down, "conns": conns}

    total_up = sum(p["up"] for p in processes.values())
    total_down = sum(p["down"] for p in processes.values())

    sorted_procs = sorted(processes.items(), key=lambda x: x[1]["up"] + x[1]["down"], reverse=True)
    sorted_remotes = sorted(remotes.items(), key=lambda x: x[1]["up"] + x[1]["down"], reverse=True)

    return {
        "host": host["name"],
        "id": host["id"],
        "target": host["target"],
        "status": status,
        "total_up": total_up,
        "total_down": total_down,
        "total_bps": total_up + total_down,
        "processes": sorted_procs,
        "remotes": sorted_remotes,
    }

def run_fleet_monitor(duration=3):
    with ThreadPoolExecutor(max_workers=len(HOSTS)) as executor:
        results = list(executor.map(lambda h: sample_host(h, duration), HOSTS))
    results.sort(key=lambda r: r["total_bps"], reverse=True)
    return results

def generate_markdown_report(results):
    lines = []
    lines.append("# Live Fleet Bandwidth & Network Activity Report")
    lines.append("")
    lines.append(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    lines.append("**Measurement Engine:** `bandwhich -r -n` (parallel raw socket packet sniffing)")
    lines.append("")
    lines.append("## Fleet Bandwidth Utilization Summary")
    lines.append("")
    lines.append("| Rank | Device | Total Rate | Download (RX) | Upload (TX) | Top Active Process | Status |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for idx, r in enumerate(results, start=1):
        if r["status"] != "online":
            lines.append(f"| **#{idx}** | **{r['host']}** | — | — | — | — | `{r['status']}` |")
            continue

        top_proc = r["processes"][0][0] if r["processes"] else "Idle"
        top_rate = ""
        if r["processes"]:
            p_tot = r["processes"][0][1]["up"] + r["processes"][0][1]["down"]
            top_rate = f" ({format_rate(p_tot)})"
        
        tot_fmt = format_rate(r["total_bps"])
        down_fmt = format_rate(r["total_down"])
        up_fmt = format_rate(r["total_up"])
        
        lines.append(f"| **#{idx}** | **{r['host']}** | **{tot_fmt}** | {down_fmt} | {up_fmt} | `{top_proc}`{top_rate} | `online` |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Per-Device Activity Breakdown")
    lines.append("")

    for r in results:
        if r["status"] != "online":
            lines.append(f"### {r['host']} (`{r['status']}`)")
            lines.append(f"- **SSH Target:** `{r['target']}`")
            lines.append("")
            continue

        lines.append(f"### {r['host']}")
        lines.append(f"- **SSH Target:** `{r['target']}`")
        lines.append(f"- **Current Throughput:** Download: **{format_rate(r['total_down'])}** | Upload: **{format_rate(r['total_up'])}** (Total: **{format_rate(r['total_bps'])}**)")
        lines.append("")
        
        if r["processes"]:
            lines.append("#### Top Processes by Bandwidth")
            lines.append("| Process | Download Rate | Upload Rate | Total Rate | Connections |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for pname, pdata in r["processes"][:5]:
                p_tot = pdata["up"] + pdata["down"]
                lines.append(f"| `{pname}` | {format_rate(pdata['down'])} | {format_rate(pdata['up'])} | **{format_rate(p_tot)}** | {pdata['conns']} |")
            lines.append("")

        if r["remotes"]:
            lines.append("#### Top Remote IP Endpoints")
            lines.append("| Remote Address | Download Rate | Upload Rate | Active Connections |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for raddr, rdata in r["remotes"][:4]:
                lines.append(f"| `{raddr}` | {format_rate(rdata['down'])} | {format_rate(rdata['up'])} | {rdata['conns']} |")
            lines.append("")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    dur = 3
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        dur = int(sys.argv[1])
    results = run_fleet_monitor(duration=dur)
    report = generate_markdown_report(results)
    print(report)
