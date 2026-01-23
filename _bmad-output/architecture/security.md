# Security

**Last Updated:** 2026-01-22

## Authentication
- **Gitea:** Bearer tokens (admin rights)
- **Storage:** Environment variables (.env)
- **Never:** Hardcoded in source

## Secrets Management
```bash
# .env (gitignored)
GITEA_ADMIN_TOKEN=gto_xxxxx
```

## API Token Permissions
- Minimum: repo, user management
- Admin rights required for user creation

## Audit Trail
- All operations logged
- Git history = permanent record
- Manual mode = issue-based approval

## Compliance
- Users = human teams (traceability)
- No shadow IT
- Audit-ready logs

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
