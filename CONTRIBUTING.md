# 🤝 Contributing to BMad-Gitea-Bridge

Thank you for considering contributing to BMad-Gitea-Bridge! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Submitting Changes](#submitting-changes)
7. [Review Process](#review-process)

---

## 🌟 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior includes:**
- ✅ Being respectful and inclusive
- ✅ Welcoming diverse perspectives
- ✅ Accepting constructive criticism gracefully
- ✅ Focusing on what's best for the community
- ✅ Showing empathy towards others

**Unacceptable behavior includes:**
- ❌ Harassment or discriminatory language
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information
- ❌ Any conduct inappropriate in a professional setting

### Enforcement

Project maintainers have the right to remove, edit, or reject contributions that don't align with this Code of Conduct.

**Report issues to:** khzd19@gmail.com

---

## 💡 How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
1. Check existing issues
2. Verify you're using the latest version
3. Check [Troubleshooting](INSTALL.md#troubleshooting) section

**Good bug report includes:**
- Clear, descriptive title
- Exact steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Relevant logs from `/logs/` directory
- Screenshots if applicable

**Template:**
```markdown
## Bug Description
[Clear description]

## Steps to Reproduce
1. Run command: `python3.14 src/sync.py ...`
2. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Python: 3.14.2
- OS: Synology DSM 7.2
- Gitea: 1.21.5
- BMad-Gitea-Bridge: 0.1.0

## Logs
```
[Paste relevant logs]
```

## Screenshots
[If applicable]
```

### Suggesting Enhancements

**Enhancement suggestions include:**
- New features
- Improvements to existing features
- Performance optimizations
- Better error messages

**Good enhancement request includes:**
- Clear use case
- Why it's needed
- How it should work
- Alternative solutions considered

### Documentation Improvements

Documentation is always welcome! Areas include:
- Fixing typos or unclear sections
- Adding examples
- Translating to other languages
- Creating tutorials or guides

### Code Contributions

See [Development Setup](#development-setup) below.

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+ (3.14 recommended)
- Git
- Gitea instance (for testing)
- MailPlus or Gmail (for testing)

### Fork and Clone
```bash
# Fork repository on GitHub
# Then clone your fork

git clone https://github.com/YOUR_USERNAME/bmad-gitea-bridge.git
cd bmad-gitea-bridge

# Add upstream remote
git remote add upstream https://github.com/khzd19/bmad-gitea-bridge.git
```

### Install Dependencies
```bash
# Create virtual environment (recommended)
python3.14 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### Configure Development Environment
```bash
# Copy example config
cp .env.example .env
nano .env  # Add your test credentials

# Create test project config
cp examples/medical-project.yaml config/projects/test.yaml
nano config/projects/test.yaml  # Adjust for your test environment
```

### Verify Installation
```bash
# Run version check
python3.14 src/sync.py --version

# Run dry-run test
python3.14 src/sync.py sync --project test --dry-run
```

---

## 📐 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

**Line length:** 100 characters (not 79)

**Imports:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import click
import yaml
from rich.console import Console

# Local
from core.config_loader import ConfigLoader
from gitea.client import GiteaClient
```

**Docstrings:**
```python
def provision_agent(self, agent: Agent) -> Dict:
    """
    Provision a single agent in Gitea.
    
    Args:
        agent: Agent object with name, email, etc.
    
    Returns:
        Dict with status: 'created', 'exists', or 'pending'
        
    Raises:
        GiteaAPIError: If API call fails
    """
    pass
```

**Type Hints:**
```python
from typing import Dict, List, Optional

def get_users(self, limit: int = 50) -> List[Dict]:
    """Get list of users"""
    pass
```

### Code Formatting

**Use Black for auto-formatting:**
```bash
# Format all files
black src/

# Check without modifying
black --check src/
```

**Use flake8 for linting:**
```bash
flake8 src/ --max-line-length=100
```

**Use mypy for type checking:**
```bash
mypy src/
```

### File Structure
```python
"""
Module description

Authors: Your Name & Original Authors
"""

# Imports
import os
from typing import Dict

# Constants
DEFAULT_TIMEOUT = 30
API_VERSION = "v1"

# Classes
class MyClass:
    """Class docstring"""
    
    def __init__(self):
        """Initialize"""
        pass
    
    def method(self) -> Dict:
        """Method docstring"""
        pass

# Functions
def helper_function() -> str:
    """Function docstring"""
    pass
```

### Error Handling
```python
# Good: Specific exceptions
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.HTTPError as e:
    logger.error(f"HTTP error: {e}")
    raise
except requests.RequestException as e:
    logger.error(f"Request failed: {e}")
    raise

# Bad: Catching everything
try:
    do_something()
except:
    pass
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug("Detailed info for debugging")
logger.info("General informational messages")
logger.warning("Warning messages")
logger.error("Error messages")
logger.exception("Error with traceback")
```

---

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agent_discovery.py

# Run specific test
pytest tests/test_agent_discovery.py::test_discover_agents
```

### Writing Tests

**Test file naming:** `test_*.py`

**Test function naming:** `test_*`

**Example test:**
```python
import pytest
from core.agent_discovery import AgentDiscovery

def test_discover_agents():
    """Test agent discovery from manifest"""
    discovery = AgentDiscovery("/path/to/bmad")
    agents = discovery.discover_all_agents()
    
    assert len(agents) > 0
    assert agents[0].name is not None
    assert agents[0].email is None  # Not assigned yet

def test_invalid_manifest_path():
    """Test error handling for invalid path"""
    with pytest.raises(FileNotFoundError):
        discovery = AgentDiscovery("/invalid/path")
        discovery.discover_all_agents()
```

### Test Coverage

Aim for **80%+ coverage** for new code.
```bash
# Generate coverage report
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html
```

---

## 📤 Submitting Changes

### Branch Naming
```bash
# Feature branch
git checkout -b feature/add-wiki-sync

# Bug fix branch
git checkout -b fix/issue-123-email-error

# Documentation branch
git checkout -b docs/update-install-guide
```

### Commit Messages

**Format:**
```
type(scope): Short description

Longer description if needed.

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code formatting (no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(provisioning): Add automatic user creation mode"

git commit -m "fix(email): Handle special characters in agent names

Agent names with hyphens were causing email generation to fail.
Now properly sanitizes names before creating emails.

Fixes #42"

git commit -m "docs(readme): Add multi-project example"
```

### Pull Request Process

1. **Update your fork:**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Ensure quality:**
```bash
# Format code
black src/

# Run linters
flake8 src/
mypy src/

# Run tests
pytest --cov=src tests/
```

3. **Push to your fork:**
```bash
git push origin feature/your-feature
```

4. **Create Pull Request on GitHub:**
   - Clear title describing the change
   - Description with:
     - What changed
     - Why it changed
     - How to test it
   - Reference any related issues

**PR Template:**
```markdown
## Description
[What does this PR do?]

## Motivation
[Why is this change needed?]

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] No new warnings
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## Related Issues
Fixes #123
Related to #456
```

---

## 🔍 Review Process

### What We Look For

**Code quality:**
- ✅ Follows style guidelines
- ✅ Well-documented
- ✅ Tests included
- ✅ No unnecessary complexity

**Functionality:**
- ✅ Solves stated problem
- ✅ Doesn't break existing features
- ✅ Edge cases handled
- ✅ Error messages helpful

**Documentation:**
- ✅ README updated if needed
- ✅ Docstrings present
- ✅ CHANGELOG.md updated

### Review Timeline

- Initial review: **Within 3 days**
- Follow-up reviews: **Within 2 days**
- Merge decision: **Within 1 week**

### Addressing Feedback
```bash
# Make requested changes
git add .
git commit -m "Address review feedback: Fix error handling"
git push origin feature/your-feature
```

No need for new PR - updates appear automatically!

---

## 🏆 Recognition

Contributors will be:
- ✅ Listed in [CONTRIBUTORS.md](CONTRIBUTORS.md)
- ✅ Credited in release notes
- ✅ Mentioned in CHANGELOG.md

**Top contributors** may be invited to become project maintainers!

---

## 📞 Questions?

**Need help?**
- Open a **Discussion** on GitHub
- Ask in issues (tag: `question`)
- Email: khzd19@gmail.com

**Want to chat?**
- We're friendly and happy to help! 😊

---

## 🙏 Thank You!

Every contribution makes BMad-Gitea-Bridge better. Whether it's:
- Reporting a bug 🐛
- Fixing a typo ✏️
- Adding a feature ✨
- Improving docs 📚

**Your help is appreciated! 💙**

---

**Maintained by:** Khaled Z. & Claude (Anthropic)  
**Last updated:** January 17, 2026  
**License:** MIT