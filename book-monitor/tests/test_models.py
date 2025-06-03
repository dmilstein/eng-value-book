"""Tests for the book monitor models."""

import unittest
from datetime import datetime
from models import Book, Chapter, Section


class TestSection(unittest.TestCase):
    """Test cases for the Section model."""

    def test_section_initialization(self):
        """Test Section initialization with basic fields."""
        section = Section(title="Introduction", content="This is the introduction.")

        self.assertEqual(section.title, "Introduction")
        self.assertEqual(section.content, "This is the introduction.")
        self.assertEqual(section.word_count, 4)  # "This is the introduction."
        self.assertEqual(section.order, 0)
        self.assertIsInstance(section.created_at, datetime)
        self.assertIsInstance(section.updated_at, datetime)

    def test_section_empty_content(self):
        """Test Section with empty content."""
        section = Section(title="Empty Section")

        self.assertEqual(section.title, "Empty Section")
        self.assertEqual(section.content, "")
        self.assertEqual(section.word_count, 0)

    def test_section_word_count_calculation(self):
        """Test automatic word count calculation."""
        content = "This is a test section with multiple words in it."
        section = Section(title="Test", content=content)

        self.assertEqual(section.word_count, 10)


class TestChapter(unittest.TestCase):
    """Test cases for the Chapter model."""

    def test_chapter_initialization(self):
        """Test Chapter initialization with basic fields."""
        chapter = Chapter(title="Chapter 1")

        self.assertEqual(chapter.title, "Chapter 1")
        self.assertEqual(len(chapter.sections), 0)
        self.assertEqual(chapter.order, 0)
        self.assertIsInstance(chapter.created_at, datetime)
        self.assertIsInstance(chapter.updated_at, datetime)
        self.assertEqual(chapter.summary, "")

    def test_chapter_calculate_word_count_empty(self):
        """Test word count calculation with no sections."""
        chapter = Chapter(title="Empty Chapter")

        self.assertEqual(chapter.calculate_word_count(), 0)

    def test_chapter_calculate_word_count_with_sections(self):
        """Test word count calculation with multiple sections."""
        chapter = Chapter(title="Test Chapter")

        section1 = Section(title="Section 1", content="This has four words.")
        section2 = Section(title="Section 2", content="This section has five words.")

        chapter.add_section(section1)
        chapter.add_section(section2)

        self.assertEqual(chapter.calculate_word_count(), 4 + 5)

    def test_chapter_get_section_by_title(self):
        """Test finding sections by title."""
        chapter = Chapter(title="Test Chapter")

        section1 = Section(title="Introduction", content="Intro content")
        section2 = Section(title="Conclusion", content="Conclusion content")

        chapter.add_section(section1)
        chapter.add_section(section2)

        found_section = chapter.get_section_by_title("Introduction")
        self.assertIsNotNone(found_section)
        self.assertEqual(found_section.content, "Intro content")

        not_found = chapter.get_section_by_title("Nonexistent")
        self.assertIsNone(not_found)


class TestBook(unittest.TestCase):
    """Test cases for the Book model."""

    def test_book_initialization(self):
        """Test Book initialization with basic fields."""
        book = Book(title="My Test Book", author="Test Author")

        self.assertEqual(book.title, "My Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(len(book.chapters), 0)
        self.assertIsInstance(book.created_at, datetime)
        self.assertIsInstance(book.updated_at, datetime)
        self.assertEqual(book.description, "")

    def test_book_calculate_total_words_empty(self):
        """Test total word calculation with no chapters."""
        book = Book(title="Empty Book")

        self.assertEqual(book.calculate_total_words(), 0)

    def test_book_calculate_total_words_with_chapters(self):
        """Test total word calculation with multiple chapters."""
        book = Book(title="Test Book")

        # Create chapters with sections
        chapter1 = Chapter(title="Chapter 1")
        section1 = Section(title="Section 1", content="This has four words.")
        chapter1.add_section(section1)

        chapter2 = Chapter(title="Chapter 2")
        section2 = Section(title="Section 2", content="This section has five words.")
        chapter2.add_section(section2)

        book.add_chapter(chapter1)
        book.add_chapter(chapter2)

        self.assertEqual(book.calculate_total_words(), 4 + 5)

    def test_book_get_chapter_by_title(self):
        """Test finding chapters by title."""
        book = Book(title="Test Book")

        chapter1 = Chapter(title="Introduction")
        chapter2 = Chapter(title="Conclusion")

        book.add_chapter(chapter1)
        book.add_chapter(chapter2)

        found_chapter = book.get_chapter_by_title("Introduction")
        self.assertIsNotNone(found_chapter)
        self.assertEqual(found_chapter.title, "Introduction")

        not_found = book.get_chapter_by_title("Nonexistent")
        self.assertIsNone(not_found)


if __name__ == '__main__':
    unittest.main()
