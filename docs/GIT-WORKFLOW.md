# Git Workflow

This document defines the Git workflow, branch naming conventions, commit message format, pull request requirements, and CI checks for the project.

## Table of Contents

- [Branching Strategy](#branching-strategy)
- [Branch Naming](#branch-naming)
- [Development Workflow](#development-workflow)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [CI Requirements](#ci-requirements)
- [Tagging Milestones](#tagging-milestones)

## Branching Strategy

The `main` branch is the protected, stable production branch.

All development work must be completed on a feature branch created from the latest `main`.

```
main         ← production (protected, auto-deploys on push)
  ↑
feature/*    ← new features (branched from main, PR back to main)
fix/*        ← bug fixes (branched from main, PR back to main)
hotfix/*     ← urgent fixes (branched from main, PR back to main)
```

## Branch Naming

Branch names must follow this format:

```
<type>/<short-description>
```

### Allowed Types

| Type | Purpose |
|------|---------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `test/` | Tests or evaluation work |
| `docs/` | Documentation updates |
| `chore/` | Tooling, CI, configuration, dependencies |
| `refactor/` | Code restructuring without changing behavior |

### Examples

```
feature/add-upload-page
feature/rag-retriever
fix/chainlit-routing
test/document-service
docs/update-readme
chore/setup-ci
refactor/rag-services
```

### Renaming a Branch

If the branch has not been pushed:

```bash
git branch -m <type>/correct-name
```

If the branch has already been pushed:

```bash
git branch -m <type>/correct-name
git push -u origin <type>/correct-name
git push origin --delete <type>/old-name
```

## Development Workflow

1. Update your local `main` branch:
   ```bash
   git checkout main && git pull
   ```

2. Create a new feature branch:
   ```bash
   git checkout -b feature/<name>
   ```

3. Make changes and commit regularly:
   ```bash
   git add <files>
   git commit -m "<type>: <description>"
   ```

4. Push your branch:
   ```bash
   git push -u origin feature/<name>
   ```

5. Create a pull request:
   ```bash
   gh pr create --base main
   ```
   Or manually create the PR on GitHub.

6. After approval and merge, GitHub will automatically delete the feature branch.

## Commit Messages

### Format

```
<type>: <description>
```

### Allowed Types

| Type | Purpose |
|------|---------|
| `feat` | New functionality |
| `fix` | Bug fix |
| `test` | Tests |
| `docs` | Documentation |
| `chore` | Configuration, tooling, CI, dependencies |
| `refactor` | Code restructuring |

### Guidelines

- Use lowercase types
- Include a colon followed by a space after the type
- Write meaningful descriptions
- Describe the change, not the process of making it
- Keep the description concise but clear

### Examples

```
feat: add document upload endpoint
feat: implement vector retrieval
fix: correct chainlit mount path
test: add document service tests
docs: update project setup instructions
chore: configure github actions
refactor: separate document processing service
```

## Pull Requests

### Requirements

- All PRs must target the `main` branch
- CI checks must pass before merge
- At least one approval required (if configured)
- No direct pushes to `main` are allowed

### Merge Strategy

**Squash merge** is used for all PRs into `main`. This:
- Keeps history linear and clean
- Maps each merge to one logical change
- Preserves the PR description in the commit message

## CI Requirements

The following GitHub Actions checks must pass before merge:

- **Dependencies and Compilation Test** — Ensures all dependencies install and code compiles
- **Branch and Commit Message Naming Checks** — Validates branch names and commit messages follow conventions

## Tagging Milestones

To mark a submission or checkpoint, tag `main` directly:

```bash
git checkout main && git pull origin main
git tag v0.1.0 -m "Milestone: <description>"
git push origin v0.1.0
```

No release branch is needed for milestones.