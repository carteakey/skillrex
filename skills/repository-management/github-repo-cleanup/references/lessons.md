# Lessons from a real cleanup

These are the failure modes and gotchas that showed up while pruning ~20 repos.

## Inventory

- `gh repo list --json` does **not** return `parent`. Fetch it per fork:
  `gh api repos/<owner>/<repo> --jq '.parent.full_name'`.
- `gh repo view` in a `for` loop can hang on deleted repos (404s). Use one
  `gh repo list --json name` call to verify deletions instead.
- `diskUsage` is in KB. A 570,000 value is ~570 MB, not 570 KB.

## Forks

- A fork that looks stale can still have unique commits. Always compare:
  `git rev-list --count upstream/<branch>..HEAD`.
- A fork with `ahead=0` is a pure mirror; delete it and use upstream.
- A fork with `ahead>0` may be a maintained fork (e.g. a revived project with
  29 merged PRs) or a single open PR. Keep it until the work lands upstream.
- Use `git clone --filter=blob:none --no-checkout` for the check; it avoids
  downloading large blobs from big forks.

## Deleting

- `gh repo delete` needs the `delete_repo` scope. `gh auth refresh -h
  github.com -s delete_repo` starts a device flow: copy the one-time code,
  open the URL, authorize, then retry.
- Archived repos are read-only. `gh repo edit` has no `--archived` flag; use
  `gh api -X PATCH repos/<owner>/<repo> -F archived=false`, push, then
  `-F archived=true`.
- Deleting a fork does not delete its upstream.

## Migrating notes before deletion

- Move the notes to the canonical notes system first, then delete. Preserve
  the exact files as attachments or patches; a summary is not a backup.
- Notion file uploads need a two-step flow: `notion-create-file-upload` →
  `POST` the file to the returned `upload_url` with the returned headers →
  use the `markdown_source` on the page.
- Subprojects (trailers, assets, generators) belong in their code repo, not
  the notes vault. Move them, update relative paths (`README`, `build.mjs`,
  `tools/*.sh`), commit, and push.
- Check for committed secrets (`.env`, keys) and rotate them whether or not
  the repo is deleted.

## Local cleanup

- Remove the clone, any `.private/` clone, and symlinks that pointed at the
  deleted notes repo.
- Before removing anything, check `git status` and `git log @{u}..HEAD` for
  unpushed work. Dirty repos are not deletion candidates.
- Keep a backup of the notes system (e.g. `context-backup`) and refresh it
  after structural changes.

## Verification

- Verify the destination has the content: the Notion page and attachments,
  the code-repo commit, or the archive.
- Verify the deleted names are absent from `gh repo list`.
- Report exactly what was deleted, what was preserved, and where.
