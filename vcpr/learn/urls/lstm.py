from ... import constants
from ..utils import import_data, split_data, threshold_acc

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM

linelimit = 15 ** 4
trainprop = 0.8
maxlen = 30
batchsize = 32

with open(constants.TOPSITES, 'r') as f:
  topsites = import_data(f, linelimit)

with open(constants.STARTUPS, 'r') as f:
  startups = import_data(f, linelimit)

data = topsites + startups
labels = ([0] * len(topsites)) + ([1] * len(startups))

(X_train, X_validate, X_test), (Y_train, Y_validate, Y_test) = split_data(data, labels, trainprop, maxlen)
print('X_train: {}, X_validate: {}, X_test: {}'.format(X_train.shape, X_validate.shape, X_test.shape))

model = Sequential()
model.add(Embedding(128, 64, mask_zero=True))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[threshold_acc(0.4)])
model.fit(X_train, Y_train, batch_size=batchsize, epochs=5, validation_data=(X_validate, Y_validate))
loss, accuracy = model.evaluate(X_test, Y_test, batch_size=batchsize)
print('Loss: {}, Accuracy: {}'.format(loss, accuracy))

model.save(constants.URL_MODEL)
