"""
Story Parser

Parse BMad story files.

Authors: Khaled Z. & Claude (Anthropic)
"""

import re
from pathlib import Path
from typing import Dict, List, Any
import logging
from .base_parser import BaseParser

logger = logging.getLogger(__name__)


class StoryParser(BaseParser):
    """Parse BMad story markdown files"""
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse story file
        
        Returns:
            Parsed story data:
            {
                'title': str,
                'story_id': str,
                'description': str,
                'acceptance_criteria': List[str],
                'tasks': List[Dict],
                'epic': str,
                'assignee': str,
                'sections': Dict[str, str],
                'file_path': Path
            }
        """
        # Read file
        self.read_file()
        
        # Extract basic info
        title = self.extract_title()
        frontmatter = self.extract_yaml_frontmatter()
        sections = self.extract_sections()
        
        # Extract story ID from filename (e.g., story-001.md -> 001)
        story_id = self._extract_story_id()
        
        # Extract description
        description = sections.get('_intro', '')
        if not description and 'Description' in sections:
            description = sections['Description']
        
        # Extract acceptance criteria
        acceptance_criteria = self._extract_acceptance_criteria()
        
        # Extract tasks
        tasks = self._extract_tasks()
        
        # Extract epic reference
        epic = self._extract_epic_reference()
        
        # Extract assignee from frontmatter if present
        assignee = frontmatter.get('assignee', '') if frontmatter else ''
        
        # Build parsed data
        self.parsed_data = {
            'title': title,
            'story_id': story_id,
            'description': description,
            'acceptance_criteria': acceptance_criteria,
            'tasks': tasks,
            'epic': epic,
            'assignee': assignee,
            'sections': sections,
            'frontmatter': frontmatter,
            'file_path': self.file_path
        }
        
        logger.info(f"Parsed story: {story_id} - {title}")
        
        return self.parsed_data
    
    def _extract_story_id(self) -> str:
        """
        Extract story ID from filename
        
        Returns:
            Story ID (e.g., '001', '042')
        """
        # Pattern: story-NNN.md or story-NNN-name.md
        pattern = r'story-(\d+)'
        match = re.search(pattern, self.file_path.name)
        
        if match:
            return match.group(1)
        
        # Fallback to filename
        return self.file_path.stem
    
    def _extract_acceptance_criteria(self) -> List[str]:
        """
        Extract acceptance criteria
        
        Returns:
            List of acceptance criteria
        """
        criteria = []
        
        sections = self.extract_sections()
        ac_section = sections.get('Acceptance Criteria', sections.get('AC', ''))
        
        if not ac_section:
            return criteria
        
        # Extract list items or numbered items
        pattern = r'^\s*(?:[-*]|\d+\.)\s+(.+)$'
        matches = re.findall(pattern, ac_section, re.MULTILINE)
        
        criteria = [match.strip() for match in matches]
        
        return criteria
    
    def _extract_tasks(self) -> List[Dict[str, Any]]:
        """
        Extract tasks/subtasks
        
        Returns:
            List of task dictionaries
        """
        tasks = []
        
        sections = self.extract_sections()
        tasks_section = sections.get('Tasks', sections.get('Implementation', ''))
        
        if not tasks_section:
            return tasks
        
        # Extract tasks with checkbox status
        pattern = r'^\s*[-*]\s+\[([ x])\]\s+(.+)$'
        matches = re.findall(pattern, tasks_section, re.MULTILINE)
        
        for checkbox, task_text in matches:
            tasks.append({
                'text': task_text.strip(),
                'completed': checkbox.lower() == 'x'
            })
        
        return tasks
    
    def _extract_epic_reference(self) -> str:
        """
        Extract epic reference
        
        Returns:
            Epic title/ID or empty string
        """
        sections = self.extract_sections()
        
        # Check frontmatter first
        frontmatter = self.extract_yaml_frontmatter()
        if frontmatter and 'epic' in frontmatter:
            return frontmatter['epic']
        
        # Look for epic mention in sections
        for section_content in sections.values():
            pattern = r'Epic:\s*(.+?)(?:\n|$)'
            match = re.search(pattern, section_content)
            if match:
                return match.group(1).strip()
        
        return ''