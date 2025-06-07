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

# First stage: generate chapters list and markdown dependencies
build/book.deps: build/chapters.txt
	@sed 's/\.org$$/.md/' $< | sed 's|^|build/|' > $@

# Second stage: include the dependencies and build the book
-include build/book.deps
build/book.md: build/chapters.txt $(shell if [ -f build/book.deps ]; then cat build/book.deps; fi)
	@echo "Building complete book..."
	@> $@
	@while IFS= read -r chapter; do \
		chapter_md="build/$$(basename "$$chapter" .org).md"; \
		cat "$$chapter_md" >> $@; \
		echo "" >> $@; \
	done < $<

# Alias for convenience
book: build/book.md

# Clean build artifacts
clean:
	rm -rf build
