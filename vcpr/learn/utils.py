import numpy as np
from keras.models import Model
import keras.backend as K
import pickle, os

__models = []

def register_model(model, serialization_path):
  __models.append((model, serialization_path))

def save_all():
  for (model, path) in __models:
    try:
      os.makedirs(os.path.dirname(path))
    except OSError:
      pass
    if isinstance(model, Model):
      save_keras_model(model, path)
    else:
      pickle_model(model, path)

def threshold_acc(threshold):
  def threshold_acc(y_true, y_pred):
    return K.mean(K.equal(y_true, K.cast(K.greater(y_pred, threshold), K.floatx())))
  threshold_acc.__name__ += '_{:g}'.format(threshold * 100)
  return threshold_acc

def read_data(f, linelimit):
  return f.read().split('\n')[:linelimit]

def split_data(data, labels, trainprop=0.8, P=None):
  P = P or np.random.permutation(len(data))
  trainvalidatelimit = int(len(data) * trainprop)
  trainlimit = int(trainvalidatelimit * trainprop)

  X = np.array(data)[P]
  Y = np.array(labels)[P]

  X_train_validate = X[:trainvalidatelimit]
  X_train = X_train_validate[:trainlimit]
  X_validate = X_train_validate[trainlimit+1:trainvalidatelimit]
  X_test = X[trainvalidatelimit+1:]

  Y_train_validate = Y[:trainvalidatelimit]
  Y_train = Y_train_validate[:trainlimit]
  Y_validate = Y_train_validate[trainlimit+1:trainvalidatelimit]
  Y_test = Y[trainvalidatelimit+1:]

  return (X_train, X_validate, X_test), (Y_train, Y_validate, Y_test)

def save_keras_model(model, path):
  K.set_learning_phase(0)
  persist = Model.from_config(model.get_config())
  persist.set_weights(model.get_weights())
  persist.save(path)

def pickle_model(model, path):
  with open(path, 'wb') as f:
    pickle.dump(model, f)

def np_zip(a, b):
  return zip(a, b)

def np_unzip(x):
  a, b = x.T
  return np.stack(a), np.stack(b)
