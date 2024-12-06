'''This py file is used to establish PageRank values'''
'''Because of the jsons crawled I haven't extract URL within CONTEXT,so first need to extract url link in context'''

import os
import json
from collections import defaultdict
import numpy as np
from scipy.sparse import csr_matrix,lil_matrix
from scipy.linalg import norm
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # import urljoin to deal with relative path
from urllib.parse import urlparse  # import urlparse to deal with relative path


# we need to get the url one by one and build a link grpah
def get_link_graph(json_dir):
    # using defaultdict to store graph
    link_graph = defaultdict(list)
    cnt = 0

    for file_name in os.listdir(json_dir):
        if file_name.endswith('json'):
            file_path = os.path.join(json_dir, file_name)
            with open(file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                url = data.get('url')
                links = data.get('links')
                cnt = cnt + 1

                # if url exists , then store links
                if url and links:
                    link_graph[url] = list(set(links))
                    print(f'Succeed to deal with the {cnt}th json \n')

    print(f'Finish Successfully! The linkgraph size is {len(link_graph)} \n')
    return link_graph

# Then We should calculate pagerank
def cal_pagerank(link_graph, d = 0.85, max_iter = 100, tol = 1e-6):
    # First we need to convert graph to numpy
    # Get urls
    nodes = list(link_graph.keys())
    # Get idx by urls
    node2idx = {node: idx for idx, node in enumerate(nodes)}
    
    # Get total urls 
    N = len(nodes)
    
    # Use csr_matrix to store
    row = []
    col = []
    for node, links in link_graph.items():
        for link in links:
            if link in node2idx:
                print(f'Succeed to deal link {link}\n')
                row.append(node2idx[link])
                col.append(node2idx[node])
    
    datas = np.ones(len(row))
    sparse_matrix = csr_matrix((datas, (row,col)), shape=(N, N))
    
    # cal out degree
    out_degree = sparse_matrix.sum(axis=0).A1
    
    # 创建一个对角矩阵用于归一化
    normalization_matrix = lil_matrix((N, N))
    for i in range(N):
        print(f'Succeed to deal {i} th out_degree\n') 
        if out_degree[i] > 0:
            normalization_matrix[i, i] = 1 / out_degree[i]
        else:
            normalization_matrix[i, i] = 1 / N

    # 归一化稀疏矩阵
    sparse_matrix = sparse_matrix @ normalization_matrix


    # Initialize pagerank
    pagerank = np.ones(N) / N
    
    M = sparse_matrix
    
    for i in range(max_iter):
        new_pagerank = d * pagerank @ M  + (1 - d) / N
        print(f'Succeed to iter circles {i} / {max_iter} \n')
        if norm(new_pagerank - pagerank, 1) < tol:
            print(f'Finish cal iter\n')
            print(f'Start to save pagescore...')
            break
        
    pagerankscore = {nodes[i]: pagerank[i] for i in range(N)}
    return pagerankscore
    


# This function is used to save the result of pagerank
# Just input the dir
def save_pagerank(output_dir, pagerank_score):
    file_path = os.path.join(output_dir, "pagerankscore.json")
    
    with open(file_path,"w", encoding='utf-8') as file:
        json.dump(pagerank_score, file, indent=4, ensure_ascii=False)
    print(f'Succeed to save pagerank score as json in {file_path}\n')

# Start to cal
# Change: use new data
file_dir = "crawled_link_data"
link_graph = get_link_graph(file_dir)
pagerankscore = cal_pagerank(link_graph=link_graph)

store_path = "pr_score"
save_pagerank(output_dir=store_path, pagerank_score=pagerankscore)
for key, value in list(link_graph.items())[:10]:  # 打印前10个节点
    print(f"{key} -> {value}")