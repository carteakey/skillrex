---
name: archive-iphone-videos
description: Export large iPhone videos from a synced Mac Photos library to Google Drive, verify original-file backups, and prepare or perform authorized iCloud Photos cleanup.
---

# Archive iPhone Videos

By default, preserve and verify original bytes in the user's chosen Drive account before removing selected assets from iCloud Photos. Upload requests alone do not authorize deleting originals.

## Scope and inventory

- Establish whether videos are in synced Mac Photos, on a connected iPhone, or already exported. The Mac must be unlocked for Photos UI access. A full iCloud account can leave newer iPhone videos unsynced.
- Ground the Drive account and folder; confirm the account when several exist. Preserve sharing settings.
- Rank by original bytes, not duration. For Mac Photos, run `scripts/inventory_videos.py --library '<Photos Library.photoslibrary>' --limit 5`. It reads SQLite without modifying it; schema failures must not be treated as an empty library.
- Honor the user's count/threshold; otherwise propose a small batch. Keep a private manifest of UUID, filename, date, duration, and original size. Filenames repeat, so match search results by date/duration and retain UUIDs. Convert the helper's UTC dates to Photos' display timezone when matching.
- Check free space before each batch, allowing for download/export and Drive sync caches. Avoid downloading the whole library or changing global Photos settings for a selective archive.

## Export and upload

- Use a supported Photos interface. On Mac: search the original filename, select the matching asset, then File → Export → Export Unmodified Original. Export outside the library bundle and outside iCloud-synced Desktop/Documents. Never modify Photos database records or library internals.
- Optimized libraries may wait several minutes for an original download while export shows 0%. The general task indicator is not reliable evidence of completion. Confirm the exported file exists with its full original byte count; investigate size mismatches before continuing.
- Preserve original filenames unless collision handling requires a date/UUID suffix. Refuse to overwrite an existing destination file. Record an MD5 checksum for Drive comparison.
- Use the Google Drive skill/connector when available, inspecting current schemas and upload limits. A 512 MiB connector limit was observed; do not retry oversized videos repeatedly or split/re-encode them without a request.
- For large files, use an already installed Drive desktop sync folder after verifying its account and destination, or use an authenticated browser file upload. Retain the staging file until cloud verification. If desktop transfers cancel or local sync files disappear, stop relying on that route, inspect the cloud folder, and retry from a retained export through another supported interface. Verify syncing actually starts.
- A file in the local sync folder is not a verified cloud backup. Observe upload completion and read cloud metadata in the target folder. Compare exact byte size and `md5Checksum` when available; displayed GB values may use different units. If the connector omits checksums, use another authenticated Drive interface or download-copy comparison before source deletion.
- For disk pressure, use the provider's supported remove-download/free-space operation only after cloud verification. Never delete the cloud file or Photos library internals to clear a cache.
- Maintain per-file states: inventoried, exported, uploading, cloud-verified, source-removed. Attribute progress/ETA to Drive; report pending uploads honestly. Do not call the archive complete until all selected files pass verification.

## Authorized cleanup

- Re-identify exact assets from the manifest and UI before deleting. By default, remove only cloud-verified assets within the user's cleanup scope. If the user explicitly requests deletion while uploads continue, first verify and retain complete local originals with exact sizes/checksums, explain that cloud backup is unfinished, and obtain any required irreversible-deletion confirmation. Record this run-specific override; do not carry it into future runs. iCloud Photos deletion propagates to other synced devices.
- Check current Apple guidance/account state before relying on recovery. Normally Recently Deleted offers recovery and does not count toward iCloud storage, so emptying it is unnecessary for space recovery.
- When iCloud exceeds its storage limit, deletion may immediately remove assets without recovery. Obtain action-time confirmation for irreversible deletion after presenting the verified archive and exact files; generic cleanup approval does not replace that confirmation.
- Never empty unrelated Recently Deleted items. Verify source removal and sync/storage updates when available. Distinguish expected original-byte savings from observed reclaimed iCloud space.

Apple references: [storage and recovery](https://support.apple.com/en-gb/108922), [Mac export and cleanup](https://support.apple.com/en-ca/guide/photos/phtda347cde8/mac).
