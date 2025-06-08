#!/usr/bin/gnuplot

# Gnuplot script to generate a word count history graph
# Usage: ./scripts/word-count-history.sh | gnuplot scripts/plot-word-history.gnuplot

# Set terminal and output
set terminal png size 800,600
set output 'build/word-count-history.png'

# Configure the plot
set title "Book Word Count History (Last 14 Days)"
set xlabel "Date"
set ylabel "Word Count"

# Configure x-axis for dates
set xdata time
set timefmt "%Y-%m-%d"
set format x "%m/%d"
set xtics rotate by -45

# Configure grid and style
set grid
set style data linespoints
set pointtype 7
set pointsize 1.5

# Plot the data from stdin
plot '-' using 2:1 with linespoints linewidth 2 title "Word Count"
