# Makefile for building book artifacts

.PHONY: all clean chapters book

# Default target
all: build/book.md

# Create build directory if it doesn't exist
build:
	mkdir -p build

# Generate chapters.txt from TOC
build/chapters.txt: build org-roam-tibook/toc.org
	cd book-monitor && python parsers/toc_parser.py ../org-roam-tibook/toc.org > ../build/chapters.txt

# Alias for convenience
chapters: build/chapters.txt

# Pattern target to build markdown for a single chapter
# Usage: make build/chapter-name.md (where chapter-name.org exists in org-roam-tibook/)
build/%.md: org-roam-tibook/%.org build
	./scripts/org-to-md.sh $< > $@

# Build the complete book by concatenating all chapters in order
build/book.md: build/chapters.txt
	@echo "Building complete book..."
	@> $@  # Clear the output file
	@while IFS= read -r chapter; do \
		echo "Adding chapter: $$chapter" >&2; \
		chapter_md="build/$$(basename "$$chapter" .org).md"; \
		$(MAKE) "$$chapter_md"; \
		cat "$$chapter_md" >> $@; \
		echo "" >> $@; \
	done < $<

# Alias for convenience
book: build/book.md

# Clean build artifacts
clean:
	rm -rf build
