---
name: backlog-creator
description: Discover and curate the next useful development backlog across one or many Git repositories by inspecting current remote PR, review, CI, release, tracker, documentation, test, and code state; identifying evidence-backed opportunities; separating speculative ideas from intentionally selected work; updating TODO.md and Linear or the repository's declared tracker without duplication; and producing a ranked handoff for Backlog Burner. Use when the user asks to create, refill, generate, discover, or prepare a backlog, find the next work after recent PRs, identify additional opportunities, or assemble the next burn-ready batch.
---

# Backlog Creator

Turn current repository reality into a small, ranked, burn-ready backlog. Discover work; do not implement it.

## Operating invariants

- Treat Git as code truth, repository Markdown as documentation truth, and the declared tracker as committed-work truth.
- Inspect actual remote PR heads, checks, reviews, and tracker state. Do not reason from a stale checkout alone.
- Keep speculative ideas in `TODO.md` or the repository's declared idea file. Put intentionally selected work in exactly one tracker.
- Never duplicate an item across `TODO.md`, Linear, and GitHub Issues.
- Prefer evidence-backed outcomes over generic cleanup, rewrites, or technology churn.
- Preserve dirty, untracked, private, generated, and user-owned files.
- Never publish Forge context, local data, secrets, incident artifacts, or unknown media.
- Do not implement, branch, commit, push, merge, deploy, or change production state unless separately requested.

## 1. Establish authority

For every repository:

1. Read the nearest `AGENTS.md`, `README`, planning files, and relevant architecture, development, release, and decision docs.
2. Read matching private Forge `Project.md` and `Scratchpad.md` when available, using them only as private context.
3. Inspect remotes, default branch, status, worktrees, branches, recent history, releases, and the repository's declared planning convention.
4. Inspect every open PR and the recent merged PR horizon relevant to the request. Default to the last 30 days or 20 merged PRs, whichever is smaller, unless repository activity suggests a better bound.
5. Read PR bodies, linked issues, unresolved review threads, current checks, and the files changed at each remote head. Distinguish superseded failures from current ones.
6. Reconcile repository aliases and search the authoritative tracker for existing projects, milestones, issues, and duplicates.

Do not make planning writes until this pass identifies the authoritative TODO surface and tracker. If Linear and GitHub Issues both contain active work without declared authority, ask which is authoritative before writing either.

## 2. Build the current-state ledger

Record a compact matrix per repository:

- latest default-branch and release state;
- open and recently merged PRs, their intent, review state, checks, and follow-up signals;
- current Backlog Reviewer verdicts or unresolved evidence gaps, when any exist;
- existing TODO candidates and committed tracker work;
- dirty or private artifacts that must remain untouched;
- gaps supported by code, tests, docs, runtime evidence, or explicit stakeholder requests;
- external dependencies such as credentials, hardware, owner content, or protected release authority.

Treat a failed check or review comment on an open PR as part of that PR unless it describes genuinely separate follow-up work. Do not manufacture a new backlog item merely to restate unfinished PR scope.
Treat missing verification on already-delivered work as verification debt on the existing issue or PR, not as a new product objective.

## 3. Discover opportunities

Search for bounded improvements in this order:

1. privacy, security, authentication, data integrity, destructive operations, migrations, and recovery;
2. correctness defects, regressions, missing acceptance coverage, and unresolved review findings;
3. operational reliability, observability, deployment, backup, and supportability;
4. accessibility, usability, performance, compatibility, and content integrity;
5. maintainability or dependency work with a demonstrated cost or risk;
6. research and product ideas with a clear question to answer.

Use concrete evidence: changed code without regression coverage, user-visible breakage, reproducible runtime behavior, contradictory docs, missing operational controls, repeated incident patterns, or explicit PR follow-ups. Exclude vague modernization, aesthetic rewrites, speculative scale work, and duplicate restatements.

Before accepting a candidate, search TODO files, the tracker, open and closed issues, PRs, branches, and recent commits. Reuse or update an existing item whenever it expresses the same outcome.

## 4. Classify and rank

For each candidate, record:

- evidence and affected users or operators;
- desired outcome, bounded scope, and non-goals;
- impact, urgency, confidence, effort, risk, readiness, and dependencies;
- measurable acceptance and verification criteria;
- provenance: PR, review, check, file, test, runtime observation, or user request.

Rank value and safety above novelty. Prefer a small executable batch over an exhaustive wish list. Read [references/opportunity-audit.md](references/opportunity-audit.md) for the scoring rubric, issue shape, and final audit.

## 5. Route each item once

Use one destination per item:

- **Tracker:** Choose high-confidence, intentionally selected work with a useful outcome, bounded acceptance criteria, and a credible verification path. Invocations that explicitly say create, refill, populate, or prepare a burn-ready backlog authorize selecting and writing this bounded batch.
- **TODO:** Keep ideas, research questions, weakly evidenced improvements, future possibilities, and items awaiting a product decision here.
- **Existing PR or issue:** Comment or update only when the user authorized planning writes and the finding belongs to that existing objective. Do not create a duplicate.
- **Discard:** Drop stale, completed, irrelevant, untestable, or purely stylistic candidates.

If the user asks only to inspect, audit, review, or suggest, present the proposed routing without mutating files or trackers.

## 6. Update planning surfaces

### TODO or idea file

Follow the repository's existing format. Create `TODO.md` only when no canonical idea file exists and the repository permits it.

- Add concise candidates with evidence or the question to resolve.
- Preserve existing content and unrelated edits.
- Remove a candidate only after its tracker issue is successfully created or it is proven complete or obsolete.
- A short pointer to the tracker is allowed; do not mirror tracker titles and checklists as a second backlog.

### Authoritative tracker

Follow the declared tracker. Default to Linear for substantial work only when the repository has no other convention; use GitHub Issues only when explicitly declared or requested.

1. Reuse the existing team, project, milestone, labels, and issues.
2. Create or refill one focused milestone for the next burn. Normally select no more than seven issues per repository.
3. Group related findings into shippable outcomes instead of creating one issue per observation.
4. Include evidence, scope, non-goals, acceptance criteria, verification, dependencies, and relevant PR or file links.
5. Represent external blockers truthfully; never invent owner content, credentials, provenance, or release authority.
6. Remove promoted TODO entries only after successful issue creation.

If the required tracker is unavailable, update only the speculative TODO surface, report the tracker blocker, and do not silently substitute another system.

## 7. Verify the created backlog

Re-read modified TODO files and every created or updated tracker object. Confirm:

- each item has exactly one authoritative home;
- no candidate duplicates open work, current PR scope, or completed behavior;
- tracker issues are implementation-ready and independently verifiable;
- speculative ideas were not represented as commitments;
- priorities reflect evidence and dependencies;
- no code, private context, or unrelated local changes were published;
- tracker links, PR links, paths, and remote states are current.

Do not mark implementation issues Done. This skill creates the work; Backlog Burner verifies and completes it.

## 8. Hand off through Backlog Reviewer

Return a compact review-and-burn packet containing:

- repositories and the remote state inspected;
- tracker project, milestone, selected issue identifiers, current states, and issue `updatedAt` or equivalent baseline;
- acceptance and non-goal snapshots that later review can compare without relying on rewritten tracker prose;
- ranked execution order and dependency edges;
- existing branches or PRs that must be reused instead of duplicated;
- expected verification and protected operations;
- external blockers;
- speculative TODO ideas explicitly excluded from the burn;
- preserved local or private artifacts.

Default to a pre-implementation review handoff: `Use $backlog-reviewer in pre-implementation mode to audit this packet.` After the packet passes, use: `Use $backlog-burner to implement the reviewer-approved items in this packet.` Do not silently skip review or invoke another skill unless the user asks to continue.
