from features import aux_features, main_features, maxlen
from ... import constants
from ..utils import read_data, split_data, threshold_acc, register_model, save_all, np_zip, np_unzip
from keras.models import Model
from keras.layers import Dense, Embedding, LSTM, Input, concatenate
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

linelimit = 1.5e4
trainprop = 0.8
batchsize = 32
epochs = 5

def data_and_labels():
  with open(constants.TOPSITES, 'r') as f:
    topsites = read_data(f, linelimit)

  with open(constants.STARTUPS, 'r') as f:
    startups = read_data(f, linelimit)

  main_data = main_features(topsites + startups)

  pipeline = Pipeline([
    ('vect', DictVectorizer(sparse=False)),
    ('scale', MinMaxScaler(feature_range=(0.0, 1.0))),
  ])
  register_model(pipeline, constants.URL_LSTM_PLUS_PIPELINE)
  aux_data = pipeline.fit_transform(aux_features(topsites + startups))

  data = np_zip(main_data, aux_data)
  labels = ([0] * len(topsites)) + ([1] * len(startups))

  return (data, labels)

if __name__ == '__main__':
  data, labels = data_and_labels()

  (X_train, X_validate, X_test), (Y_train, Y_validate, Y_test) = split_data(data, labels, trainprop)
  X_train_main, X_train_aux = np_unzip(X_train)
  X_validate_main, X_validate_aux = np_unzip(X_validate)
  X_test_main, X_test_aux = np_unzip(X_test)

  main_input = Input(shape=(maxlen,), dtype='int32', name='main_input')
  embed = Embedding(input_dim=128, output_dim=64, input_length=maxlen, mask_zero=True)(main_input)
  lstm = LSTM(64, dropout=0.2, recurrent_dropout=0.2)(embed)
  lstm_out = Dense(1, activation='sigmoid', name='lstm_out')(lstm)

  aux_input = Input(shape=(X_train_aux.shape[-1],), name='aux_input')
  merged = concatenate([lstm, aux_input])
  dense = Dense(32, activation='relu')(merged)
  main_out = Dense(1, activation='sigmoid', name='main_out')(dense)

  model = Model(inputs=[main_input, aux_input], outputs=[main_out, lstm_out])
  register_model(model, constants.URL_LSTM_PLUS_MODEL)

  model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    loss_weights=[1., 0.2],
    metrics=[
      threshold_acc(0.4),
      threshold_acc(0.5),
    ],
  )
  model.fit(
    [X_train_main, X_train_aux],
    [Y_train, Y_train],
    batch_size=batchsize,
    epochs=epochs,
    validation_data=([X_validate_main, X_validate_aux], [Y_validate, Y_validate]),
  )
  metrics = model.evaluate([X_test_main, X_test_aux], [Y_test, Y_test], batch_size=batchsize)
  print(dict(zip(model.metrics_names, metrics)))

  save_all()
