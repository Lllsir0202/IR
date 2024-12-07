# IR
This is a simple web search engine

# System condition

    Ubuntu 24.04
    python 3.12.3
    packages:scrapy,BeautifulSoup,re,numpy,scipy and so on

## Spider

In directory ``document_crawler``, And you can use command ``scrapy crawl document_spider`` to start crawl , and you can change the start url to satify your requirements.

(Notice: because of my fault,I re-crawl my dataset,so if first crawl, you need to do some changes in ``document_crawler.py`` file)

## PageRank

In directory ``PageRank``, And I finish a Makefile to make it , you can use command ``make pagerank`` in the workspace(where the makefile is) to make pagerank of all jsons in directory ``crawled_link_data``, then the py will store the pagerankscore to directory ``pr_score`` automatically.

## Inverted_index

Although I do the part of inverted index , but in fact it seems not used in my tasks. Because I will use ``sklearn`` to finish the part of ``td-idf``

You can use command ``make invert`` to calculate all words of title and body into inverted index but be careful because its size is very huge

## Tf-Idf

In this part I will use ``sklearn`` to calculate it automatically.

You can use command ``make tfidf`` to call function to calculate it automatically, but because of the large quantities of jsons, it may take some time.(Also divide ``title`` and ``body``)

## Serach
In this part I also use ``sklearn`` to calculate the nearest file.

But differently with passed work, I divided ``title`` and ``body`` into different json, and it make it more accuate for search

You can use command ``make search`` to call the function to search , and following ,I will make a ``flask`` or so to make it more free to use. 

## App
In this part we want to use ``flask`` to make a page to search more efficiently for users.

You can use command ``make app`` to start the back side if you have finished all of the previous steps.