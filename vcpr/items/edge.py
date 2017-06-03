import scrapy

class Edge(scrapy.Item):
  from_ = scrapy.Field()
  to = scrapy.Field()
  auto = scrapy.Field()
