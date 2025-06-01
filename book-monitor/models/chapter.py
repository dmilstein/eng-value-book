"""Chapter and Section models for book structure."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Section:
    """Represents a section within a chapter."""
    
    title: str
    content: str = ""
    word_count: int = 0
    order: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate word count after initialization."""
        if self.content and self.word_count == 0:
            self.word_count = len(self.content.split())


@dataclass
class Chapter:
    """Represents a chapter containing sections."""
    
    title: str
    sections: List[Section] = field(default_factory=list)
    target_words: int = 3000
    order: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    summary: str = ""
    
    def calculate_word_count(self) -> int:
        """Calculate the total word count across all sections."""
        return sum(section.word_count for section in self.sections)
    
    def get_progress_percentage(self) -> float:
        """Calculate progress as percentage of target words."""
        total_words = self.calculate_word_count()
        if self.target_words == 0:
            return 0.0
        return min(100.0, (total_words / self.target_words) * 100)
    
    def add_section(self, section: Section) -> None:
        """Add a section to the chapter."""
        self.sections.append(section)
        self.updated_at = datetime.now()
    
    def get_section_by_title(self, title: str) -> Optional[Section]:
        """Find a section by its title."""
        for section in self.sections:
            if section.title == title:
                return section
        return None
    
    def reorder_sections(self) -> None:
        """Sort sections by their order field."""
        self.sections.sort(key=lambda s: s.order)
