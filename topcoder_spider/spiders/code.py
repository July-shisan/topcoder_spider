from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log

from topcoder_spider.items import SolutionItem
from login_spider import LoginSpider
from constants import problem_detail_url, index_url, code_path, problem_solution_url
from tools import extract_text, get_param

from urlparse import urljoin, urlparse
from os.path import join

from scrapy import log

class CodeSpider(LoginSpider):
    name = "code"

    def get_failed(self):
	r = set()
	from os.path import exists
	if not exists('codes.csv'):
		return r
	import io
	f = io.open('codes.csv', 'r', encoding = 'utf-8')
	lines = f.readlines()
	f.close()
	for line in lines[1:]:
		items = line.split(',')
		pid = items[-1].strip()
		status = items[0]
		if status.find('Failed') != -1:
			r.add(pid)
	return r

    def get_already_crawled(self):
	r = set()
	from os.path import exists
	if not exists('codes.csv'):
		return r
	import io
	f = io.open('codes.csv', 'r', encoding = 'utf-8')
	lines = f.readlines()
	f.close()
	for line in lines[1:]:
		items = line.split(',')
		pid = items[-1].strip()
		r.add(pid)
	return r

    def crawl(self, response):
	import io
	f = io.open('problems.csv', 'r', encoding = 'utf-8')
	lines = f.readlines()
	f.close()

	crawled_set = self.get_already_crawled()
	#failed = self.get_failed()
	for line in lines[1:]:
		items = line.split(',')
		match_id = items[0]
		problem_id = items[-2]
		if problem_id not in crawled_set:
			yield Request(url=(problem_detail_url % (match_id, problem_id)), callback=self.extract, meta={'match_id':match_id, 'problem_id':problem_id})

    def extract(self, response):
	sel = Selector(response)
	trs = sel.xpath('/html/body/table[1]/tr/td[3]/div/table[3]').xpath('.//tr')
	code_tr = None
	for (i, tr) in enumerate(trs):
		td0 = tr.xpath('./td[1]/text()')
		row_name = extract_text(td0)
		if row_name == 'Top Submission':
			code_tr = tr
			break

	if code_tr is None:
		log.msg('No Top Submission Row found! Please check match_id: %s problem_id: %s!' % (response.meta['match_id'], response.meta['problem_id']), level=log.WARNING)
		return

	tds = code_tr.xpath('.//td')
	for (i, td) in enumerate(tds[1:-1]):
		href = urljoin(index_url, extract_text(td.xpath('./a/@href')))
		solution_id = get_param(href, 'cr')
		href = problem_solution_url % (solution_id, response.meta['match_id'], response.meta['problem_id'])
		if solution_id is None:
			continue 
		d = {'match_id':response.meta['match_id'], 'problem_id':response.meta['problem_id'], 'solution_id': solution_id, 'code_id':i}
		yield Request(url=href, callback=self.crawl_content, meta=d)

	
    def crawl_content(self, response):
	problem_id = response.meta['problem_id']
	code_id = response.meta['code_id']
	solution_id = response.meta['solution_id']
	match_id = response.meta['match_id']

	languages = ['Java', 'C++', 'C#', 'VB', 'Python']

	item = SolutionItem()
	item['problem_id'] = problem_id
	item['match_id'] = match_id
	item['solution_id'] = solution_id
	item['language'] = languages[code_id]
	item['status'] = 'Success'
	sel = Selector(response)
	trs = sel.xpath('/html/body/table[1]/tr/td[3]/table[2]/tr[1]/td/table[2]').xpath('.//tr')
	code_tr = None
	for (i, tr) in enumerate(trs):
		td0 = tr.xpath('./td[1]/@class')
		if extract_text(td0) == 'problemText':
			code_tr = tr
			break
	if code_tr is None:
		log.msg('No code found! Please check match_id: %s, problem_id: %s, solution_id: %s!' % (match_id, problem_id, solution_id), level=log.WARNING)
		item['status'] = 'Failed!1'
		return item
		
	content = extract_text(code_tr.xpath('./td'))

	import io
	f = io.open(join(code_path, problem_id + '_' + languages[code_id]), 'w', encoding='utf8')
	f.write(content)
	f.close()
	return item
