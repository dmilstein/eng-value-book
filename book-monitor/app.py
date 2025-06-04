import logging
from flask import Flask, render_template, jsonify, abort
from config import Config
from parsers.book_builder import BookBuilder

app = Flask(__name__)
app.config.from_object(Config)

# Global book data
book_data = None

def load_book_data():
    """Load book data from org files."""
    global book_data
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        builder = BookBuilder(app.config['BOOK_DIRECTORY'])
        book_data = builder.build()
        
        if book_data:
            logger.info(f"Loaded book: {book_data.title} with {len(book_data.chapters)} chapters")
        else:
            logger.warning("Failed to load book data")
            
    except Exception as e:
        logger.error(f"Error loading book data: {str(e)}")
        book_data = None

def get_book_data():
    """Get the current book data, loading if necessary."""
    global book_data
    if book_data is None:
        load_book_data()
    return book_data

def find_chapter(filename):
    """Find a chapter by filename.
    
    Args:
        filename: The filename to search for
        
    Returns:
        Chapter object if found, None otherwise
    """
    book = get_book_data()
    if not book:
        return None
    
    # Try to match by converting chapter title to expected filename format
    for chapter in book.chapters:
        # Convert chapter title to filename format (lowercase, spaces to underscores)
        expected_filename = chapter.title.replace(' ', '_').lower() + '.org'
        if expected_filename == filename:
            return chapter
    
    # Also try direct filename match (for files like "20250527083643-intro_chapter.org")
    for chapter in book.chapters:
        if filename in chapter.title or chapter.title in filename:
            return chapter
    
    return None

@app.route('/')
def home():
    """Display the book overview page."""
    book = get_book_data()
    
    if not book:
        return render_template('error.html', 
                             error_message="No book data available. Please check your configuration and ensure the book directory contains a valid toc.org file.")
    
    return render_template('overview.html', book=book)

@app.route('/chapter/<filename>')
def chapter(filename):
    """Display a specific chapter page.
    
    Args:
        filename: The chapter filename (e.g., 'chapter_1.org')
    """
    chapter_obj = find_chapter(filename)
    
    if not chapter_obj:
        abort(404)
    
    return render_template('chapter.html', chapter=chapter_obj)

@app.route('/api/refresh', methods=['POST'])
def refresh():
    """Refresh the book data by reloading from files."""
    try:
        load_book_data()
        book = get_book_data()
        
        if book:
            return jsonify({
                'success': True,
                'message': f'Successfully refreshed book data. Loaded {len(book.chapters)} chapters.',
                'chapters': len(book.chapters),
                'total_words': book.calculate_total_words()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to load book data after refresh.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error during refresh: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error during refresh: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('error.html', 
                         error_message="The requested page could not be found."), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', 
                         error_message="An internal server error occurred."), 500

if __name__ == '__main__':
    load_book_data()
    app.run(debug=True, host='localhost', port=5000)
