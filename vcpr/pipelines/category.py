from ..items.node import Node
from .. import constants
from collections import defaultdict
import pickle

class CategoryPipeline(object):
  def open_spider(self, spider):
    self.categories = defaultdict(set)

  def close_spider(self, spider):
    pickle.dump(self.categories, open(constants.CATEGORIES, 'wb'))

  def process_item(self, item, spider):
    if isinstance(item, Node):
      self.categories[item['category']].add(item['hostname'])
    return item
