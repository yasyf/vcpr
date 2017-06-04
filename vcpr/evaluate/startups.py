import networkx as nx
import pickle, models
from .. import constants
from ..items.node import Category

THRESHOLD = 0.4

def is_startup(url):
  model = models.get_model(constants.URL_MODEL)
  return model.predict([url])[0] > THRESHOLD

def get_startups(n):
  categories = pickle.load(open(constants.CATEGORIES, 'rb'))
  G = nx.read_gpickle(constants.GRAPH)

  companies = categories[Category.company]
  pr = {k:v for k,v in nx.pagerank(G).iteritems() if k in companies and is_startup(k)}
  return sorted(pr, key=pr.get)[-n:]
