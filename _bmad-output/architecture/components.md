# Components

**File:** `architecture/components.md`  
**Purpose:** Detailed breakdown of system components  
**Last Updated:** 2026-01-22

---

## Component Overview

```
┌─────────────────────────────────────────────────┐
│                  CLI Layer                      │
│            (src/sync.py - Click)                │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼──────┐    ┌────────▼────────┐
│   Core Layer  │    │   Gitea Layer   │
│               │    │                 │
│ - ConfigLoader│    │ - GiteaClient   │
│ - AgentDisc   │    │ - GiteaUsers    │
│ - EmailGen    │    │ - GiteaIssues   │
│ - Provisioner │    │ - GiteaMilestones│
└───────────────┘    └─────────────────┘
        │                     │
        │         ┌───────────┴─────────┐
        │         │                     │
    ┌───▼─────────▼───┐      ┌────────▼────────┐
    │  Parsers Layer   │      │  Utils Layer    │
    │                  │      │                 │
    │ - BaseParser     │      │ - Logger        │
    │ - EpicParser     │      │                 │
    │ - StoryParser    │      │                 │
    └──────────────────┘      └─────────────────┘
```

---

## 1. CLI Layer

### sync.py (Main Entry Point)

**Path:** `src/sync.py`

**Responsibilities:**
- CLI command definition (Click)
- Command orchestration
- Beautiful output (Rich tables)
- Error handling and exit codes

**Commands:**

**sync:**
- Provision agents from manifest
- Assign emails
- Create Gitea users/issues

**version:**
- Display version info

**Key Functions:**
```python
def sync(project: str, dry_run: bool):
    # 1. Load config
    # 2. Discover agents
    # 3. Assign emails
    # 4. Provision Gitea
    # 5. Display results
```

**Dependencies:**
- `core.config_loader.ConfigLoader`
- `core.agent_discovery.AgentDiscovery`
- `core.email_generator.EmailGenerator`
- `core.gitea_provisioner.GiteaProvisioner`
- `gitea.client.GiteaClient`
- `rich.console.Console`
- `click`

---

## 2. Core Layer

### ConfigLoader

**Path:** `src/core/config_loader.py`

**Responsibilities:**
- Load project YAML configs
- Expand environment variables
- Validate configuration
- Return ProjectConfig dataclass

**Key Methods:**
```python
class ConfigLoader:
    def load_project_config(project_name: str) -> ProjectConfig
    def _expand_env_vars(value) -> any
```

**Input:** `config/projects/{project}.yaml`  
**Output:** `ProjectConfig` object

**Error Handling:**
- FileNotFoundError: Config file missing
- ValueError: Invalid config structure
- KeyError: Missing required fields

---

### AgentDiscovery

**Path:** `src/core/agent_discovery.py`

**Responsibilities:**
- Read agent-manifest.csv
- Parse CSV to Agent objects
- Validate agent structure

**Key Methods:**
```python
class AgentDiscovery:
    def __init__(bmad_root: str, manifest_path: str)
    def discover_all_agents() -> List[Agent]
```

**Input:** `{bmad_root}/_bmad/_config/agent-manifest.csv`  
**Output:** `List[Agent]`

**Error Handling:**
- FileNotFoundError: Manifest missing
- csv.Error: Invalid CSV format
- ValueError: Missing required columns

---

### EmailGenerator

**Path:** `src/core/email_generator.py`

**Responsibilities:**
- Generate emails for agents
- Load/save email mappings
- Handle special name transformations

**Key Methods:**
```python
class EmailGenerator:
    def __init__(gmail_base: str, gmail_domain: str, config_path: str)
    def generate_email(agent_name: str) -> str
    def assign_emails_to_agents(agents: List[Agent]) -> List[Agent]
    def _load_mapping()
    def _save_mapping()
```

**Transformations:**
```python
'quick-flow-solo-dev' → 'quickdev'
'tech-writer' → 'techwriter'
'agent-builder' → 'agentbuilder'
```

**Input:** `List[Agent]` (without emails)  
**Output:** `List[Agent]` (with emails)  
**Side Effect:** Saves `{project}.email-mapping.yaml`

---

### GiteaProvisioner

**Path:** `src/core/gitea_provisioner.py`

**Responsibilities:**
- Provision agents in Gitea
- Support manual/auto modes
- Check existing users
- Create issues or users

**Key Methods:**
```python
class GiteaProvisioner:
    def __init__(gitea_client: GiteaClient, mode: str)
    def provision_agent(agent: Agent) -> Dict
    def provision_all_agents(agents: List[Agent]) -> Dict
    def _create_provisioning_issue(agent, username) -> Dict
    def _create_user_auto(agent, username) -> Dict
    def _issue_exists_for_agent(username) -> bool
```

**Modes:**
- **manual**: Create Gitea issue with instructions
- **auto**: Create Gitea user directly

**Logic:**
```python
if user_exists:
    return {"status": "exists"}
elif mode == "manual":
    if issue_exists:
        return {"status": "pending", "issue_exists": True}
    else:
        create_issue()
        return {"status": "pending", "issue_number": N}
elif mode == "auto":
    create_user()
    return {"status": "created", "user_id": N}
```

---

## 3. Gitea Layer

### GiteaClient

**Path:** `src/gitea/client.py`

**Responsibilities:**
- HTTP communication with Gitea API
- Authentication (Bearer tokens)
- Request/response handling
- Error handling

**Key Methods:**
```python
class GiteaClient:
    def __init__(base_url, token, organization, repository, ...)
    def _make_request(method, endpoint, data, params) -> Any
    def get_user(username) -> Dict
    def user_exists(username) -> bool
    def create_user(username, email, password, ...) -> Dict
    def create_issue(title, body, labels, assignee) -> Dict
    def list_issues(state) -> List[Dict]
    def get_current_user() -> Dict
    def test_connection() -> bool
```

**Authentication:**
```python
headers = {
    'Authorization': f'token {self.token}',
    'Content-Type': 'application/json'
}
```

**Error Handling:**
- GiteaAPIError: HTTP errors
- RequestException: Network errors
- 404: User/resource not found
- 422: Validation errors

---

### GiteaUsers

**Path:** `src/gitea/users.py`

**Responsibilities:**
- User-specific operations
- Idempotent user creation

**Key Methods:**
```python
class GiteaUsers:
    def get_user(username) -> Optional[Dict]
    def user_exists(username) -> bool
    def create_user(username, email, password, full_name) -> Dict
    def ensure_user_exists(...) -> Dict
```

---

### GiteaIssues

**Path:** `src/gitea/issues.py`

**Responsibilities:**
- Issue management
- Story/epic creation

**Key Methods:**
```python
class GiteaIssues:
    def create_issue(title, body, labels, assignee, milestone) -> Dict
    def create_story_issue(story_title, story_body, assignee) -> Dict
    def create_epic_tracking_issue(epic_title, description, stories) -> Dict
```

---

### GiteaMilestones

**Path:** `src/gitea/milestones.py`

**Responsibilities:**
- Milestone management
- Epic tracking

**Key Methods:**
```python
class GiteaMilestones:
    def create_milestone(title, description, due_date) -> Dict
    def create_epic_milestone(epic_title, epic_description) -> Dict
```

---

## 4. Parsers Layer

### BaseParser

**Path:** `src/parsers/base_parser.py`

**Responsibilities:**
- Abstract base for artifact parsers
- Common markdown parsing utilities

**Key Methods:**
```python
class BaseParser(ABC):
    def read_file() -> str
    def extract_yaml_frontmatter() -> Optional[Dict]
    def extract_title() -> str
    def extract_sections() -> Dict[str, str]
    @abstractmethod
    def parse() -> Dict[str, Any]
```

---

### EpicParser

**Path:** `src/parsers/epic_parser.py`

**Responsibilities:**
- Parse epic markdown files
- Extract metadata, stories, AC

**Key Methods:**
```python
class EpicParser(BaseParser):
    def parse() -> Dict
    def _extract_stories() -> List[str]
    def _extract_acceptance_criteria() -> List[str]
```

**Output:**
```python
{
    'title': str,
    'description': str,
    'stories': List[str],
    'acceptance_criteria': List[str],
    'sections': Dict[str, str],
    'frontmatter': Dict,
    'file_path': Path
}
```

---

### StoryParser

**Path:** `src/parsers/story_parser.py`

**Responsibilities:**
- Parse story markdown files
- Extract tasks, AC, epic reference

**Key Methods:**
```python
class StoryParser(BaseParser):
    def parse() -> Dict
    def _extract_story_id() -> str
    def _extract_acceptance_criteria() -> List[str]
    def _extract_tasks() -> List[Dict]
    def _extract_epic_reference() -> str
```

**Output:**
```python
{
    'title': str,
    'story_id': str,
    'description': str,
    'acceptance_criteria': List[str],
    'tasks': List[Dict],
    'epic': str,
    'assignee': str,
    'sections': Dict[str, str],
    'frontmatter': Dict,
    'file_path': Path
}
```

---

## 5. Utils Layer

### Logger

**Path:** `src/utils/logger.py`

**Responsibilities:**
- Logging configuration
- File and console handlers
- Log formatting

**Key Function:**
```python
def setup_logger(
    name: str,
    level: str,
    log_file: Optional[Path],
    console: bool
) -> logging.Logger
```

**Format:**
```
2026-01-22 10:30:00 - bmad-gitea-bridge - INFO - Message
```

---

## Component Dependencies

```
sync.py
├── ConfigLoader
├── AgentDiscovery
├── EmailGenerator
├── GiteaProvisioner
│   └── GiteaClient
│       ├── GiteaUsers
│       ├── GiteaIssues
│       └── GiteaMilestones
├── EpicParser → BaseParser
├── StoryParser → BaseParser
└── Logger
```

---

## Future Components (Roadmap)

### Phase 1: Bidirectional Sync (6 months)

**WebhookListener:**
- Path: `src/webhooks/listener.py`
- Responsibilities: Receive Gitea webhooks, trigger BMAD updates

**EventProcessor:**
- Path: `src/webhooks/processor.py`
- Responsibilities: Process webhook events, update BMAD artifacts

### Phase 2: Multi-Platform (9 months)

**JiraAdapter:**
- Path: `src/adapters/jira_adapter.py`
- Responsibilities: Jira API integration

**GitHubAdapter:**
- Path: `src/adapters/github_adapter.py`
- Responsibilities: GitHub API integration

**PlatformAdapterInterface:**
- Path: `src/adapters/base_adapter.py`
- Responsibilities: Abstract adapter interface

### Phase 3: Community Scale (12 months)

**Dashboard:**
- Path: `src/dashboard/app.py`
- Responsibilities: Metrics, analytics, monitoring

**PluginManager:**
- Path: `src/plugins/manager.py`
- Responsibilities: Load/manage third-party plugins

---

## Document Navigation

**Previous:** [Data Models](data-models.md)  
**Next:** [External APIs](external-apis.md)

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)  
**Last Updated:** 2026-01-22
