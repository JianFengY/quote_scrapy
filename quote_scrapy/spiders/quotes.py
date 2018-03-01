# -*- coding: utf-8 -*-
import scrapy
from quote_scrapy.items import QuoteItem


# cmd运行scrapy gender quotes quotes.toscrape.com直接创建该文件

class QuotesSpider(scrapy.Spider):
    name = 'quotes'  # scrapy crawl quotes启动爬虫，名字对应
    # scrapy crawl quotes -o quotes.json保存结果为quotes.json也可以保存成其他格式如jl、csv、xml、pickle、marshal等
    # scrapy crawl quotes -o ftp://user:pass@ftp.example.com/path/quotes.csv也可以使用ftp
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # scrapy shell quotes.toscrape.com命令可以用于调试
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()  # 查找第一个文本
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()  # 查找所有文本，返回列表
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)  # 拼接完整URL
        yield scrapy.Request(url=url, callback=self.parse)
