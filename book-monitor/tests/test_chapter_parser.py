"""Tests for the chapter parser."""

import unittest
import tempfile
import os
from parsers.chapter_parser import ChapterParser
from models import Chapter, Section
from utils.exceptions import FileNotFoundError, ParseError

class TestChapterParser(unittest.TestCase):
    """Test cases for the ChapterParser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def _create_test_file(self, filename: str, content: str) -> str:
        """Create a test file with given content."""
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def test_single_top_level_heading(self):
        """Test parsing file with single top-level heading."""
        content = """* Chapter Title

This is chapter content.

** Section One

Section content here.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.title, "Chapter Title")
        self.assertEqual(len(chapter.sections), 1)
        self.assertEqual(chapter.sections[0].title, "Section One")

    def test_multiple_top_level_headings_only_first_processed(self):
        """Test that only first top-level heading is processed."""
        content = """* First Chapter

Content of first chapter.

** First Section

First section content.

* Second Chapter

This should be ignored.

** Ignored Section

This section should not appear.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.title, "First Chapter")
        self.assertEqual(len(chapter.sections), 1)
        self.assertEqual(chapter.sections[0].title, "First Section")

    def test_section_extraction(self):
        """Test extraction of multiple sections."""
        content = """* Chapter Title

Chapter introduction.

** First Section

First section content.

** Second Section

Second section content.

** Third Section

Third section content.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 3)
        self.assertEqual(chapter.sections[0].title, "First Section")
        self.assertEqual(chapter.sections[1].title, "Second Section")
        self.assertEqual(chapter.sections[2].title, "Third Section")

        # Check order
        self.assertEqual(chapter.sections[0].order, 0)
        self.assertEqual(chapter.sections[1].order, 1)
        self.assertEqual(chapter.sections[2].order, 2)

    def test_word_counting_per_section(self):
        """Test word counting for each section."""
        content = """* Chapter Title

** Section One

This has four words.

** Section Two

This section has six total words.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 2)
        self.assertEqual(chapter.sections[0].word_count, 4)
        self.assertEqual(chapter.sections[1].word_count, 6)

    def test_empty_chapter(self):
        """Test handling of empty file."""
        content = ""
        file_path = self._create_test_file("empty.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNone(chapter)

    def test_chapter_with_no_sections(self):
        """Test chapter with no second-level headings."""
        content = """* Chapter Title

This chapter has content but no sections.

Just some regular text content.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.title, "Chapter Title")
        self.assertEqual(len(chapter.sections), 0)
        # Should count intro content: "This chapter has content but no sections. Just some regular text content." (13 words)
        self.assertEqual(chapter.calculate_word_count(), 13)

    def test_missing_file(self):
        """Test handling of missing file."""
        with self.assertRaises(ParseError):
            parser = ChapterParser("/nonexistent/file.org")
            parser.parse()

    def test_chapter_title_with_tags(self):
        """Test chapter title extraction with tags."""
        content = """* Chapter Title :tag1:tag2:

Chapter content here.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(chapter.title, "Chapter Title")

    def test_section_title_with_tags(self):
        """Test section title extraction with tags."""
        content = """* Chapter Title

** Section Title :important:draft:

Section content here.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 1)
        self.assertEqual(chapter.sections[0].title, "Section Title")

    def test_word_counting_excludes_org_markup(self):
        """Test that word counting properly excludes org markup."""
        content = """* Chapter Title

** Section One

This has *bold text* and /italic text/.

#+BEGIN_SRC python
def code():
    return "not counted"
#+END_SRC

Regular text after code block.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 1)
        # Should count: This has bold text and italic text Regular text after code block (12 words)
        self.assertEqual(chapter.sections[0].word_count, 12)


    def test_intro_content_word_counting(self):
        """Test that intro content (before first section) is counted."""
        content = """* Chapter Title

This is intro content before any sections.
It has multiple sentences and should be counted.

** First Section

This is section content.

** Second Section

More section content here.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 2)
        
        # Check section word counts
        self.assertEqual(chapter.sections[0].word_count, 4)  # "This is section content."
        self.assertEqual(chapter.sections[1].word_count, 4)  # "More section content here."
        
        # Check total includes intro content
        # Intro: "This is intro content before any sections. It has multiple sentences and should be counted." (15 words)
        # Sections: 4 + 4 = 8 words
        # Total: 15 + 8 = 23 words
        self.assertEqual(chapter.calculate_word_count(), 23)

    def test_intro_content_with_org_markup(self):
        """Test that intro content word counting excludes org markup."""
        content = """* Chapter Title

This intro has *bold text* and /italic text/.

#+BEGIN_SRC python
def code():
    return "not counted"
#+END_SRC

Regular intro text after code block.

** Section One

Section content here.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 1)
        
        # Section: "Section content here." (3 words)
        self.assertEqual(chapter.sections[0].word_count, 3)
        
        # Intro should count: "This intro has bold text and italic text Regular intro text after code block" (14 words)
        # Total: 14 + 3 = 17 words
        self.assertEqual(chapter.calculate_word_count(), 17)

    def test_no_intro_content(self):
        """Test chapter with sections but no intro content."""
        content = """* Chapter Title
** First Section

Section content only.

** Second Section

More section content.
"""
        file_path = self._create_test_file("test.org", content)
        parser = ChapterParser(file_path)
        chapter = parser.parse()

        self.assertIsNotNone(chapter)
        self.assertEqual(len(chapter.sections), 2)
        
        # Should only count section content, no intro
        # Section 1: "Section content only." (3 words)
        # Section 2: "More section content." (3 words)
        # Total: 3 + 3 = 6 words
        self.assertEqual(chapter.calculate_word_count(), 6)


if __name__ == '__main__':
    unittest.main()
