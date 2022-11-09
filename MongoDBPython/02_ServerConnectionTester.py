import pymongo
import pandas as pd
import matplotlib.pyplot as plt

CONNECTION_PORT = "mongodb://192.168.50.6:27017"
DATABASE_NAME = "local"
COLLECTION_NAME = "startup_log"

def Connect():
    client = pymongo.MongoClient(CONNECTION_PORT, serverSelectionTimeoutMS=5000)
    database = client.get_database(DATABASE_NAME)
    return database.get_collection(COLLECTION_NAME)

def Main():
    try:
        collection = Connect()
        items = collection.find()
        dataFrame = pd.DataFrame(items)
        print(dataFrame)
    except Exception as e:
        print(e)

Main()