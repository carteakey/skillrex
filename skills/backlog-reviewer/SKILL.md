---
name: backlog-reviewer
description: Audit development backlogs both before implementation and after implementation across one or many Git repositories. Before work starts, verify authority, evidence, scope, duplicates, dependencies, priority, acceptance criteria, verification plans, privacy, and burn readiness. After work lands, compare actual remote PR heads, code, tests, runtime evidence, documentation, and tracker state against the committed backlog and decide whether completion is justified. Use when the user asks to review, audit, critique, validate, reconcile, quality-check, approve, or sign off a backlog, milestone, burn packet, implementation batch, pull request set, or claimed completion. This skill reviews and may repair planning hygiene when explicitly requested; it does not implement product work.
---

# Backlog Reviewer

Act as the independent quality gate around backlog creation and implementation. Review the plan before execution, the evidence after execution, or both. Do not implement the backlog.

## Operating invariants

- Treat Git as code truth, repository Markdown as documentation truth, and the declared tracker as committed-work truth.
- Inspect actual remote branches, PR heads, checks, reviews, and tracker objects; never rely on a stale checkout or summary alone.
- Keep ideas and commitments separate. Do not duplicate work across TODO files, Linear, and GitHub Issues.
- Preserve dirty, untracked, private, generated, and user-owned files. Never publish Forge context, local data, credentials, incident artifacts, recordings, models, or unknown media.
- Distinguish missing implementation from an external dependency, protected operation, superseded objective, or speculative idea.
- Demand evidence proportional to risk. A checkbox, tracker comment, green mock test, or successful renderer is not sufficient by itself.
- Default to read-only for requests framed as review, audit, critique, validate, or sign-off.
- Modify TODO or tracker state only when the user explicitly asks to reconcile, repair, update, or apply review findings. Never edit product code, open implementation branches, merge, deploy, or mutate production under this skill.

## 1. Select the review mode

Infer one of three modes from the request:

- **Pre-implementation:** Review a TODO, issue set, milestone, plan, or burn packet before work begins.
- **Post-implementation:** Review PRs, branches, commits, tracker claims, or a completed burn after work is reported done.
- **Full lifecycle:** Establish the pre-implementation baseline, then compare the delivered result with it.

If the phase is ambiguous, inspect the repository and tracker state. Review both when a backlog already has implementation attached. State the selected mode and mutation boundary before acting.

## 2. Establish authority and evidence scope

For each repository:

1. Read the nearest `AGENTS.md`, `README`, canonical planning file, and relevant architecture, development, release, and decision docs.
2. Read matching Forge `Project.md` and `Scratchpad.md` only as private context.
3. Inspect remotes, default branch, status, worktrees, branches, recent history, releases, and open PRs.
4. Determine the declared tracker. If Linear and GitHub Issues are both active without an authority declaration, stop planning writes and report the ambiguity.
5. Reconcile repository aliases, tracker projects, milestones, issues, linked PRs, and recent merged work.
6. Record dirty/private exclusions and protected operations before evaluating readiness or completion.

Bound the review to the supplied backlog or implementation batch. Route unrelated opportunities to Backlog Creator rather than expanding this review.

## 3. Run the pre-implementation gate

Build a candidate ledger and challenge each committed item:

- **Authority:** Does it live in exactly one committed-work system?
- **Currency:** Is it still unsolved on the latest default branch and open PR heads?
- **Evidence:** Is the problem supported by code, tests, runtime behavior, documentation, review feedback, an incident, or an explicit user decision?
- **Deduplication:** Does an existing issue, PR, branch, TODO entry, or completed change already express the same outcome?
- **Outcome and scope:** Is the user/operator outcome clear, bounded, and separated from non-goals?
- **Dependencies:** Are prerequisite PRs, owner content, credentials, hardware, data provenance, decisions, and protected operations explicit?
- **Priority:** Do impact, urgency, confidence, risk, effort, and readiness support the proposed order?
- **Acceptance:** Are criteria observable and resistant to checkbox-only completion?
- **Verification:** Are focused tests, full checks, build, runtime, migration, browser, accessibility, visual, security, privacy, or recovery evidence specified as appropriate?
- **Execution shape:** Can it be implemented and reviewed coherently without hidden coupling or oversized branches?

Use [references/review-gates.md](references/review-gates.md) for the detailed rubric and verdict rules.

Return one verdict per item:

- **Ready:** Can enter Backlog Burner unchanged.
- **Ready with conditions:** Executable after named prerequisites or protected approvals.
- **Needs revision:** Valuable but scope, evidence, acceptance, priority, or verification is insufficient.
- **Blocked:** Cannot start safely because a required external input or authority is absent.
- **Reject or reroute:** Duplicate, complete, stale, speculative, or belongs in an existing PR/TODO rather than committed work.

Do not approve the batch merely because every issue has prose. The batch is burn-ready only when sequencing, verification, and protected boundaries are coherent as a whole.

## 4. Run the post-implementation gate

Treat the pre-approved issue and acceptance criteria as the baseline. If no baseline review exists, reconstruct it from the tracker state and issue history that predated implementation.

For every claimed result:

1. Resolve the actual remote PR head, base, commit range, changed files, reviews, unresolved threads, and current checks. Treat actionable unresolved review findings as evidence; do not treat draft/open/unmerged state by itself as incomplete unless merge or release is part of acceptance or repository policy.
2. Map each acceptance criterion to concrete code, tests, documentation, runtime or visual evidence, and tracker evidence.
3. Verify the implementation did not silently narrow, reinterpret, or remove acceptance criteria after work began.
4. Inspect test quality: meaningful changed behavior, negative and failure paths, determinism, appropriate integration boundaries, and no weakened gate.
5. Require runtime or artifact evidence when semantics depend on a browser, operating system, external binding, database, migration, hardware, network service, model, or deployment environment.
6. Inspect generated visual artifacts rather than accepting renderer success; reject blank, clipped, uniform, or misleading output.
7. Audit privacy and publication: secrets, credentials, local paths, private metadata, recordings, user data, Forge context, unknown media, and generated artifacts must stay excluded.
8. Check documentation, configuration examples, changelog/release state, and rollback or recovery instructions against actual behavior.
9. Verify tracker issue, milestone, and project states are truthful. External dependencies remain open even when scaffolding exists.
10. Confirm original dirty/private work and unrelated branches were preserved.
11. Distinguish missing code from missing evidence. A real runtime, browser, binding, or artifact gate may close the gap without a code change or empty commit.

Return one verdict per issue or PR:

- **Pass:** Implementation acceptance is fully evidenced and Done is justified, even if a draft PR still awaits ordinary review or merge that was not part of acceptance.
- **Conditional pass:** Implemented scope passes, but an explicitly separate non-blocking follow-up, merge, release, or rollout remains.
- **Not complete:** One or more committed acceptance gates lack evidence or failed.
- **Blocked after implementation:** Code is ready, but required external validation or authority still blocks completion.
- **Superseded or invalid:** The delivered work no longer corresponds to a valid objective.

Never call an issue complete when the missing evidence is the risky part of the issue.
Do not make merge, deployment, or release a hidden completion criterion. Require it only when the backlog, repository policy, or behavior under review explicitly depends on it.

## 5. Audit lifecycle drift

In full-lifecycle mode, compare before and after explicitly:

- issue scope and non-goals;
- acceptance criteria added, removed, or edited;
- dependency and sequencing changes;
- implementation files and PR topology;
- planned versus actual verification;
- risk discovered during CI or runtime validation;
- tracker and documentation state;
- protected operations performed or deferred.

Classify every deviation as justified, unresolved, or scope creep. A justified deviation needs evidence and an updated tracker or PR explanation.

## 6. Apply review repairs only when authorized

When the user asks to reconcile or fix review findings, make the smallest planning-only corrections:

- update existing issue evidence, scope, acceptance, dependencies, links, priority, or state;
- remove or reroute duplicate and stale TODO/tracker entries;
- restore an incorrectly completed issue to an active or blocked state;
- attach current PRs, commits, checks, or runtime evidence;
- split an oversized objective only when its independent outcomes are already intentionally committed;
- update an existing Forge handoff when private project status materially changed.

Do not create speculative follow-up issues. Do not fix product code under this skill. Hand implementation findings to Backlog Burner and new unrelated opportunities to Backlog Creator.

After writes, re-read every modified object and verify no parallel backlog or accidental publication was created.

For every **Needs revision**, **Not complete**, or **Blocked after implementation** verdict, produce a bounded remediation packet for Backlog Burner. Include:

- issue identifier, current state, baseline acceptance, and missing evidence;
- exact existing branch, worktree, and PR to reuse;
- allowed implementation or evidence scope and explicit non-goals;
- verification environment, protected operations, cleanup, and privacy boundaries;
- the state transition required before mutation and the evidence required before returning to Done;
- whether an evidence-only repair with no new commit is acceptable.

When tracker reconciliation is authorized, move an incorrectly Done issue to the appropriate active state and record the gap before implementation begins. Do not rewrite acceptance criteria to match the eventual result.

## 7. Produce the review packet

Lead with the overall gate:

- **Pre:** burn-ready, conditionally ready, or not ready.
- **Post:** completion justified, partially justified, or rejected.
- **Full lifecycle:** planned scope delivered, drift requiring action, and truthful remaining dependencies.

Then provide a compact matrix with repository, issue/PR, verdict, strongest evidence, missing evidence, dependency, and required action. For failed gates, append the bounded remediation packet rather than leaving Backlog Burner to rediscover scope. Separate:

1. blocking findings;
2. non-blocking follow-ups already committed;
3. speculative or unrelated opportunities routed to Backlog Creator;
4. protected/private artifacts preserved.

End with one actionable handoff:

- `Use $backlog-burner to implement the items marked Ready from this reviewed baseline.`
- `Use $backlog-burner in remediation mode on the failed gates in this packet, then rerun $backlog-reviewer in post-implementation mode.`
- `Use $backlog-creator to investigate the unrelated opportunities excluded from this review.`

Do not automatically invoke another skill unless the user asks to continue.
