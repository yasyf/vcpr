import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def __from_root(*args):
  return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, *args))

def __getenv(name):
  if name not in os.environ:
    raise NameError('{} must be set'.format(name))

# Graph Crawl

CATEGORIES = __from_root('data', 'categories.pickle')
GRAPH = __from_root('data', 'graph.pickle')

# Learning Data

TOPSITES = __from_root('data', 'topsites.txt')
STARTUPS = __from_root('data', 'startups.txt')

# Learning Models

## URL Model

URL_LSTM_MODEL = __from_root('data', 'url', 'lstm.h5')

URL_LSTM_PLUS_MODEL = __from_root('data', 'url', 'lstm_plus.h5')
URL_LSTM_PLUS_PIPELINE = __from_root('data', 'url', 'lstm_plus_pipeline.pickle')

# API KEYS

CB_API_KEY = __getenv('CB_API_KEY')
