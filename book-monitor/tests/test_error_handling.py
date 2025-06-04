"""Tests for error handling functionality."""

import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from app import app
from utils.exceptions import BookMonitorException, FileNotFoundError, ParseError, ConfigError
from parsers.book_builder import BookBuilder


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.test_dir)

    def test_404_response_html(self):
        """Test 404 responses for HTML requests."""
        response = self.app.get('/nonexistent-page')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
        self.assertIn(b'404', response.data)

    def test_404_response_api(self):
        """Test 404 responses for API requests."""
        response = self.app.get('/api/nonexistent-endpoint')
        
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not Found')
        self.assertEqual(data['status_code'], 404)

    def test_500_response_html(self):
        """Test 500 responses for HTML requests."""
        with patch('app.get_book_data') as mock_get_book_data:
            # Force an exception in the route
            mock_get_book_data.side_effect = Exception("Test error")
            
            response = self.app.get('/')
            
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'Internal Server Error', response.data)
            self.assertIn(b'500', response.data)

    def test_parse_error_recovery(self):
        """Test recovery from parse errors."""
        # Create invalid TOC file
        toc_content = "This is not valid org content [[invalid"
        toc_path = os.path.join(self.test_dir, "toc.org")
        with open(toc_path, 'w') as f:
            f.write(toc_content)
        
        builder = BookBuilder(self.test_dir)
        
        # Should handle parse errors gracefully
        book = builder.build()
        self.assertIsNone(book)

    def test_missing_file_handling(self):
        """Test handling of missing files."""
        # Test with non-existent directory
        with self.assertRaises(ConfigError):
            BookBuilder("/nonexistent/directory")

    def test_config_error_handling(self):
        """Test configuration error handling."""
        # Test with empty directory path
        with self.assertRaises(ConfigError) as context:
            BookBuilder("")
        
        self.assertIn("Directory path cannot be empty", str(context.exception))

    def test_file_not_found_exception(self):
        """Test FileNotFoundError exception."""
        error = FileNotFoundError("/path/to/missing/file.org", "Test details")
        
        self.assertEqual(error.file_path, "/path/to/missing/file.org")
        self.assertEqual(error.details, "Test details")
        self.assertIn("File not found", str(error))

    def test_parse_error_exception(self):
        """Test ParseError exception."""
        error = ParseError("/path/to/file.org", line_number=42, details="Invalid syntax")
        
        self.assertEqual(error.file_path, "/path/to/file.org")
        self.assertEqual(error.line_number, 42)
        self.assertEqual(error.details, "Invalid syntax")
        self.assertIn("line 42", str(error))

    def test_config_error_exception(self):
        """Test ConfigError exception."""
        error = ConfigError("BOOK_DIRECTORY", "Directory not found")
        
        self.assertEqual(error.config_key, "BOOK_DIRECTORY")
        self.assertEqual(error.details, "Directory not found")
        self.assertIn("BOOK_DIRECTORY", str(error))

    def test_book_monitor_exception_base(self):
        """Test base BookMonitorException."""
        error = BookMonitorException("Test message", "Test details")
        
        self.assertEqual(error.message, "Test message")
        self.assertEqual(error.details, "Test details")
        self.assertEqual(str(error), "Test message: Test details")

    def test_api_error_responses(self):
        """Test API error response format."""
        with patch('app.load_book_data') as mock_load:
            mock_load.side_effect = ConfigError("TEST_KEY", "Test error")
            
            response = self.app.post('/api/refresh')
            
            self.assertEqual(response.status_code, 500)
            
            data = json.loads(response.data)
            self.assertFalse(data['success'])
            self.assertIn('Configuration error', data['error'])
            self.assertEqual(data['config_key'], 'TEST_KEY')

    def test_error_collection_in_builder(self):
        """Test that BookBuilder collects non-fatal errors."""
        # Create TOC with mix of valid and invalid chapters
        toc_content = """* Table of Contents
** [[file:good.org][Good Chapter]]
** [[file:missing.org][Missing Chapter]]
"""
        toc_path = os.path.join(self.test_dir, "toc.org")
        with open(toc_path, 'w') as f:
            f.write(toc_content)
        
        # Create only the good chapter
        good_content = """* Good Chapter
This is a valid chapter.
"""
        good_path = os.path.join(self.test_dir, "good.org")
        with open(good_path, 'w') as f:
            f.write(good_content)
        
        builder = BookBuilder(self.test_dir)
        book = builder.build()
        
        # Should build successfully with one chapter
        self.assertIsNotNone(book)
        self.assertEqual(len(book.chapters), 1)
        
        # Should have collected errors for missing chapter
        errors = builder.get_errors()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("missing.org" in error for error in errors))


if __name__ == '__main__':
    unittest.main()
