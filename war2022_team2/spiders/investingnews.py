from fileinput import filename
import scrapy


class InvestingSpider(scrapy.Spider):
    name = 'investing'
    allowed_domains = ['ru.investing.com']
    base_url = 'https://ru.investing.com/crypto/bitcoin/analysis{}'
    current_page = 1
    total_pages = 14

    def start_requests(self):
       
        request = scrapy.Request(self.base_url.format(self.current_page), cookies={'store_language': 'ru'},
                              callback=self.parse)
        yield request

        
    def parse(self, response):
         

        for item in response.css('#fullColumn > div.fullHeaderTwoColumnPage--content.cryptoContentColumn >\
         div.js-content-wrapper > div.js-articles-wrapper.largeTitle.analysisImg.js-analysis-items > article') :
            
            article_link = item.css('a::attr(href)').extract_first()
            print(article_link)
            yield {"link":
                'https://ru.investing.com'+article_link
            }

            if(self.current_page!=self.total_pages):
                self.current_page+=1
                yield scrapy.Request(self.base_url.format(self.current_page), cookies={'store_language': 'ru'},
                              callback=self.parse)

        
       
