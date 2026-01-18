"""
Gitea Issues Management

Issue-related operations for Gitea API.

Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
from typing import Dict, List, Optional
from .client import GiteaClient

logger = logging.getLogger(__name__)


class GiteaIssues:
    """Manage Gitea issues"""
    
    def __init__(self, client: GiteaClient):
        """
        Initialize issues manager
        
        Args:
            client: GiteaClient instance
        """
        self.client = client
    
    def create_issue(
        self,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        milestone: Optional[int] = None
    ) -> Dict:
        """
        Create an issue
        
        Args:
            title: Issue title
            body: Issue description
            labels: Label names
            assignee: Username to assign
            milestone: Milestone ID
            
        Returns:
            Created issue data
        """
        issue = self.client.create_issue(
            title=title,
            body=body,
            labels=labels,
            assignee=assignee
        )
        
        logger.info(f"Created issue #{issue.get('number')}: {title}")
        return issue
    
    def create_story_issue(
        self,
        story_title: str,
        story_body: str,
        assignee: str = None
    ) -> Dict:
        """
        Create an issue for a BMad story
        
        Args:
            story_title: Story title
            story_body: Story content/acceptance criteria
            assignee: Gitea username to assign
            
        Returns:
            Created issue data
        """
        return self.create_issue(
            title=story_title,
            body=story_body,
            labels=['story', 'bmad'],
            assignee=assignee
        )
    
    def create_epic_tracking_issue(
        self,
        epic_title: str,
        epic_description: str,
        stories: List[str]
    ) -> Dict:
        """
        Create a tracking issue for an epic
        
        Args:
            epic_title: Epic title
            epic_description: Epic description
            stories: List of story titles in this epic
            
        Returns:
            Created issue data
        """
        # Build epic body with story checklist
        body = f"{epic_description}\n\n## Stories\n\n"
        
        for story in stories:
            body += f"- [ ] {story}\n"
        
        return self.create_issue(
            title=f"Epic: {epic_title}",
            body=body,
            labels=['epic', 'bmad']
        )