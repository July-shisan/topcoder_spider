from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request

from topcoder_spider.items import MatchItem
from constants import domain, index_url, Login, match_list_url

class LoginSpider(Spider):
    name = "login"
    allowed_domains = [domain]
    start_urls = (
        Login.login_url,
        )

    def parse(self, response):
	return [FormRequest.from_response(response, formdata=Login.formdata, formname=Login.formname, callback=self.crawl)]
