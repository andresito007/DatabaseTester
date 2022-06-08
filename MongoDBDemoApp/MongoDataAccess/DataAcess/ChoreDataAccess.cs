using MongoDataAccess.Models;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MongoDataAccess.DataAcess
{
    public class ChoreDataAccess
    {
        private const string ConnectionString = "mongodb://127.0.0.1:27017";
        private const string DatabaseName = "choredb";
        private const string ChoreCollection = "chore_chart";
        private const string UserCollection = "users";
        private const string ChoreHistoryCollection = "chore_history";

        private IMongoCollection<T> ConnectToMongo<T>(in string collection)
        {
            MongoClient client = new MongoClient(ConnectionString);
            IMongoDatabase db = client.GetDatabase(DatabaseName);
            return db.GetCollection<T>(collection);
        }

        public async Task<List<UserModel>> GetAllUsers()
        {
            IMongoCollection<UserModel> usersCollecton = ConnectToMongo<UserModel>(UserCollection);
            IAsyncCursor<UserModel> results = await usersCollecton.FindAsync(_ => true);
            return results.ToList();
        }

        public async Task<List<ChoreModel>> GetAllChores()
        {
            
            IMongoCollection<ChoreModel> choresCollection = ConnectToMongo<ChoreModel>(ChoreCollection);
            IAsyncCursor<ChoreModel> results = await choresCollection.FindAsync(_ => true);
            return results.ToList();
        }

        public async Task<List<ChoreModel>> GetAllChoresForAUser(UserModel user)
        {
            IMongoCollection<ChoreModel> choresCollecton = ConnectToMongo<ChoreModel>(ChoreCollection);
            IAsyncCursor<ChoreModel> results = await choresCollecton.FindAsync(c => c.AssignedTo.Id == user.Id);
            return results.ToList();
        }

        public Task CreateUser(UserModel user)
        {
            IMongoCollection<UserModel> usersCollecton = ConnectToMongo<UserModel>(UserCollection);
            return usersCollecton.InsertOneAsync(user);
        }

        public Task CreateChore(ChoreModel chore)
        {
            IMongoCollection<ChoreModel> choresCollection = ConnectToMongo<ChoreModel>(ChoreCollection);
            return choresCollection.InsertOneAsync(chore);
        }

        public Task UpdateChore(ChoreModel chore)
        {
            IMongoCollection<ChoreModel> choresCollection = ConnectToMongo<ChoreModel>(ChoreCollection);
            FilterDefinition<ChoreModel> filter = Builders<ChoreModel>.Filter.Eq("Id", chore.Id);
            return choresCollection.ReplaceOneAsync(filter, chore, new ReplaceOptions() { IsUpsert = true });
        }

        public Task DeleteChore(ChoreModel chore)
        {
            IMongoCollection<ChoreModel> choresCollection = ConnectToMongo<ChoreModel>(ChoreCollection);
            return choresCollection.DeleteOneAsync(c => c.Id == chore.Id);
        }

        public async Task CompleteChore(ChoreModel chore)
        {
            IMongoCollection<ChoreModel> choresCollection = ConnectToMongo<ChoreModel>(ChoreCollection);
            FilterDefinition<ChoreModel> filter = Builders<ChoreModel>.Filter.Eq("Id", chore.Id);
            await choresCollection.ReplaceOneAsync(filter, chore);

            IMongoCollection<ChoreHistoryModel> choreHistoryCollection = ConnectToMongo<ChoreHistoryModel>(ChoreHistoryCollection);
            await choreHistoryCollection.InsertOneAsync(new ChoreHistoryModel(chore));
        }

        public void TestTSCollection()
        {
            MongoClient client = new MongoClient(ConnectionString);
            IMongoDatabase db = client.GetDatabase(DatabaseName);
            db.CreateCollectionAsync("serverMetrics",
                new CreateCollectionOptions() 
                { 
                    TimeSeriesOptions = new TimeSeriesOptions
                    (
                        "reportTime", 
                        new Optional<string>("server"), 
                        new Optional<TimeSeriesGranularity?>(TimeSeriesGranularity.Seconds)
                    ),
                }
            );
        }
    }
}
