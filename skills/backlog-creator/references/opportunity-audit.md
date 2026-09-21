# Opportunity audit

Use this reference while ranking candidates and before reporting a created backlog.

## Current-state matrix

| Field | Required evidence |
| --- | --- |
| Repository | Local path, canonical remote, default branch, and current remote SHA |
| PR horizon | Every open PR plus the bounded recent merged range inspected |
| PR state | Head SHA, linked objective, review threads, checks, merge state, and follow-up signals |
| Planning | Canonical TODO surface, declared tracker, project, milestone, existing issue matches, and current reviewer verdicts |
| Product state | Release, runtime, docs, tests, operational signals, and user-visible behavior examined |
| Safety | Dirty/private artifacts, protected operations, and external authority boundaries |

## Evidence bar

Accept a candidate when at least one source directly supports the problem or opportunity and a second source confirms scope or verification when practical.

Strong sources include:

- reproducible behavior or runtime output;
- a current failed test, check, or unresolved review finding;
- changed production code lacking coverage for a meaningful behavior;
- a contradiction among code, public docs, schemas, or release behavior;
- a linked PR follow-up or explicit stakeholder request;
- repeated operational failure with logs or incident evidence.

Weak sources include generic TODO comments, age alone, dependency freshness alone, aesthetic preference, hypothetical scale, or architecture fashion. Keep these speculative or discard them unless corroborated.

## Ranking rubric

Score each dimension from 1 to 5. Use scores for ordering, not false precision.

| Dimension | A high score means |
| --- | --- |
| Impact | Material user, privacy, correctness, or operator benefit |
| Urgency | Active breakage, exposure, deadline, or blocking dependency |
| Confidence | Direct, current, reproducible evidence |
| Readiness | Scope, owner, dependencies, and verification are clear |
| Effort | Small enough to complete safely in a bounded burn |
| Risk | High implementation or rollout risk; subtract from priority |

A useful ordering heuristic is `(impact + urgency + confidence + readiness + effort) - risk`. Override the number when dependency order, data safety, or external authority requires it.

## Candidate disposition

For every finding choose exactly one:

| Disposition | Use when |
| --- | --- |
| Existing objective | It is already covered by an active PR or issue |
| Tracker commitment | It is intentionally selected, bounded, valuable, and verifiable |
| TODO idea | It is speculative, research-oriented, weakly evidenced, or awaiting a decision |
| Discard | It is stale, completed, duplicated, irrelevant, or has no useful outcome |

Never use a new issue to mirror a failing open PR. Fixing or completing that PR remains its existing objective unless the follow-up is independently shippable.

## Tracker issue shape

Write each burn-ready issue with:

1. **Outcome** — the user or operator result.
2. **Evidence** — current PR, check, review, path, test, runtime, or documentation proof.
3. **Scope** — bounded components and behavior.
4. **Non-goals** — adjacent work intentionally excluded.
5. **Acceptance criteria** — observable implementation requirements.
6. **Verification** — focused regression plus relevant full checks, build, runtime, visual, migration, or hosted evidence.
7. **Dependencies and safety** — sequencing, external input, privacy, migration, deploy, or protected-operation limits.

Group observations only when one implementation and verification story covers them. Split issues when they have different risk, dependencies, owners, or release paths.

## TODO entry shape

Keep entries concise and explicitly non-committal:

```markdown
- Investigate <question or opportunity>. Evidence: <current source>. Decide: <unknown that blocks commitment>.
```

Do not paste the tracker issue body into the TODO. After promotion, remove the entry and optionally retain one repository-level pointer to the authoritative tracker.

## Final deduplication audit

1. Search candidate phrases and synonyms across TODO files, Linear, GitHub Issues, PRs, branches, and recent commits.
2. Re-read actual remote PR heads and current check suites.
3. Verify selected issues are not already satisfied on another branch or PR.
4. Verify every TODO removal has a successful tracker destination.
5. Verify every issue has evidence, acceptance criteria, and a feasible verification path.
6. Verify external blockers remain open and name the required owner or authority.
7. Inspect the local diff and remote writes for private or unrelated content.

## Review-and-burn packet template

Start with totals: repositories scanned, PRs inspected, tracker issues created or reused, TODO ideas added, duplicates avoided, and external blockers.

Then use one row per repository:

| Repository | Remote state | Tracker baseline | Next-burn milestone | Ranked issues | TODO-only ideas |
| --- | --- | --- | --- | --- | --- |
| Example | `main@abc123`; 2 open / 5 recent merged PRs | `ABC-12` Todo at `<updatedAt>`; acceptance snapshot recorded | Project / Milestone | `ABC-12`, `ABC-15` | 3 speculative ideas |

Finish with:

1. dependency-aware burn order;
2. acceptance and verification highlights;
3. external inputs or protected operations;
4. preserved private or dirty artifacts;
5. a ready-to-run pre-implementation `$backlog-reviewer` prompt;
6. after review passes, a `$backlog-burner` prompt naming only the approved scope.
