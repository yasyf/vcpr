from scrapy.exceptions import IgnoreRequest
from collections import defaultdict
from ..utils import extract_hostname

LIMIT = 10

class LimitedHostsMiddleware(object):
  def __init__(self):
    self.counts = defaultdict(int)

  def process_request(self, request, spider):
    hostname = extract_hostname(request)
    if hostname not in getattr(spider, 'limited', set()):
      return
    if self.counts[hostname] > LIMIT:
      raise IgnoreRequest
    else:
      self.counts[hostname] += 1
