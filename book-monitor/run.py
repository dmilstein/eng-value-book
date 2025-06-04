#!/usr/bin/env python3
"""
Book Monitor Application Runner

This script provides a proper entry point for the Book Monitor application
with configuration validation, logging setup, and graceful error handling.
"""

import sys
import os
import logging
import signal
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, load_book_data
from config import Config
from utils.exceptions import ConfigError, FileNotFoundError, ParseError


def setup_logging():
    """Configure logging for the application."""
    log_level = logging.DEBUG if Config.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('book_monitor.log')
        ]
    )
    
    # Reduce noise from werkzeug in production
    if not Config.DEBUG:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)


def validate_configuration():
    """Validate the application configuration.
    
    Raises:
        ConfigError: If configuration is invalid
    """
    logger = logging.getLogger(__name__)
    
    # Check if book directory is configured
    if not hasattr(Config, 'BOOK_DIRECTORY') or not Config.BOOK_DIRECTORY:
        raise ConfigError('BOOK_DIRECTORY', 'Book directory not configured')
    
    # Check if book directory exists
    book_dir = Path(Config.BOOK_DIRECTORY)
    if not book_dir.exists():
        raise ConfigError('BOOK_DIRECTORY', f'Directory does not exist: {Config.BOOK_DIRECTORY}')
    
    if not book_dir.is_dir():
        raise ConfigError('BOOK_DIRECTORY', f'Path is not a directory: {Config.BOOK_DIRECTORY}')
    
    # Check if TOC file exists
    toc_file = book_dir / 'toc.org'
    if not toc_file.exists():
        logger.warning(f'TOC file not found: {toc_file}')
        logger.warning('The application will start but may not display any content')
    
    logger.info(f'Configuration validated. Book directory: {Config.BOOK_DIRECTORY}')


def signal_handler(signum, frame):
    """Handle keyboard interrupt gracefully."""
    logger = logging.getLogger(__name__)
    logger.info('Received interrupt signal, shutting down gracefully...')
    sys.exit(0)


def main():
    """Main entry point for the application."""
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info('Starting Book Monitor application...')
    
    try:
        # Validate configuration
        validate_configuration()
        
        # Load initial book data
        logger.info('Loading initial book data...')
        load_book_data()
        logger.info('Book data loaded successfully')
        
        # Start the Flask application
        logger.info('Starting Flask server...')
        logger.info(f'Application will be available at http://localhost:5000')
        
        app.run(
            debug=Config.DEBUG,
            host='localhost',
            port=5000,
            use_reloader=False  # Disable reloader to avoid double startup
        )
        
    except ConfigError as e:
        logger.error(f'Configuration error: {e}')
        logger.error('Please check your configuration and try again')
        sys.exit(1)
        
    except FileNotFoundError as e:
        logger.error(f'Required file not found: {e}')
        logger.error('Please ensure all required files exist and try again')
        sys.exit(1)
        
    except ParseError as e:
        logger.error(f'Parse error: {e}')
        logger.error('Please check your org files for syntax errors and try again')
        sys.exit(1)
        
    except Exception as e:
        logger.error(f'Unexpected error during startup: {e}')
        logger.error('Please check the logs for more details')
        sys.exit(1)


if __name__ == '__main__':
    main()
