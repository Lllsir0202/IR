from search import search, load_pagerank,load_tfidf_and_mapping_body,load_tfidf_and_mapping_title
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json
from flask_cors import CORS
import re


app = Flask(__name__)
CORS(app)  # 启用跨域支持



pagerank_file = 'data/pr_score/pagerankscore.json'
pageranks = load_pagerank(pagerank_file)

inputdir = "data/tfidf"

vectorizer_body = TfidfVectorizer()
vectorizer_title = TfidfVectorizer()

loaded_matrix_body, features_body, loaded_urls_body = load_tfidf_and_mapping_body(input_dir=inputdir)
vectorizer_body.fit(features_body)

loaded_matrix_title, features_title, loaded_urls_title = load_tfidf_and_mapping_title(input_dir=inputdir)
vectorizer_title.fit(features_title)


@app.route('/search', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('query')
        results_body = search(query, loaded_matrix_body, vectorizer_body, loaded_urls_body, pageranks, features_body)
        results = list(map(lambda x: x[0], results_body))
        results = sorted(results, key=lambda x: (x[1],-len(x[0])), reverse=True)
        results = results[:100]
        data_path = 'crawled_link_data'

        final_results = []


        for file_name in os.listdir(data_path):
            if file_name.endswith('json'):
                file_path = os.path.join(data_path, file_name)
                with open(file_path, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    url = data.get('url')
                    title = data.get('title','')
                    body = data.get('body', '')
                    if url in results:
                        cleaned_text = re.sub(r'\s+', ' ', body).strip()
                        text = cleaned_text[:30]
                        final_results.append(
                            {
                                'url':url,
                                'title':title,
                                'body':text
                            }
                        )
        
        return jsonify({'results': final_results})
    return jsonify({'results'}, results=None)

if __name__ == '__main__':
    app.run(debug=True)