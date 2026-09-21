---
name: wiki-sync
description: Multi-vault and wiki Git synchronization, auditing, and automated backup tool. Automatically synchronizes notes, Obsidian vaults, Forge project scratchpads, and Quartz documentation wikis across /Users/kchauhan/wikis. Handles timestamped automated backups, fast-forward pulls from mobile/cloud sync, and conflict-safe branch pushes.
---

# Wiki Sync

A multi-vault Git synchronization, audit, and automated backup engine designed for Obsidian vaults, Forge project contexts, and Quartz markdown knowledge bases.

## Overview

Wikis and personal knowledge bases (`/Users/kchauhan/wikis`) behave differently from standard software repositories:
1. They frequently receive updates from multiple devices (Obsidian mobile sync, laptop edits, web clippings).
2. Changes consist of atomic notes, images, clippings, and scratchpads that benefit from timestamped backup commits.
3. System metadata files (like macOS `.DS_Store`) should be filtered or ignored so they do not obstruct synchronization.

`wiki-sync` provides automated, conflict-safe workflows to audit all vaults, fast-forward incoming notes, safely commit ongoing scratchpad updates, and push all commits to GitHub.

---

## Managed Vaults & Knowledge Bases

The default directory is `/Users/kchauhan/wikis`, containing:
- **`vault-76`**: Primary personal Obsidian vault and knowledge base.
- **`forge`**: Private development project specs, scratchpads, and agent handoffs.
- **`homelabbr`**: Infrastructure, service configurations, and self-hosted runbooks.
- **`cartepedia`**: Curated reference knowledge and encyclopedic notes.
- **`llamapedia`**: AI/LLM models, prompt engineering, and agent architecture notes.
- **`wiki.carteakey.dev`**: Public-facing Quartz wiki website.
- **`wikibones`** & **`vault-76-template`**: Vault templates and structural patterns.

---

## CLI Tool Usage

The skill provides an automated helper script at `scripts/wiki_sync.py`:

```bash
# 1. Audit all wiki vaults (fast local scan)
python3 scripts/wiki_sync.py audit

# 2. Audit with remote fetch (contacts GitHub for incoming edits from other devices)
python3 scripts/wiki_sync.py audit --fetch

# 3. Pull incoming notes across all vaults (safe fast-forward)
python3 scripts/wiki_sync.py pull

# 4. Push all committed notes/branches to GitHub
python3 scripts/wiki_sync.py push

# 5. Create timestamped backup commit for all uncommitted notes across vaults
python3 scripts/wiki_sync.py backup --push

# 6. Full sync cycle (Pull incoming -> Backup local notes -> Push to GitHub)
python3 scripts/wiki_sync.py sync --commit
```

---

## Interactive Agent Workflow

When the user asks to sync their wikis, vaults, or notes:

### Step 1: Audit Vault Status
Run `scripts/wiki_sync.py audit --fetch` to inspect:
- Vaults with incoming edits from mobile/web.
- Vaults with uncommitted scratchpad notes or clippings.
- Vaults with unpushed commits.

### Step 2: Safe Fast-Forward Pull
Run `scripts/wiki_sync.py pull` to pull incoming changes:
- If working notes have no overlapping file conflicts, fast-forward cleanly.
- If uncommitted notes touch the same file as incoming commits, warn and isolate before pulling.

### Step 3: Automated Backup Commit (Optional / User-Requested)
If the user requests syncing their current working notes:
- Stage and commit with a standard timestamped message: `wiki backup: YYYY-MM-DD HH:MM:SS` (or descriptive context for Forge scratchpads).

### Step 4: Push to GitHub
Run `scripts/wiki_sync.py push` to ensure all vaults have zero unpushed commits on GitHub.
