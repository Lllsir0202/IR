import scrapy

class DocumentCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
