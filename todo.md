# Book Monitor Implementation Checklist

## Project Setup and Foundation

### Step 1: Project Bootstrap
- [x] Create `book-monitor/` directory
- [x] Create directory structure:
  - [x] `templates/` directory
  - [x] `static/` directory
  - [x] `parsers/` directory with `__init__.py`
  - [x] `models/` directory with `__init__.py`
  - [x] `tests/` directory
  - [x] `utils/` directory
- [x] Create `requirements.txt` with dependencies
- [x] Create `app.py` with minimal Flask app
- [x] Verify Flask server starts on localhost:5000
- [x] Test root route returns "Book Monitor Running"
- [x] Initialize git repository
- [x] Create `.gitignore` file

### Step 2: Configuration and Models
- [x] Create `config.py` with Config class
- [x] Add all configuration constants
- [x] Create `models/book.py`:
  - [x] Book dataclass with all fields
  - [x] `calculate_total_words()` method
- [x] Create `models/chapter.py`:
  - [x] Section dataclass
  - [x] Chapter dataclass
  - [x] `calculate_word_count()` method
- [x] Update `models/__init__.py` with exports
- [x] Create `tests/test_models.py`:
  - [x] Test Book initialization
  - [x] Test Book.calculate_total_words()
  - [x] Test Chapter initialization
  - [x] Test Chapter.calculate_word_count()
  - [x] Test Section initialization
- [x] Run tests and ensure all pass

### Step 3: Org Parsing Utilities
- [x] Create `parsers/org_utils.py`:
  - [x] `count_words(text: str) -> int` function
  - [x] `remove_org_markup(text: str) -> str` function
  - [x] `extract_org_links(text: str) -> List[Tuple[str, str]]` function
- [x] Implement word counting exclusions:
  - [x] Exclude org directives (#+)
  - [x] Exclude property drawers
  - [x] Exclude tags
  - [x] Exclude comments
  - [x] Exclude code blocks
- [x] Create `tests/test_org_utils.py`:
  - [x] Test word counting with plain text
  - [x] Test word counting with bold/italic markup
  - [x] Test word counting with code blocks
  - [x] Test word counting with property drawers
  - [x] Test link extraction with valid links
  - [x] Test link extraction with malformed links
  - [x] Test markup removal
- [x] Run tests and ensure all pass

## File Processing Implementation

### Step 4: TOC Parser
- [ ] Create `parsers/toc_parser.py`:
  - [ ] TocParser class
  - [ ] `__init__` method accepting file path
  - [ ] `parse()` method returning chapter list
- [ ] Implement parsing logic:
  - [ ] Find all [[file:][title]] links
  - [ ] Extract filename and title
  - [ ] Maintain order
  - [ ] Skip invalid links
- [ ] Create `tests/fixtures/` directory
- [ ] Create `tests/fixtures/test_toc.org` with sample content
- [ ] Create `tests/test_toc_parser.py`:
  - [ ] Test parsing valid TOC file
  - [ ] Test handling missing TOC file
  - [ ] Test malformed links are skipped
  - [ ] Test empty TOC file
  - [ ] Test order preservation
- [ ] Add error handling for file operations
- [ ] Run tests and ensure all pass

### Step 5: Chapter Parser
- [ ] Create `parsers/chapter_parser.py`:
  - [ ] ChapterParser class
  - [ ] `__init__` method accepting file path
  - [ ] `parse()` method returning Chapter object
- [ ] Implement first-heading-only rule:
  - [ ] Find first "* " heading
  - [ ] Extract chapter title
  - [ ] Process only content until next "* " or EOF
  - [ ] Extract all "** " sections
  - [ ] Calculate word counts
- [ ] Create `tests/fixtures/test_chapter.org` with sample content
- [ ] Create `tests/test_chapter_parser.py`:
  - [ ] Test single top-level heading
  - [ ] Test multiple top-level headings (only first processed)
  - [ ] Test section extraction
  - [ ] Test word counting per section
  - [ ] Test empty chapter
  - [ ] Test chapter with no sections
- [ ] Integrate with org_utils for word counting
- [ ] Run tests and ensure all pass

### Step 6: Book Builder
- [ ] Create `parsers/book_builder.py`:
  - [ ] BookBuilder class
  - [ ] `__init__` method accepting directory path
  - [ ] `build()` method returning Book object
- [ ] Implement building logic:
  - [ ] Use TocParser for TOC file
  - [ ] Use ChapterParser for each chapter
  - [ ] Handle missing chapters gracefully
  - [ ] Calculate book statistics
- [ ] Add logging:
  - [ ] Import Python logging module
  - [ ] Log missing files as warnings
  - [ ] Log successful parsing as info
  - [ ] Log parse errors
- [ ] Update `app.py`:
  - [ ] Import Config and BookBuilder
  - [ ] Create global `book_data` variable
  - [ ] Create `load_book_data()` function
  - [ ] Call `load_book_data()` on startup
- [ ] Create `tests/test_book_builder.py`:
  - [ ] Test building complete book
  - [ ] Test handling missing chapters
  - [ ] Test empty TOC
  - [ ] Test word count aggregation
  - [ ] Mock file system for tests
- [ ] Run tests and ensure all pass

## Web Interface Implementation

### Step 7: Web Templates
- [ ] Create `templates/base.html`:
  - [ ] HTML5 doctype and structure
  - [ ] Meta tags for viewport
  - [ ] Navigation header
  - [ ] {% block content %}
  - [ ] Link to CSS file
- [ ] Create `templates/overview.html`:
  - [ ] Extend base.html
  - [ ] Display book title
  - [ ] Create chapters table
  - [ ] Show chapter numbers
  - [ ] Show chapter titles as links
  - [ ] Show section counts
  - [ ] Show word counts
  - [ ] Display total book word count
  - [ ] Add refresh button
- [ ] Create `templates/chapter.html`:
  - [ ] Extend base.html
  - [ ] Display chapter title
  - [ ] Show chapter word count
  - [ ] List all sections
  - [ ] Show section titles
  - [ ] Show section word counts
  - [ ] Display section content
  - [ ] Add back to overview link
- [ ] Create `static/style.css`:
  - [ ] Basic typography
  - [ ] Table styling
  - [ ] Navigation styling
  - [ ] Responsive design
  - [ ] Button styling
- [ ] Create `templates/error.html`:
  - [ ] Generic error template
  - [ ] Error message placeholder
  - [ ] Link to home

### Step 8: API Endpoints
- [ ] Update `app.py` with routes:
  - [ ] Implement `/` route:
    - [ ] Load book data
    - [ ] Pass to overview.html
    - [ ] Handle no data case
  - [ ] Implement `/chapter/<filename>` route:
    - [ ] Find chapter by filename
    - [ ] Pass to chapter.html
    - [ ] Return 404 if not found
  - [ ] Implement `/api/refresh` route:
    - [ ] Accept POST method
    - [ ] Reload book data
    - [ ] Return JSON response
- [ ] Add helper functions:
  - [ ] `get_book_data()` function
  - [ ] `find_chapter(filename)` function
- [ ] Update templates with Jinja2 variables:
  - [ ] overview.html variables
  - [ ] chapter.html variables
- [ ] Create `tests/test_routes.py`:
  - [ ] Test overview page loads
  - [ ] Test chapter page with valid filename
  - [ ] Test chapter page with invalid filename
  - [ ] Test refresh endpoint
  - [ ] Test JSON responses
- [ ] Run tests and ensure all pass

## Error Handling and Polish

### Step 9: Error Handling
- [ ] Create `utils/__init__.py`
- [ ] Create `utils/exceptions.py`:
  - [ ] BookMonitorException base class
  - [ ] FileNotFoundError class
  - [ ] ParseError class
  - [ ] ConfigError class
- [ ] Update parsers with error handling:
  - [ ] toc_parser.py error handling
  - [ ] chapter_parser.py error handling
  - [ ] book_builder.py error collection
- [ ] Create `utils/error_handler.py`:
  - [ ] Flask error handler setup function
  - [ ] 404 handler
  - [ ] 500 handler
  - [ ] Custom exception handlers
- [ ] Update `app.py`:
  - [ ] Import error handlers
  - [ ] Register error handlers
  - [ ] Add try/except to routes
  - [ ] Configure logging
- [ ] Create error templates:
  - [ ] `templates/errors/404.html`
  - [ ] `templates/errors/500.html`
  - [ ] Update generic error.html
- [ ] Add comprehensive logging:
  - [ ] Configure log format
  - [ ] Set log levels
  - [ ] Add contextual information
- [ ] Create `tests/test_error_handling.py`:
  - [ ] Test 404 responses
  - [ ] Test 500 responses
  - [ ] Test parse error recovery
  - [ ] Test missing file handling
- [ ] Run tests and ensure all pass

### Step 10: Final Integration
- [ ] Create `run.py`:
  - [ ] Logging setup
  - [ ] Configuration validation
  - [ ] Flask app startup
  - [ ] Keyboard interrupt handling
- [ ] Create `Makefile`:
  - [ ] `install` target
  - [ ] `run` target
  - [ ] `test` target
  - [ ] `clean` target
  - [ ] `lint` target
- [ ] Create `README.md`:
  - [ ] Project description
  - [ ] Features list
  - [ ] Installation instructions
  - [ ] Usage guide
  - [ ] Configuration documentation
  - [ ] Troubleshooting section
  - [ ] Contributing guidelines
- [ ] Create `sample_book/` directory:
  - [ ] Sample TOC file
  - [ ] 3 sample chapter files
  - [ ] Sample book README
- [ ] Add integration tests:
  - [ ] Create `tests/test_integration.py`
  - [ ] Test full workflow
  - [ ] Test refresh functionality
  - [ ] Test concurrent access
- [ ] Code quality improvements:
  - [ ] Add docstrings to all functions
  - [ ] Add type hints throughout
  - [ ] Format code with black
  - [ ] Run pylint/flake8
- [ ] Performance optimization:
  - [ ] Add caching mechanism
  - [ ] Implement change detection
  - [ ] Add simple benchmarks
- [ ] Update `.gitignore`:
  - [ ] Python artifacts
  - [ ] Virtual environment
  - [ ] IDE files
  - [ ] Log files

## Final Verification

### Testing and Validation
- [ ] Run all unit tests
- [ ] Run all integration tests
- [ ] Manual testing of all features
- [ ] Test with malformed org files
- [ ] Test with missing files
- [ ] Test with empty book
- [ ] Test refresh functionality
- [ ] Test error pages
- [ ] Verify logging works correctly

### Documentation Review
- [ ] README is complete and accurate
- [ ] All code has docstrings
- [ ] Configuration is documented
- [ ] Sample files demonstrate features
- [ ] Installation steps are clear
- [ ] Troubleshooting covers common issues

### Code Quality
- [ ] All code is formatted consistently
- [ ] No linting errors
- [ ] Type hints are complete
- [ ] Error handling is comprehensive
- [ ] Logging is informative
- [ ] No hardcoded values (use config)

### Deployment Ready
- [ ] Virtual environment works
- [ ] All dependencies in requirements.txt
- [ ] Makefile targets work
- [ ] Application starts without errors
- [ ] Can process sample book
- [ ] Performance is acceptable

## Optional Enhancements (Future)
- [ ] Add file watching for auto-refresh
- [ ] Implement WebSocket for live updates
- [ ] Add export functionality (PDF/EPUB)
- [ ] Create progress tracking over time
- [ ] Add search functionality
- [ ] Implement theming support
- [ ] Add multi-book support
- [ ] Create backup functionality
