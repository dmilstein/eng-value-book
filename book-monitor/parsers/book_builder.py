"""Builder for constructing Book objects from org files."""

import logging
import os
from typing import Optional, List
from models import Book, Chapter
from parsers.toc_parser import TocParser
from parsers.chapter_parser import ChapterParser
from utils.exceptions import FileNotFoundError, ParseError, ConfigError


class BookBuilder:
    """Builder for constructing Book objects from org files."""

    def __init__(self, directory_path: str):
        """Initialize builder with directory path.

        Args:
            directory_path: Path to the directory containing org files

        Raises:
            ConfigError: If directory path is invalid
        """
        if not directory_path:
            raise ConfigError("BOOK_DIRECTORY", "Directory path cannot be empty")

        if not os.path.exists(directory_path):
            raise ConfigError("BOOK_DIRECTORY", f"Directory does not exist: {directory_path}")

        if not os.path.isdir(directory_path):
            raise ConfigError("BOOK_DIRECTORY", f"Path is not a directory: {directory_path}")

        self.directory_path = directory_path
        self.logger = logging.getLogger(__name__)
        self.errors = []  # Collect non-fatal errors

    def build(self) -> Optional[Book]:
        """Build a Book object from org files in the directory.

        Returns:
            Book object if successful, None if TOC file not found or empty

        Raises:
            FileNotFoundError: If TOC file doesn't exist
            ParseError: If TOC file cannot be parsed
        """
        # Clear previous errors
        self.errors = []

        # Find and parse TOC file
        toc_path = os.path.join(self.directory_path, "toc.org")

        try:
            toc_parser = TocParser(toc_path)
            chapter_list = toc_parser.parse()
        except (FileNotFoundError, ParseError) as e:
            self.logger.error(f"Failed to parse TOC: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error parsing TOC: {str(e)}")
            raise ParseError(toc_path, details=f"Unexpected error: {str(e)}")

        if not chapter_list:
            self.logger.warning(f"No chapters found in TOC file {toc_path}")
            return None

        self.logger.info(f"Found {len(chapter_list)} chapters in TOC")

        # Create book object
        book = Book(title="Book Monitor", author="Unknown")

        # Process each chapter
        successful_chapters = 0
        for filename, title in chapter_list:
            try:
                chapter = self._parse_chapter(filename, title)
                if chapter:
                    book.add_chapter(chapter)
                    successful_chapters += 1
                else:
                    self.errors.append(f"Chapter {filename} returned no content")
            except (FileNotFoundError, ParseError) as e:
                self.logger.warning(f"Failed to parse chapter {filename}: {str(e)}")
                self.errors.append(f"Chapter {filename}: {str(e)}")
            except Exception as e:
                self.logger.error(f"Unexpected error parsing chapter {filename}: {str(e)}")
                self.errors.append(f"Chapter {filename}: Unexpected error - {str(e)}")

        if successful_chapters == 0:
            self.logger.error("No chapters could be parsed successfully")
            return None

        self.logger.info(f"Successfully built book with {len(book.chapters)} chapters")
        self.logger.info(f"Total word count: {book.calculate_total_words()}")

        if self.errors:
            self.logger.warning(f"Encountered {len(self.errors)} non-fatal errors during build")

        return book

    def _parse_chapter(self, filename: str, expected_title: str) -> Optional[Chapter]:
        """Parse a single chapter file.

        Args:
            filename: Name of the chapter file
            expected_title: Expected title from TOC

        Returns:
            Chapter object if successful, None if file not found or parse error

        Raises:
            FileNotFoundError: If chapter file doesn't exist
            ParseError: If chapter file cannot be parsed
        """
        chapter_path = os.path.join(self.directory_path, filename)

        parser = ChapterParser(chapter_path)
        chapter = parser.parse()

        if chapter:
            self.logger.info(f"Successfully parsed chapter: {filename} ({chapter.calculate_word_count()} words)")
            return chapter
        else:
            self.logger.warning(f"Chapter file {filename} contains no parseable content")
            return None

    def get_errors(self) -> List[str]:
        """Get list of non-fatal errors encountered during build.

        Returns:
            List of error messages
        """
        return self.errors.copy()


def create_word_count_bar(word_count: int, max_count: int, width: int = 20) -> str:
    """Create a horizontal bar representation of word count using Unicode blocks.

    Args:
        word_count: Current word count to display
        max_count: Maximum word count for scaling
        width: Width of the bar in characters

    Returns:
        String representation of the bar chart
    """
    if max_count == 0:
        return '░' * width

    # Calculate how many full blocks and partial block
    ratio = word_count / max_count
    filled_chars = ratio * width
    full_blocks = int(filled_chars)
    partial = filled_chars - full_blocks

    # Unicode block characters from full to empty
    blocks = ['█', '▉', '▊', '▋', '▌', '▍', '▎', '▏']

    # Build the bar
    bar = '█' * full_blocks

    # Add partial block if needed
    if partial > 0 and full_blocks < width:
        partial_index = int(partial * len(blocks))
        if partial_index >= len(blocks):
            partial_index = len(blocks) - 1
        bar += blocks[partial_index]
        full_blocks += 1

    # Fill remaining with light shade
    #bar += '░' * (width - full_blocks)
    bar += ' ' * (width - full_blocks)

    return bar


def main():
    """Main function for command-line usage."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Build book from org files and display word counts')
    parser.add_argument('directory', help='Directory containing org files with toc.org')
    args = parser.parse_args()

    # Configure basic logging
    logging.basicConfig(
        level=logging.WARNING,  # Only show warnings and errors
        format='%(levelname)s: %(message)s'
    )

    # Build the book
    builder = BookBuilder(args.directory)
    book = builder.build()

    if not book:
        print("Failed to build book from directory:", args.directory)
        sys.exit(1)

    # Output word counts with visual bars
    print(f"Book: {book.title}")
    print(f"Author: {book.author}")
    print(f"Total Words: {book.calculate_total_words()}")
    print()

    # Find max word counts for scaling bars
    max_chapter_words = max(chapter.calculate_word_count() for chapter in book.chapters) if book.chapters else 0
    max_section_words = 0
    for chapter in book.chapters:
        if chapter.sections:
            chapter_max = max(section.word_count for section in chapter.sections)
            max_section_words = max(max_section_words, chapter_max)

    # Section 2: All sections organized by chapter, using consistent scale
    print("SECTIONS:")
    print("-" * 60)
    for i, chapter in enumerate(book.chapters, 1):
        if chapter.sections:
            print(f"Chapter {i}: {chapter.title}")

            for j, section in enumerate(chapter.sections, 1):
                section_bar = create_word_count_bar(section.word_count, max_section_words, 20)
                print(f" {section.word_count:>5} {section_bar} Section {j}: {section.title:.80}")
            print()

    print()

    # Section 2: Chapter overview with word counts and bars
    print("CHAPTERS:")
    print("-" * 60)
    for i, chapter in enumerate(book.chapters, 1):
        chapter_words = chapter.calculate_word_count()
        chapter_bar = create_word_count_bar(chapter_words, max_chapter_words, 25)
        print(f"{chapter_words:6} {chapter_bar} Chapter {i}: {chapter.title}")

    print(f"Summary: {len(book.chapters)} chapters, {book.calculate_total_words()} total words")

if __name__ == '__main__':
    main()
