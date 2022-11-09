import pymongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CONNECTION_PORT = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "MotorMetrics"
COLLECTION_A_NAME = "MotorAStatus"
LENGTH = 1000000

def Connect():
    client = pymongo.MongoClient(CONNECTION_PORT, serverSelectionTimeoutMS=5000)
    try:
        database = client.get_database(DATABASE_NAME)
        collectionA = database.get_collection(COLLECTION_A_NAME)
    except Exception:
        collectionA = None
        print("Unable to connect to the server.")

    return collectionA

def Main():
    collection = Connect()
    if collection is None:
        return None

    fig, ax = plt.subplots(1,1)
    ax.grid(True)

    items = collection.find().sort("ReportTime", pymongo.DESCENDING).limit(LENGTH)
    frame = pd.DataFrame(items)
    elems, = ax.plot(frame['Position'][::-1])

    plt.show()

Main()


