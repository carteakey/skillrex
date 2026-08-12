# Backlog review gates

Use this reference for both pre-implementation readiness and post-implementation completion reviews.

## Pre-implementation scorecard

Score each dimension from 0 to 2:

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Authority | Conflicting or absent source | Authority inferred | Explicit single source |
| Currency | Stale or already complete | Partially checked | Verified on current remote state |
| Evidence | Opinion only | Indirect signal | Reproducible or source-linked evidence |
| Deduplication | Duplicate likely | Search incomplete | Tracker, PR, branch, TODO, and history checked |
| Outcome | Task phrasing only | Outcome implied | User/operator outcome and non-goals explicit |
| Scope | Unbounded or coupled | Some boundaries | Small coherent reviewable slice |
| Dependencies | Hidden | Partially named | Sequenced with owners and protected gates |
| Priority | Arbitrary | Qualitative | Impact, urgency, confidence, risk, effort, readiness |
| Acceptance | Checkbox or subjective | Partly observable | Measurable success and failure conditions |
| Verification | Generic “tests pass” | Focused checks only | Risk-matched focused, full, and runtime evidence |
| Privacy/safety | Unaddressed | General warning | Exact data, secret, destructive, and publication bounds |
| Execution shape | No branch/PR strategy | Plausible | Safe base, isolation, logical commits, review topology |

Verdict guidance:

- **Ready:** no zeroes; authority, evidence, scope, acceptance, verification, and privacy all score 2.
- **Ready with conditions:** no zeroes in authority/scope/acceptance/privacy; named prerequisite or approval remains.
- **Needs revision:** any critical dimension scores 0 but can be corrected locally.
- **Blocked:** required owner input, credential, provenance, hardware, permission, or decision is unavailable.
- **Reject or reroute:** duplicate, completed, speculative, stale, or part of an existing PR objective.

Scores support judgment; do not average away a critical zero.

## Acceptance-criterion test

A strong criterion identifies:

1. actor or affected system;
2. observable behavior or state transition;
3. important bounds and negative behavior;
4. evidence source;
5. environment when semantics depend on one;
6. cleanup, rollback, or recovery for destructive/durable operations.

Reject criteria that merely say implement, support, improve, handle, document, test, production-ready, secure, accessible, performant, or robust without an observable condition.

## Verification depth by risk

| Change type | Minimum credible evidence |
| --- | --- |
| Pure docs | Link/path validation, factual comparison, formatting/build if rendered |
| Logic or API | Focused regression, full unit/type/lint, negative paths |
| UI | Build, interaction contract, keyboard/mobile/accessibility, browser or inspected snapshot |
| Auth/privacy | Unauthorized/wrong/right paths, secret-safe logging, publication audit |
| Persistence/migration | Real store/schema test, replay/idempotency, rollback or backup evidence |
| Destructive admin | Preview, bounds, confirmation, partial failure, idempotency, residual audit |
| External binding | Disposable real-binding smoke plus exact teardown when mocks cannot prove semantics |
| Deployment/service | Clean artifact, start/restart, health, relevant Tailscale URL, rollback boundary |
| Hardware/model/data | Target environment evidence, provenance/licensing, resource bounds, owner authority |

## Post-implementation evidence matrix

For each issue record:

| Field | Required evidence |
| --- | --- |
| Baseline | Issue version and acceptance before implementation |
| Remote state | PR URL, base/head SHA, draft/open, mergeability, current reviews/checks |
| Implementation | Changed files and behavior mapped to each acceptance criterion |
| Regression | Focused tests that fail without the fix and cover negative paths |
| Full verification | Repository-standard lint/type/test/build and relevant hosted checks |
| Runtime/artifacts | Actual environment or inspected visual evidence where required |
| Documentation | Public behavior/config/recovery/release docs match implementation |
| Privacy | No secrets, private data/context, unknown media, or local-only paths published |
| Preservation | Dirty/untracked/concurrent user work unchanged |
| Tracker truth | Issue/milestone/project state matches remaining acceptance |

A draft or unmerged PR may still pass an implementation review. Block completion only for actionable unresolved findings, failed/current checks, merge-dependent acceptance, release policy, or behavior that cannot be evidenced before merge or deployment.

## Red flags that reject completion

- The PR head differs from the SHA that was tested or reviewed.
- CI is green only because a meaningful step is non-blocking, skipped, or weakened.
- Tests assert implementation details or mocks unrelated to the promised behavior.
- Acceptance criteria were edited after implementation to match what happened.
- A destructive flow lacks preview, bounds, confirmation, retry/idempotency, or residual proof.
- A browser, binding, database, hardware, model, or deployment claim relies only on unit mocks.
- Visual artifacts were generated but never inspected.
- Documentation promises behavior not present in code or validated at runtime.
- Private context, user data, credentials, recordings, models, or unknown media entered the branch.
- An external dependency is described as a follow-up even though it is part of committed acceptance.
- Tracker Done state is based on code presence while the risky runtime gate remains unverified.
- Ordinary review or merge is treated as a blocker despite not being part of acceptance or repository policy.

## Drift ledger

For a before/after review, classify every difference:

| Classification | Meaning | Required response |
| --- | --- | --- |
| Justified | New evidence changed the safe approach without weakening outcome | Update issue/PR rationale and verify replacement evidence |
| Unresolved | Acceptance or verification is still missing | Keep issue active and name the exact gate |
| Scope creep | Work unrelated to the approved outcome entered the batch | Remove, split, or explicitly authorize it |
| Superseded | External change made the objective unnecessary or invalid | Close with evidence; do not claim implementation |

## Review packet template

Start with counts: repositories, issues, PRs, pre-ready items, post-passing items, blockers, and planning repairs applied.

| Repository | Issue / PR | Phase | Verdict | Evidence | Missing / next action |
| --- | --- | --- | --- | --- | --- |

Finish with separate sections for blockers, committed non-blocking follow-ups, excluded opportunities, and preserved private artifacts.
