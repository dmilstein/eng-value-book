# Technical Book Writing System - Implementation Blueprint

## Phase 1: Foundation and Core Parsing

### Step 1.1: Project Setup
- Create directory structure
- Set up virtual environment
- Create requirements.txt
- Initialize git repository

### Step 1.2: Basic Flask Application
- Create minimal Flask app
- Set up basic routing
- Create placeholder templates
- Verify server runs

### Step 1.3: Configuration System
- Create config.py with settings
- Set up environment-based configuration
- Add path validation

### Step 1.4: Data Models
- Create book.py with Book dataclass
- Create chapter.py with Chapter and Section dataclasses
- Add basic validation methods

### Step 1.5: Org-mode Parsing Foundation
- Create org_utils.py with basic parsing functions
- Implement word counting logic
- Add markup removal functions

## Phase 2: File Processing

### Step 2.1: TOC Parser
- Create toc_parser.py
- Implement org link parsing
- Extract filenames and titles
- Handle malformed links

### Step 2.2: Chapter Parser
- Create chapter_parser.py
- Implement first-heading-only rule
- Parse sections under first heading
- Calculate word counts

### Step 2.3: Book Assembly
- Create book_builder.py
- Combine TOC and chapter data
- Calculate aggregate statistics
- Handle missing files

## Phase 3: Web Interface

### Step 3.1: Base Templates
- Create base.html template
- Set up Jinja2 inheritance
- Add minimal CSS

### Step 3.2: Overview Page
- Create overview.html template
- Display TOC with word counts
- Add total book statistics

### Step 3.3: Chapter Pages
- Create chapter.html template
- Display chapter content
- Show section breakdown

### Step 3.4: Navigation and Refresh
- Add navigation between pages
- Implement refresh endpoint
- Add error pages

## Phase 4: Error Handling and Testing

### Step 4.1: Error Handling
- Add file system error handling
- Implement parsing error recovery
- Create user-friendly error messages

### Step 4.2: Testing Infrastructure
- Set up pytest configuration
- Create test fixtures
- Add sample test files

### Step 4.3: Unit Tests
- Test parsers
- Test models
- Test utilities

### Step 4.4: Integration Tests
- Test Flask routes
- Test end-to-end workflows
- Test error scenarios

---

# Refined Implementation Steps

After reviewing the phases, here are the optimized, right-sized implementation steps:

## Implementation Steps

1. **Project Bootstrap**
   - Create directory structure and requirements.txt
   - Set up Flask with single route
   - Verify basic server functionality

2. **Configuration and Models**
   - Create config.py and data models
   - Add validation to models
   - Write tests for models

3. **Org Parsing Utilities**
   - Create word counting function
   - Add markup removal
   - Test with sample org content

4. **TOC Parser**
   - Parse org links from TOC file
   - Extract chapter information
   - Test with various link formats

5. **Chapter Parser**
   - Implement first-heading extraction
   - Parse sections under first heading
   - Test edge cases

6. **Book Builder**
   - Assemble book from TOC and chapters
   - Calculate statistics
   - Handle missing files gracefully

7. **Web Templates**
   - Create base template with navigation
   - Add overview page
   - Add chapter detail page

8. **API Endpoints**
   - Wire up overview route
   - Wire up chapter routes
   - Add refresh endpoint

9. **Error Handling**
   - Add comprehensive error handling
   - Create error templates
   - Test error scenarios

10. **Final Integration**
    - Connect all components
    - Add logging
    - Final testing pass

---

# LLM Implementation Prompts

## Prompt 1: Project Bootstrap

```text
Create a Python Flask application for monitoring a technical book written in org-mode files.

Set up the following:

1. Create this directory structure:
```
book-monitor/
├── app.py
├── requirements.txt
├── templates/
├── static/
├── parsers/
│   └── __init__.py
└── models/
    └── __init__.py
```

2. In requirements.txt, add:
```
Flask==2.3.3
Jinja2==3.1.2
orgparse==0.3.2
pytest==7.4.0
pytest-flask==1.2.0
```

3. In app.py, create a minimal Flask application with:
- A single route '/' that returns "Book Monitor Running"
- Configuration to run on localhost:5000
- Debug mode enabled

4. Create empty __init__.py files in parsers/ and models/ directories

Test that the server starts and responds to requests. Use proper Python project structure and follow Flask best practices.
```

## Prompt 2: Configuration and Models

```text
Building on the Flask book monitor app, create the configuration system and data models.

1. Create config.py in the root directory with:
```python
class Config:
    BOOK_DIRECTORY = "org-roam-tibook"
    TOC_FILENAME = "20250522085650-tech_investment_toc.org"
    HOST = "127.0.0.1"
    PORT = 5000
    DEBUG = True
    EXCLUDE_PATTERNS = [
        r'#\+.*',  # Org directives
        r':\w+:',  # Tags
        r'#.*',    # Comments
    ]
```

2. Create models/book.py with:
- A Book dataclass containing: title, chapters list, total_word_count, toc_file_path
- A method calculate_total_words() that sums chapter word counts

3. Create models/chapter.py with:
- A Section dataclass containing: title, content, word_count
- A Chapter dataclass containing: title, filename, sections list, word_count, section_count
- A method calculate_word_count() that sums section word counts

4. Update models/__init__.py to export the classes

5. Create tests/test_models.py with:
- Test for Book.calculate_total_words()
- Test for Chapter.calculate_word_count()
- Test for proper dataclass initialization

Use Python dataclasses, type hints, and follow Python best practices. Ensure all tests pass.
```

## Prompt 3: Org Parsing Utilities

```text
Create org-mode parsing utilities for the book monitor.

1. Create parsers/org_utils.py with:
- A function count_words(text: str) -> int that counts words excluding org markup
- A function remove_org_markup(text: str) -> str that strips org formatting
- A function extract_org_links(text: str) -> List[Tuple[str, str]] that finds [[file:][title]] links

2. The word counter should exclude:
- Org directives (lines starting with #+)
- Property drawers (:PROPERTIES: blocks)
- Tags (:tag:)
- Comments (lines starting with #)
- Code blocks (#+BEGIN_SRC blocks)

3. Create tests/test_org_utils.py with tests for:
- Word counting with plain text
- Word counting with org markup
- Link extraction with valid links
- Link extraction with malformed links
- Markup removal

Example org content to handle:
```
* Chapter Title
:PROPERTIES:
:ID: some-id
:END:

This is **bold** and *italic* text.

** Section One
Some content here with [[file:other.org][a link]].

#+BEGIN_SRC python
def code():
    pass
#+END_SRC
```

Ensure robust parsing that handles edge cases gracefully.
```

## Prompt 4: TOC Parser

```text
Create the TOC (Table of Contents) parser for the book monitor.

1. Create parsers/toc_parser.py with:
- A class TocParser that takes a file path
- A method parse() that returns a list of chapter info dictionaries
- Each chapter info should contain: filename, title, order

2. The parser should:
- Find all org links in format [[file:filename.org][Display Title]]
- Extract both the filename and display title
- Maintain the order as they appear in the file
- Skip invalid or malformed links
- Handle missing files gracefully

3. Create tests/test_toc_parser.py with:
- Test parsing a valid TOC file
- Test handling missing TOC file
- Test malformed links are skipped
- Test order preservation

4. Create tests/fixtures/test_toc.org with sample content:
```
* Table of Contents

** Part 1
- [[file:intro.org][Introduction]]
- [[file:chapter1.org][Getting Started]]

** Part 2
- [[file:chapter2.org][Advanced Topics]]
- [[broken-link]]
- [[file:missing.org][Missing Chapter]]
```

Use the org_utils functions from the previous step. Return empty list for missing files rather than raising exceptions.
```

## Prompt 5: Chapter Parser

```text
Create the chapter parser that implements the first-heading-only rule.

1. Create parsers/chapter_parser.py with:
- A class ChapterParser that takes a file path
- A method parse() that returns a Chapter object
- Logic to only process content under the FIRST top-level heading (*)

2. The parser should:
- Find the first line starting with "* " (single asterisk)
- Use that as the chapter title
- Only process content between this heading and the next top-level heading (or EOF)
- Extract all "** " sections within this range
- Calculate word counts for each section
- Ignore everything after the first top-level heading

3. Create tests/test_chapter_parser.py with:
- Test parsing a chapter with single top-level heading
- Test parsing a chapter with multiple top-level headings (only first processed)
- Test section extraction
- Test word counting

4. Create tests/fixtures/test_chapter.org:
```
#+TITLE: Test Chapter

Some preamble text that should be ignored.

* First Chapter Title
:PROPERTIES:
:ID: chapter-id
:END:

Introduction paragraph for the chapter.

** Section One
Content for section one.

** Section Two
More content here.

* Second Top Level
This should be completely ignored.

** Ignored Section
This content should not appear.
```

Use the Chapter and Section models from earlier. Integrate with org_utils for word counting.
```

## Prompt 6: Book Builder

```text
Create the book builder that assembles the complete book structure.

1. Create parsers/book_builder.py with:
- A class BookBuilder that takes a book directory path
- A method build() that returns a Book object
- Logic to read TOC and process all chapters

2. The builder should:
- Use TocParser to get chapter list from TOC file
- Use ChapterParser for each chapter file
- Handle missing chapter files (skip with warning)
- Calculate total book statistics
- Use paths from config.py

3. Update app.py to:
- Import Config and BookBuilder
- Create a global book_data variable
- Add a function load_book_data() that uses BookBuilder
- Call load_book_data() on startup

4. Create tests/test_book_builder.py with:
- Test building a complete book
- Test handling missing chapters
- Test word count aggregation
- Mock file system for tests

5. Add logging to book_builder.py:
- Log warnings for missing files
- Log info for successful parsing
- Log errors for parse failures

The builder should be resilient - if some chapters are missing or malformed, it should still build a book with the available chapters.
```

## Prompt 7: Web Templates

```text
Create the web templates for displaying the book content.

1. Create templates/base.html:
- Basic HTML5 structure
- Navigation header with "Book Monitor" title
- {% block content %} for child templates
- Link to minimal CSS

2. Create templates/overview.html extending base.html:
- Display book title
- Table showing all chapters with:
  - Chapter number
  - Title (linked to chapter detail)
  - Section count
  - Word count
- Total book word count at bottom
- Refresh button

3. Create templates/chapter.html extending base.html:
- Chapter title
- Total word count
- List of sections with:
  - Section title
  - Word count
  - Section content (rendered)
- Back to overview link

4. Create static/style.css with minimal styling:
- Basic typography
- Table styling
- Navigation styling
- Mobile-friendly responsive design

5. Create templates/error.html:
- Generic error page
- Error message display
- Link back to overview

Use Jinja2 templating features. Keep styling minimal and functional. Ensure templates are accessible and semantic HTML.
```

## Prompt 8: API Endpoints

```text
Wire up the Flask routes to serve the book content using the templates.

1. Update app.py with these routes:

- @app.route('/')
  - Load book data if not loaded
  - Render overview.html with book data
  - Handle case where no book data exists

- @app.route('/chapter/<filename>')
  - Find chapter by filename
  - Render chapter.html with chapter data
  - Return 404 if chapter not found

- @app.route('/api/refresh', methods=['POST'])
  - Reload book data
  - Return JSON response with success/error
  - Include new word count in response

2. Add helper functions:
- get_book_data() - safely access global book data
- find_chapter(filename) - find chapter in book data

3. Update templates to use the passed data:
- overview.html: use book.chapters, book.total_word_count
- chapter.html: use chapter.title, chapter.sections, etc.

4. Add error handling:
- Try/except blocks around file operations
- Proper HTTP status codes
- User-friendly error messages

5. Create tests/test_routes.py:
- Test overview page loads
- Test chapter page with valid filename
- Test chapter page with invalid filename
- Test refresh endpoint

Ensure all routes handle missing data gracefully and return appropriate status codes.
```

## Prompt 9: Error Handling

```text
Add comprehensive error handling throughout the application.

1. Create utils/exceptions.py with custom exceptions:
- BookMonitorException (base)
- FileNotFoundError
- ParseError
- ConfigError

2. Update parsers to handle errors gracefully:
- toc_parser.py: catch file errors, return empty list
- chapter_parser.py: catch parse errors, return empty chapter
- book_builder.py: collect errors, log them, continue processing

3. Create utils/error_handler.py:
- Function to set up Flask error handlers
- Handle 404, 500, and custom exceptions
- Log errors with context

4. Update app.py:
- Import and register error handlers
- Add try/except to all routes
- Add logging configuration

5. Create templates/errors/ directory with:
- 404.html - Page not found
- 500.html - Server error
- error.html - Generic error with message

6. Add comprehensive logging:
- Use Python logging module
- Different log levels (INFO, WARNING, ERROR)
- Include timestamps and context

7. Create tests/test_error_handling.py:
- Test 404 responses
- Test parse error recovery
- Test missing file handling

The app should never crash - all errors should be caught, logged, and shown to the user in a friendly way.
```

## Prompt 10: Final Integration

```text
Complete the final integration and polish for the book monitor application.

1. Create a run.py script:
- Set up logging
- Validate configuration
- Start the Flask app
- Handle keyboard interrupt gracefully

2. Add a Makefile with targets:
- install: Set up virtual environment and dependencies
- run: Start the development server
- test: Run all tests
- clean: Remove generated files

3. Create comprehensive README.md with:
- Project description
- Installation instructions
- Usage guide
- Configuration options
- Troubleshooting section

4. Add integration tests in tests/test_integration.py:
- Test full workflow: TOC → Chapters → Web display
- Test refresh functionality
- Test error recovery

5. Create sample_book/ directory with:
- Sample TOC file
- 3 sample chapter files
- README explaining the structure

6. Final polish:
- Add docstrings to all functions/classes
- Type hints throughout
- Code formatting with black
- Update .gitignore

7. Performance optimization:
- Cache parsed data
- Only re-parse changed files
- Add simple benchmarking

Ensure the application is production-ready for local use, well-documented, and easy to extend.
```

## Summary

These prompts build incrementally from a basic Flask setup to a fully functional book monitoring system. Each prompt:

1. Has a clear, focused objective
2. Builds on previous work
3. Includes testing requirements
4. Handles errors appropriately
5. Follows Python best practices

The progression ensures that at each step, you have a working system that can be tested before moving to the next phase. No code is left orphaned - everything connects into the final integrated application.
