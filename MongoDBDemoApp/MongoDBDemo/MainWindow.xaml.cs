using System;
using System.Collections.Generic;
using System.Windows;
using MongoDataAccess.DataAcess;
using MongoDataAccess.Models;
using MongoDB.Bson;

namespace MongoDBDemo
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        ChoreDataAccess db = new ChoreDataAccess();
        TSDataAccess tsda = new TSDataAccess();

        private void btnInsert_Click(object sender, RoutedEventArgs e)
        {
            //await db.CreateUser(new UserModel() { FirstName = "Andres", LastName = "Gaona", data = new List<double>() { 0, 0.1, 0.2, 0.3 } });

            //var unixEpoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
            //var target = DateTime.UtcNow;
            //var diff = target.ToUniversalTime() - unixEpoch;
            //var seconds = (diff.TotalMilliseconds + 18000000) / 1000;
            //var ts = new BsonTimestamp((int)seconds, 1);

            tsda.CreateNewEntry(new MotorMeasurementsModel()
            {
                Position = 10.0,
                Speed = 11.0,
                Current = 12.0,
                MotorDescription = new MotorDescriptionModel() { MotorID = "OSI", VendorID = "YAS" }
            });
        }

        private void btGetUsers_Click(object sender, RoutedEventArgs e)
        {
            //List<UserModel> users = await db.GetAllUsers();
            //ChoreModel chore = new ChoreModel() { AssignedTo = users[0], ChoreText = "Mow the lawn", FrequencyInDays = 7 };
            //await db.CreateChore(chore);
        }

        private void btnCreate_Click(object sender, RoutedEventArgs e)
        {
            tsda.CreateTimeSeriesCollection();
        }
    }
}
