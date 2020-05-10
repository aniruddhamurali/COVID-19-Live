import pymongo
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn import tree

import sys
sys.path.append("../")
from mongodb_info import getClient

myClient = getClient()
client = pymongo.MongoClient(myClient)
mydb = client['resource_data']
mycol = mydb['mortality_factors']

df = pd.DataFrame(list(mycol.find()))

df = df.replace("undefined", np.NaN)
df = df.replace("", np.NaN)
df = df.dropna(how='any',axis=0) 


'''df.drop(['ip_accuracy', 'smoking', 'alcohol', 'cannabis', 'amphetamines', 'cocaine',
         'lsd', 'mdma', 'contacts_count', 'house_count', 'text_working', 'rate_government_action', 
         'rate_reducing_risk_single', 'rate_reducing_risk_house', 'rate_reducing_mask', 
         'prescription_medication', 'opinion_infection', 'opinion_mortality', 'risk_infection'], axis=1, inplace=True)
'''
X = df.drop(['_id', 'risk_mortality'], axis=1)
y = df['risk_mortality']


X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state = 0)

# All categorical columns
#object_cols = [col for col in X_train.columns if X_train[col].dtype == "object"]
object_cols = [col for col in X_train.columns if col not in ["ip_latitude", "ip_longitude", "height", "weight", "bmi"]]

print(object_cols)

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))
print(OH_cols_valid.head())

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index


# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)
print(num_X_valid.head())

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)
print(OH_X_valid.head())

def get_mae(max_leaf_nodes):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(OH_X_train, y_train)
    preds_val = model.predict(OH_X_valid)
    print(y_valid.head())
    print(preds_val[:5])
    print(' ')
    mae = mean_absolute_error(y_valid, preds_val)
    return(mae)

X = pd.concat([OH_X_train, OH_X_valid], axis=0)
y = pd.concat([y_train, y_valid], axis=0)

model = DecisionTreeRegressor(max_leaf_nodes=500, random_state=0)
model.fit(X, y)

#tree.plot_tree(model)

'''
# compare MAE with differing values of max_leaf_nodes
# 500 did very well
for max_leaf_nodes in [5, 50, 500]:
    my_mae = get_mae(max_leaf_nodes)
    print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(max_leaf_nodes, my_mae))
'''



from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus

dot_data = StringIO()

export_graphviz(model, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,
                feature_names=X.columns)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())
graph.write_png("model")

