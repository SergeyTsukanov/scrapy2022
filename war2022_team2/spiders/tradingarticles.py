import scrapy
from scrapy.http import Request
from war2022_team2.items import War2022Team2Item
import json
import hashlib

class TradingSpider(scrapy.Spider):
    name = 'tradingviewarticle'

    def start_requests(self):
        # Open the JSON file which contains article links
        data=[]
        with open('./tradingviewlinks.json') as json_file:
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

        news_body = ""
        # Extracts the news_title and stores in scrapy item
        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_datetime'] = response.css('body > div.tv-main > div.tv-content > div > div >\
             div:nth-child(1) > div.tv-chart-view__header > div.tv-chart-view__title.selectable >\
                  div > div.tv-chart-view__title-row.tv-chart-view__title-row--user >\
                       span.tv-chart-view__title-time::text').extract_first()

        item['article_title'] = response.css('body > div.tv-main > div.tv-content > div > div >\
             div:nth-child(1) > div.tv-chart-view__header > div.tv-chart-view__title.selectable >\
                  div > div.tv-chart-view__title-row.tv-chart-view__title-row--name > div > h1::text').extract_first()
            
        item['article_text'] = "".join(response.xpath('/html/body/div[2]/div[4]/div/div/div[1]/div[6]//text()').getall())
        item['article_author'] =  response.css("body > div.tv-main > div.tv-content > div > div >\
             div:nth-child(1) > div.tv-chart-view__header > div.tv-chart-view__title.selectable > div >\
                  div.tv-chart-view__title-row.tv-chart-view__title-row--user >\
                       span.tv-chart-view__title-user-link > a.tv-user-link__wrap.tv-chart-view__title-user-name-wrap.js-userlink-popup > span::text").get()
        
        yield (item)
