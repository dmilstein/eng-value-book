#!/usr/bin/env python3
"""
Parse org-mode CLOCK lines from tib-todos.org and sum hours by date.
Outputs a sorted list of dates and total hours clocked.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta

def create_hours_bar(hours: float, max_hours: float, width: int = 10) -> str:
    """Create a horizontal bar representation of hours using Unicode blocks.

    Args:
        hours: Current hours to display
        max_hours: Maximum hours for scaling
        width: Width of the bar in characters

    Returns:
        String representation of the bar chart
    """
    if max_hours == 0 or hours == 0:
        return ' ' * width

    # Calculate how many full blocks and partial block
    ratio = hours / max_hours
    filled_chars = ratio * width
    full_blocks = int(filled_chars)
    partial = filled_chars - full_blocks

    # Unicode block characters from full to empty
    blocks = ['█', '▉', '▊', '▋', '▌', '▍', '▎', '▏']

    # Build the bar
    bar = '█' * full_blocks

    # Add partial block if needed
    if partial > 0 and full_blocks < width:
        partial_index = int(partial * len(blocks))
        if partial_index >= len(blocks):
            partial_index = len(blocks) - 1
        bar += blocks[partial_index]
        full_blocks += 1

    # Fill remaining with spaces
    bar += ' ' * (width - full_blocks)

    return bar

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
        # Get date range from first to last date
        all_dates = sorted(hours_by_date.keys())
        start_date = datetime.strptime(all_dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(all_dates[-1], '%Y-%m-%d')
        
        # Find max hours for scaling bars
        max_daily_hours = max(hours_by_date.values()) if hours_by_date.values() else 0
        
        # Calculate weekly totals first to find max weekly hours
        weekly_totals = []
        current_date = start_date
        weekly_hours = 0.0
        week_start = None
        
        while current_date <= end_date:
            hours = hours_by_date.get(current_date.strftime('%Y-%m-%d'), 0.0)
            
            if current_date.weekday() == 0:  # Monday - start of week
                if week_start is not None:  # Save previous week total
                    weekly_totals.append(weekly_hours)
                week_start = current_date
                weekly_hours = hours
            else:
                weekly_hours += hours
            
            current_date += timedelta(days=1)
        
        # Save final week total
        if week_start is not None:
            weekly_totals.append(weekly_hours)
        
        max_weekly_hours = max(weekly_totals) if weekly_totals else 0
        
        print("Date       Hours")
        print("-" * 35)
        
        # Collect weekly data for summary section
        weekly_data = []
        
        # Generate all dates in range and output with hours and bars
        current_date = start_date
        weekly_hours = 0.0
        week_start = None
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            hours = hours_by_date.get(date_str, 0.0)
            
            if hours == 0.0:
                print(f"{date_str}       {' ' * 10}")
            else:
                hours_bar = create_hours_bar(hours, max_daily_hours, 10)
                print(f"{date_str}  {hours:4.1f} {hours_bar}")
            
            # Track weekly totals (Monday = 0, Sunday = 6)
            if current_date.weekday() == 0:  # Monday - start of week
                if week_start is not None:  # Save previous week data
                    week_end = current_date - timedelta(days=1)
                    weekly_data.append((week_start, week_end, weekly_hours))
                    print(f"Week {week_start.strftime('%m/%d')}-{week_end.strftime('%m/%d')}")
                    print()
                week_start = current_date
                weekly_hours = hours
            else:
                weekly_hours += hours
            
            current_date += timedelta(days=1)
        
        # Save final week data
        if week_start is not None:
            week_end = end_date
            weekly_data.append((week_start, week_end, weekly_hours))
            print(f"Week {week_start.strftime('%m/%d')}-{week_end.strftime('%m/%d')}")
            print()
        
        total_hours = sum(hours_by_date.values())
        print("-" * 35)
        print(f"Total      {total_hours:4.1f}")
        print()
        
        # Weekly summary section
        print("Weekly Summary")
        print("-" * 35)
        for week_start, week_end, weekly_hours in weekly_data:
            weekly_bar = create_hours_bar(weekly_hours, max_weekly_hours, 15)
            print(f"Week {week_start.strftime('%m/%d')}-{week_end.strftime('%m/%d')}  {weekly_hours:4.1f} {weekly_bar}")
        
        # Current week section (most recent week with daily breakdown)
        if weekly_data:
            print()
            print("Current Week")
            print("-" * 35)
            current_week_start, current_week_end, current_weekly_hours = weekly_data[-1]
            
            # Show each day of the current week
            current_date = current_week_start
            while current_date <= current_week_end:
                date_str = current_date.strftime('%Y-%m-%d')
                hours = hours_by_date.get(date_str, 0.0)
                
                if hours == 0.0:
                    print(f"{date_str}       {' ' * 10}")
                else:
                    hours_bar = create_hours_bar(hours, max_daily_hours, 10)
                    print(f"{date_str}  {hours:4.1f} {hours_bar}")
                
                current_date += timedelta(days=1)
            
            # Show weekly summary
            current_weekly_bar = create_hours_bar(current_weekly_hours, max_weekly_hours, 15)
            print(f"Week {current_week_start.strftime('%m/%d')}-{current_week_end.strftime('%m/%d')}  {current_weekly_hours:4.1f} {current_weekly_bar}")
    else:
        print("No CLOCK entries found")

if __name__ == '__main__':
    main()
