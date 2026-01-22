"""
Gitea Organizations & Teams Management

Handles organization, team, and repository provisioning in Gitea.

Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
from typing import Dict, List, Optional, Any
from .client import GiteaClient, GiteaAPIError

logger = logging.getLogger(__name__)


class GiteaOrganizations:
    """Manage Gitea organizations, teams, and repositories"""

    def __init__(self, client: GiteaClient):
        """
        Initialize organization manager

        Args:
            client: GiteaClient instance with admin token
        """
        self.client = client
        logger.info("Initialized Gitea organization manager")

    def organization_exists(self, org_name: str) -> bool:
        """
        Check if organization exists

        Args:
            org_name: Organization name

        Returns:
            True if organization exists, False otherwise
        """
        try:
            response = self.client.get(f"/api/v1/orgs/{org_name}")
            return response.status_code == 200
        except GiteaAPIError:
            return False

    def create_organization(self, org_name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new organization

        Args:
            org_name: Organization name
            description: Organization description

        Returns:
            Organization data from API

        Raises:
            GiteaAPIError: If creation fails
        """
        payload = {
            "username": org_name,
            "description": description,
            "visibility": "private"
        }

        response = self.client.post("/api/v1/orgs", json=payload)
        logger.info(f"Created organization: {org_name}")
        return response.json()

    def ensure_organization(self, org_name: str, description: str = "") -> Dict[str, Any]:
        """
        Ensure organization exists (create if missing)

        Args:
            org_name: Organization name
            description: Organization description

        Returns:
            Organization data
        """
        if self.organization_exists(org_name):
            logger.info(f"Organization already exists: {org_name}")
            response = self.client.get(f"/api/v1/orgs/{org_name}")
            return response.json()
        else:
            return self.create_organization(org_name, description)

    def create_team(
        self,
        org_name: str,
        team_name: str,
        description: str = "",
        permission: str = "write",
        includes_all_repos: bool = True,
        units: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a team in an organization

        Args:
            org_name: Organization name
            team_name: Team name
            description: Team description
            permission: Team permission level (read, write, admin)
            includes_all_repos: Include all repositories
            units: Repository access types

        Returns:
            Team data from API

        Raises:
            GiteaAPIError: If creation fails
        """
        if units is None:
            units = [
                "repo.code",
                "repo.issues",
                "repo.pulls",
                "repo.releases",
                "repo.wiki",
                "repo.projects"
            ]

        payload = {
            "name": team_name,
            "description": description,
            "permission": permission,
            "includes_all_repositories": includes_all_repos,
            "units": units
        }

        response = self.client.post(f"/api/v1/orgs/{org_name}/teams", json=payload)
        logger.info(f"Created team: {team_name} in {org_name}")
        return response.json()

    def add_user_to_team(self, team_id: int, username: str) -> bool:
        """
        Add a user to a team

        Args:
            team_id: Team ID
            username: Username to add

        Returns:
            True if successful

        Raises:
            GiteaAPIError: If addition fails
        """
        try:
            self.client.put(f"/api/v1/teams/{team_id}/members/{username}")
            logger.debug(f"Added {username} to team {team_id}")
            return True
        except GiteaAPIError as e:
            logger.error(f"Failed to add {username} to team {team_id}: {e}")
            raise

    def add_users_to_team(self, team_id: int, usernames: List[str]) -> Dict[str, int]:
        """
        Add multiple users to a team

        Args:
            team_id: Team ID
            usernames: List of usernames

        Returns:
            Dictionary with success/failure counts
        """
        results = {"success": 0, "failed": 0}

        for username in usernames:
            try:
                self.add_user_to_team(team_id, username)
                results["success"] += 1
            except GiteaAPIError:
                results["failed"] += 1

        logger.info(f"Added {results['success']}/{len(usernames)} users to team {team_id}")
        return results

    def create_repo_in_org(
        self,
        org_name: str,
        repo_name: str,
        description: str = "",
        private: bool = True,
        auto_init: bool = True
    ) -> Dict[str, Any]:
        """
        Create a repository in an organization

        Args:
            org_name: Organization name
            repo_name: Repository name
            description: Repository description
            private: Make repository private
            auto_init: Initialize with README

        Returns:
            Repository data from API

        Raises:
            GiteaAPIError: If creation fails
        """
        payload = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": auto_init
        }

        response = self.client.post(f"/api/v1/orgs/{org_name}/repos", json=payload)
        logger.info(f"Created repository: {org_name}/{repo_name}")
        return response.json()
