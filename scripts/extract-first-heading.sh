#!/bin/bash

# Extract the first heading from an org-mode file and strip comment lines
# Usage: cat file.org | ./extract-first-heading.sh

awk '
/^\* / {
    if (found_first) {
        exit
    }
    found_first = 1
    print
    next
}
found_first {
    print
}
' | \

    # Strip out org comment lines
sed '/^#/d'
