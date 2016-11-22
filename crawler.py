import scrapy
from scrapy.crawler import CrawlerProcess
import re

# Shortcuts of settings for crawler
output_filename = 'data/quotes.csv'
page_from = 1
page_to = 300


class MySpider(scrapy.Spider):
    name = "quota_spider"
    allowed_domains = ["www.bash.org"]

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_IP': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # 0.5*DOWNLOAD_DELAY < delay < 1.5*DOWNLOAD_DELAY
        'DOWNLOAD_DELAY':  0.5,

        'FEED_FORMAT': 'csv',
        'FEED_URI': output_filename,
        'FEED_EXPORT_ENCODING': 'utf-8',

        'DOWNLOADER_MIDDLEWARES_BASE': {
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,  # disabled default
            'random_useragent.RandomUserAgentMiddleware': 400,  # enabled scrapy-random-useragent
        },
    }

    def start_requests(self):
        for number_of_page in range(page_from, page_to):
            yield self.make_requests_from_url("http://www.bash.org/?browse&p=%d" % number_of_page)

    def parse(self, response):
        for quote in response.css('table tr td p.qt'):
            yield {
                # Reason for regex: non-standard, mixed with tags text in target tags
                'text': re.sub(r'<\/p>*|<p .*?qt..>*|[<,&][/,a-z]*[>,;]', '', quote.extract(), flags=re.MULTILINE),
            }


process = CrawlerProcess()
process.crawl(MySpider)
process.start()  # the script will block here until the crawling is finished
