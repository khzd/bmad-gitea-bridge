"""
Gitea Provisioner Module

Automatically provisions Gitea users for BMad agents.

Authors: Khaled Z. & Claude (Anthropic)
"""

import secrets
import string
from typing import Dict, List, Optional
import logging
from .agent_discovery import Agent

logger = logging.getLogger(__name__)


class GiteaProvisioner:
    """Provisions Gitea users for BMad agents"""
    
    def __init__(self, gitea_client, mode: str = "manual"):
        """
        Initialize provisioner
        
        Args:
            gitea_client: GiteaClient instance
            mode: 'auto' or 'manual'
                - auto: Automatically create Gitea users
                - manual: Create provisioning issues for approval
        """
        self.client = gitea_client
        self.mode = mode
        
        if mode not in ['auto', 'manual']:
            raise ValueError(f"Invalid mode: {mode}. Must be 'auto' or 'manual'")
    
    def _generate_password(self, length: int = 24) -> str:
        """
        Generate a secure random password
        
        Args:
            length: Password length
            
        Returns:
            Secure random password
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def _user_exists(self, username: str) -> bool:
        """
        Check if a user exists in Gitea
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists, False otherwise
        """
        try:
            user = self.client.get_user(username)
            return user is not None
        except Exception as e:
            logger.debug(f"User {username} does not exist: {e}")
            return False
    
    def _create_gitea_user(self, agent: Agent, password: str) -> Dict:
        """
        Create a user in Gitea
        
        Args:
            agent: Agent object
            password: Password for the user
            
        Returns:
            User creation result
        """
        username = f"bmad-{agent.name}"
        
        try:
            user = self.client.create_user(
                username=username,
                email=agent.email,
                password=password,
                full_name=agent.display_name,
                send_notify=False
            )
            
            logger.info(f"✅ Created Gitea user: {username}")
            
            return {
                'status': 'created',
                'username': username,
                'email': agent.email,
                'password': password,
                'user_id': user.get('id')
            }
        
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}")
            raise
    
    def _create_provisioning_issue(self, agent: Agent) -> Dict:
        """
        Create a provisioning issue in Gitea
        
        Args:
            agent: Agent object
            
        Returns:
            Issue creation result
        """
        username = f"bmad-{agent.name}"
        
        issue_title = f"🤖 Provision Gitea user for agent: {agent.display_name}"
        
        issue_body = f"""
## New BMad Agent Detected

**Agent**: `{agent.name}`  
**Display Name**: {agent.display_name}  
**Title**: {agent.title}  
**Module**: {agent.module}  
**Icon**: {agent.icon}

## Action Required

A new BMad agent has been detected and needs a Gitea user account.

### Proposed User Details

- **Username**: `{username}`
- **Email**: `{agent.email}`
- **Full Name**: `{agent.display_name}`
- **Password**: [Auto-generate secure password]

### Manual Creation Steps
```bash
# Via Gitea API
curl -X POST "{self.client.base_url}/api/v1/admin/users" \\
  -H "Authorization: token YOUR_ADMIN_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "username": "{username}",
    "email": "{agent.email}",
    "password": "GENERATE_SECURE_PASSWORD",
    "full_name": "{agent.display_name}",
    "send_notify": false
  }}'
```

Or via Gitea Web UI:
1. Go to Site Administration → User Accounts
2. Click "Create User Account"
3. Fill in the details above
4. Click "Create User Account"

### After Creation

Once the user is created, close this issue and the agent will be fully provisioned.

---

*This issue was automatically created by BMad-Gitea-Bridge*
"""
        
        try:
            issue = self.client.create_issue(
                title=issue_title,
                body=issue_body,
                labels=['provisioning', 'infrastructure', 'admin-required']
            )
            
            logger.info(f"📋 Created provisioning issue #{issue.get('number')} for {username}")
            
            return {
                'status': 'pending',
                'username': username,
                'email': agent.email,
                'issue_number': issue.get('number'),
                'issue_url': issue.get('html_url')
            }
        
        except Exception as e:
            logger.error(f"Failed to create provisioning issue for {username}: {e}")
            raise
    
    def provision_agent(self, agent: Agent) -> Dict:
        """
        Provision a single agent
        
        Args:
            agent: Agent to provision
            
        Returns:
            Provisioning result dict with status
        """
        username = f"bmad-{agent.name}"
        
        # Check if user already exists
        if self._user_exists(username):
            logger.info(f"User {username} already exists, skipping")
            return {
                'status': 'exists',
                'username': username,
                'email': agent.email
            }
        
        # Auto mode: create user directly
        if self.mode == 'auto':
            password = self._generate_password()
            return self._create_gitea_user(agent, password)
        
        # Manual mode: create provisioning issue
        else:
            return self._create_provisioning_issue(agent)
    
    def provision_all_agents(self, agents: List[Agent]) -> Dict[str, List[Dict]]:
        """
        Provision all agents
        
        Args:
            agents: List of agents to provision
            
        Returns:
            Dict with lists of results by status:
            {
                'created': [...],
                'exists': [...],
                'pending': [...]
            }
        """
        results = {
            'created': [],
            'exists': [],
            'pending': []
        }
        
        for agent in agents:
            try:
                result = self.provision_agent(agent)
                status = result['status']
                results[status].append(result)
            
            except Exception as e:
                logger.error(f"Failed to provision agent {agent.name}: {e}")
                # Continue with other agents
                continue
        
        # Log summary
        logger.info(f"Provisioning complete: "
                   f"{len(results['created'])} created, "
                   f"{len(results['exists'])} existing, "
                   f"{len(results['pending'])} pending")
        
        return results