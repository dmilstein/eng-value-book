#!/bin/bash

# Script to count total words in the book by finding chapter files
# Usage: ./count-book-words.sh [directory]
# If no directory is provided, defaults to org-roam-tibook

# Set the directory to search (default to org-roam-tibook)
ORG_DIR="${1:-org-roam-tibook}"

# Check if directory exists
if [ ! -d "$ORG_DIR" ]; then
    echo "Error: Directory '$ORG_DIR' does not exist" >&2
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

# Find all org files in the specified directory that contain ':Chapter:'
for org_file in "$ORG_DIR"/*.org; do
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
