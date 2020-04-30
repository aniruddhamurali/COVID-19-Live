import pymongo

client = pymongo.MongoClient("mongodb+srv://mainUser:An1ruddha@hospitalization-ptx4a.gcp.mongodb.net/test")
mydb = client['resource_data']
mycol = mydb['resources_4_27']

'''doc = mycol.find()
for data in doc:
    print(data['ICUbed_mean'])
'''
for data in mycol.find({"date":"2020-04-27"}):
    print(data)
