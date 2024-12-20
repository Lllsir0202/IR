from search import search, load_pagerank,load_tfidf_and_mapping_body,load_tfidf_and_mapping_title
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json
from flask_cors import CORS
import re
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz , save_npz
import requests
from bs4 import BeautifulSoup

# Used for url as filename 
from urllib.parse import quote, unquote
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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

# Load user data
userdatapath = 'Userdata'
currentuser = 'visitor'
currentlog = []
# Remember history need to reorder
history = []


@app.route('/search', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('query')
        search_type = data.get('search_type', 'title')  # 获取搜索类型，默认按标题搜索
        

        if search_type == 'title':
            results, query_tfidf = search(query, loaded_matrix_title, vectorizer_title, loaded_urls_title, pageranks, features_title ,currentuser)
        else:  # 默认为按内容搜索
            results, query_tfidf = search(query, loaded_matrix_body, vectorizer_body, loaded_urls_body, pageranks, features_body, currentuser)

        filepath = currentuser + ".json"
        filename = os.path.join(userdatapath, filepath)
        with open(filename, "r",encoding='utf-8') as file:
            data = json.load(file)
            history = data.get('history')
            if query not in history:
                history.append(query)
            else:
                history.remove(query)
                history.append(query)
        with open(filename, "w", encoding='utf-8') as file:
            history = history[-20:]
            json.dump({"history":history},file, indent=4, ensure_ascii=False)


        results_dict = {url: score for url, score in results}
        results = list(map(lambda x: x[0], results))
        results = results[:100]

        data_path = 'crawled_link_data'
        final_results = []

        # Add snapshots
        snappath = "Search/templates/Snapshots"
        sendpath = "Snapshots"

        for file_name in os.listdir(data_path):
            if file_name.endswith('json'):
                file_path = os.path.join(data_path, file_name)
                with open(file_path, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    url = data.get('url')
                    title = data.get('title', '')
                    body = data.get('body', '')
                    if url in results:
                        if title and body:
                            cleaned_title = re.sub(r'\s+', ' ', title).strip()
                            cleaned_text = re.sub(r'\s+', ' ', body).strip()
                            text = cleaned_text[:100]  
                            title = cleaned_title
                        else:
                            text = body
                        encoded_url = url.replace(':', '').replace('/', '').replace('?','') # Encode url
                        urlpath = encoded_url
                        snapshot = os.path.join(snappath, urlpath)
                        path = os.path.join(sendpath,urlpath)
                        if os.path.exists(snapshot):
                            path = os.path.join(path, "index.html")
                            final_results.append({
                                'score': results_dict[url],
                                'url': url,
                                'title': title,
                                'body': text,
                                'snapshot':path
                            })
                        else:
                            final_results.append({
                                'score': results_dict[url],
                                'url': url,
                                'title': title,
                                'body': text,
                            })
        
        final_results = sorted(final_results, key=lambda x: (x['score'] ,-len(x['url'])), reverse=True)
        return jsonify({'results': final_results, 'history':history[-5:]})
    
    return jsonify({'results': None, 'history':None})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        # Get username and add log
        username = data.get('username')
        global currentuser
        currentuser = username
        filepath = username + ".json"
        filename = os.path.join(userdatapath, filepath)
        if not os.path.exists(filename):
            with open(filename, "w",encoding='utf-8') as file:
                json.dump({"history":[]}, file, indent=4, ensure_ascii=False)
                return jsonify({'history':[]})
        else:
            print(filename)
            with open(filename,"r",encoding='utf-8') as file:
                data = json.load(file)
                history = data.get('history','')
                if history:
                    history = history[-5:]
                            # Return history
                return jsonify({'history':history})

@app.route('/recommendations', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        if currentuser != 'visiter':
            filepath = currentuser + ".json"
            filename = os.path.join(userdatapath, filepath)
            if os.path.exists(filename):
                with open(filename,"r",encoding='utf-8') as file:
                    data = json.load(file)
                    query = data.get('history')
                    allquery = " ".join(query)
                vector = vectorizer_body.transform([allquery])
                # calculate cos
                cosine_similarities = cosine_similarity(vector, loaded_matrix_body)
        
                # get most relative file
                similar_indices = cosine_similarities.argsort().flatten()[::-1]

                N = len(loaded_urls_body)

                results = []
                for index in similar_indices:
                    url = loaded_urls_body[index]
                    pagerank = pageranks.get(url, 1 / N)
                    if cosine_similarities[0,index] == 1:
                        combined_score = 1
                    elif cosine_similarities[0,index] == 0:
                        combined_score = 0
                    else:
                        combined_score = cosine_similarities[0, index] * 0.7 + pagerank * 0.3
                    if combined_score > 1e-6:
                        results.append((url, combined_score))  # Store url and similarities
                results = sorted(results, key=lambda x: (x[1],-len(x[0])), reverse=True)
            
                results_dict = {url: score for url, score in results}
                results = list(map(lambda x: x[0], results))
                results = results[:100]

                data_path = 'crawled_link_data'
                final_results = []

                for file_name in os.listdir(data_path):
                    if file_name.endswith('json'):
                        file_path = os.path.join(data_path, file_name)
                        with open(file_path, "r", encoding='utf-8') as file:
                            data = json.load(file)
                            url = data.get('url')
                            title = data.get('title', '')
                            body = data.get('body', '')
                            if url in results:
                                if title and body:
                                    cleaned_title = re.sub(r'\s+', ' ', title).strip()
                                    cleaned_text = re.sub(r'\s+', ' ', body).strip()
                                    text = cleaned_text[:100]  
                                    title = cleaned_title
                                else:
                                    text = body
                                final_results.append({
                                    'score': results_dict[url],
                                    'url': url,
                                    'title': title,
                                    'body': text
                                })
                final_results = sorted(final_results, key=lambda x: (x['score'] ,-len(x['url'])), reverse=True)

                return jsonify({'recommend': final_results[:5]})
        return jsonify({'recommend':[]})

@app.route('/snapshot', methods=['GET', 'POST'])
def save_html_with_resources():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get('url', '')
        snappath = "Search/templates/Snapshots"
        encoded_url = url.replace(':', '').replace('/', '').replace('?','')
        save_dir = os.path.join(snappath, encoded_url)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

            # 下载 HTML
            response = requests.get(url)
            response.encoding = "utf-8"  # 手动指定编码
            html_content = response.text

            # 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 下载所有资源
            for tag in soup.find_all(['img', 'link', 'script']):
                src = tag.get('src') or tag.get('href')
                if src:
                    resource_url = requests.compat.urljoin(url, src)
                    resource_path = os.path.join(save_dir, os.path.basename(src))

                    # 下载资源
                    resource_data = requests.get(resource_url).content
                    with open(resource_path, 'wb') as f:
                        f.write(resource_data)

                    # 修改 HTML 中的路径
                    if tag.name == 'img':
                        tag['src'] = os.path.basename(src)
                    else:
                        tag['href'] = os.path.basename(src)

            # 保存修改后的 HTML
            with open(os.path.join(save_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(str(soup))

        return jsonify({'success': 'ok', 'snapshot_url': f'/snapshots/{encoded_url}/index.html'})


if __name__ == '__main__':
    app.run(debug=True)