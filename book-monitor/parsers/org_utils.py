"""Utilities for parsing and processing org-mode files."""

import re
from typing import List, Tuple


def count_words(text: str) -> int:
    """
    Count words in text, excluding org-mode markup and directives.
    
    Args:
        text: The text content to count words in
        
    Returns:
        Number of words in the text
    """
    if not text:
        return 0
    
    # Remove org directives (lines starting with #+)
    text = re.sub(r'^#\+.*$', '', text, flags=re.MULTILINE)
    
    # Remove property drawers (everything between :PROPERTIES: and :END:)
    text = re.sub(r':PROPERTIES:.*?:END:', '', text, flags=re.DOTALL)
    
    # Remove tags (words starting with : at end of headings)
    text = re.sub(r'\s+:[a-zA-Z0-9_@#%:]+:\s*$', '', text, flags=re.MULTILINE)
    
    # Remove comments (lines starting with #)
    text = re.sub(r'^#[^+].*$', '', text, flags=re.MULTILINE)
    
    # Remove code blocks (everything between #+BEGIN_SRC and #+END_SRC)
    text = re.sub(r'#\+BEGIN_SRC.*?#\+END_SRC', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove example blocks (everything between #+BEGIN_EXAMPLE and #+END_EXAMPLE)
    text = re.sub(r'#\+BEGIN_EXAMPLE.*?#\+END_EXAMPLE', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove quote blocks (everything between #+BEGIN_QUOTE and #+END_QUOTE)
    text = re.sub(r'#\+BEGIN_QUOTE.*?#\+END_QUOTE', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Split into words and count
    words = text.split()
    return len(words)


def remove_org_markup(text: str) -> str:
    """
    Remove org-mode markup from text, leaving plain text.
    
    Args:
        text: The text with org markup
        
    Returns:
        Plain text with markup removed
    """
    if not text:
        return ""
    
    # Remove bold markup (*text*)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # Remove italic markup (/text/)
    text = re.sub(r'/([^/]+)/', r'\1', text)
    
    # Remove underline markup (_text_)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # Remove strikethrough markup (+text+)
    text = re.sub(r'\+([^+]+)\+', r'\1', text)
    
    # Remove code markup (~text~ and =text=)
    text = re.sub(r'[~=]([^~=]+)[~=]', r'\1', text)
    
    # Remove links but keep the description [[url][description]] -> description
    text = re.sub(r'\[\[[^\]]+\]\[([^\]]+)\]\]', r'\1', text)
    
    # Remove simple links [[url]] -> url
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    
    return text


def extract_org_links(text: str) -> List[Tuple[str, str]]:
    """
    Extract org-mode links from text.
    
    Args:
        text: The text to extract links from
        
    Returns:
        List of tuples (url, description) for each link found
    """
    if not text:
        return []
    
    links = []
    
    # Find links with description [[url][description]]
    pattern = r'\[\[([^\]]+)\]\[([^\]]+)\]\]'
    matches = re.findall(pattern, text)
    for url, description in matches:
        links.append((url, description))
    
    # Find simple links [[url]]
    pattern = r'\[\[([^\]]+)\]\]'
    # Only match if not already captured by the previous pattern
    simple_matches = re.findall(pattern, text)
    for url in simple_matches:
        # Check if this URL was already captured with a description
        already_found = any(existing_url == url for existing_url, _ in links)
        if not already_found:
            links.append((url, url))
    
    return links
