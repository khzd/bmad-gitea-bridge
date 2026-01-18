# 📜 Changelog

All notable changes to BMad-Gitea-Bridge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Automatic Gitea user updates when agent metadata changes
- Label management for Gitea issues
- Wiki synchronization from BMad documentation
- Milestone tracking for epics
- Webhook support for real-time updates
- GitHub Actions integration

---

## [0.1.0] - 2026-01-17

### 🎉 Initial Release

First public release of BMad-Gitea-Bridge!

### ✨ Added

#### Core Features
- **Agent Discovery**: Automatic discovery of BMad agents from `agent-manifest.csv`
- **Email Assignment**: Generate unique emails for each agent (MailPlus/Gmail support)
- **Gitea Provisioning**: Create Gitea users via issues (manual mode) or directly (auto mode)
- **Multi-Project Support**: Configure and sync multiple BMad projects independently

#### CLI Interface
- `sync` command with `--project` and `--dry-run` options
- `version` command
- Beautiful CLI output with Rich tables
- Comprehensive logging

#### Configuration
- YAML-based project configuration
- Environment variable support (`.env`)
- Email mapping persistence
- Flexible provisioning modes (manual/auto)

#### Infrastructure
- MailPlus Server integration with alias support
- Gitea API v1 client
- SMTP configuration for email notifications
- Error handling and validation

#### Documentation
- Complete README.md
- Detailed INSTALL.md guide
- Comprehensive USAGE.md
- CONTRIBUTING.md for contributors
- MIT License

### 🔧 Technical

#### Architecture
```
src/
├── core/
│   ├── agent_discovery.py    # BMad agent discovery
│   ├── config_loader.py       # Configuration management
│   ├── email_generator.py     # Email assignment
│   └── gitea_provisioner.py   # Gitea provisioning logic
├── gitea/
│   ├── client.py              # Gitea API client
│   ├── users.py               # User management
│   └── issues.py              # Issue creation
└── sync.py                    # Main CLI entry point
```

#### Dependencies
- Python 3.10+ (tested with 3.14.2)
- click 8.1.7 (CLI framework)
- rich 13.7.0 (Terminal UI)
- requests 2.31.0 (HTTP client)
- PyYAML 6.0.1 (YAML parsing)
- python-dotenv 1.0.0 (Environment variables)

#### Platforms Tested
- ✅ Synology DSM 7.2 (NAS)
- ✅ Ubuntu 22.04 LTS
- ✅ Debian 12

#### Gitea Versions Tested
- ✅ Gitea 1.21.5
- ✅ Gitea 1.20.x

### 🐛 Bug Fixes
- Fixed `urljoin()` issue causing `/v1` to disappear from API URLs
- Fixed label format error (HTTP 422) in issue creation
- Corrected SMTP configuration for Gitea 1.19+ (`PROTOCOL` instead of `MAILER_TYPE`)

### 📝 Known Limitations
- Labels not yet supported in issues (commented out in code)
- User updates not implemented (only creation)
- No webhook support yet
- Single-threaded sync (sequential processing)

### 🙏 Contributors
- **Khaled Z.** (khzd19) - Project lead, architecture, infrastructure
- **Claude** (Anthropic) - Development, documentation, collaboration

### 📊 Statistics
- **29 files** created
- **~2,000 lines** of Python code
- **13 BMad agents** synchronized in test project
- **13 Gitea issues** created automatically
- **20 email aliases** configured in MailPlus
- **4 hours** of intense development session

### 🎯 Initial Use Case
Medical project with BMad Method agents requiring:
- HIPAA/RGPD compliance (MailPlus on-premise)
- Gitea for version control
- Automatic agent provisioning
- Email notifications

---

## [0.0.1] - 2026-01-17

### 🌱 Project Inception
- Initial project structure created
- Basic agent discovery implemented
- Email generation prototype

---

## Version Format
```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes
```

**Examples:**
- `0.1.0` → `0.2.0` : New feature (wiki sync)
- `0.1.0` → `0.1.1` : Bug fix
- `0.9.0` → `1.0.0` : Stable release (breaking changes)

---

## Links

- [GitHub Repository](https://github.com/khzd19/bmad-gitea-bridge)
- [Issue Tracker](https://github.com/khzd19/bmad-gitea-bridge/issues)
- [Documentation](README.md)

---

**Maintained by:** Khaled Z. & Claude (Anthropic)  
**License:** MIT