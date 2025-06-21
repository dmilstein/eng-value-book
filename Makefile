# Makefile for building book artifacts

.PHONY: all clean chapters book

# Default target
all: build/book.md

# Create build directory if it doesn't exist
build:
	mkdir -p build

# Generate chapters.txt from TOC
build/chapters.txt: org-roam-tibook/toc.org
	cd book-monitor && python parsers/toc_parser.py ../org-roam-tibook/toc.org > ../build/chapters.txt

# Alias for convenience
chapters: build/chapters.txt

# Pattern target to build markdown for a single chapter
# Usage: make build/chapter-name.md (where chapter-name.org exists in org-roam-tibook/)
build/%.md: org-roam-tibook/%.org
	pandoc --from=org --to=gfm $< > $@

# First stage: generate chapters list and markdown dependencies
build/book.deps: build/chapters.txt
	@echo "CHAPTER_MDS = \\" > $@
	@sed 's/\.org$$/.md/' $< | sed 's|^|build/|' | sed 's/$$/ \\/' | grep -v "None" >> $@
	@echo "" >> $@

# Second stage: include the dependencies and build the book
-include build/book.deps
#build/book.md: $(CHAPTER_MDS)
build/book.md: build/book.deps
	@echo "Building complete book..."
	@> $@
	@while IFS= read -r chapter; do \
		chapter_md="build/$$(basename "$$chapter" .org).md"; \
		$(MAKE) "$$chapter_md"; \
		cat "$$chapter_md" >> $@; \
		echo "" >> $@; \
	done < build/chapters.txt

# Alias for convenience
book: build/book.md

# Generate word count history data and averages (both created by same script)
build/word-count-data.txt build/word-averages.txt: $(CHAPTER_MDS)
	cd book-monitor && python word_count_history.py > ../build/word-count-data.txt

# Generate word count history graph
build/word-count-history.png: build/word-count-data.txt build/word-averages.txt
	gnuplot scripts/plot-word-history.gnuplot

# Alias for convenience
word-count-graph: build/word-count-history.png

# Clean build artifacts
clean:
	rm -rf build
