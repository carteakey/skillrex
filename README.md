# skillrex

Personal, portable AI-agent skills marketplace.

This repo is the maintained home for reusable skills that should work across agents such as Codex, Claude, and compatible local assistants. Skills are organized by category and kept as plain folders with a required `SKILL.md` plus optional `scripts/`, `references/`, `assets/`, or `templates/`.

## Layout

- `skills/` - curated skills, grouped by category.
- `marketplace/index.json` - generated machine-readable catalog.
- `marketplace/catalog.md` - generated human-readable catalog.
- `scripts/build_index.py` - catalog generator.

## Current Skills

- `email-management` - Himalaya email workflows plus scheduled newsletter, OTP/security, and smart organizer jobs.
- `event-monitoring` - recurring web/event discovery, including the historical Toronto Meetup monitor.
- `research/toronto-weekend-events` - Toronto weekend digest collection and formatting.
- `research/tpl-map-pass-monitor` - TPL MAP/ePass availability checks without committed credentials.
- `notes/vault-76-organization` - weekly Markdown vault summary and task extraction.

## Historical Cron Mapping

- `Newsletter Cleanup (Weekly)` -> `email-management`
- `OTP/Security Cleanup (Weekly)` -> `email-management`
- `Smart Inbox Organizer (Weekly)` -> `email-management`
- `TPL Map Monitor Heartbeat Fixed` -> `research/tpl-map-pass-monitor`
- `TPL Map Pass Monitor (Active Alerts)` -> `research/tpl-map-pass-monitor`
- `Meetup Event Discovery (Toronto)` -> `event-monitoring`
- `Vault-76 Sync & Organization (Weekly)` -> `notes/vault-76-organization`
- `Toronto Weekend Digest` -> `research/toronto-weekend-events`

## Install Manually

Copy a skill folder into the target agent's skills directory.

Codex example:

```bash
mkdir -p ~/.codex/skills
cp -a skills/software-development/code-review ~/.codex/skills/code-review
```

Claude-style local example:

```bash
mkdir -p ~/.claude/skills
cp -a skills/software-development/code-review ~/.claude/skills/code-review
```

For agents that support categorized skills, preserve the category path:

```bash
mkdir -p ~/.agent/skills/software-development
cp -a skills/software-development/code-review ~/.agent/skills/software-development/code-review
```

## Rebuild Catalog

```bash
python3 scripts/build_index.py
```

## Add A Skill

1. Add a directory under `skills/<category>/<skill-name>/`.
2. Put portable instructions in `SKILL.md`.
3. Put reusable helpers in `scripts/`, `references/`, `assets/`, or `templates/`.
4. Keep frontmatter minimal: `name` and `description`.
5. Run `python3 scripts/build_index.py`.
6. Commit the skill and updated marketplace files.

## Policy

This repo is curated, agent-agnostic, and non-destructive. Raw backups, private automation state, memories, cron prompts, chat names, and secrets stay outside the repo. Only copy them in after explicit review.
