#!/usr/bin/env python3
"""
repo_sync.py - Multi-Repository Git Synchronization and Audit Utility

Scans a directory of Git repositories (e.g., /Users/kchauhan/repos) to:
- Audit uncommitted changes (tracked vs untracked).
- Detect unpushed branches / ahead commits.
- Detect incoming commits / behind branches.
- Safely push local branches to remote with upstream tracking.
- Safely fast-forward pull branches when clean.
"""

import os
import sys
import argparse
import subprocess
import json

def find_git_repos(root_dir):
    repos = []
    for root, dirs, files in os.walk(root_dir):
        if ".git" in dirs:
            dirs.remove(".git")
            repos.append(root)
            dirs.clear()
    repos.sort()
    return repos

def run_git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)

def audit_repo(repo_path, root_dir, fetch=False):
    rel_path = os.path.relpath(repo_path, root_dir)
    
    # Check remotes
    remotes_res = run_git(["remote"], repo_path)
    remotes = [r.strip() for r in remotes_res.stdout.splitlines() if r.strip()]
    has_origin = "origin" in remotes

    if fetch and has_origin:
        run_git(["fetch", "origin", "--prune"], repo_path)

    # Current branch
    branch_res = run_git(["branch", "--show-current"], repo_path)
    current_branch = branch_res.stdout.strip()
    if not current_branch:
        head_res = run_git(["rev-parse", "--short", "HEAD"], repo_path)
        current_branch = f"HEAD ({head_res.stdout.strip()})"

    # Uncommitted changes
    st_res = run_git(["status", "--porcelain"], repo_path)
    status_lines = [l for l in st_res.stdout.splitlines() if l.strip()]
    staged = [l for l in status_lines if l[0] in "MADRC"]
    unstaged = [l for l in status_lines if l[1] in "MD"]
    untracked = [l for l in status_lines if l.startswith("??")]

    # Local branches analysis
    branches_res = run_git(["for-each-ref", "--format=%(refname:short)|%(upstream:short)", "refs/heads"], repo_path)
    
    unpushed_branches = []
    pullable_branches = []
    unrelated_branches = []
    missing_remote = len(remotes) == 0

    if missing_remote:
        commits_cnt = run_git(["rev-list", "--count", "HEAD"], repo_path).stdout.strip() or "0"
        unpushed_branches.append(f"local only ({commits_cnt} commits, no remote configured)")
    else:
        for line in branches_res.stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split("|")
            b_name = parts[0]
            upstream = parts[1] if len(parts) > 1 else ""

            if upstream:
                ahead_p = run_git(["rev-list", f"{upstream}..{b_name}", "--count"], repo_path)
                behind_p = run_git(["rev-list", f"{b_name}..{upstream}", "--count"], repo_path)
                if ahead_p.returncode == 0 and behind_p.returncode == 0:
                    ahead = int(ahead_p.stdout.strip() or 0)
                    behind = int(behind_p.stdout.strip() or 0)
                    if ahead > 0:
                        unpushed_branches.append(f"{b_name} (+{ahead} ahead of {upstream})")
                    if behind > 0:
                        pullable_branches.append(f"{b_name} (-{behind} behind {upstream})")
                else:
                    unrelated_branches.append(f"{b_name} vs {upstream}")
            else:
                # No upstream: check if origin/<b_name> exists
                ref_res = run_git(["rev-parse", "--verify", f"origin/{b_name}"], repo_path)
                remote_exists = (ref_res.returncode == 0)

                if not remote_exists:
                    unpushed_branches.append(f"{b_name} (new branch, not on remote)")
                else:
                    ahead_p = run_git(["rev-list", f"origin/{b_name}..{b_name}", "--count"], repo_path)
                    behind_p = run_git(["rev-list", f"{b_name}..origin/{b_name}", "--count"], repo_path)

                    if ahead_p.returncode != 0 or behind_p.returncode != 0:
                        unrelated_branches.append(b_name)
                    else:
                        ahead = int(ahead_p.stdout.strip() or 0)
                        behind = int(behind_p.stdout.strip() or 0)
                        if ahead > 0:
                            unpushed_branches.append(f"{b_name} (+{ahead} ahead of origin/{b_name})")
                        if behind > 0:
                            pullable_branches.append(f"{b_name} (-{behind} behind origin/{b_name})")

    return {
        "repo": rel_path,
        "path": repo_path,
        "current_branch": current_branch,
        "uncommitted_count": len(status_lines),
        "staged_count": len(staged),
        "unstaged_count": len(unstaged),
        "untracked_count": len(untracked),
        "unpushed_branches": unpushed_branches,
        "pullable_branches": pullable_branches,
        "unrelated_branches": unrelated_branches,
        "has_remote": len(remotes) > 0,
        "is_clean": len(status_lines) == 0 and len(unpushed_branches) == 0 and len(pullable_branches) == 0
    }

def cmd_audit(args):
    repos = find_git_repos(args.dir)
    print(f"Auditing {len(repos)} repositories in {args.dir} (fetch={args.fetch})...\n")
    results = []
    clean_count = 0

    for r in repos:
        info = audit_repo(r, args.dir, fetch=args.fetch)
        results.append(info)
        if info["is_clean"]:
            clean_count += 1
        else:
            print(f"[{info['repo']}] (branch: {info['current_branch']})")
            if info["uncommitted_count"] > 0:
                print(f"  - Uncommitted: {info['uncommitted_count']} files ({info['staged_count']} staged, {info['unstaged_count']} modified, {info['untracked_count']} untracked)")
            if info["unpushed_branches"]:
                print(f"  - Unpushed: {', '.join(info['unpushed_branches'])}")
            if info["pullable_branches"]:
                print(f"  - Pullable: {', '.join(info['pullable_branches'])}")
            if info["unrelated_branches"]:
                print(f"  - Unrelated Histories: {', '.join(info['unrelated_branches'])}")
            if not info["has_remote"]:
                print(f"  - WARNING: No remote configured")
            print()

    print(f"Summary: {clean_count}/{len(repos)} clean repositories.")

def cmd_push(args):
    repos = find_git_repos(args.dir)
    print(f"Scanning {len(repos)} repositories for unpushed branches...\n")

    pushed_total = 0
    for r in repos:
        info = audit_repo(r, args.dir, fetch=False)
        if not info["has_remote"]:
            continue

        branches_res = run_git(["for-each-ref", "--format=%(refname:short)|%(upstream:short)", "refs/heads"], r)
        for line in branches_res.stdout.splitlines():
            if not line.strip():
                continue
            b_name = line.split("|")[0]
            ref_res = run_git(["rev-parse", "--verify", f"origin/{b_name}"], r)
            needs_push = False

            if ref_res.returncode != 0:
                needs_push = True
            else:
                ahead_p = run_git(["rev-list", f"origin/{b_name}..{b_name}", "--count"], r)
                if ahead_p.returncode == 0 and int(ahead_p.stdout.strip() or 0) > 0:
                    needs_push = True

            if needs_push:
                print(f"[{info['repo']}] Pushing branch '{b_name}' with upstream tracking...")
                p = run_git(["push", "-u", "origin", b_name], r)
                if p.returncode == 0:
                    print(f"  ✓ Successfully pushed '{b_name}'")
                    pushed_total += 1
                else:
                    print(f"  ✗ Failed to push '{b_name}': {p.stderr.strip()}")

    print(f"\nCompleted push. {pushed_total} branch(es) pushed.")

def cmd_pull(args):
    repos = find_git_repos(args.dir)
    print(f"Fetching and pulling branches across {len(repos)} repositories...\n")

    pulled_total = 0
    for r in repos:
        info = audit_repo(r, args.dir, fetch=True)
        if not info["has_remote"]:
            continue

        for pb in info["pullable_branches"]:
            b_name = pb.split()[0]
            # If it's the currently checked-out branch, pull only if working tree is clean
            if b_name == info["current_branch"]:
                if info["uncommitted_count"] == 0:
                    p = run_git(["pull", "--ff-only"], r)
                    if p.returncode == 0:
                        print(f"[{info['repo']}] ✓ Pulled active branch '{b_name}'")
                        pulled_total += 1
                    else:
                        print(f"[{info['repo']}] ✗ Fast-forward pull failed on '{b_name}': {p.stderr.strip()}")
                else:
                    print(f"[{info['repo']}] ⚠ Skipped active branch '{b_name}' because working tree has uncommitted changes.")
            else:
                # Non-active branch: check if it's strictly behind and can be safely fast-forwarded via ref update
                anc = run_git(["merge-base", "--is-ancestor", b_name, f"origin/{b_name}"], r)
                if anc.returncode == 0:
                    ff = run_git(["branch", "-f", b_name, f"origin/{b_name}"], r)
                    if ff.returncode == 0:
                        print(f"[{info['repo']}] ✓ Fast-forwarded local branch '{b_name}' to origin/{b_name}")
                        pulled_total += 1
                    else:
                        print(f"[{info['repo']}] ✗ Failed to fast-forward '{b_name}': {ff.stderr.strip()}")

    print(f"\nCompleted pull. {pulled_total} branch(es) updated.")

def cmd_sync(args):
    print("=== STEP 1: Fetch and Pull ===")
    cmd_pull(args)
    print("\n=== STEP 2: Push Local Branches ===")
    cmd_push(args)

def main():
    parser = argparse.ArgumentParser(description="Multi-Repository Git Synchronization Utility")
    parser.add_argument("--dir", default="/Users/kchauhan/repos", help="Target repositories directory")
    
    subparsers = parser.add_subparsers(dest="command")
    
    audit_parser = subparsers.add_parser("audit", help="Audit all repositories")
    audit_parser.add_argument("--fetch", action="store_true", help="Fetch remotes before auditing")
    
    subparsers.add_parser("push", help="Push unpushed/new local branches with upstream tracking")
    subparsers.add_parser("pull", help="Fast-forward branches that are behind remote")
    subparsers.add_parser("sync", help="Run pull then push across all repositories")
    
    args = parser.parse_args()
    if not args.command or args.command == "audit":
        cmd_audit(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "sync":
        cmd_sync(args)

if __name__ == "__main__":
    main()
