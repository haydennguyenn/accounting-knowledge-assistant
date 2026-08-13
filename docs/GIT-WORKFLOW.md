# Git Workflow

This document defines the Git workflow, branch naming, commit message conventions, pull request requirements, GitHub Actions checks, and local validation process for the project.

## Branching Strategy

The `main` branch is the protected, stable branch.

All development work should be completed on a feature branch created from the latest `main`.

```
main         ← production (protected, deploys automatically on push)
  ↑
feature/*    ← new features (branched from main, PR back to main)
hotfix/*     ← urgent fixes (branched from main, PR back to main)
```

### Branch Naming

Branch names must follow:

```text
<type>/<short-description>
```

Allowed types:
```text
feature/ — new functionality
fix/ — bug fixes
test/ — tests or evaluation work
docs/ — documentation
chore/ — tooling, CI, configuration, dependencies
refactor/ — code restructuring without changing intended behaviour
```

Examples:
```text
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

```
git branch -m feature/correct-name
```
If the old branch has already been pushed:

```
git branch -m feature/correct-name
git push -u origin feature/correct-name
git push origin --delete feature/old-name
```

## Workflow

```
git checkout main && git pull
git checkout -b feature/(name)

# ...make changes, commit...

git push -u origin feature/(name)

gh pr create --base main   # or go to github and create pull request
# review, merge, GitHub deletes the branch automatically
```

## Commit Messages

Commits format:
```
<type>: <description>
```

Allowed types:
``` text
feat — new functionality
fix — bug fix
test — tests
docs — documentation
chore — configuration, tooling, CI, dependencies
refactor — code restructuring
```

Examples:
``` text
feat: add document upload endpoint
feat: implement vector retrieval
fix: correct chainlit mount path
test: add document service tests
docs: update project setup instructions
chore: configure github actions
refactor: separate document processing service
```

Commit messages should:
- use lowercase types
- contain a colon followed by a space
- have a meaningful description
- describe the change rather than the process of making it

### Making a Commit
```
git add .
git commit -m "feat: add document upload endpoint"
```

## Merge Strategy

Squash merge every PR into `main` — keeps history linear and each merge maps to one logical
change.

## Protected Branch

`main` is protected — no direct pushes. All changes go through a pull request.

CI must pass before merge:
- Dependencies and Compilation Test
- Branch and Commit Message Naming Checks

## Tagging a milestone (optional)

If you want to mark a submission or checkpoint, tag `main` directly — no release branch needed:

```bash
git checkout main && git pull origin main
git tag v0.1.0 -m "Milestone: <what this is>"
git push origin v0.1.0
```