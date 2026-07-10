---
name: subtitle-management
description: Manage movie and TV subtitle workflows for Kartikey's media stack, including Bazarr embedded subtitles, extracting MKV subtitle tracks, combining forced foreign-dialogue subtitles with full English subtitles, creating sidecar SRT files, and refreshing Jellyfin/Bazarr metadata without modifying media files.
---

# Subtitle Management

Use this skill for subtitle-specific work on the media server. Use
`media-server-management` as well when host paths, service health, Docker
Compose, or Jellyfin/Radarr/Bazarr URLs are needed.

## Rules

- Do not modify MKV files when the task is only subtitle extraction or sidecar
  creation. `mkvextract` and `ffprobe` are read-only against the MKV.
- Prefer exact embedded tracks over random internet subtitles when the MKV has
  suitable embedded SRT/ASS tracks.
- For foreign-dialogue coverage plus normal English captions, combine the
  English forced track with the full English track into one `.en.srt` sidecar.
- Do not include SDH/HI cues unless the user asks for hearing-impaired captions.
- Avoid printing subtitle text into chat; report paths, cue counts, languages,
  and validation results instead.

## Bazarr

Bazarr config is on `fx505`:

```bash
/opt/appdata/config/bazarr/config/config.yaml
```

For embedded subtitle extraction, ensure:

- `general.enabled_providers` includes `embeddedsubtitles`
- `general.use_embedded_subs` is `False`

Restart Bazarr after config changes:

```bash
ssh -o BatchMode=yes fx505 'cd /home/kchauhan/services/media-server && docker compose restart bazarr'
```

Trigger a Bazarr disk scan for a movie:

```bash
ssh -o BatchMode=yes fx505 'python3 - <<'"'"'PY'"'"'
import urllib.parse, urllib.request, yaml
radarr_id = 29
cfg = yaml.safe_load(open("/opt/appdata/config/bazarr/config/config.yaml"))
key = cfg["auth"]["apikey"]
params = urllib.parse.urlencode({"radarrid": radarr_id, "action": "scan-disk"})
req = urllib.request.Request(
    f"http://127.0.0.1:6767/api/movies?{params}",
    data=b"",
    method="PATCH",
    headers={"X-API-KEY": key},
)
print(urllib.request.urlopen(req, timeout=20).status)
PY'
```

## Extract And Combine

Install `mkvtoolnix-cli` on `fx505` if `mkvextract` is missing. Then inspect
tracks:

```bash
ssh -o BatchMode=yes fx505 'ffprobe -v error -show_entries stream=index,codec_type,codec_name:stream_tags=language,title -of json "/path/movie.mkv"'
```

Extract only the needed subtitle tracks:

```bash
ssh -o BatchMode=yes fx505 'mkvextract tracks "/path/movie.mkv" 2:"/tmp/forced.en.srt" 3:"/tmp/full.en.srt"'
```

Combine SRTs by parsing cue timestamps, sorting by start time, and renumbering
cues. Do not concatenate files blindly; duplicate numbering and unsorted cues
can confuse players. Write the sidecar beside the movie with the exact movie
basename plus `.en.srt`.

Validate the result by checking file size and cue count:

```bash
ssh -o BatchMode=yes fx505 'python3 - <<'"'"'PY'"'"'
from pathlib import Path
import re
p = Path("/path/Movie Name.en.srt")
text = p.read_text(encoding="utf-8", errors="replace")
blocks = [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
print(p.exists(), p.stat().st_size, len(blocks))
PY'
```

## Timing Offset

If subtitles are early, shift the sidecar later with a positive offset. If they
are late, shift earlier with a negative offset. Always create a backup before
rewriting the sidecar, then refresh Bazarr and Jellyfin.

For small subjective drift, start with `500` to `1000` ms. Dune Part Two was
shifted `+750 ms` after the combined sidecar appeared slightly early.

## Jellyfin Refresh

After creating sidecars, trigger Bazarr scan first, then refresh Jellyfin. Use
an existing Jellyfin API key from its local database only for the refresh call;
do not store or print API keys.

```bash
ssh -o BatchMode=yes fx505 'python3 - <<'"'"'PY'"'"'
import sqlite3, urllib.request
con = sqlite3.connect("/opt/appdata/config/jellyfin/data/data/jellyfin.db")
token = con.execute("select AccessToken from ApiKeys order by Id limit 1").fetchone()[0]
req = urllib.request.Request(
    "http://127.0.0.1:8096/Library/Refresh",
    data=b"",
    method="POST",
    headers={"X-Emby-Token": token},
)
print(urllib.request.urlopen(req, timeout=20).status)
PY'
```

## Known Files

- Dune Part Two sidecar:
  `/mnt/media/movies/Dune - Part Two (2024)/Dune - Part Two (2024) WEBDL-2160p.en.srt`
- Dune Part Two Bazarr/Radarr ID: `29`
- The Dune Part Two sidecar was built from embedded English forced plus full
  English tracks; SDH was intentionally excluded.
