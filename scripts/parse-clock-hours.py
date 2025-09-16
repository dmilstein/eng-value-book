#!/usr/bin/env python3
"""
Parse org-mode CLOCK lines from tib-todos.org and sum hours by date.
Outputs a sorted list of dates and total hours clocked.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime

def parse_clock_line(line):
    """
    Parse a CLOCK line and return (date, hours) or None if invalid.
    Expected format: CLOCK: [2025-09-14 Sun 09:19]--[2025-09-14 Sun 11:16] =>  1:57
    """
    # Match CLOCK lines with start and end times
    pattern = r'CLOCK:\s*\[(\d{4}-\d{2}-\d{2})\s+\w+\s+\d{2}:\d{2}\]--\[(\d{4}-\d{2}-\d{2})\s+\w+\s+\d{2}:\d{2}\]\s*=>\s*(\d+):(\d{2})'
    match = re.search(pattern, line)
    
    if match:
        start_date = match.group(1)
        end_date = match.group(2)
        hours = int(match.group(3))
        minutes = int(match.group(4))
        
        # Convert to decimal hours
        total_hours = hours + minutes / 60.0
        
        # Use start date for the entry
        return start_date, total_hours
    
    return None

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'tib-todos.org'
    
    # Dictionary to sum hours by date
    hours_by_date = defaultdict(float)
    
    # List of files to process
    files_to_process = [filename]
    
    # Add archive file if it exists
    archive_filename = filename + '_archive'
    try:
        with open(archive_filename, 'r', encoding='utf-8'):
            files_to_process.append(archive_filename)
    except FileNotFoundError:
        pass  # Archive file doesn't exist, that's okay
    
    # Process each file
    for current_file in files_to_process:
        try:
            with open(current_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if 'CLOCK:' in line:
                        result = parse_clock_line(line)
                        if result:
                            date, hours = result
                            hours_by_date[date] += hours
                        else:
                            print(f"Warning: Could not parse CLOCK line {line_num} in {current_file}: {line}", file=sys.stderr)
        
        except FileNotFoundError:
            if current_file == filename:
                print(f"Error: File '{current_file}' not found", file=sys.stderr)
                sys.exit(1)
            # Archive file not found is okay, we already checked for it
        except Exception as e:
            print(f"Error reading file {current_file}: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Sort by date and output
    if hours_by_date:
        print("Date       Hours")
        print("-" * 15)
        for date in sorted(hours_by_date.keys()):
            hours = hours_by_date[date]
            print(f"{date}  {hours:5.2f}")
        
        total_hours = sum(hours_by_date.values())
        print("-" * 15)
        print(f"Total      {total_hours:5.2f}")
    else:
        print("No CLOCK entries found")

if __name__ == '__main__':
    main()
