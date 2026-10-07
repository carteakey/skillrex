#!/usr/bin/env python3
"""List the largest active videos from Mac Photos metadata without modifying it."""
import argparse
import datetime
import json
from pathlib import Path
import sqlite3


def inventory(library, limit):
    database = library.expanduser().resolve() / "database" / "Photos.sqlite"
    if not database.is_file():
        raise FileNotFoundError(database)
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("""
            SELECT a.ZUUID AS uuid, b.ZORIGINALFILENAME AS name,
                   b.ZORIGINALFILESIZE AS bytes, a.ZDURATION AS duration_seconds,
                   a.ZDATECREATED AS date
            FROM ZASSET a JOIN ZADDITIONALASSETATTRIBUTES b ON b.ZASSET=a.Z_PK
            WHERE a.ZKIND=1 AND a.ZTRASHEDSTATE=0 AND b.ZORIGINALFILESIZE>0
            ORDER BY b.ZORIGINALFILESIZE DESC, a.ZUUID LIMIT ?
        """, (limit,)).fetchall()
    epoch = datetime.datetime(2001, 1, 1, tzinfo=datetime.timezone.utc)
    videos = []
    for row in rows:
        video = dict(row)
        if video["date"] is not None:
            video["date"] = (epoch + datetime.timedelta(seconds=video["date"])).isoformat()
        videos.append(video)
    return {"source": "Mac Photos original-size metadata", "videos": videos,
            "total_bytes": sum(video["bytes"] for video in videos)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    try:
        result = inventory(args.library, args.limit)
    except (OSError, sqlite3.Error) as error:
        parser.exit(1, f"Cannot read Photos metadata: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
