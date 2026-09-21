---
name: backlog-burner
description: Reconcile and clear substantial canonical TODO backlogs across one or many Git repositories by discovering authoritative planning sources, syncing chosen work to Linear or the declared tracker before implementation, coordinating Luna-heavy execution in impact-ranked batches, creating safe branches and logical draft PRs, verifying behavior, preserving private or dirty work, and reporting only evidence-backed completion or genuine external blockers. Use when the user asks to burn down, clear, implement, finish, or operationalize a TODO or backlog inventory, especially across multiple repositories.
---

# Backlog Burner

Turn a repository backlog into reviewed, tested draft PRs and truthful tracker state. Optimize for completed work, not closed checkboxes.

## Operating invariants

- Treat Git as code truth, repository Markdown as documentation truth, and the project's declared tracker as committed-work truth.
- Distinguish canonical committed TODOs from ideas, research, generated checklists, and stale duplicate planning surfaces.
- Reconcile the tracker before implementation. Never create parallel Linear and GitHub backlogs.
- Preserve dirty, untracked, private, generated, or user-owned files unless their inclusion is explicitly authorized.
- Never publish private Forge context, local data, credentials, incident artifacts, or unknown media.
- Mark work Done only after acceptance evidence passes. Keep external dependencies open and explicit.
- Open draft PRs. Do not merge, deploy, mutate production data, or execute protected releases without authority.
- Treat a Backlog Reviewer remediation packet as the scope boundary. Reuse its issue, branch, worktree, and PR instead of creating parallel planning or review surfaces.

## 1. Establish authority

For every repository:

1. Read the nearest `AGENTS.md`, `README`, canonical TODO or roadmap, and relevant architecture/development docs.
2. Read matching private Forge `Project.md` and `Scratchpad.md` when available. Use it only as private working context.
3. Inspect Git remotes, default branch, status, worktrees, current branches, recent history, and open PRs.
4. Determine the authoritative tracker from repository declarations. Default to Linear only when no convention exists and the work is substantial.
5. Reconcile repository aliases, renamed remotes, existing projects, milestones, and issues before creating anything.
6. Record uncertainty rather than guessing which of two active trackers is authoritative.

Do not mutate repositories, trackers, or external systems until this authority pass is complete.

When consuming a reviewer packet, confirm it matches the current remote head and tracker history. If an affected issue is incorrectly Done, move it to the appropriate active state and record the missing gate before implementation or protected runtime mutation. Preserve the original acceptance baseline.

## 2. Build the canonical inventory

Scan the supplied inventory document first. If none exists, locate likely planning files with `rg --files`, then inspect only authoritative candidates.

Create a working matrix with:

- repository and canonical path;
- open item count;
- declared tracker and existing project;
- impact, risk, dependencies, and expected verification;
- privacy-sensitive or unknown local files;
- pre-existing objectives that are not part of this burn;
- genuine external requirements such as owner content, credentials, hardware, or protected release authority.

Prefer explicit repository declarations over inferred TODO counts. Do not absorb unrelated `TODO` comments or speculative roadmaps into committed scope.

## 3. Reconcile committed work

For each repository with intentionally selected work:

1. Reuse or create one tracker project and one focused milestone.
2. Promote canonical items into a small number of coherent issues, normally no more than seven per repository.
3. Write measurable acceptance criteria covering implementation, tests, documentation, privacy, and runtime evidence.
4. Link related or pre-existing issues instead of duplicating them.
5. Remove or check repository TODO entries only after the tracker mapping exists.
6. Keep speculative discoveries in `TODO.md`; promote only work intentionally chosen for implementation.

An issue grouping should describe a shippable outcome, not merely mirror every checkbox.

## 4. Lay out execution

Rank repositories by user impact, safety risk, dependency leverage, and readiness. Process them in bounded batches; five batches is a good default for a large inventory.

Create one safe branch per repository before implementation, using the repository's convention and tracker identifiers when appropriate. Use isolated worktrees where concurrent work or dirty state makes that safer.

In remediation mode, prefer the existing reviewed branch and draft PR. Create a new branch only when the packet explicitly requires an independent slice or the original branch is unavailable or unsafe.

### Delegation policy

For multi-repository burns, delegate implementation while the coordinator plans, steers, and performs light review.

- When the user requests the Sol/Luna pattern, use Sol as coordinator and Luna workers for at least 90% of inspection, tracker work, implementation, documentation, tests, Git, and PR work.
- Give each worker explicit repository, file, or outcome ownership. State that other work may be concurrent and existing changes must not be reverted.
- Use a small Luna read-only capability gate before mutations. If Luna or required Git metadata is unavailable, stop that repository and recreate the task or worktree before any write.
- Use Terra only after documenting a concrete Luna insufficiency for a bounded task. Keep Terra below 5% and return its findings to Luna for integration.
- Create user-owned Codex tasks only when the user explicitly asks for per-repository tasks or chats. Otherwise use internal collaboration workers.

Do not duplicate implementation across workers. Reuse an existing worker for follow-up fixes in its owned repository.

## 5. Implement by risk

Within each repository, order work as follows:

1. privacy, authentication, data integrity, destructive operations, and migrations;
2. core correctness and durable persistence;
3. operational reliability, observability, and recovery;
4. user experience, accessibility, performance, and content;
5. optional research or low-impact polish.

Follow existing architecture and conventions. Prefer the smallest maintainable solution and fewer dependencies.

When a discovered defect is narrowly related and necessary for acceptance, fix it and record why. For unrelated defects, capture an idea or intentionally create a follow-up issue; do not silently expand scope.

## 6. Verify continuously

Run focused tests after each logical slice, then the repository's full relevant checks. Add missing deterministic regression coverage for behavior changed by the burn.

Verification can include:

- formatting, lint, type checks, unit, integration, race, dependency, and security tests;
- production builds, container builds, unprivileged runtime smokes, and HTTP checks;
- database migration, backup/restore, schema, and idempotency proof;
- browser, accessibility, static-output, mobile-width, or visual snapshot checks;
- hosted CI when local toolchains cannot provide authoritative evidence.

Inspect generated visual artifacts. A successful renderer that produces blank output is not valid evidence.

Evidence-only remediation is valid when implementation already satisfies acceptance but a real browser, binding, database, hardware, or runtime gate was missing. Do not manufacture an empty commit. Record the environment and result in the existing PR and tracker, verify the branch head remains synchronized, and require the same cleanup and privacy evidence as a code-changing burn.

For disposable external resources, a failed readiness attempt is recovery evidence, not acceptance evidence. Recover exact generated targets, verify absence, then use a fresh bounded run for acceptance. Never weaken the gate merely to accommodate propagation delay.

Never weaken a correct test merely to obtain green CI. Fix implementation semantics unless the expectation is demonstrably wrong.

## 7. Commit and publish reviewable work

Create logical commits with tracker identifiers. Push only intended files and verify the branch tracks its remote.

Open logical draft PRs with:

- outcome-oriented summary;
- exact verification evidence;
- tracker links or identifiers;
- explicit external blockers and protected operations not performed;
- privacy or artifact exclusions where relevant.

Prefer one coherent PR per repository unless independent slices materially improve reviewability. Use an integration PR when multiple component branches must be reviewed together.

## 8. Close the loop

Before marking issues or projects complete:

1. audit every canonical item against files, tests, runtime evidence, tracker state, commits, and PRs;
2. inspect the actual remote PR head rather than a stale main checkout;
3. verify every PR is open, draft, mergeable, and synchronized;
4. verify hosted checks, distinguishing code failures from external authorization or runner constraints;
5. restore truthful issue state for anything requiring owner input, credentials, hardware, protected release authority, or provenance;
6. update existing Forge status or handoff context when the project's private status materially changed;
7. confirm unknown/private artifacts remain unpublished.
8. for remediation burns, verify tracker history shows the issue active before mutation and Done only after the missing gate passed;
9. accept a no-new-commit result only when the existing remote head plus new external evidence satisfies every criterion.

Read [references/completion-audit.md](references/completion-audit.md) before the final multi-repository audit or report.

## Completion rule

Call the burn complete only when all feasible implementation is verified and every remaining item is one of:

- an explicit external dependency with an active tracker issue;
- a pre-existing objective outside the selected inventory;
- a speculative idea that was never committed to this burn.

Do not represent those categories as implemented. Report them separately with the exact next authority or input required.

## Final response

Lead with the cross-repository outcome. Include:

- repositories, branches, draft PRs, and tracker states;
- concise verification highlights;
- remaining external dependencies and pre-existing non-batch work;
- protected or private artifacts intentionally preserved;
- delegation mix, including whether Terra was needed;
- created task links when the user requested per-repository tasks.

Keep the report compact enough to act on. Link directly to PRs and tracker issues instead of reproducing their full contents.
