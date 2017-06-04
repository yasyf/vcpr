import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def __from_root(*args):
  return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, *args))

def __getenv(name):
  if name not in os.environ:
    raise NameError('{} must be set'.format(name))

CATEGORIES = __from_root('data', 'categories.pickle')
GRAPH = __from_root('data', 'graph.pickle')

TOPSITES = __from_root('data', 'topsites.txt')
STARTUPS = __from_root('data', 'startups.txt')

URL_MODEL = __from_root('data', 'url.h5')

CB_API_KEY = __getenv('CB_API_KEY')
