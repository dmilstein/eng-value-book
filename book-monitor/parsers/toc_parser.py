"""Parser for table of contents (TOC) org files."""

import re
import os
from typing import List, Tuple, Optional


class TocParser:
    """Parser for extracting chapter information from TOC org files."""
    
    def __init__(self, file_path: str):
        """
        Initialize the TOC parser.
        
        Args:
            file_path: Path to the TOC org file
        """
        self.file_path = file_path
    
    def parse(self) -> List[Tuple[str, str]]:
        """
        Parse the TOC file and extract chapter information.
        
        Returns:
            List of tuples (filename, title) for each chapter found
            
        Raises:
            FileNotFoundError: If the TOC file doesn't exist
            IOError: If there's an error reading the file
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"TOC file not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except IOError as e:
            raise IOError(f"Error reading TOC file {self.file_path}: {e}")
        
        return self._extract_chapters(content)
    
    def _extract_chapters(self, content: str) -> List[Tuple[str, str]]:
        """
        Extract chapter links from TOC content.
        
        Args:
            content: The content of the TOC file
            
        Returns:
            List of tuples (filename, title) for valid chapter links
        """
        chapters = []
        
        # Pattern to match [[file:filename][title]] links
        pattern = r'\[\[file:([^\]]+)\]\[([^\]]+)\]\]'
        
        matches = re.findall(pattern, content)
        
        for filename, title in matches:
            # Clean up filename and title
            filename = filename.strip()
            title = title.strip()
            
            # Skip empty filenames or titles
            if filename and title:
                chapters.append((filename, title))
        
        return chapters
