from fileinput import filename
import scrapy


class NewslabSpider(scrapy.Spider):
    name = 'forklognews'
    allowed_domains = ['forklog.com']
    start_urls = ['https://forklog.com/tag/prognozy/']

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)
            # Request to get the HTML content
            request = scrapy.Request(link_url, cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

        
    def parse(self, response):
         

        for item in response.css('body > main > div.inner > div.category_page_grid > div.cell:nth-child(n):nth-child(-n+7)') :
            
            # print("11111111111111111111")
            # print(article_link)
            
            # item = article_link.xpath('//a/@href').extract_first()
            # print("22222222222222222222222")
          
            article_link = item.css('a::attr(href)').extract_first()
            print(article_link)
            yield {"link":
                article_link
            }
        
       
