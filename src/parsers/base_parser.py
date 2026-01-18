"""
Base Parser

Abstract base class for all BMad file parsers.

Authors: Khaled Z. & Claude (Anthropic)
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Base class for parsing BMad artifact files"""
    
    def __init__(self, file_path: Path):
        """
        Initialize parser
        
        Args:
            file_path: Path to file to parse
        """
        self.file_path = Path(file_path)
        self.content = ""
        self.parsed_data: Dict[str, Any] = {}
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
    
    def read_file(self) -> str:
        """
        Read file content
        
        Returns:
            File content as string
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return self.content
        except Exception as e:
            logger.error(f"Error reading file {self.file_path}: {e}")
            raise
    
    def extract_yaml_frontmatter(self) -> Optional[Dict]:
        """
        Extract YAML frontmatter if present
        
        Returns:
            Frontmatter as dict or None
        """
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, self.content, re.DOTALL)
        
        if match:
            try:
                import yaml
                frontmatter = yaml.safe_load(match.group(1))
                return frontmatter
            except Exception as e:
                logger.warning(f"Failed to parse YAML frontmatter: {e}")
                return None
        
        return None
    
    def extract_title(self) -> str:
        """
        Extract title from markdown (first # heading)
        
        Returns:
            Title or filename if not found
        """
        pattern = r'^#\s+(.+)$'
        match = re.search(pattern, self.content, re.MULTILINE)
        
        if match:
            return match.group(1).strip()
        
        # Fallback to filename
        return self.file_path.stem
    
    def extract_sections(self) -> Dict[str, str]:
        """
        Extract markdown sections (## headings)
        
        Returns:
            Dict of section_title: content
        """
        sections = {}
        
        # Split by ## headings
        pattern = r'^##\s+(.+?)$'
        parts = re.split(pattern, self.content, flags=re.MULTILINE)
        
        # First part is before any ## heading
        if parts[0].strip():
            sections['_intro'] = parts[0].strip()
        
        # Process section pairs (heading, content)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                section_title = parts[i].strip()
                section_content = parts[i + 1].strip()
                sections[section_title] = section_content
        
        return sections
    
    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Parse the file and extract structured data
        
        Returns:
            Parsed data as dictionary
        """
        pass
    
    def get_parsed_data(self) -> Dict[str, Any]:
        """
        Get parsed data
        
        Returns:
            Parsed data dictionary
        """
        if not self.parsed_data:
            self.parse()
        
        return self.parsed_data