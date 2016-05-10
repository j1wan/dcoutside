from dcoutside.crawler import DCInsideCrawler
from pprint import pprint

crawler = DCInsideCrawler(include_comments=True)
pprint(crawler.get_post('produce101', 1))
