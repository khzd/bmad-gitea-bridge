# Tech Stack

**File:** `architecture/tech-stack.md`  
**Purpose:** Technologies, libraries, tools, and infrastructure  
**Last Updated:** 2026-01-22

---

## Core Technologies

### Programming Language

**Python 3.14**
- **Version:** 3.14.2 (recommended), 3.10+ minimum
- **Rationale:** Strategic choice for maintainability vs shell scripts
- **Features Used:**
  - Type hints (gradual typing)
  - Dataclasses
  - f-strings
  - Pathlib
  - Context managers

### CLI Framework

**Click 8.1.7**
- **Purpose:** Command-line interface structure
- **Features:**
  - Declarative commands
  - Automatic help generation
  - Type validation
  - Composable commands

### Terminal UI

**Rich 13.7.0**
- **Purpose:** Beautiful terminal output
- **Features:**
  - Tables (formatted output)
  - Progress bars (future)
  - Syntax highlighting
  - Colors and styling

### Configuration

**PyYAML 6.0.1**
- **Purpose:** YAML parsing for project configs
- **Features:**
  - safe_load (security)
  - Hierarchical data
  - Environment variable expansion

### HTTP Client

**Requests 2.31.0**
- **Purpose:** API calls to Gitea/Jira/GitHub
- **Features:**
  - Session management
  - Retry logic (custom)
  - Error handling
  - SSL verification control

### Environment Variables

**python-dotenv 1.0.0**
- **Purpose:** Load .env files
- **Features:**
  - Secret management
  - Environment isolation
  - Override support

---

## Development Tools

### Version Control

**Git 2.x+**
- **Purpose:** Source control and audit trail
- **Workflow:** Feature branches, PRs, semantic commits
- **Hosting:** GitHub (public), Gitea (internal)

### Code Editor

**VS Code** (primary)
- **Extensions:**
  - Python (Microsoft)
  - YAML
  - Markdown All in One
  - GitLens

### Linting (Future)

**flake8**
- **Purpose:** PEP 8 compliance
- **Config:** `.flake8` or `setup.cfg`

**black**
- **Purpose:** Auto-formatting
- **Config:** `pyproject.toml`

### Testing (Future)

**pytest**
- **Purpose:** Unit and integration tests
- **Plugins:**
  - pytest-cov (coverage)
  - pytest-mock (mocking)
  - pytest-xdist (parallel)

---

## Infrastructure

### Deployment Platforms

**Primary: Synology NAS**
- **OS:** DSM 7.2
- **Python:** 3.14 via SynoCommunity
- **Storage:** /volume1/tools/
- **Network:** Local network access

**Secondary: Linux Servers**
- **OS:** Ubuntu 22.04, Debian 12
- **Python:** 3.10+ via apt
- **Deployment:** Git clone + pip install

### Email Infrastructure

**MailPlus Server** (Synology)
- **Purpose:** Email generation for agents
- **Protocol:** SMTP (port 25 local)
- **Domain:** bmad.local (custom)
- **Aliases:** Configured manually

**Alternative: Gmail**
- **Purpose:** Email aliases
- **Format:** bmad-{agent}@gmail.com
- **Auth:** App passwords

### Platform APIs

**Gitea 1.21.5+**
- **API:** REST API v1
- **Auth:** Bearer tokens
- **Endpoints:**
  - /api/v1/admin/users
  - /api/v1/repos
  - /api/v1/issues
  - /api/v1/milestones

**Future: Jira Cloud/Server**
- **API:** REST API v3
- **Auth:** API tokens or OAuth
- **Features:** Issues, Projects, Users

**Future: GitHub**
- **API:** REST API v3, GraphQL v4
- **Auth:** Personal access tokens
- **Features:** Repos, Issues, Milestones

---

## Dependencies

### Production Dependencies

```
requests>=2.31.0
PyYAML>=6.0.1
python-dotenv>=1.0.0
click>=8.1.7
rich>=13.7.0
```

### Development Dependencies (Future)

```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
black>=23.7.0
flake8>=6.1.0
mypy>=1.5.0
```

### Installation

**On Synology NAS:**
```bash
python3.14 -m pip install -r requirements.txt --break-system-packages --user
```

**On Standard Linux:**
```bash
python3.14 -m pip install -r requirements.txt --user
```

---

## Technology Versions

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.14.2 | ✅ Current |
| Click | 8.1.7 | ✅ Current |
| Rich | 13.7.0 | ✅ Current |
| PyYAML | 6.0.1 | ✅ Current |
| Requests | 2.31.0 | ✅ Current |
| python-dotenv | 1.0.0 | ✅ Current |
| Gitea API | v1 | ✅ Stable |
| Jira API | v3 | ⏳ Future |
| GitHub API | v3/v4 | ⏳ Future |

---

## Technology Decision Rationale

### Why Python 3.14?

**Pros:**
- ✅ Maintainable vs shell
- ✅ Rich ecosystem
- ✅ Type hints
- ✅ Modern features
- ✅ Enterprise-ready

**Cons:**
- ➖ Requires installation
- ➖ Slower than compiled languages
- ➖ Global interpreter lock (GIL)

**Decision:** Benefits outweigh cons for automation tool

### Why Click Over argparse?

**Pros:**
- ✅ Declarative syntax
- ✅ Automatic help
- ✅ Composable commands
- ✅ Type validation

**Cons:**
- ➖ Additional dependency
- ➖ Learning curve

**Decision:** Developer experience worth the dependency

### Why Rich Over plain print?

**Pros:**
- ✅ Professional output
- ✅ Tables, progress bars
- ✅ Better UX
- ✅ Colors/formatting

**Cons:**
- ➖ Additional dependency
- ➖ Terminal compatibility

**Decision:** UX critical for CLI tool adoption

---

## Future Technology Additions

### Phase 1: Bidirectional Sync (6 months)

**Webhook Listener:**
- **Framework:** Flask or FastAPI
- **Purpose:** Receive Gitea webhooks
- **Deployment:** systemd service

**Event Queue (optional):**
- **Technology:** Redis or RabbitMQ
- **Purpose:** Reliable event processing
- **Usage:** Async processing

### Phase 2: Multi-Platform (9 months)

**Jira Library:**
- **jira-python** or **atlassian-python-api**
- **Purpose:** Jira API abstraction

**GitHub Library:**
- **PyGithub** or **ghapi**
- **Purpose:** GitHub API abstraction

### Phase 3: Community Scale (12 months)

**Database (optional):**
- **PostgreSQL**
- **Purpose:** Analytics, metrics, cache

**Web Framework (optional):**
- **FastAPI**
- **Purpose:** Self-service portal

**Message Queue:**
- **Celery + Redis**
- **Purpose:** Background tasks

---

## Technology Constraints

### Python Version Compatibility

**Minimum:** Python 3.10  
**Recommended:** Python 3.14  
**Not Supported:** Python 2.x, 3.9 and below

**Rationale:**
- Type hints improvements (3.10+)
- Match statements (3.10+)
- Performance improvements (3.14)
- Long-term support

### Platform Compatibility

**Supported:**
- ✅ Linux (Ubuntu, Debian, RHEL)
- ✅ Synology DSM 7+
- ✅ macOS 12+

**Future Support:**
- ⏳ Windows (WSL recommended)
- ⏳ Docker containers

### Network Requirements

**Required:**
- Internet access (for pip install)
- Access to Gitea instance (HTTP/HTTPS)
- Access to MailPlus SMTP (optional)

**Firewall Rules:**
- Outbound HTTP/HTTPS (ports 80, 443)
- Outbound SMTP (port 25 or 587)
- Inbound webhooks (future: port 5000+)

---

## Document Navigation

**Previous:** [High-Level Architecture](./high-level-architecture.md)  
**Next:** [Data Models](./data-models.md)

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)  
**Review Status:** Draft  
**Last Updated:** 2026-01-22
