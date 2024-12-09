# Define Python
PYTHON = python3

# Define PageRank
PAGERANK = PageRank/pagerank.py

# Define Invert
INVERT = Inverted_Index/inverted_index.py

# Define Tf-Idf
TFIDF = Tf_Idf/tf_idf.py

# Define Search
SEARCH = Search/search.py

# Define App
APP = Search/app.py

# Targets
# First write about make pagerank
# Second write about make inverted_index
# Third write about make tf_idf
.PHONY: pagerank invert tfidf search app

all: app

# make pagerank
pagerank:
	$(PYTHON) $(PAGERANK)

# make inverted_index
invert:
	$(PYTHON) $(INVERT)

# make tf_idf
tfidf:
	$(PYTHON) $(TFIDF)

# make search
search:
	$(PYTHON) $(SEARCH)

# make app
app:
	$(PYTHON) $(APP)