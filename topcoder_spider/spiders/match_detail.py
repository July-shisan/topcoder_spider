from scrapy.selector import Selector
from scrapy.http import Request

from topcoder_spider.items import MatchDetailItem
from login_spider import LoginSpider
from tools import extract_text

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
		item['username'] = extract_text(tds[1].xpath('./a/text()'))
		item['score'] = extract_text(tds[2].xpath('./text()'))
		item['place'] = extract_text(tds[3].xpath('./text()'))
		items.append(item)
		
		if(len(tds) < 6):
			continue

		item = MatchDetailItem()
		item['match_id'] = response.meta['match_id']
		item['division'] = 2
		item['username'] = extract_text(tds[6].xpath('./a/text()'))
		item['score'] = extract_text(tds[7].xpath('./text()'))
		item['place'] = extract_text(tds[8].xpath('./text()'))
		items.append(item)
	return items
