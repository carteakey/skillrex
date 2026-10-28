---
name: worktree-cleanup
description: Multi-repository Git worktree auditing, pruning, and safe cleanup tool. Automatically discovers linked worktrees across workspaces (e.g., /Users/kchauhan/repos, ~/.codex/worktrees), prunes ghost metadata for deleted directories, identifies merged and remote-pushed worktrees, and safely reclaims disk space while strictly protecting uncommitted changes and scratch files.
---

# Worktree Cleanup

A multi-repository Git worktree auditing, pruning, and safe cleanup engine for local development workspaces.

## Overview

When developing with multiple agents or parallel features, git worktrees often accumulate across directories (e.g. `/Users/kchauhan/repos/<repo>-<branch>`, `~/.codex/worktrees/<uuid>/<repo>`, `/private/tmp/*`). Over time, these consume gigabytes of disk space (especially with nested `node_modules`, `target`, or build artifacts) and clutter workspace directories.

`worktree-cleanup` provides conflict-safe, automated workflows to audit, prune stale references, and safely remove completed worktrees across dozens of repositories simultaneously without risking data loss.

## Core Rules & Safety Guardrails

1. **Protect Uncommitted Work**: Never remove a worktree containing uncommitted tracked modifications or untracked scratch files unless explicitly instructed with `--force`.
2. **Never Clobber Branches**: Removing a git worktree (`git worktree remove`) only unlinks and deletes the checked-out working folder; the underlying git branch and commit history remain completely preserved in the repository.
3. **Prune Ghost Metadata First**: When directories in `/private/tmp` expire or get reboot-deleted, git leaves stale bookkeeping records. Pruning (`git worktree prune`) cleans these records safely without modifying any branches.
4. **Preserve Unmerged Experiments**: Any worktree on an unmerged branch that has not yet been pushed to `origin` must be preserved or explicitly backed up to a remote branch before cleanup.
5. **Clean Empty Parents**: When secondary worktrees in dedicated subdirectories (such as `.worktrees/` or task UUID folders) are removed, clean up empty parent directories to keep the filesystem orderly.

---

## CLI Tool Usage

The skill provides an automated helper script at `scripts/worktree_cleanup.py`.

```bash
# 1. Audit all worktrees in workspace (shows size, branch, merged status, dirty files)
python3 scripts/worktree_cleanup.py audit

# 2. Output structured JSON for automation or agents
python3 scripts/worktree_cleanup.py audit --json

# 3. Prune stale worktree metadata (ghost worktrees whose directories were deleted)
python3 scripts/worktree_cleanup.py prune

# 4. Dry-run cleanup (previews what would be removed and disk space reclaimed)
python3 scripts/worktree_cleanup.py clean --dry-run

# 5. Safely clean up all merged and pushed worktrees (skips dirty/uncommitted work)
python3 scripts/worktree_cleanup.py clean

# 6. Target custom directory
python3 scripts/worktree_cleanup.py --dir /path/to/repos audit
```

---

## Interactive Agent Procedure

When the user asks to inspect, audit, or clean up worktrees:

### Step 1: Audit
Run `python3 scripts/worktree_cleanup.py audit` to categorize all worktrees across repositories into:
1. **Primary Repositories**: The main clone roots (never deleted).
2. **Prunable Ghosts**: Worktree registrations whose directories no longer exist on disk (e.g. `/private/tmp/*`).
3. **Safe to Remove (Merged)**: Secondary worktrees whose branch is fully merged into `main`/`master` and whose working tree is clean.
4. **Safe to Remove (Pushed)**: Secondary worktrees whose branch is clean and fully pushed to `origin`.
5. **Protected (Uncommitted / Scratch)**: Worktrees with uncommitted changes, untracked files, or unpushed local work.

### Step 2: Prune Ghost Worktrees
Run `python3 scripts/worktree_cleanup.py prune` (or `git worktree prune` in the affected repositories) to purge stale git pointers.

### Step 3: Verify and Protect Uncommitted Work
For any worktrees flagged with uncommitted changes or scratch files:
- Inspect the diff (`git status`, `git diff`).
- If valuable, commit and push to a feature or backup branch (`backup/<task-name>`).
- If ephemeral or obsolete, ask the user before discarding or leave behind as requested.

### Step 4: Safely Clean Up Completed Worktrees
Run `python3 scripts/worktree_cleanup.py clean` to remove clean worktrees that are merged or pushed, reclaiming disk space and removing directory clutter.
