#!/bin/bash

# Watch script for clock hours - monitors todo org files and updates hour counts
# Usage: ./watch_hours.sh

TODO_FILE="../tib-todos.org"
TODO_ARCHIVE="../tib-todos.org_archive"
HOURS_SCRIPT="../scripts/parse-clock-hours.py"

# Check if required files exist
if [ ! -f "$TODO_FILE" ]; then
    echo "Error: File $TODO_FILE not found"
    exit 1
fi

if [ ! -f "$HOURS_SCRIPT" ]; then
    echo "Error: Hours script $HOURS_SCRIPT not found"
    exit 1
fi

# Check if fswatch is available (macOS)
if ! command -v fswatch &> /dev/null; then
    echo "Error: fswatch not found. Install with: brew install fswatch"
    exit 1
fi

echo "Watching $TODO_FILE and $TODO_ARCHIVE for changes..."
echo "Press Ctrl+C to stop"
echo "================================"

# Function to run hours parser and display results
run_hours_parser() {
    clear
    echo "Clock Hours Monitor"
    echo "=================="
    echo "Last updated: $(date)"
    echo ""

    # Run the hours parser
    cd "$(dirname "$0")" || exit 1
    python3 "$HOURS_SCRIPT" "$TODO_FILE" 2>/dev/null

    echo ""
    echo "Watching for changes in todo files..."
    echo "Press Ctrl+C to stop"
}

# Run initial parse
run_hours_parser

# Watch for changes in todo files (both main and archive)
# Create list of files to watch, including archive if it exists
WATCH_FILES="$TODO_FILE"
if [ -f "$TODO_ARCHIVE" ]; then
    WATCH_FILES="$WATCH_FILES $TODO_ARCHIVE"
fi

fswatch -o $WATCH_FILES | while read -r num; do
    run_hours_parser
done
