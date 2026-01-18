"""
Gitea Milestones Management

Milestone-related operations for Gitea API.

Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
from typing import Dict, List, Optional
from .client import GiteaClient

logger = logging.getLogger(__name__)


class GiteaMilestones:
    """Manage Gitea milestones"""
    
    def __init__(self, client: GiteaClient):
        """
        Initialize milestones manager
        
        Args:
            client: GiteaClient instance
        """
        self.client = client
    
    def create_milestone(
        self,
        title: str,
        description: str = "",
        due_date: Optional[str] = None
    ) -> Dict:
        """
        Create a milestone
        
        Args:
            title: Milestone title
            description: Milestone description
            due_date: Due date (ISO format)
            
        Returns:
            Created milestone data
        """
        # Build endpoint
        if self.client.organization:
            endpoint = f"/repos/{self.client.organization}/{self.client.repository}/milestones"
        else:
            user = self.client.get_current_user()
            endpoint = f"/repos/{user['login']}/{self.client.repository}/milestones"
        
        data = {
            'title': title,
            'description': description
        }
        
        if due_date:
            data['due_on'] = due_date
        
        milestone = self.client._make_request('POST', endpoint, data=data)
        logger.info(f"Created milestone: {title}")
        
        return milestone
    
    def create_epic_milestone(
        self,
        epic_title: str,
        epic_description: str
    ) -> Dict:
        """
        Create a milestone for a BMad epic
        
        Args:
            epic_title: Epic title
            epic_description: Epic description
            
        Returns:
            Created milestone data
        """
        return self.create_milestone(
            title=f"Epic: {epic_title}",
            description=epic_description
        )