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

# Store word counts for calculating 7-day average
word_counts=()
dates=()

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
            word_counts+=($word_count)
            dates+=($date_str)
        else
            echo -e "$date_str\t0"
            word_counts+=(0)
            dates+=($date_str)
        fi
    else
        # No commits on this date
        echo -e "$date_str\t0"
        word_counts+=(0)
        dates+=($date_str)
    fi
done

# Calculate 7-day average words per day (last 7 days) and write to separate file
if [ ${#word_counts[@]} -ge 7 ]; then
    # Get the most recent 7 word counts (first 7 elements since we're going backwards in time)
    recent_counts=(${word_counts[@]:0:7})
    
    # Calculate the difference between first and last day of the 7-day period
    if [ ${recent_counts[6]} -gt 0 ] && [ ${recent_counts[0]} -gt 0 ]; then
        total_words_added=$((${recent_counts[0]} - ${recent_counts[6]}))
        avg_words_per_day=$((total_words_added / 7))
        
        # Write the 7-day average to build directory
        echo "$avg_words_per_day" > build/7day-average.txt
    else
        echo "0" > build/7day-average.txt
    fi
else
    echo "0" > build/7day-average.txt
fi
