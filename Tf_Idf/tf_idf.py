import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import numpy as np
from scipy.sparse import save_npz
import pickle

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
    return filter_words

# Then load the url and the text
# This is for body
def load_body(file_dir):
    texts = []
    doc_ids = []
    for file_name in os.listdir(file_dir):
        if file_name.endswith('json'):
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                body = data.get('body')
                url = data.get('url')
                if body:
                    texts.extend(segment_words(body))
                doc_ids.append(url)
                print(f'Succeed to load body of {url}...')
    return doc_ids, texts

# This is for title
def load_title(file_dir):
    texts = []
    doc_ids = []
    for file_name in os.listdir(file_dir):
        if file_name.endswith('json'):
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                title = data.get('title','')
                url = data.get('url')
                if title:
                    texts.extend(segment_words(title))
                doc_ids.append(url)
                print(f'Succeed to load title of {url}...')
    return doc_ids, texts

# Next we need to calculate the Tf-Idf
def compute_tfidf(documents):
    """
    Compute TF-IDF for the given documents.
    """
    vectorizer = TfidfVectorizer()  # Use custom stopwords
    tfidf_matrix = vectorizer.fit_transform(documents)  # Compute TF-IDF
    feature_names = vectorizer.get_feature_names_out()  # Get the terms (vocabulary)
    print("Succeed to compute tf-idf...")
    return tfidf_matrix, feature_names

# Store tfidf mapped to urls
def save_tfidf_and_mapping_body(tfidf_matrix, feature_names, urls, output_dir):
    # Store npz
    save_npz(os.path.join(output_dir, 'tfidf_matrix_body.npz'), tfidf_matrix)
    # Store features
    np.savetxt(os.path.join(output_dir, 'features_body.txt'), feature_names, delimiter="\n", fmt="%s")
    # url -> tf-idf map
    with open(os.path.join(output_dir, 'urls_body.pkl'), 'wb') as f:
        pickle.dump(urls, f)

# Store tfidf mapped to urls
def save_tfidf_and_mapping_title(tfidf_matrix, feature_names, urls, output_dir):
    # Store npz
    save_npz(os.path.join(output_dir, 'tfidf_matrix_title.npz'), tfidf_matrix)
    # Store features
    np.savetxt(os.path.join(output_dir, 'features_title.txt'), feature_names, delimiter="\n", fmt="%s")
    # url -> tf-idf map
    with open(os.path.join(output_dir, 'urls_title.pkl'), 'wb') as f:
        pickle.dump(urls, f)


file_dir = 'crawled_link_data'
output_dir = 'data/tfidf'

# Get documents and urls
urls, documents = load_body(file_dir)

# calculate tf-idf
tfidf_matrix, feature_names = compute_tfidf(documents)

# Store tfidf mapped to urls
save_tfidf_and_mapping_body(tfidf_matrix, feature_names, urls, output_dir)

# Get documents and urls
urls, documents = load_title(file_dir)

# calculate tf-idf
tfidf_matrix, feature_names = compute_tfidf(documents)

# Store tfidf mapped to urls
save_tfidf_and_mapping_title(tfidf_matrix, feature_names, urls, output_dir)