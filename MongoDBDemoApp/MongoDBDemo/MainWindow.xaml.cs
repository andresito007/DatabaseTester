using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
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
            tsda = new TSDataAccess();
        }

        //private ChoreDataAccess db = new ChoreDataAccess();
        private TSDataAccess tsda;
        private MotorMeasurementModel motorMeasurementModel;
        private CancellationTokenSource cancellationToken;

        private void btnInsert_Click(object sender, RoutedEventArgs e)
        {
            //await db.CreateUser(new UserModel() { FirstName = "Andres", LastName = "Gaona", data = new List<double>() { 0, 0.1, 0.2, 0.3 } });

            //tsda.CreateNewEntry(new MotorMeasurementModel()
            //{
            //    Position = 10.0,
            //    Speed = 11.0,
            //    Current = 12.0,
            //    MotorDescription = new MotorDescriptionModel() { MotorID = "OSI", VendorID = "YAS" }
            //});
        }
        private void btGetUsers_Click(object sender, RoutedEventArgs e)
        {
            //List<UserModel> users = await db.GetAllUsers();
            //ChoreModel chore = new ChoreModel() { AssignedTo = users[0], ChoreText = "Mow the lawn", FrequencyInDays = 7 };
            //await db.CreateChore(chore);

            //tsda.CheckCreated();
        }

        private void btnCreate_Click(object sender, RoutedEventArgs e)
        {
            tsda.CreateTimeSeriesCollection();
        }

        private void btnStop_Click(object sender, RoutedEventArgs e)
        {
            cancellationToken.Cancel();
        }
        
        private void btnStart_Click(object sender, RoutedEventArgs e)
        {
            MotorDescriptionModel motorDescription = new MotorDescriptionModel()
            {
                MotorID = "OSI",
                VendorID = "YAS"
            };

            motorMeasurementModel = new MotorMeasurementModel()
            {
                MotorDescription = motorDescription
            };

            cancellationToken = new CancellationTokenSource();
            CancellationToken token = cancellationToken.Token;

            Task publishTask = new Task(() => PublishTaskProc(token), token);
            publishTask.Start();
        }

        private void PublishTaskProc(CancellationToken token)
        {
            double i = 0;
            while(true)
            {
                Dispatcher.Invoke(() =>
                {
                    tbSample.Text = i.ToString();
                });

                motorMeasurementModel.Position = Math.Sin(i);
                motorMeasurementModel.Speed = Math.Cos(i) * 10;
                motorMeasurementModel.Current = 0.10;
                tsda.CreateNewEntry(motorMeasurementModel);
                i+=0.1;
                
                Thread.Sleep(100);
                if (token.IsCancellationRequested)
                    break;
            }
        }
    }
}
