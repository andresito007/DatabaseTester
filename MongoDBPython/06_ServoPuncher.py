import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta

CONNECTION_PORT = "mongodb://192.168.50.4:27017"
DATABASE_NAME = "ServoPuncher"
COLLECTION_NAME = "Tests"
SHAPE = (5, 5)

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
    collection = Connect()
    if collection is None:
        return None
    
    limit = SHAPE[0]
    tz = timezone(timedelta(hours=8))
    filter = { 'TestDescription.Timestamp': { '$gt': datetime(2022, 10, 20, 0, 0, 0, tzinfo=tz) } }

    for i in range(5):
        fig, axs = plt.subplots(SHAPE[0], SHAPE[1], sharex=True)
        items = collection.find(filter).sort("TestDescription.Timestamp", pymongo.DESCENDING).skip(i*limit).limit(limit)

        dataFrame = pd.DataFrame(items)

        j, k = 0, 0
        for m in range(dataFrame.shape[0]):
            pos = dataFrame["MotorData"][m]["Position"]
            vel = dataFrame["MotorData"][m]["Velocity"]
            tor = dataFrame["MotorData"][m]["Torque"]
            cur = dataFrame["MotorData"][m]["Current"]
            tit = dataFrame["TestDescription"][m]["Timestamp"]
            # dataFrame2save = pd.DataFrame(dataFrame["MotorData"][m])
            # dataFrame2save.to_csv("0_{}.csv".format(format(m, "03")))

            if k >= SHAPE[1]:
                j += 1
                k = 0
            
            axs[j, k+0].annotate('Timestamp: {0}'.format(tit), xy=(0,0))
            axs[j, k+0].set_ylim([-3, 3])
            axs[j, k+0].xaxis.set_tick_params(labelbottom=False, bottom=False)
            axs[j, k+0].yaxis.set_tick_params(labelbottom=False, left=False)
            axs[j, k+0].spines['top'].set_visible(False)
            axs[j, k+0].spines['right'].set_visible(False)
            axs[j, k+0].spines['bottom'].set_visible(False)
            axs[j, k+0].spines['left'].set_visible(False)

            axs[j, k+1].plot(pos)
            axs[j, k+2].plot(vel, 'r')
            axs[j, k+3].plot(tor, 'k')
            axs[j, k+4].plot(cur, 'b')
            
            axs[j, k+1].grid(True)
            axs[j, k+2].grid(True)
            axs[j, k+3].grid(True)
            axs[j, k+4].grid(True)

            axs[j, k+1].ticklabel_format(style='sci')
            axs[j, k+2].ticklabel_format(style='sci', scilimits=(0,0))
            axs[j, k+3].ticklabel_format(style='sci', scilimits=(0,0))
            axs[j, k+4].ticklabel_format(style='sci', scilimits=(0,0))
            
            if(j==0):
                axs[j, k+1].set_title("Position (cmd)")
                axs[j, k+2].set_title("Velocity (cmd/s)")
                axs[j, k+3].set_title(r"Torque (mN$\times$m)")
                axs[j, k+4].set_title("Current (mA)")

            k += SHAPE[1]

    plt.show()

            
Main()

