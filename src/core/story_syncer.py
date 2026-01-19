"""
Story Syncer - Synchronize BMad Stories to Gitea Issues

Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional
from parsers.story_parser import StoryParser
from gitea.issues import GiteaIssues

logger = logging.getLogger(__name__)


class StorySyncer:
    """Synchronize BMad stories to Gitea issues"""
    
    def __init__(self, gitea_client, bmad_artifacts_path: Path, agents: List):
        """
        Initialize story syncer
        
        Args:
            gitea_client: GiteaClient instance
            bmad_artifacts_path: Path to BMad artifacts directory
            agents: List of Agent objects (for assignee mapping)
        """
        self.gitea_client = gitea_client
        self.issues = GiteaIssues(gitea_client)
        self.artifacts_path = Path(bmad_artifacts_path)
        self.stories_path = self.artifacts_path / "stories"
        self.agents = {agent.name: agent for agent in agents}
        
        if not self.stories_path.exists():
            logger.warning(f"Stories directory not found: {self.stories_path}")
    
    def discover_stories(self) -> List[Path]:
        """
        Discover all story markdown files
        
        Returns:
            List of story file paths
        """
        if not self.stories_path.exists():
            return []
        
        story_files = list(self.stories_path.glob("story-*.md"))
        logger.info(f"Discovered {len(story_files)} story files")
        
        return story_files
    
    def parse_story(self, story_file: Path) -> Dict:
        """
        Parse story markdown file
        
        Args:
            story_file: Path to story file
        
        Returns:
            Parsed story data
        """
        parser = StoryParser(story_file)
        story_data = parser.parse()
        
        return story_data
    
    def _extract_assignee(self, story_data: Dict) -> Optional[str]:
        """
        Extract assignee from story data
        
        Args:
            story_data: Parsed story data
        
        Returns:
            Gitea username (e.g., 'bmad-dev') or None
        """
        sections = story_data.get('sections', {})
        
        # Look for "Assignee" section
        assignee_section = sections.get('Assignee', '')
        
        # Try to extract agent name (e.g., "Dev (Amelia)" or just "Dev")
        match = re.search(r'\*\*([A-Za-z-]+)\*\*', assignee_section)
        
        if match:
            agent_name = match.group(1).lower()
            
            # Map to Gitea username
            if agent_name in self.agents:
                return f"bmad-{agent_name}"
        
        return None
    
    def _extract_status(self, story_data: Dict) -> str:
        """
        Extract status from story data
        
        Args:
            story_data: Parsed story data
        
        Returns:
            Status string ('Todo', 'In Progress', 'Done', etc.)
        """
        sections = story_data.get('sections', {})
        
        # Look for "Status" section
        status_section = sections.get('Status', '')
        
        # Extract status (typically "**Todo**" or "**In Progress**")
        match = re.search(r'\*\*([A-Za-z\s]+)\*\*', status_section)
        
        if match:
            return match.group(1).strip()
        
        return 'Unknown'
    
    def _extract_labels(self, story_data: Dict) -> List[str]:
        """
        Extract labels from story data
        
        Args:
            story_data: Parsed story data
        
        Returns:
            List of label names
        """
        sections = story_data.get('sections', {})
        
        # Look for "Labels" section
        labels_section = sections.get('Labels', '')
        
        # Extract labels (typically `label1`, `label2`)
        labels = re.findall(r'`([^`]+)`', labels_section)
        
        return labels
    
    def _build_issue_body(self, story_data: Dict) -> str:
        """
        Build issue body from story data
        
        Args:
            story_data: Parsed story data
        
        Returns:
            Formatted issue body (markdown)
        """
        sections = story_data.get('sections', {})
        
        # Build body
        body_parts = []
        
        # User Story
        if 'User Story' in sections:
            body_parts.append(f"## User Story\n\n{sections['User Story']}")
        
        # Description
        if story_data.get('description'):
            body_parts.append(f"## Description\n\n{story_data['description']}")
        
        # Epic reference
        if 'Epic' in sections:
            body_parts.append(f"## Epic\n\n{sections['Epic']}")
        
        # Acceptance Criteria
        if story_data.get('acceptance_criteria'):
            body_parts.append("## Acceptance Criteria\n")
            for criterion in story_data['acceptance_criteria']:
                body_parts.append(f"- [ ] {criterion}")
        
        # Tasks
        if story_data.get('tasks'):
            body_parts.append("\n## Tasks\n")
            for task in story_data['tasks']:
                checkbox = "[x]" if task['completed'] else "[ ]"
                body_parts.append(f"- {checkbox} {task['text']}")
        
        # Story Points
        if 'Story Points' in sections:
            body_parts.append(f"\n## Story Points\n\n{sections['Story Points']}")
        
        # Priority
        if 'Priority' in sections:
            body_parts.append(f"\n## Priority\n\n{sections['Priority']}")
        
        # Footer
        body_parts.append("\n---\n*Synced from BMad Method*")
        
        return "\n\n".join(body_parts)
    
    def _issue_exists(self, story_title: str) -> Optional[Dict]:
        """
        Check if issue already exists for this story
        
        Args:
            story_title: Story title to search for
        
        Returns:
            Issue data if exists, None otherwise
        """
        try:
            issues = self.gitea_client.list_issues(state='all')
            
            for issue in issues:
                if issue['title'] == story_title:
                    return issue
            
            return None
        
        except Exception as e:
            logger.warning(f"Could not check existing issues: {e}")
            return None
    
    def sync_story(self, story_file: Path, dry_run: bool = False) -> Dict:
        """
        Sync single story to Gitea issue
        
        Args:
            story_file: Path to story file
            dry_run: If True, don't create issue
        
        Returns:
            Sync result with status and issue data
        """
        # Parse story
        story_data = self.parse_story(story_file)
        
        title = story_data['title']
        body = self._build_issue_body(story_data)
        assignee = self._extract_assignee(story_data)
        status = self._extract_status(story_data)
        labels = self._extract_labels(story_data)
        
        logger.info(f"Syncing story: {title}")
        
        # Check if already exists
        existing = self._issue_exists(title)
        
        if existing:
            logger.info(f"Issue already exists for story: {title}")
            return {
                'status': 'exists',
                'story_file': str(story_file),
                'issue': existing
            }
        
        if dry_run:
            logger.info(f"DRY RUN: Would create issue for: {title}")
            return {
                'status': 'dry_run',
                'story_file': str(story_file),
                'title': title,
                'assignee': assignee,
                'labels': labels
            }
        
        # Create issue
        try:
            issue = self.issues.create_story_issue(
                story_title=title,
                story_body=body,
                assignee=assignee
            )
            
            # Close issue if status is "Done"
            if status.lower() == 'done':
                # TODO: Close issue via API
                logger.info(f"Story {title} is marked as Done (would close issue)")
            
            logger.info(f"✅ Created issue for story: {title}")
            
            return {
                'status': 'created',
                'story_file': str(story_file),
                'issue': issue,
                'assignee': assignee
            }
        
        except Exception as e:
            logger.error(f"Failed to create issue for {title}: {e}")
            return {
                'status': 'failed',
                'story_file': str(story_file),
                'error': str(e)
            }
    
    def sync_all_stories(self, dry_run: bool = False) -> Dict:
        """
        Sync all stories to Gitea issues
        
        Args:
            dry_run: If True, don't create issues
        
        Returns:
            Summary with results for all stories
        """
        story_files = self.discover_stories()
        
        results = {
            'created': [],
            'exists': [],
            'failed': [],
            'dry_run': []
        }
        
        for story_file in story_files:
            result = self.sync_story(story_file, dry_run=dry_run)
            
            status = result['status']
            results[status].append(result)
        
        # Log summary
        logger.info(
            f"Story sync complete: "
            f"{len(results['created'])} created, "
            f"{len(results['exists'])} existing, "
            f"{len(results['failed'])} failed"
        )
        
        return results
