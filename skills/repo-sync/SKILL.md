---
name: repo-sync
description: Multi-repository Git synchronization and health auditing tool. Automatically audits local git repositories across a directory (e.g., /Users/kchauhan/repos) for uncommitted changes, unpushed branches, behind/incoming commits, and missing remotes. Safely pushes branches with upstream tracking and fast-forwards clean branches.
---

# Repo Sync

A multi-repository synchronization, auditing, and backup engine designed for local development workspaces.

## Overview

When managing multiple concurrent codebases, branches often get left unpushed, remotes remain unlinked, and incoming changes sit un-pulled. `repo-sync` provides automated, conflict-safe workflows to inspect, pull, and push across dozens of repositories simultaneously without risking data loss.

## Core Rules & Safety Guardrails

1. **Never Force Push**: Never overwrite remote history unless explicitly requested by the user.
2. **Never Pull Over Dirty Trees**: If a repository has uncommitted changes that could conflict with incoming remote commits, do **not** run destructive pulls. Instead, isolate the changes to a feature/migration branch first.
3. **Always Track Upstream**: When creating new remote branches, always establish tracking (`git push -u origin <branch>`) so future status queries are immediately aware of upstream state.
4. **Preserve Unrelated Histories**: If a local repository and its remote have divergent or unrelated histories, do not blindly clobber; push to a dedicated branch (e.g. `origin/local-main`) or merge with `--allow-unrelated-histories`.
5. **Private Remote Backups**: If a repository has local branches but no remote, use GitHub CLI (`gh repo create <owner>/<repo> --private`) to create an authenticated backup remote immediately.

---

## CLI Tool Usage

The skill provides an automated helper script at `scripts/repo_sync.py`.

```bash
# 1. Audit all repositories in workspace (fast local scan)
python3 scripts/repo_sync.py audit

# 2. Audit with remote fetch (contacts origin to check latest incoming commits)
python3 scripts/repo_sync.py audit --fetch

# 3. Safely fast-forward pull all clean branches that are behind remote
python3 scripts/repo_sync.py pull

# 4. Push all local branches that are new or ahead of remote with upstream tracking
python3 scripts/repo_sync.py push

# 5. Full sync (Pull clean branches + Push local branches)
python3 scripts/repo_sync.py sync

# 6. Target custom directory
python3 scripts/repo_sync.py --dir /path/to/repos audit
```

---

## Interactive Agent Procedure

When the user asks to check repository status, push changes, or sync their repos:

### Step 1: Audit
Run `repo_sync.py audit --fetch` (or run a structured inspection) to categorize all repos into:
1. **Clean & in-sync**: No actions needed.
2. **Unpushed branches / commits**: Local branches ready to push.
3. **Behind remote**: Clean branches ready to fast-forward.
4. **Active working sets**: Repos with uncommitted modifications or staged files.
5. **Orphan repos**: Repos lacking a configured remote.

### Step 2: Establish Missing Remotes
For any repository lacking a remote:
1. Check if a GitHub repository already exists under the user's account with `gh repo view <owner>/<repo>`.
2. If it exists, add it: `git remote add origin https://github.com/<owner>/<repo>.git`.
3. If it does not exist, create a private repository: `gh repo create <owner>/<repo> --private` and attach remote.

### Step 3: Fast-Forward Clean Repositories
For branches that are strictly behind origin:
- If the branch is currently checked out and the working tree is clean: `git pull --ff-only`.
- If the branch is not checked out: `git branch -f <branch> origin/<branch>` to update the ref instantly without switching worktrees.
- If the working tree is dirty: **skip** and report conflict risk to the user.

### Step 4: Push Local Branches with Upstream Tracking
For any branch that is ahead of upstream or has not yet been published to remote:
- Run `git push -u origin <branch>`.
- If local branch name matches a remote branch with unrelated history, push as an explicit refspec: `git push -u origin <branch>:local-<branch>`.

### Step 5: Triage Dirty Workspaces
For repositories with active uncommitted work that needs syncing with remote:
1. Create a migration/WIP branch: `git checkout -b codex/<feature>-sync`.
2. Commit local changes with an explicit summary.
3. Fast-forward `main` to `origin/main`.
4. Merge `main` into the feature branch, resolving any conflicts cleanly.
5. Push the feature branch to GitHub with upstream tracking.
