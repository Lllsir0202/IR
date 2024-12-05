# Define Python
PYTHON = python3

# Define PageRank
PAGERANK = PageRank/pagerank.py

# Targets
# First write about make pagerank
.PHONY: pagerank

# make pagerank
pagerank:
	$(PYTHON) $(PAGERANK)
