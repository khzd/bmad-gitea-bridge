# High-Level Architecture

**File:** `architecture/high-level-architecture.md`  
**Purpose:** System overview, component diagram, architectural patterns  
**Last Updated:** 2026-01-22

---

## System Overview

BMAD-Gitea-Bridge is a **CLI-based automation tool** that bridges BMAD Method artifacts with infrastructure management platforms (Gitea, future: Jira/GitHub).

### Architectural Style

**Style:** Modular Pipeline Architecture with Adapter Pattern

**Characteristics:**
- **Stateless:** Each operation is independent
- **Configuration-driven:** Behavior controlled by YAML configs
- **Idempotent:** Safe to re-run operations
- **Extensible:** New adapters can be plugged in

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User (CLI)                                │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ sync command │ │sync-artifacts│ │    (future)  │
│              │ │   command    │ │   commands   │
└──────┬───────┘ └──────┬───────┘ └──────────────┘
       │                │
       └────────┬───────┘
                │
        ┌───────▼────────┐
        │ Core Orchestrator│
        │    (sync.py)     │
        └───────┬──────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Config │ │ Agent  │ │ Email  │
│ Loader │ │Discovery│ │Generator│
└────┬───┘ └───┬────┘ └───┬────┘
     │         │          │
     │         └──────┬───┘
     │                │
     ▼                ▼
┌──────────────────────────────┐
│   Gitea Provisioner          │
│   (manual/auto modes)        │
└────────────┬─────────────────┘
             │
     ┌───────┼────────┐
     │       │        │
     ▼       ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Epic   │ │ Story  │ │ (future)│
│ Syncer │ │ Syncer │ │ Syncers │
└────┬───┘ └───┬────┘ └────────┘
     │         │
     └────┬────┘
          │
    ┌─────▼──────────┐
    │  Gitea Client   │
    │  (API Wrapper)  │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Gitea Server   │
    │  (REST API)     │
    └─────────────────┘
```

---

## Data Flow

### Primary Flow: Agent Provisioning

```
1. User runs: python src/sync.py sync --project medical

2. ConfigLoader
   ├─ Loads: config/projects/medical.yaml
   ├─ Resolves: .env variables
   └─ Returns: ProjectConfig object

3. AgentDiscovery
   ├─ Reads: {bmad_root}/_bmad/_config/agent-manifest.csv
   ├─ Parses: Agent metadata (name, role, module, icon)
   └─ Returns: List[Agent]

4. EmailGenerator
   ├─ Checks: config/projects/medical.email-mapping.yaml
   ├─ Generates: bmad-{agent}@{domain} for new agents
   ├─ Saves: Updated mapping file
   └─ Returns: List[Agent] with emails assigned

5. GiteaProvisioner
   ├─ Mode check: manual or auto?
   ├─ For each agent:
   │  ├─ GiteaClient.user_exists(username)?
   │  ├─ IF exists: skip
   │  ├─ IF manual: create_issue(provisioning instructions)
   │  └─ IF auto: create_user(username, email, password)
   └─ Returns: ProvisioningResults

6. Output
   ├─ Rich tables: Agents discovered, emails assigned, provisioning status
   ├─ Logs: Detailed operation log
   └─ Exit: 0 (success) or 1 (error)
```

### Secondary Flow: Artifact Synchronization

```
1. User runs: python src/sync.py sync-artifacts --project medical

2. ConfigLoader
   └─ Same as primary flow

3. EpicSyncer
   ├─ Discovers: {artifacts}/epics/*.md
   ├─ Parses: Epic metadata (title, description, due_date)
   ├─ For each epic:
   │  ├─ GiteaClient.milestone_exists(title)?
   │  ├─ IF exists: skip (idempotent)
   │  └─ IF not: create_milestone(title, description, due_date)
   └─ Returns: EpicSyncResults

4. StorySyncer
   ├─ Discovers: {artifacts}/stories/*.md
   ├─ Parses: Story metadata (title, description, assignee, epic, AC, tasks)
   ├─ For each story:
   │  ├─ GiteaClient.issue_exists(title)?
   │  ├─ IF exists: skip (idempotent)
   │  └─ IF not: create_issue(title, body, milestone, assignee, checklists)
   └─ Returns: StorySyncResults

5. Output
   ├─ Rich tables: Epics synced, stories synced
   ├─ Logs: Detailed sync log
   └─ Exit: 0 (success) or 1 (error)
```

---

## Architectural Patterns

### 1. Adapter Pattern (Platform Abstraction)

**Intent:** Decouple core business logic from platform-specific APIs

**Current Implementation:**

```python
# Abstract interface (future)
class PlatformAdapter:
    def user_exists(username: str) -> bool
    def create_user(username: str, email: str, ...) -> User
    def create_milestone(title: str, ...) -> Milestone
    def create_issue(title: str, ...) -> Issue

# Concrete implementations
class GiteaAdapter(PlatformAdapter):
    # Gitea-specific API calls
    
class JiraAdapter(PlatformAdapter):  # Future
    # Jira-specific API calls
    
class GitHubAdapter(PlatformAdapter):  # Future
    # GitHub-specific API calls
```

**Benefits:**
- ✅ Easy to add new platforms (Jira, GitHub)
- ✅ Core logic unchanged when switching platforms
- ✅ Test with mock adapters

### 2. Repository Pattern (Data Access)

**Intent:** Abstract data storage/retrieval from business logic

**Implementation:**

```python
# ConfigLoader: Abstracts YAML file access
config = ConfigLoader().load_project_config("medical")

# EmailGenerator: Abstracts email mapping storage
generator = EmailGenerator(config_path="...")
agents = generator.assign_emails_to_agents(agents)

# AgentDiscovery: Abstracts CSV parsing
discovery = AgentDiscovery(bmad_root, manifest_path)
agents = discovery.discover_all_agents()
```

**Benefits:**
- ✅ Easy to change storage format (CSV → JSON → DB)
- ✅ Business logic doesn't know about files
- ✅ Test with in-memory repositories

### 3. Command Pattern (CLI)

**Intent:** Encapsulate operations as command objects

**Implementation:**

```python
# Click commands
@cli.command()
def sync(project: str, dry_run: bool):
    # Encapsulates agent provisioning workflow
    
@cli.command()
def sync_artifacts(project: str, dry_run: bool):
    # Encapsulates artifact synchronization workflow
```

**Benefits:**
- ✅ Commands composable and reusable
- ✅ Easy to add new commands
- ✅ Clear separation of concerns

### 4. Strategy Pattern (Provisioning Modes)

**Intent:** Select algorithm at runtime based on configuration

**Implementation:**

```python
class GiteaProvisioner:
    def __init__(self, mode: str):  # 'manual' or 'auto'
        self.mode = mode
    
    def provision_agent(self, agent):
        if self.mode == 'manual':
            return self._create_provisioning_issue(agent)
        elif self.mode == 'auto':
            return self._create_user_auto(agent)
```

**Benefits:**
- ✅ Different provisioning strategies without code duplication
- ✅ Easy to add new modes (e.g., 'hybrid')
- ✅ Configuration-driven behavior

### 5. Pipeline Pattern (Workflow)

**Intent:** Process data through a series of transformations

**Implementation:**

```
Input → Discovery → Email Assignment → Provisioning → Output
     ↓            ↓                   ↓              ↓
   Config     Agents            Agents+Emails   Results
```

**Benefits:**
- ✅ Clear data flow
- ✅ Each stage independent and testable
- ✅ Easy to add/remove stages

---

## System Boundaries

### In Scope

**Current (v0.2.0):**
- CLI interface (Click + Rich)
- Agent discovery from CSV
- Email generation and mapping
- Gitea user provisioning (manual/auto)
- Gitea repo creation
- Epic → Milestone sync
- Story → Issue sync
- Multi-project configuration
- Logging and audit trail

**Future (Roadmap):**
- Gitea → BMAD sync (bidirectional)
- Jira adapter (9 months)
- GitHub adapter (9 months)
- Dashboard and metrics
- Webhooks
- Multi-instance support
- Plugin architecture

### Out of Scope

**Explicitly NOT in Scope:**
- Web UI (CLI-first philosophy)
- BMAD Method itself (integration only)
- Gitea installation/management
- MailPlus configuration
- User training (documentation only)
- Real-time collaboration features
- Mobile apps

---

## Key Architectural Decisions

### Decision 1: Python Over Shell

**Context:** Need automation tool, choice between shell scripts and Python

**Decision:** Python 3.14+

**Rationale:**
- ✅ "Shell is challengy to maintain" (stakeholder quote)
- ✅ Better error handling
- ✅ Rich ecosystem (Click, Rich, PyYAML, Requests)
- ✅ Type hints for robustness
- ✅ Testable and refactorable

**Consequences:**
- ➕ Easier to maintain long-term
- ➕ Better developer experience
- ➖ Requires Python installation
- ➖ Slightly more boilerplate than shell

### Decision 2: CLI-First, No Web UI

**Context:** Interface choice for automation tool

**Decision:** Command-line interface only (no web UI)

**Rationale:**
- ✅ Target users: DevOps/developers comfortable with CLI
- ✅ Automation-friendly (scripts, CI/CD)
- ✅ Faster development (no frontend complexity)
- ✅ Better for batch operations

**Consequences:**
- ➕ Simple, focused tool
- ➕ Easy CI/CD integration
- ➖ Less accessible to non-technical users
- ➖ No visual dashboards (future enhancement)

### Decision 3: Configuration Over Code

**Context:** Multi-project support approach

**Decision:** YAML configuration files per project

**Rationale:**
- ✅ No code changes for new projects
- ✅ Human-readable configs
- ✅ Environment variable expansion
- ✅ Template-driven customization

**Consequences:**
- ➕ Highly flexible
- ➕ Non-developers can configure
- ➖ Configuration validation needed
- ➖ Schema documentation required

### Decision 4: Manual Provisioning Default

**Context:** Safety vs automation tradeoff

**Decision:** Default mode is `manual` (creates issues), `auto` is opt-in

**Rationale:**
- ✅ Governance and compliance first
- ✅ Manual review before user creation
- ✅ Audit trail via issues
- ✅ Safe for production

**Consequences:**
- ➕ Safe, compliant, auditable
- ➕ CISO approval easier
- ➖ Extra manual step required
- ➖ Slower for dev environments

### Decision 5: Idempotent Operations

**Context:** Reliability and retry handling

**Decision:** All operations check before create/update

**Rationale:**
- ✅ Safe to re-run after failures
- ✅ Partial failure recovery
- ✅ Concurrent execution safety
- ✅ Developer experience (no cleanup needed)

**Consequences:**
- ➕ Robust and reliable
- ➕ Error recovery simplified
- ➖ Extra API calls (existence checks)
- ➖ Slightly slower execution

### Decision 6: Adapter Pattern for Platforms

**Context:** Need to support Gitea, Jira, GitHub

**Decision:** Abstract adapter interface with concrete implementations

**Rationale:**
- ✅ Easy to add new platforms
- ✅ Core logic platform-agnostic
- ✅ Test with mock adapters
- ✅ Swap platforms without business logic changes

**Consequences:**
- ➕ Highly extensible
- ➕ Clean separation of concerns
- ➖ Extra abstraction layer
- ➖ Initial implementation overhead

---

## Non-Functional Characteristics

### Performance

**Current:**
- Single project provisioning: < 5 minutes
- Agent discovery: < 10 seconds
- Artifact sync (100 stories): < 2 minutes

**Target:**
- Batch provisioning (50 projects): < 4 hours
- Concurrent operations: 10 projects simultaneously
- Scaling: 100+ projects configured

### Reliability

**Current:**
- Idempotent operations (safe re-run)
- Error logging (detailed)
- Graceful degradation (partial failures OK)

**Target:**
- Uptime: > 99% (fallback manual if down)
- MTTR: < 1 hour
- Retry logic (network failures, rate limits)

### Security

**Current:**
- Secrets in .env (not hardcoded)
- API tokens (admin rights)
- Logs mask sensitive data
- Audit trail (complete)

**Target:**
- Token rotation support
- RBAC integration (future)
- Security audit certification

### Maintainability

**Current:**
- Python 3.14+ (modern)
- Modular architecture
- Docstrings (some)
- Documentation (comprehensive)

**Target:**
- Code coverage > 80%
- Type hints (complete)
- Automated tests (CI/CD)
- Contribution guide

---

## Technology Choices Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.14 | Maintainable, rich ecosystem, strategic |
| CLI Framework | Click | Declarative, composable, automatic help |
| Terminal UI | Rich | Beautiful tables, professional output |
| Config | PyYAML | Human-readable, hierarchical, standard |
| HTTP Client | Requests | Simple, reliable, well-documented |
| Testing | pytest | Industry standard, powerful, extensible |
| Linting | flake8, black | Code quality, consistency |
| Version Control | Git | Standard, audit trail, collaboration |

---

## Future Architecture Evolution

### Phase 1: Bidirectional Sync (6 months)

**Addition:** Gitea → BMAD sync layer

```
┌────────────────┐
│  Gitea Events  │ (webhooks)
└────────┬───────┘
         │
    ┌────▼────┐
    │ Webhook │
    │ Listener│
    └────┬────┘
         │
┌────────▼────────┐
│ Event Processor │
│ (Gitea → BMAD)  │
└────────┬────────┘
         │
    ┌────▼────┐
    │  BMAD   │
    │ Agents  │
    └─────────┘
```

### Phase 2: Multi-Platform (9 months)

**Addition:** Jira and GitHub adapters

```
┌─────────────┐
│ Core Logic  │
└──────┬──────┘
       │
┌──────┴──────────────────┐
│                         │
▼                         ▼
┌────────────┐   ┌────────────┐
│   Gitea    │   │    Jira    │
│  Adapter   │   │   Adapter  │
└────────────┘   └────────────┘
                         │
                    ┌────▼────┐
                    │  GitHub │
                    │ Adapter │
                    └─────────┘
```

### Phase 3: Community Scale (12 months)

**Addition:** Plugin architecture and self-service

```
┌──────────────────┐
│  Web Portal      │ (self-service)
└────────┬─────────┘
         │
┌────────▼──────────┐
│   Plugin System   │
└────────┬──────────┘
         │
┌────────┴───────────┐
│                    │
▼                    ▼
┌─────────────┐   ┌──────────────┐
│   Core      │   │  3rd Party   │
│  Plugins    │   │   Plugins    │
└─────────────┘   └──────────────┘
```

---

## Document Navigation

**Previous:** [Introduction](./introduction.md)  
**Next:** [Tech Stack](./tech-stack.md)

**Related:**
- [Components](./components.md) - Detailed component descriptions
- [External APIs](./external-apis.md) - API integration details

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)  
**Review Status:** Draft  
**Last Updated:** 2026-01-22
