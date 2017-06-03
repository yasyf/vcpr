import scrapy
from .. import utils
from scrapy.linkextractors import LinkExtractor

class BaseSpider(scrapy.Spider):
  def __init__(self):
    super(BaseSpider, self).__init__()
    self.le = LinkExtractor(deny=['tel:'], deny_domains=[
      'twitter.com', 'facebook.com', 'wikipedia.org', 'youtube.com',
      'instagram.com', 'plus.google.com', 'linkedin.com',
    ])
    self.limited = set()

  @staticmethod
  def extract_hostname(o):
    return utils.extract_hostname(o)

  @staticmethod
  def extract_base_hostname(o):
    return utils.extract_base_hostname(o)
