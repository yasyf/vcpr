import networkx as nx
import pickle, models
from .. import constants
from ..learn.urls.features import aux_features
from ..items.node import Category

def is_startup(domain):
  pipeline = models.get_pickle(constants.URL_LINEAR_MODEL)
  data = aux_features([domain])
  pred = pipeline.predict(data)
  return bool(pred[0])

def get_startups(n):
  categories = pickle.load(open(constants.CATEGORIES, 'rb'))
  G = nx.read_gpickle(constants.GRAPH)

  companies = categories[Category.company]
  pr = {k:v for k,v in nx.pagerank(G).iteritems() if k in companies and is_startup(k)}
  return sorted(pr, key=pr.get)[-n:]
