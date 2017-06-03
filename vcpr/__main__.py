import networkx as nx
import pickle, sys, constants
from items.node import Category

if __name__ == '__main__':
  categories = pickle.load(open(constants.CATEGORIES, 'rb'))
  G = nx.read_gpickle(constants.GRAPH)

  companies = categories[Category.company]
  pr = {k:v for k,v in nx.pagerank(G).iteritems() if k in companies}
  print sorted(pr, key=pr.get)[-int(sys.argv[1]):]
