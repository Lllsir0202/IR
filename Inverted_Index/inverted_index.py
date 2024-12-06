import os
import jieba
import json
from collections import defaultdict

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
    filter_words = set(filter_words)
    return filter_words

# Using this function to get all jsons' body
# next should to load jsons and make index(used for body)
def build_body_invert_index(file_dir):
        bodyindex = defaultdict(list)
        cnt = 0
        for file_name in os.listdir(file_dir):
            if file_name.endswith('json'):
                file_path = os.path.join(file_dir, file_name)
                with open(file_path, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    body = data.get('body')
                    words = list(segment_words(body))
                    for word in words:
                        bodyindex[word].append(cnt)
                    print(f'Succeed to build {cnt}th inverted index of body')
                    cnt += 1
        return bodyindex

def build_title_invert_index(file_dir):
    titleindex = defaultdict(list)
    cnt = 0
    for file_name in os.listdir(file_dir):
        if file_name.endswith('json'):
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                title = data.get('title')
                if title:
                    words = segment_words(title)
                    for word in words:
                        titleindex[word].append(cnt)
                    print(f'Succeed to build {cnt}th inverted index of title')
                    cnt += 1
    return titleindex

def save_body_invert_index(index, output_dir):
    # Store body index into a json
    file_path = os.path.join(output_dir, "body_index.json")

    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(index, file, indent=4, ensure_ascii=False)

    print(f'Succeed to store body index into {file_path}')

def save_title_invert_index(index, output_dir):
    # Store body index into a json
    file_path = os.path.join(output_dir, "title_index.json")

    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(index, file, indent=4, ensure_ascii=False)

    print(f'Succeed to store title index into {file_path}')


inputpath = "crawled_link_data"
outputpath = "data/inv_index"

# bodyindex = build_body_invert_index(inputpath)
# save_body_invert_index(index=bodyindex, output_dir=outputpath)

titleindex = build_title_invert_index(inputpath)
save_title_invert_index(index=titleindex, output_dir=outputpath)
