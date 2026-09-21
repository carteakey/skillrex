# Completion audit

Use this checklist for the final cross-repository pass. Audit remote review heads, not whichever local checkout happens to be open.

## Repository evidence matrix

For each repository record:

| Field | Required evidence |
| --- | --- |
| Scope | Canonical TODO paths and original open-item count |
| Authority | Declared tracker, project, milestone, and issue identifiers |
| Branch | Branch name, remote tracking state, and intended commit range |
| PR | Draft URL, base/head, open state, and mergeability |
| Implementation | Files or components satisfying each grouped issue |
| Verification | Focused tests, full checks, builds, runtime or visual evidence |
| Privacy | Unknown, private, generated, or local-only files excluded |
| Remaining | Exact external dependency or pre-existing non-batch objective |
| Remediation | Reviewer verdict, pre-mutation tracker state, reused PR/head, and whether code changed |

## Canonical TODO audit

1. Search every canonical TODO path on the PR head for unchecked boxes or unpromoted plain-list entries.
2. Map every remaining line to an active issue and state why it cannot be completed locally.
3. Check that completed lines have implementation evidence, not only tracker comments or documentation.
4. Confirm migrated TODO files point to the authoritative tracker without maintaining a second backlog.
5. Keep speculative or research-only files separate from the committed inventory.

## Tracker audit

For each project:

- list all issues and summarize states;
- distinguish issues created for this burn from older project objectives;
- verify acceptance comments link commits, PRs, tests, or runtime proof;
- mark the milestone complete only when all issues in its intended scope are Done;
- leave the broader project active when unrelated pre-existing work remains;
- avoid declaring an externally blocked issue Done merely because implementation scaffolding exists.

## Git and PR audit

Verify:

- branch and remote head SHAs match;
- intended work is committed and pushed;
- no user files were accidentally staged or published;
- each PR is open, draft, and mergeable;
- PR bodies describe the final head rather than an earlier validation state;
- required CI is green, or its external failure is precisely identified;
- integration PRs include the latest component fixes.
- evidence-only repairs do not contain empty commits and record the unchanged tested head;
- failed disposable attempts have exact recovery evidence and are not counted as acceptance runs.

For repositories without hosted checks, retain exact local commands and results in the PR body and tracker comment.

## Verification quality

Reject evidence when:

- tests only exercise mocks unrelated to the changed behavior;
- a production build was never attempted despite being available;
- a destructive flow lacks preview, bounds, confirmation, idempotency, or partial-failure tests;
- visual snapshots are blank, uniform, clipped beyond usefulness, or never inspected;
- CI is green only because a meaningful gate was made non-failing;
- sensitive fixtures or production data entered the branch.

For reviewer-driven remediation, also reject completion when the issue stayed Done during mutation, the original acceptance baseline was rewritten, or a new issue/PR duplicated the reviewed objective.

Prefer a narrow regression for every defect found during hosted or runtime verification.

## Final report template

Start with totals:

- repositories processed;
- draft PRs opened;
- completed milestones;
- active external blockers;
- delegation mix.

Then report one compact row per repository:

| Repository | Draft PR | Tracker result | Verification |
| --- | --- | --- | --- |
| Example | PR link | Milestone complete; older issue remains active | Unit, build, runtime smoke |

Finish with three separate lists:

1. **External dependencies** — required user content, credentials, hardware, protected release authority, or third-party permissions.
2. **Pre-existing non-batch work** — active work that was not part of the selected canonical inventory.
3. **Preserved local/private artifacts** — dirty or untracked material deliberately excluded from commits.

Never collapse these categories into a vague “remaining work” statement.
