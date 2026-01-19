"""
Epic Syncer - Synchronize BMad Epics to Gitea Milestones

Authors: Khaled Z. & Claude (Anthropic)
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
from parsers.epic_parser import EpicParser
from gitea.milestones import GiteaMilestones

logger = logging.getLogger(__name__)


class EpicSyncer:
    """Synchronize BMad epics to Gitea milestones"""
    
    def __init__(self, gitea_client, bmad_artifacts_path: Path):
        """
        Initialize epic syncer
        
        Args:
            gitea_client: GiteaClient instance
            bmad_artifacts_path: Path to BMad artifacts directory
        """
        self.gitea_client = gitea_client
        self.milestones = GiteaMilestones(gitea_client)
        self.artifacts_path = Path(bmad_artifacts_path)
        self.epics_path = self.artifacts_path / "epics"
        
        if not self.epics_path.exists():
            logger.warning(f"Epics directory not found: {self.epics_path}")
    
    def discover_epics(self) -> List[Path]:
        """
        Discover all epic markdown files
        
        Returns:
            List of epic file paths
        """
        if not self.epics_path.exists():
            return []
        
        epic_files = list(self.epics_path.glob("epic-*.md"))
        logger.info(f"Discovered {len(epic_files)} epic files")
        
        return epic_files
    
    def parse_epic(self, epic_file: Path) -> Dict:
        """
        Parse epic markdown file
        
        Args:
            epic_file: Path to epic file
        
        Returns:
            Parsed epic data
        """
        parser = EpicParser(epic_file)
        epic_data = parser.parse()
        
        return epic_data
    
    def _extract_due_date(self, epic_data: Dict) -> Optional[str]:
        """
        Extract due date from epic data
        
        Args:
            epic_data: Parsed epic data
        
        Returns:
            ISO format date string or None
        """
        sections = epic_data.get('sections', {})
        timeline = sections.get('Timeline', '')
        
        # Look for "Target:" date
        import re
        match = re.search(r'Target[:\s]+(\d{4}-\d{2}-\d{2})', timeline)
        
        if match:
            return match.group(1) + 'T23:59:59Z'  # ISO format
        
        return None
    
    def _milestone_exists(self, title: str) -> Optional[Dict]:
        """
        Check if milestone already exists
        
        Args:
            title: Milestone title to search for
        
        Returns:
            Milestone data if exists, None otherwise
        """
        # TODO: Implement milestone listing in GiteaMilestones
        # For now, we'll create new milestones each time
        return None
    
    def sync_epic(self, epic_file: Path, dry_run: bool = False) -> Dict:
        """
        Sync single epic to Gitea milestone
        
        Args:
            epic_file: Path to epic file
            dry_run: If True, don't create milestone
        
        Returns:
            Sync result with status and milestone data
        """
        # Parse epic
        epic_data = self.parse_epic(epic_file)
        
        title = epic_data['title']
        description = epic_data['description']
        due_date = self._extract_due_date(epic_data)
        
        logger.info(f"Syncing epic: {title}")
        
        # Check if already exists
        existing = self._milestone_exists(title)
        
        if existing:
            logger.info(f"Milestone already exists for epic: {title}")
            return {
                'status': 'exists',
                'epic_file': str(epic_file),
                'milestone': existing
            }
        
        if dry_run:
            logger.info(f"DRY RUN: Would create milestone for: {title}")
            return {
                'status': 'dry_run',
                'epic_file': str(epic_file),
                'title': title,
                'description': description,
                'due_date': due_date
            }
        
        # Create milestone
        try:
            milestone = self.milestones.create_epic_milestone(
                epic_title=title,
                epic_description=description
            )
            
            logger.info(f"✅ Created milestone for epic: {title}")
            
            return {
                'status': 'created',
                'epic_file': str(epic_file),
                'milestone': milestone
            }
        
        except Exception as e:
            logger.error(f"Failed to create milestone for {title}: {e}")
            return {
                'status': 'failed',
                'epic_file': str(epic_file),
                'error': str(e)
            }
    
    def sync_all_epics(self, dry_run: bool = False) -> Dict:
        """
        Sync all epics to Gitea milestones
        
        Args:
            dry_run: If True, don't create milestones
        
        Returns:
            Summary with results for all epics
        """
        epic_files = self.discover_epics()
        
        results = {
            'created': [],
            'exists': [],
            'failed': [],
            'dry_run': []
        }
        
        for epic_file in epic_files:
            result = self.sync_epic(epic_file, dry_run=dry_run)
            
            status = result['status']
            results[status].append(result)
        
        # Log summary
        logger.info(
            f"Epic sync complete: "
            f"{len(results['created'])} created, "
            f"{len(results['exists'])} existing, "
            f"{len(results['failed'])} failed"
        )
        
        return results
