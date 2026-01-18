# 📘 BMad-Gitea-Bridge - Usage Guide

Complete guide for using BMad-Gitea-Bridge in daily operations.

---

## 📋 Table of Contents

1. [Basic Usage](#basic-usage)
2. [Command Reference](#command-reference)
3. [Provisioning Modes](#provisioning-modes)
4. [Multi-Project Management](#multi-project-management)
5. [Email Management](#email-management)
6. [Workflow Examples](#workflow-examples)
7. [Best Practices](#best-practices)
8. [Advanced Usage](#advanced-usage)

---

## 🚀 Basic Usage

### Running a Sync
```bash
cd /volume1/tools/bmad-gitea-bridge

# Dry-run (simulation, no changes)
python3.14 src/sync.py sync --project medical --dry-run

# Real sync
python3.14 src/sync.py sync --project medical
```

### What Happens During Sync

**Phase 1: Agent Discovery**
- Reads BMad `agent-manifest.csv`
- Discovers all agents with metadata
- Validates agent structure

**Phase 2: Email Assignment**
- Generates unique email for each agent
- Saves mapping to `config/projects/{project}.email-mapping.yaml`
- Reuses existing mappings on subsequent runs

**Phase 3: Gitea Provisioning**
- Checks which users exist in Gitea
- **Manual mode**: Creates issues for missing users
- **Auto mode**: Creates users directly

---

## 📖 Command Reference

### Sync Command
```bash
python3.14 src/sync.py sync --project PROJECT_NAME [OPTIONS]
```

**Required Arguments:**
- `--project`, `-p`: Project name (must match config file)

**Optional Flags:**
- `--dry-run`: Simulation mode (no changes made)

**Examples:**
```bash
# Sync medical project (real)
python3.14 src/sync.py sync --project medical

# Sync CRM project (dry-run)
python3.14 src/sync.py sync --project crm --dry-run

# Short syntax
python3.14 src/sync.py sync -p medical
```

### Version Command
```bash
python3.14 src/sync.py version
```

**Output:**
```
BMad-Gitea-Bridge
Version: 0.1.0
Authors: Khaled Z. & Claude (Anthropic)
License: MIT
```

### Help Command
```bash
python3.14 src/sync.py --help
python3.14 src/sync.py sync --help
```

---

## 🔧 Provisioning Modes

### Manual Mode (Recommended)

Creates **Gitea issues** for each agent requiring provisioning.

**Configuration:**
```yaml
# config/projects/medical.yaml
sync:
  provisioning: manual
```

**Workflow:**
1. Script discovers new agents
2. Creates issue for each agent with details:
   - Suggested username: `bmad-{agent}`
   - Email: `bmad-{agent}@bmad.local`
   - Full name: Agent display name
   - Instructions for manual creation
3. Admin reviews issues
4. Admin creates users manually in Gitea
5. Admin closes issues

**Advantages:**
- ✅ Manual review before user creation
- ✅ Audit trail via issues
- ✅ Safe for production
- ✅ Compliance-friendly

**Example Issue Created:**
```
Title: 🤖 Provision user for agent: John (PM)
Body:
Agent: pm
Display Name: John
Suggested Username: bmad-pm
Email: bmad-pm@bmad.local
Module: bmm

Please create this user in Gitea:
1. Site Admin → Users → Create User
2. Username: bmad-pm
3. Email: bmad-pm@bmad.local
4. Full Name: John
5. Send activation email: No
```

### Auto Mode

Automatically creates Gitea users.

**Configuration:**
```yaml
# config/projects/medical.yaml
sync:
  provisioning: auto
```

**Workflow:**
1. Script discovers new agents
2. Creates users directly in Gitea
3. No manual intervention needed

**Advantages:**
- ✅ Fully automated
- ✅ Fast provisioning
- ✅ Good for development/testing

**Cautions:**
- ⚠️ No manual review
- ⚠️ User passwords auto-generated
- ⚠️ Requires careful configuration

---

## 🗂️ Multi-Project Management

### Creating Additional Projects

**Example: CRM Project**
```bash
# Copy template
cp config/projects/medical.yaml config/projects/crm.yaml

# Edit configuration
nano config/projects/crm.yaml
```

**CRM Configuration:**
```yaml
project:
  name: crm
  description: "Mini CRM project"

bmad:
  root: /volume1/projects/mini-crm
  manifest: _bmad/_config/agent-manifest.csv

gitea:
  url: http://192.168.0.76:3000
  organization: MiniCRM  # Optional organization
  repository: crm-main
  admin_token: ${GITEA_ADMIN_TOKEN}

gmail:
  base: bmad
  domain: bmad.local  # Same email domain
  enabled: true

sync:
  provisioning: manual
```

**Create Gitea organization (if using):**
1. Gitea → **+** → **New Organization**
2. Name: `MiniCRM`
3. Create repository: `crm-main`

**Sync CRM project:**
```bash
python3.14 src/sync.py sync --project crm --dry-run
python3.14 src/sync.py sync --project crm
```

### Managing Multiple Projects

**Project Structure:**
```
config/projects/
├── medical.yaml          # Medical project
├── crm.yaml              # CRM project
├── homeassistant.yaml    # Home automation project
└── template.yaml         # Template for new projects
```

**Email reuse:**
All projects can share the **same email domain** (`bmad.local`).

**Example:**
- Medical project: `bmad-pm@bmad.local` → John (medical PM)
- CRM project: `bmad-pm@bmad.local` → Same John or different PM

**MailPlus filtering:**
Set up rules to filter by project name in subject.

---

## 📧 Email Management

### Email Mapping File

After first sync, email mappings are saved:
```yaml
# config/projects/medical.email-mapping.yaml
agent_emails:
  pm: bmad-pm@bmad.local
  dev: bmad-dev@bmad.local
  analyst: bmad-analyst@bmad.local
  # ... all agents
gmail_base: bmad
gmail_domain: bmad.local
```

**This file is reused on subsequent syncs** to maintain consistency.

### Changing Email Assignments

**Method 1: Edit mapping file**
```bash
nano config/projects/medical.email-mapping.yaml
```

Change email, save, then sync.

**Method 2: Delete mapping file**
```bash
rm config/projects/medical.email-mapping.yaml
python3.14 src/sync.py sync --project medical
```

New mappings will be generated.

### Adding New Agents

When you add a new agent to `agent-manifest.csv`:

1. **Sync project:**
```bash
python3.14 src/sync.py sync --project medical
```

2. **New agent detected:**
   - Email generated automatically
   - Saved to mapping file
   - Gitea issue created (manual mode)

3. **Add MailPlus alias:**
```
MailPlus Server → Domains → bmad.local → Aliases
Add: bmad-new-agent → Bmad
```

---

## 🎯 Workflow Examples

### Scenario 1: New BMad Project Setup

**Goal:** Set up Gitea for a new BMad project

**Steps:**

1. **Create Gitea repository**
```
Gitea → New Repository
Name: new-project-main
Visibility: Private
```

2. **Create project config**
```bash
cd /volume1/tools/bmad-gitea-bridge
cp examples/medical-project.yaml config/projects/newproject.yaml
nano config/projects/newproject.yaml
# Edit paths, repo name, etc.
```

3. **First sync (dry-run)**
```bash
python3.14 src/sync.py sync --project newproject --dry-run
```

4. **Review output, verify agents discovered**

5. **Real sync**
```bash
python3.14 src/sync.py sync --project newproject
```

6. **Create MailPlus aliases for new agents (if any)**

7. **Process Gitea issues to create users**

### Scenario 2: Adding New Custom Agent

**Goal:** Add a custom FHIR agent to medical project

**Steps:**

1. **Add agent to manifest**
```bash
nano /volume1/concept/bmad/_bmad/_config/agent-manifest.csv
```

Add line:
```csv
"fhir-specialist","FHIR Specialist","FHIR Integration","🏥","integration","medical-custom","/path/to/agent"
```

2. **Sync project**
```bash
python3.14 src/sync.py sync --project medical
```

**Output:**
```
📋 Phase 1: Agent Discovery
   ✅ Discovered 14 agents  # Was 13, now 14

🔧 Phase 3: Gitea User Provisioning
   ✅ Provisioning complete
      Pending (issues): 1   # New issue created
```

3. **Add MailPlus alias**
```
Alias: bmad-fhir-specialist → Bmad
```

4. **Create Gitea user from issue**

### Scenario 3: Re-syncing After Agent Updates

**Goal:** Update agent metadata in Gitea

**Steps:**

1. **Update agent-manifest.csv**
```bash
nano /volume1/concept/bmad/_bmad/_config/agent-manifest.csv
# Change display name, icon, etc.
```

2. **Sync project**
```bash
python3.14 src/sync.py sync --project medical
```

**Current behavior:** Email mapping preserved, new issues created if needed.

**Future feature:** Update existing Gitea users (coming in v0.2.0)

---

## ✅ Best Practices

### 1. Always Dry-Run First
```bash
# Before any real sync
python3.14 src/sync.py sync --project medical --dry-run
```

Verify:
- ✅ Agent count correct
- ✅ Emails look good
- ✅ No unexpected errors

### 2. Backup Before Major Changes
```bash
# Backup configs
cp -r config config.backup.$(date +%Y%m%d)

# Backup email mappings
cp config/projects/*.email-mapping.yaml backups/
```

### 3. Use Manual Mode in Production
```yaml
sync:
  provisioning: manual  # Safer for production
```

### 4. Monitor Gitea Issues

Regularly check:
```
http://your-gitea/org/repo/issues?labels=provisioning
```

Process pending user creation requests.

### 5. Keep Email Mappings Under Version Control
```bash
cd /volume1/tools/bmad-gitea-bridge
git add config/projects/*.email-mapping.yaml
git commit -m "Update email mappings"
git push
```

### 6. Document Custom Agents

Maintain a README in your BMad project:
```
/volume1/concept/bmad/_bmad/_config/CUSTOM_AGENTS.md
```

### 7. Regular Syncs

Set up cron for periodic syncs:
```bash
# Sync every Monday at 9 AM
0 9 * * 1 cd /volume1/tools/bmad-gitea-bridge && python3.14 src/sync.py sync --project medical >> logs/cron.log 2>&1
```

---

## 🔬 Advanced Usage

### Custom Email Domains

**Use different domain per project:**
```yaml
# medical.yaml
gmail:
  base: bmad
  domain: medical.local

# crm.yaml
gmail:
  base: bmad
  domain: crm.local
```

**Requires:** Create separate MailPlus domains.

### Organization-Based Repos
```yaml
gitea:
  organization: ProjetMedical  # Use organization
  repository: main
```

**Requires:** Create Gitea organization first.

### Filtering Logs
```bash
# View only errors
cat logs/sync.log | grep ERROR

# View specific agent
cat logs/sync.log | grep "bmad-pm"

# Tail live logs
tail -f logs/sync.log
```

### Scripting Multiple Projects

**Sync all projects:**
```bash
#!/bin/bash
for project in medical crm homeassistant; do
    echo "Syncing $project..."
    python3.14 src/sync.py sync --project $project
done
```

---

## 📊 Output Interpretation

### Successful Sync
```
✅ Discovered 13 agents
✅ Assigned emails to 13 agents
✅ Provisioning complete
   Created: 0
   Already exist: 13
   Pending (issues): 0
```

**Meaning:** All agents have Gitea users, nothing to do.

### New Agents Detected
```
✅ Discovered 15 agents  # Was 13
✅ Assigned emails to 15 agents
✅ Provisioning complete
   Created: 0
   Already exist: 13
   Pending (issues): 2  # New issues created
```

**Action:** Check Gitea issues, create 2 new users.

### Connection Error
```
❌ Cannot connect to Gitea
```

**Troubleshooting:**
1. Check Gitea is running: `docker ps | grep gitea`
2. Verify token in `.env`
3. Test API: `curl -H "Authorization: token TOKEN" http://gitea/api/v1/user`

---

## 🆘 Common Issues

### Issue: Email Mapping Changed Unexpectedly

**Cause:** Mapping file deleted or corrupted.

**Solution:**
```bash
# Restore from backup
cp backups/medical.email-mapping.yaml.20260117 config/projects/medical.email-mapping.yaml
```

### Issue: Duplicate Issues Created

**Cause:** Sync run multiple times before users created.

**Solution:**
1. Close duplicate issues in Gitea
2. Create users
3. Re-sync to verify

### Issue: Agent Not Detected

**Cause:** Invalid CSV format in agent-manifest.

**Solution:**
```bash
# Check CSV syntax
cat /volume1/concept/bmad/_bmad/_config/agent-manifest.csv

# Verify commas, quotes, newlines
```

---

## 📞 Support

Questions? Issues? Suggestions?

- **GitHub Issues**: https://github.com/khzd19/bmad-gitea-bridge/issues
- **Email**: khzd19@gmail.com
- **Logs**: `/volume1/tools/bmad-gitea-bridge/logs/`

---

**Written by:** Khaled Z. & Claude (Anthropic)  
**Last updated:** January 17, 2026  
**Version:** 0.1.0