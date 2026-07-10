# Media Server Service Reference

This reference records service details that may change. Verify live state before
acting.

## URLs

- Jellyfin: `http://100.81.22.64:8096`
- Radarr: `http://100.81.22.64:7878`
- qBittorrent: `http://100.81.22.64:8087`
- Prowlarr: `http://100.81.22.64:9696`
- Seerr: `http://100.81.22.64:5055`

## Compose Services

Stack path on `fx505`:

```text
/home/kchauhan/services/media-server/compose.yaml
```

Known services in the stack:

- `jellyfin`
- `sonarr`
- `radarr`
- `lidarr`
- `prowlarr`
- `qbittorrent`
- `bazarr`
- `seerr`
- `readarr`
- `profilarr`
- `flaresolverr`

## NFS Exports

`glowdesk` exports to `fx505` at `192.168.1.1`.

Expected core exports:

```text
/mnt/hdd
/mnt/hdd2
/mnt/hdd3
```

`/mnt/hdd4` is external/optional and should not be required for NFS startup.
