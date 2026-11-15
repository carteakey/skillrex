---
name: github-repo-cleanup
description: Audit and prune a GitHub account's repositories safely. Use when the user asks which repos to delete, wants to consolidate notes/docs repos, clean up forks, archive stale projects, or reduce repo sprawl. Covers inventory, safe-delete classification, fork unique-commit checks, migrating content before deletion, the delete_repo scope, local clone cleanup, and verification.
---

# GitHub Repo Cleanup

Reduce repository sprawl without losing work. The rule: delete only when the content is preserved elsewhere or the repo is a pure fork with no unique commits.

## 1. Inventory

```bash
gh repo list <owner> --limit 200 \
  --json name,description,isArchived,isFork,diskUsage,pushedAt
```

Sort by `pushedAt`. Flag archived repos, forks, missing descriptions, large `diskUsage` (KB), and anything not pushed in 12+ months.

`gh repo list --json` does **not** include `parent`; fetch it per fork with `gh api`.

## 2. Classify

| Class | Action |
| --- | --- |
| Content moved or superseded (e.g. "MOVED →", old blog) | Delete |
| Archived coursework / one-off demos | Delete if the user does not need the archive |
| Active project | Keep |
| Notes / docs / scratch repo | Migrate to the canonical notes system, then delete |
| Fork | Check unique commits (step 3) |
| Repo with unpushed local work | Do not delete |

Present a tiered list: **safe now**, **delete if not needed**, **keep**, and call out the biggest space wins.

## 3. Check forks before deleting

Get the parent and its default branch:

```bash
gh api repos/<owner>/<repo> --jq '{parent: .parent.full_name, branch: .parent.default_branch}'
```

Compare with a blobless clone:

```bash
tmp=$(mktemp -d)
git clone --filter=blob:none --no-checkout "https://github.com/<owner>/<repo>" "$tmp/repo"
git -C "$tmp/repo" remote add upstream "https://github.com/<parent>"
git -C "$tmp/repo" fetch upstream <branch>
echo "ahead:  $(git -C "$tmp/repo" rev-list --count upstream/<branch>..HEAD)"
echo "behind: $(git -C "$tmp/repo" rev-list --count HEAD..upstream/<branch>)"
git -C "$tmp/repo" log --oneline upstream/<branch>..HEAD | head
```

- **ahead = 0** → pure fork, safe to delete; use upstream.
- **ahead > 0** → keep, or land the work upstream first. Check open PRs with `gh pr list -R <parent> --author <user>`.

Do not assume a fork is pure because it looks old; `ahead` is the only reliable signal.

## 4. Migrate before deleting

- Notes/docs → the canonical notes system (Notion, Obsidian vault, wiki). Preserve the exact files as attachments or patches; do not summarize away the only copy.
- Subprojects → move them into their code repo, update path references (`README`, build scripts, relative asset paths), commit, and push.
- Check for committed secrets (`.env`, keys). Rotate them regardless of whether the repo is deleted.
- Keep a backup of the notes system (e.g. a `context-backup` repo) and refresh it after structural changes.

## 5. Delete

```bash
gh repo delete <owner>/<repo> --yes
```

This needs the `delete_repo` scope:

```bash
gh auth refresh -h github.com -s delete_repo
```

The refresh is a device flow: it prints a one-time code and a URL, then waits. Complete it in the browser and retry.

Archived repos are read-only. To push to one, unarchive temporarily:

```bash
gh api -X PATCH repos/<owner>/<repo> -F archived=false
# push
gh api -X PATCH repos/<owner>/<repo> -F archived=true
```

`gh repo edit` has no `--archived` flag; use the API.

## 6. Clean up locally

- Remove the clone: `rm -rf <path>`.
- Remove `.private/` clones and symlinks that pointed at the deleted notes repo.
- Before removing anything, check for unpushed work: `git status` and `git log @{u}..HEAD`.

## 7. Verify

```bash
gh repo list <owner> --limit 200 --json name
```

Check the deleted names are absent. `gh repo list` is faster and more reliable than looping `gh repo view` (which can hang on 404s).

Then verify the destination really has the content: the Notion page and attachments, the code-repo commit, or the archive.

## Safety rules

- Never delete a repo with unique commits or unpushed work.
- Never delete the only copy of notes; migrate first.
- Rotate any secrets found in deleted repos.
- Prefer archiving over deleting when unsure.
- Report exactly what was deleted and what was preserved.

## Helper scripts

- `scripts/audit.sh <owner>` — inventory plus fork parent/branch.
- `scripts/fork-check.sh <owner> <repo> <parent> <branch>` — ahead/behind for one fork.
