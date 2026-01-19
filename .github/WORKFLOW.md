# Git Workflow BMad Bridge

## Développement quotidien
```bash
# Push vers Gitea (dev privé, WIP OK)
git push-dev feature/ma-feature
```

## Release stable vers GitHub
```bash
# 1. Merger dans main
git checkout main
git merge feature/ma-feature

# 2. Tagger
git tag v0.3.0
git push-dev main --tags

# 3. APRÈS tests complets → GitHub
git push-stable main
git push-stable --tags
```

## Règle
⛔ GitHub = releases stables uniquement
✅ Gitea = dev avec bugs OK
