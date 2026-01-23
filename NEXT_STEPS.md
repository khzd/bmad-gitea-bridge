# Next Steps - BMad-Gitea-Bridge

## Statut actuel ✅

- ✅ TODO implémenté: Fermeture automatique des issues
- ✅ Configuration corrigée: Pointage vers HealthProducts/healthcare
- ✅ Synchronisation fonctionnelle: 1 milestone + 3 issues créées
- ✅ Script de diagnostic: test_gitea_connection.py

## Prochaines étapes 🚀

### 1. Provisionner le projet complet dans Gitea

**Objectif:** Automatiser la création complète de l'infrastructure Gitea

**Tâches:**
- [ ] Créer l'organisation HealthProducts (si n'existe pas)
- [ ] Créer le repository healthcare (si n'existe pas)
- [ ] Provisionner les équipes (teams) dans l'organisation
- [ ] Configurer les permissions par équipe
- [ ] Créer les labels standards (story, epic, bmad, etc.)

**Commande cible:**
```bash
python3 src/sync.py provision-project -p medical
```

**Fichiers à modifier/créer:**
- `src/sync.py` - Ajouter commande `provision-project`
- `src/core/project_provisioner.py` - Nouveau module
- `config/projects/medical.yaml` - Ajouter section teams/labels

---

### 2. Améliorer la création d'Epic et lier les Issues

**Objectif:** Créer un vrai Epic (tracking issue) et lier les stories au milestone

**Problème actuel:**
- ✅ Milestone créé pour l'Epic
- ❌ Pas de tracking issue pour l'Epic
- ❌ Stories pas liées au milestone

**Tâches:**
- [ ] Créer une tracking issue pour chaque Epic
- [ ] Lier les stories (issues) au milestone de l'Epic
- [ ] Ajouter checklist des stories dans la tracking issue
- [ ] Synchroniser l'état du milestone avec les stories

**Modifications nécessaires:**

**A. `src/core/epic_syncer.py`:**
```python
def sync_epic(self, epic_file: Path, dry_run: bool = False) -> Dict:
    # ... parsing existant ...

    # 1. Créer le milestone
    milestone = self.milestones.create_epic_milestone(...)

    # 2. Créer la tracking issue pour l'Epic
    epic_issue = self.issues.create_epic_tracking_issue(
        epic_title=title,
        epic_description=description,
        stories=epic_data['stories'],
        milestone_id=milestone['id']  # ← Lier au milestone
    )

    return {
        'milestone': milestone,
        'tracking_issue': epic_issue
    }
```

**B. `src/core/story_syncer.py`:**
```python
def sync_story(self, story_file: Path, milestone_id: int = None, dry_run: bool = False):
    # ... code existant ...

    issue = self.issues.create_story_issue(
        story_title=title,
        story_body=body,
        assignee=assignee,
        milestone=milestone_id  # ← Lier au milestone de l'Epic
    )
```

**C. `src/gitea/issues.py`:**
```python
def create_story_issue(
    self,
    story_title: str,
    story_body: str,
    assignee: str = None,
    milestone: int = None  # ← Nouveau paramètre
) -> Dict:
    return self.create_issue(
        title=story_title,
        body=story_body,
        labels=['story', 'bmad'],
        assignee=assignee,
        milestone=milestone  # ← Passer au client
    )
```

**D. `src/sync.py` - Command `sync-artifacts`:**
```python
# Phase 3: Sync Epics
epic_results = epic_syncer.sync_all_epics(dry_run=dry_run)

# Construire un mapping epic_name -> milestone_id
epic_milestones = {}
for result in epic_results['created']:
    epic_name = result['epic_data']['title']  # Nom de l'epic
    milestone_id = result['milestone']['id']
    epic_milestones[epic_name] = milestone_id

# Phase 4: Sync Stories avec milestone
story_syncer = StorySyncer(gitea_client, artifacts_path, agents)

for story_file in story_syncer.discover_stories():
    story_data = story_syncer.parse_story(story_file)

    # Extraire l'epic associé
    epic_name = story_data.get('epic')  # À extraire du markdown
    milestone_id = epic_milestones.get(epic_name)

    story_syncer.sync_story(story_file, milestone_id=milestone_id, dry_run=dry_run)
```

---

### 3. Synchronisation bidirectionnelle (future)

**Objectif:** Synchroniser les changements de Gitea vers BMad

**Tâches:**
- [ ] Détecter les changements dans Gitea (issues fermées, commentaires, etc.)
- [ ] Mettre à jour les fichiers BMad artifacts
- [ ] Gérer les conflits de synchronisation

---

### 4. Merge de la branche avec TODO implémenté

**Important:** La fonctionnalité de fermeture automatique des issues est sur la branche `claude/fix-todo-mkqsv1ppqx7iu533-dy07Q`

**Tâches:**
- [ ] Tester la branche en local
- [ ] Merger dans `main` si tout fonctionne
- [ ] Ou cherry-pick les commits nécessaires

**Commandes:**
```bash
# Option 1: Merge complet
git checkout main
git merge claude/fix-todo-mkqsv1ppqx7iu533-dy07Q
git push origin main

# Option 2: Cherry-pick seulement les commits du TODO
git checkout main
git cherry-pick <commit-hash-du-todo>
git push origin main
```

---

## Priorité recommandée

1. **Priorité HAUTE:** Étape 2 - Lier les issues aux milestones (améliore l'organisation immédiate)
2. **Priorité MOYENNE:** Étape 1 - Provisionnement automatique (pratique mais pas critique)
3. **Priorité BASSE:** Étape 3 - Sync bidirectionnel (fonctionnalité avancée)

---

## Notes techniques

### Architecture actuelle

```
BMad Artifacts (markdown)
    ↓
[Parsers] → Epic/Story data
    ↓
[Syncers] → Gitea API
    ↓
Gitea (Milestones + Issues)
```

### Architecture cible (Étape 2)

```
Epic (markdown) → Milestone + Tracking Issue
    ↓
Stories (markdown) → Issues liées au Milestone
    ↓
Gitea: Epic tracking issue contient checklist des Stories
```

### Exemple résultat attendu dans Gitea

**Milestone #1:** Epic: Patient Portal
- **Tracking Issue #10:** Epic: Patient Portal - Medical Records Access
  ```markdown
  ## Description
  Epic description here...

  ## Stories
  - [x] #11: Story-001: Patient Account Creation
  - [ ] #12: Story-002: View Lab Results
  - [x] #13: Story-003: Download Medical Records
  ```

**Issues liées au Milestone #1:**
- Issue #11: Story-001 (milestone=1, closed)
- Issue #12: Story-002 (milestone=1, open)
- Issue #13: Story-003 (milestone=1, closed)

---

## Ressources

- [Gitea API Documentation](https://try.gitea.io/api/swagger)
- [Milestones API](https://try.gitea.io/api/swagger#/issue/issueCreateMilestone)
- [Issues API](https://try.gitea.io/api/swagger#/issue/issueCreateIssue)

---

**Dernière mise à jour:** 2026-01-23
**Auteurs:** Khaled Z. & Claude (Anthropic)
