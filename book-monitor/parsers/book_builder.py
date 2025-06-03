"""Builder for constructing Book objects from org files."""

import logging
import os
from typing import Optional
from models import Book, Chapter
from parsers.toc_parser import TocParser
from parsers.chapter_parser import ChapterParser


class BookBuilder:
    """Builder for constructing Book objects from org files."""

    def __init__(self, directory_path: str):
        """Initialize builder with directory path.

        Args:
            directory_path: Path to the directory containing org files
        """
        self.directory_path = directory_path
        self.logger = logging.getLogger(__name__)

    def build(self) -> Optional[Book]:
        """Build a Book object from org files in the directory.

        Returns:
            Book object if successful, None if TOC file not found or empty
        """
        # Find and parse TOC file
        toc_path = os.path.join(self.directory_path, "toc.org")
        if not os.path.exists(toc_path):
            self.logger.warning(f"TOC file not found at {toc_path}")
            return None

        toc_parser = TocParser(toc_path)
        chapter_list = toc_parser.parse()

        if not chapter_list:
            self.logger.warning(f"No chapters found in TOC file {toc_path}")
            return None

        self.logger.info(f"Found {len(chapter_list)} chapters in TOC")

        # Create book object
        book = Book(title="Book Monitor", author="Unknown")

        # Process each chapter
        for filename, title in chapter_list:
            chapter = self._parse_chapter(filename, title)
            if chapter:
                book.add_chapter(chapter)
            else:
                self.logger.warning(f"Failed to parse chapter: {filename}")

        self.logger.info(f"Successfully built book with {len(book.chapters)} chapters")
        self.logger.info(f"Total word count: {book.calculate_total_words()}")

        return book

    def _parse_chapter(self, filename: str, expected_title: str) -> Optional[Chapter]:
        """Parse a single chapter file.

        Args:
            filename: Name of the chapter file
            expected_title: Expected title from TOC

        Returns:
            Chapter object if successful, None if file not found or parse error
        """
        chapter_path = os.path.join(self.directory_path, filename)

        if not os.path.exists(chapter_path):
            self.logger.warning(f"Chapter file not found: {chapter_path}")
            return None

        try:
            parser = ChapterParser(chapter_path)
            chapter = parser.parse()

            if chapter:
                self.logger.info(f"Successfully parsed chapter: {filename} ({chapter.calculate_word_count()} words)")
                return chapter
            else:
                self.logger.error(f"Failed to parse chapter content: {filename}")
                return None

        except Exception as e:
            self.logger.error(f"Error parsing chapter {filename}: {str(e)}")
            return None


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
    
    # Output word counts in simple text format
    print(f"Book: {book.title}")
    print(f"Author: {book.author}")
    print(f"Total Words: {book.calculate_total_words()}")
    print()
    
    for i, chapter in enumerate(book.chapters, 1):
        chapter_words = chapter.calculate_word_count()
        print(f"Chapter {i}: {chapter.title} ({chapter_words} words)")
        
        for j, section in enumerate(chapter.sections, 1):
            print(f"  Section {j}: {section.title} ({section.word_count} words)")
    
    print()
    print(f"Summary: {len(book.chapters)} chapters, {book.calculate_total_words()} total words")


if __name__ == '__main__':
    main()
