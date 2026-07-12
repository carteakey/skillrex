# Development Philosophy

Optimize for simplicity.

- Git is the source of truth for code.
- Markdown is the source of truth for documentation.
- Each project has one source of truth for committed planned work. Linear is the default during the current trial; GitHub Issues is used only when the repository explicitly chooses GitHub planning.
- Avoid creating process for its own sake.

Prefer existing conventions over inventing new ones.

Do not maintain parallel backlogs in Linear and GitHub Issues.

---

## Choosing Linear or GitHub

Follow the project's existing declared convention first.

If no convention exists, default to Linear for substantial, intentionally chosen development work. This applies to single-repository work as well as cross-repository planning so Linear receives a fair trial.

Choose GitHub Issues instead only when:

- The repository already declares GitHub Issues as its planning system.
- The user explicitly requests a GitHub-native workflow.
- The work must be public or contributor-facing in GitHub.

Use neither tracker for trivial or one-off work that does not benefit from tracking.

If Linear is unavailable, say so and continue without silently switching the project to GitHub Issues. Do not let tracker availability block explicitly requested implementation work.

GitHub Projects may organize GitHub Issues, but it is a view of the work rather than a second backlog.

If both Linear and GitHub Issues already contain active work and no authority is declared, ask which one is authoritative before creating or updating issues. Do not copy or migrate items without an explicit request.

---

## Before Starting Work

1. Read the repository README and any relevant documentation.
2. Check Forge at `/Users/kchauhan/wikis/forge` for private project context:
   - Look for `projects/<repository-name>/Project.md` first.
   - If the directory name differs, search Forge project frontmatter for the repository's absolute path in `repo` or `local_path`.
   - Read the matching `Project.md`, `Scratchpad.md`, and only the additional notes relevant to the current task.
   - If no matching Forge project exists, continue normally; do not create one for trivial or speculative work unless the user asks.
3. Determine whether the project uses Linear, GitHub Issues, or no formal issue tracker. Follow the existing convention and do not introduce a tracker for trivial work.
4. When choosing what to work on:
   - If Linear is the planning system and Linear MCP is available, find the active project, read the current milestone, and review the highest-priority open issues.
   - If GitHub Issues is the planning system, use `gh` when it is sufficient.
5. When given a specific task:
   - Treat an explicit implementation request as intentionally chosen work.
   - Read the relevant issue, milestone, comments, and related issues only as needed.
   - If substantial work in a project with a chosen tracker has no issue, suggest creating one there, but do not block implementation solely because an issue is absent unless repository conventions require one.
6. Do not start implementing until the problem is understood.

---

## TODO.md vs Issue Trackers

`TODO.md` is for thinking.

Store:

- ideas
- research
- questions
- future possibilities
- rough notes

Linear is the default for commitments. GitHub Issues serves that role only in a repository that explicitly chooses it.

Create or update an issue only when work has been intentionally chosen for implementation. An explicit implementation request counts as an intentional choice.

Do not create issues for speculative ideas.

When an idea in `TODO.md` becomes an active objective, remove it from `TODO.md` and create an issue in the project's chosen tracker.

Do not duplicate the same item across `TODO.md`, Linear, and GitHub Issues.

---

## Personal Tasks

Keep personal obligations outside development planning systems unless explicitly requested otherwise. Use the designated personal task manager for them.

Do not choose a personal task manager solely because it supports MCP; prioritize capture, reminders, recurrence, and everyday usability.

---

## During Implementation

- Keep changes focused on the current issue.
- Follow the existing architecture and coding style.
- Prefer simple, maintainable solutions.
- Avoid unnecessary abstractions.
- If unrelated problems are discovered, do not expand scope. Record speculative ideas in `TODO.md`; create follow-up issues only for intentionally committed work.

---

## Documentation

Update documentation whenever behavior or architecture changes.

Prefer:

- `README.md`
- `ARCHITECTURE.md`
- `DECISIONS.md`

Avoid duplicating information across multiple files.

### Forge: Private Project Context

Forge at `/Users/kchauhan/wikis/forge` is the private working layer for development projects.

Use Forge for:

- private or pre-publication specifications
- working ideas and exploratory designs
- active project scratchpads
- agent handoffs and investigation notes
- links to the repository, Linear, Notion, documentation, and other project systems
- context that is valuable to future agents but does not belong in the public repository

Source-of-truth boundaries:

- The repository remains authoritative for code, public/canonical documentation, architecture, and checked-in decisions.
- The project's declared tracker remains authoritative for committed work.
- Forge is authoritative only for private working context and project pointers.
- Generic technical notes remain in `vault-76`, not Forge.

Privacy and publication rules:

- Do not copy Forge content into a repository, issue, pull request, public documentation, or external service unless the user explicitly requests it.
- Treat Forge notes as private by default even when the project repository is public.
- Never store secrets, credentials, tokens, recovery codes, or private production data in Forge.
- Prefer links and concise context over duplicating repository documentation or tracker items.

When a matching Forge project already exists and implementation materially changes its status, next action, or private working context, update its `Project.md` or `Scratchpad.md` as part of the work. Do not create a parallel backlog there.

---

## Git Workflow

Use Git locally.

Write clear commit messages.

When working on a tracked issue, reference its identifier in the branch name and commit message when appropriate.

Example branch:

```text
feature/ED-42-stamina
```

Example commit:

```text
ED-42 Implement stamina regeneration
```

---

## After Completing Work

If the work is associated with an issue in the project's chosen tracker:

- Update the issue with a concise implementation summary.
- Record important design decisions.
- Mention any intentionally committed follow-up work.
- Move the issue to Done only when the requested work is complete and relevant verification has passed.

Then summarize:

- What changed
- Files modified
- Testing performed
- Remaining work

---

## Decision Making

When multiple approaches exist:

1. Prefer the simplest solution.
2. Prefer fewer dependencies.
3. Prefer standard library over third-party packages.
4. Prefer explicit code over clever code.
5. Optimize for maintainability rather than novelty.

---

## Tooling Philosophy

Prefer the simplest interface capable of completing the task.

Typical preference order:

- Local files
- Git
- CLI tools
- MCP
- Web APIs

Examples:

- Git → local Git
- GitHub → `gh` CLI when sufficient
- Docker → Docker Compose / CLI
- Linear → Linear MCP

Do not treat MCP or CLI as categorically better. Prefer a mature local or CLI interface when it is simpler; use MCP when its structured remote context or actions materially reduce friction.

Do not choose a tool solely because it supports MCP.

Do not introduce additional infrastructure unless it meaningfully reduces long-term complexity.

---

## Communication

When beginning a session:

- Briefly summarize your understanding of the current task.
- Call out any assumptions.

When finishing:

- Summarize completed work.
- Identify any remaining blockers.
- Suggest the next logical task from the project's chosen planning system if available.
