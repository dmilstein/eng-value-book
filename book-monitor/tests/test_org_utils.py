"""Tests for org-mode parsing utilities."""

import unittest
from parsers.org_utils import count_words, remove_org_markup, extract_org_links


class TestOrgUtils(unittest.TestCase):
    """Test cases for org-mode utility functions."""
    
    def test_count_words_plain_text(self):
        """Test word counting with plain text."""
        text = "This is a simple test with seven words."
        self.assertEqual(count_words(text), 8)
    
    def test_count_words_empty_text(self):
        """Test word counting with empty text."""
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words(None), 0)
    
    def test_count_words_with_bold_italic_markup(self):
        """Test word counting with bold and italic markup."""
        text = "This has *bold text* and /italic text/ markup."
        # Should count: This has bold text and italic text markup (8 words)
        self.assertEqual(count_words(text), 8)
    
    def test_count_words_with_code_blocks(self):
        """Test word counting excludes code blocks."""
        text = """This is regular text.
#+BEGIN_SRC python
def hello():
    print("This should not be counted")
#+END_SRC
More regular text here."""
        # Should count: This is regular text More regular text here (7 words)
        self.assertEqual(count_words(text), 7)
    
    def test_count_words_with_property_drawers(self):
        """Test word counting excludes property drawers."""
        text = """This is regular text.
:PROPERTIES:
:ID: some-id
:CREATED: 2023-01-01
:END:
More text after properties."""
        # Should count: This is regular text More text after properties (7 words)
        self.assertEqual(count_words(text), 7)
    
    def test_count_words_with_org_directives(self):
        """Test word counting excludes org directives."""
        text = """#+TITLE: My Document
#+AUTHOR: Test Author
#+DATE: 2023-01-01

This is the actual content that should be counted."""
        # Should count: This is the actual content that should be counted (9 words)
        self.assertEqual(count_words(text), 9)
    
    def test_count_words_with_tags(self):
        """Test word counting excludes tags."""
        text = """* Heading with tags :tag1:tag2:
This content should be counted.
** Subheading :another_tag:
More content here."""
        # Should count: Heading with tags This content should be counted Subheading More content here (10 words)
        self.assertEqual(count_words(text), 10)
    
    def test_count_words_with_comments(self):
        """Test word counting excludes comments."""
        text = """This is regular text.
# This is a comment and should not be counted
More regular text."""
        # Should count: This is regular text More regular text (6 words)
        self.assertEqual(count_words(text), 6)
    
    def test_remove_org_markup_bold_italic(self):
        """Test markup removal for bold and italic text."""
        text = "This has *bold text* and /italic text/."
        expected = "This has bold text and italic text."
        self.assertEqual(remove_org_markup(text), expected)
    
    def test_remove_org_markup_underline_strikethrough(self):
        """Test markup removal for underline and strikethrough."""
        text = "This has _underlined text_ and +strikethrough text+."
        expected = "This has underlined text and strikethrough text."
        self.assertEqual(remove_org_markup(text), expected)
    
    def test_remove_org_markup_code(self):
        """Test markup removal for code."""
        text = "This has ~inline code~ and =verbatim text=."
        expected = "This has inline code and verbatim text."
        self.assertEqual(remove_org_markup(text), expected)
    
    def test_remove_org_markup_links(self):
        """Test markup removal for links."""
        text = "Visit [[https://example.com][Example Site]] or [[https://test.com]]."
        expected = "Visit Example Site or https://test.com."
        self.assertEqual(remove_org_markup(text), expected)
    
    def test_remove_org_markup_empty_text(self):
        """Test markup removal with empty text."""
        self.assertEqual(remove_org_markup(""), "")
        self.assertEqual(remove_org_markup(None), "")
    
    def test_extract_org_links_with_description(self):
        """Test link extraction with description."""
        text = "Visit [[https://example.com][Example Site]] for more info."
        links = extract_org_links(text)
        expected = [("https://example.com", "Example Site")]
        self.assertEqual(links, expected)
    
    def test_extract_org_links_simple(self):
        """Test link extraction without description."""
        text = "Visit [[https://example.com]] for more info."
        links = extract_org_links(text)
        expected = [("https://example.com", "https://example.com")]
        self.assertEqual(links, expected)
    
    def test_extract_org_links_multiple(self):
        """Test extraction of multiple links."""
        text = "Visit [[https://example.com][Example]] and [[https://test.com]]."
        links = extract_org_links(text)
        expected = [
            ("https://example.com", "Example"),
            ("https://test.com", "https://test.com")
        ]
        self.assertEqual(links, expected)
    
    def test_extract_org_links_malformed(self):
        """Test handling of malformed links."""
        text = "This has [[incomplete link and [[https://good.com][Good Link]]."
        links = extract_org_links(text)
        expected = [("https://good.com", "Good Link")]
        self.assertEqual(links, expected)
    
    def test_extract_org_links_empty_text(self):
        """Test link extraction with empty text."""
        self.assertEqual(extract_org_links(""), [])
        self.assertEqual(extract_org_links(None), [])


if __name__ == '__main__':
    unittest.main()
