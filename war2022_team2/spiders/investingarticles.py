import scrapy
from scrapy.http import Request
from war2022_team2.items import War2022Team2Item
import json
import hashlib

class RbcarticlesSpider(scrapy.Spider):
    name = 'investingarticles'

    def start_requests(self):
        # Open the JSON file which contains article links
        data=[]
        with open('./investinglinks.json') as json_file:
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
        
        item['article_datetime'] = response.css('#leftColumn > div.contentSectionDetails >\
         span:nth-child(3)::text').get()

        item['article_title'] = response.css('#leftColumn > h1::text').extract_first()
         
        
            
        item['article_text'] = "".join(response.xpath('//*[@id="articlePage"]/div//text()').getall())
        item['article_author'] =  response.css("#leftColumn > div.contentSectionDetails > i > a::text").get()
        if (not item['article_author']):
            item['article_author'] = "unknown"

        if("битк" in item['article_title'].lower() or "bitc" in item['article_title'].lower()):
            yield (item)
