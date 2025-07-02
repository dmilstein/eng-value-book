"""Parser for table of contents (TOC) org files."""

import re
import os
import glob
import sys
from typing import List, Tuple, Optional, Union
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
        self.directory_path = os.path.dirname(file_path)

    def parse(self) -> List[Union[Tuple[str, str], Tuple[None, str]]]:
        """
        Parse the TOC file and extract chapter information and parts.

        Returns:
            List of tuples where:
            - (filename, title) for chapters
            - (None, part_title) for book parts

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

    def _extract_chapters(self, content: str) -> List[Union[Tuple[str, str], Tuple[None, str]]]:
        """
        Extract chapter links and parts from TOC content within the first org-mode section only.

        Args:
            content: The content of the TOC file

        Returns:
            List of tuples where:
            - (filename, title) for chapters
            - (None, part_title) for book parts
        """
        # Find the first top-level heading and extract content until the next one
        first_section_content = self._extract_first_section(content)

        items = []
        lines = first_section_content.split('\n')

        for line in lines:
            # Check for second-level headings (parts)
            part_match = re.match(r'^\*\*\s+(.+)$', line)
            if part_match:
                part_title = part_match.group(1).strip()
                # Check if this line contains a link - if so, it's not a part
                if not re.search(r'\[\[(?:file:|id:)[^\]]+\]\[[^\]]+\]\]', line):
                    items.append((None, part_title))
                    continue

            # Pattern to match [[file:filename][title]] links
            file_matches = re.findall(r'\[\[file:([^\]]+)\]\[([^\]]+)\]\]', line)
            for filename, title in file_matches:
                filename = filename.strip()
                title = title.strip()
                if filename and title:
                    items.append((filename, title))

            # Pattern to match [[id:guid][title]] links (org-roam)
            id_matches = re.findall(r'\[\[id:([^\]]+)\]\[([^\]]+)\]\]', line)
            for guid, title in id_matches:
                guid = guid.strip()
                title = title.strip()
                if guid and title:
                    filename = self._resolve_guid_to_filename(guid)
                    if filename:
                        items.append((filename, title))

        return items

    def _extract_first_section(self, content: str) -> str:
        """
        Extract content from the first org-mode section only.

        Args:
            content: The full content of the TOC file

        Returns:
            Content of the first section (from first * heading to next * heading or EOF)
        """
        lines = content.split('\n')
        first_heading_found = False
        section_lines = []

        for line in lines:
            # Check if this is a top-level heading (starts with single *)
            if re.match(r'^\*\s+', line):
                if first_heading_found:
                    # We've reached the second top-level heading, stop here
                    break
                else:
                    # This is the first top-level heading, start collecting
                    first_heading_found = True
                    section_lines.append(line)
            elif first_heading_found:
                # We're inside the first section, collect all lines
                section_lines.append(line)
            # If we haven't found the first heading yet, skip lines

        return '\n'.join(section_lines)

    def _resolve_guid_to_filename(self, guid: str) -> Optional[str]:
        """
        Resolve an org-roam GUID to its corresponding filename.

        Args:
            guid: The GUID to resolve

        Returns:
            Filename if found, None otherwise
        """
        # Search for org files in the directory
        org_files = glob.glob(os.path.join(self.directory_path, "*.org"))

        for file_path in org_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                    # Look for #+ID: guid or :ID: guid patterns
                    id_patterns = [
                        rf'^#\+ID:\s*{re.escape(guid)}\s*$',
                        rf'^\s*:ID:\s*{re.escape(guid)}\s*$'
                    ]

                    for pattern in id_patterns:
                        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                            return os.path.basename(file_path)

            except (IOError, UnicodeDecodeError):
                # Skip files that can't be read
                continue

        return None


def main():
    """
    Command line interface for the TOC parser.

    Usage: python toc_parser.py <path_to_toc_file>

    For now, just skips over the "Part I/II/III" dividers.
    """
    if len(sys.argv) != 2:
        print("Usage: python toc_parser.py <path_to_toc_file>", file=sys.stderr)
        sys.exit(1)

    toc_file_path = sys.argv[1]

    try:
        parser = TocParser(toc_file_path)
        chapters = parser.parse()

        # Output just the filenames in order
        for filename, title in chapters:
            if filename is not None:
                print(filename)

    except (FileNotFoundError, ParseError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
