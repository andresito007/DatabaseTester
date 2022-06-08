using MongoDataAccess.Models;
using MongoDB.Driver;
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
            return database.GetCollection<T>(CollectionName);
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

        public void CreateNewEntry()
        {
            IMongoCollection<MotorMeasurementsModel> collection = ConnectToMongo<MotorMeasurementsModel>(CollectionName);
        }

    }
}
