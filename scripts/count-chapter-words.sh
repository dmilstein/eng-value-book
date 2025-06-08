#!/bin/bash

# Script to count words in each chapter and output totals
# Usage: ./count-chapter-words.sh

# Check if build/chapters.txt exists
if [ ! -f "build/chapters.txt" ]; then
    echo "Error: build/chapters.txt not found. Run 'make chapters' first." >&2
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract-first-heading.sh"

# Check if extract-first-heading.sh exists
if [ ! -f "$EXTRACT_SCRIPT" ]; then
    echo "Error: extract-first-heading.sh not found at $EXTRACT_SCRIPT" >&2
    exit 1
fi

total_words=0

# Read each chapter filename and process it
while IFS= read -r filename; do
    # Skip empty lines
    if [ -z "$filename" ]; then
        continue
    fi
    
    # Construct full path to org file
    org_file="org-roam-tibook/$filename"
    
    # Check if file exists
    if [ ! -f "$org_file" ]; then
        echo "Warning: File '$org_file' does not exist, skipping..." >&2
        continue
    fi
    
    # Extract first heading and count words
    word_count=$(cat "$org_file" | "$EXTRACT_SCRIPT" | wc -w)
    
    # Output tab-separated line
    echo -e "$word_count\t$filename"
    
    # Add to total
    total_words=$((total_words + word_count))
    
done < build/chapters.txt

# Output total
echo -e "$total_words\tTOTAL"
