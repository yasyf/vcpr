import keras, pickle

__model_cache = {}

def get_model(path, metrics=None):
  if path not in __model_cache:
    __model_cache[path] = keras.models.load_model(path, custom_objects=metrics or {})
  return __model_cache[path]

def get_pickle(path):
  if path not in __model_cache:
    with open(path, 'rb') as f:
      __model_cache[path] = pickle.load(f)
  return __model_cache[path]
