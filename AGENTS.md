# Development Philosophy

Optimize for simplicity.

- Git is the source of truth for code.
- Markdown is the source of truth for documentation.
- Each project has one source of truth for committed planned work: Linear when the project uses Linear, or GitHub Issues when the repository explicitly uses GitHub planning.
- Avoid creating process for its own sake.

Prefer existing conventions over inventing new ones.

Do not maintain parallel backlogs in Linear and GitHub Issues.

---

## Before Starting Work

1. Read the repository README and any relevant documentation.
2. Determine whether the project uses Linear, GitHub Issues, or no formal issue tracker. Follow the existing convention and do not introduce a tracker for trivial work.
3. When choosing what to work on:
   - If Linear is the planning system and Linear MCP is available, find the active project, read the current milestone, and review the highest-priority open issues.
   - If GitHub Issues is the planning system, use `gh` when it is sufficient.
4. When given a specific task:
   - Treat an explicit implementation request as intentionally chosen work.
   - Read the relevant issue, milestone, comments, and related issues only as needed.
   - If substantial work in a project with a chosen tracker has no issue, suggest creating one there, but do not block implementation solely because an issue is absent unless repository conventions require one.
5. Do not start implementing until the problem is understood.

---

## TODO.md vs Issue Trackers

`TODO.md` is for thinking.

Store:

- ideas
- research
- questions
- future possibilities
- rough notes

Linear—or GitHub Issues in a repository that explicitly uses it—is for commitments.

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
