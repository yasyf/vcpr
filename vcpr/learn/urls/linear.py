from features import aux_features
from ... import constants
from ..utils import read_data, split_data, register_model, save_all
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

linelimit = 1.5e4
trainprop = 0.8

def data_and_labels():
  with open(constants.TOPSITES, 'r') as f:
    topsites = read_data(f, linelimit)

  with open(constants.STARTUPS, 'r') as f:
    startups = read_data(f, linelimit)

  data = aux_features(topsites + startups)
  labels = ([0] * len(topsites)) + ([1] * len(startups))

  return (data, labels)

if __name__ == '__main__':
  data, labels = data_and_labels()
  (X_train, X_validate, X_test), (Y_train, Y_validate, Y_test) = split_data(data, labels, trainprop)

  pipeline = Pipeline([
    ('vect', DictVectorizer(sparse=False)),
    ('scale', MinMaxScaler(feature_range=(0.0, 1.0))),
    ('logreg', LogisticRegression(n_jobs=-1))
  ])
  register_model(pipeline, constants.URL_LINEAR_MODEL)

  pipeline.fit(X_train, Y_train)
  acc = pipeline.score(X_test, Y_test)
  print('Test Accuracy: {}'.format(acc))

  save_all()
