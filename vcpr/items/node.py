import scrapy, enum

class Category(enum.Enum):
  company = 1
  news = 2

class Node(scrapy.Item):
  hostname = scrapy.Field()
  category = scrapy.Field()
