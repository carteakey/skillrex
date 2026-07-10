---
name: lytte-deploy
description: Use when working on a Lytte repo deployment, sync, Docker compose stacks, ASR runtime updates, Parakeet/pyannote rollout, GPU ASR health checks, or tests before deploying to a configured remote host.
---

# Lytte deployment skill

When this skill triggers, first orient in the repo:

```bash
pwd
git status --short --branch
git log --oneline -3
```

If `docs/DEPLOYMENT-SYNC.md` exists in the current repo, read it and follow it as the source of truth. Prefer updating that runbook over repeating long deployment instructions in chat.

Use environment variables for deployment-specific details instead of hardcoding personal information:

```bash
export LYTTE_DEPLOY_HOST="${LYTTE_DEPLOY_HOST:-user@host}"
export LYTTE_REMOTE_REPO="${LYTTE_REMOTE_REPO:-/path/to/lytte}"
export LYTTE_WEB_URL="${LYTTE_WEB_URL:-http://host:15173}"
export LYTTE_API_HEALTH_URL="${LYTTE_API_HEALTH_URL:-http://host:13001/health}"
export LYTTE_ASR_HEALTH_URL="${LYTTE_ASR_HEALTH_URL:-http://host:18001/health}"
```

Core habits:

- Preserve user/remote changes before pulling: inspect `git status`; stash dirty remote worktrees with a descriptive message before `git pull --ff-only`.
- Treat `$LYTTE_DEPLOY_HOST` as the deployment SSH target and `$LYTTE_REMOTE_REPO` as the repo path when set.
- Treat the `docker-compose.alt.yml` stack as the live shifted-port deployment unless the user says otherwise:
  - web `15173`
  - API `13001`
  - ASR `18001`
- Verify health before and after changes with local-host curls on the remote and configured external health URLs from the local machine.
- For GPU ASR, verify `nvidia-smi`, Docker's `nvidia` runtime, and `docker exec lytte-whisper-alt nvidia-smi`.
- Do not paste or commit secrets. Use local shell env vars or `.env` for `HF_TOKEN`.

Minimum local checks before sync:

```bash
PYTHONPATH=.:../../packages/engine/src python3 -m unittest discover -s tests -v
python3 -m compileall apps/whisper-service packages/engine/src
npm exec -- pnpm --filter @lytte/server test -- --run
npm exec -- pnpm --filter @lytte/web test -- --run
bash scripts/check-compose-config.sh
```

Run `python3 -m pytest packages/engine/tests -q` when `pytest` is installed.

Parakeet rollout posture:

- Build/test Parakeet separately before replacing the live ASR container.
- Prefer `ASR_MODE=parakeet-single-speaker` for a no-token smoke test.
- Use `ASR_MODE=parakeet-pyannote` only with `HF_TOKEN`/`HUGGINGFACE_TOKEN` and accepted pyannote model terms.
- The checked-in E2E smoke path is `bash scripts/parakeet-e2e-smoke.sh`; run it on a GPU Docker host, not casually on the Mac.
- Keep the current GPU `faster-whisper` deployment as the rollback path.
