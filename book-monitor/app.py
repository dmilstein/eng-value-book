import logging
from flask import Flask
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

@app.route('/')
def home():
    return "Book Monitor Running"

if __name__ == '__main__':
    load_book_data()
    app.run(debug=True, host='localhost', port=5000)
