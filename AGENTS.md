# Development Philosophy

Optimize for simplicity.

- Git is the source of truth for code.
- Markdown is the source of truth for documentation.
- Linear is the source of truth for planned work.
- Avoid creating process for its own sake.

Prefer existing conventions over inventing new ones.

---

## Before Starting Work

1. Read the repository README and any relevant documentation.
2. If Linear MCP is available:
   - Find the active project.
   - Read the current milestone.
   - Review the highest-priority open issue.
   - Understand related issues before making changes.
3. If no suitable issue exists, suggest creating one before beginning substantial work.
4. Do not start implementing until the problem is understood.

---

## TODO.md vs Linear

`TODO.md` is for thinking.

Store:

- ideas
- research
- questions
- future possibilities
- rough notes

Linear is for commitments.

Create or update a Linear issue only when work has been intentionally chosen for implementation.

Do not create Linear issues for speculative ideas.

When an idea in `TODO.md` becomes an active objective, remove it from `TODO.md` and create a Linear issue.

Do not duplicate the same item in both places.

---

## During Implementation

- Keep changes focused on the current issue.
- Follow the existing architecture and coding style.
- Prefer simple, maintainable solutions.
- Avoid unnecessary abstractions.
- If unrelated problems are discovered, create follow-up issues instead of expanding scope.

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

When working on a Linear issue, reference its identifier in the branch name and commit message when appropriate.

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

If Linear MCP is available:

- Update the issue with a concise implementation summary.
- Record important design decisions.
- Mention any follow-up work.
- Move the issue to Done only when the requested work is complete.

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

Do not introduce additional infrastructure unless it meaningfully reduces long-term complexity.

---

## Communication

When beginning a session:

- Briefly summarize your understanding of the current task.
- Call out any assumptions.

When finishing:

- Summarize completed work.
- Identify any remaining blockers.
- Suggest the next logical task from Linear if available.
