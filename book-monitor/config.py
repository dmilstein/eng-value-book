"""Configuration settings for the book monitor application."""

class Config:
    """Application configuration constants."""
    
    # File paths
    BOOK_SOURCE_DIR = "org-roam-tibook"
    OUTPUT_DIR = "output"
    
    # Word count targets
    TARGET_WORDS_PER_CHAPTER = 3000
    TARGET_TOTAL_WORDS = 50000
    
    # File extensions to process
    SUPPORTED_EXTENSIONS = ['.org', '.md', '.txt']
    
    # Monitoring settings
    REFRESH_INTERVAL = 30  # seconds
    
    # Display settings
    SHOW_WORD_COUNTS = True
    SHOW_PROGRESS_BARS = True
    
    # Debug settings
    DEBUG = True
