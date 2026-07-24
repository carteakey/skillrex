#!/usr/bin/env bash

# Exit on error
set -eo pipefail

echo "============================================="
echo "   OpenAI Codex SSD Wear Impact Analyzer     "
echo "============================================="

# 1. Check Codex Installation & Version
echo -n "Checking Codex CLI installation: "
if command -v codex >/dev/null 2>&1; then
    CODEX_VER=$(codex --version 2>&1)
    echo "Found ($CODEX_VER)"
else
    echo "Not found in PATH"
fi

# 2. Check Database Files
CODEX_DIR="$HOME/.codex"
if [ -d "$CODEX_DIR" ]; then
    echo -e "\nCodex configuration directory exists at: $CODEX_DIR"
    echo "Checking log database files:"
    
    # List files with sizes
    found_logs=0
    for f in "$CODEX_DIR"/logs_2.sqlite*; do
        if [ -e "$f" ]; then
            filename=$(basename "$f")
            size=$(du -sh "$f" | cut -f1)
            echo "  - $filename: $size"
            found_logs=1
        fi
    done
    
    if [ "$found_logs" -eq 0 ]; then
        echo "  No log files (logs_2.sqlite*) found."
    fi
else
    echo -e "\nNo ~/.codex directory found. Codex has likely not been run on this user account."
fi

# 3. OS and Disk Wear Analysis
OS_TYPE=$(uname -s)
echo -e "\nDetected OS: $OS_TYPE"

case "$OS_TYPE" in
    Linux)
        # Find root block device
        root_dev=$(df / | tail -1 | awk '{print $1}')
        echo "Root filesystem device: $root_dev"
        
        # Resolve to physical disk
        if [[ "$root_dev" =~ ^/dev/nvme[0-9]+n[0-9]+p[0-9]+ ]]; then
            disk_name=$(echo "$root_dev" | grep -oE '/dev/nvme[0-9]+n[0-9]+')
            echo "Physical Disk Type: NVMe SSD ($disk_name)"
            echo -e "\nTo check your NVMe SSD lifetime writes and health, run:"
            echo "  sudo smartctl -A $disk_name"
        elif [[ "$root_dev" =~ ^/dev/sd[a-z][0-9]+ ]]; then
            disk_name=$(echo "$root_dev" | grep -oE '/dev/sd[a-z]')
            
            # Check if rotational
            base_name=$(basename "$disk_name")
            if [ -f "/sys/block/$base_name/queue/rotational" ]; then
                rotational=$(cat "/sys/block/$base_name/queue/rotational")
                if [ "$rotational" -eq 0 ]; then
                    echo "Physical Disk Type: SATA SSD ($disk_name)"
                    echo -e "\nTo check your SATA SSD lifetime writes, run:"
                    echo "  sudo smartctl -A $disk_name | grep -i Total_LBAs_Written"
                else
                    echo "Physical Disk Type: Rotational HDD ($disk_name)"
                    echo "Note: Rotational hard drives are not subject to SSD-style write endurance wear-out."
                fi
            else
                echo "Physical Disk Type: SATA Device ($disk_name)"
            fi
        else
            echo "Unable to automatically resolve physical disk type for $root_dev."
            echo "You can check available disks with 'lsblk' and run 'sudo smartctl -A /dev/<disk>'"
        fi
        ;;
        
    Darwin) # macOS
        echo "System: macOS (Apple Silicon or Intel)"
        echo -e "\nTo check your SSD write wear on macOS, install smartmontools via Homebrew:"
        echo "  brew install smartmontools"
        echo "  sudo smartctl -A /dev/disk0"
        echo -e "\n*Important Note:* macOS /tmp and \$TMPDIR sit on the on-disk APFS volume."
        echo "Do NOT use the symlink-to-tmp stopgap on macOS as it will not spare your SSD."
        echo "Update Codex instead."
        ;;
        
    *)
        echo "For Windows: Open CrystalDiskInfo to view 'Total Host Writes' or 'Total NVMe Host Writes'."
        ;;
esac

echo "============================================="
