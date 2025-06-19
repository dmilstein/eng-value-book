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
set autoscale x
set format x "%m/%d"
set xtics rotate by -45

# Configure grid and style
set grid
set style data linespoints
#set pointtype 7
#set pointsize 1.5

# Read averages from file
avg_7day = system("grep '7day:' build/word-averages.txt | cut -d' ' -f2")
avg_14day = system("grep '14day:' build/word-averages.txt | cut -d' ' -f2")

# Add labels showing averages
set label sprintf("7-day avg:  %4s words/day", avg_7day) at graph 0.02, graph 0.95 font "monospace,12" tc rgb "black"
set label sprintf("14-day avg: %4s words/day", avg_14day) at graph 0.02, graph 0.90 font "monospace,12" tc rgb "black"

# Plot the data from file
plot "build/word-count-data.txt" using 1:2 with linespoints linewidth 2 title "Word Count"
