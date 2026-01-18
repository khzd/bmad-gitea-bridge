"""
Epic Parser

Parse BMad epic files.

Authors: Khaled Z. & Claude (Anthropic)
"""

import re
from pathlib import Path
from typing import Dict, List, Any
import logging
from .base_parser import BaseParser

logger = logging.getLogger(__name__)


class EpicParser(BaseParser):
    """Parse BMad epic markdown files"""
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse epic file
        
        Returns:
            Parsed epic data:
            {
                'title': str,
                'description': str,
                'stories': List[str],
                'acceptance_criteria': List[str],
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
        
        # Extract description (intro or first section)
        description = sections.get('_intro', '')
        if not description and 'Description' in sections:
            description = sections['Description']
        
        # Extract stories
        stories = self._extract_stories()
        
        # Extract acceptance criteria
        acceptance_criteria = self._extract_acceptance_criteria()
        
        # Build parsed data
        self.parsed_data = {
            'title': title,
            'description': description,
            'stories': stories,
            'acceptance_criteria': acceptance_criteria,
            'sections': sections,
            'frontmatter': frontmatter,
            'file_path': self.file_path
        }
        
        logger.info(f"Parsed epic: {title} ({len(stories)} stories)")
        
        return self.parsed_data
    
    def _extract_stories(self) -> List[str]:
        """
        Extract story references from epic
        
        Returns:
            List of story titles/IDs
        """
        stories = []
        
        # Look for stories section
        sections = self.extract_sections()
        stories_section = sections.get('Stories', sections.get('User Stories', ''))
        
        if not stories_section:
            return stories
        
        # Extract list items
        pattern = r'^\s*[-*]\s+(.+)$'
        matches = re.findall(pattern, stories_section, re.MULTILINE)
        
        for match in matches:
            # Clean up checkbox syntax if present
            story = re.sub(r'\[[ x]\]\s*', '', match).strip()
            stories.append(story)
        
        return stories
    
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
        
        # Extract list items
        pattern = r'^\s*[-*]\s+(.+)$'
        matches = re.findall(pattern, ac_section, re.MULTILINE)
        
        criteria = [match.strip() for match in matches]
        
        return criteria