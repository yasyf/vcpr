import networkx as nx
import pickle, models
from .. import constants
from ..learn.utils import threshold_acc
from ..learn.urls.features import main_features, aux_features
from ..items.node import Category

THRESHOLD = 0.4

def is_startup(domain):
  model = models.get_model(constants.URL_LSTM_PLUS_MODEL, {
    'threshold_acc_40': threshold_acc(0.4),
    'threshold_acc_50': threshold_acc(0.5),
  })
  pipeline = models.get_pickle(constants.URL_LSTM_PLUS_PIPELINE)

  main_data = main_features([domain])
  aux_data = pipeline.transform(aux_features([domain]))

  pred = model.predict([main_data, aux_data])
  return pred[0][0][0] > THRESHOLD

def get_startups(n):
  categories = pickle.load(open(constants.CATEGORIES, 'rb'))
  G = nx.read_gpickle(constants.GRAPH)

  companies = categories[Category.company]
  pr = {k:v for k,v in nx.pagerank(G).iteritems() if k in companies and is_startup(k)}
  return sorted(pr, key=pr.get)[-n:]
