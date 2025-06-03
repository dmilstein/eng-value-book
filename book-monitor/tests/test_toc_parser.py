"""Tests for the TOC parser."""

import unittest
import os
import tempfile
from parsers.toc_parser import TocParser


class TestTocParser(unittest.TestCase):
    """Test cases for the TocParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.test_toc_path = os.path.join(self.test_fixtures_dir, 'test_toc.org')
    
    def test_parsing_valid_toc_file(self):
        """Test parsing a valid TOC file."""
        parser = TocParser(self.test_toc_path)
        chapters = parser.parse()
        
        expected = [
            ('chapter1.org', 'Introduction'),
            ('chapter2.org', 'Getting Started'),
            ('chapter3.org', 'Advanced Topics'),
            ('appendix.org', 'Appendix A'),
            ('chapter4.org', 'Conclusion'),
            ('chapter5.org', 'References and Bibliography')
        ]
        
        self.assertEqual(chapters, expected)
    
    def test_handling_missing_toc_file(self):
        """Test handling of missing TOC file."""
        parser = TocParser('nonexistent_file.org')
        
        with self.assertRaises(FileNotFoundError) as context:
            parser.parse()
        
        self.assertIn('TOC file not found', str(context.exception))
        self.assertIn('nonexistent_file.org', str(context.exception))
    
    def test_malformed_links_are_skipped(self):
        """Test that malformed links are properly skipped."""
        # Create a temporary file with only malformed links
        malformed_content = """
#+TITLE: Malformed Links Test

* Bad Links
** [[file:][Empty Title]]
** [[file:missing_title.org]]
** [[incomplete_link.org][Missing File Prefix]]
** [[file:empty_filename.org][]]
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as temp_file:
            temp_file.write(malformed_content)
            temp_file_path = temp_file.name
        
        try:
            parser = TocParser(temp_file_path)
            chapters = parser.parse()
            
            # Should return empty list since all links are malformed
            self.assertEqual(chapters, [])
        finally:
            os.unlink(temp_file_path)
    
    def test_empty_toc_file(self):
        """Test handling of empty TOC file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as temp_file:
            temp_file.write("")
            temp_file_path = temp_file.name
        
        try:
            parser = TocParser(temp_file_path)
            chapters = parser.parse()
            
            self.assertEqual(chapters, [])
        finally:
            os.unlink(temp_file_path)
    
    def test_order_preservation(self):
        """Test that chapter order is preserved."""
        content = """
* First Chapter
** [[file:z_last.org][Should Be First]]

* Second Chapter  
** [[file:a_first.org][Should Be Second]]

* Third Chapter
** [[file:m_middle.org][Should Be Third]]
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            parser = TocParser(temp_file_path)
            chapters = parser.parse()
            
            expected = [
                ('z_last.org', 'Should Be First'),
                ('a_first.org', 'Should Be Second'),
                ('m_middle.org', 'Should Be Third')
            ]
            
            self.assertEqual(chapters, expected)
        finally:
            os.unlink(temp_file_path)
    
    def test_file_read_error_handling(self):
        """Test handling of file read errors."""
        # Create a file and then make it unreadable (if possible on this system)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as temp_file:
            temp_file.write("test content")
            temp_file_path = temp_file.name
        
        try:
            # Try to make file unreadable
            os.chmod(temp_file_path, 0o000)
            
            parser = TocParser(temp_file_path)
            
            with self.assertRaises(IOError) as context:
                parser.parse()
            
            self.assertIn('Error reading TOC file', str(context.exception))
        except (OSError, PermissionError):
            # Skip this test if we can't change file permissions
            self.skipTest("Cannot change file permissions on this system")
        finally:
            # Restore permissions and clean up
            try:
                os.chmod(temp_file_path, 0o644)
                os.unlink(temp_file_path)
            except (OSError, PermissionError):
                pass


if __name__ == '__main__':
    unittest.main()
