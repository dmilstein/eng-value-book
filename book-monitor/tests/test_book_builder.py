"""Tests for the book builder."""

import unittest
import tempfile
import os
import logging
from unittest.mock import patch, MagicMock
from parsers.book_builder import BookBuilder
from models import Book, Chapter, Section


class TestBookBuilder(unittest.TestCase):
    """Test cases for the BookBuilder class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        # Disable logging during tests
        logging.disable(logging.CRITICAL)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Re-enable logging
        logging.disable(logging.NOTSET)
        
        # Clean up temporary files
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)
    
    def _create_test_file(self, filename: str, content: str) -> str:
        """Create a test file with given content."""
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_building_complete_book(self):
        """Test building a complete book with TOC and chapters."""
        # Create TOC file
        toc_content = """#+TITLE: Table of Contents

* Chapters

- [[file:chapter1.org][First Chapter]]
- [[file:chapter2.org][Second Chapter]]
"""
        self._create_test_file("toc.org", toc_content)
        
        # Create chapter files
        chapter1_content = """* First Chapter

This is the first chapter introduction.

** Section One

Content of section one.

** Section Two

Content of section two.
"""
        self._create_test_file("chapter1.org", chapter1_content)
        
        chapter2_content = """* Second Chapter

This is the second chapter.

** Another Section

More content here.
"""
        self._create_test_file("chapter2.org", chapter2_content)
        
        # Build book
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        # Verify book structure
        self.assertIsNotNone(book)
        self.assertEqual(len(book.chapters), 2)
        self.assertEqual(book.chapters[0].title, "First Chapter")
        self.assertEqual(book.chapters[1].title, "Second Chapter")
        
        # Verify sections
        self.assertEqual(len(book.chapters[0].sections), 2)
        self.assertEqual(len(book.chapters[1].sections), 1)
        
        # Verify word count aggregation
        total_words = book.calculate_total_words()
        self.assertGreater(total_words, 0)
    
    def test_handling_missing_chapters(self):
        """Test handling of missing chapter files."""
        # Create TOC with reference to missing chapter
        toc_content = """#+TITLE: Table of Contents

* Chapters

- [[file:existing.org][Existing Chapter]]
- [[file:missing.org][Missing Chapter]]
"""
        self._create_test_file("toc.org", toc_content)
        
        # Create only one chapter file
        chapter_content = """* Existing Chapter

This chapter exists.

** Section

Some content.
"""
        self._create_test_file("existing.org", chapter_content)
        
        # Build book
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        # Should still build with available chapters
        self.assertIsNotNone(book)
        self.assertEqual(len(book.chapters), 1)
        self.assertEqual(book.chapters[0].title, "Existing Chapter")
    
    def test_empty_toc(self):
        """Test handling of empty TOC file."""
        # Create empty TOC
        self._create_test_file("toc.org", "")
        
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        self.assertIsNone(book)
    
    def test_missing_toc_file(self):
        """Test handling of missing TOC file."""
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        self.assertIsNone(book)
    
    def test_word_count_aggregation(self):
        """Test that word counts are properly aggregated."""
        # Create TOC
        toc_content = """#+TITLE: Table of Contents

* Chapters

- [[file:chapter1.org][Chapter One]]
"""
        self._create_test_file("toc.org", toc_content)
        
        # Create chapter with known word count
        chapter_content = """* Chapter One

** Section One

This has four words.

** Section Two

This section has five words.
"""
        self._create_test_file("chapter1.org", chapter_content)
        
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        self.assertIsNotNone(book)
        self.assertEqual(book.calculate_total_words(), 9)  # 4 + 5
    
    def test_chapter_parse_error_handling(self):
        """Test handling of chapter parse errors."""
        # Create TOC
        toc_content = """#+TITLE: Table of Contents

* Chapters

- [[file:good.org][Good Chapter]]
- [[file:bad.org][Bad Chapter]]
"""
        self._create_test_file("toc.org", toc_content)
        
        # Create good chapter
        good_content = """* Good Chapter

This is a valid chapter.
"""
        self._create_test_file("good.org", good_content)
        
        # Create bad chapter (no top-level heading)
        bad_content = """This file has no proper heading structure.

Just some random text.
"""
        self._create_test_file("bad.org", bad_content)
        
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        # Should build with only the good chapter
        self.assertIsNotNone(book)
        self.assertEqual(len(book.chapters), 1)
        self.assertEqual(book.chapters[0].title, "Good Chapter")
    
    @patch('parsers.book_builder.TocParser')
    def test_toc_parser_exception_handling(self, mock_toc_parser):
        """Test handling of TOC parser exceptions."""
        # Mock TocParser to raise exception
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse.side_effect = Exception("Parse error")
        mock_toc_parser.return_value = mock_parser_instance
        
        # Create TOC file
        self._create_test_file("toc.org", "dummy content")
        
        builder = BookBuilder(self.test_dir)
        
        # Should handle exception gracefully
        with self.assertLogs(level='ERROR'):
            book = builder.build()
        
        # Should return None due to exception
        self.assertIsNone(book)
    
    @patch('parsers.book_builder.ChapterParser')
    def test_chapter_parser_exception_handling(self, mock_chapter_parser):
        """Test handling of chapter parser exceptions."""
        # Create TOC
        toc_content = """#+TITLE: Table of Contents

* Chapters

- [[file:chapter1.org][Chapter One]]
"""
        self._create_test_file("toc.org", toc_content)
        self._create_test_file("chapter1.org", "dummy content")
        
        # Mock ChapterParser to raise exception
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse.side_effect = Exception("Parse error")
        mock_chapter_parser.return_value = mock_parser_instance
        
        builder = BookBuilder(self.test_dir)
        
        # Should handle exception gracefully
        with self.assertLogs(level='ERROR'):
            book = builder.build()
        
        # Should still return book object but with no chapters
        self.assertIsNotNone(book)
        self.assertEqual(len(book.chapters), 0)
    
    def test_logging_behavior(self):
        """Test that appropriate log messages are generated."""
        # Create complete book structure
        toc_content = """#+TITLE: Table of Contents

* Chapters

- [[file:chapter1.org][Chapter One]]
"""
        self._create_test_file("toc.org", toc_content)
        
        chapter_content = """* Chapter One

** Section

Some content here.
"""
        self._create_test_file("chapter1.org", chapter_content)
        
        builder = BookBuilder(self.test_dir)
        
        # Re-enable logging for this test
        logging.disable(logging.NOTSET)
        
        with self.assertLogs(level='INFO') as log:
            book = builder.build()
        
        # Verify log messages
        log_messages = [record.message for record in log.records]
        self.assertTrue(any("Found 1 chapters in TOC" in msg for msg in log_messages))
        self.assertTrue(any("Successfully parsed chapter" in msg for msg in log_messages))
        self.assertTrue(any("Successfully built book" in msg for msg in log_messages))
        
        # Disable logging again for tearDown
        logging.disable(logging.CRITICAL)


if __name__ == '__main__':
    unittest.main()
