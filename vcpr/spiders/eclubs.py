import base
from ..items.node import Category, Node
from ..items.edge import Edge

class EclubsSpider(base.BaseSpider):
  name = 'eclubs'
  start_urls = [
    'http://entrepreneurship.mit.edu/accelerator/demo-day/'
  ]

  def parse(self, response):
    hostname = self.extract_hostname(response)
    for l in self.le.extract_links(response):
      if self.extract_hostname(l) == hostname:
        yield response.follow(l.url, self.parse)
      else:
        yield response.follow(l.url, self.parse_company_site)

  def parse_company_site(self, response):
    hostname = self.extract_hostname(response)
    seen = set()

    yield Node(hostname=hostname, category=Category.company)

    for l in self.le.extract_links(response):
      l_hostname = self.extract_hostname(l)
      l_base_hostname = self.extract_base_hostname(l)

      if l_hostname == hostname:
        self.limited.add(hostname)
        yield response.follow(l.url, self.parse_company_site)
      elif l_base_hostname not in seen:
        seen.add(l_base_hostname)
        yield Edge(from_=hostname, to=l_base_hostname, auto=True)
        yield response.follow(l.url, self.parse_news_site)

  def parse_news_site(self, response):
    base_hostname = self.extract_base_hostname(response)
    seen = set()

    yield Node(hostname=base_hostname, category=Category.news)

    for l in self.le.extract_links(response):
      l_base_hostname = self.extract_base_hostname(l)
      if l_base_hostname not in seen:
        seen.add(l_base_hostname)
        yield Edge(from_=base_hostname, to=l_base_hostname, auto=False)
