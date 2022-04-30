from fileinput import filename
import scrapy


class TradingviewSpider(scrapy.Spider):
    name = 'tradingview'
    allowed_domains = ['ru.tradingview.com']
    base_url = 'https://ru.tradingview.com/symbols/BTCUSDT/ideas/page-{}'
    current_page = 1
    total_pages = 56

    def start_requests(self):
       
        request = scrapy.Request(self.base_url.format(self.current_page), cookies={'store_language': 'ru'},
                              callback=self.parse)
        yield request

        
    def parse(self, response):
         

        for item in response.xpath('//p[@class = "tv-widget-idea__description-row tv-widget-idea__description-row--clamped js-widget-idea__popup"]'):
            
            article_link = item.css('::attr(data-href)').extract_first()
            print(article_link)
            yield {"link":
                'https://ru.tradingview.com'+article_link
            }

            if(self.current_page!=self.total_pages):
                self.current_page+=1
                yield scrapy.Request(self.base_url.format(self.current_page), cookies={'store_language': 'ru'},
                              callback=self.parse)

        
       
