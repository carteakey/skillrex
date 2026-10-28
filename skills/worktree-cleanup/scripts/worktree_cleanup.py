#!/usr/bin/env python3
"""
worktree_cleanup.py - Git Worktree Audit, Prune, and Safe Removal Tool

Scans repositories (in /Users/kchauhan/repos, ~/.codex/worktrees, etc.) to:
- Audit all linked git worktrees across multiple repositories.
- Identify ghost/prunable worktrees whose filesystem directories no longer exist.
- Check merged status against default branches (main/master).
- Check remote synchronization status with origin.
- Safely prune stale metadata and remove clean, merged, or pushed worktrees.
- Protect uncommitted changes, scratch files, and detached experiments.
"""

import os
import sys
import argparse
import subprocess
import json
import shutil

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def run_git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)

def find_primary_repos(root_dir):
    repos = []
    if not os.path.exists(root_dir):
        return repos
    for entry in os.scandir(root_dir):
        if entry.is_dir():
            git_path = os.path.join(entry.path, ".git")
            # Only genuine repository roots have a .git directory, not a .git file (which worktrees use)
            if os.path.isdir(git_path):
                repos.append(entry.path)
    repos.sort()
    return repos

def get_default_branch(repo_path):
    res = run_git(["rev-parse", "--verify", "main"], repo_path)
    if res.returncode == 0:
        return "main"
    res = run_git(["rev-parse", "--verify", "master"], repo_path)
    if res.returncode == 0:
        return "master"
    return "main"

def inspect_worktrees(repo_path):
    raw = run_git(["worktree", "list", "--porcelain"], repo_path)
    if raw.returncode != 0:
        return []
    
    lines = raw.stdout.strip().splitlines()
    worktrees = []
    cur = {}
    for line in lines:
        if not line:
            if cur:
                worktrees.append(cur)
                cur = {}
        elif line.startswith("worktree "):
            cur["path"] = line[9:]
        elif line.startswith("HEAD "):
            cur["head"] = line[5:]
        elif line.startswith("branch "):
            cur["branch"] = line[7:]
        elif line == "detached":
            cur["detached"] = True
        elif line == "prunable":
            cur["prunable"] = True
    if cur:
        worktrees.append(cur)
        
    return worktrees

def audit_repo_worktrees(repo_path):
    wts = inspect_worktrees(repo_path)
    if not wts:
        return []

    default_branch = get_default_branch(repo_path)
    records = []

    for wt in wts:
        path = wt["path"]
        is_main = (os.path.realpath(path) == os.path.realpath(repo_path))
        head = wt.get("head", "")
        branch_ref = wt.get("branch", "")
        branch_name = branch_ref.replace("refs/heads/", "") if branch_ref else "detached"
        exists = os.path.exists(path)
        prunable = wt.get("prunable", False) or not exists

        dirty_files = 0
        untracked_files = 0
        size_bytes = 0

        if exists:
            # Check dirty
            st = run_git(["status", "--porcelain"], path)
            if st.returncode == 0 and st.stdout.strip():
                for sl in st.stdout.strip().splitlines():
                    if sl.startswith("??"):
                        untracked_files += 1
                    else:
                        dirty_files += 1
            # Fast size check via du
            try:
                du_res = subprocess.run(["du", "-sk", path], capture_output=True, text=True)
                if du_res.returncode == 0:
                    kb = int(du_res.stdout.split()[0])
                    size_bytes = kb * 1024
            except:
                pass

        # Check merged to default branch
        merged_to_default = False
        if head:
            mb = run_git(["merge-base", "--is-ancestor", head, default_branch], repo_path)
            merged_to_default = (mb.returncode == 0)

        # Check remote status
        pushed_to_remote = False
        remote_info = "no remote"
        if branch_name and branch_name != "detached":
            rem_chk = run_git(["rev-parse", "--verify", f"origin/{branch_name}"], repo_path)
            if rem_chk.returncode == 0:
                ab = run_git(["rev-list", "--left-right", "--count", f"{branch_name}...origin/{branch_name}"], repo_path)
                if ab.returncode == 0:
                    ahead, behind = ab.stdout.strip().split()
                    pushed_to_remote = (ahead == "0")
                    remote_info = f"origin/{branch_name} (ahead: {ahead}, behind: {behind})"
            else:
                remote_info = "local only"

        # Classification
        if is_main:
            classification = "main_repository"
        elif prunable:
            classification = "prunable_ghost"
        elif dirty_files > 0 or untracked_files > 0:
            classification = "has_uncommitted_work"
        elif merged_to_default:
            classification = "merged_clean"
        elif pushed_to_remote:
            classification = "pushed_clean"
        else:
            classification = "unmerged_clean"

        records.append({
            "repo_path": repo_path,
            "repo_name": os.path.basename(repo_path),
            "worktree_path": path,
            "is_main": is_main,
            "branch": branch_name,
            "head": head[:7] if head else "",
            "exists": exists,
            "prunable": prunable,
            "merged_to_default": merged_to_default,
            "default_branch": default_branch,
            "pushed_to_remote": pushed_to_remote,
            "remote_info": remote_info,
            "dirty_files": dirty_files,
            "untracked_files": untracked_files,
            "size_bytes": size_bytes,
            "classification": classification
        })

    return records

def format_size(bytes_num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} TB"

def cmd_audit(args):
    repos = find_primary_repos(args.dir)
    all_records = []
    
    for repo in repos:
        recs = audit_repo_worktrees(repo)
        all_records.extend(recs)

    if args.json:
        print(json.dumps(all_records, indent=2))
        return

    # Filter to secondary worktrees
    secondary = [r for r in all_records if not r["is_main"]]

    if not secondary:
        print(f"{Colors.GREEN}✓ No secondary worktrees found across {len(repos)} repositories.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}Auditing worktrees across {len(repos)} repos in {args.dir}:{Colors.RESET}\n")

    by_repo = {}
    for r in secondary:
        by_repo.setdefault(r["repo_name"], []).append(r)

    for repo_name, records in by_repo.items():
        print(f"{Colors.CYAN}{Colors.BOLD}▶ Repo: {repo_name}{Colors.RESET}")
        for r in records:
            cls = r["classification"]
            if cls == "prunable_ghost":
                status_color = Colors.YELLOW
                status_label = "[PRUNABLE - DIR MISSING]"
            elif cls == "has_uncommitted_work":
                status_color = Colors.RED
                status_label = f"[UNCOMMITTED WORK: {r['dirty_files']} modified, {r['untracked_files']} untracked]"
            elif cls == "merged_clean":
                status_color = Colors.GREEN
                status_label = f"[MERGED to {r['default_branch']} - SAFE TO REMOVE]"
            elif cls == "pushed_clean":
                status_color = Colors.BLUE
                status_label = "[PUSHED TO REMOTE - SAFE TO REMOVE]"
            else:
                status_color = Colors.YELLOW
                status_label = "[UNMERGED LOCAL COMMITS]"

            size_label = format_size(r["size_bytes"]) if r["exists"] else "0 B"
            print(f"  • {r['worktree_path']}")
            print(f"    Branch: {r['branch']} ({r['head']}) | Size: {size_label}")
            print(f"    Status: {status_color}{status_label}{Colors.RESET} ({r['remote_info']})")
        print()

def cmd_prune(args):
    repos = find_primary_repos(args.dir)
    pruned_count = 0
    for repo in repos:
        res = run_git(["worktree", "prune", "-v"], repo)
        if res.returncode == 0 and res.stdout.strip():
            print(f"{Colors.CYAN}[{os.path.basename(repo)}]{Colors.RESET}")
            for l in res.stdout.strip().splitlines():
                print(f"  {Colors.YELLOW}Pruned:{Colors.RESET} {l}")
                pruned_count += 1
    if pruned_count == 0:
        print(f"{Colors.GREEN}✓ No stale worktree metadata needed pruning.{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}✓ Successfully pruned {pruned_count} stale worktree records.{Colors.RESET}")

def cmd_clean(args):
    repos = find_primary_repos(args.dir)
    all_records = []
    for repo in repos:
        all_records.extend(audit_repo_worktrees(repo))

    secondary = [r for r in all_records if not r["is_main"]]
    if not secondary:
        print(f"{Colors.GREEN}✓ No secondary worktrees to clean up.{Colors.RESET}")
        return

    # First prune ghosts
    cmd_prune(args)

    # Next filter candidates for removal
    candidates = []
    preserved = []

    for r in secondary:
        if not r["exists"]:
            continue
        
        # Rule: Never remove worktrees with uncommitted work unless --force is given
        if (r["dirty_files"] > 0 or r["untracked_files"] > 0) and not args.force:
            preserved.append((r, "Contains uncommitted changes or scratch files"))
            continue

        # Safe conditions: Merged to default branch OR pushed to remote
        if r["merged_to_default"] or r["pushed_to_remote"] or args.force:
            candidates.append(r)
        else:
            preserved.append((r, "Branch has local unmerged commits not pushed to origin"))

    if preserved:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Preserving worktrees with uncommitted work or unpushed commits:{Colors.RESET}")
        for r, reason in preserved:
            print(f"  - {Colors.BOLD}{r['worktree_path']}{Colors.RESET} ({reason})")

    if not candidates:
        print(f"\n{Colors.GREEN}No safe-to-remove worktrees found.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}Candidates for removal ({len(candidates)}):{Colors.RESET}")
    total_bytes = 0
    for r in candidates:
        total_bytes += r["size_bytes"]
        reason = "Merged to " + r["default_branch"] if r["merged_to_default"] else "Pushed to remote"
        print(f"  • {r['worktree_path']} ({format_size(r['size_bytes'])}) - {reason}")

    print(f"\nTotal disk space to reclaim: {Colors.GREEN}{Colors.BOLD}{format_size(total_bytes)}{Colors.RESET}")

    if args.dry_run:
        print(f"\n{Colors.CYAN}[Dry Run] No worktrees were deleted. Pass without --dry-run to remove.{Colors.RESET}")
        return

    # Execute removal
    removed_count = 0
    for r in candidates:
        cmd = ["worktree", "remove", r["worktree_path"]]
        if args.force:
            cmd.append("--force")
        res = run_git(cmd, r["repo_path"])
        if res.returncode == 0:
            print(f"{Colors.GREEN}✓ Removed:{Colors.RESET} {r['worktree_path']}")
            removed_count += 1
            # Check if parent dir is now empty (e.g. .worktrees or uuid folder)
            parent = os.path.dirname(r["worktree_path"])
            try:
                if os.path.exists(parent) and not os.listdir(parent):
                    os.rmdir(parent)
            except:
                pass
        else:
            print(f"{Colors.RED}✗ Failed to remove {r['worktree_path']}: {res.stderr.strip()}{Colors.RESET}")

    print(f"\n{Colors.GREEN}{Colors.BOLD}Successfully cleaned up {removed_count} worktrees.{Colors.RESET}")

def main():
    parser = argparse.ArgumentParser(description="Git Worktree Audit, Prune, and Safe Removal Tool")
    parser.add_argument("--dir", default="/Users/kchauhan/repos", help="Target workspace root directory (default: /Users/kchauhan/repos)")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Audit
    audit_parser = subparsers.add_parser("audit", help="Audit worktrees across repositories")
    audit_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    
    # Prune
    prune_parser = subparsers.add_parser("prune", help="Prune stale worktree metadata records")
    
    # Clean
    clean_parser = subparsers.add_parser("clean", help="Safely clean up merged and pushed worktrees")
    clean_parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without executing")
    clean_parser.add_argument("--force", action="store_true", help="Force removal even if uncommitted changes exist")

    args = parser.parse_args()

    if not args.command or args.command == "audit":
        cmd_audit(args)
    elif args.command == "prune":
        cmd_prune(args)
    elif args.command == "clean":
        cmd_clean(args)

if __name__ == "__main__":
    main()
