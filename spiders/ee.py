from email import header
from pytz import country_names
import scrapy
from scrapy_splash import SplashRequest
from . import countries


class EeSpider(scrapy.Spider):
    name = 'ee'

    headers = {
        'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    all_countries = countries.countries_list
    

    def start_requests(self):
        for each in self.all_countries:
            country_name = each
            country_url = self.all_countries[each]
            #import pdb; pdb.set_trace()
            yield SplashRequest(url=country_url,args={"timeout": 3000,'resource_timeout': 20}, meta= {'country' : country_name})


    def parse(self, response):
        nodes = response.xpath('//div[@class = "col-xs-12 col-sm-6 col-md-4 partner-card grid-item"]')
        country = response.meta['country']
        for node in nodes:
            url = ''.join(node.xpath('./a[@class = "partner-card__logo"]/@href').extract())
            full_url = "https://ee24.com" + url
            #import pdb; pdb.set_trace()

            yield SplashRequest(url = full_url, args={"timeout": 3000,'resource_timeout': 20}, callback = self.parse_details, meta = {'country' : country})

        next_page = ''.join(response.xpath('//a[@aria-label = "Next"]/@href').extract())
        next_page_url = "https://ee24.com/partners/" + country + next_page

        #import pdb; pdb.set
        
        yield SplashRequest(url = next_page_url,args={"timeout": 3000,'resource_timeout': 20}, callback= self.parse, meta= {'country' : country})

    def parse_details(self, response):
        country = response.meta['country']
        name = ''.join(response.xpath('//h1[@class = "sub-title sub-title--large"]/text()').extract()).strip()  
        email = ''.join(response.xpath('//p[@class = "text-center partner-detail__email"]/a/text()').extract()).strip()
        website = ''.join(response.xpath('//p[@class = "text-center realestate-detail__url"]/a/text()').extract()).strip()
        phone = ''.join(response.xpath('//p[@class = "text-center realestate-detail__phones"]/text()').extract()).strip()
        #import pdb; pdb.set_trace()
        yield {
            'country' : country,
            'name' : name,
            'email' : email,
            'website' : website,
            'phone' : phone,
        }
