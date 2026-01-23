# Feature Request: Organization & Team Provisioning

## Context

BMad-Gitea-Bridge currently provisions individual users but doesn't handle:
- Organization management
- Team creation
- User assignment to teams

This feature adds full organization/team provisioning capabilities.

---

## Requirements

### 1. Organization Management

**Create organization if missing:**
```bash
curl -X POST \
  -H "Authorization: token {GITEA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "HealthProducts",
    "description": "Healthcare Products Organization"
  }' \
  "http://192.168.0.76:3000/api/v1/orgs"
```

**Check if organization exists:**
```bash
curl -H "Authorization: token {GITEA_TOKEN}" \
  "http://192.168.0.76:3000/api/v1/orgs/HealthProducts"
```

---

### 2. Team Creation

**Create team with permissions:**
```bash
curl -X POST \
  -H "Authorization: token {GITEA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "BMad-Core",
    "description": "BMad Method Agents - Core Team",
    "permission": "write",
    "includes_all_repositories": true,
    "can_create_org_repo": false,
    "units": [
      "repo.code",
      "repo.issues",
      "repo.pulls",
      "repo.releases",
      "repo.wiki",
      "repo.projects"
    ]
  }' \
  "http://192.168.0.76:3000/api/v1/orgs/HealthProducts/teams"
```

**List existing teams:**
```bash
curl -H "Authorization: token {GITEA_TOKEN}" \
  "http://192.168.0.76:3000/api/v1/orgs/HealthProducts/teams"
```

---

### 3. User Assignment to Teams

**Add user to team (by team ID):**
```bash
curl -X PUT \
  -H "Authorization: token {GITEA_TOKEN}" \
  "http://192.168.0.76:3000/api/v1/teams/{TEAM_ID}/members/{USERNAME}"
```

**Example - Add all BMad agents:**
```bash
# After creating team (ID: 4), add each agent:
for agent in bmad-bmad-master bmad-analyst bmad-architect bmad-pm \
             bmad-dev bmad-sm bmad-tea bmad-tech-writer \
             bmad-ux-designer bmad-agent-builder bmad-module-builder \
             bmad-workflow-builder bmad-quick-flow-solo-dev; do
  curl -X PUT \
    -H "Authorization: token {GITEA_TOKEN}" \
    "http://192.168.0.76:3000/api/v1/teams/4/members/$agent"
done
```

**List team members:**
```bash
curl -H "Authorization: token {GITEA_TOKEN}" \
  "http://192.168.0.76:3000/api/v1/teams/{TEAM_ID}/members"
```

---

### 4. Repository Creation in Organization

**Create repo in org:**
```bash
curl -X POST \
  -H "Authorization: token {GITEA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "HealthAI-Platform",
    "description": "AI-powered post-hospitalization VIP patient monitoring",
    "private": true,
    "auto_init": true,
    "default_branch": "main",
    "readme": "Default"
  }' \
  "http://192.168.0.76:3000/api/v1/orgs/HealthProducts/repos"
```

---

## Implementation Requirements

### New Module: `src/gitea/organizations.py`
```python
class GiteaOrganizations:
    """Manage Gitea organizations and teams"""
    
    def __init__(self, client: GiteaClient):
        self.client = client
    
    def organization_exists(self, org_name: str) -> bool:
        """Check if organization exists"""
        pass
    
    def create_organization(self, org_name: str, description: str) -> Dict:
        """Create organization"""
        pass
    
    def ensure_organization(self, org_name: str, description: str) -> Dict:
        """Create org if doesn't exist, return existing otherwise"""
        pass
    
    def create_team(
        self,
        org_name: str,
        team_name: str,
        description: str,
        permission: str = "write",
        includes_all_repos: bool = True
    ) -> Dict:
        """Create team in organization"""
        pass
    
    def add_user_to_team(self, team_id: int, username: str) -> bool:
        """Add user to team"""
        pass
    
    def add_users_to_team(self, team_id: int, usernames: List[str]) -> Dict:
        """Bulk add users to team"""
        pass
    
    def create_repo_in_org(
        self,
        org_name: str,
        repo_name: str,
        description: str,
        private: bool = True
    ) -> Dict:
        """Create repository in organization"""
        pass
```

---

### Configuration Extension

**Update `config/projects/medical.yaml`:**
```yaml
gitea:
  url: http://192.168.0.76:3000
  admin_token: ${GITEA_ADMIN_TOKEN}
  
  # NEW: Organization configuration
  organization:
    name: HealthProducts
    description: "Healthcare Products Organization"
    create_if_missing: true
    
    # NEW: Team configuration
    teams:
      - name: BMad-Core
        description: "BMad Method Agents - Core Team"
        permission: write
        includes_all_repositories: true
        members: all  # 'all' = all discovered agents
        units:
          - repo.code
          - repo.issues
          - repo.pulls
          - repo.releases
          - repo.wiki
          - repo.projects
    
    # NEW: Repository configuration
    repositories:
      - name: HealthAI-Platform
        description: "AI-powered post-hospitalization monitoring"
        private: true
        auto_init: true
```

---

### Sync Workflow Extension

**Update `src/sync.py`:**
```python
# After Phase 3: Gitea User Provisioning
# Add Phase 4: Organization Setup

if project_config.gitea_organization:
    console.print("\n[bold]🏢 Phase 4: Organization & Team Setup[/bold]")
    
    from gitea.organizations import GiteaOrganizations
    
    org_manager = GiteaOrganizations(gitea_client)
    
    # 1. Ensure organization exists
    org_config = project_config.gitea_organization
    org = org_manager.ensure_organization(
        org_config['name'],
        org_config.get('description', '')
    )
    
    # 2. Create teams
    for team_config in org_config.get('teams', []):
        team = org_manager.create_team(
            org_name=org_config['name'],
            team_name=team_config['name'],
            description=team_config['description'],
            permission=team_config.get('permission', 'write'),
            includes_all_repos=team_config.get('includes_all_repositories', True)
        )
        
        # 3. Add agents to team
        if team_config.get('members') == 'all':
            usernames = [f"bmad-{agent.name}" for agent in agents]
            org_manager.add_users_to_team(team['id'], usernames)
    
    # 4. Create repositories
    for repo_config in org_config.get('repositories', []):
        org_manager.create_repo_in_org(
            org_name=org_config['name'],
            repo_name=repo_config['name'],
            description=repo_config['description'],
            private=repo_config.get('private', True)
        )
```

---

## Testing

### Manual Test Commands
```bash
# 1. Test organization creation
python3 src/sync.py sync --project medical --dry-run

# 2. Real sync with org provisioning
python3 src/sync.py sync --project medical

# 3. Verify in Gitea web interface:
# http://192.168.0.76:3000/HealthProducts
```

### Expected Output
```
🏢 Phase 4: Organization & Team Setup
   ✅ Organization: HealthProducts (exists)
   ✅ Created team: BMad-Core
   ✅ Added 13 members to BMad-Core
   ✅ Created repository: HealthAI-Platform
```

---

## Success Criteria

- [ ] Organizations can be created via config
- [ ] Teams created with proper permissions
- [ ] All BMad agents assigned to teams
- [ ] Repositories created in organizations
- [ ] Existing orgs/teams detected (idempotent)
- [ ] Config validates before execution
- [ ] Clear error messages for API failures

---

## API Reference

**Gitea API v1 docs:** https://try.gitea.io/api/swagger

**Key endpoints used:**
- `POST /api/v1/orgs` - Create organization
- `GET /api/v1/orgs/{org}` - Get organization
- `POST /api/v1/orgs/{org}/teams` - Create team
- `PUT /api/v1/teams/{id}/members/{username}` - Add member
- `POST /api/v1/orgs/{org}/repos` - Create repo

---

## Notes

- Token requires `admin:org` scope
- Team ID returned after creation needed for member additions
- `units` field is mandatory for team creation
- Repository creation returns full repo object

---

**Author:** Khaled Z.  
**Date:** 2026-01-21  
**Related Issue:** Organization provisioning for BMAD at Scale
