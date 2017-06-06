from keras.preprocessing import sequence

maxlen = 20

def transform_data(data):
  return map(lambda l: map(ord, l), data)

def main_features(X):
  return sequence.pad_sequences(transform_data(X), maxlen=maxlen)

def aux_features(X):
  return [{'len': len(x), 'tld': x.split('.')[-1]} for x in X]
