#!/usr/bin/env bash
# Inventory a GitHub account's repos and list fork parents.
# Usage: scripts/audit.sh [owner]
set -euo pipefail

owner="${1:-$(gh api user --jq .login)}"

echo "== Repos for $owner =="
gh repo list "$owner" --limit 200 \
  --json name,description,isArchived,isFork,diskUsage,pushedAt \
  | python3 -c '
import json, sys
repos = json.load(sys.stdin)
print("repo".ljust(32), "arch".ljust(5), "fork".ljust(5), "MB".rjust(7), " pushed", "     description")
for r in sorted(repos, key=lambda x: x["pushedAt"] or ""):
    print(
        r["name"].ljust(32),
        str(r["isArchived"]).ljust(5),
        str(r["isFork"]).ljust(5),
        ("%.1f" % (r["diskUsage"] / 1024)).rjust(7),
        " ",
        (r["pushedAt"] or "")[:10],
        " ",
        (r["description"] or "")[:60],
    )
print("TOTAL", len(repos))
'

echo
echo "== Forks =="
gh repo list "$owner" --limit 200 --json name,isFork \
  | python3 -c 'import json,sys; [print(r["name"]) for r in json.load(sys.stdin) if r["isFork"]]' \
  | while read -r repo; do
      info=$(gh api "repos/$owner/$repo" --jq '"\(.parent.full_name // "none")|\(.parent.default_branch // "main")"')
      parent="${info%%|*}"
      branch="${info##*|}"
      printf "%-30s <- %-42s branch=%s\n" "$repo" "$parent" "$branch"
    done
