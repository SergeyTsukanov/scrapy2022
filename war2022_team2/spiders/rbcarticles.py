import scrapy
from scrapy.http import Request
from war2022_team2.items import War2022Team2Item
import json
import hashlib

class RbcarticlesSpider(scrapy.Spider):
    name = 'rbcarticles'

    def start_requests(self):
        # Open the JSON file which contains article links
        data=[]
        with open('./rbclinks.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('URL: ' + link_url['link'])
            # Request to get the HTML content
            request = Request(link_url['link'],
                              cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022Team2Item()


         
        # Extracts the news_title and stores in scrapy item
        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        
        item['article_datetime'] = response.css('body > div.l-window.l-window-overflow-mob > \
             div.g-relative.g-clear > div.l-col-container > div.l-table > div.js-rbcslider > \
                 div > div.article.g-relative.js-rbcslider-article > div > div.l-col-main > \
                     div > div.article__header.js-article-header > div.article__header__info-block >\
                          span.article__header__date::text').get()

        item['article_title'] = response.css('body > div.l-window.l-window-overflow-mob > \
            div.g-relative.g-clear > div.l-col-container > div.l-table > div.js-rbcslider > \
                div > div.article.g-relative.js-rbcslider-article > div > div.l-col-main > \
                    div > div.article__header.js-article-header > div.article__header__title > h1::text').get()
         
        
            
        item['article_text'] = "".join(response.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/div[5]/div/div[1]/div//text()').getall())
        item['article_author'] =  response.css("body > div.l-window.l-window-overflow-mob > div.g-relative.g-clear > div.l-col-container > div.l-table > div.js-rbcslider > div:nth-child(1) > div.article.g-relative.js-rbcslider-article > div > div.l-col-main > div > div.article__authors > div > div.article__authors__author__wrap > span > span::text").get()
        if (not item['article_author']):
            item['article_author'] = "unknown"

        if("битк" in item['article_title'].lower() or "bitc" in item['article_title'].lower()):
            yield (item)
