#!/bin/bash

# Script to count book words at a specific git commit using git archive
# Usage: ./count-words-at-commit.sh <commit-hash>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <commit-hash>" >&2
    echo "Example: $0 abc1234" >&2
    exit 1
fi

COMMIT="$1"

# Check if the commit exists
if ! git rev-parse --verify "$COMMIT" >/dev/null 2>&1; then
    echo "Error: Commit '$COMMIT' not found" >&2
    exit 1
fi

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
ORG_DIR="$TEMP_DIR/org-roam-tibook"

# Function to cleanup
cleanup() {
    rm -rf "$TEMP_DIR"
}

# Set up trap to cleanup on exit
trap cleanup EXIT

# Extract org-roam-tibook directory from the specified commit
if ! git archive "$COMMIT" org-roam-tibook | tar -x -C "$TEMP_DIR" 2>/dev/null; then
    echo "Error: Failed to extract org-roam-tibook from commit '$COMMIT'" >&2
    echo "This might be because the org-roam-tibook directory doesn't exist at that commit" >&2
    exit 1
fi

# Check if any org files were extracted
if [ ! -d "$ORG_DIR" ] || [ -z "$(ls -A "$ORG_DIR"/*.org 2>/dev/null)" ]; then
    echo "Error: No org files found in org-roam-tibook at commit '$COMMIT'" >&2
    exit 1
fi

# Run the word count script with the extracted directory
word_count=$(./scripts/count-book-words.sh "$ORG_DIR" 2>/dev/null)

# Check if the script ran successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to count words at commit '$COMMIT'" >&2
    exit 1
fi

# Output the result
echo "Word count at commit $COMMIT: $word_count"
