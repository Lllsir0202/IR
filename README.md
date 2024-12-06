# IR
This is a simple web search engine

# System condition

    Ubuntu 23.04
    python 3.12.3
    packages:scrapy,BeautifulSoup,re,numpy,scipy and so on

## Spider

In directory ``document_crawler``, And you can use command ``scrapy crawl document_spider`` to start crawl , and you can change the start url to satify your requirements.

(Notice: because of my fault,I re-crawl my dataset,so if first crawl, you need to do some changes in ``document_crawler.py`` file)

## PageRank

In directory ``PageRank``, And I finish a Makefile to make it , you can use command ``make pagerank`` in the workspace(where the makefile is) to make pagerank of all jsons in directory ``crawled_link_data``, then the py will store the pagerankscore to directory ``pr_score`` automatically.

## Inverted_index

