from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

from topcoder_spider.items import ProblemItem
from login_spider import LoginSpider
from constants import problem_list_url, index_url, problem_content_path
from tools import extract_text

from urlparse import urljoin, urlparse
from os.path import join

class ProblemSpider(LoginSpider):
    name = "problem"

    def get_crawled(self):
	r = set()
	import os
	if not os.path.exists('problems.csv'):
		return r
	import io
	f = io.open('problems.csv', 'r', encoding = 'utf-8')
	lines = f.readlines()
	f.close()
	for line in lines[1:]:
		match_id = line.split(',')[0]
		r.add(int(match_id))
	return r

    def crawl(self, response):
	return Request(url=problem_list_url, callback=self.extract)

    def extract(self, response):
	crawled = self.get_crawled()

	sel = Selector(response)
	trs = sel.xpath('/html/body/table[1]/tr/td[3]/table[2]/tr[1]/td/form/table[2]/table/table/tr')

	for tr in trs[3:-6]:#-6
		#try:
			item = ProblemItem()
			tds = tr.xpath('.//td[@class="statText"]')
			item['name'] = extract_text(tds[0].xpath('./a/text()'))
			item['href'] = urljoin(index_url, extract_text(tds[0].xpath('./a/@href')))
			item['problem_id'] = int({param.split('=')[0]: param.split('=')[1] for param in urlparse(item['href']).query.split('&')}['pm'])
			match_href = extract_text(tds[1].xpath('./a/@href'))
			item['match_id'] = int({param.split('=')[0]: param.split('=')[1] for param in urlparse(match_href).query.split('&')}['rd'])
			item['date'] = extract_text(tds[2].xpath('./text()'))
			item['writer'] = extract_text(tds[3].xpath('./a/text()'))
			item['categary'] = extract_text(tds[4].xpath('./text()'))
			item['level_div1'] = extract_text(tds[5].xpath('./text()'))
			item['rate_div1'] = extract_text(tds[6].xpath('./text()'))
			item['level_div2'] = extract_text(tds[7].xpath('./text()'))
			item['rate_div2'] = extract_text(tds[8].xpath('./text()'))
			
			if item['match_id'] in crawled:
				break
			yield Request(url=item['href'], callback=self.crawl_content, meta={'item':item})
		#except Exception,e:
		#	log.msg(tr.extract(), level=log.ERROR)
		#	print e

    def crawl_content(self, response):
	item = response.meta['item']
	sel = Selector(response)
	content = extract_text(sel.xpath('/html/body/table[1]/tr/td[3]/table[2]/tr[1]/td/table/tr[6]/td'))
	item['content'] = join(problem_content_path, str(item['problem_id']))
	import io
	f = io.open(item['content'], 'w', encoding='utf8')
	f.write(content)
	f.close()
	return item
