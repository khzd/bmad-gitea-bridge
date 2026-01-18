"""
Gitea API Client

Main client for interacting with Gitea REST API.

Authors: Khaled Z. & Claude (Anthropic)
"""

import requests
import logging
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class GiteaAPIError(Exception):
    """Base exception for Gitea API errors"""
    pass


class GiteaClient:
    """Client for Gitea REST API v1"""
    
    def __init__(
        self,
        base_url: str,
        token: str,
        organization: str = "",
        repository: str = "",
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize Gitea client
        
        Args:
            base_url: Gitea instance URL (e.g., http://gitea:3000)
            token: Admin API token
            organization: Organization name (optional)
            repository: Repository name
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.organization = organization
        self.repository = repository
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # API version
        self.api_base = f"{self.base_url}/api/v1"
        
        # Default headers
        self.headers = {
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        logger.info(f"Initialized Gitea client for {self.base_url}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Any:
        """
        Make HTTP request to Gitea API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint (without /api/v1 prefix)
            data: Request body data
            params: URL query parameters
            
        Returns:
            Response JSON data
            
        Raises:
            GiteaAPIError: If request fails
        """


        # Construction manuelle pour éviter le bug urljoin
        if endpoint.startswith('/'):
            url = f"{self.api_base}{endpoint}"
        else:
            url = f"{self.api_base}/{endpoint}"



        """
        print(f"DEBUG api_base: {self.api_base}")       # ← AJOUTER
        print(f"DEBUG endpoint: {endpoint}")             # ← AJOUTER
        print(f"DEBUG final URL: {url}")                 # ← AJOUTER
        """
        
        logger.debug(f"{method} {url}")


        logger.debug(f"{method} {url}")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            # Log response status
            logger.debug(f"Response: {response.status_code}")
            
            # Raise for HTTP errors
            response.raise_for_status()
            
            # Return JSON if available
            if response.content:
                return response.json()
            return None
        
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error: {e}"
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = f"HTTP {e.response.status_code}: {error_data.get('message', str(e))}"
                except:
                    pass
            
            logger.error(error_msg)
            raise GiteaAPIError(error_msg)
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {e}"
            logger.error(error_msg)
            raise GiteaAPIError(error_msg)
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user information
        
        Args:
            username: Username to lookup
            
        Returns:
            User data or None if not found
        """
        try:
            return self._make_request('GET', f'/users/{username}')
        except GiteaAPIError as e:
            if '404' in str(e):
                return None
            raise
    def user_exists(self, username: str) -> bool:
        """
        Check if a user exists
        
        Args:
            username: Username to check
        
        Returns:
            True if user exists, False otherwise
        """
        try:
            user = self.get_user(username)
            return user is not None
        except Exception:
            return False



    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = "",
        send_notify: bool = False
    ) -> Dict:
        """
        Create a new user (requires admin token)
        
        Args:
            username: Username
            email: Email address
            password: Password
            full_name: Full name/display name
            send_notify: Send email notification
            
        Returns:
            Created user data
        """
        data = {
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name or username,
            'send_notify': send_notify,
            'must_change_password': False
        }
        
        return self._make_request('POST', '/admin/users', data=data)
    
    def create_issue(
        self,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None
    ) -> Dict:
        """
        Create an issue in the configured repository
        
        Args:
            title: Issue title
            body: Issue body/description
            labels: List of label names
            assignee: Username to assign
            
        Returns:
            Created issue data
        """
        # Determine repository path
        if self.organization:
            repo_path = f"/repos/{self.organization}/{self.repository}/issues"
        else:
            # Assume user repository
            user = self.get_current_user()
            repo_path = f"/repos/{user['login']}/{self.repository}/issues"
        
        data = {
            'title': title,
            'body': body
        }
        """        
        if labels:
            data['labels'] = labels
        """        
        if assignee:
            data['assignee'] = assignee
        
        return self._make_request('POST', repo_path, data=data)

    def list_issues(self, state: str = 'open') -> List[Dict]:
        """
        List issues in repository
        
        Args:
            state: Issue state ('open', 'closed', 'all')
        
        Returns:
            List of issues
        """
        try:
            # Build repo path
            if self.organization:
                repo_path = f"{self.organization}/{self.repository}"
            else:
                # Get current user for personal repos
                current_user = self.get_current_user()
                repo_path = f"{current_user['login']}/{self.repository}"
            
            # List issues
            endpoint = f"/repos/{repo_path}/issues"
            params = {'state': state}
            
            issues = self._make_request('GET', endpoint, params=params)
            
            return issues if issues else []
            
        except Exception as e:
            logger.error(f"Failed to list issues: {e}")
            return []












    def get_current_user(self) -> Dict:
        """
        Get current authenticated user
        
        Returns:
            Current user data
        """
        return self._make_request('GET', '/user')
    
    def list_labels(self) -> List[Dict]:
        """
        List all labels in repository
        
        Returns:
            List of labels
        """
        if self.organization:
            endpoint = f"/repos/{self.organization}/{self.repository}/labels"
        else:
            user = self.get_current_user()
            endpoint = f"/repos/{user['login']}/{self.repository}/labels"
        
        return self._make_request('GET', endpoint)
    
    def create_label(
        self,
        name: str,
        color: str,
        description: str = ""
    ) -> Dict:
        """
        Create a label in repository
        
        Args:
            name: Label name
            color: Color hex code (without #)
            description: Label description
            
        Returns:
            Created label data
        """
        if self.organization:
            endpoint = f"/repos/{self.organization}/{self.repository}/labels"
        else:
            user = self.get_current_user()
            endpoint = f"/repos/{user['login']}/{self.repository}/labels"
        
        # Remove # from color if present
        color = color.lstrip('#')
        
        data = {
            'name': name,
            'color': color,
            'description': description
        }
        
        return self._make_request('POST', endpoint, data=data)
    
    def test_connection(self) -> bool:
        """
        Test connection to Gitea API
        
        Returns:
            True if connection successful
        """
        try:
            user = self.get_current_user()
            logger.info(f"✅ Connected to Gitea as: {user['login']}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to Gitea: {e}")
            return False
