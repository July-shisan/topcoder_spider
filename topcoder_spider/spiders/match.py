from scrapy.selector import Selector
from scrapy.http import Request

from topcoder_spider.items import MatchItem
from login_spider import LoginSpider
from constants import match_list_url, index_url

from urlparse import urljoin,urlparse
import json

class MatchSpider(LoginSpider):
    name = "match"

    stop = False

    def get_crawled(self):
	r = set()
	import os
	if not os.path.exists('match.json'):
		return r
	l = json.loads(open('match.json', 'r').read())
	for d in l:
		match_id = d['match_id']
		r.add(match_id)
	return r

    crawled = None

    def crawl(self, response):
	self.crawled = self.get_crawled()
	for i in xrange(1, 1000, 200):
		if not self.stop:
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
		item['href'] = urljoin(index_url, hrefs[i])
		item['match_id'] = {param.split('=')[0]: param.split('=')[1] for param in urlparse(item['href']).query.split('&')}['rd']
		if item['match_id'] in self.crawled:
			self.stop = True
			break
		item['date'] = '.'.join([dates[i][0].split('.')[2]] + dates[i][0].split('.')[:2])
		items.append(item)
	return items
