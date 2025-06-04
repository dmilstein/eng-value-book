"""Tests for Flask routes."""

import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from app import app, load_book_data, get_book_data, find_chapter
from models import Book, Chapter, Section


class TestRoutes(unittest.TestCase):
    """Test cases for Flask routes."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Mock the book directory configuration
        app.config['BOOK_DIRECTORY'] = self.test_dir
        
        # Create test book data
        self.test_book = Book(title="Test Book", author="Test Author")
        
        chapter1 = Chapter(title="Introduction")
        section1 = Section(title="Section One", content="This is section one content.")
        chapter1.add_section(section1)
        
        chapter2 = Chapter(title="Second Chapter")
        section2 = Section(title="Section Two", content="This is section two content.")
        chapter2.add_section(section2)
        
        self.test_book.add_chapter(chapter1)
        self.test_book.add_chapter(chapter2)

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)

    @patch('app.get_book_data')
    def test_home_route_with_book_data(self, mock_get_book_data):
        """Test home route with valid book data."""
        mock_get_book_data.return_value = self.test_book
        
        response = self.app.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)
        self.assertIn(b'Test Author', response.data)

    @patch('app.get_book_data')
    def test_home_route_without_book_data(self, mock_get_book_data):
        """Test home route when no book data is available."""
        mock_get_book_data.return_value = None
        
        response = self.app.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No book data available', response.data)

    @patch('app.find_chapter')
    def test_chapter_route_with_valid_filename(self, mock_find_chapter):
        """Test chapter route with valid filename."""
        mock_find_chapter.return_value = self.test_book.chapters[0]
        
        response = self.app.get('/chapter/introduction.org')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Introduction', response.data)
        self.assertIn(b'Section One', response.data)

    @patch('app.find_chapter')
    def test_chapter_route_with_invalid_filename(self, mock_find_chapter):
        """Test chapter route with invalid filename."""
        mock_find_chapter.return_value = None
        
        response = self.app.get('/chapter/nonexistent.org')
        
        self.assertEqual(response.status_code, 404)

    @patch('app.load_book_data')
    @patch('app.get_book_data')
    def test_refresh_endpoint_success(self, mock_get_book_data, mock_load_book_data):
        """Test refresh endpoint with successful reload."""
        mock_get_book_data.return_value = self.test_book
        
        response = self.app.post('/api/refresh')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['chapters'], 2)
        self.assertGreater(data['total_words'], 0)

    @patch('app.load_book_data')
    @patch('app.get_book_data')
    def test_refresh_endpoint_failure(self, mock_get_book_data, mock_load_book_data):
        """Test refresh endpoint when reload fails."""
        mock_get_book_data.return_value = None
        
        response = self.app.post('/api/refresh')
        
        self.assertEqual(response.status_code, 500)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    @patch('app.load_book_data')
    def test_refresh_endpoint_exception(self, mock_load_book_data):
        """Test refresh endpoint when an exception occurs."""
        mock_load_book_data.side_effect = Exception("Test error")
        
        response = self.app.post('/api/refresh')
        
        self.assertEqual(response.status_code, 500)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Test error', data['error'])

    def test_find_chapter_function(self):
        """Test the find_chapter helper function."""
        with patch('app.get_book_data') as mock_get_book_data:
            mock_get_book_data.return_value = self.test_book
            
            # Test finding existing chapter
            chapter = find_chapter('introduction.org')
            self.assertIsNotNone(chapter)
            self.assertEqual(chapter.title, 'Introduction')
            
            # Test finding non-existent chapter
            chapter = find_chapter('nonexistent.org')
            self.assertIsNone(chapter)

    def test_find_chapter_no_book_data(self):
        """Test find_chapter when no book data is available."""
        with patch('app.get_book_data') as mock_get_book_data:
            mock_get_book_data.return_value = None
            
            chapter = find_chapter('any_chapter.org')
            self.assertIsNone(chapter)

    def test_get_book_data_function(self):
        """Test the get_book_data helper function."""
        with patch('app.book_data', None):
            with patch('app.load_book_data') as mock_load:
                get_book_data()
                mock_load.assert_called_once()

    def test_404_error_handler(self):
        """Test 404 error handler."""
        response = self.app.get('/nonexistent-route')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'could not be found', response.data)

    def test_json_response_format(self):
        """Test that API endpoints return proper JSON."""
        with patch('app.get_book_data') as mock_get_book_data:
            mock_get_book_data.return_value = self.test_book
            
            response = self.app.post('/api/refresh')
            
            # Verify it's valid JSON
            data = json.loads(response.data)
            
            # Verify required fields
            self.assertIn('success', data)
            self.assertIn('message', data)
            self.assertIn('chapters', data)
            self.assertIn('total_words', data)

    def test_refresh_endpoint_only_accepts_post(self):
        """Test that refresh endpoint only accepts POST requests."""
        response = self.app.get('/api/refresh')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed


if __name__ == '__main__':
    unittest.main()
