import scrapy
from scrapy.http import Request
from war2022_team2.items import War2022Team2Item
import json
import hashlib

class UraarticlesSpider(scrapy.Spider):
    name = 'forklogarticles'

    def start_requests(self):
        # Open the JSON file which contains article links
        data=[]
        with open('./forkloglinks.json') as json_file:
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
        item['article_datetime'] = response.css('body > main > div:nth-child(1) > \
             div.post_content > div.article_meta > span::text').extract_first()
        item['article_title'] = response.css('body > main > div:nth-child(1) > \
            div.post_content > h1::text').extract_first()
         
        article_text = "" 
        for paragraph in response.css('body > main > div:nth-child(1) > div.post_content > p'):
            article_text+=paragraph.css("::text").get()
            
        item['article_text'] = article_text 
        item['article_author'] =  response.css("body > main > div:nth-child(1) > \
            div.post_content > div.article_meta > a::text").get()
        
        yield (item)
