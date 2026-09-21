#!/usr/bin/env python3
"""
wiki_sync.py - Multi-Vault / Wiki Git Synchronization Utility

Manages Git synchronization, automated backup commits, and health audits
across knowledge bases, Obsidian vaults, and Quartz documentation wikis
in /Users/kchauhan/wikis (or custom directory).
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

DEFAULT_WIKIS_DIR = "/Users/kchauhan/wikis"

def find_wiki_repos(root_dir):
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

def audit_vault(repo_path, root_dir, fetch=False):
    rel_path = os.path.relpath(repo_path, root_dir)
    remotes_res = run_git(["remote"], repo_path)
    remotes = [r.strip() for r in remotes_res.stdout.splitlines() if r.strip()]
    has_origin = "origin" in remotes

    if fetch and has_origin:
        run_git(["fetch", "origin", "--prune"], repo_path)

    branch_res = run_git(["branch", "--show-current"], repo_path)
    current_branch = branch_res.stdout.strip()
    if not current_branch:
        head_res = run_git(["rev-parse", "--short", "HEAD"], repo_path)
        current_branch = f"HEAD ({head_res.stdout.strip()})"

    st_res = run_git(["status", "--porcelain"], repo_path)
    status_lines = [l for l in st_res.stdout.splitlines() if l.strip()]
    
    # Filter out or report .DS_Store
    non_ds_store = [l for l in status_lines if ".DS_Store" not in l]
    has_ds_store = any(".DS_Store" in l for l in status_lines)

    staged = [l for l in non_ds_store if l[0] in "MADRC"]
    unstaged = [l for l in non_ds_store if l[1] in "MD"]
    untracked = [l for l in non_ds_store if l.startswith("??")]

    unpushed_branches = []
    pullable_branches = []

    if not remotes:
        unpushed_branches.append("No remote configured")
    else:
        branches_res = run_git(["for-each-ref", "--format=%(refname:short)|%(upstream:short)", "refs/heads"], repo_path)
        for line in branches_res.stdout.splitlines():
            if not line.strip():
                continue
            b_name, upstream = line.split("|")[0], (line.split("|")[1] if "|" in line else "")
            target_upstream = upstream if upstream else f"origin/{b_name}"

            ref_res = run_git(["rev-parse", "--verify", target_upstream], repo_path)
            if ref_res.returncode == 0:
                ahead_p = run_git(["rev-list", f"{target_upstream}..{b_name}", "--count"], repo_path)
                behind_p = run_git(["rev-list", f"{b_name}..{target_upstream}", "--count"], repo_path)
                if ahead_p.returncode == 0 and behind_p.returncode == 0:
                    ahead = int(ahead_p.stdout.strip() or 0)
                    behind = int(behind_p.stdout.strip() or 0)
                    if ahead > 0:
                        unpushed_branches.append(f"{b_name} (+{ahead} ahead of {target_upstream})")
                    if behind > 0:
                        pullable_branches.append(f"{b_name} (-{behind} behind {target_upstream})")
            else:
                unpushed_branches.append(f"{b_name} (not published to remote)")

    return {
        "repo": rel_path,
        "path": repo_path,
        "current_branch": current_branch,
        "uncommitted_count": len(non_ds_store),
        "has_ds_store": has_ds_store,
        "staged_count": len(staged),
        "unstaged_count": len(unstaged),
        "untracked_count": len(untracked),
        "unpushed_branches": unpushed_branches,
        "pullable_branches": pullable_branches,
        "has_remote": len(remotes) > 0,
        "is_clean": len(non_ds_store) == 0 and len(unpushed_branches) == 0 and len(pullable_branches) == 0
    }

def cmd_audit(args):
    repos = find_wiki_repos(args.dir)
    print(f"Auditing {len(repos)} wiki vaults in {args.dir} (fetch={args.fetch})...\n")
    clean_count = 0

    for r in repos:
        info = audit_vault(r, args.dir, fetch=args.fetch)
        if info["is_clean"]:
            clean_count += 1
        else:
            print(f"[{info['repo']}] (branch: {info['current_branch']})")
            if info["uncommitted_count"] > 0:
                print(f"  - Uncommitted notes/files: {info['uncommitted_count']} ({info['staged_count']} staged, {info['unstaged_count']} modified, {info['untracked_count']} untracked)")
            if info["has_ds_store"]:
                print(f"  - Note: contains untracked/modified .DS_Store")
            if info["unpushed_branches"]:
                print(f"  - Unpushed: {', '.join(info['unpushed_branches'])}")
            if info["pullable_branches"]:
                print(f"  - Incoming updates: {', '.join(info['pullable_branches'])}")
            if not info["has_remote"]:
                print(f"  - WARNING: No remote configured")
            print()

    print(f"Summary: {clean_count}/{len(repos)} vaults clean & fully synced.")

def cmd_pull(args):
    repos = find_wiki_repos(args.dir)
    print(f"Pulling remote updates across {len(repos)} wiki vaults...\n")
    pulled = 0

    for r in repos:
        info = audit_vault(r, args.dir, fetch=True)
        if not info["has_remote"]:
            continue

        for pb in info["pullable_branches"]:
            b_name = pb.split()[0]
            if b_name == info["current_branch"]:
                if info["uncommitted_count"] == 0:
                    p = run_git(["pull", "--ff-only"], r)
                    if p.returncode == 0:
                        print(f"[{info['repo']}] ✓ Pulled incoming notes on '{b_name}'")
                        pulled += 1
                    else:
                        print(f"[{info['repo']}] ✗ Fast-forward pull failed on '{b_name}': {p.stderr.strip()}")
                else:
                    # Check if there is overlap
                    overlap_check = run_git(["diff", "--name-only", f"HEAD..origin/{b_name}"], r)
                    remote_files = set(overlap_check.stdout.splitlines())
                    local_files = set(run_git(["diff", "--name-only"], r).stdout.splitlines())
                    if not remote_files.intersection(local_files):
                        p = run_git(["pull", "--ff-only"], r)
                        if p.returncode == 0:
                            print(f"[{info['repo']}] ✓ Pulled incoming notes on '{b_name}' (no file conflict with working notes)")
                            pulled += 1
                        else:
                            print(f"[{info['repo']}] ⚠ Skipped pull on '{b_name}': uncommitted local edits")
                    else:
                        print(f"[{info['repo']}] ⚠ Skipped pull on '{b_name}': incoming notes conflict with local edits")
            else:
                anc = run_git(["merge-base", "--is-ancestor", b_name, f"origin/{b_name}"], r)
                if anc.returncode == 0:
                    ff = run_git(["branch", "-f", b_name, f"origin/{b_name}"], r)
                    if ff.returncode == 0:
                        print(f"[{info['repo']}] ✓ Fast-forwarded branch '{b_name}'")
                        pulled += 1

    print(f"\nCompleted pull. {pulled} vault branch(es) updated.")

def cmd_push(args):
    repos = find_wiki_repos(args.dir)
    print(f"Pushing unpushed branches across {len(repos)} wiki vaults...\n")
    pushed = 0

    for r in repos:
        info = audit_vault(r, args.dir, fetch=False)
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
                print(f"[{info['repo']}] Pushing '{b_name}' to GitHub...")
                p = run_git(["push", "-u", "origin", b_name], r)
                if p.returncode == 0:
                    print(f"  ✓ Pushed '{b_name}'")
                    pushed += 1
                else:
                    print(f"  ✗ Failed to push '{b_name}': {p.stderr.strip()}")

    print(f"\nCompleted push. {pushed} vault branch(es) pushed.")

def cmd_backup(args):
    repos = find_wiki_repos(args.dir)
    msg = args.message or f"wiki backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"Running automated backup commit across {len(repos)} wiki vaults: '{msg}'\n")

    committed = 0
    for r in repos:
        info = audit_vault(r, args.dir, fetch=False)
        if info["uncommitted_count"] > 0:
            # Stage all files
            run_git(["add", "-A"], r)
            p = run_git(["commit", "-m", msg], r)
            if p.returncode == 0:
                print(f"[{info['repo']}] ✓ Committed {info['uncommitted_count']} modified/new note(s)")
                committed += 1
            else:
                print(f"[{info['repo']}] ✗ Commit failed: {p.stderr.strip()}")
        else:
            print(f"[{info['repo']}] Clean (nothing to commit)")

    print(f"\nCommitted changes in {committed} vault(s).")
    if args.push:
        print("\nPushing backups to remote...")
        cmd_push(args)

def cmd_sync(args):
    print("=== STEP 1: Pull Remote Changes ===")
    cmd_pull(args)
    if args.commit:
        print("\n=== STEP 2: Backup Local Notes ===")
        cmd_backup(args)
    print("\n=== STEP 3: Push to GitHub ===")
    cmd_push(args)

def main():
    parser = argparse.ArgumentParser(description="Multi-Vault / Wiki Git Synchronization Utility")
    parser.add_argument("--dir", default=DEFAULT_WIKIS_DIR, help="Target wikis/vaults directory")

    subparsers = parser.add_subparsers(dest="command")

    audit_parser = subparsers.add_parser("audit", help="Audit all wiki vaults")
    audit_parser.add_argument("--fetch", action="store_true", help="Fetch remotes before auditing")

    subparsers.add_parser("pull", help="Fast-forward pull incoming notes from remote")
    subparsers.add_parser("push", help="Push local vault branches to remote")

    backup_parser = subparsers.add_parser("backup", help="Auto-commit uncommitted notes and optionally push")
    backup_parser.add_argument("-m", "--message", help="Custom commit message (default: timestamped backup)")
    backup_parser.add_argument("--push", action="store_true", help="Push after committing")

    sync_parser = subparsers.add_parser("sync", help="Run pull, optional backup commit, and push")
    sync_parser.add_argument("--commit", action="store_true", help="Auto-commit local notes before pushing")
    sync_parser.add_argument("-m", "--message", help="Custom commit message if committing")

    args = parser.parse_args()
    if not args.command or args.command == "audit":
        cmd_audit(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "backup":
        cmd_backup(args)
    elif args.command == "sync":
        cmd_sync(args)

if __name__ == "__main__":
    main()
