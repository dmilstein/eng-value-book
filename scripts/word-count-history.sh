#!/bin/bash

# Script to count book words for the last commit of each of the last 14 days
# Usage: ./word-count-history.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COUNT_AT_COMMIT_SCRIPT="$SCRIPT_DIR/count-words-at-commit.sh"

# Check if count-words-at-commit.sh exists
if [ ! -f "$COUNT_AT_COMMIT_SCRIPT" ]; then
    echo "Error: count-words-at-commit.sh not found at $COUNT_AT_COMMIT_SCRIPT" >&2
    exit 1
fi

# Loop through the last 14 days
for i in $(seq 0 13); do
    # Calculate the date (i days ago)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS date command
        date_str=$(date -v-${i}d +%Y-%m-%d)
    else
        # Linux date command
        date_str=$(date -d "${i} days ago" +%Y-%m-%d)
    fi

    # Find the last commit on that date
    # Use --until to get commits up to the end of that day
    # Use --since to get commits from the start of that day
    last_commit=$(git log --since="$date_str 00:00:00" --until="$date_str 23:59:59" --format="%H" -n 1 2>/dev/null)

    if [ -n "$last_commit" ]; then
        # Get word count for that commit
        word_count_output=$("$COUNT_AT_COMMIT_SCRIPT" "$last_commit" 2>/dev/null)

        if [ $? -eq 0 ]; then
            # Extract just the number from "Word count at commit abc123: 1234"
            word_count=$(echo "$word_count_output" | sed 's/.*: //')
            echo -e "$date_str\t$word_count"
        else
            echo -e "0\t$date_str"
        fi
    else
        # No commits on this date
        echo -e "$date_str\t0"
    fi
done
