#!/bin/bash

# Script to convert multiple org files to markdown and concatenate them
# Usage: echo "file1.org\nfile2.org" | ./concat-org-to-md.sh
# Or: cat filelist.txt | ./concat-org-to-md.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORG_TO_MD_SCRIPT="$SCRIPT_DIR/org-to-md.sh"

# Check if org-to-md.sh exists
if [ ! -f "$ORG_TO_MD_SCRIPT" ]; then
    echo "Error: org-to-md.sh script not found at $ORG_TO_MD_SCRIPT" >&2
    exit 1
fi

# Read filenames from stdin and process each one
while IFS= read -r filename; do
    # Skip empty lines
    if [ -z "$filename" ]; then
        continue
    fi
    
    # Check if file exists
    if [ ! -f "$filename" ]; then
        echo "Warning: File '$filename' does not exist, skipping..." >&2
        continue
    fi
    
    # Convert to markdown and output to stdout
    "$ORG_TO_MD_SCRIPT" "$filename"
    
    # Add a blank line between chapters for readability
    echo
done
