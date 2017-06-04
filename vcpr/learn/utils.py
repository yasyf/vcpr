import numpy as np
from keras.preprocessing import sequence
import keras.backend as K

def threshold_acc(threshold):
  def threshold_acc(y_true, y_pred):
    return K.mean(K.equal(y_true, K.cast(K.greater(y_pred, threshold), K.floatx())))
  threshold_acc.__name__ += '_{:g}'.format(threshold * 100)
  return threshold_acc

def transform_data(data):
  return map(lambda l: map(ord, l), data)

def import_data(f, linelimit):
  # Import domains as arrays of ascii key codes
  return transform_data(f.read().split('\n')[:linelimit])

def split_data(data, labels, trainprop, maxlen):
  P = np.random.permutation(len(data))
  trainvalidatelimit = int(len(data) * trainprop)
  trainlimit = int(trainvalidatelimit * trainprop)

  X = np.array(data)[P]
  Y = np.array(labels)[P]

  X_train_validate = sequence.pad_sequences(X[:trainvalidatelimit], maxlen=maxlen)
  X_train = X_train_validate[:trainlimit]
  X_validate = X_train_validate[trainlimit+1:trainvalidatelimit]
  X_test = sequence.pad_sequences(X[trainvalidatelimit+1:], maxlen=maxlen)

  Y_train_validate = Y[:trainvalidatelimit]
  Y_train = Y_train_validate[:trainlimit]
  Y_validate = Y_train_validate[trainlimit+1:trainvalidatelimit]
  Y_test = Y[trainvalidatelimit+1:]

  return (X_train, X_validate, X_test), (Y_train, Y_validate, Y_test)
