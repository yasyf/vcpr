from ..items.node import Node
from ..items.edge import Edge
from .. import constants
import networkx as nx
from scrapy.exceptions import DropItem

class GraphPipeline(object):
  def open_spider(self, spider):
    self.G = nx.DiGraph()

  def close_spider(self, spider):
    nx.write_gpickle(self.G, constants.GRAPH)

  def process_item(self, item, spider):
    if isinstance(item, Node):
      self.G.add_node(item['hostname'])
    elif isinstance(item, Edge):
      if item['from_'] == item['to']:
        raise DropItem
      if not item['auto'] and ((not self.G.has_node(item['from_'])) or (not self.G.has_node(item['to']))):
        raise DropItem
      self.G.add_edge(item['from_'], item['to'])
    return item
