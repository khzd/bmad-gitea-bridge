# 🌉 BMad-Gitea-Bridge

> Automatic synchronization bridge between BMad Method agents and Gitea

**Version:** 0.1.0  
**Authors:** Khaled Z. (khzd) & Claude (Anthropic)  
**License:** MIT  
**Date:** January 17, 2026

---

## 🎯 What is BMad-Gitea-Bridge?

BMad-Gitea-Bridge automatically discovers BMad Method agents from your project and provisions them in Gitea with:

- ✅ **Automatic agent discovery** from `agent-manifest.csv`
- ✅ **Email assignment** via MailPlus Server (or Gmail)
- ✅ **Gitea user provisioning** (manual or automatic mode)
- ✅ **Issue-based workflow** for manual approval
- ✅ **Multi-project support** with separate configurations

---

## 🏗️ Architecture
```
BMad Project
    ↓
agent-manifest.csv (13+ agents)
    ↓
BMad-Gitea-Bridge Script
    ├── Agent Discovery
    ├── Email Generation (bmad-{agent}@domain.local)
    └── Gitea Provisioning
        ↓
Gitea Instance
    ├── Users created (bmad-pm, bmad-dev, etc.)
    └── Issues for manual approval
        ↓
MailPlus Server
    └── Email notifications
```

---

## 🆕 Recent Updates

### v0.2.0 - Artifact Sync (2026-01-19)

**New Features:**
- ✨ **Epic Sync**: Automatically sync BMad epics to Gitea milestones
- ✨ **Story Sync**: Automatically sync BMad stories to Gitea issues with agent assignment
- ✨ **New Command**: `sync-artifacts` for artifact synchronization
- ✨ **Task Parsing**: Automatically parse acceptance criteria and tasks as checklists

**New Files:**
- `src/core/epic_syncer.py` - Epic → Milestone synchronization
- `src/core/story_syncer.py` - Story → Issue synchronization  
- `test-artifacts/` - Sample epic and stories for testing

**Usage:**
```bash
# Sync artifacts (dry-run)
python3.14 src/sync.py sync-artifacts --project medical --dry-run

# Sync artifacts (real)
python3.14 src/sync.py sync-artifacts --project medical
```

**What it does:**
1. Discovers epics and stories from BMad artifacts directory
2. Creates Gitea milestones for epics
3. Creates Gitea issues for stories
4. Assigns issues to appropriate BMad agents
5. Parses acceptance criteria and tasks as checklists

**Configuration:**
Add `artifacts` path to your project config:
```yaml
bmad:
  root: /volume1/concept/bmad
  manifest: _bmad/_config/agent-manifest.csv
  artifacts: /volume1/tools/bmad-gitea-bridge/test-artifacts
```

**Tested on:**
- ✅ Synology DSM 7.2
- ✅ Python 3.14
- ✅ Gitea 1.21.5

**Contributors:** Khaled Z. & Claude (Anthropic)

---

## ✨ Features

### 🔍 **Phase 1: Agent Discovery**
...
```

---

## ✅ **Résultat final :**
```
...intro...

## 🆕 Recent Updates        ← NOUVEAU
(toute la section)

## ✨ Features              ← Existant
(Phase 1, 2, 3...)


## ✨ Features

### 🔍 **Phase 1: Agent Discovery**
- Reads `agent-manifest.csv` from BMad project
- Discovers all agents with metadata (name, role, module, icon)
- Validates agent structure

### 📧 **Phase 2: Email Assignment**
- Generates unique emails for each agent
- Supports MailPlus Server or Gmail aliases
- Saves mapping to `{project}.email-mapping.yaml`
- Reuses existing mappings on subsequent runs

### 🔧 **Phase 3: Gitea Provisioning**
- **Manual mode**: Creates issues for each agent (recommended)
- **Auto mode**: Creates Gitea users directly
- Checks for existing users (no duplicates)
- Integrates with MailPlus SMTP for notifications

---

## 📸 Screenshots

### Agent Discovery
```
                  Discovered Agents                   
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Icon ┃ Name                ┃ Display Name ┃ Module ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 🧙   │ bmad-master         │ BMad Master  │ core   │
│ 📋   │ pm                  │ John         │ bmm    │
│ 💻   │ dev                 │ Amelia       │ bmm    │
│ 🧪   │ tea                 │ Murat        │ bmm    │
└──────┴─────────────────────┴──────────────┴────────┘
   ✅ Discovered 13 agents
```

### Email Mapping
```
                       Email Mappings                        
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Agent               ┃ Email                               ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ bmad-master         │ bmad-bmad-master@bmad.local         │
│ pm                  │ bmad-pm@bmad.local                  │
│ dev                 │ bmad-dev@bmad.local                 │
└─────────────────────┴─────────────────────────────────────┘
   ✅ Assigned emails to 13 agents
```

### Provisioning Results
```
                   Provisioning Results                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Agent                    ┃ Status           ┃ Details   ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ bmad-pm                  │ 📋 Issue created │ Issue #8  │
│ bmad-dev                 │ 📋 Issue created │ Issue #7  │
│ bmad-tea                 │ 📋 Issue created │ Issue #11 │
└──────────────────────────┴──────────────────┴───────────┘
   ✅ Provisioning complete: 13 pending (issues)
```

---

## 🚀 Quick Start

### Prerequisites
- Synology NAS (DSM 7+) or Linux server
- Python 3.10+
- Gitea instance (local or remote)
- MailPlus Server or Gmail account
- BMad Method project

### Installation
```bash
# Clone repository
cd /volume1/tools
git clone https://github.com/khzd/bmad-gitea-bridge.git
cd bmad-gitea-bridge

# Install dependencies
python3.14 -m pip install -r requirements.txt --user

# Configure environment
cp .env.example .env
nano .env  # Add your tokens and credentials

# Configure project
cp examples/medical-project.yaml config/projects/medical.yaml
nano config/projects/medical.yaml  # Adjust paths
```

### First Sync
```bash
# Dry-run (no changes)
python3.14 src/sync.py sync --project medical --dry-run

# Real sync
python3.14 src/sync.py sync --project medical
```

---

## 📚 Documentation

- **[Installation Guide](INSTALL.md)** - Detailed setup instructions
- **[Usage Guide](USAGE.md)** - How to use the tool
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🛠️ Configuration

### Project Configuration (`config/projects/{name}.yaml`)
```yaml
project:
  name: medical
  description: "Medical project with BMad agents"

bmad:
  root: /volume1/concept/bmad
  manifest: _bmad/_config/agent-manifest.csv

gitea:
  url: http://192.168.0.76:3000
  organization: ""  # Empty for personal repos
  repository: projet-medical-main
  admin_token: ${GITEA_ADMIN_TOKEN}

gmail:
  base: bmad
  domain: bmad.local
  enabled: true

sync:
  mode: manual
  provisioning: manual  # or 'auto'
```

### Environment Variables (`.env`)
```bash
GITEA_URL=http://192.168.0.76:3000
GITEA_ADMIN_TOKEN=gto_xxxxxxxxxxxxx
GMAIL_BASE=bmad
GMAIL_DOMAIN=bmad.local
LOG_LEVEL=INFO
```

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Credits

**Authors:**
- **Khaled Z.** (khzd) - Architecture, Infrastructure, Integration
- **Claude** (Anthropic) - Development, Documentation, Collaboration

**Built with:**
- Python 3.14
- Click (CLI)
- Rich (Beautiful tables)
- Requests (API calls)
- PyYAML (Config)
- Gitea API
- MailPlus Server (Synology)

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: khzd19@gmail.com

---

**Made with ❤️ for the BMad Method community**

*Follow the Sun* ☀️Test
Test
