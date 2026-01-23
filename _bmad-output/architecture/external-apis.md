# External APIs

**File:** `architecture/external-apis.md`  
**Purpose:** Third-party API integrations  
**Last Updated:** 2026-01-22

---

## Gitea REST API v1

### Base Configuration
- **URL:** Configured per project
- **Auth:** Bearer token (admin rights)
- **Format:** JSON

### Endpoints Used

#### User Management
- `GET /api/v1/users/{username}` - Get user info
- `POST /api/v1/admin/users` - Create user (admin)
- `GET /api/v1/user` - Get current user

#### Repository Management
- `GET /api/v1/repos/{owner}/{repo}` - Get repo info
- `POST /api/v1/org/{org}/repos` - Create repo in org
- `POST /api/v1/user/repos` - Create user repo

#### Issue Management
- `GET /api/v1/repos/{owner}/{repo}/issues` - List issues
- `POST /api/v1/repos/{owner}/{repo}/issues` - Create issue
- `PATCH /api/v1/repos/{owner}/{repo}/issues/{index}` - Update issue

#### Milestone Management
- `POST /api/v1/repos/{owner}/{repo}/milestones` - Create milestone
- `GET /api/v1/repos/{owner}/{repo}/milestones` - List milestones

### Rate Limits
- No official limits documented
- Best practice: 100 req/min max
- Implement exponential backoff

---

## Future: Jira REST API v3

### Base Configuration
- **URL:** `https://{instance}.atlassian.net`
- **Auth:** API token or OAuth 2.0
- **Format:** JSON

### Planned Endpoints
- `POST /rest/api/3/user` - Create user
- `POST /rest/api/3/issue` - Create issue
- `POST /rest/api/3/project` - Create project

---

## Future: GitHub REST API v3

### Base Configuration
- **URL:** `https://api.github.com`
- **Auth:** Personal access token
- **Format:** JSON

### Planned Endpoints
- `POST /orgs/{org}/repos` - Create repo
- `POST /repos/{owner}/{repo}/issues` - Create issue
- `POST /repos/{owner}/{repo}/milestones` - Create milestone

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
