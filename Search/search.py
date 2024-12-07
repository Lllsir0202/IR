import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.sparse import load_npz
import pickle
import jieba
import re

# First we need to read all of the jsons
# Because of the quantities of jsons
# We need to read jsons by blocks
def load_stopwords(file_dir):
    # Load all stopwords
    stopwords = set()
    for file_name in os.listdir(file_dir):
        if file_name.endswith('txt'):
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "r", encoding='utf-8') as file:
                # Store all stopwords in set
                stopwords.update(file.read().splitlines())    
    # ret set
    return stopwords

# Then need a function to split
def segment_words(text):
    file_dir = "stopwords"
    stopwords = load_stopwords(file_dir=file_dir)
    words = jieba.lcut(text)
    filter_words = [word for word in words if word not in stopwords]
    return " ".join(filter_words)

# Use this function to solve questions of ? and *
def process_query(query, feature):
    result = []
    query = query.replace('*','.*')
    query = query.replace('?','.')
    for word in feature:
        if re.match(query,word):
            result.append(word)
    return " ".join(result)

# Load pagerank
def load_pagerank(pagerank_file):
    with open(pagerank_file, 'r', encoding='utf-8') as file:
        pagerank = json.load(file)
    return pagerank

# Load tfidf mapped to urls
def load_tfidf_and_mapping_body(input_dir):
    # Store npz
    tfidf_matrix = load_npz(os.path.join(input_dir, 'tfidf_matrix_body.npz'))
    # Store features
    feature_names = np.loadtxt(os.path.join(input_dir, 'features_body.txt'), dtype=str)
    # url -> tf-idf map
    with open(os.path.join(input_dir, 'urls_body.pkl'), 'rb') as f:
        urls = pickle.load(f)
    return tfidf_matrix, feature_names, urls

# Load tfidf mapped to urls
def load_tfidf_and_mapping_title(input_dir):
    # Store npz
    tfidf_matrix = load_npz(os.path.join(input_dir, 'tfidf_matrix_title.npz'))
    # Store features
    feature_names = np.loadtxt(os.path.join(input_dir, 'features_title.txt'), dtype=str)
    # url -> tf-idf map
    with open(os.path.join(input_dir, 'urls_title.pkl'), 'rb') as f:
        urls = pickle.load(f)
    return tfidf_matrix, feature_names, urls

# calculateTf-Idf vector of query
def compute_query_tfidf(query, vectorizer):
    query_tfidf = vectorizer.transform([query])  # Transform query into vector
    return query_tfidf

# calculate query results
def search(query, tfidf_matrix, vectorizer, urls, pageranks, features, alpha = 0.7, beta = 0.3):
    if '?' in query or '*' in query:
        query_list = process_query(query=query, feature=features)
    else:
        query_list = segment_words(query)
    query_tfidf = compute_query_tfidf(query_list, vectorizer)
    
    # calculate cos
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix)
    
    # get most relative file
    similar_indices = cosine_similarities.argsort().flatten()[::-1]
    

    N = len(urls)

    results = []
    for index in similar_indices:
        url = urls[index]
        pagerank = pageranks.get(url, 1 / N)
        if cosine_similarities[0,index] == 1:
            combined_score = 1
        elif cosine_similarities[0,index] == 0:
            combined_score = 0
        else:
            combined_score = cosine_similarities[0, index] * alpha + pagerank * beta
        if combined_score > 1e-6:
            results.append((url, combined_score))  # Store url and similarities
    results = sorted(results, key=lambda x: (x[1],-len(x[0])), reverse=True)

    return results

'''
query = input()


pagerank_file = 'data/pr_score/pagerankscore.json'
pageranks = load_pagerank(pagerank_file)

vectorizer = TfidfVectorizer()
inputdir = "data/tfidf"
loaded_matrix, features, loaded_urls = load_tfidf_and_mapping_body(input_dir=inputdir)
vectorizer.fit(features)

results = search(query, loaded_matrix, vectorizer, loaded_urls, pageranks, features)

for url, score in results[:10]:
    print(f"URL: {url}, Combined_score: {score}")'''