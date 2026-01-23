# Infrastructure and Deployment

**Last Updated:** 2026-01-22

## Deployment Environments

### Primary: Synology NAS
- OS: DSM 7.2
- Python: 3.14 (SynoCommunity)
- Path: `/volume1/tools/bmad-gitea-bridge`
- Network: Local network access

### Installation
```bash
cd /volume1/tools
git clone https://github.com/khzd/bmad-gitea-bridge.git
cd bmad-gitea-bridge
python3.14 -m pip install -r requirements.txt --break-system-packages --user
cp .env.example .env
# Edit .env with credentials
```

### Running
```bash
python3.14 src/sync.py sync --project medical
```

### Logs
- Location: `/volume1/tools/bmad-gitea-bridge/logs/sync.log`
- Rotation: Manual (future: logrotate)

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
