import pymongo
import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import export_graphviz
from six import StringIO 

from IPython.display import Image  
import pydotplus

import sys
sys.path.append("../")
from mongodb_info import getClient

# Receive hospital resource data from MongoDB Atlas
myClient = getClient()
client = pymongo.MongoClient(myClient)
mydb = client['resource_data']
mycol = mydb['mortality_factors']

df = pd.DataFrame(list(mycol.find().limit(20000)))

# Deal with undefine/NaN values
df = df.replace("undefined", np.NaN)
df = df.replace("", np.NaN)
df = df.dropna(how='any',axis=0) 

# Create factors and target sets
X = df.drop(['_id', 'risk_mortality'], axis=1)
y = df['risk_mortality']

# Split data into training and testing data
X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state = 0)

# All categorical columns
object_cols = [col for col in X_train.columns if col not in ["ip_latitude", "ip_longitude", "height", "weight", "bmi"]]

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

# Rename encoded columns
names = OH_encoder.get_feature_names()
for i in range(len(names)):
    x = names[i].find('_')
    names[i] = names[i][x+1:]
    if i >= 3 and i <= 13: names[i] += "_age"
    elif i >= 14 and i <= 22: names[i] += "_blood-type"
    elif i == 23: names[i] = 'covid19 negative'
    elif i == 24: names[i] = 'covid19 positive'
    elif i == 25: names[i] = 'no covid19 symptoms'
    elif i == 26: names[i] = 'has covid19 symptoms'
    elif i == 27: names[i] = 'no covid19 contact'
    elif i == 28: names[i] = 'had covid19 contact'
    elif i == 29: names[i] = 'no asthma'
    elif i == 30: names[i] = 'asthma'
    elif i == 31: names[i] = 'no kidney disease'
    elif i == 32: names[i] = 'kidney disease'
    elif i == 33: names[i] = 'not immunocompromised'
    elif i == 34: names[i] = 'immunocompromised'
    elif i == 35: names[i] = 'no heart disease'
    elif i == 36: names[i] = 'heart disease'
    elif i == 37: names[i] = 'no lung disease'
    elif i == 38: names[i] = 'lung disease'
    elif i == 39: names[i] = 'no diabetes'
    elif i == 40: names[i] = 'diabetes'
    elif i == 41: names[i] = 'hiv negative'
    elif i == 42: names[i] = 'hiv positive'
    elif i == 43: names[i] = 'no hypertension'
    elif i == 44: names[i] = 'hypertension'
    elif i == 45: names[i] = 'no other chronic illnesses'
    elif i == 46: names[i] = 'other chronic illnesses'

OH_cols_train.columns = names
OH_cols_valid.columns = names


# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

# Put together data to be used for fitting model
X = pd.concat([OH_X_train, OH_X_valid], axis=0)
y = pd.concat([y_train, y_valid], axis=0)

# Decision tree regression model
model = DecisionTreeRegressor(max_leaf_nodes=500, random_state=0)
model.fit(X, y)

# Save model
pickle.dump(model, open('model.sav', 'wb'))

'''
# compare MAE with differing values of max_leaf_nodes

def get_mae(max_leaf_nodes):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(OH_X_train, y_train)
    preds_val = model.predict(OH_X_valid)
    print(y_valid.head())
    print(preds_val[:5])
    print(' ')
    mae = mean_absolute_error(y_valid, preds_val)
    return(mae)

# 500 did very well
for max_leaf_nodes in [5, 50, 500]:
    my_mae = get_mae(max_leaf_nodes)
    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(max_leaf_nodes, my_mae))
'''

# Create decision tree visual
dot_data = StringIO()

export_graphviz(model, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,
                feature_names=X.columns)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())
graph.write_png("model.png")

