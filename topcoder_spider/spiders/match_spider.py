from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request

from topcoder_spider.items import MatchItem
from constants import domain, index_url, Login, match_list_url

class MatchSpider(Spider):
    name = "match"
    allowed_domains = [domain]
    start_urls = (
        Login.login_url,
        )

    def parse(self, response):
	return [FormRequest.from_response(response, formdata=Login.formdata, formname=Login.formname, callback=self.crawl_match)]


    def crawl_match(self, response):
	for i in xrange(0, 1000, 200):
		yield Request(url=match_list_url % i,callback=self.extract)

    def extract(self, response):
	items = []
	sel = Selector(response)
	names = sel.xpath('//td[@class="value"]').xpath('.//a/text()').extract()
	hrefs = sel.xpath('//td[@class="value"]').xpath('.//a/@href').extract()
	dates_sel = sel.xpath('//td[@class="valueC"]')
	dates = [dates_sel[i].xpath('.//text()').extract() for i in xrange(0, len(dates_sel), 2)]
		
	for i in xrange(len(names)):
		#print names[i], index_url + hrefs[i], dates[i]
		item = MatchItem()
		item['name'] = names[i]
		if names[i] == 'SRM 611':
			print response.request.url
		item['href'] = index_url + hrefs[i]
		item['date'] = '.'.join([dates[i][0].split('.')[2]] + dates[i][0].split('.')[:2])
		items.append(item)
	return items
