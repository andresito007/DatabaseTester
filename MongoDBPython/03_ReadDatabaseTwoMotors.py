import pymongo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CONNECTION_PORT = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "MotorMetrics"
COLLECTION_A_NAME = "MotorAStatus"
COLLECTION_B_NAME = "MotorBStatus"
LENGTH = 100

def Connect():
    client = pymongo.MongoClient(
        CONNECTION_PORT, serverSelectionTimeoutMS=5000)
    try:
        database = client.get_database(DATABASE_NAME)
        collectionA = database.get_collection(COLLECTION_A_NAME)
        collectionB = database.get_collection(COLLECTION_B_NAME)
    except Exception:
        collectionA = None
        collectionB = None
        print("Unable to connect to the server.")

    return collectionA, collectionB

def Main():
    plt.ion()
    fig = plt.figure()

    axA = fig.add_subplot(211)
    axB = fig.add_subplot(212)

    axA.grid(True)
    axB.grid(True)

    collectionA, collectionB = Connect()
    if collectionA is None and collectionB is None:
        return None

    itemsA = collectionA.find().sort("ReportTime", pymongo.DESCENDING).limit(LENGTH)
    dataFrameA = pd.DataFrame(itemsA)
    elementsA, = axA.plot(dataFrameA['Position'][::-1])

    itemsB = collectionB.find().sort("ReportTime", pymongo.DESCENDING).limit(LENGTH)
    dataFrameB = pd.DataFrame(itemsB)
    elementsB, = axB.plot(dataFrameB['Position'][::-1])

    axA.set_title("Motor %s" % dataFrameA['MotorData'][0]['MotorID'])
    axB.set_title("Motor %s" % dataFrameB['MotorData'][0]['MotorID'])

    while True:
        itemsA = collectionA.find().sort("ReportTime", pymongo.DESCENDING).limit(LENGTH)
        itemsB = collectionB.find().sort("ReportTime", pymongo.DESCENDING).limit(LENGTH)

        frameA = pd.DataFrame(itemsA)['Position']
        frameB = pd.DataFrame(itemsB)['Position']

        elementsA.set_ydata(frameA)
        elementsB.set_ydata(frameB)

        axA.set_ylim(np.min(frameA)-0.5, np.max(frameA)+0.5)
        axB.set_ylim(np.min(frameB)-0.5, np.max(frameB)+0.5)

        fig.canvas.draw()
        fig.canvas.flush_events()

Main()
