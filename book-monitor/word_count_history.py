#!/usr/bin/env python3
"""
Script to count book words for the last commit of each of the last 14 days.
Python equivalent of scripts/word-count-history.sh
"""

import subprocess
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


def run_command(cmd, capture_output=True, check=False):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=capture_output, 
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        return e


def get_date_string(days_ago):
    """Get date string for N days ago in YYYY-MM-DD format."""
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime('%Y-%m-%d')


def get_last_commit_on_date(date_str):
    """Get the last commit hash for a specific date."""
    cmd = f'git log --since="{date_str} 00:00:00" --until="{date_str} 23:59:59" --format="%H" -n 1'
    result = run_command(cmd)
    
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


def count_words_at_commit(commit_hash):
    """Count words at a specific commit using the existing shell script."""
    # Change to parent directory to run the script from the correct location
    original_dir = os.getcwd()
    parent_dir = Path(__file__).parent.parent
    script_path = parent_dir / "scripts" / "count-words-at-commit.sh"
    
    if not script_path.exists():
        print(f"Error: count-words-at-commit.sh not found at {script_path}", file=sys.stderr)
        return None
    
    try:
        # Change to the parent directory (project root)
        os.chdir(parent_dir)
        
        cmd = f"./scripts/count-words-at-commit.sh {commit_hash}"
        result = run_command(cmd)
        
        if result.returncode == 0:
            # Extract just the number from "Word count at commit abc123: 1234"
            output = result.stdout.strip()
            if ": " in output:
                return int(output.split(": ")[-1])
        else:
            # Debug: print error output
            print(f"Error running count-words-at-commit.sh for {commit_hash}: {result.stderr}", file=sys.stderr)
    
    finally:
        # Always change back to original directory
        os.chdir(original_dir)
    
    return None


def calculate_7day_average(word_counts):
    """Calculate 7-day average words per day from word counts list."""
    if len(word_counts) < 7:
        return 0
    
    # Get the most recent 7 word counts (first 7 elements since we're going backwards in time)
    recent_counts = word_counts[:7]
    
    # Calculate the difference between first and last day of the 7-day period
    if recent_counts[6] > 0 and recent_counts[0] > 0:
        total_words_added = recent_counts[0] - recent_counts[6]
        avg_words_per_day = total_words_added // 7
        return avg_words_per_day
    
    return 0


def main():
    """Main function to generate word count history."""
    word_counts = []
    dates = []
    
    # Loop through the last 14 days
    for i in range(14):
        date_str = get_date_string(i)
        last_commit = get_last_commit_on_date(date_str)
        
        if last_commit:
            word_count = count_words_at_commit(last_commit)
            if word_count is not None:
                print(f"{date_str}\t{word_count}")
                word_counts.append(word_count)
                dates.append(date_str)
            else:
                print(f"{date_str}\t0")
                word_counts.append(0)
                dates.append(date_str)
        else:
            # No commits on this date
            print(f"{date_str}\t0")
            word_counts.append(0)
            dates.append(date_str)
    
    # Calculate 7-day average and write to separate file
    avg_words_per_day = calculate_7day_average(word_counts)
    
    # Ensure build directory exists
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Write the 7-day average to build directory
    with open(build_dir / "7day-average.txt", "w") as f:
        f.write(str(avg_words_per_day))


if __name__ == "__main__":
    main()
