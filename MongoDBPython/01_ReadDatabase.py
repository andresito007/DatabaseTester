import pymongo
import pandas as pd
import matplotlib.pyplot as plt

CONNECTION_PORT = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "MotorMetrics"
COLLECTION_NAME = "MotorStatus"

def Connect():
    client = pymongo.MongoClient(CONNECTION_PORT, serverSelectionTimeoutMS=5000)
    try:
        database = client.get_database(DATABASE_NAME)
        collection = database.get_collection(COLLECTION_NAME)
    except Exception:
        collection = None
        print("Unable to connect to the server.")

    return collection

def Main():
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    collection = Connect()
    if collection is None:
        return None
    
    items = collection.find().sort("ReportTime", pymongo.DESCENDING).limit(50)
    dataFrame = pd.DataFrame(items)
    elements, = ax.plot(dataFrame['Position'][::-1])

    while True:
        items = collection.find().sort("ReportTime", pymongo.DESCENDING).limit(50)
        dataFrame = pd.DataFrame(items)
        # print(dataFrame.count)
        elements.set_ydata(dataFrame['Position'])
        fig.canvas.draw()
        fig.canvas.flush_events()

Main()