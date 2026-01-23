# Test Strategy and Standards

**Last Updated:** 2026-01-22

## Testing Philosophy
- Test behavior, not implementation
- Integration tests > Unit tests (for API-heavy code)
- Mock external APIs

## Test Structure (Future)
```
tests/
├── unit/
│   ├── test_agent_discovery.py
│   ├── test_email_generator.py
│   └── test_config_loader.py
├── integration/
│   ├── test_gitea_client.py
│   └── test_provisioner.py
└── fixtures/
    ├── sample_manifest.csv
    └── sample_config.yaml
```

## Coverage Goal
- Target: 80%+
- Tool: pytest-cov

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
