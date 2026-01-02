#!/usr/bin/env python3
"""
Split the Offer Tactic Stories file into individual chapter files.
"""

import os
import re
import sys

def snake_case(text):
    """Convert text to snake_case filename."""
    # Remove org markup and clean up
    text = re.sub(r'\*+\s*', '', text)  # Remove asterisks
    text = re.sub(r'[^\w\s-]', '', text)  # Remove special chars except hyphens
    text = re.sub(r'\s+', '_', text.strip())  # Replace spaces with underscores
    return text.lower()

def split_offer_tactics():
    """Split the Offer Tactic Stories file into individual files."""
    
    input_file = "org-roam-tibook/20251229092547-offer_tactic_stories.org"
    output_dir = "org-roam-tibook/generated-chapters"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return False
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into sections by ** headings
    sections = []
    current_section = []
    lines = content.split('\n')
    
    # Skip until we find the first ** heading
    in_content = False
    
    for line in lines:
        if line.startswith('** '):
            if current_section and in_content:
                sections.append('\n'.join(current_section))
            current_section = [line]
            in_content = True
        elif in_content:
            current_section.append(line)
    
    # Add the last section
    if current_section and in_content:
        sections.append('\n'.join(current_section))
    
    generated_files = []
    
    for section in sections:
        lines = section.split('\n')
        if not lines or not lines[0].startswith('** '):
            continue
            
        # Extract title from first line
        title = lines[0][3:].strip()  # Remove '** '
        filename = snake_case(title) + '.org'
        filepath = os.path.join(output_dir, filename)
        
        # Convert ** to * for the new file
        section_content = section.replace('** ' + title, '* ' + title, 1)
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(section_content)
        
        generated_files.append((filename, title))
        print(f"Created: {filepath}")
    
    return generated_files

def update_toc(generated_files):
    """Update toc.org to replace the Offer Tactic Stories link with individual links."""
    
    toc_file = "org-roam-tibook/toc.org"
    
    with open(toc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the Offer Tactic Stories link
    old_link_pattern = r'\[\[id:EE70A408-E4BA-4E74-9788-D8EE6DF5E9BE\]\[Offer Tactic Stories\]\]'
    
    # Create new links
    new_links = []
    for filename, title in generated_files:
        new_links.append(f'** [[file:generated-chapters/{filename}][{title}]]')
    
    new_content = '\n'.join(new_links)
    
    # Replace the old link
    updated_content = re.sub(old_link_pattern, new_content, content)
    
    # Write back to file
    with open(toc_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {toc_file} with {len(generated_files)} new links")

def main():
    """Main function."""
    print("Splitting Offer Tactic Stories into individual files...")
    
    generated_files = split_offer_tactics()
    if not generated_files:
        print("No files generated")
        return 1
    
    print(f"\nGenerated {len(generated_files)} files:")
    for filename, title in generated_files:
        print(f"  - {filename}: {title}")
    
    print("\nUpdating toc.org...")
    update_toc(generated_files)
    
    print("\nDone!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
