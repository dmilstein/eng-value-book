"""Book model for tracking book structure and progress."""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .chapter import Chapter


@dataclass
class Book:
    """Represents a book with chapters and metadata."""
    
    title: str
    author: str = ""
    chapters: List['Chapter'] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    description: str = ""
    
    def calculate_total_words(self) -> int:
        """Calculate the total word count across all chapters."""
        return sum(chapter.calculate_word_count() for chapter in self.chapters)
    
    def add_chapter(self, chapter: 'Chapter') -> None:
        """Add a chapter to the book."""
        self.chapters.append(chapter)
        self.updated_at = datetime.now()
    
    def get_chapter_by_title(self, title: str) -> Optional['Chapter']:
        """Find a chapter by its title."""
        for chapter in self.chapters:
            if chapter.title == title:
                return chapter
        return None
