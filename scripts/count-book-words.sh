#!/bin/bash

# Script to count total words in the book by finding chapter files
# Usage: ./count-book-words.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract-first-heading.sh"

# Check if extract-first-heading.sh exists
if [ ! -f "$EXTRACT_SCRIPT" ]; then
    echo "Error: extract-first-heading.sh not found at $EXTRACT_SCRIPT" >&2
    exit 1
fi

total_words=0

# Find all org files in org-roam-tibook that contain ':Chapter:'
for org_file in org-roam-tibook/*.org; do
    # Check if file exists and contains ':Chapter:'
    if [ -f "$org_file" ] && grep -q ':Chapter:' "$org_file"; then
        # Extract first heading and count words
        word_count=$(cat "$org_file" | "$EXTRACT_SCRIPT" | wc -w)
        
        # Add to total
        total_words=$((total_words + word_count))
    fi
done

# Output total
echo "$total_words"
