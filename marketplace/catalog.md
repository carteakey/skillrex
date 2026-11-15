# skillrex Catalog

## hatch-pet-fastpath

- Path: `creative/hatch-pet-fastpath`
- Category: `creative`
- Description: Add quota-aware staging, early visual approval, repair routing, and final-QA ordering to Codex v2 animated pet production. Use with hatch-pet when the user wants a fast or low-waste pet workflow, wants to approve a base before full animation, mentions limited image-generation quota, requests a retro low-poly or PS2-style pet, or wants to avoid repeated full-atlas rebuilds.
- References: 1

## deal-finder

- Path: `deal-finder`
- Description: Scrapes and summarizes the top deals from rfd.davegallant.ca.

## did-openai-cook-my-drive

- Path: `did_openai_cook_my_drive`
- Description: Checks if the user is affected by the OpenAI Codex CLI SSD wear bug (TRACE logging to SQLite). Diagnoses the local database size, version, and guides the user on checking SSD write wear stats on Linux, macOS, and Windows.
- Scripts: 1

## email-management

- Path: `email-management`
- Description: Comprehensive email management: CLI control with Himalaya, specialized auditing, and automated workflows for inbox organization, security, and cleanup.
- Scripts: 3
- References: 8

## event-monitoring

- Path: `event-monitoring`
- Description: Automate the discovery and reporting of new items from web sources with robust deduplication.
- References: 2

## fleet-bandwidth

- Path: `fleet-bandwidth`
- Description: Monitor real-time network activity, per-process bandwidth utilization, and socket connections across all homelab fleet devices (KPC, FX505, Mac Server M1, MacBook Air M2, and Raspberry Pi) using bandwhich. Use this skill when the user asks to check network activity, diagnose high bandwidth usage, inspect network traffic across machines, or generate a fleet bandwidth report.
- Scripts: 1
- References: 2

## himalaya

- Path: `himalaya`
- Description: Himalaya CLI: IMAP/SMTP email from terminal.
- References: 2

## letterboxd-log-watches

- Path: `letterboxd-log-watches`
- Description: Add historical cinema watches to a user's Letterboxd diary from receipts, booking confirmations, ticket text, screenshots, or pasted showtime lists. Use when Codex must parse film titles and screening dates, prepare one or more dated Letterboxd diary entries in the user's logged-in browser, avoid duplicates, obtain required save confirmation, and verify the resulting diary rows.

## llm-wiki

- Path: `llm-wiki`
- Description: Karpathy's LLM Wiki: build/query interlinked markdown KB.

## model-inventory-manager

- Path: `model-inventory-manager`
- Description: Audit and cleanup model files and configurations. Use when identifying old models, cleaning up disk space, or reconciling serving configs with physical files.
- Scripts: 1

## qwen4exp-refresh

- Path: `qwen4exp-refresh`
- Description: Audit, refresh, build, and benchmark both Strata (Platinum tier) and llama.cpp (Gold & Experimental tiers) for Qwen3.8-Flash-Next (qwen4exp). Tracks merged and open PRs (native MTP, MoE LRU cache, fast FA, indexer optimizations), maintains worktrees, compiles server binaries, and executes standardized 7-way parity benchmarks against identical model quants.
- Scripts: 4
- References: 1

## refresh-llama

- Path: `refresh-llama`
- Description: Inspect upstream llama.cpp changes, track open pull requests, update/fast-forward master (Gold tier), maintain the Unified QSA Sparsity + MTP branch, compile server/bench binaries, and verify model serving through llama-swap. Use this skill when the user asks to refresh llama, update llama.cpp, check upstream commits or PRs, rebuild llama-server/llama-bench, or verify gold/experimental serving parity.
- Scripts: 1
- References: 1

## github-repo-cleanup

- Path: `repository-management/github-repo-cleanup`
- Category: `repository-management`
- Description: Audit and prune a GitHub account's repositories safely. Use when the user asks which repos to delete, wants to consolidate notes/docs repos, clean up forks, archive stale projects, or reduce repo sprawl. Covers inventory, safe-delete classification, fork unique-commit checks, migrating content before deletion, the delete_repo scope, local clone cleanup, and verification.
- Scripts: 2
- References: 1

## system-performance

- Path: `system-performance`
- Description: Performs system load, memory, swap, and thermal diagnostics on macOS and Linux hosts, identifies resource hogs (including ANECompilerService/CoreML loops), and outputs a formatted markdown performance report. Trigger this skill whenever the user asks about system slowness, diagnostic reports, or system monitoring.

## toronto-weekend-events

- Path: `toronto-weekend-events`
- Description: Aggregate Toronto events from multiple sources (blogTO, Eventbrite, Meetup, r/toronto, Narcity) into a categorized digest. Covers weekend events, career/professional Meetup monitoring, and delta-based change detection. Designed for cron delivery.
- Scripts: 1
- References: 3

## tpl-map-pass-monitor

- Path: `tpl-map-pass-monitor`
- Description: Monitor Toronto Public Library MAP/ePass availability for configured attractions and report only when target passes are available; use for TPL MAP pass checks, heartbeat checks, and silent-if-no-results scheduled runs.

## vault-76-organization

- Path: `vault-76-organization`
- Description: Summarize and organize a local Markdown notes vault by pulling latest changes, reviewing recent notes, extracting tasks, and producing a concise executive digest.
