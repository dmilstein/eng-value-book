#!/bin/bash

# Watch script for book builder - monitors org files and updates word counts
# Usage: ./watch_book.sh

BOOK_DIR="org-roam-tibook"
BUILDER_SCRIPT="book-monitor/parsers/book_builder.py"

# Check if required directories exist
if [ ! -d "$BOOK_DIR" ]; then
    echo "Error: Directory $BOOK_DIR not found"
    exit 1
fi

if [ ! -f "$BUILDER_SCRIPT" ]; then
    echo "Error: Book builder script $BUILDER_SCRIPT not found"
    exit 1
fi

# Check if fswatch is available (macOS)
if ! command -v fswatch &> /dev/null; then
    echo "Error: fswatch not found. Install with: brew install fswatch"
    exit 1
fi

echo "Watching $BOOK_DIR for changes..."
echo "Press Ctrl+C to stop"
echo "================================"

# Function to run book builder and display results
run_builder() {
    clear
    echo "Book Word Count Monitor"
    echo "======================="
    echo "Last updated: $(date)"
    echo ""
    
    # Run the book builder
    cd "$(dirname "$0")" || exit 1
    python3 "$BUILDER_SCRIPT" "$BOOK_DIR" 2>/dev/null
    
    echo ""
    echo "Watching for changes in $BOOK_DIR..."
    echo "Press Ctrl+C to stop"
}

# Run initial build
run_builder

# Watch for changes in .org files
fswatch -o "$BOOK_DIR"/*.org | while read -r num; do
    run_builder
done
