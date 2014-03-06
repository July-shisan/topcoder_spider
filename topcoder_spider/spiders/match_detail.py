from scrapy.selector import Selector
from scrapy.http import Request

from topcoder_spider.items import MatchDetailItem
from login_spider import LoginSpider

class MatchDetailSpider(LoginSpider):
    name = "match_detail"

    def crawl(self, response):
	f = open('match.csv', 'r')
	lines = f.readlines()
	f.close()
	self.start_url = []  
	for line in lines[1:]:
		date, href, match_id, name = [item.strip() for item in line.split(',')]
		meta = {'date':date, 'href':href, 'name':name, 'match_id':match_id}
		yield Request(url=href, callback=self.extract, meta=meta)

    def extract(self, response):
	items = []
	sel = Selector(response)
	trs = sel.xpath('/html/body/table[1]/tr/td[3]/table[3]/tr')
	for tr in trs[3:]:
		tds = tr.xpath('.//td')

		item = MatchDetailItem()
		item['match_id'] = response.meta['match_id']
		item['division'] = 1
		item['username'] = tds[1].xpath('./a/text()').extract()[0].strip()
		item['score'] = tds[2].xpath('./text()').extract()[0].strip()
		item['place'] = tds[3].xpath('./text()').extract()[0].strip()
		items.append(item)
		
		if(len(tds) < 6):
			continue

		item = MatchDetailItem()
		item['match_id'] = response.meta['match_id']
		item['division'] = 2
		item['username'] = tds[6].xpath('./a/text()').extract()[0].strip()
		item['score'] = tds[7].xpath('./text()').extract()[0].strip()
		item['place'] = tds[8].xpath('./text()').extract()[0].strip()
		items.append(item)
	return items
