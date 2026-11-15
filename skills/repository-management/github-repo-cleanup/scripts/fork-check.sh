#!/usr/bin/env bash
# Check whether a fork has unique commits against its upstream.
# Usage: scripts/fork-check.sh <owner> <repo> <parent-owner/repo> <parent-branch>
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "usage: $0 <owner> <repo> <parent-owner/repo> <parent-branch>" >&2
  exit 1
fi

owner="$1"
repo="$2"
parent="$3"
branch="$4"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

git clone -q --filter=blob:none --no-checkout "https://github.com/$owner/$repo" "$tmp/repo"
git -C "$tmp/repo" remote add upstream "https://github.com/$parent"
git -C "$tmp/repo" fetch -q upstream "$branch"

ahead=$(git -C "$tmp/repo" rev-list --count "upstream/$branch..HEAD")
behind=$(git -C "$tmp/repo" rev-list --count "HEAD..upstream/$branch")

echo "$repo: ahead=$ahead behind=$behind"
if [ "$ahead" -gt 0 ]; then
  echo "unique commits:"
  git -C "$tmp/repo" log --oneline "upstream/$branch..HEAD" | head -20
else
  echo "pure fork (no unique commits) — safe to delete; use upstream"
fi
