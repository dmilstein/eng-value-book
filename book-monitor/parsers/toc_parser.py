"""Parser for table of contents (TOC) org files."""

import re
import os
from typing import List, Tuple, Optional
from utils.exceptions import FileNotFoundError, ParseError


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
            ParseError: If there's an error reading or parsing the file
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(self.file_path, "TOC file is required for building the book")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except PermissionError:
            raise ParseError(self.file_path, details="Permission denied reading TOC file")
        except UnicodeDecodeError:
            raise ParseError(self.file_path, details="File encoding error - expected UTF-8")
        except Exception as e:
            raise ParseError(self.file_path, details=f"Unexpected error reading file: {str(e)}")
        
        if not content.strip():
            raise ParseError(self.file_path, details="TOC file is empty")
        
        try:
            return self._extract_chapters(content)
        except Exception as e:
            raise ParseError(self.file_path, details=f"Error extracting chapters: {str(e)}")
    
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
