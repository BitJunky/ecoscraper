# Scraper to scrape outbound links from economotimes

import scrapy
from ecoscrap.items import EcoscrapItem

#Main scraper class
class ecoscraper(scrapy.Spider):
    name = 'ecoscraper'
    start_urls = ["http://econotimes.com/nature?page=%s"% page for page in range(1,2)]

    def parse(self, response):
        for item in self.get_articles(response):
            yield item

    #Funtion to get article title and url from pages and passing article to function below for domain extraction.
    def get_articles(self, response):
        article = EcoscrapItem()
        base_url = 'http://econotimes.com'
        
        #Get all articles from a single page
        articles_selector = response.css('div .articleList')

        #Process single article from articles
        for article_selctor in articles_selector:
            article_title = article_selctor.css('.title a::text').get()
            article_url = base_url + article_selctor.css('.title a::attr(href)').get()
            article = {}
            article['title'] = article_title
            article['url'] = article_url
            
            #Pass article to domain extracting function
            results = scrapy.Request(article_url, callback=self.get_domains)
            results.meta['item'] = article
            yield results

    #Domain extraction funtion. Extracts all outbount links from an article
    def get_domains(self, response):
        item = response.meta['item']
        #get domains
        item['domains'] = response.css('.viewArticle a::attr(href)').getall()
        yield item