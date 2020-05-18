import pickle
import json
import geocoder

from sklearn.tree import DecisionTreeRegressor

# get current location
def getCoords():
    g = geocoder.ip('me')
    return g.latlng


def makeInput(d):
    keys = d.keys()
    coords = getCoords()
    inputs = []

    # add latitude and longitude
    inputs.append(coords[0])
    inputs.append(coords[1])

    # add height and weight
    inputs.append(float(d['height']))
    inputs.append(float(d['weight']))

    # add bmi
    bmi = (float(d['weight'])) / (float(d['height'])/100)**2
    inputs.append(bmi)

    # add sex encodings
    sex = d['sex']
    inputs += [sex == "female", sex == "male", sex == "other"]

    # add age encodings
    age = d['age']
    inputs += [age == "0_10", age == "10_20", age == "20_30", age == "30_40", age == "40_50", age == "50_60", 
               age == "60_70", age == "70_80", age == "80_90", age == "90_100", age == "100_110"]

    # add blood type encodings
    blood = d['blood_type']
    inputs += [blood == "abn", blood == "abp", blood == "an", blood == "ap", blood == "bn", blood == "bp", 
               blood == "on", blood == "op", blood == "unknown"]
    
    # add covid-19 positive encodings
    if "covid19_positive" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add covid-19 symptoms encodings
    if "covid19_symptoms" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add covid-19 contact encodings
    if "covid19_contact" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add asthma encodings
    if "asthma" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add kidney disease encodings
    if "kidney_disease" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add immunocompromised encodings
    if "compromised_immune" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add heart disease encodings
    if "heart_disease" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add lung disease encodings
    if "lung_disease" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add diabetes encodings
    if "diabetes" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add hiv positive encodings
    if "hiv_positive" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add hypertension encodings
    if "hypertension" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # add other chronic illnesses encodings
    if "other_chronic" in keys:
        inputs += [0, 1]
    else:
        inputs += [1, 0]

    # Convert all inputs to integers
    for i in range(len(inputs)):
        inputs[i] = float(inputs[i])

    return inputs
        

# Predict mortality risk based on inputs and model
def predict(d):
    # Load model
    model = pickle.load(open('other_data/model.sav', 'rb'))
    inputs = makeInput(d)
    x = model.predict([inputs])
    return x[0]
