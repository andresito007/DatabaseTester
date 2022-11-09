import pymongo
import pandas as pd
import matplotlib.pyplot as plt

CONNECTION_PORT = "mongodb://localhost:27017"
DATABASE_NAME = "MotorTester"
COLLECTION_NAME  = "Test1"

def Connect():
    client = pymongo.MongoClient(CONNECTION_PORT, serverSelectionTimeoutMS=5000)
    database = client.get_database(DATABASE_NAME)
    return database.get_collection(COLLECTION_NAME)

def Main():
    try:
        collection = Connect()

        pos = [0,1,2,3,4,5,6,7,8,9]
        vel = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        tor = [9,8,7,6,5,4,3,2,1,0]
        cur = [0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
        record = {
            "Motor description": {"Motor ID": 1, "Brand": 1657, "Model": 654687653781},
            "Motor data": {"Position": pos, "Velocity": vel, "Torque": tor, "Current": cur},
            "Test description": {"Test ID": 134}
        }
        collection.insert_one(record)

    except Exception as e:
        print(e)

Main()