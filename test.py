import os
import json
import jieba

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

json_dir = "crawled_link_data"
for file_name in os.listdir(json_dir):
        if file_name.endswith('json'):
            file_path = os.path.join(json_dir, file_name)
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                url = data.get('url')
                body = data.get('body')
                title = data.get('title')
                links = data.get('links')
                if url == "https://law.nankai.edu.cn":
                    print(f'url is {url}, title is {title}')
