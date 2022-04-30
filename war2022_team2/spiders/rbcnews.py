from fileinput import filename
import scrapy
from scrapy.selector import Selector
 

class RbcNewsSpider(scrapy.Spider):
    base_url = "https://www.rbc.ru/crypto/ajax/get-news-by-filters/?tag=5df0dd989a7947c70d08b4ae&offset={}&limit=12"
    name = 'rbcnews'
    allowed_domains = ['rbc.ru']
    start_urls = [base_url.format(20)]
    offset = 20
    portion = 20
    total_links_to_get = 20
    
    def start_requests(self):
         
            # Request to get the HTML content
        request = scrapy.Request(self.base_url.format(self.offset), cookies={'store_language': 'ru'},
                              callback=self.parse)
        yield request

        
    def parse(self, response):
        data = response.json()
        #todo parse links from data
        text="<body>"+data['html']+"</body>"
        for item in Selector(text=text).css("a:nth-child(even)"):
            fulllink = item.css('a::attr(href)').extract_first()
            
            key = fulllink.split('/')[-1]
            yield {"link":
                    fulllink
                }

        if(self.offset!=self.total_links_to_get):
            self.offset+=self.portion
            request = scrapy.Request(self.base_url.format(self.offset), cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

        
        
       
