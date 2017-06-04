import numpy as np
from ... import constants

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM

linelimit = 10 ** 4
trainprop = 0.8
maxlen = 30
batchsize = 32

def import_data(f):
  # Import domains as arrays of ascii key codes
  return map(lambda l: map(ord, l), f.read().split('\n')[:linelimit])

with open(constants.TOPSITES, 'r') as f:
  topsites = import_data(f)

with open(constants.STARTUPS, 'r') as f:
  startups = import_data(f)

data = topsites + startups
labels = ([0] * len(topsites)) + ([1] * len(startups))

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

print('X_train: {}, X_validate: {}, X_test: {}'.format(X_train.shape, X_validate.shape, X_test.shape))

model = Sequential()
model.add(Embedding(128, 64, mask_zero=True))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=batchsize, epochs=10, validation_data=(X_test, Y_test))
loss, accuracy = model.evaluate(X_test, Y_test, batch_size=batchsize)
print('Loss: {}, Accuracy: {}'.format(loss, accuracy))
