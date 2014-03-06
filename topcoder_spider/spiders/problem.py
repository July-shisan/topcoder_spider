from scrapy.selector import Selector
from scrapy.http import Request

from topcoder_spider.items import ProblemItem
from login_spider import LoginSpider
from constants import problem_list_url, index_url, problem_content_path

from urlparse import urljoin, urlparse
from os.path import join

class ProblemSpider(LoginSpider):
    name = "problem"

    def crawl(self, response):
	return Request(url=problem_list_url, callback=self.extract)

    def extract(self, response):
	sel = Selector(response)
	trs = sel.xpath('/html/body/table[1]/tr/td[3]/table[2]/tr[1]/td/form/table[2]/table/table/tr')

	for tr in trs[3:-6]:#-6
		item = ProblemItem()
		tds = tr.xpath('.//td[@class="statText"]')
		item['name'] = tds[0].xpath('./a/text()').extract()[0].strip()
		item['href'] = urljoin(index_url, tds[0].xpath('./a/@href').extract()[0]).strip()
		item['problem_id'] = int({param.split('=')[0]: param.split('=')[1] for param in urlparse(item['href']).query.split('&')}['pm'])
		match_href = tds[1].xpath('./a/@href').extract()[0].strip()
		item['match_id'] = int({param.split('=')[0]: param.split('=')[1] for param in urlparse(match_href).query.split('&')}['rd'])
		item['date'] = tds[2].xpath('./text()').extract()[0].strip()
		item['writer'] = tds[3].xpath('./a/text()').extract()[0].strip()
		item['categary'] = tds[4].xpath('./text()').extract()[0].strip()
		item['level_div1'] = tds[5].xpath('./text()').extract()[0].strip()
		item['rate_div1'] = tds[6].xpath('./text()').extract()[0].strip()
		item['level_div2'] = tds[7].xpath('./text()').extract()[0].strip()
		item['rate_div2'] = tds[8].xpath('./text()').extract()[0].strip()

		yield Request(url=item['href'], callback=self.crawl_content, meta={'item':item})
    def crawl_content(self, response):
	item = response.meta['item']
	sel = Selector(response)
	content = sel.xpath('/html/body/table[1]/tr/td[3]/table[2]/tr[1]/td/table/tr[6]/td').extract()[0].strip()
	item['content'] = join(problem_content_path, str(item['problem_id']))
	import io
	f = io.open(item['content'], 'w', encoding='utf8')
	f.write(content)
	f.close()
	return item
