import keras

__model_cache = {}

def get_model(path):
  if path not in __model_cache:
    __model_cache[path] = keras.models.load_model(path)
  return __model_cache[path]
