---
name: linear-init-repo
description: Initialize or connect a Git repository to Linear by inspecting repository context, reusing or creating a Linear project, proposing a focused milestone and committed issues, keeping speculative TODO items out, and recording the repository-to-Linear mapping. Use when asked to init, initialize, set up, bootstrap, connect, or onboard a repository or project to Linear.
---

# Initialize a Repository in Linear

Create the smallest useful Linear planning structure for a repository without turning speculative notes into commitments.

## Inspect

1. Read the applicable `AGENTS.md`, `README.md`, relevant documentation, `TODO.md`, recent Git history, and Git remotes.
2. Preserve unrelated local changes.
3. Confirm that Linear MCP is available and authenticated. If it is unavailable, report the blocker; do not silently substitute GitHub Issues or web automation.
4. Search Linear by repository name, remote name, and known aliases. Reuse an existing team, project, milestone, or issue rather than creating a duplicate.

## Establish the Active Objective

Treat work as committed only when supported by an explicit user request, an existing issue, or repository documentation that clearly marks it as active.

Treat `TODO.md` entries as speculative by default. Do not promote the whole file. If the current committed objective is unclear, ask one concise question before proposing Linear changes.

## Propose

Unless the user explicitly authorizes direct creation, present this proposal before writing to Linear:

- Existing or proposed Linear team and project
- One initial milestone
- Up to seven meaningful implementation issues; use fewer than three when the committed scope does not justify more
- Priorities and dependencies only where they affect execution order
- Any `TODO.md` items to promote and remove
- The local file that will record the Linear project mapping

Wait for approval before creating or modifying Linear data.

## Create

After approval:

1. Reuse existing Linear objects wherever possible.
2. Create no more than one project, one initial milestone, and seven initial issues unless the user requests broader planning.
3. Give each issue a clear objective, bounded scope, and concise acceptance or verification criteria.
4. Do not create issues for completed work, vague possibilities, trivial chores, or speculative research.
5. Use priorities, dependencies, labels, estimates, and dates only when they add concrete planning value. Prefer existing workspace conventions.
6. Promote only intentionally chosen `TODO.md` items. Remove each promoted item from `TODO.md` only after its Linear issue is created successfully.
7. Record the Linear team, project name, project URL, and its role as the authority for committed planned work in the repository-specific `AGENTS.md`, preserving existing instructions. If the file does not exist, include creating a minimal one in the approved proposal.
8. Do not commit or push local changes unless the user requests it or repository instructions explicitly require it.

## Verify and Report

Re-read the created or updated Linear objects and inspect the local diff. Confirm that no planned item remains duplicated across `TODO.md`, Linear, and GitHub Issues.

Summarize:

- Linear project and milestone links
- Issues created or reused
- Local files changed
- `TODO.md` items promoted
- Remaining blockers or decisions
