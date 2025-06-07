#!/bin/bash

# Script to convert multiple org files to markdown and concatenate them
# Usage: echo "file1.org\nfile2.org" | ./concat-org-to-md.sh <directory>
# Or: cat filelist.txt | ./concat-org-to-md.sh <directory>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>" >&2
    echo "Example: cat filelist.txt | $0 /path/to/org/files" >&2
    exit 1
fi

DIRECTORY="$1"

# Check if directory exists
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: Directory '$DIRECTORY' does not exist" >&2
    exit 1
fi

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
    
    # Construct full path
    full_path="$DIRECTORY/$filename"
    
    # Check if file exists
    if [ ! -f "$full_path" ]; then
        echo "Warning: File '$full_path' does not exist, skipping..." >&2
        continue
    fi
    
    # Log which file we're processing
    echo "Converting: $full_path" >&2
    
    # Convert to markdown and output to stdout
    "$ORG_TO_MD_SCRIPT" "$full_path"
    
    # Add a blank line between chapters for readability
    echo
done
