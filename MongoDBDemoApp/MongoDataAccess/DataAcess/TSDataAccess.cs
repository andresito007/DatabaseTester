using MongoDataAccess.Models;
using MongoDB.Bson;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MongoDataAccess.DataAcess
{
    public class TSDataAccess
    {
        private const string ConnectionPort = "mongodb://127.0.0.1:27017";
        private const string DatabaseName = "TimeSeriesTester";
        private const string CollectionName = "MotorMetrics";
        private const string TimeField = "ReportTime";
        private const string MetaFiled = "Motor";

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

        public async void CreateNewEntry(MotorMeasurementsModel motorMeasurement)
        {
            IMongoCollection<BsonDocument> collection = ConnectToMongo<BsonDocument>(CollectionName);



            //var element1 = new BsonElement(TimeField, motorMeasurement.ReportTime);
            //var element2 = new BsonElement(MetaFiled, motorMeasurement.Position);
            //var element3 = new BsonElement("Position", motorMeasurement.Speed);

            //var elements = new List<BsonElement>() { element1, element2, element3 };

            //var document1 = new BsonDocument(elements);
            //var array1 = new BsonArray(document1);
            var dic = new Dictionary<string, object>();
            dic.Add(TimeField, DateTime.UtcNow);
            dic.Add(MetaFiled, motorMeasurement.MotorDescription.ToBsonDocument());
            dic.Add("Position", motorMeasurement.Position);
            dic.Add("Speed", motorMeasurement.Speed);
            dic.Add("Current", motorMeasurement.Current);
            var doc = new BsonDocument(dic);
            //motorMeasurement.ReportTime = new BsonElement(TimeField, DateTime.UtcNow);
            await collection.InsertOneAsync(doc);
        }

    }
}
