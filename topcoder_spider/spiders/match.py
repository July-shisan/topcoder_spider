from scrapy.selector import Selector
from scrapy.http import Request

from topcoder_spider.items import MatchItem
from login_spider import LoginSpider
from constants import match_list_url, index_url

from urlparse import urljoin,urlparse

class MatchSpider(LoginSpider):
    name = "match"

    stop = False

    def get_crawled(self):
	r = set()
	import os
	if not os.path.exists('match.csv'):
		return r
	import io
	f = io.open('match.csv', 'r', encoding='utf-8')
	lines = f.readlines()
	f.close()
	for line in lines[1:]:
		match_id = line.split(',')[2]
		r.add(int(match_id))
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
		item['match_id'] = int({param.split('=')[0]: param.split('=')[1] for param in urlparse(item['href']).query.split('&')}['rd'])
		if item['match_id'] in self.crawled:
			self.stop = True
			break
		item['date'] = '.'.join([dates[i][0].split('.')[2]] + dates[i][0].split('.')[:2])
		items.append(item)
	return items
