import scrapy
import re
from pdf_url.items import PdfUrlItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class PdfUrlSpider(CrawlSpider):
    # This name is required. I is how we refer to this PdfUrlSpider class in the CMD 
    name = 'pdf_url'

    # Every link we look at MUST be a part of the adobe.com domain. Must contain "adobe.com" in the url itself
    allowed_domains = ['adobe.com']

    # this is the url we will start from (Check all the links on this webpage first, then go deeper)
    start_urls = ['https://www.adobe.com']

    # This Rule says:
    # 1. allow all links to be extracted. If you want more restrictions you can do something like "/categories"
    # 2. call parse_httpresponse on each extracted link
    # 3. follow all links ("click" on them) so we can check all the links on THAT webpage too
    rules = [Rule(LinkExtractor(allow=""), callback='parse_httpresponse', follow=True)]

    def parse_httpresponse(self, response):
        # 200 means successful GET. If we don't get 200, (broken link) then skip 
        if response.status != 200:
            return None
        print(response.url)

        item = PdfUrlItem()
        if b'Content-Type' in response.headers.keys():
            links_to_pdf = 'application/pdf' in str(response.headers['Content-Type'])
        else:
            return None

        #check if content disposition exist
        content_disposition_exist = b'Content-Disposition' in response.headers.keys()
        
        if links_to_pdf:
            if content_disposition_exist:
                item['filename'] = re.search('filename="(.+)', str(response.headers['Content-Disposition'])).group(1)
                item['url'] = response.url
            else:
                item['filename'] = response.url.split('/')[-1]
                item['url'] = response.url
 
        else:
            return None


        return item