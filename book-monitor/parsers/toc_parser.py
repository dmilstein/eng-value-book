"""Parser for table of contents (TOC) org files."""

import re
import os
import glob
import sys
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
        self.directory_path = os.path.dirname(file_path)

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
        file_pattern = r'\[\[file:([^\]]+)\]\[([^\]]+)\]\]'
        file_matches = re.findall(file_pattern, content)

        for filename, title in file_matches:
            # Clean up filename and title
            filename = filename.strip()
            title = title.strip()

            # Skip empty filenames or titles
            if filename and title:
                chapters.append((filename, title))

        # Pattern to match [[id:guid][title]] links (org-roam)
        id_pattern = r'\[\[id:([^\]]+)\]\[([^\]]+)\]\]'
        id_matches = re.findall(id_pattern, content)

        for guid, title in id_matches:
            # Clean up guid and title
            guid = guid.strip()
            title = title.strip()

            # Skip empty guids or titles
            if guid and title:
                # Resolve GUID to filename
                filename = self._resolve_guid_to_filename(guid)
                if filename:
                    chapters.append((filename, title))

        return chapters

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
            print(filename)

    except (FileNotFoundError, ParseError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
