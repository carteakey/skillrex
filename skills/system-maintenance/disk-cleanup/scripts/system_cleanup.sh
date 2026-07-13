#!/bin/bash
# system_cleanup.sh - A script to safely clean up disk space on Linux

echo "Starting system cleanup..."

# 1. Empty Trash
echo "Emptying trash..."
rm -rf ~/.local/share/Trash/files/* ~/.local/share/Trash/info/* ~/.local/share/Trash/expunged/* 2>/dev/null

# 2. Clear App Caches
echo "Clearing app caches..."
rm -rf ~/.cache/camoufox/* ~/.cache/uv/* ~/.cache/mozilla/* ~/.cache/zen/* ~/.cache/ms-playwright/* 2>/dev/null

# 3. Flatpak Unused Runtimes (Requires sudo for system-wide, falling back to user)
echo "Removing unused user Flatpak runtimes..."
flatpak uninstall --unused --user -y

# Instructions for system-wide commands
echo "======================================================"
echo "Cleanup complete for user-level directories."
echo "To clean up system-wide packages, please run:"
echo "1. sudo flatpak uninstall --unused -y"
echo "2. sudo pacman -Sc"
echo "======================================================"
