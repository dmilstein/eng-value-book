#!/bin/bash

# Script to convert org files to markdown using Emacs
# Usage: ./org-to-md.sh <input-file.org>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input-file.org>"
    echo "Example: $0 /path/to/file.org"
    exit 1
fi

INPUT_FILE="$1"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' does not exist"
    exit 1
fi

# Get the directory and filename without extension
DIR=$(dirname "$INPUT_FILE")
BASENAME=$(basename "$INPUT_FILE" .org)
OUTPUT_FILE="$DIR/$BASENAME.md"

# Run Emacs in batch mode to export org to markdown
emacs --batch \
      --eval "(require 'ox-md)" \
      --visit="$INPUT_FILE" \
      --funcall org-md-export-to-markdown \
      --kill

echo "Converted '$INPUT_FILE' to '$OUTPUT_FILE'"
