# Define Python
PYTHON = python3

# Define PageRank
PAGERANK = PageRank/pagerank.py

# Define Invert
INVERT = Inverted_Index/inverted_index.py

# Targets
# First write about make pagerank
# Second write about make inverted_index
.PHONY: pagerank invert

# make pagerank
pagerank:
	$(PYTHON) $(PAGERANK)

# make inverted_index
invert:
	$(PYTHON) $(INVERT)