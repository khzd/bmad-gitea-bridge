# Coding Standards

**Last Updated:** 2026-01-22

## Python Style

### PEP 8 Compliance
- Line length: 100 characters (not 79)
- Indentation: 4 spaces
- Naming:
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`

### Type Hints
```python
def provision_agent(self, agent: Agent) -> Dict[str, Any]:
    pass
```

### Docstrings
```python
def create_user(username: str, email: str) -> Dict:
    """
    Create Gitea user.
    
    Args:
        username: Gitea username
        email: Email address
    
    Returns:
        Created user data
    
    Raises:
        GiteaAPIError: If creation fails
    """
```

### Imports Order
1. Standard library
2. Third-party
3. Local

---

**Author:** Winston (Architect) & Bibi (Khaled Z.)
