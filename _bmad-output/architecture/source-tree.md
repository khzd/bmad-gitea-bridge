# Source Tree

**File:** `architecture/source-tree.md`  
**Purpose:** Repository structure and organization  
**Last Updated:** 2026-01-22

---

## Directory Structure

```
bmad-gitea-bridge/
├── .cache/                     # Cache directory (gitignored)
├── .env                        # Environment variables (gitignored)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── CONTRIBUTORS.md             # Contributors list
├── INSTALL.md                  # Installation guide
├── LICENSE                     # MIT License
├── README.md                   # Project overview
├── USAGE.md                    # Usage documentation
├── config/                     # Configuration files
│   └── projects/               # Project-specific configs
│       ├── medical.yaml        # Example project
│       ├── medical.email-mapping.yaml  # Email mappings
│       └── test.yaml           # Test config (gitignored)
├── docs/                       # Documentation
│   ├── architecture.md         # Architecture overview
│   └── images/                 # Documentation images
├── examples/                   # Example configurations
│   └── medical-project.yaml    # Template config
├── logs/                       # Log files (gitignored)
│   └── sync.log                # Sync logs
├── requirements.txt            # Python dependencies
├── scripts/                    # Utility scripts
│   └── setup.sh                # Setup script
├── src/                        # Source code
│   ├── __init__.py
│   ├── sync.py                 # Main CLI entry point
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── agent_discovery.py  # Agent discovery
│   │   ├── config_loader.py    # Config management
│   │   ├── email_generator.py  # Email assignment
│   │   └── gitea_provisioner.py  # Gitea provisioning
│   ├── gitea/                  # Gitea integration
│   │   ├── __init__.py
│   │   ├── client.py           # API client
│   │   ├── issues.py           # Issue management
│   │   ├── milestones.py       # Milestone management
│   │   ├── users.py            # User management
│   │   └── wiki.py             # Wiki management (future)
│   ├── parsers/                # Artifact parsers
│   │   ├── __init__.py
│   │   ├── base_parser.py      # Abstract base
│   │   ├── epic_parser.py      # Epic parser
│   │   └── story_parser.py     # Story parser
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── logger.py           # Logging setup
└── tests/                      # Test suite (future)
    ├── __init__.py
    ├── fixtures/               # Test fixtures
    └── test_*.py               # Test files
```

---

## File Purposes

### Root Level
- `.env` - Secrets (Gitea token, etc.)
- `README.md` - Project overview, quick start
- `INSTALL.md` - Detailed installation
- `USAGE.md` - Usage guide
- `CHANGELOG.md` - Version history
- `requirements.txt` - Python dependencies

### Configuration
- `config/projects/{name}.yaml` - Project configs
- `config/projects/{name}.email-mapping.yaml` - Email mappings
- `.env` - Secrets and environment variables

### Source Code
- `src/sync.py` - CLI entry point
- `src/core/` - Business logic
- `src/gitea/` - Gitea API layer
- `src/parsers/` - Markdown parsers
- `src/utils/` - Utilities

### Documentation
- `docs/` - Additional documentation
- `examples/` - Example configurations

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
