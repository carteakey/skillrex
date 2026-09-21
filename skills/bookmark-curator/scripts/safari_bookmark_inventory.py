#!/usr/bin/env python3
"""Summarize Safari bookmarks without exposing individual URLs by default."""

import argparse
import collections
import json
import plistlib
from pathlib import Path
from urllib.parse import urlparse


def walk(node, parents, rows):
    title = node.get("Title") or node.get("URIDictionary", {}).get("title") or "(untitled)"
    children = node.get("Children")
    if isinstance(children, list):
        next_parents = parents
        if title not in {"Root", "History"}:
            next_parents = parents + [title]
        for child in children:
            walk(child, next_parents, rows)
        return

    url = node.get("URLString")
    if not url:
        return
    parsed = urlparse(url)
    rows.append(
        {
            "title": title,
            "folder": " / ".join(parents) or "(root)",
            "host": (parsed.hostname or "").lower(),
            "url": url,
        }
    )


def is_local(host):
    return host in {"localhost", "127.0.0.1", "::1"} or host.startswith(("10.", "100.", "192.168.")) or host.endswith(".local")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=str(Path.home() / "Library/Safari/Bookmarks.plist"))
    parser.add_argument("--json", action="store_true", help="Emit item-level JSON, including URLs")
    parser.add_argument("--limit", type=int, default=30, help="Maximum folder/domain rows in summary mode")
    args = parser.parse_args()

    with open(args.path, "rb") as handle:
        root = plistlib.load(handle)

    rows = []
    walk(root, [], rows)
    if args.json:
        print(json.dumps(rows))
        return

    folders = collections.Counter(row["folder"] for row in rows)
    domains = collections.Counter(row["host"] for row in rows if row["host"])
    reading = sum("com.apple.ReadingList" in row["folder"] for row in rows)
    local = sum(is_local(row["host"]) for row in rows)

    print(f"total_urls\t{len(rows)}")
    print(f"reading_list\t{reading}")
    print(f"local_or_private_hosts\t{local}")
    print("folders")
    for name, count in folders.most_common(args.limit):
        print(f"{count}\t{name}")
    print("domains")
    for name, count in domains.most_common(args.limit):
        print(f"{count}\t{name}")


if __name__ == "__main__":
    main()
