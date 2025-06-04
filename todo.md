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
- [x] Create `parsers/toc_parser.py`:
  - [x] TocParser class
  - [x] `__init__` method accepting file path
  - [x] `parse()` method returning chapter list
- [x] Implement parsing logic:
  - [x] Find all [[file:][title]] links
  - [x] Extract filename and title
  - [x] Maintain order
  - [x] Skip invalid links
- [x] Create `tests/fixtures/` directory
- [x] Create `tests/fixtures/test_toc.org` with sample content
- [x] Create `tests/test_toc_parser.py`:
  - [x] Test parsing valid TOC file
  - [x] Test handling missing TOC file
  - [x] Test malformed links are skipped
  - [x] Test empty TOC file
  - [x] Test order preservation
- [x] Add error handling for file operations
- [x] Run tests and ensure all pass

### Step 5: Chapter Parser
- [x] Create `parsers/chapter_parser.py`:
  - [x] ChapterParser class
  - [x] `__init__` method accepting file path
  - [x] `parse()` method returning Chapter object
- [x] Implement first-heading-only rule:
  - [x] Find first "* " heading
  - [x] Extract chapter title
  - [x] Process only content until next "* " or EOF
  - [x] Extract all "** " sections
  - [x] Calculate word counts
- [x] Create `tests/fixtures/test_chapter.org` with sample content
- [x] Create `tests/test_chapter_parser.py`:
  - [x] Test single top-level heading
  - [x] Test multiple top-level headings (only first processed)
  - [x] Test section extraction
  - [x] Test word counting per section
  - [x] Test empty chapter
  - [x] Test chapter with no sections
- [x] Integrate with org_utils for word counting
- [x] Run tests and ensure all pass

### Step 6: Book Builder
- [x] Create `parsers/book_builder.py`:
  - [x] BookBuilder class
  - [x] `__init__` method accepting directory path
  - [x] `build()` method returning Book object
- [x] Implement building logic:
  - [x] Use TocParser for TOC file
  - [x] Use ChapterParser for each chapter
  - [x] Handle missing chapters gracefully
  - [x] Calculate book statistics
- [x] Add logging:
  - [x] Import Python logging module
  - [x] Log missing files as warnings
  - [x] Log successful parsing as info
  - [x] Log parse errors
- [x] Update `app.py`:
  - [x] Import Config and BookBuilder
  - [x] Create global `book_data` variable
  - [x] Create `load_book_data()` function
  - [x] Call `load_book_data()` on startup
- [x] Create `tests/test_book_builder.py`:
  - [x] Test building complete book
  - [x] Test handling missing chapters
  - [x] Test empty TOC
  - [x] Test word count aggregation
  - [x] Mock file system for tests
- [x] Run tests and ensure all pass

## Web Interface Implementation

### Step 7: Web Templates
- [x] Create `templates/base.html`:
  - [x] HTML5 doctype and structure
  - [x] Meta tags for viewport
  - [x] Navigation header
  - [x] {% block content %}
  - [x] Link to CSS file
- [x] Create `templates/overview.html`:
  - [x] Extend base.html
  - [x] Display book title
  - [x] Create chapters table
  - [x] Show chapter numbers
  - [x] Show chapter titles as links
  - [x] Show section counts
  - [x] Show word counts
  - [x] Display total book word count
  - [x] Add refresh button
- [x] Create `templates/chapter.html`:
  - [x] Extend base.html
  - [x] Display chapter title
  - [x] Show chapter word count
  - [x] List all sections
  - [x] Show section titles
  - [x] Show section word counts
  - [x] Display section content
  - [x] Add back to overview link
- [x] Create `static/style.css`:
  - [x] Basic typography
  - [x] Table styling
  - [x] Navigation styling
  - [x] Responsive design
  - [x] Button styling
- [x] Create `templates/error.html`:
  - [x] Generic error template
  - [x] Error message placeholder
  - [x] Link to home

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
