"""
Gitea Users Management

User-related operations for Gitea API.

Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
from typing import Dict, List, Optional
from .client import GiteaClient

logger = logging.getLogger(__name__)


class GiteaUsers:
    """Manage Gitea users"""
    
    def __init__(self, client: GiteaClient):
        """
        Initialize users manager
        
        Args:
            client: GiteaClient instance
        """
        self.client = client
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user by username
        
        Args:
            username: Username to find
            
        Returns:
            User data or None if not found
        """
        return self.client.get_user(username)
    
    def user_exists(self, username: str) -> bool:
        """
        Check if user exists
        
        Args:
            username: Username to check
            
        Returns:
            True if exists, False otherwise
        """
        user = self.get_user(username)
        return user is not None
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = ""
    ) -> Dict:
        """
        Create new user
        
        Args:
            username: Username
            email: Email address
            password: Password
            full_name: Display name
            
        Returns:
            Created user data
        """
        return self.client.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name
        )
    
    def ensure_user_exists(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = ""
    ) -> Dict:
        """
        Ensure user exists, create if not
        
        Args:
            username: Username
            email: Email address
            password: Password (used only if creating)
            full_name: Display name
            
        Returns:
            User data with 'created' boolean field
        """
        user = self.get_user(username)
        
        if user:
            logger.info(f"User {username} already exists")
            return {**user, 'created': False}
        
        logger.info(f"Creating user {username}")
        new_user = self.create_user(username, email, password, full_name)
        return {**new_user, 'created': True}