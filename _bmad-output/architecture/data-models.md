# Data Models

**File:** `architecture/data-models.md`  
**Purpose:** Data structures, schemas, and formats  
**Last Updated:** 2026-01-22

---

## Configuration Models

### Project Configuration (YAML)

**File:** `config/projects/{project}.yaml`

```yaml
project:
  name: string                    # Project identifier
  description: string            # Human-readable description

bmad:
  root: path                     # BMAD project root directory
  manifest: path                 # agent-manifest.csv location

gitea:
  url: string                    # Gitea instance URL
  organization: string           # Organization name (optional)
  repository: string             # Repository name
  admin_token: string            # Admin API token (from .env)

gmail:
  base: string                   # Email base (e.g., "bmad")
  domain: string                 # Email domain (e.g., "bmad.local")
  enabled: boolean               # Enable email features

sync:
  provisioning: enum             # "manual" or "auto"

logging:
  level: enum                    # DEBUG, INFO, WARNING, ERROR
```

**Example:**
```yaml
project:
  name: medical
  description: "Medical AI Project"

bmad:
  root: /volume1/concept/bmad
  manifest: _bmad/_config/agent-manifest.csv

gitea:
  url: http://192.168.0.76:3000
  organization: ""
  repository: projet-medical-main
  admin_token: ${GITEA_ADMIN_TOKEN}

gmail:
  base: bmad
  domain: bmad.local
  enabled: true

sync:
  provisioning: manual

logging:
  level: INFO
```

---

## Agent Manifest (CSV)

**File:** `{bmad_root}/_bmad/_config/agent-manifest.csv`

### Schema

```csv
"name","displayName","title","icon","role","module","path"
```

**Fields:**
- `name`: Agent identifier (e.g., "pm", "dev")
- `displayName`: Human-readable name (e.g., "John")
- `title`: Job title (e.g., "Product Manager")
- `icon`: Emoji icon (e.g., "📋")
- `role`: Agent role (e.g., "planning")
- `module`: BMAD module (e.g., "bmm")
- `path`: Agent directory path

**Example:**
```csv
"pm","John","Product Manager","📋","planning","bmm","/agents/pm"
"dev","Amelia","Senior Developer","💻","implementation","bmm","/agents/dev"
"tea","Murat","Test Engineer","🧪","testing","bmm","/agents/tea"
```

### Python Dataclass

```python
@dataclass
class Agent:
    name: str              # Agent identifier
    display_name: str      # Human-readable name
    title: str             # Job title
    icon: str              # Emoji icon
    role: str              # Agent role
    module: str            # BMAD module
    path: str              # Agent directory
    email: str = None      # Assigned email (generated)
    gitea_username: str = None  # Gitea username (generated)
```

---

## Email Mapping (YAML)

**File:** `config/projects/{project}.email-mapping.yaml`

### Schema

```yaml
agent_emails:
  {agent_name}: {email_address}

gmail_base: string
gmail_domain: string
```

**Example:**
```yaml
agent_emails:
  pm: bmad-pm@bmad.local
  dev: bmad-dev@bmad.local
  tea: bmad-tea@bmad.local
  analyst: bmad-analyst@bmad.local
  architect: bmad-architect@bmad.local

gmail_base: bmad
gmail_domain: bmad.local
```

**Generation Rules:**
- Format: `bmad-{agent_name}@{domain}`
- Special transformations:
  - `quick-flow-solo-dev` → `quickdev`
  - `tech-writer` → `techwriter`
  - Hyphens removed, lowercase

---

## Artifact Models

### Epic Format

**File:** `{bmad_output}/epics/{epic-id}.md`

```markdown
---
epic_id: string
title: string
priority: enum (High, Medium, Low)
status: enum (Draft, Active, Completed)
assignee: string
due_date: date (ISO 8601)
---

# Epic Title

## Description
Epic description text...

## User Stories
- [ ] Story 1
- [ ] Story 2

## Acceptance Criteria
- AC 1
- AC 2
```

**Python Model:**
```python
@dataclass
class Epic:
    epic_id: str
    title: str
    description: str
    stories: List[str]
    acceptance_criteria: List[str]
    priority: str
    status: str
    assignee: str
    due_date: str
    file_path: Path
```

### Story Format

**File:** `{bmad_output}/stories/{story-id}.md`

```markdown
---
story_id: string
epic: string
assignee: string
priority: enum (High, Medium, Low)
status: enum (Draft, Active, Completed)
---

# Story Title

## Description
Story description...

## Acceptance Criteria
- AC 1
- AC 2

## Tasks
- [ ] Task 1
- [ ] Task 2
```

**Python Model:**
```python
@dataclass
class Story:
    story_id: str
    title: str
    description: str
    epic: str
    assignee: str
    acceptance_criteria: List[str]
    tasks: List[Dict[str, Any]]
    priority: str
    status: str
    file_path: Path
```

---

## Gitea API Models

### User

```python
@dataclass
class GiteaUser:
    id: int
    username: str
    email: str
    full_name: str
    active: bool
    admin: bool
    created: str
```

**API Response:**
```json
{
  "id": 42,
  "username": "bmad-pm",
  "email": "bmad-pm@bmad.local",
  "full_name": "John (PM)",
  "active": true,
  "is_admin": false,
  "created": "2026-01-22T10:00:00Z"
}
```

### Repository

```python
@dataclass
class GiteaRepo:
    id: int
    name: str
    full_name: str
    description: str
    private: bool
    owner: GiteaUser
    created: str
```

**API Response:**
```json
{
  "id": 123,
  "name": "projet-medical-main",
  "full_name": "Zadmin/projet-medical-main",
  "description": "Medical project",
  "private": true,
  "owner": {...},
  "created_at": "2026-01-22T09:00:00Z"
}
```

### Issue

```python
@dataclass
class GiteaIssue:
    id: int
    number: int
    title: str
    body: str
    state: str
    assignee: GiteaUser
    milestone: GiteaMilestone
    labels: List[str]
    created: str
    updated: str
```

**API Response:**
```json
{
  "id": 456,
  "number": 8,
  "title": "Story: Implement user authentication",
  "body": "...",
  "state": "open",
  "assignee": {...},
  "milestone": {...},
  "labels": ["story", "bmad"],
  "created_at": "2026-01-22T11:00:00Z",
  "updated_at": "2026-01-22T11:00:00Z"
}
```

### Milestone

```python
@dataclass
class GiteaMilestone:
    id: int
    title: str
    description: str
    state: str
    due_on: str
    closed_at: str
```

**API Response:**
```json
{
  "id": 10,
  "title": "Epic: Authentication System",
  "description": "...",
  "state": "open",
  "due_on": "2026-03-01T00:00:00Z",
  "closed_at": null
}
```

---

## Internal Data Structures

### Provisioning Result

```python
@dataclass
class ProvisioningResult:
    status: str               # "created", "exists", "pending"
    username: str             # Gitea username
    email: str                # Assigned email
    issue_number: int = None  # Issue number (manual mode)
    user_id: int = None       # User ID (auto mode)
```

### Sync Result

```python
@dataclass
class SyncResult:
    created: List[Dict]       # Successfully created
    exists: List[Dict]        # Already existed
    pending: List[Dict]       # Pending (issues)
    failed: List[Dict]        # Failed operations
```

---

## Environment Variables (.env)

```bash
# Gitea Configuration
GITEA_URL=http://192.168.0.76:3000
GITEA_ADMIN_TOKEN=gto_xxxxxxxxxxxxxxxxxxxxxxxx

# Email Configuration
GMAIL_BASE=bmad
GMAIL_DOMAIN=bmad.local

# Logging
LOG_LEVEL=INFO
LOG_FILE=/volume1/tools/bmad-gitea-bridge/logs/sync.log

# Sync Settings
DEFAULT_SYNC_MODE=manual
DEFAULT_PROVISIONING_MODE=manual
```

---

## Document Navigation

**Previous:** [Tech Stack](tech-stack.md)  
**Next:** [Components](components.md)

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)  
**Last Updated:** 2026-01-22
