# 📦 BMad-Gitea-Bridge - Installation Guide

Complete step-by-step installation guide for BMad-Gitea-Bridge on Synology NAS (DSM 7) or Linux.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Preparation](#system-preparation)
3. [Python Installation](#python-installation)
4. [Project Installation](#project-installation)
5. [MailPlus Configuration](#mailplus-configuration)
6. [Gitea Configuration](#gitea-configuration)
7. [First Sync Test](#first-sync-test)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Hardware
- **Synology NAS** (DS218+, DS920+, or similar) with DSM 7+
- OR **Linux server** (Ubuntu 20.04+, Debian 11+)
- **2GB RAM minimum** (4GB recommended)
- **1GB free disk space**

### Software
- **Python 3.10+** (3.14 recommended)
- **Gitea** instance (local or remote)
- **MailPlus Server** (Synology) OR **Gmail** account
- **BMad Method** project installed

### Access
- SSH access to your NAS/server
- Admin access to Gitea
- Admin access to MailPlus (if using Synology)

---

## 🖥️ System Preparation

### Step 1: Enable SSH on Synology

1. **DSM** → **Control Panel** → **Terminal & SNMP**
2. Check **Enable SSH service**
3. Port: `22` (default)
4. Click **Apply**

### Step 2: Connect via SSH
```bash
ssh your_admin_user@192.168.0.76
# Example: ssh Zadmin@192.168.0.76
```

### Step 3: Create Project Directory
```bash
# Create tools directory
sudo mkdir -p /volume1/tools
sudo chown $(whoami):users /volume1/tools
cd /volume1/tools
```

---

## 🐍 Python Installation

### On Synology NAS (Recommended: Python 3.14)

#### Method 1: SynoCommunity (Easiest)

1. **Add SynoCommunity to Package Center**:
   - Package Center → Settings → Package Sources
   - Add: `https://packages.synocommunity.com`
   - Name: `SynoCommunity`

2. **Install Python 3.14**:
   - Package Center → Community
   - Search: `Python 3.14`
   - Install

3. **Verify installation**:
```bash
python3.14 --version
# Output: Python 3.14.2
```

#### Method 2: Manual Installation
```bash
# Download Python 3.14 (if SynoCommunity unavailable)
wget https://www.python.org/ftp/python/3.14.2/Python-3.14.2.tgz
tar -xzf Python-3.14.2.tgz
cd Python-3.14.2
./configure --prefix=/usr/local
make
sudo make install
```

### On Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.14 python3.14-pip python3.14-venv

# Verify
python3.14 --version
```

---

## 📥 Project Installation

### Step 1: Clone Repository
```bash
cd /volume1/tools
git clone https://github.com/khzd19/bmad-gitea-bridge.git
cd bmad-gitea-bridge
```

**OR** if Git not available:
```bash
cd /volume1/tools
wget https://github.com/khzd19/bmad-gitea-bridge/archive/refs/heads/main.zip
unzip main.zip
mv bmad-gitea-bridge-main bmad-gitea-bridge
cd bmad-gitea-bridge
```

### Step 2: Install Dependencies
```bash
# On Synology NAS (use --break-system-packages)
python3.14 -m pip install -r requirements.txt --break-system-packages --user

# On standard Linux
python3.14 -m pip install -r requirements.txt --user
```

**Expected output**:
```
Successfully installed click-8.1.7 rich-13.7.0 requests-2.31.0 PyYAML-6.0.1 ...
```

### Step 3: Verify Installation
```bash
python3.14 src/sync.py --version
# Output: sync.py, version 0.1.0
```

### Step 4: Create Environment File
```bash
cp .env.example .env
nano .env
```

**Edit `.env`**:
```bash
# Gitea Configuration
GITEA_URL=http://192.168.0.76:3000
GITEA_ADMIN_TOKEN=  # To be filled later

# Email Configuration
GMAIL_BASE=bmad
GMAIL_DOMAIN=bmad.local
GMAIL_APP_PASSWORD=  # Leave empty for MailPlus

# Logging
LOG_LEVEL=INFO
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 📧 MailPlus Configuration

### Step 1: Install MailPlus Server

1. **Package Center** → Search `MailPlus Server`
2. **Install**
3. **Open MailPlus Server**

### Step 2: Create Domain

1. **MailPlus Server** → **Domains**
2. **Create** → Domain: `bmad.local`
3. **Users**: 5 (free licenses)

### Step 3: Create System Account

1. **DSM** → **Control Panel** → **User & Group**
2. **Create User**:
   - Username: `Bmad`
   - Password: [secure password]
   - Groups: `users`
   - Permissions: **None** (no folder access)
   - Applications: **MailPlus only**

### Step 4: Activate Email for Bmad

1. **MailPlus Server** → **Domains** → `bmad.local`
2. **Users** → Select `Bmad`
3. **Activate email**: `bmad@bmad.local`
4. **Quota**: 2 GB

### Step 5: Create Email Aliases

1. **MailPlus Server** → **Domains** → `bmad.local` → **Aliases**
2. **Add aliases** (all pointing to `Bmad`):
```
bmad-master
bmad-bmad-master
bmad-analyst
bmad-architect
bmad-pm
bmad-dev
bmad-sm
bmad-tea
bmad-quick-flow-solo-dev
bmad-quickdev
bmad-tech-writer
bmad-techwriter
bmad-ux
bmad-ux-designer
bmad-agent-builder
bmad-agentbuilder
bmad-module-builder
bmad-modulebuilder
bmad-workflow-builder
bmad-workflowbuilder
```

**Destination for ALL**: `Bmad`

### Step 6: Test Email
```bash
# Send test email
echo "Test MailPlus" | mail -s "Test" bmad-pm@bmad.local
```

**Verify**: Log into MailPlus webmail with `Bmad` account and check inbox.

---

## 🦊 Gitea Configuration

### Step 1: Create Admin Token

1. **Gitea** → Login as admin
2. **Avatar** (top right) → **Settings**
3. **Applications** → **Generate New Token**
4. **Token Name**: `bmad-gitea-bridge`
5. **Select Permissions**:
   - ✅ `repo` (all)
   - ✅ `admin:org` (all)
   - ✅ `write:user`
6. **Generate Token**
7. **Copy token** (starts with `gto_...`)

### Step 2: Add Token to .env
```bash
cd /volume1/tools/bmad-gitea-bridge
nano .env
```

**Update**:
```bash
GITEA_ADMIN_TOKEN=gto_xxxxxxxxxxxxxxxxxxxxxxxx
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 3: Configure Gitea SMTP (MailPlus)

**Edit Gitea config**:
```bash
# Find Gitea app.ini (Docker example)
cd /volume1/docker/gitea/gitea/conf
nano app.ini
```

**Add/Update `[mailer]` section**:
```ini
[mailer]
ENABLED = true
FROM = gitea@bmad.local
PROTOCOL = smtp
SMTP_ADDR = 192.168.0.76
SMTP_PORT = 25
```

Save and **restart Gitea**:
```bash
docker restart gitea
# OR via Container Manager in DSM
```

### Step 4: Test Gitea Email

1. **Gitea** → **Site Administration**
2. **Configuration** → Find **Send Testing Email**
3. **To**: your email
4. **Send**

**Verify email received** ✅

### Step 5: Create Gitea Repository

1. **Gitea** → **+** (top right) → **New Repository**
2. **Owner**: Your username (e.g., `Zadmin`)
3. **Repository Name**: `projet-medical-main`
4. **Description**: `Medical project with BMad agents`
5. **Visibility**: **Private**
6. **Initialize**: ✅ Add README
7. **Create Repository**

**Repository URL**: `http://192.168.0.76:3000/Zadmin/projet-medical-main`

---

## ⚙️ Project Configuration

### Step 1: Create Project Config
```bash
cd /volume1/tools/bmad-gitea-bridge
cp examples/medical-project.yaml config/projects/medical.yaml
nano config/projects/medical.yaml
```

**Edit configuration**:
```yaml
project:
  name: medical
  description: "Medical project with BMad agents"

bmad:
  root: /volume1/concept/bmad  # ← YOUR BMAD PATH
  manifest: _bmad/_config/agent-manifest.csv

gitea:
  url: http://192.168.0.76:3000  # ← YOUR GITEA URL
  organization: ""  # Empty for personal repo
  repository: projet-medical-main  # ← YOUR REPO NAME
  admin_token: ${GITEA_ADMIN_TOKEN}

gmail:
  base: bmad
  domain: bmad.local
  enabled: true

sync:
  mode: manual
  provisioning: manual  # Creates issues (recommended)

logging:
  level: INFO
  console: true
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 2: Verify BMad Path
```bash
# Check BMad project exists
ls -la /volume1/concept/bmad/_bmad/_config/agent-manifest.csv
```

**Expected**: File should exist ✅

---

## 🧪 First Sync Test

### Step 1: Dry-Run Test
```bash
cd /volume1/tools/bmad-gitea-bridge
python3.14 src/sync.py sync --project medical --dry-run
```

**Expected output**:
```
🌉 BMad-Gitea-Bridge
Version 0.1.0
============================================================
Project: medical
BMad Root: /volume1/concept/bmad
Gitea: http://192.168.0.76:3000
🔍 DRY RUN - No changes

📋 Phase 1: Agent Discovery
   ✅ Discovered 13 agents
[Beautiful table with all agents]

📧 Phase 2: Email Assignment
   ✅ Assigned emails to 13 agents
[Table with email mappings]

🔧 Phase 3: Gitea User Provisioning
   ⏭️  Skipped (dry-run mode)

============================================================
✅ Dry-run completed!
```

### Step 2: Real Sync
```bash
python3.14 src/sync.py sync --project medical
```

**Expected output**:
```
🔧 Phase 3: Gitea User Provisioning
   ✅ Connected to Gitea as: Zadmin
   ✅ Provisioning complete
      Created: 0
      Already exist: 0
      Pending (issues): 13

[Table showing 13 issues created]
```

### Step 3: Verify in Gitea

**Open Gitea repository**:
```
http://192.168.0.76:3000/Zadmin/projet-medical-main/issues
```

**You should see 13 issues** with provisioning instructions! 🎉

---

## 🔧 Troubleshooting

### Python Not Found
```bash
# Verify Python installation
which python3.14
python3.14 --version

# If not found, check SynoCommunity packages
# or reinstall Python
```

### Permission Denied
```bash
# Fix ownership
sudo chown -R $(whoami):users /volume1/tools/bmad-gitea-bridge

# Fix permissions
chmod +x src/sync.py
```

### Gitea Connection Failed
```bash
# Test Gitea API manually
curl -H "Authorization: token YOUR_TOKEN" \
     http://192.168.0.76:3000/api/v1/user

# Should return your user info as JSON
```

### MailPlus Emails Not Received

1. **Check aliases exist**: MailPlus Server → Domains → Aliases
2. **Check SMTP config**: Gitea app.ini → `[mailer]` section
3. **Restart Gitea**: `docker restart gitea`
4. **Send test email**: Gitea → Site Admin → Send Testing Email

### Agent Manifest Not Found
```bash
# Verify path in config
cat config/projects/medical.yaml | grep manifest

# Check file exists
ls -la /volume1/concept/bmad/_bmad/_config/agent-manifest.csv
```

### Module Import Errors
```bash
# Reinstall dependencies
python3.14 -m pip install -r requirements.txt --break-system-packages --user --force-reinstall
```

---

## ✅ Installation Complete!

Your BMad-Gitea-Bridge is now installed and operational! 🎉

**Next steps**:
- Read [USAGE.md](USAGE.md) for daily operations
- Configure additional projects
- Set up automated syncs (cron)

---

## 📞 Support

If you encounter issues:
1. Check this troubleshooting section
2. Review logs: `/volume1/tools/bmad-gitea-bridge/logs/`
3. Open an issue on GitHub
4. Contact: khzd19@gmail.com

---

**Installation by:** Khaled Z. & Claude (Anthropic)  
**Last updated:** January 17, 2026