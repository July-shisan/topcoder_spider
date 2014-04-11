# Scrapy settings for topcoder_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'topcoder_spider'

SPIDER_MODULES = ['topcoder_spider.spiders']
NEWSPIDER_MODULE = 'topcoder_spider.spiders'

CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_SPIDERS = 1
DOWNLOAD_DELAY = 1	
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'topcoder_spider (+http://www.yourdomain.com)'
