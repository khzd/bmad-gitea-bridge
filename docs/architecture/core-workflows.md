# Core Workflows

**File:** `architecture/core-workflows.md`  
**Purpose:** Key operational workflows  
**Last Updated:** 2026-01-22

---

## Workflow 1: Agent Provisioning

```
┌─────────────────────────────────────────────────┐
│ 1. User runs: sync --project medical           │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 2. Load config (medical.yaml + .env)            │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 3. Discover agents (agent-manifest.csv)        │
│    Output: List[Agent] (13 agents)              │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 4. Assign emails (generate/load mapping)       │
│    Output: List[Agent] with emails              │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 5. Provision Gitea (manual or auto)            │
│    For each agent:                              │
│      - Check if user exists                     │
│      - If manual: create issue                  │
│      - If auto: create user                     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 6. Display results (Rich tables)               │
│    - Agents discovered                          │
│    - Emails assigned                            │
│    - Provisioning status                        │
└─────────────────────────────────────────────────┘
```

**Idempotency:** Re-running workflow skips existing users.

---

## Workflow 2: Artifact Synchronization (Future)

```
┌─────────────────────────────────────────────────┐
│ 1. User runs: sync-artifacts --project medical │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 2. Load config                                  │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 3. Discover epics (*.md in epics/)             │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 4. Sync epics → milestones                     │
│    For each epic:                               │
│      - Parse epic markdown                      │
│      - Check if milestone exists                │
│      - Create or update milestone               │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 5. Discover stories (*.md in stories/)         │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 6. Sync stories → issues                       │
│    For each story:                              │
│      - Parse story markdown                     │
│      - Check if issue exists                    │
│      - Create or update issue                   │
│      - Link to milestone                        │
│      - Assign to agent                          │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│ 7. Display results                              │
└─────────────────────────────────────────────────┘
```

---

## Workflow 3: Error Recovery

When operations fail (network error, API rate limit):

```
1. Operation fails
2. Log error with context
3. If retriable (network, 429):
   - Wait (exponential backoff)
   - Retry (max 3 attempts)
4. If non-retriable (400, 403):
   - Log error
   - Continue with next operation
5. Return partial results
```

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
