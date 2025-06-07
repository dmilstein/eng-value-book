#!/bin/bash

# Script to convert org files to markdown using Emacs
# Usage: ./org-to-md.sh <input-file.org>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input-file.org>" >&2
    echo "Example: $0 /path/to/file.org" >&2
    exit 1
fi

INPUT_FILE="$1"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' does not exist" >&2
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run Emacs in batch mode to export org to markdown and output to stdout
emacs --batch \
      --load "$SCRIPT_DIR/emacs-batch-init.el" \
      --visit="$INPUT_FILE" \
      --eval "(progn
                (setq org-export-with-toc nil)
                (setq org-export-with-broken-links 'mark)
                (goto-char (point-min))
                (when (re-search-forward \"^\\* \" nil t)
                  (beginning-of-line)
                  (org-narrow-to-subtree))
                (princ (org-export-as 'gfm)))" \
      --kill
