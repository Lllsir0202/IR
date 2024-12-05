import scrapy
import os
import io
import json
import fitz  # PyMuPDF
from docx import Document
from document_crawler.items import DocumentCrawlerItem
from bs4 import BeautifulSoup

class DocumentSpider(scrapy.Spider):
    name = 'document_spider'
    allowed_domains = ['nankai.edu.cn']
    start_urls = ['https://news.nankai.edu.cn/']
    output_directory = '../crawled_data'  # 保存路径，使用绝对路径
    max_pages = 50000  # 设定最大抓取页面数量
    pages_crawled = 0  # 当前已抓取页面数量

    def __init__(self, *args, **kwargs):
        super(DocumentSpider, self).__init__(*args, **kwargs)
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def parse(self, response):
        """主页面解析方法"""
        if self.pages_crawled >= self.max_pages:  # 检查是否达到最大页面数
            self.logger.info(f"Reached max page count: {self.max_pages}")
            return  # 在这里停止爬取
        
        # 只有 HTML 页面才用 BeautifulSoup 解析
        if "text/html" in response.headers.get('Content-Type', '').decode():
            # 使用 BeautifulSoup 来解析 HTML 内容
            soup = BeautifulSoup(response.text, 'lxml')

            # 去除不需要的标签，例如广告、脚本、样式等
            for script in soup(["script", "style", "header", "footer", "nav"]):
                script.decompose()  # 删除这些标签

            # 提取正文内容
            body = soup.get_text(separator=' ', strip=True)

            # 进行文本清洗（去除多余的空格、换行符等）
            body = self.clean_text(body)

            # 创建 Item 并保存数据
            item = DocumentCrawlerItem()
            item['url'] = response.url
            item['title'] = response.css('title::text').get()
            item['body'] = body
            self.save_as_json(item)

            self.pages_crawled += 1  # 增加已抓取页面计数

            # 处理网页中的 PDF 和 DOCX 链接
            links = soup.find_all('a', href=True)
            for link in links:
                full_url = response.urljoin(link['href'])
                if full_url.endswith('.pdf'):
                    yield scrapy.Request(full_url, callback=self.handle_pdf)
                elif full_url.endswith('.docx'):
                    yield scrapy.Request(full_url, callback=self.handle_docx)
                elif full_url.startswith('http') and self.pages_crawled < self.max_pages:
                    yield scrapy.Request(full_url, callback=self.parse)  # 递归爬取

        else:
            # 如果是 PDF 或 DOCX 文件，则直接处理二进制内容
            if response.url.endswith('.pdf'):
                yield self.handle_pdf(response)
            elif response.url.endswith('.docx'):
                yield self.handle_docx(response)

    def handle_pdf(self, response):
        text = self.extract_pdf_text(response)
        item = DocumentCrawlerItem()
        item['url'] = response.url
        item['title'] = response.url.split('/')[-1]
        item['body'] = text
        self.save_as_json(item)

    def handle_docx(self, response):
        text = self.extract_docx_text(response)
        item = DocumentCrawlerItem()
        item['url'] = response.url
        item['title'] = response.url.split('/')[-1]
        item['body'] = text
        self.save_as_json(item)

    def extract_pdf_text(self, response):
        try:
            # 使用 PyMuPDF 读取 PDF 文件
            doc = fitz.open(stream=response.body, filetype="pdf")
            text = ''
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text("text")  # 获取文本内容
            return self.clean_text(text)
        except Exception as e:
            self.logger.error(f"Failed to extract PDF text from {response.url}: {str(e)}")
            return ''

    def extract_docx_text(self, response):
        try:
            # 使用 io.BytesIO 处理字节流
            doc = Document(io.BytesIO(response.body))  # 这里使用 BytesIO 处理字节流
            text = ''
            for para in doc.paragraphs:
                text += para.text + '\n'
            return self.clean_text(text)
        except Exception as e:
            self.logger.error(f"Failed to extract DOCX text from {response.url}: {str(e)}")
            return ''

    def clean_text(self, text):
        """清洗文本：去除换行符、空格及不需要的符号，包括乱码字符"""
        # 去除乱码字符（可以根据需要自定义）
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        text = ' '.join(text.split())  # 去除多余的空格
        return text

    def save_as_json(self, item):
        """将爬取的项存储为 JSON 文件"""
        filename = item['url'].split('/')[-1] + '.json'
        filepath = os.path.join(self.output_directory, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=4)
