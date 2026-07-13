---
name: github-workflow
description: "Comprehensive guide for GitHub operations: Authentication, Repositories, Issues, and PRs"
---

# GitHub Workflow Management

A unified guide for managing the entire GitHub lifecycle, from authentication and repository setup to issue tracking and pull request workflows.

## 1. Authentication

Ensure you have access to GitHub before performing operations.

### GitHub CLI (gh) Authentication
If `gh` is installed, it is the recommended method.
```bash
# Interactive login
gh auth login

# Headless login (with token)
echo "<YOUR_TOKEN>" | gh auth login --with-token

# Verify status
gh auth status
```

### Git-Only Authentication (HTTPS/SSH)
Use this if `gh` is not available.

#### HTTPS with Personal Access Token (PAT)
1. Generate a PAT at https://github.com/settings/tokens (Scopes: `repo`, `workflow`, `read:org`).
2. Configure git to cache credentials:
   ```bash
   git config --global credential.helper store
   ```
3. Perform a git operation to trigger the prompt, then enter your username and PAT as the password.

#### SSH Key Authentication
1. Generate a key: `ssh-keygen -t ed25519 -C "your-email@example.com"`
2. Add the `.pub` content to https://github.com/settings/keys.
3. Test: `ssh -T git@github.com`

---

## 2. Repository Management

### Cloning and Creating
```bash
# Clone a repository
git clone https://github.com/owner/repo.git

# Create a new repository (via gh)
gh repo create my-new-project --public --clone

# Create a repository from a template
gh repo create my-app --template owner/template-repo --public --clone
```

### Forking and Syncing
```bash
# Fork a repository
gh repo fork owner/repo --clone

# Sync a fork
gh repo sync owner/repo
```

### Repository Settings and Secrets
```bash
# Edit description
gh repo edit --description "New description"

# Manage secrets (GitHub Actions)
gh secret set API_KEY --body "your-secret-value"
gh secret list
```

### Releases
```bash
# Create a release
gh release create v1.0.0 --title "v1.0.0" --generate-notes
```

---

## 3. Issue Management

### Viewing and Searching
```bash
# List open issues
gh issue list --state open

# Search issues
gh issue list --search "authentication error"

# View a specific issue
gh issue view 42
```

### Creating and Managing
```bash
# Create an issue
gh issue create --title "Bug: login fails" --body "Detailed description" --label "bug"

# Add labels and assignees
gh issue edit 42 --add-label "priority:high" --add-assignee @me

# Comment on an issue
gh issue comment 42 --body "Investigating this now."

# Close an issue
gh issue close 42
```

### Triage Workflow
1. **List untriaged issues:** `gh issue list --label "needs-triage"`
2. **Categorize:** Read details, apply labels, and assign.

---

## 4. Pull Request Lifecycle

### Branching and Committing
```bash
# Create a new feature branch
git checkout -b feat/new-feature

# Stage and commit changes
git add .
git commit -m "feat: implement new feature"
```

### Creating and Monitoring PRs
```bash
# Create a PR
gh pr create --title "feat: new feature" --body "Summary of changes"

# Monitor CI status
gh pr checks --watch

# Check PR diff
gh pr diff
```

### Merging
```bash
# Squash and merge (recommended for clean history)
gh pr merge --squash --delete-branch

# Enable auto-merge
gh pr merge --auto --squash --delete-branch
```

### Auto-Fixing CI Failures
1. **Identify failure:** `gh run list --branch <branch> --limit 5`
2. **Read logs:** `gh run view <RUN_ID> --log-failed`
3. **Fix and push:** `git commit -am "fix: resolve CI" && git push`
4. **Verify:** `gh pr checks`
