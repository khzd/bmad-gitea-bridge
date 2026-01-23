---
project: bmad-gitea-bridge
version: 0.2.0
status: in-documentation
created: 2026-01-22
author: John (Product Manager) & Bibi (Khaled Z.)
classification:
  projectType: Integration/Bridge Tool (CLI-based automation)
  domain: DevOps / Infrastructure Automation / Developer Productivity
  complexity: Medium-High
  projectContext: Brownfield
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-03-success
inputDocuments:
  - brainstorming-session-results.md
  - README.md
  - CHANGELOG.md
documentCounts:
  briefCount: 0
  researchCount: 0
  brainstormingCount: 1
  projectDocsCount: 5
---

# Product Requirements Document (PRD)
## BMAD-Gitea-Bridge v0.2.0

**Project:** BMAD-Gitea-Bridge  
**Version:** 0.2.0 (Current) | Roadmap to 1.0.0  
**Date:** January 22, 2026  
**Author:** John (Product Manager) & Bibi (Khaled Z.)  
**Status:** Active Development - Documentation Phase  
**Communication Language:** French  
**Document Language:** French

---

## Executive Summary

### The Problem

Les organisations adoptant la méthodologie BMAD (Breakthrough Method for Agile AI-Driven Development) font face à un défi critique de passage à l'échelle : **provisionner et synchroniser 1000-1500 agents BMAD** à travers des dizaines voire centaines de projets nécessite un processus manuel chronophage, sujet aux erreurs, et générant une dette de provisioning importante.

**Pain Points Identifiés :**
- **Process manuel inefficace** : Créer des users Gitea, assigner des emails, configurer les repos → 2-3 jours par projet
- **Aller-retours ticket épuisants** : Demandes incomplètes → 2-3 cycles de validation → centaines d'heures perdues
- **Pic de charge janvier** : Arrivée des budgets → 50+ projets à provisionner en flux tendu → chaos garanti
- **Traçabilité fragmentée** : Audit trail manuel → non-conformité potentielle → risques de gouvernance
- **Projets secrets/confidentiels invisibles** : Méthode du "chuchottement" → pas de traçabilité formelle

### The Solution

**BMAD-Gitea-Bridge** est un pont de synchronisation automatique qui transforme le provisioning manuel en un processus industriel, traçable et conforme. C'est le **HUB d'aéroport** qui coordonne automatiquement le trafic entre :
- **BMAD Method** (génération d'agents, epics, stories)
- **Infrastructure Gitea/Jira/GitHub** (repos, users, issues, milestones)

**Proposition de Valeur Clé :**
- **Automatisation à l'échelle** : De 2-3 jours à < 5 minutes par projet
- **Économie massive** : 80 heures économisées par projet (2 semaines de travail)
- **Audit trail instantané** : Traçabilité complète sans effort
- **Enabler de gouvernance** : Users techniques = binômes humains, compliance built-in
- **Cheval de Troie BMAD** : Facilite l'adoption de la méthodologie entreprise

### Success in One Sentence

Le bridge permet à 100% des équipes adoptant BMAD d'être provisionnées automatiquement, sans dette de provisioning, avec un audit trail complet, économisant des centaines d'heures et transformant le chaos du pic budget janvier en coordination fluide.

---

## Goals & Background

### Business Goals

**Objectif Principal :**
Rendre BMAD Method scalable au niveau organisationnel en automatisant complètement le provisioning et la synchronisation des agents BMAD avec l'infrastructure de gestion de projets (Gitea/Jira/GitHub).

**Objectifs Secondaires :**
1. **Éliminer la dette de provisioning** : Zéro équipe BMAD en attente de provisioning
2. **Devenir le standard d'onboarding BMAD** : 100% des nouvelles équipes utilisent le bridge
3. **Faciliter l'adoption BMAD** : Réduire les frictions techniques pour encourager l'adoption méthodologique
4. **Garantir la gouvernance** : Traçabilité complète et conformité audit built-in
5. **Scaler vers l'open-source** : Permettre à d'autres organisations d'adopter BMAD at Scale

### User Goals

**Personas Principaux :**

**1. DevOps Engineer (Utilisateur principal)**
- Provisionner des projets BMAD rapidement et sans erreur
- Gérer le pic de charge janvier (50+ projets) sans paniquer
- Garantir la traçabilité pour l'audit sans effort manuel
- **Moment "Aha!" :** "Je lance une commande et BOOM - 100 projets provisionnés avec audit trail complet"

**2. Product Manager**
- Onboarder des équipes sur BMAD sans friction technique
- Avoir visibilité sur tous les projets (dashboard Gitea/Jira)
- Mesurer la vélocité et burn-down des équipes
- **Moment "Aha!" :** "Je réalise que j'ai économisé 2 semaines de travail manuel en 1 journée"

**3. Enterprise Architect**
- Garantir la conformité et la gouvernance à l'échelle
- Support multi-plateformes (Gitea → Jira → GitHub selon stratégie)
- Migration fluide entre environnements (dev/staging/prod)
- **Moment "Aha!" :** "L'audit trail est là, complet, conforme, sans que j'aie levé le petit doigt"

**4. CISO / Compliance Officer**
- Users techniques = binômes humains (pas de shadow IT)
- Traçabilité native via Git (audit trail built-in)
- Contrôles de sécurité robustes (modes manuel/auto)
- **Moment "Aha!" :** "Je peux auditer n'importe quel projet BMAD en temps réel"

### Background & Context

**Contexte Brownfield :**
Le bridge existe déjà en version 0.2.0 avec les fonctionnalités core implémentées en Python 3.14. Ce PRD documente l'état actuel et définit la roadmap vers la version 1.0.0.

**Historique du Projet :**
- Développé initialement comme sandbox pour HealthAI-Platform (projet healthcare avec BMAD v6 alpha)
- Pivot stratégique vers un outil générique "BMAD at Scale" pour toute organisation
- Installation BMAD dans le repo bridge pour documenter rétroactivement selon la méthodologie
- Session de brainstorming extensive (22 janvier 2026) capturant insights stratégiques

**Architecture Actuelle :**
- **Langage :** Python 3.14 (choix stratégique vs shell "challengy à maintenir")
- **CLI Framework :** Click (interface ligne de commande)
- **Output :** Rich (tables formatées)
- **Config :** PyYAML (multi-projets)
- **APIs :** Gitea API, (future: Jira API, GitHub API)

**Écosystème Multi-Tiers :**
```
Niveau 1 : Gitea (MVP actuel)
  └─ Projets secrets/confidentiels
  └─ Infrastructure on-premise
  └─ Preuve de concept du bridge

Niveau 2 & 3 (roadmap 9 mois) :
  ├─ Jira : Projets internes (recommandé par Archi)
  └─ GitHub : Projets publics (poussé par management)
  
Arbitrage : Comité Architecture
```

**Méthodologie "Chuchottement" :**
Stratégie de déploiement commençant par les projets les plus sensibles (secrets/confidentiels) pour prouver la sécurité et la gouvernance avant de scaler vers Jira/GitHub. "Si ça marche pour nos secrets, ça marchera partout."

---

## Success Criteria

### User Success

**Moments "Aha!" Critiques :**

**1. Audit Trail Instantané** ✨
- **Objectif :** Traçabilité complète générée en < 5 minutes (vs plusieurs jours manuellement)
- **Mesure :** Temps pour générer audit trail complet d'un projet
- **Succès :** < 5 minutes, format conforme audit, zéro intervention manuelle

**2. ROI Immédiat Visible** 💰
- **Objectif :** Économie de 80 heures/projet (2 semaines de travail manuel)
- **Mesure :** Temps de provisioning automatisé vs manuel
- **Succès :** Économie mesurable et quantifiable par projet

**3. Scaling au Pic Budget Janvier** 🚀
- **Objectif :** Capacity de 100 projets/jour en flux tendu (vs 2-3 manuellement)
- **Mesure :** Nombre de projets provisionnés pendant le pic janvier
- **Succès :** Zéro stress, zéro backlog, coordination fluide

**Résultats Utilisateur :**
- ✅ Zéro aller-retours ticket pour provisioning
- ✅ Coordination automatique type "HUB d'aéroport" - zéro collision
- ✅ Gouvernance garantie (users = binômes humains)
- ✅ Process manuel éliminé pour les nouveaux projets BMAD

### Business Success

**Timeline Success Metrics :**

**3 mois (MVP Success) :**
- ✅ **100% des équipes adoptant BMAD** provisionnées automatiquement via le bridge
- ✅ **Zéro dette de provisioning** - pas d'équipes en attente
- ✅ **Bridge = standard d'onboarding BMAD** dans l'organisation
- ✅ Accompagnement à l'adhésion inclut systématiquement le bridge

**6 mois (Phase 2 - Bidirectional) :**
- ✅ **Sync bidirectionnelle opérationnelle** (Gitea → BMAD pour incidents)
- ✅ Agents BMAD activables depuis Gitea
- ✅ Workflow incident → analyse automatique validé en production
- ✅ Gain de temps incident management quantifié

**9 mois (Multi-Platform) :**
- ✅ **Bridge supporte Gitea + Jira + GitHub**
- ✅ Architecture adaptateur universel prouvée sur 3 plateformes
- ✅ Migration entre plateformes documentée et testée
- ✅ Stratégie multi-tiers validée par Comité Architecture

**12 mois (Community Scale) :**
- ✅ **Extension communauté open-source** - N organisations externes adoptent
- ✅ Documentation complète pour adoption externe publiée
- ✅ Ecosystem BMAD at Scale mature et contributif
- ✅ Bridge reconnu comme standard de facto "BMAD at Scale"

### Technical Success

**Architecture & Code Quality :**
- ✅ **Python maintenable et évolutif** (vs shell "challengy")
- ✅ Architecture adaptateur universel (prêt pour Gitea/Jira/GitHub)
- ✅ Code testé (unit tests, integration tests)
- ✅ Documentation technique complète (architecture shardée)

**Performance & Scalability :**
- ✅ **Zero friction technique** - pas de nouveau budget infra requis
- ✅ Provisioning < 5 min par projet
- ✅ Scaling horizontal : 100 projets/jour capacity
- ✅ Support multi-projets concurrent

**Security & Compliance :**
- ✅ **Traçabilité native via Git** (audit trail built-in)
- ✅ Users techniques = binômes humains (gouvernance)
- ✅ Modes manuel/auto pour contrôle de sécurité
- ✅ Tokens/credentials sécurisés (.env, secrets management)

**Integration & Extensibility :**
- ✅ API Gitea intégrée et stable
- ✅ Architecture prête pour Jira/GitHub adapters
- ✅ Webhooks configurables
- ✅ Plugin architecture (future)

### Measurable Outcomes

**Efficiency Metrics :**
| Metric | Manual | Automated | Improvement |
|--------|--------|-----------|-------------|
| Provisioning Time | 2-3 jours | < 5 min | **99% faster** |
| Hours Saved | 0h | 80h/projet | **2 weeks saved** |
| Peak Capacity | 2-3 projets/jour | 100 projets/jour | **50x scaling** |
| Ticket Round-trips | 2-3 cycles | 0 cycles | **100% eliminated** |

**Adoption Metrics :**
- **3 mois :** 100% des équipes BMAD utilisent le bridge
- **6 mois :** Sync bidirectionnelle en production
- **9 mois :** 3 plateformes supportées (Gitea/Jira/GitHub)
- **12 mois :** N organisations externes en production

**Quality Metrics :**
- **Audit trail compliance :** 100% des projets tracés
- **Zero provisioning debt :** 0 équipes en attente
- **Uptime :** > 99% (fallback manuel si incident)
- **Error rate :** < 1% des opérations

---

## Product Scope

### MVP - Minimum Viable Product (v0.2.0 - DÉJÀ LIVRÉ)

**Status :** ✅ Implemented & Operational

**Core Features :**

**1. Agent Discovery & Provisioning**
- ✅ Découverte automatique depuis `agent-manifest.csv`
- ✅ Parsing des métadonnées agents (name, role, module, icon)
- ✅ Validation de la structure agent
- ✅ Support de 13+ agents BMAD standard

**2. Email Assignment**
- ✅ Génération d'emails uniques par agent
- ✅ Support MailPlus Server (Synology)
- ✅ Support Gmail aliases
- ✅ Format : `bmad-{agent}@{domain}.local`
- ✅ Mapping sauvegardé dans `{project}.email-mapping.yaml`
- ✅ Réutilisation des mappings existants (idempotence)

**3. Gitea User Provisioning**
- ✅ Mode manuel : Création d'issues Gitea pour approbation
- ✅ Mode auto : Création directe des users
- ✅ Vérification users existants (pas de duplicates)
- ✅ Intégration SMTP pour notifications
- ✅ Attribution d'emails aux users

**4. Repository & Project Provisioning**
- ✅ Création automatique des repos Gitea
- ✅ Support organisation ou repos personnels
- ✅ Configuration des permissions
- ✅ Initialisation de la structure projet

**5. Artifacts Synchronization**
- ✅ **Epic → Milestone Sync**
  - Parsing des epics depuis artefacts BMAD
  - Création de milestones Gitea
  - Mapping epic metadata → milestone properties
- ✅ **Story → Issue Sync**
  - Parsing des stories depuis artefacts BMAD
  - Création d'issues Gitea
  - Assignment automatique aux agents appropriés
  - Parsing acceptance criteria → checklists
  - Parsing tasks → checklists

**6. Multi-Project Support**
- ✅ Configuration YAML par projet (`config/projects/{name}.yaml`)
- ✅ Variables d'environnement (.env)
- ✅ Isolation des projets (repos, logs séparés)
- ✅ Support projets concurrent

**7. CLI Interface**
- ✅ Framework Click (commandes structurées)
- ✅ Rich output (tables formatées, couleurs)
- ✅ Dry-run mode (`--dry-run`)
- ✅ Logging détaillé (fichiers logs)
- ✅ Help contextuelle

**8. Documentation**
- ✅ README.md complet
- ✅ INSTALL.md (guide installation)
- ✅ USAGE.md (guide utilisation)
- ✅ CHANGELOG.md (historique versions)
- ✅ CONTRIBUTING.md (guide contribution)
- ✅ Examples (configurations projets)

**MVP Value Proposition :**
> "Prove the concept - automated provisioning at scale works. Économie de 80h/projet validée. Audit trail garanti. Gouvernance opérationnelle."

**What's NOT in MVP :**
- ❌ Sync bidirectionnelle (Gitea → BMAD)
- ❌ Support Jira/GitHub
- ❌ Dashboard metrics/analytics
- ❌ Webhooks automation
- ❌ Multi-instance support
- ❌ Advanced error recovery

---

### Growth Features (Post-MVP, 3-9 mois)

**Phase 1 : Bidirectional Sync (v0.3.0-0.4.0 - 6 mois)**

**Vision :** Permettre aux événements Gitea de déclencher des agents BMAD pour analyses automatiques.

**Features :**

**1. Gitea → BMAD Sync**
- Détection d'événements Gitea (issues, comments, status changes)
- Parsing des données Gitea → format BMAD
- Mise à jour des artefacts BMAD locaux
- Historique de synchronisation

**2. Incident Management Automation**
- **Trigger :** Incident critique créé dans Gitea
- **Action :** Active agent BMAD approprié (Tea, Dev, Architect)
- **Output :** Analyse pré-mâchée pour incident manager
  - Logs collectés automatiquement
  - Patterns identifiés
  - Contexte historique ajouté
  - Actions recommandées
- **Value :** Gain de temps énorme en situation critique

**3. Webhooks Integration**
- Configuration webhooks Gitea → Bridge endpoint
- Routing intelligent vers agents BMAD
- Retry logic & error handling
- Webhook logs & monitoring

**4. Status Synchronization**
- Issue status Gitea → Story status BMAD
- Comment sync (bidirectionnel)
- Assignee updates
- Priority/Label changes

**Success Criteria Phase 1 :**
- ✅ Sync bidirectionnelle opérationnelle en production
- ✅ Incident workflow validé (temps d'analyse réduit de 50%+)
- ✅ Webhooks stables (< 1% error rate)

---

**Phase 2 : Multi-Platform Support (v0.5.0-0.6.0 - 9 mois)**

**Vision :** Architecture adaptateur universel prouvée - support Gitea + Jira + GitHub.

**Features :**

**1. Jira Adapter**
- API Jira intégrée
- Mapping BMAD → Jira
  - Epics → Jira Epics
  - Stories → Jira Issues
  - Agents → Jira Users
- Configuration spécifique Jira
- Migration Gitea → Jira

**2. GitHub Adapter**
- API GitHub intégrée
- Mapping BMAD → GitHub
  - Epics → GitHub Milestones
  - Stories → GitHub Issues
  - Agents → GitHub Users/Teams
- Configuration spécifique GitHub
- Migration Gitea → GitHub

**3. Universal Adapter Architecture**
- Interface commune pour tous les adapters
- Plugin system pour nouveaux adapters
- Abstraction des différences API
- Tests adapter-agnostic

**4. Migration Tools**
- Export/Import entre plateformes
- Data validation & reconciliation
- Rollback capability
- Migration logs & reports

**5. Dashboard & Metrics**
- Vélocité par agent
- Burn-down charts
- Cycle time analysis
- Cross-platform analytics

**Success Criteria Phase 2 :**
- ✅ Bridge supporte Gitea + Jira + GitHub en production
- ✅ Migration validée sur 10+ projets
- ✅ Architecture extensible prouvée
- ✅ Dashboard utilisé quotidiennement par PMs

---

### Vision (Future - 12 mois+)

**Phase 3 : Community Scale & Ecosystem**

**Vision :** Bridge devient LE standard de facto pour "BMAD at Scale" - adoption open-source communautaire.

**Features :**

**1. Open-Source Community**
- Documentation externe complète
- Contribution guidelines
- Issue templates
- PR review process
- Community forum/Discord
- Regular releases & roadmap public

**2. Multi-Instance Support**
- Support dev/staging/prod simultané
- Environment isolation
- Configuration per-instance
- Promotion workflows (dev → staging → prod)

**3. Advanced Analytics**
- Predictive analytics (vélocité, burn-down)
- Anomaly detection
- Team health metrics
- Custom reports builder

**4. Plugin Architecture**
- Third-party adapter marketplace
- Custom workflow plugins
- Integration extensions (Slack, Teams, etc.)
- Plugin SDK & docs

**5. Self-Service Portal**
- Web UI pour configuration
- Onboarding wizard
- Project templates
- Health checks & diagnostics

**6. Enterprise Features**
- SSO/SAML integration
- RBAC (Role-Based Access Control)
- Audit logs advanced
- SLA monitoring
- Enterprise support tier

**Vision Success Criteria :**
- ✅ N organisations externes en production (N > 10)
- ✅ Ecosystem mature avec contributions régulières
- ✅ Bridge = référence pour BMAD at Scale
- ✅ Community active (forum, PRs, issues)

---

## User Journeys & Workflows

### Primary User Journey: DevOps Engineer - Project Provisioning

**Context :** Nouvelle équipe adopte BMAD, besoin de provisionner agents + infrastructure Gitea.

**Journey :**

**1. Setup Initial**
```bash
# Clone bridge repo
git clone https://github.com/khzd/bmad-gitea-bridge.git
cd bmad-gitea-bridge

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add tokens, credentials
```

**2. Project Configuration**
```bash
# Copy project template
cp examples/medical-project.yaml config/projects/mon-projet.yaml

# Configure project paths
nano config/projects/mon-projet.yaml
# - bmad.root: path to BMAD project
# - bmad.manifest: path to agent-manifest.csv
# - gitea.url: Gitea instance URL
# - gitea.repository: target repo name
```

**3. Dry-Run Discovery**
```bash
# Test agent discovery without changes
python3.14 src/sync.py sync --project mon-projet --dry-run
```

**Output :**
```
Discovered Agents
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Icon ┃ Name                ┃ Display Name ┃ Module ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 🧙   │ bmad-master         │ BMad Master  │ core   │
│ 📋   │ pm                  │ John         │ bmm    │
│ 💻   │ dev                 │ Amelia       │ bmm    │
└──────┴─────────────────────┴──────────────┴────────┘
✅ Discovered 13 agents
```

**4. Real Provisioning**
```bash
# Execute real sync
python3.14 src/sync.py sync --project mon-projet
```

**Output :**
```
Email Mappings
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Agent               ┃ Email                          ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ bmad-master         │ bmad-bmad-master@bmad.local    │
│ pm                  │ bmad-pm@bmad.local             │
└─────────────────────┴────────────────────────────────┘
✅ Assigned emails to 13 agents

Provisioning Results
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Agent            ┃ Status           ┃ Details   ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ bmad-pm          │ 📋 Issue created │ Issue #8  │
│ bmad-dev         │ 📋 Issue created │ Issue #7  │
└──────────────────┴──────────────────┴───────────┘
✅ Provisioning complete: 13 pending (issues)
```

**5. Artifacts Sync (Epics & Stories)**
```bash
# Sync artifacts to Gitea
python3.14 src/sync.py sync-artifacts --project mon-projet
```

**Output :**
```
Epic Sync Results
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Epic              ┃ Milestone       ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ epic-001.md       │ Milestone #1    │
│ epic-002.md       │ Milestone #2    │
└───────────────────┴─────────────────┘

Story Sync Results
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Story             ┃ Issue       ┃ Assigned To ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ story-001.md      │ Issue #12   │ bmad-dev    │
│ story-002.md      │ Issue #13   │ bmad-pm     │
└───────────────────┴─────────────┴─────────────┘
✅ Artifacts sync complete
```

**6. Validation & Audit Trail**
- ✅ Check Gitea pour users créés
- ✅ Vérifier issues d'approbation (mode manuel)
- ✅ Valider milestones & issues
- ✅ Audit trail complet dans logs/

**Success Moment :**
> "Wow, je viens de provisionner un projet complet avec 13 agents en 5 minutes. L'audit trail est là, tout est tracé, et je n'ai pas touché à l'interface Gitea une seule fois."

**Time Investment :**
- **Setup initial :** 15-20 min (one-time)
- **Per-project provisioning :** < 5 min
- **Manual equivalent :** 2-3 jours

**ROI :** 80 heures économisées par projet

---

### Secondary Journey: PM - Multi-Project Scaling

**Context :** Pic budget janvier - 50 projets à provisionner rapidement.

**Journey :**

**1. Batch Configuration**
```bash
# Créer configs pour 50 projets
for i in {1..50}; do
  cp config/projects/template.yaml config/projects/project-$i.yaml
  # Script pour auto-populate paths
done
```

**2. Batch Provisioning**
```bash
# Loop sur tous les projets
for project in config/projects/*.yaml; do
  name=$(basename $project .yaml)
  echo "Provisioning $name..."
  python3.14 src/sync.py sync --project $name
done
```

**3. Monitoring & Reporting**
```bash
# Check provisioning status
grep "✅" logs/*.log | wc -l  # Count successes
grep "❌" logs/*.log           # Check errors

# Generate report
python3.14 src/sync.py report --all-projects
```

**Success Moment :**
> "Le pic janvier ? Pas de stress. J'ai provisionné 50 projets en une journée. Avec le process manuel, ça m'aurait pris 3 mois. Je viens d'économiser 4000 heures de travail."

---

### Tertiary Journey: Architect - Audit & Compliance

**Context :** Audit de sécurité - besoin de tracer tous les projets BMAD.

**Journey :**

**1. Audit Trail Generation**
```bash
# Export complete audit trail
python3.14 src/sync.py audit --project mon-projet --output audit-report.pdf
```

**2. Compliance Verification**
```bash
# Check user bindings (users = human teams)
python3.14 src/sync.py verify-bindings --all-projects

# Validate governance rules
python3.14 src/sync.py validate-governance
```

**3. Security Review**
- ✅ Review email mappings (no shadow IT)
- ✅ Verify Git commit history (full traceability)
- ✅ Check access permissions (least privilege)
- ✅ Validate encryption (secrets management)

**Success Moment :**
> "L'auditeur me demande la traçabilité complète d'un projet. Je génère le rapport en 2 minutes. Tout est là : qui a créé quoi, quand, pourquoi. Conformité validée."

---

## Functional Requirements (FR)

### FR-1: Agent Discovery

**Priority:** CRITICAL (P0)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit découvrir automatiquement tous les agents BMAD depuis le fichier `agent-manifest.csv` du projet.

**Acceptance Criteria:**
- ✅ Parse `agent-manifest.csv` avec tous les champs (name, displayName, role, module, icon)
- ✅ Valider la structure du manifest (colonnes requises présentes)
- ✅ Support de 13+ agents BMAD standard
- ✅ Détection d'agents custom (modules additionnels)
- ✅ Rapport de découverte formaté (table Rich)
- ✅ Logging détaillé des agents découverts

**Technical Notes:**
- Format CSV avec header: `name,displayName,role,module,icon,description`
- Path configurable via `bmad.manifest` dans project config
- Validation des champs obligatoires (name, displayName, module)

---

### FR-2: Email Assignment

**Priority:** CRITICAL (P0)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit générer et assigner des emails uniques pour chaque agent découvert.

**Acceptance Criteria:**
- ✅ Génération format `bmad-{agent}@{domain}.local`
- ✅ Support MailPlus Server (Synology DSM)
- ✅ Support Gmail aliases
- ✅ Mapping sauvegardé dans `{project}.email-mapping.yaml`
- ✅ Réutilisation des mappings existants (idempotence)
- ✅ Validation email format (RFC 5322)
- ✅ Rapport email assignments (table Rich)

**Technical Notes:**
- Domain configurable via `gmail.domain` dans project config
- MailPlus SMTP configuration via environment variables
- Mapping file format: YAML avec structure `{agent: email}`

---

### FR-3: Gitea User Provisioning

**Priority:** CRITICAL (P0)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit créer des users Gitea pour chaque agent avec les emails assignés.

**Acceptance Criteria:**
- ✅ **Mode manuel :** Création d'issues Gitea pour approbation admin
- ✅ **Mode auto :** Création directe des users via API
- ✅ Vérification users existants (pas de duplicates)
- ✅ Attribution des emails aux users
- ✅ Configuration permissions par défaut
- ✅ Intégration SMTP notifications (optional)
- ✅ Rapport provisioning (statut par agent)
- ✅ Logging détaillé (succès/erreurs)

**Technical Notes:**
- API Gitea: `POST /api/v1/admin/users`
- Mode configurable via `sync.provisioning` (manual/auto)
- Issue template pour mode manuel (custom markdown)
- Error handling: user already exists, API failures, network errors

---

### FR-4: Repository Provisioning

**Priority:** HIGH (P1)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit créer automatiquement les repositories Gitea pour les projets BMAD.

**Acceptance Criteria:**
- ✅ Création repo avec nom configuré
- ✅ Support organisation ou personal repos
- ✅ Configuration visibilité (public/private)
- ✅ Initialisation structure (README, .gitignore)
- ✅ Configuration permissions (access control)
- ✅ Vérification repo existant (idempotence)
- ✅ Rapport création repo

**Technical Notes:**
- API Gitea: `POST /api/v1/user/repos` ou `POST /api/v1/org/{org}/repos`
- Configuration via `gitea.organization` et `gitea.repository`
- Default visibility: private (sécurité first)

---

### FR-5: Epic to Milestone Sync

**Priority:** HIGH (P1)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit synchroniser les epics BMAD vers des milestones Gitea.

**Acceptance Criteria:**
- ✅ Discovery epics depuis `{artifacts}/epics/`
- ✅ Parsing metadata epic (title, description, due_date)
- ✅ Création milestones Gitea via API
- ✅ Mapping epic properties → milestone properties
- ✅ Vérification milestones existants (idempotence)
- ✅ Support épics shardés (index.md + multiple files)
- ✅ Rapport sync epics (table Rich)
- ✅ Logging détaillé

**Technical Notes:**
- API Gitea: `POST /api/v1/repos/{owner}/{repo}/milestones`
- Epic format: Markdown avec frontmatter YAML
- Sharded support: Lecture index.md + tous les fichiers du dossier
- Mapping: epic.title → milestone.title, epic.description → milestone.description

---

### FR-6: Story to Issue Sync

**Priority:** HIGH (P1)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit synchroniser les stories BMAD vers des issues Gitea.

**Acceptance Criteria:**
- ✅ Discovery stories depuis `{artifacts}/stories/`
- ✅ Parsing metadata story (title, description, assignee, epic, acceptance_criteria, tasks)
- ✅ Création issues Gitea via API
- ✅ Assignment automatique agent approprié
- ✅ Link issue → milestone (via epic)
- ✅ Parsing acceptance criteria → issue checklist
- ✅ Parsing tasks → issue checklist
- ✅ Vérification issues existantes (idempotence)
- ✅ Support stories shardées
- ✅ Rapport sync stories (table Rich)
- ✅ Logging détaillé

**Technical Notes:**
- API Gitea: `POST /api/v1/repos/{owner}/{repo}/issues`
- Story format: Markdown avec frontmatter YAML
- Checklist format: Markdown task list `- [ ] Task`
- Assignee mapping: story.assignee → Gitea user (via email mapping)

---

### FR-7: Multi-Project Configuration

**Priority:** HIGH (P1)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit supporter la configuration et gestion de multiples projets simultanément.

**Acceptance Criteria:**
- ✅ Configuration YAML par projet (`config/projects/{name}.yaml`)
- ✅ Isolation complète entre projets (repos, logs, mappings)
- ✅ Variables d'environnement partagées (.env)
- ✅ Override config par projet (precedence)
- ✅ Support projets concurrent (pas de race conditions)
- ✅ CLI project selection (`--project {name}`)
- ✅ Validation configuration (required fields)
- ✅ Template configuration (examples/)

**Technical Notes:**
- Config schema: YAML avec sections project, bmad, gitea, gmail, sync
- Environment variables via python-dotenv
- Config loading order: .env → project config → CLI args
- Validation via Pydantic models (future enhancement)

---

### FR-8: CLI Interface

**Priority:** CRITICAL (P0)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit fournir une interface ligne de commande intuitive et complète.

**Acceptance Criteria:**
- ✅ Framework Click (commands, options, arguments)
- ✅ Rich output (tables, colors, formatting)
- ✅ Commands implémentées:
  - `sync` : Sync agents/repos/users
  - `sync-artifacts` : Sync epics/stories
- ✅ Global options:
  - `--project` : Project selection
  - `--dry-run` : Simulation mode
  - `--verbose` : Detailed logging
- ✅ Help contextuelle (`--help`)
- ✅ Error messages claires
- ✅ Success/failure indicators
- ✅ Progress feedback (spinners future)

**Technical Notes:**
- Click framework for CLI structure
- Rich for beautiful terminal output
- Logging to both console and files
- Exit codes: 0 (success), 1 (error)

---

### FR-9: Logging & Audit Trail

**Priority:** CRITICAL (P0)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit logger toutes les opérations pour audit trail complet.

**Acceptance Criteria:**
- ✅ Logs fichier dans `logs/{project}-{date}.log`
- ✅ Structured logging (timestamps, levels, context)
- ✅ Niveaux: DEBUG, INFO, WARNING, ERROR, CRITICAL
- ✅ Log rotation (éviter files trop gros)
- ✅ Séparation logs par projet
- ✅ Logs Git commits (via Gitea API)
- ✅ Rapport audit exportable
- ✅ Sensitive data masking (tokens, passwords)

**Technical Notes:**
- Python logging module
- Format: `[TIMESTAMP] [LEVEL] [MODULE] Message`
- Rotation: max 10MB par fichier, keep 5 backups
- Git history = audit trail permanent

---

### FR-10: Dry-Run Mode

**Priority:** HIGH (P1)  
**Status:** ✅ Implemented (v0.2.0)

**Description:**
Le système doit permettre simulation complète sans modifications réelles.

**Acceptance Criteria:**
- ✅ CLI flag `--dry-run`
- ✅ Simule toutes les opérations (discovery, provisioning, sync)
- ✅ Affiche ce qui serait fait (WOULD CREATE, WOULD UPDATE)
- ✅ Aucun appel API réel (no side effects)
- ✅ Aucune modification fichiers (no writes)
- ✅ Validation configuration complète
- ✅ Rapport détaillé des actions simulées

**Technical Notes:**
- Flag global propagé à tous les modules
- API calls remplacés par mocks (conditionnels)
- File writes disabled (conditionnels)
- Full validation logic executed

---

### FR-11 to FR-20: Future Features (Growth & Vision)

Ces features sont documentées dans la section "Growth Features" et "Vision" du scope produit.

**Growth Features (6-9 mois) :**
- FR-11: Bidirectional Sync (Gitea → BMAD)
- FR-12: Incident Management Automation
- FR-13: Webhooks Integration
- FR-14: Jira Adapter
- FR-15: GitHub Adapter
- FR-16: Dashboard & Metrics

**Vision Features (12 mois+) :**
- FR-17: Multi-Instance Support
- FR-18: Plugin Architecture
- FR-19: Web UI Portal
- FR-20: Enterprise Features (SSO, RBAC)

---

## Non-Functional Requirements (NFR)

### NFR-1: Performance

**Priority:** HIGH (P1)

**Requirements:**

**Provisioning Speed:**
- Single project provisioning: < 5 minutes
- Batch provisioning (50 projects): < 4 hours
- Agent discovery: < 10 seconds
- Artifact sync (100 stories): < 2 minutes

**Scalability:**
- Support 100+ projects configurés simultanément
- Support 1000+ agents provisionnés
- Support 10,000+ issues/milestones synced
- Concurrent operations: 10 projects simultanément

**Resource Usage:**
- Memory: < 512 MB per sync operation
- CPU: < 50% single core (avg)
- Disk: Logs < 100 MB per project per month
- Network: Efficient API calls (batch when possible)

**Acceptance Criteria:**
- ✅ Benchmarks validés sur datasets réels
- ✅ Load testing (50+ projets concurrent)
- ✅ Performance regression tests
- ✅ Monitoring & profiling tools

---

### NFR-2: Reliability

**Priority:** CRITICAL (P0)

**Requirements:**

**Availability:**
- Uptime target: > 99% (fallback manuel si down)
- Mean Time to Recovery (MTTR): < 1 hour
- Graceful degradation (partial failures OK)

**Error Handling:**
- Retry logic (network failures, API rate limits)
- Transactional operations (rollback on failure)
- Idempotence (safe to re-run)
- Clear error messages (actionable)

**Data Integrity:**
- No data loss (logs, mappings, configs)
- Atomic operations (all-or-nothing)
- Validation before operations
- Backup recommendations

**Acceptance Criteria:**
- ✅ Error scenarios documented
- ✅ Retry mechanisms tested
- ✅ Rollback procedures validated
- ✅ SLA defined and monitored

---

### NFR-3: Security

**Priority:** CRITICAL (P0)

**Requirements:**

**Authentication & Authorization:**
- Gitea API tokens (admin rights required)
- Environment variables for secrets (.env)
- No hardcoded credentials
- Least privilege principle

**Data Protection:**
- Sensitive data masking in logs
- Secure storage (file permissions)
- HTTPS for all API calls
- Token rotation support

**Audit & Compliance:**
- Complete audit trail (logs + Git history)
- User bindings (agents = human teams)
- GDPR compliance (data minimal)
- Security audit ready

**Acceptance Criteria:**
- ✅ Security review completed
- ✅ Penetration testing (basic)
- ✅ Secrets management validated
- ✅ Audit trail comprehensive

---

### NFR-4: Maintainability

**Priority:** HIGH (P1)

**Requirements:**

**Code Quality:**
- Python 3.14+ (modern features)
- Type hints (gradual typing)
- Docstrings (Google style)
- Linting (flake8, black)
- Unit tests (pytest)
- Integration tests

**Documentation:**
- README.md comprehensive
- INSTALL.md step-by-step
- USAGE.md with examples
- Architecture documentation (sharded)
- API documentation (future)
- Troubleshooting guide

**Extensibility:**
- Modular architecture (adapters)
- Plugin system (future)
- Configuration-driven
- Clear interfaces

**Acceptance Criteria:**
- ✅ Code coverage > 80%
- ✅ Documentation up-to-date
- ✅ CI/CD pipeline functional
- ✅ Contribution guide available

---

### NFR-5: Usability

**Priority:** HIGH (P1)

**Requirements:**

**User Experience:**
- Intuitive CLI commands
- Clear output messages
- Helpful error messages
- Progress indicators
- Beautiful tables (Rich)

**Onboarding:**
- Quick start guide (< 15 min)
- Templates & examples
- Video tutorials (future)
- Interactive wizard (future)

**Feedback:**
- Real-time progress
- Success confirmations
- Error diagnostics
- Actionable suggestions

**Acceptance Criteria:**
- ✅ User testing (5+ users)
- ✅ Onboarding time < 20 min
- ✅ Error message quality validated
- ✅ Help documentation complete

---

### NFR-6: Portability

**Priority:** MEDIUM (P2)

**Requirements:**

**Platform Support:**
- Linux (primary: Debian, Ubuntu)
- Synology DSM 7+ (tested)
- macOS (compatible)
- Windows (future: WSL)

**Dependencies:**
- Python 3.10+ (3.14 recommended)
- Standard library preferred
- Minimal external dependencies
- Requirements.txt pinned versions

**Deployment:**
- Git clone + pip install
- Docker support (future)
- No complex setup
- Environment variables config

**Acceptance Criteria:**
- ✅ Tested on 3+ platforms
- ✅ Installation documented
- ✅ Dependency conflicts resolved
- ✅ Docker image available (future)

---

### NFR-7: Compliance & Governance

**Priority:** CRITICAL (P0)

**Requirements:**

**Regulatory Compliance:**
- Audit trail mandatory
- User traceability (bindings)
- Data protection (GDPR-ready)
- Security standards (OWASP)

**Governance:**
- Manual approval mode (default)
- Auto mode (opt-in with justification)
- Change logging (Git + files)
- Access control (Gitea permissions)

**Best Practices:**
- Semantic versioning
- Changelog maintained
- Release notes
- Migration guides

**Acceptance Criteria:**
- ✅ Compliance checklist completed
- ✅ Governance policy documented
- ✅ Audit procedures validated
- ✅ External audit ready

---

## Technical Architecture Overview

**Note:** Architecture détaillée dans `docs/architecture/` (15 fichiers shardés selon BMAD Method).

**High-Level Components:**

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface (Click)                 │
│                  Rich Output & Logging                   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │   Core Orchestrator      │
        │   (sync.py)              │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────────────────┐
        │                                     │
┌───────▼────────┐              ┌────────────▼───────────┐
│ Agent Discovery│              │   Artifact Syncers     │
│ & Provisioning │              │   (Epics/Stories)      │
└───────┬────────┘              └────────────┬───────────┘
        │                                    │
        │                                    │
┌───────▼────────────────────────────────────▼───────────┐
│              Gitea API Client                          │
│       (users, repos, issues, milestones)               │
└────────────────────────┬───────────────────────────────┘
                         │
                ┌────────▼────────┐
                │   Gitea Server   │
                │  (on-premise)    │
                └──────────────────┘
```

**Key Architectural Decisions:**

1. **Python Strategic Choice** : Maintenable vs shell "challengy"
2. **Adapter Pattern** : Universal pour Gitea/Jira/GitHub
3. **CLI-First** : Developer-friendly, automation-ready
4. **Configuration-Driven** : Multi-projets, zero hardcoding
5. **Idempotent Operations** : Safe re-runs, no duplicates
6. **Audit Trail Native** : Logs + Git history

**Tech Stack:**
- **Language:** Python 3.14
- **CLI:** Click
- **Output:** Rich
- **Config:** PyYAML
- **HTTP:** Requests
- **Testing:** pytest (future)
- **Linting:** flake8, black (future)

---

## Epics & User Stories

**Note:** Stories détaillées dans `docs/stories/` selon BMAD Method.

### Epic 1: Core Provisioning (v0.2.0 - ✅ COMPLETE)

**Goal:** Automated agent discovery and Gitea provisioning at scale.

**Stories:**
1. ✅ Story 1.1: Agent Discovery from CSV
2. ✅ Story 1.2: Email Generation & Assignment
3. ✅ Story 1.3: Gitea User Provisioning (Manual Mode)
4. ✅ Story 1.4: Gitea User Provisioning (Auto Mode)
5. ✅ Story 1.5: Repository Creation
6. ✅ Story 1.6: Multi-Project Configuration

**Status:** ✅ SHIPPED (v0.2.0)

---

### Epic 2: Artifact Synchronization (v0.2.0 - ✅ COMPLETE)

**Goal:** Sync BMAD artifacts (epics/stories) to Gitea (milestones/issues).

**Stories:**
1. ✅ Story 2.1: Epic → Milestone Sync
2. ✅ Story 2.2: Story → Issue Sync
3. ✅ Story 2.3: Agent Assignment Logic
4. ✅ Story 2.4: Checklist Parsing (Acceptance Criteria)
5. ✅ Story 2.5: Checklist Parsing (Tasks)

**Status:** ✅ SHIPPED (v0.2.0)

---

### Epic 3: Developer Experience (v0.2.0 - ✅ COMPLETE)

**Goal:** Intuitive CLI, beautiful output, comprehensive docs.

**Stories:**
1. ✅ Story 3.1: CLI Commands (sync, sync-artifacts)
2. ✅ Story 3.2: Rich Tables & Formatting
3. ✅ Story 3.3: Dry-Run Mode
4. ✅ Story 3.4: Logging & Audit Trail
5. ✅ Story 3.5: Documentation Suite

**Status:** ✅ SHIPPED (v0.2.0)

---

### Epic 4: Bidirectional Sync (v0.3.0 - ROADMAP 6 mois)

**Goal:** Enable Gitea → BMAD sync for incident automation.

**Stories:**
1. ⏳ Story 4.1: Webhook Listener
2. ⏳ Story 4.2: Event Parser (Gitea → BMAD)
3. ⏳ Story 4.3: Incident Detection Logic
4. ⏳ Story 4.4: Agent Activation Workflow
5. ⏳ Story 4.5: Analysis Output Generation

**Status:** ⏳ PLANNED

---

### Epic 5: Multi-Platform Support (v0.5.0 - ROADMAP 9 mois)

**Goal:** Support Gitea + Jira + GitHub avec architecture universelle.

**Stories:**
1. ⏳ Story 5.1: Abstract Adapter Interface
2. ⏳ Story 5.2: Jira Adapter Implementation
3. ⏳ Story 5.3: GitHub Adapter Implementation
4. ⏳ Story 5.4: Migration Tools
5. ⏳ Story 5.5: Dashboard & Metrics

**Status:** ⏳ PLANNED

---

### Epic 6: Community Scale (v1.0.0 - ROADMAP 12 mois)

**Goal:** Open-source readiness, external adoption, ecosystem.

**Stories:**
1. ⏳ Story 6.1: External Documentation
2. ⏳ Story 6.2: Contribution Guidelines
3. ⏳ Story 6.3: Multi-Instance Support
4. ⏳ Story 6.4: Plugin Architecture
5. ⏳ Story 6.5: Community Portal

**Status:** ⏳ VISION

---

## Risks & Mitigations

### Risk 1: API Rate Limits (Gitea/Jira/GitHub)

**Probability:** MEDIUM  
**Impact:** HIGH  
**Severity:** MEDIUM-HIGH

**Description:**
Lors du provisioning de 50+ projets concurrent, risque de hitting API rate limits.

**Mitigation:**
- Implement exponential backoff retry logic
- Batch operations when possible
- Rate limiting client-side (throttling)
- Monitor API usage in logs
- Provide clear error messages with wait times

**Contingency:**
- Manual mode (issues) as fallback
- Distribute provisioning across time windows
- Contact platform for rate limit increase

---

### Risk 2: Data Loss During Sync

**Probability:** LOW  
**Impact:** CRITICAL  
**Severity:** MEDIUM

**Description:**
Failure pendant sync → data loss potentiel (mappings, artifacts).

**Mitigation:**
- Transactional operations (atomic)
- Backup before sync (optional flag)
- Idempotent operations (safe re-run)
- Comprehensive logging
- Validation before operations

**Contingency:**
- Rollback procedures documented
- Git history as source of truth
- Manual recovery steps

---

### Risk 3: Configuration Errors

**Probability:** MEDIUM  
**Impact:** MEDIUM  
**Severity:** MEDIUM

**Description:**
Mauvaise configuration → provisioning incorrect ou failures.

**Mitigation:**
- Configuration validation (schema)
- Dry-run mandatory for first runs
- Template configurations (examples/)
- Clear error messages
- Onboarding documentation

**Contingency:**
- Configuration troubleshooting guide
- Support channels (GitHub issues)
- Common errors documented

---

### Risk 4: Security Breach (Token Leak)

**Probability:** LOW  
**Impact:** CRITICAL  
**Severity:** MEDIUM-HIGH

**Description:**
API tokens leaked → unauthorized access to Gitea/Jira/GitHub.

**Mitigation:**
- Environment variables (no hardcoding)
- .env in .gitignore
- Token rotation support
- Least privilege (scoped tokens)
- Security audit documentation

**Contingency:**
- Token revocation procedures
- Incident response plan
- Post-mortem process

---

### Risk 5: Change Management Resistance

**Probability:** MEDIUM  
**Impact:** HIGH  
**Severity:** MEDIUM-HIGH

**Description:**
Équipes résistent à adopter BMAD Method → bridge inutilisé.

**Mitigation:**
- ROI quantifié clairement (80h/projet)
- "Cheval de Troie" strategy
- Onboarding support (documentation + training)
- Success stories (early adopters)
- Executive sponsorship

**Contingency:**
- Pilot projects (proof of value)
- Gradual rollout (volunteers first)
- Feedback loops (iterate)

---

### Risk 6: Platform API Changes (Breaking)

**Probability:** MEDIUM  
**Impact:** HIGH  
**Severity:** MEDIUM-HIGH

**Description:**
Gitea/Jira/GitHub change APIs → bridge breaks.

**Mitigation:**
- API version pinning
- Comprehensive tests (integration)
- Monitoring API deprecations
- Abstract adapter layer (isolation)
- Active maintenance commitment

**Contingency:**
- Quick patch releases
- Communication to users
- Fallback to older API versions

---

## Open Questions & Decisions Needed

### Q1: Jira vs GitHub Priority?

**Status:** ⏳ PENDING - Comité Architecture Decision

**Context:**
Roadmap 9 mois inclut support Jira + GitHub. Quelle priorité ?

**Options:**
- **Option A:** Jira first (recommandé par Archi, projets internes)
- **Option B:** GitHub first (poussé par management, projets publics)
- **Option C:** Parallel (double effort, plus rapide mais risqué)

**Decision Criteria:**
- Nombre de projets Jira vs GitHub (demand)
- Complexité technique relative (APIs)
- Ressources disponibles (team capacity)
- Strategic alignment (internal vs external focus)

**Timeline:** Décision avant fin Q1 2026 pour planning roadmap

---

### Q2: Webhook vs Polling for Bidirectional Sync?

**Status:** ⏳ PENDING - Technical Design

**Context:**
Sync Gitea → BMAD peut être webhook-based ou polling-based.

**Options:**
- **Option A:** Webhooks (real-time, efficient, complexe setup)
- **Option B:** Polling (simple, less real-time, resource usage)
- **Option C:** Hybrid (webhooks + fallback polling)

**Decision Criteria:**
- Real-time requirements (how critical?)
- Infrastructure constraints (webhook endpoint hosting)
- Reliability (webhook delivery failures)
- Simplicity (developer experience)

**Timeline:** Décision avant start Phase 2 (6 mois)

---

### Q3: Open-Source License Choice?

**Status:** ⏳ PENDING - Legal & Business Decision

**Context:**
Bridge deviendra open-source (12 mois). Quelle licence ?

**Options:**
- **Option A:** MIT (permissive, adoption facile)
- **Option B:** Apache 2.0 (patent protection)
- **Option C:** GPL v3 (copyleft, communauté driven)
- **Option D:** Dual license (commercial + open-source)

**Decision Criteria:**
- Community adoption goals
- Commercial interests
- Patent protection needs
- BMAD Method licensing alignment

**Timeline:** Décision avant Q4 2026 (prepare open-source launch)

---

### Q4: Multi-Tenant Support Needed?

**Status:** ⏳ PENDING - Product Strategy

**Context:**
Actuellement single-tenant. Besoin de multi-tenant pour SaaS futur ?

**Options:**
- **Option A:** Single-tenant forever (simpler, current model)
- **Option B:** Multi-tenant (SaaS opportunity, complex)
- **Option C:** Hybrid (single-tenant on-premise + SaaS option)

**Decision Criteria:**
- SaaS business model viability
- Technical complexity (data isolation, security)
- Customer demand (self-hosted vs SaaS)
- Resource investment required

**Timeline:** Décision avant roadmap v2.0.0 (18+ mois)

---

## Assumptions & Dependencies

### Assumptions

1. **BMAD Adoption:** Organizations will continue adopting BMAD Method
2. **Agent Manifest Stability:** `agent-manifest.csv` format remains stable
3. **API Availability:** Gitea/Jira/GitHub APIs remain accessible and documented
4. **Python Support:** Python 3.10+ will remain widely supported
5. **Git Infrastructure:** Organizations have Git infrastructure (Gitea/GitHub/Jira)
6. **Network Access:** Bridge has network access to target platforms
7. **Admin Rights:** Users have admin rights on Gitea (for provisioning)
8. **Budget Approval:** Organizations approve BMAD tooling investments

### Dependencies

**External Dependencies:**

1. **Gitea Platform**
   - Version: 1.21.5+ (tested)
   - API: v1 stable
   - Self-hosted or cloud

2. **BMAD Method Framework**
   - Version: 6.0.0-alpha.23+
   - Agent manifest format
   - Artifact structure (epics/stories)

3. **Python Ecosystem**
   - Python: 3.10+ (3.14 recommended)
   - pip: Latest
   - Dependencies: Click, Rich, PyYAML, Requests

4. **Infrastructure**
   - Linux/macOS (primary)
   - Synology DSM 7+ (tested)
   - Network connectivity

**Internal Dependencies:**

1. **BMAD Project Structure**
   - `_bmad/` directory structure
   - `agent-manifest.csv` present
   - Artifacts directory configured

2. **Configuration Files**
   - `.env` with tokens/credentials
   - `config/projects/*.yaml` per project
   - Email mappings (generated or provided)

3. **Gitea Setup**
   - Gitea instance operational
   - Admin user/token available
   - SMTP configured (optional, for notifications)

**Future Dependencies (Roadmap):**

- Jira Cloud/Server instance (9 mois)
- GitHub account/organization (9 mois)
- Webhook endpoint hosting (6 mois)
- PostgreSQL (optional, for advanced analytics)

---

## Success Metrics (KPIs)

### Adoption Metrics

| Metric | 3 Months | 6 Months | 9 Months | 12 Months |
|--------|----------|----------|----------|-----------|
| Teams Using Bridge | 100% of BMAD teams | 100% + 5 pilot external | 100% + 10 external | 100% + 20 external |
| Projects Provisioned | 20+ | 50+ | 100+ | 200+ |
| Agents Provisioned | 500+ | 1,000+ | 2,000+ | 5,000+ |

### Efficiency Metrics

| Metric | Target | Current | Improvement |
|--------|--------|---------|-------------|
| Provisioning Time | < 5 min | 2-3 days (manual) | **99% faster** |
| Hours Saved per Project | 80h | 0h (manual) | **80h saved** |
| Peak Capacity (Jan) | 100 projets/jour | 2-3 projets/jour | **50x scaling** |
| Ticket Round-trips | 0 | 2-3 cycles | **100% eliminated** |

### Quality Metrics

| Metric | Target | Success Criteria |
|--------|--------|------------------|
| Audit Trail Compliance | 100% | All projects traceable |
| Provisioning Errors | < 1% | Error rate monitored |
| User Satisfaction (NPS) | > 50 | Quarterly surveys |
| Documentation Completeness | 100% | All features documented |

### Business Impact Metrics

| Metric | 6 Months | 12 Months | 24 Months |
|--------|----------|-----------|-----------|
| ROI (Hours Saved) | 4,000h | 16,000h | 50,000h |
| BMAD Adoption Rate | +20% | +50% | +100% |
| External Organizations | 5 | 20 | 50+ |
| Community Contributors | 0 | 5+ | 20+ |

---

## Constraints

### Technical Constraints

1. **Python Version:** 3.10+ minimum (3.14 recommended)
2. **API Rate Limits:** Subject to platform limits (Gitea/Jira/GitHub)
3. **Network:** Requires connectivity to target platforms
4. **Admin Rights:** Provisioning requires admin access
5. **File System:** Requires read/write access for configs/logs

### Resource Constraints

1. **Team Size:** Solo developer + AI pair (Claude) currently
2. **Budget:** Bootstrap phase (zero additional infra spend)
3. **Time:** Part-time development (competing priorities)
4. **Infrastructure:** On-premise Synology NAS (limited resources)

### Organizational Constraints

1. **Change Management:** BMAD adoption prerequisite
2. **Governance:** Manual approval default (compliance)
3. **Architecture Committee:** Platform decisions (Jira vs GitHub)
4. **Security Audits:** Required before production rollout

### Legal & Compliance Constraints

1. **Audit Trail:** Mandatory for all operations
2. **Data Protection:** GDPR compliance required
3. **Security Standards:** OWASP guidelines
4. **Licensing:** TBD for open-source release

---

## Glossary

**Agent:** An AI persona in BMAD Method with specific role (PM, Dev, Architect, etc.)

**Artifact:** BMAD-generated document (epic, story, PRD, architecture, etc.)

**BMAD Method:** Breakthrough Method for Agile AI-Driven Development

**Bridge:** This tool - automated sync between BMAD and Gitea/Jira/GitHub

**Brownfield:** Existing project (code already exists)

**Chuchottement:** "Whispering method" - stealth provisioning for secret projects

**Epic:** High-level feature collection (maps to Milestone in Gitea)

**Greenfield:** New project (starting from scratch)

**HUB d'Aéroport:** Airport hub metaphor - coordination at scale

**Manifest:** `agent-manifest.csv` - list of all BMAD agents

**Milestone:** Gitea concept (equivalent to epic in BMAD)

**Provisioning:** Creating users, repos, issues in Gitea

**Story:** User story in BMAD (maps to Issue in Gitea)

**Sync:** Synchronization of artifacts between BMAD and Gitea

**Tour de Babel:** Babel Tower metaphor - chaos without coordination

---

## Appendices

### Appendix A: Configuration Schema

**Project Configuration (config/projects/{name}.yaml):**

```yaml
project:
  name: string              # Project identifier
  description: string       # Project description

bmad:
  root: string             # Path to BMAD project root
  manifest: string         # Path to agent-manifest.csv
  artifacts: string        # Path to artifacts directory (optional)

gitea:
  url: string              # Gitea instance URL
  organization: string     # Org name (empty for personal)
  repository: string       # Repository name
  admin_token: string      # Admin API token (or ${ENV_VAR})

gmail:
  base: string             # Email prefix (e.g., "bmad")
  domain: string           # Email domain
  enabled: boolean         # Enable email generation

sync:
  mode: string             # "manual" or "auto"
  provisioning: string     # "manual" or "auto"
```

**Environment Variables (.env):**

```bash
GITEA_URL=http://192.168.0.76:3000
GITEA_ADMIN_TOKEN=gto_xxxxxxxxxxxxx
GMAIL_BASE=bmad
GMAIL_DOMAIN=bmad.local
LOG_LEVEL=INFO
```

---

### Appendix B: API Endpoints

**Gitea API v1 Endpoints Used:**

```
POST /api/v1/admin/users                          # Create user
GET  /api/v1/users/{username}                     # Check user exists
POST /api/v1/user/repos                           # Create personal repo
POST /api/v1/org/{org}/repos                      # Create org repo
POST /api/v1/repos/{owner}/{repo}/issues          # Create issue
POST /api/v1/repos/{owner}/{repo}/milestones      # Create milestone
GET  /api/v1/repos/{owner}/{repo}/milestones      # List milestones
PATCH /api/v1/repos/{owner}/{repo}/issues/{index} # Update issue
```

**Authentication:** Bearer token in Authorization header

**Rate Limits:** Variable per instance (check X-RateLimit headers)

---

### Appendix C: Email Mapping Format

**File:** `{project}.email-mapping.yaml`

**Format:**

```yaml
bmad-master: bmad-bmad-master@bmad.local
pm: bmad-pm@bmad.local
dev: bmad-dev@bmad.local
architect: bmad-architect@bmad.local
qa: bmad-qa@bmad.local
# ... additional agents
```

**Properties:**
- Key: Agent name (from manifest)
- Value: Generated email address
- Reused on subsequent runs (idempotence)

---

### Appendix D: Artifact Structure

**Epic Format (epic-001.md):**

```markdown
---
title: "Epic Title"
description: "Epic description"
due_date: "2026-12-31"
status: "in-progress"
---

# Epic: Epic Title

Description and details...
```

**Story Format (story-001.md):**

```markdown
---
title: "Story Title"
description: "Story description"
assignee: "dev"
epic: "epic-001"
status: "todo"
---

# Story: Story Title

## Acceptance Criteria
- [ ] AC 1
- [ ] AC 2

## Tasks
- [ ] Task 1
- [ ] Task 2

Details...
```

---

### Appendix E: CLI Commands Reference

**sync - Main provisioning command:**
```bash
python3.14 src/sync.py sync --project {name} [--dry-run] [--verbose]
```

**sync-artifacts - Artifact synchronization:**
```bash
python3.14 src/sync.py sync-artifacts --project {name} [--dry-run]
```

**Options:**
- `--project {name}` : Select project config
- `--dry-run` : Simulation mode (no real changes)
- `--verbose` : Detailed logging output

**Examples:**
```bash
# Dry-run provisioning
python3.14 src/sync.py sync --project medical --dry-run

# Real provisioning
python3.14 src/sync.py sync --project medical

# Sync artifacts
python3.14 src/sync.py sync-artifacts --project medical

# Verbose logging
python3.14 src/sync.py sync --project medical --verbose
```

---

### Appendix F: Troubleshooting Guide

**Common Issues:**

**Issue 1: API Authentication Failed**
- **Symptom:** 401 Unauthorized errors
- **Solution:** Check GITEA_ADMIN_TOKEN in .env, verify token validity
- **Verification:** `curl -H "Authorization: token $TOKEN" $GITEA_URL/api/v1/user`

**Issue 2: Agent Manifest Not Found**
- **Symptom:** "File not found: agent-manifest.csv"
- **Solution:** Check `bmad.manifest` path in project config, verify file exists
- **Verification:** `ls -l {path}/agent-manifest.csv`

**Issue 3: Email Already Exists**
- **Symptom:** "Email already registered"
- **Solution:** User already exists, check Gitea users, use different email domain
- **Verification:** Check Gitea admin panel → Users

**Issue 4: Rate Limit Exceeded**
- **Symptom:** 429 Too Many Requests
- **Solution:** Wait and retry, implement backoff, contact Gitea admin for limit increase
- **Verification:** Check X-RateLimit headers in API responses

**Issue 5: Permission Denied (Logs)**
- **Symptom:** Cannot write to logs directory
- **Solution:** Check file permissions, create logs/ directory, verify user access
- **Verification:** `ls -ld logs/` and `touch logs/test.txt`

---

### Appendix G: Migration Guide (Future)

**Gitea → Jira Migration:**
- TBD (roadmap 9 mois)
- Export Gitea data
- Transform to Jira format
- Import via Jira API
- Validate data integrity

**Gitea → GitHub Migration:**
- TBD (roadmap 9 mois)
- Similar process to Jira
- GitHub-specific considerations (Teams vs Users)

---

### Appendix H: Contributing Guide

**How to Contribute:**

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make changes** (follow coding standards)
4. **Add tests** (pytest)
5. **Commit** (`git commit -m 'Add amazing feature'`)
6. **Push** (`git push origin feature/amazing-feature`)
7. **Open Pull Request**

**Coding Standards:**
- Python 3.10+ compatible
- Type hints preferred
- Docstrings (Google style)
- Black formatting
- Flake8 linting

**Testing:**
- Unit tests required
- Integration tests for APIs
- Dry-run validation

**Documentation:**
- Update README if needed
- Add examples
- Update CHANGELOG

---

### Appendix I: Roadmap Timeline

**Visual Timeline:**

```
2026
├─ Q1 (Jan-Mar): Documentation Phase (current)
│  ├─ ✅ Brainstorming (Jan 22)
│  ├─ ✅ PRD (Jan 22)
│  └─ ⏳ Architecture (Jan 23+)
│
├─ Q2 (Apr-Jun): Bidirectional Sync Phase
│  ├─ v0.3.0: Webhook listener
│  ├─ v0.3.5: Incident automation
│  └─ v0.4.0: Full bidirectional operational
│
├─ Q3 (Jul-Sep): Multi-Platform Phase
│  ├─ v0.5.0: Jira adapter (if prioritized)
│  ├─ v0.5.5: GitHub adapter (if prioritized)
│  └─ v0.6.0: Dashboard & metrics
│
└─ Q4 (Oct-Dec): Community Scale Phase
   ├─ v0.9.0: Open-source prep
   ├─ v0.9.5: External documentation
   └─ v1.0.0: Official community launch

2027+
└─ v2.0.0+: Enterprise features, Plugin architecture
```

---

## Document Metadata

**Version:** 1.0  
**Status:** DRAFT - Ready for Review  
**Created:** 2026-01-22  
**Last Updated:** 2026-01-22  
**Authors:** John (Product Manager) & Bibi (Khaled Z.)  
**Reviewers:** TBD (Architecture team, Security team, CISO)  
**Approval:** Pending  
**Next Review:** 2026-02-01  

**Change Log:**
- v1.0 (2026-01-22): Initial PRD creation from brainstorming session

---

**Document Status:** ✅ READY FOR REVIEW

**Next Steps:**
1. Review by Architecture team (validate technical decisions)
2. Review by Security/CISO (validate governance & compliance)
3. Review by Product leadership (validate roadmap & priorities)
4. Approval & Publication
5. Transition to Architecture phase (docs/architecture/)

---

*"Follow the Sun"* ☀️ - BMAD at Scale Initiative