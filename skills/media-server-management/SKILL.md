---
name: media-server-management
description: Manage Kartikey's homelab media server stack across fx505 and glowdesk. Use when Codex needs to check or repair Jellyfin, Radarr, qBittorrent, media downloads, download cleanup after Radarr imports, Docker Compose services, NFS mounts/exports, Tailscale URLs, or the fx505 media-server stack backed by glowdesk storage.
---

# Media Server Management

Use this skill for operational work on the homelab media stack. Prefer current
checks over remembered state, and preserve user data/configs.

## Hosts

- `fx505`: media app host.
  - Tailscale IP: `100.81.22.64`
  - LAN IP: `10.0.0.123`
  - SSH alias: `fx505`, `fx505-ts`
  - User: `kchauhan`
  - Key: `~/.ssh/id_ed25519_fx505`
- `glowdesk`: NAS/NFS server.
  - Tailscale IP: `100.94.234.125`
  - Ethernet/NFS IP: `192.168.1.2`
  - User: `kchauhan`
- `fx505` Ethernet/NFS client IP is `192.168.1.1`.

Use `ssh -o BatchMode=yes fx505 ...` for routine `fx505` checks. If `glowdesk`
key auth is not configured yet, password auth has previously been used only
interactively/in-session; do not save passwords in files or repos.

## Layout

On `fx505`:

- Compose stack: `/home/kchauhan/services/media-server/compose.yaml`
- App config root: `/opt/appdata/config`
- Media mounts:
  - `/mnt/media` -> `192.168.1.2:/mnt/hdd2`
  - `/mnt/share` -> `192.168.1.2:/mnt/hdd`
  - `/mnt/archive` -> `192.168.1.2:/mnt/hdd3`
  - `/mnt/music` -> `192.168.1.2:/mnt/usb2`
- Important containers:
  - `jellyfin` on `8096`
  - `radarr` on `7878`
  - `qbittorrent` on host `8087` mapping container `8080`
  - `bazarr` on `6767`
  - `prowlarr` on `9696`
  - `seerr` on `5055`

On `glowdesk`:

- Exports file: `/etc/exports`
- Required exports to `192.168.1.1`: `/mnt/hdd`, `/mnt/hdd2`, `/mnt/hdd3`
- `/mnt/hdd4` is external/optional. It must not block NFS startup. It has
  previously mounted but failed `exportfs` with `does not support NFS export`.

## Guard Units

On `fx505`:

- `ensure-jellyfin.service`
- `ensure-jellyfin.timer`
- Script: `/usr/local/sbin/ensure-jellyfin.sh`

The Jellyfin guard waits for `/mnt/media` to be a real NFS mount, runs
`docker compose up -d jellyfin`, and checks local HTTP.

On `glowdesk`:

- `ensure-nfs-exports.service`
- `ensure-nfs-exports.timer`
- Script: `/usr/local/sbin/ensure-nfs-exports.sh`

The NFS guard verifies required mounts, keeps optional `/mnt/hdd4` from
breaking NFS, reloads exports, restarts `rpcbind`/`nfs-server`, and checks
port `2049`.

## Common Checks

Check Tailscale and SSH:

```bash
tailscale status | rg -i 'fx505|glowdesk|100\.81\.22\.64|100\.94\.234\.125'
ssh -o BatchMode=yes fx505 'hostname; whoami; uptime'
```

Check NFS from `fx505`:

```bash
ssh -o BatchMode=yes fx505 'nc -vz -w 3 192.168.1.2 2049; findmnt -rn -t nfs4 -T /mnt/media; timeout 8 ls /mnt/media >/dev/null && echo media-readable'
```

Check NFS service on `glowdesk`:

```bash
ssh glowdesk 'systemctl is-active ensure-nfs-exports.timer ensure-nfs-exports.service nfs-server rpcbind; sudo exportfs -v'
```

Check media containers:

```bash
ssh -o BatchMode=yes fx505 'cd /home/kchauhan/services/media-server && docker compose ps --all'
```

Check app URLs:

```bash
curl -fsS --max-time 10 -I http://100.81.22.64:8096
curl -fsS --max-time 10 -I http://100.81.22.64:7878
curl -fsS --max-time 10 -I http://100.81.22.64:8087
```

Expected web responses:

- Jellyfin: `302 Found` to `web/`
- Radarr: `401 Unauthorized` means the app is up and auth is required
- qBittorrent: `200 OK` means the WebUI is up

## Repairs

If Jellyfin is down but NFS is healthy:

```bash
ssh -o BatchMode=yes fx505 'cd /home/kchauhan/services/media-server && docker compose up -d jellyfin'
ssh -o BatchMode=yes fx505 'sudo systemctl restart ensure-jellyfin.service'
```

If Jellyfin player errors show `FFmpeg exited with code 187` during VAAPI
transcoding, check whether the container has `/dev/dri`. Jellyfin may have been
recreated by an image update without GPU access if Compose does not declare the
device. The `jellyfin` service should include:

```yaml
devices:
  - /dev/dri:/dev/dri
```

Then recreate only Jellyfin and verify:

```bash
ssh -o BatchMode=yes fx505 'cd /home/kchauhan/services/media-server && docker compose up -d jellyfin && docker exec jellyfin ls -l /dev/dri'
```

If `/mnt/media` is not mounted:

```bash
ssh -o BatchMode=yes fx505 'sudo systemctl reset-failed mnt-media.mount; sudo systemctl restart mnt-media.automount; timeout 15 ls /mnt/media >/dev/null; findmnt -T /mnt/media'
```

If NFS is down on `glowdesk`:

```bash
ssh glowdesk 'sudo systemctl restart ensure-nfs-exports.service; systemctl --no-pager --lines=60 status ensure-nfs-exports.service'
```

If Radarr is not running:

```bash
ssh -o BatchMode=yes fx505 'cd /home/kchauhan/services/media-server && docker compose up -d radarr qbittorrent'
```

## Downloads

Radarr API key is in `/opt/appdata/config/radarr/config.xml`. Read it from the
host instead of hardcoding it in future updates.

Radarr imports completed downloads into the library path, but qBittorrent may
keep the original download under `/mnt/media/downloads` for seeding. Do not
assume an imported movie's download copy was cleared. When `/mnt/media` is full,
look for completed qBittorrent items that already have a library copy, then
remove only the qBittorrent seed copy.

If qBittorrent reports no tracked torrents, it is safe to inspect and clean
`/mnt/media/downloads` directly. For old imported leftovers, file size plus a
matching title in the library path is usually enough evidence; avoid relying on
Radarr/qBittorrent APIs when the filesystem already shows the duplicate.

Check Radarr queue:

```bash
ssh -o BatchMode=yes fx505 'python - <<'"'"'PY'"'"'
import json, urllib.request, xml.etree.ElementTree as ET
key = ET.parse("/opt/appdata/config/radarr/config.xml").getroot().findtext("ApiKey")
req = urllib.request.Request("http://127.0.0.1:7878/api/v3/queue?page=1&pageSize=20", headers={"X-Api-Key": key})
data = json.load(urllib.request.urlopen(req, timeout=10))
for r in data.get("records", []):
    total, left = r.get("size") or 0, r.get("sizeleft") or 0
    done = (total - left) / total * 100 if total else 0
    print(f"{r.get('title')} | {r.get('status')} | {done:.1f}% | left={r.get('timeleft')} | eta={r.get('estimatedCompletionTime')}")
PY'
```

For qBittorrent details, host-side localhost API may return `403`; querying
inside the container has worked:

```bash
ssh -o BatchMode=yes fx505 'docker exec qbittorrent curl -fsS --max-time 10 http://127.0.0.1:8080/api/v2/torrents/info'
```

Check download disk usage:

```bash
ssh -o BatchMode=yes fx505 'df -h /mnt/media /mnt/share; du -h -d 1 /mnt/media/downloads 2>/dev/null | sort -h | tail -30'
```

Check whether qBittorrent is tracking anything before direct cleanup:

```bash
ssh -o BatchMode=yes fx505 'docker exec qbittorrent curl -fsS "http://127.0.0.1:8080/api/v2/torrents/info?filter=all"; echo'
```

Compare download leftovers to library titles:

```bash
ssh -o BatchMode=yes fx505 'du -h -d 0 /mnt/media/downloads/* 2>/dev/null | sort -h'
ssh -o BatchMode=yes fx505 'find /mnt/media/movies /mnt/share/movies /mnt/media/tv /mnt/share/tv -mindepth 1 -maxdepth 2 -printf "%p\n" 2>/dev/null | sort'
```

When qBittorrent is empty and a download has a matching library item, remove the
download-side leftover directly:

```bash
ssh -o BatchMode=yes fx505 'rm -rf -- "/mnt/media/downloads/<download-name>"; df -h /mnt/media'
```

List completed qBittorrent items:

```bash
ssh -o BatchMode=yes fx505 'docker exec qbittorrent curl -fsS "http://127.0.0.1:8080/api/v2/torrents/info?filter=completed" | python3 - <<'"'"'PY'"'"'
import json, sys
for t in sorted(json.load(sys.stdin), key=lambda x: x.get("size", 0), reverse=True):
    print(f"{t.get('size',0)/1024**3:6.1f} GiB | {t.get('category')} | {t.get('state')} | {t.get('name')} | {t.get('hash')}")
PY'
```

Before deleting a completed download, verify Radarr has imported it into
`/mnt/share/movies` or `/mnt/media/movies`. Use title/path checks rather than
guessing from the torrent name:

```bash
ssh -o BatchMode=yes fx505 'find /mnt/share/movies /mnt/media/movies -maxdepth 2 -iname "*Predestination*" -print 2>/dev/null'
```

Remove an already-imported qBittorrent download copy:

```bash
ssh -o BatchMode=yes fx505 'HASH="<torrent-hash>"; docker exec qbittorrent curl -fsS -X POST --data-urlencode "hashes=$HASH" --data-urlencode "deleteFiles=true" http://127.0.0.1:8080/api/v2/torrents/delete; df -h /mnt/media'
```

For qBittorrent v5, use `torrents/start` instead of the older `resume` endpoint
when recovering errored torrents:

```bash
ssh -o BatchMode=yes fx505 'HASH="<torrent-hash>"; docker exec qbittorrent curl -fsS -X POST --data-urlencode "hashes=$HASH" http://127.0.0.1:8080/api/v2/torrents/start'
```

If qBittorrent reports `error`, read the persistent log; Docker stdout may not
include file-write failures:

```bash
ssh -o BatchMode=yes fx505 'tail -250 /opt/appdata/config/qbittorrent/data/logs/qbittorrent.log | rg -i -C 3 "error|failed|no space|permission|denied|Dune|<torrent-hash>"'
```

If qBittorrent leaves `.fuse_hidden...` files after a failed delete, restart
qBittorrent and retry cleanup. If the hidden file persists but is tiny, it is
less urgent than freeing large completed downloads.

## Bad or Glitching Movie Files

When playback glitches, separate client/transcode problems from file corruption:

1. Check Jellyfin logs to see whether it is transcoding, remuxing, or direct
   playing.
2. Check NFS read speed from the movie path.
3. Probe and decode the suspected time range with `ffmpeg`.
4. If qBittorrent still has the torrent, force a recheck.

Useful commands:

```bash
ssh -o BatchMode=yes fx505 'docker logs --since=2h --tail=200 jellyfin 2>&1 | rg -i "Dune|ffmpeg|transcod|remux|error|warn|subtitle|stream" || true'
ssh -o BatchMode=yes fx505 'FILE="/path/to/movie.mkv"; ffmpeg -hide_banner -v error -ss 00:55:00 -t 180 -i "$FILE" -map 0:v:0 -map 0:a:0 -f null - 2>&1 | sed -n "1,120p"'
ssh -o BatchMode=yes fx505 'HASH="<torrent-hash>"; docker exec qbittorrent curl -fsS -X POST --data-urlencode "hashes=$HASH" http://127.0.0.1:8080/api/v2/torrents/recheck'
```

HEVC errors like `Could not find ref with POC` and `Error constructing the frame
RPS` indicate real video stream corruption. Matroska warnings like `invalid as
first byte of an EBML number` can indicate container or stream damage. A simple
remux is not enough if a remuxed sample still decodes with HEVC reference-frame
errors; get a replacement release.

During qBittorrent recheck, `amount_left` can temporarily look huge because
unchecked pieces are counted as missing. Wait for the recheck to finish before
deciding. If it drops below 100% and starts downloading, bad pieces were found.
If the disk is full, repair can fail with `No space left on device`.

Radarr/Prowlarr replacement search may report zero results even when an indexer
exists. Check:

```bash
ssh -o BatchMode=yes fx505 'docker logs --since=10m --tail=250 radarr 2>&1 | rg -i "search|indexer|reject|grab|download|error|warn" || true'
ssh -o BatchMode=yes fx505 'python3 - <<'"'"'PY'"'"'
import json, urllib.request, xml.etree.ElementTree as ET
key = ET.parse("/opt/appdata/config/radarr/config.xml").getroot().findtext("ApiKey")
req = urllib.request.Request("http://127.0.0.1:7878/api/v3/indexer", headers={"X-Api-Key": key})
for i in json.load(urllib.request.urlopen(req, timeout=20)):
    print(i["name"], i.get("enableAutomaticSearch"), i.get("enableInteractiveSearch"))
PY'
```

## Subtitles

Bazarr API key is in `/opt/appdata/config/bazarr/config/config.yaml`. Read it
from the host instead of hardcoding it in future updates.

Start Bazarr if needed:

```bash
ssh -o BatchMode=yes fx505 'cd /home/kchauhan/services/media-server && docker compose up -d bazarr'
```

If Bazarr automatic search fails because wanted languages/profiles are not
populated or provider credentials are missing, a matching sidecar `.srt` next
to the movie file is an acceptable fallback. Name sidecars with the exact movie
basename plus language suffix, for example `Movie Name.en.srt`, then trigger a
Bazarr disk scan for the Radarr movie ID.

For MKVs that already contain correct embedded subtitles, prefer extracting the
embedded tracks over downloading mismatched web subtitles. Enable Bazarr's
embedded provider in `general.enabled_providers` and set
`general.use_embedded_subs` to `False` in
`/opt/appdata/config/bazarr/config/config.yaml`, then restart Bazarr. This lets
Bazarr extract embedded tracks as sidecars instead of relying on Jellyfin to use
embedded subtitles directly.

Trigger a Bazarr disk scan:

```bash
ssh -o BatchMode=yes fx505 'python - <<'"'"'PY'"'"'
import urllib.parse, urllib.request, yaml
movie_id = 170
cfg = yaml.safe_load(open("/opt/appdata/config/bazarr/config/config.yaml"))
key = cfg["auth"]["apikey"]
params = urllib.parse.urlencode({"radarrid": movie_id, "action": "scan-disk"})
req = urllib.request.Request(f"http://127.0.0.1:6767/api/movies?{params}", data=b"", method="PATCH", headers={"X-API-KEY": key})
print(urllib.request.urlopen(req, timeout=10).status)
PY'
```

Validate sidecars:

```bash
ssh -o BatchMode=yes fx505 'find "/mnt/share/movies/Dune (2021) {tmdb-438631}" -maxdepth 1 -type f \( -name "*.mkv" -o -name "*.srt" \) -printf "%f\n"'
```

When combining forced/foreign-dialogue subtitles with full English subtitles,
extract the embedded tracks with `mkvextract`, parse SRT cues by timestamp, and
write one sidecar sorted by start time. Do not concatenate SRT files blindly:
renumber cues and preserve cue timing. For Dune Part Two, the useful embedded
tracks were English forced plus full English; the SDH track was not used.

## fx505 Wi-Fi Routing

`fx505` has two Wi-Fi paths on the `10.0.0.0/24` LAN:

- `wlan1`: external USB 5 GHz adapter, preferred for internet and Jellyfin
  client traffic. Expected IP: `10.0.0.244`.
- `wlan0`: internal 2.4 GHz adapter, fallback only. Expected IP:
  `10.0.0.123`.

NFS to `glowdesk` must stay on Ethernet:

- `enp4s0`: `192.168.1.1/24`
- `glowdesk`: `192.168.1.2`

Check active routing:

```bash
ssh -o BatchMode=yes fx505 'ip route get 1.1.1.1; ip route get 10.0.0.84; iw dev wlan0 link; iw dev wlan1 link'
```

The Fire TV has recently appeared as `10.0.0.84`. If playback stutters while
Jellyfin is only remuxing (`-codec:v:0 copy`), check route and ping to the Fire
TV. Bad case was traffic over `wlan0` with 100-400 ms ping spikes; good case is
over `wlan1` with low single-digit to low tens of ms.

NetworkManager's USB 5 GHz profile has not reliably installed a gateway route,
and a blunt "disconnect 2.4 whenever 5 GHz appears" approach can destabilize
SSH/NetworkManager. Use the guarded controller stored in the homelab repo:

```bash
fx505/scripts/fx505-wifi-failback.sh
fx505/config/NetworkManager/dispatcher.d/90-fx505-wifi-failback
fx505/systemd/fx505-wifi-failback.service
fx505/systemd/fx505-wifi-failback.timer
```

The intended policy is:

- Keep `wlan0` 2.4 GHz autoconnect disabled by default.
- If `wlan1` 5 GHz is missing or fails gateway checks, enable and bring up
  `wlan0` as fallback.
- After `wlan1` passes multiple consecutive stability checks, restore routes to
  `wlan1`, disable `wlan0` autoconnect, then disconnect `wlan0`.

Do not use the old disabled hook
`/etc/NetworkManager/dispatcher.d/90-prefer-usb-5g.disabled` as a template.

Expected routes when healthy:

```text
default via 10.0.0.1 dev wlan1 src 10.0.0.244 metric 100
10.0.0.0/24 dev wlan1 src 10.0.0.244 metric 100
default via 10.0.0.1 dev wlan0 src 10.0.0.123 metric 900
10.0.0.0/24 dev wlan0 src 10.0.0.123 metric 900
192.168.1.0/24 dev enp4s0 src 192.168.1.1
```

## Known Current Facts

As of 2026-07-06:

- Jellyfin is expected at `http://100.81.22.64:8096` or `http://10.0.0.244:8096`.
- Radarr is expected at `http://100.81.22.64:7878`.
- qBittorrent is expected at `http://100.81.22.64:8087`.
- Jellyfin VAAPI transcoding depends on `/dev/dri` being mapped into the
  container. This is persisted in
  `/home/kchauhan/services/media-server/compose.yaml`; if a future update
  recreates Jellyfin and playback fails immediately, verify that mapping first.
- Dune Part Two on Fire TV should avoid video encoding by disabling video
  playback transcoding for user `kchauhan`; Jellyfin then remuxes with
  `-codec:v:0 copy`. If it still slows down, check Wi-Fi routing before blaming
  NFS or Jellyfin: the Fire TV route accidentally used internal 2.4 GHz
  `wlan0`, while USB 5 GHz `wlan1` was the intended priority path.
- `Dune - Part Two (2024)` exists under `/mnt/media/movies`.
- `Dune (2021)` completed as a 2160p HMAX WEB-DL under
  `/mnt/share/movies/Dune (2021) {tmdb-438631}`.
- `Dune (2021)` has a manually downloaded English SubtitleCat sidecar:
  `Dune (2021) {tmdb-438631} [WEBDL-2160p][HDR10][EAC3 Atmos 5.1][HEVC]-EVO.en.srt`.
- The 2160p BluRay REMUX grab for `Dune (2021)` was cancelled and removed from
  qBittorrent/Radarr queue.
- `Dune (2021)` EVO/TGx file previously glitched in playback. ffmpeg showed
  HEVC reference-frame errors around 55 minutes and Jellyfin logged Matroska
  EBML warnings. Moving the file back to the qBittorrent download path and
  forcing a torrent recheck found and repaired bad pieces; the repaired MKV was
  moved back to the Jellyfin library path.
- `Dune - Part Two (2024)` has a combined English sidecar at
  `/mnt/media/movies/Dune - Part Two (2024)/Dune - Part Two (2024) WEBDL-2160p.en.srt`.
  It was built from embedded English forced plus full English SRT tracks using
  `mkvextract`; Bazarr Radarr ID is `29`.
- `/mnt/media` filled because Radarr-imported downloads remained under
  `/mnt/media/downloads` for seeding. Trash cleanup freed about 20 GB from
  `/mnt/media/.Trash-1000`; Predestination's completed seed copy was also
  removed after confirming its library copy existed under `/mnt/share/movies`.
- `/mnt/media/.Trash-1000` had tiny Blade Runner entries with NFS input/output
  errors. They were not the main space issue after trash cleanup.
- Radarr search for replacement Dune reported `0 active indexers` / no results
  even though Radarr had `The Pirate Bay (Prowlarr)` configured and Prowlarr was
  up. Check Radarr/Prowlarr indexer state before assuming replacement search is
  functional.
- A direct filesystem cleanup of already-imported leftovers under
  `/mnt/media/downloads` freed `/mnt/media` from `22G` available to `144G`
  available. qBittorrent returned `[]` for tracked torrents, so the cleanup did
  not remove active downloads. Matching used title names and file sizes against
  library entries under `/mnt/media/movies`, `/mnt/share/movies`,
  `/mnt/media/tv`, and `/mnt/share/tv`.
- After direct cleanup, `/mnt/media/downloads` was effectively empty except for
  a tiny Dune `.fuse_hidden...` NFS remnant around 718 bytes. Treat tiny
  `.fuse_hidden` remnants as cosmetic unless they consume meaningful space.

## Updating This Skill

When the user says there is "more to come" or asks to remember new media-server
operational knowledge, update this skill. Keep secrets out of the skill. Prefer
verified commands, host paths, unit names, and current service behavior.
