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

And It has a essential frontier page as ``index.html``, and it has capability of ``login in `` and ``login out ``. It remains ``login`` state until user decided to loginout. Also I add a ``visitor`` to store all unlogin history but it has some points to optimize. 

## Some details
In this part , I want to introduce some details of some points.

### Snapshots
I deal with snapshots as a ``cache``. When user ``click`` a page and we will store ``all of the resources of the page``, accordlying when your meet this page again, you can ``click`` the new botton ``View Snapshot`` to view the local resouces of the page, However in some cases, it may have some questions ^ - ^

## Projects
    Project/
    │
    ├── crawled_link_data/
    |       
    │
    ├── data/
    │
    ├── document_crawler/
    │
    ├── Inverted_Index/
    │
    ├── PageRank/
    |
    ├── Search/
    |       ├── templates/
    |       |           ├── Sanpshots/
    |       |           ├── index.html
    |       |           ├── search.svg
    |       |
    |       ├── search.py
    |       |
    |       ├── app.py    
    |
    ├── stopwords/
    |
    ├── test/
    |
    ├── Tf_idf/
    |
    ├── Userdata/
    |
    ├── Makefile
Follolwing are some simple introductions to the project directories.

``document_crawler`` is the ``scrapy`` project used for spider(just as its name).

``Inverted_index`` is used to build inverted index but we haven't use it at the full process.

``PageRank`` is used to set up ``link graph`` and calculate ``pagerank`` as well as store it into directory ``data/pr_score``.

``Search`` directory is the main py file of the ``Web Search Engine`` and it finishes the frontier and background as well as solve search from the dataset.

``stopwords`` stores some popular ``stopwords`` includeing:``baidu_stopwords``,``cn_stopwords``,``hit_stopwords`` and ``scu_stopwords`` from github [reposity](https://github.com/goto456/stopwords)

``test`` is a ``very`` small dataset of of the full dataset and I use it to test in some cases.(just to avoid very very... long time of waiting calculating)

``Tf_Idf`` is used to calculate ``tfidf`` weight and store it as ``npz`` as well as store ``features`` as ``text``.

``Userdata`` is used by the ability of ``user login`` and ``recommendation`` and so on personal capability. It stores all users' histories as ``json`` files.

``Makefile`` is just as I haven't intruduced previously, and I have given the ``command`` before. 