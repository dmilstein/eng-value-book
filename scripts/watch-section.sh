#!/bin/bash
# watch-section.sh - Watch and export a specific org section to HTML

POINTER_FILE="current-edit.org"
BUILD_DIR="build"

# Create build directory if it doesn't exist
mkdir -p "$BUILD_DIR"

# Download CSS file if it doesn't exist
CSS_FILE="$BUILD_DIR/water.css"
if [ ! -f "$CSS_FILE" ]; then
    echo "Downloading CSS file for offline use..."
    curl -s "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css" -o "$CSS_FILE"
    if [ $? -eq 0 ]; then
        echo "CSS file downloaded successfully"
    else
        echo "Warning: Could not download CSS file, will use online version"
    fi
fi

# Function to extract file path and optional heading from simple format
parse_pointer_file() {
    if [ ! -f "$POINTER_FILE" ]; then
        echo "Error: Pointer file $POINTER_FILE not found"
        echo "Create it with: filename.org [Heading Name]"
        exit 1
    fi

    # Read first line and split on whitespace
    local line=$(head -1 "$POINTER_FILE")
    if [ -z "$line" ]; then
        echo "Error: Pointer file is empty"
        echo "Expected format: filename.org [Heading Name]"
        exit 1
    fi

    # Split into filename (first word) and heading (rest, optional)
    ORG_FILE=$(echo "$line" | cut -d' ' -f1)
    HEADING=$(echo "$line" | cut -d' ' -f2-)

    if [ -z "$ORG_FILE" ]; then
        echo "Error: Could not parse pointer file"
        echo "Expected format: filename.org [Heading Name]"
        exit 1
    fi

    # If heading is same as filename, then no heading was provided
    if [ "$HEADING" = "$ORG_FILE" ]; then
        HEADING=""
    fi

    # Expand tilde to home directory if present
    ORG_FILE="${ORG_FILE/#\~/$HOME}"

    # Generate output filename from org file basename
    local basename=$(basename "$ORG_FILE" .org)
    OUTPUT_FILE="$BUILD_DIR/${basename}.html"

    echo "Watching: $ORG_FILE"
    if [ -n "$HEADING" ]; then
        echo "Section: $HEADING"
    else
        echo "Mode: Full file"
    fi
    echo "Output: $OUTPUT_FILE"
    echo ""

    if [ ! -f "$ORG_FILE" ]; then
        echo "Error: Org file $ORG_FILE not found"
        exit 1
    fi
}

# Function to extract section and convert to HTML
export_section() {
    if [ -n "$HEADING" ]; then
        # Extract specific section
        awk -v heading="$HEADING" '
        BEGIN {
            in_section = 0
            level = 0
            found = 0
        }
        /^\*+ / {
            current_level = gsub(/\*/, "&")
            # Remove leading/trailing whitespace from heading for comparison
            line_heading = $0
            gsub(/^\*+ */, "", line_heading)
            gsub(/ *$/, "", line_heading)

            if (line_heading == heading && !found) {
                in_section = 1
                level = current_level
                found = 1
                print $0
            } else if (in_section && current_level <= level) {
                exit
            } else if (in_section) {
                print $0
            }
            next
        }
        in_section { print $0 }
        ' "$ORG_FILE" > /tmp/section.org

        if [ ! -s /tmp/section.org ]; then
            echo "Warning: No content found for heading '$HEADING'"
            echo "<h1>Section Not Found</h1><p>Could not find heading: $HEADING</p>" > "$OUTPUT_FILE"
            return
        fi
        
        local title="$HEADING"
    else
        # Use entire file
        cp "$ORG_FILE" /tmp/section.org
        local basename=$(basename "$ORG_FILE" .org)
        local title="$basename"
    fi

    # Convert to HTML with pandoc
    if [ -f "$CSS_FILE" ]; then
        # Use local CSS file if available
        pandoc -f org -t html \
            --standalone \
            --css="../build/water.css" \
            --title="$title" \
            /tmp/section.org -o "$OUTPUT_FILE"
    else
        # Fall back to online CSS
        pandoc -f org -t html \
            --standalone \
            --css="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css" \
            --title="$title" \
            /tmp/section.org -o "$OUTPUT_FILE"
    fi
    
    # Create/update symlink to preview.html
    local preview_link="$BUILD_DIR/preview.html"
    rm -f "$preview_link"
    ln -s "$(basename "$OUTPUT_FILE")" "$preview_link"
    
    if [ -n "$HEADING" ]; then
        printf "Exported section to %s at %s\n" "$OUTPUT_FILE" "$(date)"
    else
        printf "Exported full file to %s at %s\n" "$OUTPUT_FILE" "$(date)"
    fi
    
    rm -f /tmp/section.org
}

# Check if pandoc is available
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc not found. Install with: brew install pandoc"
    exit 1
fi

# Check if fswatch is available
if ! command -v fswatch &> /dev/null; then
    echo "Error: fswatch not found. Install with: brew install fswatch"
    exit 1
fi

# Parse the pointer file
parse_pointer_file

# Initial export
export_section

echo ""
echo "Watching for changes... Press Ctrl+C to stop"

# Watch for changes
fswatch -o "$ORG_FILE" | while read -r num; do
    export_section
done
