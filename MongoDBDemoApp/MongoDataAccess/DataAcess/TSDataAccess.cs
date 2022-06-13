using MongoDataAccess.Models;
using MongoDB.Bson;
using MongoDB.Driver;
using System;
using System.Collections.Generic;

namespace MongoDataAccess.DataAcess
{
    public class TSDataAccess
    {
        private const string ConnectionPort = "mongodb://127.0.0.1:27017";
        private const string DatabaseName = "MotorMetrics";
        private const string CollectionName = "MotorStatus";
        private const string TimeField = "ReportTime";
        private const string MetaFiled = "MotorData";

        private IMongoCollection<T> ConnectToMongo<T>(in string collection)
        {
            MongoClient client = new MongoClient(ConnectionPort);
            IMongoDatabase database = client.GetDatabase(DatabaseName);
            return database.GetCollection<T>(collection);
        }

        public async void CreateTimeSeriesCollection()
        {
            MongoClient client = new MongoClient(ConnectionPort);
            IMongoDatabase database = client.GetDatabase(DatabaseName);
            await database.CreateCollectionAsync(CollectionName, new CreateCollectionOptions
            {
                TimeSeriesOptions = new TimeSeriesOptions(TimeField, MetaFiled)
            });
        }

        public void CreateNewEntry(MotorMeasurementModel motorMeasurement)
        {
            IMongoCollection<BsonDocument> collection = ConnectToMongo<BsonDocument>(CollectionName);

            Dictionary<string, object> dic = new Dictionary<string, object>
            {
                { TimeField, DateTime.UtcNow },
                { MetaFiled, motorMeasurement.MotorDescription.ToBsonDocument() },
                { nameof(motorMeasurement.Position), motorMeasurement.Position },
                { nameof(motorMeasurement.Speed), motorMeasurement.Speed },
                { nameof(motorMeasurement.Current), motorMeasurement.Current }
            };
            BsonDocument doc = new BsonDocument(dic);
            collection.InsertOneAsync(doc).Wait();

        }

        public void CheckCreated()
        {

        }
    }
}
