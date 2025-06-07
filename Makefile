# Makefile for building book artifacts

.PHONY: all clean chapters

# Default target
all: build/chapters.txt

# Create build directory if it doesn't exist
build:
	mkdir -p build

# Generate chapters.txt from TOC
build/chapters.txt: build org-roam-tibook/toc.org
	cd book-monitor && python parsers/toc_parser.py ../org-roam-tibook/toc.org > ../build/chapters.txt

# Alias for convenience
chapters: build/chapters.txt

# Clean build artifacts
clean:
	rm -rf build
