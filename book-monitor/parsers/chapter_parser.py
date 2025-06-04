"""Parser for extracting chapter information from org files."""

import re
from typing import Optional
from models import Chapter, Section
from parsers.org_utils import count_words, remove_org_markup
from utils.exceptions import FileNotFoundError, ParseError


class ChapterParser:
    """Parser for extracting chapter information from org files."""
    
    def __init__(self, file_path: str):
        """Initialize parser with file path.
        
        Args:
            file_path: Path to the org file to parse
        """
        self.file_path = file_path
    
    def parse(self) -> Optional[Chapter]:
        """Parse the org file and return a Chapter object.
        
        Returns:
            Chapter object if parsing successful, None if file not found or empty
            
        Raises:
            FileNotFoundError: If the chapter file doesn't exist
            ParseError: If the file cannot be parsed
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(self.file_path, "Chapter file referenced in TOC but not found")
        except PermissionError:
            raise ParseError(self.file_path, details="Permission denied reading chapter file")
        except UnicodeDecodeError:
            raise ParseError(self.file_path, details="File encoding error - expected UTF-8")
        except Exception as e:
            raise ParseError(self.file_path, details=f"Unexpected error reading file: {str(e)}")
        
        if not content.strip():
            return None
        
        try:
            return self._extract_chapter(content)
        except Exception as e:
            raise ParseError(self.file_path, details=f"Error extracting chapter content: {str(e)}")
    
    def _extract_chapter(self, content: str) -> Optional[Chapter]:
        """Extract chapter information from file content.
        
        Args:
            content: The full file content
            
        Returns:
            Chapter object or None if no valid chapter found
        """
        lines = content.split('\n')
        
        # Find first top-level heading (starts with "* ")
        chapter_start = None
        chapter_title = None
        
        for i, line in enumerate(lines):
            if line.startswith('* '):
                chapter_start = i
                # Extract title (remove "* " prefix and any tags)
                title_line = line[2:].strip()
                # Remove tags (anything after first colon followed by word characters)
                title_match = re.match(r'^([^:]+?)(?:\s+:[a-zA-Z0-9_:]+:)?$', title_line)
                if title_match:
                    chapter_title = title_match.group(1).strip()
                else:
                    chapter_title = title_line
                break
        
        if chapter_start is None or not chapter_title:
            return None
        
        # Find end of chapter (next top-level heading or end of file)
        chapter_end = len(lines)
        for i in range(chapter_start + 1, len(lines)):
            if lines[i].startswith('* '):
                chapter_end = i
                break
        
        # Extract chapter content (only the first top-level heading section)
        chapter_lines = lines[chapter_start:chapter_end]
        chapter_content = '\n'.join(chapter_lines)
        
        # Create chapter object
        chapter = Chapter(title=chapter_title)
        
        # Extract sections (second-level headings "** ")
        sections = self._extract_sections(chapter_content)
        for section in sections:
            chapter.add_section(section)
        
        return chapter
    
    def _extract_sections(self, chapter_content: str) -> list[Section]:
        """Extract sections from chapter content.
        
        Args:
            chapter_content: Content of the chapter
            
        Returns:
            List of Section objects
        """
        sections = []
        lines = chapter_content.split('\n')
        
        current_section = None
        current_content_lines = []
        
        for line in lines:
            if line.startswith('** '):
                # Save previous section if exists
                if current_section is not None:
                    content = '\n'.join(current_content_lines).strip()
                    word_count = count_words(content)
                    section = Section(
                        title=current_section,
                        content=content,
                        order=len(sections)
                    )
                    # Override the auto-calculated word count with our org-aware count
                    section.word_count = word_count
                    sections.append(section)
                
                # Start new section
                title_line = line[3:].strip()
                # Remove tags
                title_match = re.match(r'^([^:]+?)(?:\s+:[a-zA-Z0-9_:]+:)?$', title_line)
                if title_match:
                    current_section = title_match.group(1).strip()
                else:
                    current_section = title_line
                current_content_lines = []
            
            elif current_section is not None:
                # Add line to current section content
                current_content_lines.append(line)
        
        # Save last section if exists
        if current_section is not None:
            content = '\n'.join(current_content_lines).strip()
            word_count = count_words(content)
            section = Section(
                title=current_section,
                content=content,
                order=len(sections)
            )
            # Override the auto-calculated word count with our org-aware count
            section.word_count = word_count
            sections.append(section)
        
        return sections
