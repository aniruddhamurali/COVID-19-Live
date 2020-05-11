import pickle
import json

from sklearn.tree import DecisionTreeRegressor

model = pickle.load(open('model.sav', 'rb'))


def predict():
    inputs = None
    x = model.predict(inputs)
