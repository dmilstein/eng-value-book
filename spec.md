Draft a detailed, step-by-step blueprint for building this project. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

# Technical Book Writing System - Developer Specification

## Project Overview
A Python-based local web server that monitors org-mode files for a book project and generates HTML pages with word counts and rendered content. The system provides real-time visibility into writing progress through a web interface.

## Requirements

### Functional Requirements
1. Parse a table of contents org file to determine chapter order
2. Process individual chapter org files with specific content rules
3. Generate word counts at book, chapter, and section levels
4. Serve HTML pages via local web server
5. Support manual refresh for content updates
6. Render org-mode content to HTML

### Non-Functional Requirements
- Local development environment only
- Manual refresh mechanism (with future auto-refresh capability)
- Minimal styling (functional over aesthetic)
- Cross-platform Python compatibility
- Graceful handling of malformed org files

## Architecture

### Technology Stack
- **Backend**: Python 3.8+
- **Web Framework**: Flask (lightweight, suitable for local development)
- **Org Parsing**: Custom parser or `orgparse` library
- **HTML Generation**: Jinja2 templates (included with Flask)
- **File Monitoring**: `watchdog` library (for future auto-refresh)

### Directory Structure
```
book-monitor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template
│   ├── overview.html     # TOC and word counts
│   └── chapter.html      # Individual chapter view
├── static/
│   └── style.css         # Minimal CSS
├── parsers/
│   ├── __init__.py
│   ├── toc_parser.py     # TOC file parsing
│   ├── chapter_parser.py # Chapter file parsing
│   └── org_utils.py      # Org-mode utilities
└── models/
    ├── __init__.py
    ├── book.py           # Book data model
    └── chapter.py        # Chapter data model
```

## Data Models

### Book Class
```python
@dataclass
class Book:
    title: str
    chapters: List[Chapter]
    total_word_count: int
    toc_file_path: str

    def calculate_total_words(self) -> int:
        return sum(chapter.word_count for chapter in self.chapters)
```

### Chapter Class
```python
@dataclass
class Section:
    title: str
    content: str
    word_count: int

@dataclass
class Chapter:
    title: str
    filename: str
    sections: List[Section]
    word_count: int
    section_count: int

    def calculate_word_count(self) -> int:
        return sum(section.word_count for section in self.sections)
```

## File Processing Rules

### TOC File (`toc.org`)
- Parse org-mode links in format: `[[file:filename.org][Display Title]]`
- Extract filename and display title
- Maintain order as specified in file
- Handle missing or malformed links gracefully

### Chapter Files
- **Content Inclusion Rule**: Only process content under the first top-level heading (`* Title`)
- **Chapter Title**: Use the first top-level heading text
- **Sections**: All `**` subheadings under the first top-level heading
- **Ignored Content**: Everything after the first top-level heading
- **Word Counting**: Count all text content, excluding:
  - Org-mode markup (`**bold**`, `*italic*`, etc.)
  - Property drawers (`:PROPERTIES:` blocks)
  - Comments (`# comment`)
  - Code blocks and other special blocks

## API Endpoints

### Routes
```python
@app.route('/')
def overview():
    """Serve overview page with TOC and word counts"""

@app.route('/chapter/<filename>')
def chapter_detail(filename):
    """Serve individual chapter page"""

@app.route('/api/refresh')
def refresh_data():
    """Force refresh of all data (for manual refresh)"""
```

## Error Handling

### File System Errors
- **Missing TOC file**: Display error message, continue with empty book
- **Missing chapter files**: Skip missing chapters, log warnings
- **Permission errors**: Log error, display user-friendly message

### Parsing Errors
- **Malformed org syntax**: Skip problematic sections, continue processing
- **Invalid links in TOC**: Skip invalid entries, log warnings
- **Empty files**: Handle gracefully, show zero word count

### Web Server Errors
- **Port conflicts**: Try alternative ports (5000, 5001, 5002)
- **Template errors**: Fall back to plain text output
- **Static file serving**: Graceful degradation without CSS

## Configuration

### Settings File (`config.py`)
```python
class Config:
    # File paths
    BOOK_DIRECTORY = "org-roam-tibook"
    TOC_FILENAME = "toc.org"

    # Server settings
    HOST = "127.0.0.1"
    PORT = 5000
    DEBUG = True

    # Word counting
    EXCLUDE_PATTERNS = [
        r'#\+.*',  # Org directives
        r':\w+:',  # Tags
        r'#.*',    # Comments
    ]
```

## Implementation Plan

### Phase 1: Core Functionality
1. Set up Flask application structure
2. Implement basic org-mode parsing
3. Create data models
4. Build TOC parsing
5. Implement chapter parsing with content rules
6. Create basic HTML templates
7. Add word counting functionality

### Phase 2: Web Interface
1. Design overview page layout
2. Create chapter detail pages
3. Add navigation between pages
4. Implement manual refresh mechanism
5. Add basic error handling

### Phase 3: Polish & Future-Proofing
1. Add comprehensive error handling
2. Implement logging
3. Add file watching infrastructure (disabled by default)
4. Create minimal CSS styling
5. Add configuration management

## Testing Strategy

### Unit Tests
```python
# test_parsers.py
def test_toc_parser_valid_file():
    """Test parsing valid TOC file"""

def test_toc_parser_missing_file():
    """Test handling of missing TOC file"""

def test_chapter_parser_first_heading_only():
    """Test that only first top-level heading is processed"""

def test_word_count_accuracy():
    """Test word counting excludes markup"""

# test_models.py
def test_book_total_word_count():
    """Test book word count calculation"""

def test_chapter_section_parsing():
    """Test chapter section extraction"""
```

### Integration Tests
```python
# test_app.py
def test_overview_page_loads():
    """Test overview page renders without errors"""

def test_chapter_page_loads():
    """Test individual chapter pages load"""

def test_refresh_endpoint():
    """Test manual refresh functionality"""
```

### Test Data
Create sample org files:
- `test_toc.org` with valid and invalid links
- `test_chapter.org` with multiple top-level headings
- `malformed_chapter.org` with parsing edge cases

## Dependencies (`requirements.txt`)
```
Flask==2.3.3
Jinja2==3.1.2
watchdog==3.0.0
orgparse==0.3.2
pytest==7.4.0
pytest-flask==1.2.0
```

## Deployment Instructions

### Setup
```bash
# Clone/create project directory
cd book-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure book directory path in config.py
```

### Running
```bash
# Start development server
python app.py

# Access at http://localhost:5000
```

## Future Enhancements (Out of Scope)
- Auto-refresh via WebSocket connections
- Export functionality (PDF, EPUB)
- Writing progress tracking over time
- Advanced styling and themes
- Multi-book support
- Collaborative editing features

This specification provides a complete roadmap for implementing the technical book writing system with clear boundaries, error handling strategies, and extensibility for future features.
