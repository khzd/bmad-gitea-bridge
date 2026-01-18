"""
Gitea Provisioner
Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
from typing import Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class GiteaProvisioner:
    """
    Provisions BMad agents in Gitea
    
    Modes:
    - manual: Create issues for manual user creation
    - auto: Automatically create users
    """
    
    def __init__(self, gitea_client, mode: str = 'manual'):
        """
        Initialize provisioner
        
        Args:
            gitea_client: GiteaClient instance
            mode: 'manual' or 'auto'
        """
        self.gitea_client = gitea_client
        self.mode = mode
        
        if mode not in ['manual', 'auto']:
            raise ValueError(f"Invalid mode: {mode}. Must be 'auto' or 'manual'")
        
        logger.info(f"Initialized Gitea provisioner in '{mode}' mode")
    
    def _issue_exists_for_agent(self, username: str) -> bool:
        """
        Check if a provisioning issue already exists for this agent
        
        Args:
            username: Gitea username (e.g., 'bmad-pm')
        
        Returns:
            True if issue exists, False otherwise
        """
        try:
            # Get all open issues in the repository
            issues = self.gitea_client.list_issues(state='open')
            
            # Check if any issue title contains this agent
            for issue in issues:
                title = issue.get('title', '')
                # Check if username is in the title
                if username in title or username.replace('bmad-', '') in title:
                    logger.info(f"📋 Issue already exists for {username}: #{issue['number']}")
                    return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Could not check existing issues: {e}")
            return False  # En cas d'erreur, on assume qu'il n'existe pas
    
    def _create_provisioning_issue(self, agent, username: str) -> Dict:
        """
        Create a Gitea issue for manual user provisioning
        
        Args:
            agent: Agent object
            username: Suggested Gitea username
        
        Returns:
            Created issue data
        """
        # Get current user for assignment
        current_user = self.gitea_client.get_current_user()
        
        # Issue title
        title = f"🤖 Provision user: {username}"
        # Issue body with instructions
        body = f"""## Agent Information

**Agent Name:** `{agent.name}`  
**Display Name:** {agent.display_name}  
**Icon:** {agent.icon}  
**Module:** {agent.module}  

---

## Suggested Gitea User

**Username:** `{username}`  
**Email:** `{agent.email}`  
**Full Name:** `{agent.display_name}`  

---

## Manual Provisioning Steps

1. **Go to Gitea Site Administration**
   - Settings → Users → Create User

2. **Fill user details:**
```
   Username: {username}
   Email: {agent.email}
   Full Name: {agent.display_name}
   Password: [generate secure password]
```

3. **Save and activate user**

4. **Close this issue** when done

---

**Created by:** BMad-Gitea-Bridge  
**Mode:** Manual provisioning
"""
        
        # Create issue
        issue = self.gitea_client.create_issue(
            title=title,
            body=body,
            assignee=current_user.get('login')
        )
        
        logger.info(f"📋 Created provisioning issue #{issue['number']} for {username}")
        
        return issue
    
    def _create_user_auto(self, agent, username: str) -> Dict:
        """
        Automatically create Gitea user
        
        Args:
            agent: Agent object
            username: Gitea username
        
        Returns:
            Created user data
        """
        import secrets
        
        # Generate secure password
        password = secrets.token_urlsafe(16)
        
        user = self.gitea_client.create_user(
            username = username,
            email = agent.email,
            full_name = agent.display_name,
            password  = password,
            must_change_password = False,
            send_notify = True
        )
     
     
        logger.info(f"✅ Created user {username} automatically")
        
        return user
    
    def provision_agent(self, agent) -> Dict:
        """
        Provision a single agent in Gitea
        
        Args:
            agent: Agent object with name, email, etc.
        
        Returns:
            Dict with provisioning status
        """
        # Generate Gitea username (e.g., 'bmad-pm')
        username = f"bmad-{agent.name}"
        
        logger.info(f"Provisioning agent: {agent.name} → {username}")
        
        # Check if user exists
        user_exists = self.gitea_client.user_exists(username)
        
        if user_exists:
            logger.info(f"✅ User {username} already exists")
            return {
                'status': 'exists',
                'username': username,
                'email': agent.email
            }
        
        # User doesn't exist - check if issue already exists (manual mode)
        if self.mode == 'manual':
            # Check if issue already created
            if self._issue_exists_for_agent(username):
                logger.info(f"⏭️  Issue already exists for {username}, skipping")
                return {
                    'status': 'pending',
                    'username': username,
                    'email': agent.email,
                    'issue_exists': True
                }
            
            # Create provisioning issue
            issue = self._create_provisioning_issue(agent, username)
            
            return {
                'status': 'pending',
                'username': username,
                'email': agent.email,
                'issue_number': issue['number']
            }
        
        # Auto mode - create user directly
        elif self.mode == 'auto':
            user = self._create_user_auto(agent, username)
            
            return {
                'status': 'created',
                'username': username,
                'email': agent.email,
                'user_id': user.get('id')
            }
    
    def provision_all_agents(self, agents: List) -> Dict:
        """
        Provision all agents
        
        Args:
            agents: List of Agent objects
        
        Returns:
            Dict with results summary
        """
        results = {
            'created': [],
            'exists': [],
            'pending': [],
            'failed': []
        }
        
        for agent in agents:
            try:
                result = self.provision_agent(agent)
                
                status = result['status']
                
                if status == 'created':
                    results['created'].append(result)
                elif status == 'exists':
                    results['exists'].append(result)
                elif status == 'pending':
                    results['pending'].append(result)
                
            except Exception as e:
                logger.error(f"Failed to provision agent {agent.name}: {e}")
                results['failed'].append({
                    'agent': agent.name,
                    'error': str(e)
                })
        
        # Log summary
        logger.info(
            f"Provisioning complete: "
            f"{len(results['created'])} created, "
            f"{len(results['exists'])} existing, "
            f"{len(results['pending'])} pending"
        )
        
        return results