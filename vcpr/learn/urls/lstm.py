from features import main_features
from ... import constants
from ..utils import read_data, split_data, threshold_acc, register_model, save_all
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM

linelimit = 15 ** 4
trainprop = 0.8
batchsize = 32
epochs = 5

def data_and_labels():
  with open(constants.TOPSITES, 'r') as f:
    topsites = read_data(f, linelimit)

  with open(constants.STARTUPS, 'r') as f:
    startups = read_data(f, linelimit)

  data = main_features(topsites + startups)
  labels = ([0] * len(topsites)) + ([1] * len(startups))

  return (data, labels)

if __name__ == '__main__':
  data, labels = data_and_labels()
  (X_train, X_validate, X_test), (Y_train, Y_validate, Y_test) = split_data(data, labels, trainprop)

  model = Sequential()
  model.add(Embedding(128, 64, mask_zero=True))
  model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
  model.add(Dense(1, activation='sigmoid'))

  register_model(model, constants.URL_LSTM_MODEL)

  model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=[
      threshold_acc(0.4),
      threshold_acc(0.5),
    ],
  )
  model.fit(
    X_train,
    Y_train,
    batch_size=batchsize,
    epochs=epochs,
    validation_data=(X_validate, Y_validate),
  )
  metrics = model.evaluate(X_test, Y_test, batch_size=batchsize)
  print(dict(zip(model.metrics_names, metrics)))

  save_all()
